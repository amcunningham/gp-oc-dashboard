# Workforce panel rebuilt from raw NHSE censuses (13 Aug 2026)

**What was done.** `workforce_panel.{csv,parquet}` carried only TOTAL GP FTE and had a nurse
column that changed name between vintages (§4.30, and the trap logged in
`change_model_2526.py`). Neither limitation is in the source data. The panel has been rebuilt
from the raw NHSE practice-level censuses, carrying the fully-qualified / trainee GP split
across the whole series. Output: `research/data/workforce_panel_rebuilt.{csv,parquet}`, built by
`research/scripts/build_workforce_panel.py` from 26 downloaded publication zips.

**The old panel is not modified.** The rebuild is additive, following the `xsec_master_rebuilt`
precedent.

---

## 1. What the rebuild gives you

| | Old panel | Rebuilt |
|---|---|---|
| Periods | 32 (2018-03 … 2026-03) | **41 (2015-09 … 2026-03)** |
| Practice-periods | — | 276,354 |
| GP measures | total FTE only | total, **fully qualified**, **trainee grades**, FQ-excluding-locums, locum |
| Nurse column | `nurse_fte` *or* `nurses_fte` by vintage | both populated, identical values |
| Per-10k series | GP only | GP, FQ, trainee, nurse, DPC, admin |
| Provenance | — | `fq_source`, `pub_vintage` per row |

Every old column name is preserved and populated, so existing code can point at the rebuild
unchanged.

## 2. The vintage bridge (why this isn't a two-line extract)

NHSE renamed the GP columns partway through the series, and the two names are **not the same
measure**:

- 2015–2019 vintage: `TOTAL_GP_EXR_FTE` excludes **registrars only**
- 2020–2026 vintage: `TOTAL_GP_EXTG_FTE` excludes **all trainee grades** (registrars *and* F1/F2)

Reading `EXR` as though it were `EXTG` would silently leave foundation doctors inside the
"fully qualified" count for the early years. The rebuild instead derives fully-qualified on the
old vintage as `TOTAL_GP_FTE − REG_ST1_4 − REG_F1_2`, reproducing the EXTG definition. The
`fq_source` column records which route each row took.

Note also: the alternating `nurse_fte`/`nurses_fte` names were introduced by the **old derived
panel**, not by NHSE. The raw files call it `TOTAL_NURSES_FTE` in every vintage.

## 3. A series break the old panel could not survive — and the rebuild does

Validating per-period national totals against the old panel: **2021-06 onward matches exactly
(0.0% on total GP FTE, every quarter).** Before that the two diverge, by up to 15.5% at 2018-06.

The cause is a real break in the source, visible in the trainee share:

| Period | Total GP FTE | Fully qualified | Trainee | Trainee % |
|---|---|---|---|---|
| 2017-12 | 30,171 | 28,631 | 1,540 | 5.1% |
| 2018-03 | 29,993 | 28,518 | 1,475 | 4.9% |
| **2018-06** | **32,535** | **28,272** | **4,264** | **13.1%** |
| 2018-09 | 33,022 | 27,999 | 5,023 | 15.2% |
| 2019-12 | 33,364 | 27,856 | 5,507 | 16.5% |
| 2025-12 | 36,896 | 28,607 | 8,289 | 22.5% |

Trainee FTE nearly triples between March and June 2018 — a coverage/definition change, not real
recruitment. **The total-GP series breaks there; the fully-qualified series does not** (28,518 →
28,272, −0.9% across the break).

This is the strongest argument for the rebuild: the old panel's only GP column was the one that
breaks. Anything using panel `gp_fte` across 2018 is reading a discontinuity as a trend. The FQ
series is continuous from 2015 to 2026 and shows the familiar shape — fully-qualified GPs
roughly flat around 27,000–28,800 for a decade while trainees grew from 5% to 25% of the total.

**Guidance:** for anything spanning 2018, use `gp_fte_fq`. Treat `gp_fte` before 2018-06 as not
comparable with later values.

## 4. Validation

