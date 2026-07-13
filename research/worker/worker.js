/**
 * GP Access Explorer — shared-demo proxy.
 * Sits between explore.html and the Anthropic API so visitors can try the tool
 * without their own key. Holds the API key server-side, restricts to the
 * explorer's origin, rate-limits per visitor and globally, and logs questions.
 *
 * Deploy: Cloudflare Workers (free tier). See SETUP.md alongside this file.
 * Bindings required:
 *   - secret  ANTHROPIC_API_KEY   (wrangler secret put ANTHROPIC_API_KEY)
 *   - KV      LOGS                (for question logging and rate counters)
 *   - secret  LOG_SALT            (recommended: long random string mixed into the visitor
 *                                  hash so log codes cannot be recomputed from an IP;
 *                                  works without it, but codes are then only pseudonymous)
 * Optional environment variables (defaults shown):
 *   - ALLOWED_ORIGIN  https://amcunningham.github.io
 *   - MODEL           claude-haiku-4-5-20251001
 *   - PER_IP_HOURLY   20
 *   - GLOBAL_DAILY    500
 *   - DEMO_ENABLED    "true"   (set to "false" to switch the demo off without redeploying)
 */

const CORS = (origin) => ({
  "Access-Control-Allow-Origin": origin,
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "content-type",
});

