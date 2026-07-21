# Auto-refresh pipeline

Automatically refresh the dashboard when new open NHS data is published — with a **human
Pull-Request review gate** before anything reaches the public site.

## Why it's shaped this way

The hard part isn't scheduling; it's two things:

1. **Discovery.** NHS England / NHS Digital publish at opaque, non-templatable URLs
   (`files.digital.nhs.uk/BC/A65BD0/Practice_Level_Crosstab_Feb_26.zip`; FFT filenames that
   change format month to month). You can't construct next month's URL — you must read the
   publication page and extract it. That's what the **resolvers** do.
2. **Safe publishing.** This feeds a public tool that names practices, and `PANEL_NOTES`
   records real incidents an unattended run would otherwise ship silently (the corrupt CSV
   that dropped 96 practices; the workforce ×2 doubling). So nothing publishes unless the
   **validation gates** pass, and even then it lands as a **PR you review and merge**, not a
   direct push.

## How it runs

`.github/workflows/data-refresh.yml` (GitHub Actions, free for public repos, no server):

```
cron (23rd–31st, daily)  ->  refresh.py
  resolve latest edition  ->  compare to data_manifest.json
    if new:  download  ->  aggregate (scripts/agg_duck2.py)  ->  validation gates
      all pass  ->  update manifest + write PR body  ->  Actions opens a PR
      any fail  ->  run goes red, you get notified, NO PR
  merge the PR  ->  GitHub Pages redeploys
```

The job is cheap: on days when nothing new is out it exits in seconds.

## Files

| File | Role |
|---|---|
| `data_manifest.json` | State of record: latest ingested period per source + expected-count bands for the gates. **Set `latest_period` to the true current value before first use.** |
| `resolvers.py` | One function per source that finds the latest published file URL. GPAD wired; others follow the same shape. Each honours a `<NAME>_OVERRIDE_URL` env fallback. |
| `validate.py` | The safety gates (row counts, months-per-release, practice-count band, no negatives, component ≤ total). Fails the run on any breach. |
| `refresh.py` | Orchestrator. `python research/pipeline/refresh.py --source gpad`. |

## Before the first live run — checklist

1. Confirm `data_manifest.json` → `gpad.latest_period` is your true current release (so the
   pipeline fires only on the *next* one).
2. **Verify the resolver against the live page** once: `GPAD_OVERRIDE_URL="" python research/pipeline/refresh.py --source gpad`
   locally, or trigger the workflow manually (Actions → data-refresh → Run workflow) and read
   the log. The scraping selectors in `resolvers.py` are marked `VERIFY`.
3. Sanity-check the `expected_practices_min/max` band against a recent release.
4. Merge this scaffold, then let the manual run open a test PR so you can see the gate report.

## What phase 1 does and doesn't do

**Does:** proves the whole spine for one source end to end — schedule, discover, download,
aggregate with your own code, gate, and open a reviewable PR containing the new per-release
aggregate + manifest bump.

**Doesn't yet:** merge the new months into `panel_merged` and rebuild the cross-section that
the live pages read. That integration point is marked clearly in `refresh.py` — wire your
existing `build_xsec_full.py` there when ready, and add the cross-section gates noted at the
bottom of `validate.py` (national GPPS reproduces to ~0.05pp; workforce not ×2; no silent
practice drop).

## Adding a source

Write `resolve_<name>(publication_url)` in `resolvers.py` (returns
`{"period","label","url"}`), add a `data_manifest.json` entry with its expected-count band,
add a `validate_<name>_release(...)`, and give it a step in the workflow (or generalise
`refresh.py` to loop over `--source all`). CBT, OC submissions, workforce and FFT are the
next four and all share the GPAD shape.

## Note on secrets and data storage

- **No secrets needed** for the data leg — every source is open data. (The explorer's
  Anthropic key stays in the Cloudflare Worker, untouched by this.)
- Phase 1 keeps committing compact derived data to the repo, as now. If history growth becomes
  a concern, switch the pages' data URLs to versioned **GitHub Release assets** — an isolated
  change that keeps `main` lean. Decide later; not needed to prove the spine.
- The cross-section rebuild currently backfills geography from `adoption_risk_2027.csv`, which
  now lives in gitignored `drafts/` and so is **not** on a CI runner. Rather than smuggle it
  into Actions, this is the nudge to finish source-reproducibility — pull ODS epraccur and
  NHSBSA EPD from source (already on the 30-July list) — which removes the dependency.
