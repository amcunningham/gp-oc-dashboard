# Shared-demo proxy — setup (about 10 minutes, all free tier)

The Worker lets visitors use the explorer on your Anthropic key, safely: the key never leaves
Cloudflare, requests only work from your site, each visitor gets 20 questions/hour, the whole
demo is capped at 500 questions/day (≈ £1–2/day worst case on Haiku), and every question is
logged (anonymised) for you to review.

## One-time setup

1. **Create a Cloudflare account** (free): https://dash.cloudflare.com/sign-up

2. **Create the Worker.** Dashboard → Workers & Pages → Create → Worker.
   Name it `gp-explorer-demo`. Replace the default code with the contents of `worker.js`
   (paste into the online editor) and Deploy.

3. **Add the KV store** (for logs and rate counters). Workers & Pages → KV →
   Create namespace, name `gp-explorer-logs`. Then in your Worker → Settings → Bindings →
   Add binding → KV namespace: variable name `LOGS`, select the namespace.

4. **Add your API key as a secret.** Worker → Settings → Variables and Secrets →
   Add → type Secret, name `ANTHROPIC_API_KEY`, paste your key.
   (Tip: create a *separate* key for the demo at console.anthropic.com and set a monthly
   spend limit on the account, so the blast radius is bounded whatever happens.)

4b. **Add a log salt as a secret** (recommended). Same place: type Secret, name `LOG_SALT`,
   value = a long random string (30+ characters; you never need it again). This is mixed into
   the daily visitor hash so a log code cannot be recomputed by someone who knows an IP
   address — making the logs effectively anonymous rather than pseudonymous. The Worker runs
   fine without it; on the day you add it, hourly rate counters simply start fresh.

5. **Optional variables** (Settings → Variables, type Plaintext):
   `ALLOWED_ORIGIN` = https://amcunningham.github.io (default already)
   `PER_IP_HOURLY` = 20 · `GLOBAL_DAILY` = 500 · `DEMO_ENABLED` = true

6. **Note your Worker URL** — it looks like
   `https://gp-explorer-demo.<your-subdomain>.workers.dev`
   Put it into `explore.html` in the `DEMO_PROXY_URL` constant near the top of the script,
   then commit and push.

## Switching the demo on and off

Set `DEMO_ENABLED` to `false` in the Worker's variables (takes effect immediately, no
redeploy). Visitors then see a polite message and can still use their own key or Ollama.

## Exporting the whole question log

Add one more secret to the Worker: name `LOG_TOKEN`, value = a passphrase you invent (long and
random-ish). Then the full log downloads as a CSV from:

`https://gp-explorer-demo.<your-subdomain>.workers.dev/logs?token=YOURPASSPHRASE`

Columns: time, visitor (daily-rotating hash), kind (sql / interpret / notes), ok, question.
Anyone without the token gets a 404, and the export stays off entirely until LOG_TOKEN is set.
Treat the URL like a password — don't share it or leave it in browser history on shared machines.

## Reading the question log

Worker → your KV namespace → "KV pairs": entries are keyed `log:<timestamp>:<visitor-hash>`,
each a JSON record `{t, who, kind (sql|interpret|notes), q, ok}`. Visitor hashes rotate daily
and no raw IPs are stored. Entries expire after 30 days.
For a quick export: Workers dashboard → your namespace → the API tab shows a curl command,
or just page through in the UI — a few hours of demo will be a few hundred entries at most.

## Costs and safety notes

- Haiku pricing means a typical question (2 calls: SQL + interpretation) costs well under 1p;
  the 500/day cap bounds the worst case around £1–2/day.
- The Worker only forwards to Anthropic's messages endpoint with your chosen model — visitors
  cannot pick an expensive model or use the key elsewhere.
- The page shows a "questions are logged" notice whenever shared-demo mode is selected.
