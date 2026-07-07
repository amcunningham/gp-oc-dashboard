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
    if (request.method !== "POST")
      return new Response("POST only", { status: 405, headers: cors });

    if ((env.DEMO_ENABLED || "true") !== "true")
      return json({ error: "The shared demo is currently switched off. You can still use your own API key or a local model." }, 503, cors);

    if (origin !== allowed && !origin.startsWith("http://localhost"))
      return json({ error: "Origin not allowed." }, 403, cors);

    // ---- rate limits (KV counters; coarse but adequate for a demo) ----
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const hour = new Date().toISOString().slice(0, 13);
    const day = hour.slice(0, 10);
    const ipKey = `rate:${ip}:${hour}`;
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
      model: env.MODEL || "claude-haiku-4-5-20251001",
      max_tokens: Math.min(body.max_tokens || 700, 1200),
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
      const ipHash = await sha256(ip + day);        // rotates daily; no raw IPs stored
      const entry = {
        t: new Date().toISOString(),
        who: ipHash.slice(0, 12),
        kind: payload.system.startsWith("You translate") ? "sql"
            : payload.system.startsWith("You are helping") ? "interpret"
            : "notes",
        q: (userMsg ? userMsg.content : "").slice(0, 2000),
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
