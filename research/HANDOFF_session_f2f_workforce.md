# Session handoff — f2f / workforce / closure work (10 Jul 2026)

Companion session to "Same-day GP appointments research". Everything below is STAGED in the
working tree, NOT committed. Some overlaps with what that session already banked in PANEL_NOTES
(§4.12 weighting, closure_exposed ~line 266) — noted inline. Hand this to whichever session owns
the commit so it can absorb cleanly.

## Scripts (research/scripts/)
- ingest_gpps2026.py — GPPS 2026 ingest. Integrity/changelog check (aborts if Q32/Q7/Q12/practice-code
  renamed); sentinel clean (<0 -> null); extracts QSET; prints RESPONDENT-WEIGHTED national headlines
  (weight = .baseevalw); merges to xsec_master_2026; writes wave3_gpps.csv. Adds *_basew columns
  (satisfaction/continuity/access/phone). NOTE: QSET does NOT yet carry website_easy_2026 / app_easy_2026 /
  deflection_2025 / couldnt_contact_2025 — the parallel session added those post-hoc; fold into QSET before
  re-running so a re-run doesn't drop them.
- did_anima.py — Anima/Continuum adoption DiD, 3 estimators (unadjusted / adjusted / propensity-matched).
- f2f_increasers.py — practices raising f2f vs national tide; nested models with capacity controls; writes
  f2f_increaser_cohort.csv.

## Data written (research/data/)
- xsec_master_2026.{csv,parquet} — 98 cols, incl *_basew (mine) + website/app easy (parallel session). Coherent.
- wave3_gpps.csv — 2024/25/26 satisfaction & continuity panel.
- workforce_panel.{parquet,csv} — per-practice GP/nurse/DPC/admin FTE + patients, 32 quarters 2018-2026
  (7,352 practices). CAVEAT: gp_fte = TOTAL GP FTE (incl registrars/locums); fully-qualified (EXRL) only
  captured for 2018 (NHS renamed the column after 2018). National total GP FTE/10k rose 4.8->6.0, registrar-driven.
- did_anima_results.csv, f2f_increaser_cohort.csv (n=884), gp_f2f_windows.csv (per-practice GP-f2f shares).

## explore.html
- PCN/England GPPS benchmark rows now RESPONDENT-WEIGHTED (SUM(x*gpps_n_2026)/SUM(gpps_n_2026)) instead of a
  plain AVG across practices (which over-weighted small practices, ran a few points high). Structural (M)
  metrics left as AVG. Restored from git first (on-disk copy had been truncated by OneDrive to 48.9KB vs 53.2KB).
- Exact upgrade available: weight each metric by its own *_basew column (now in the data) instead of gpps_n.

## Findings (this session)
1. Anima/Continuum DiD: matched DiD suggested worse satisfaction/access/continuity, BUT parallel-trends FAILS —
   adopters were already declining pre-adoption (satisfaction PRE -1.6 vs POST -0.9; continuity PRE -1.9 vs POST -2.8).
   Honest read: selection on trajectory; no satisfaction harm; continuity may take an incremental hit on an
   already-falling path. Adopter flag (latest-month Continuum) likely misclassifies mixed-supplier practices
   (e.g. Wealden is Accurx) — supplier-field opacity.
2. f2f -> satisfaction: practices raising f2f against the national decline gained more satisfaction; robust to
   Δappts/patient AND ΔGP-FTE/10k (corr(Δf2f, ΔGP-FTE) = -0.01). GP capacity has its own separate +effect.
   Horse race: GP f2f +0.42/SD > other-staff f2f +0.28/SD, both independently significant. Windows = Jan-Feb
   2024 vs Jan-Feb 2026 (GPPS fieldwork-aligned).
3. Two-wave satisfaction model 2025 vs 2026: drivers essentially unchanged (GP FTE +, deprivation -, size -,
   phone-ease dominant); same-day share a non-predictor both years. Continuity +1.5pp nationally (but has-pref
   fell -0.9, so the pool wanting continuity is shrinking).
4. Closure warning-signs event study (gpps_long 2012-2023): exiting practices show a monotone, widening
   satisfaction deficit over their final 3 years (-0.8 -> -2.1pp vs same-year national, p<1e-16). Phone/continuity
   sit above national (small-practice composition) but erode toward exit. Corrects an LLM "no warning signs"
   result caused by a windowing bug. => proposed PANEL_NOTES §4.15 (drafted separately).
5. Weighting reconciliation: practice-mean vs respondent-weighted (already banked by parallel session §4.12).
   Reconciled our figures to Arjus/official exactly (overall 76.7, phone 56.9, website 57.6, app 54.3, pref-HCP 31.2).

## Open / to do
- Fold website_easy/app_easy/deflection_2025/couldnt_contact_2025 into ingest QSET (dedupe the two ingest versions).
- Optional: capture fully-qualified GP FTE (EXRL) post-2018 in workforce_panel (needs column-name mapping).
- Optional: upgrade explorer benchmarks from gpps_n weighting to exact *_basew weighting.
- NOTHING is committed to git. Two sessions editing PANEL_NOTES / ingest / xsec concurrently — coordinate before commit.