export default {
  async fetch(request, env) {
    const allowed = env.ALLOWED_ORIGIN || "https://amcunningham.github.io";
    const origin = request.headers.get("Origin") || "";
    const cors = CORS(origin === allowed || origin.startsWith("http://localhost") ? origin : allowed);

    if (request.method === "OPTIONS") return new Response(null, { headers: cors });

    // ---- private log export: GET /logs?token=... (set secret LOG_TOKEN to enable) ----
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/logs") {
      if (!env.LOG_TOKEN || url.searchParams.get("token") !== env.LOG_TOKEN)
        return new Response("Not found", { status: 404 });
      const clean = s => '"' + String(s || "").replace(/"/g, '""').replace(/\r?\n/g, " ") + '"';
      const rows = [["time", "visitor", "kind", "ok", "question", "answer", "verdict", "comment"]];
      for (const prefix of ["log:", "fb:"]) {
        let cursor;
        do {
          const page = await env.LOGS.list({ prefix, cursor });
          for (const k of page.keys) {
            const v = await env.LOGS.get(k.name);
            if (!v) continue;
            try {
              const e = JSON.parse(v);
              rows.push(prefix === "log:"
                ? [e.t, e.who, e.kind, e.ok, clean(String(e.q).replace(/^Question:\s*/i, "")), clean(e.a), "", ""]
                : [e.t, e.who, e.kind || "feedback", "", clean(e.q), "", e.verdict, clean(e.comment)]);
            } catch {}
          }
          cursor = page.list_complete ? null : page.cursor;
        } while (cursor);
      }
      return new Response(rows.map(r => r.join(",")).join("\n"), {
        headers: { "content-type": "text/csv; charset=utf-8",
                   "content-disposition": "attachment; filename=gp-explorer-questions.csv" },
      });
    }

    if (request.method !== "POST")
      return new Response("POST only", { status: 405, headers: cors });

    // ---- feedback: POST /feedback {verdict, comment, question, kind} ----
    if (url.pathname === "/feedback") {
      if (origin !== allowed && !origin.startsWith("http://localhost"))
        return json({ error: "Origin not allowed." }, 403, cors);
      const ip = request.headers.get("CF-Connecting-IP") || "unknown";
      const day = new Date().toISOString().slice(0, 10);
      const who = (await sha256(ip + day + (env.LOG_SALT || ""))).slice(0, 12);
      const fbKey = `ratefb:${who}:${day}`;
      const n = parseInt(await env.LOGS.get(fbKey) || "0");
      if (n >= 20) return json({ error: "Feedback limit reached for today." }, 429, cors);
      await env.LOGS.put(fbKey, String(n + 1), { expirationTtl: 90000 });
      let b;
      try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400, cors); }
      const entry = {
        t: new Date().toISOString(), who,
        verdict: b.verdict === "up" ? "up" : "down",
        comment: String(b.comment || "").slice(0, 1000),
        q: String(b.question || "").slice(0, 500),
        kind: String(b.kind || "").slice(0, 20),
      };
      await env.LOGS.put(`fb:${entry.t}:${who}`, JSON.stringify(entry), { expirationTtl: 60 * 60 * 24 * 90 });
      return json({ ok: true }, 200, cors);
    }

    if ((env.DEMO_ENABLED || "true") !== "true")
      return json({ error: "The shared demo is currently switched off. You can still use your own API key or a local model." }, 503, cors);

    if (origin !== allowed && !origin.startsWith("http://localhost"))
      return json({ error: "Origin not allowed." }, 403, cors);

    // ---- rate limits (KV counters; coarse but adequate for a demo) ----
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const hour = new Date().toISOString().slice(0, 13);
    const day = hour.slice(0, 10);
    const ipDayHash = (await sha256(ip + day + (env.LOG_SALT || ""))).slice(0, 12); // no raw IPs stored; salted so codes can't be recomputed from an IP
    const ipKey = `rate:${ipDayHash}:${hour}`;
    const dayKey = `rate:global:${day}`;
    const [ipCount, dayCount] = await Promise.all([
      env.LOGS.get(ipKey).then(v => parseInt(v || "0")),
      env.LOGS.get(dayKey).then(v => parseInt(v || "0")),
    ]);
    if (ipCount >= parseInt(env.PER_IP_HOURLY || "20"))
      return json({ error: "Rate limit reached (20 questions/hour on the shared demo). Try later, or use your own API key." }, 429, cors);
    if (dayCount >= parseInt(env.GLOBAL_DAILY || "500"))
      return json({ error: "The shared demo has reached its daily budget. Try tomorrow, or use your own API key." }, 429, cors);
    await Promise.all([
      env.LOGS.put(ipKey, String(ipCount + 1), { expirationTtl: 3900 }),
      env.LOGS.put(dayKey, String(dayCount + 1), { expirationTtl: 90000 }),
    ]);

    // ---- forward to Anthropic ----
    let body;
    try { body = await request.json(); } catch { return json({ error: "Bad request" }, 400, cors); }
    const payload = {
      model: body.tier === "smart"
        ? (env.SMART_MODEL || "claude-sonnet-5")
        : (env.MODEL || "claude-haiku-4-5-20251001"),
      max_tokens: Math.min(body.max_tokens || 700, 2000),
      system: String(body.system || "").slice(0, 40000),
      messages: (body.messages || []).slice(-2).map(m => ({
        role: m.role === "assistant" ? "assistant" : "user",
        content: String(m.content).slice(0, 30000),
      })),
    };
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify(payload),
    });
    const data = await r.json();

    // ---- log the question (fire-and-forget; anonymised to IP hash) ----
    try {
      const userMsg = payload.messages.filter(m => m.role === "user").pop();
      const sys = payload.system.trim();
      const entry = {
        t: new Date().toISOString(),
        who: ipDayHash,               // rotates daily; no raw IPs stored
        kind: sys.startsWith("You translate") ? "sql"
            : sys.startsWith("You are helping") ? "interpret"
            : "notes",
        q: (userMsg ? userMsg.content : "").slice(0, 2000),
        a: r.ok ? (data.content || []).map(c => c.text || "").join("").slice(0, 3000) : "",
        ok: r.ok,
      };
      await env.LOGS.put(`log:${entry.t}:${entry.who}`, JSON.stringify(entry), { expirationTtl: 60 * 60 * 24 * 30 });
    } catch (e) { /* logging must never break the request */ }

    return json(data, r.status, cors);
  },
};

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), {
    status, headers: { ...headers, "content-type": "application/json" },
  });
}
async function sha256(s) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, "0")).join("");
}
