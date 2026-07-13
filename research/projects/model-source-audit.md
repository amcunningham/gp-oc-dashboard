# Model & data-source currency audit — session brief

_Goal: from scratch, review every model we've produced and confirm each is built on the MOST UP-TO-DATE
published source. Output an audit + action list. Do NOT rebuild everything or switch the live pages over
(that's the 30 July rebuild); this session diagnoses and recommends. Created 13 Jul 2026._

## What to audit

The models / analytical artefacts and the cross-section under them:
- Cross-section `data/xsec_master_2026.{csv,parquet}` (the feature table every model reads) + its rebuild
  `data/xsec_master_rebuilt.csv` and `scripts/build_xsec_full.py` / `XSEC_REBUILD_PROPOSAL.md`.
- Predictor models: `predictors.html`, PANEL_NOTES §4.22-4.23 (Q32/Q16/Q1 cross-sectional), §4.21 training, §4.31 GP composition.
- `scripts/did_anima.py` (Anima/Continuum DiD), `scripts/f2f_increasers.py`, `scripts/ingest_gpps2026.py`.
- The triage substitution study (`projects/triage-substitution-study.md`) and FFT layer.

## Per source: is it the latest?

For each input, check the version we use vs the latest NHSE/OHID publication (fetch the publication page,
compare release date/period). Build a table: **source | file we use | our version/date | latest available | current? | action.**

- **GPPS** — should be 2026 (latest). Confirm models use `*_2026` cols, not 2025.
- **QOF disease prevalence** — `qof_prevalence_2425` = 2024/25 (latest, pulled 13 Jul). Confirm models use it, not just `dm_prev`.
- **CVDPREVENT** — `cvdprevent_practice` = to Dec 2025 (pulled 13 Jul). New; check if any model should use it.
- **Workforce (NWRS)** — `workforce_panel` to 2026. **KNOWN BUG:** live xsec `gp_fte`/`dpc_fte`/`admin_fte` are
  2x too high (summed total + component rows; §4.17/§4.33). Verify the model per-10k figures and FIX (halve / use corrected panel).
- **NHS Payments** — `xsec_ext_payments2425` + `practice_weighted_list` = 2024/25 (latest annual). OK.
- **Registration / list size** — see PROJECTS.md provenance note: 4 flavours, all NHSE. Confirm models use ONE
  consistent denominator (canonical = "Patients Registered at a GP Practice"); flag any per-capita metric mixing sources.
- **IMD** — check we're on the latest English IMD (2019 was latest; verify no newer release).
- **GPAD / OC / CBT** — panels to ~May 2026 / Mar 2026 / May 2026. Confirm no staler extract is silently in use
  (the §4.25 corrupt/truncated `panel_merged.CSV` incident: build reads the parquet, not the stale CSV).
- **Prescribing (NHSBSA EPD)** — `abx_per1k`, `statins_per1k`, `items_per_pt`: not yet source-reproducible
  (XSEC_REBUILD_PROPOSAL §157). Check currency / flag.
- **Fingertips** — `xsec_ext_fingertips2425` = 2024/25; `fingertips_cancer_emergency_practice` = 2024/25. OK.
- **ODS epraccur** — closure/merger flags (`closure_exposed`, `merger_recipient`) need epraccur derivation (not yet reproducible).

## Known issues to resolve or confirm

1. **Workforce doubling (2x)** — the single most important correctness bug; verify + fix in the model inputs.
2. **xsec_master vs xsec_master_rebuilt** — rebuilt recovers 126 spuriously-dropped practices and reproduces
   72/98 cols exactly (corr 1.0); 26 cols need external re-linkage. Decide whether models should move to the rebuilt cross-section.
3. **List-size denominator** — confirm one consistent source across all per-capita/per-10k metrics.
4. **New sources not yet integrated** — QOF 21-register prevalence, CVDPREVENT, weighted list, age/sex are in `data/`
   but may not be in the models. Flag which models should ingest them.

## Deliverable

- The currency/provenance audit table (above).
- A short findings note: what's stale, what's buggy (workforce), what's inconsistent (denominators), what's new-but-unused.
- A recommendation: the ordered fix list (what to update before the models are re-run at the 30 July rebuild),
  and whether to switch models onto `xsec_master_rebuilt`.

## Method / hazards

- Verify "latest version" by fetching the NHSE/OHID publication page (WebFetch) and comparing period/release date —
  do not assume. Search-first for anything post-May-2025.
- OneDrive truncation: check on-disk byte counts vs `git show HEAD:...` before trusting a repo-file read.
- Git index null-sha1: `git read-tree HEAD` then re-add; set `git config user.email` to commit.
- Do NOT re-run the models or edit the live pages/explorer in this session — audit + recommend only.