- **Against NHSE's published headline (Dec 2025):** NHSE reports 28,777 FTE fully qualified GPs,
  +2.1% on Dec 2024. The rebuild gives 28,607 (−0.6% below the headline) and **+2.2% year on
  year** — the level sits slightly low because practice-level files exclude staff not allocated
  to a practice and NHSE's national figure includes estimates for non-responders, but the
  *change*, which is what the models use, reproduces.
- **Against the old panel:** exact match on total GP FTE for every quarter from 2021-06.
- **Against `workforce_dec24_dec25.csv`:** max absolute difference 0.0000000000 on FQ per 10k at
  both censuses.
- **No all-null quarters** for any of FQ, nurse, DPC or admin — the failure mode that made the
  old panel's nurse delta silently empty cannot recur.

## 5. A bug this surfaced in the interim script

`build_workforce_dec.py` (written earlier the same day) used `groupby().sum(numeric_only=True)`,
which returns **0.0 for an all-missing group** rather than NaN. That silently converted "this
practice did not report nurse FTE" into "this practice has no nurses", inflating the change
model's sample from 2,762 to 3,015 (CBT) and 5,527 to 5,978 (all practices) with fabricated
zeros. Fixed with `min_count=1`; the panel build uses `min_count=1` throughout. **The lower
sample sizes are the correct ones** — the earlier run in the change-model note overstated
coverage. Roughly 350 practices per census genuinely do not report nurse FTE.

## 6. Effect on the change model

`change_model_2526.py` now reads the rebuilt panel as its single workforce source, and the
seven-year horizon uses **the same FQ definition at both ends** (Dec 2018 → Dec 2025, a true
seven years) instead of splicing two files:

| Outcome | 7-year ΔFQ GP per 10k |
|---|---|
| Q32 overall | +0.22 |
| Q16 contact | +0.27 |
| Q1 phone ease | +0.35 |
| Q7 continuity | +0.16 ns |

§4.16 banks +0.6/SD. On a consistent definition it is +0.22 to +0.35 — so the banked figure
still does not reproduce, and the earlier hypothesis that it was a mis-filed continuity result
now looks less likely too, since continuity is the one outcome that goes non-significant here.
That number needs tracing to its original run.

In-year terms are essentially unchanged from the corrected run: ΔFQ GP +0.39 (Q16), Δtrainee
+0.85 on continuity, adoption −1.6 to −2.7, interaction +0.87 to +1.02.

## 7. Coverage gaps

Two quarters in the old panel could not be re-downloaded: **2018-06 and 2019-06** (the archive
pages 403'd). They are present in the rebuild anyway, recovered from the cumulative Dec 2019 and
Dec 2021 archives, which republish the full back-series. Nothing in the old panel's coverage is
lost. Two source files were skipped as genuinely GP-only (no nurse/DPC/admin columns at all):
Dec 2016 and Jun 2017 in the Dec 2019 archive — both periods are covered from other editions.

Where a practice-period appears in more than one edition (313,338 rows do, because several
editions ship cumulative back-series), the rebuild keeps the **most recently published** value,
since NHSE revises between editions. `pub_vintage` records which edition each row came from.

## 8. Suggested next actions

1. Repoint `build_xsec_full.py` and `pipeline/validate.py` at the rebuilt panel and confirm
   `xsec` is unchanged where it should be.
2. Amend §4.30: the FQ limitation was the panel's, not the data's; add the 2018-06 total-GP
   series break, which is not currently documented anywhere.
3. Consider whether any past finding used panel `gp_fte` across 2018. The §4.16 seven-year GP
   figure is the obvious candidate.

**Files.** `research/scripts/build_workforce_panel.py`,
`research/data/workforce_panel_rebuilt.parquet`, `research/scripts/gpw_sources.txt` (the 26 source URLs; the 61MB CSV is not committed -- regenerate with the script),
this document.

**Sources.** [General Practice Workforce (current series)](https://digital.nhs.uk/data-and-information/publications/statistical/general-and-personal-medical-services) ·
[General Practice Workforce archive](https://digital.nhs.uk/data-and-information/publications/statistical/general-practice-workforce-archive) ·
[31 December 2025 edition](https://digital.nhs.uk/data-and-information/publications/statistical/general-and-personal-medical-services/31-december-2025)
