# The 2025→2026 change model — runner reconstructed and reproduction check (13 Aug 2026)

**What was run.** The GPPS 2025→2026 practice-level change model banked in `PANEL_NOTES.md`
§4.16 (with §4.2 and §4.3) and published as Explorer KEY_FINDING 16 had no saved runner
script — it existed only as prose. `research/scripts/change_model_2526.py` now regenerates it
in one command, on the same footing `predictors_models.py` established for the cross-sectional
page on 15 Jul. No live page or existing data file was modified.

**Two new inputs were downloaded** (NHS England, General Practice Workforce, 31 December 2024
and 31 December 2025 practice-level CSVs), because the derived workforce panel cannot supply a
fully-qualified GP measure at those dates. `build_workforce_dec.py` extracts them.

**Headline: the substantive findings replicate. An earlier version of this note reported that the
telephony coefficients did not; that was an error on my part, corrected in section 2 on 14 Aug.**

---

## 1. What replicates

| Banked in §4.16 | This rerun | Verdict |
|---|---|---|
| Adoption of triage-first intake, −1.8 to −2.3pp | −1.6 (Q32), −2.0 (Q16), −2.5 (Q1) | Replicates |
| Adoption × baseline deflection, +0.75/SD | +0.73 (Q16), +0.89 (Q1), +1.20 (Q7) | Replicates |
| Admin staffing growth, +0.5pp phone ease | +0.43 (Q1), and only on Q1 | Replicates |
| ΔGP small and positive in-year, +0.2–0.3/SD | +0.36 (Q16); +0.37–0.42 on the full sample | Replicates |
| Nurses null | Null on every outcome | Replicates |
| Adoption events, "1,350 surge adopters" | 1,354 | Replicates |

The adoption penalty and the pre-specified interaction survive dropping the baseline-outcome
control, dropping baseline deflection, correcting the workforce source, and moving to the full
~5,978-practice sample. **The core reading of KEY_FINDING 16 stands.**

## 2. The queue-answering finding — retracted correction (updated 14 Aug 2026)

**This section originally reported that §4.16's queue-answering coefficients did not replicate.
That conclusion was wrong, and the banked figures stand.**

The original finding: Δanswering +0.5pp on contact experience. My first rerun got +0.22, not
significant, and I attributed the gap to §4.16 having omitted the baseline-outcome control.

Controlling a difference score for its own baseline is the standard guard against regression to
the mean, but it assumes the baseline is measured without error. A GPPS practice score is a sample
statistic — a few hundred respondents — so it is not. Controlling for a noisy baseline
**over-corrects**: the coefficient absorbs sampling noise as well as real starting level, and any
exposure correlated with the baseline is attenuated with it.

The 2024 wave is an independent noisy measurement of the same underlying practice level, so it
instruments the 2025 baseline — the sampling errors come from different surveys, the true levels
are shared:

| Outcome / exposure | No baseline control | Baseline as measured | Baseline instrumented |
|---|---|---|---|
| Q16 contact / Δanswering | +0.61 | +0.22 ns | **+0.50 (p=0.003)** |
| Q32 overall / Δanswering | +0.43 | +0.12 ns | +0.36 (p=0.026) |
| Q1 phone / ΔIVR fall | +0.78 | +0.39 | +0.54 (p=0.004) |
| Q7 continuity / Δanswering | +0.56 | +0.00 ns | +0.44 ns |

**+0.50 on Q16 is exactly the figure banked in §4.16.** The baseline coefficient itself moves from
−4.84 to −1.28 when instrumented, which is the size of the problem: most of the apparent mean
reversion was sampling noise in the 2025 practice score, not real reversion.

So the uncorrected specification — the one I recommended — was the wrong reading, and §4.16's
"broadest lever" sentence does not need amending. KEY_FINDING 16 stands as published. The IVR
figure is the one that remains short of what was banked: +0.54 per SD fall against +1.00.

Assumption worth stating: the 2024 score affects the 2025→2026 change only through the 2025 level.
Practice-specific trends would violate that. The first stage is strong (t>30) and the direction of
the correction is what classical measurement error predicts, but this is an assumption rather than
a proof.

Reproduced by the `errors_in_variables` pass in `change_model_2526.py`, which needs
`gpps_2024_extra.csv` (Q16 and Q1 2024 columns, extracted from the GPPS 2024 practice file).

## 3. The workforce measure was wrong, and it changes the answer

§4.30 records that `workforce_panel` carries only TOTAL GP FTE — "fully-qualified (EXRL) is
captured only for 2018 (NHS renamed the column)". That is a limitation of the **derived panel,
not of the source**: every quarterly NHSE practice-level detailed CSV carries the full role
breakdown (`TOTAL_GP_EXTG_FTE` = excluding trainee grades = fully qualified;
`TOTAL_GP_EXTGL_FTE` = also excluding locums; every trainee and locum grade separately).

The Dec 2024 and Dec 2025 files have now been downloaded and extracted. This matters more than
a definitional tidy-up, because **the two GP measures move in opposite directions over exactly
this window**:

| FTE per 10,000 patients | Dec 2024 | Dec 2025 | Change |
|---|---|---|---|
| Total GP | 5.855 | 5.775 | **−1.4%** |
| Fully qualified | 4.390 | 4.477 | **+2.0%** |
| FQ excluding locums | 4.298 | 4.387 | +2.1% |
| Nurses | 2.575 | 2.546 | −1.1% |
| Other direct patient care | 2.699 | 2.749 | +1.9% |
| Admin | 11.926 | 11.928 | +0.0% |

Total GP FTE per patient *fell* while fully-qualified GP FTE *rose*. The gap is trainee grades.
Any statement of the form "GP staffing did X in 2025" is therefore undetermined until the
measure is named — and §4.16's "WORKFORCE CORRECTIONS" paragraph, which quotes FQ figures, is
using a different definition from the model term sitting three lines above it.

Decomposing total GP into its two parts, entered together:

| Outcome | ΔFully-qualified | ΔTrainee grades |
|---|---|---|
| Q32 overall | +0.22 ns | +0.02 ns |
| Q16 contact | **+0.36** | +0.02 ns |
| Q1 phone ease | +0.13 ns | +0.05 ns |
| Q7 continuity | +0.15 ns | **+0.65** |

**The continuity association runs entirely through trainee grades, not fully-qualified GPs** —
and it is the larger of the two effects. Using total GP FTE (as the panel forces) blends these
into a single +0.62 on continuity and hides which component carries it. This is counterintuitive
given registrars rotate, and §4.21 found training practices score higher on experience *despite*
slightly lower continuity. It should be interrogated, not banked: growing trainee capacity
plausibly marks practices with the slack and stability to take trainees, rather than trainees
causing continuity.

Correcting the source also **improves coverage**: n rises from 2,762 to 3,015 (CBT sample) and
from 5,527 to 5,978 (all practices), because the raw censuses match more practices than the
panel's alternately-named columns survive.

**Seven-year horizon.** §4.16 banks +0.6pp/SD. Using FQ GP FTE from
`practice_workforce_2019_latest.csv` (the §4.21 split file): +0.20 (Q16), +0.27 (Q1),
**+0.52 (Q7 continuity)**, +0.20 ns (Q32). Only continuity approaches the banked +0.6. Either
§4.16's seven-year figure is a continuity result filed under an experience heading, or it came
from a specification not yet identified — it is not the no-baseline-control one, which pushes
the number *down*.

## 4. A related trap in the panel, now guarded

`workforce_panel.parquet` renames columns between publication vintages. Nurses are `nurse_fte`
for 2018-03…2019-03 and again from 2025-09, but `nurses_fte` across the whole 2019-06…2025-06
stretch. Reading a single name silently yields an **all-null difference** — it does not error,
it drops every practice. A naive Dec 2024 → Dec 2025 nurse delta returns nothing at all. The
script coalesces across names and documents this at the point of use. Anything else built off
that panel with a hard-coded column name is worth re-checking.

## 5. The 2,751-practice sample is selected, and the selection is on the exposure

The constraint is not GPPS — 6,006 practices have usable scores at both waves. It is the CBT
telephony rollout, mid-flight at the 2025 end:

| CBT panel, practices reporting | |
|---|---|
| Mar 2025 | 3,071 |
| May 2025 | 3,114 |
| Mar 2026 | 4,901 |
| May 2026 | 4,957 |

So the §4.16 sample is **the practices that migrated to cloud telephony earliest** — which
tracks ICB procurement waves and practice size, and is itself a form of the operational
modernisation the model is trying to price. The within-practice estimates are not invalidated,
but the national framing in KEY_FINDING 16 is doing unstated work.

The script reports two samples from one build: `CBT` (phone terms in, n≈3,015) and `ALL` (phone
terms dropped, n≈5,978). Adoption, admin, FQ GP and the interaction hold in both.

## 6. New in this rerun

Two outcomes §4.16 did not report are now estimated on the same footing: **Q12 deflection** and
**Q7 continuity**. Adoption of triage-first intake is associated with −2.6pp continuity in the
CBT sample and −2.0pp across all practices — directionally consistent with §4.3's −3.0 and now
significant with the corrected workforce controls. §4.4's routing-dependence caveat applies:
this is a shifted distribution, not a universal effect.

Also: practice size (−0.75/SD on Q32) and deprivation (−0.69/SD) predict *smaller* gains, while
baseline FQ GP staffing predicts *larger* ones (+0.87/SD) — the improvement was not evenly
shared, which cuts against the pro-poor reading in §4.2. That tension needs resolving before the
briefing uses either: §4.2's finding is on unadjusted deltas by IMD quintile, this is adjusted
and conditional on baseline. Both can be true; they answer different questions.

## 7. Suggested next actions

1. No amendment needed to §4.16 or KEY_FINDING 16 on queue answering — see section 2. Worth adding
   to §4.3 that the baseline-outcome control must be instrumented, since the naive version
   understates every exposure correlated with the baseline.
2. Amend §4.30: the FQ limitation belongs to the panel, not the data. Consider rebuilding
   `workforce_panel` from the raw quarterly censuses so the FQ/trainee split is available
   throughout, rather than patching per-analysis.
3. Interrogate the trainee–continuity result before it goes anywhere near a briefing.
4. Resolve the §4.2 pro-poor vs adjusted-gradient tension.

**Files.** `research/scripts/change_model_2526.py` (runner),
`research/scripts/build_workforce_dec.py` (workforce extract),
`research/data/workforce_dec24_dec25.csv`, `data/GPWPracticeCSV.122024.zip`,
`data/GPWPracticeCSV.122025.zip`, `change_2025_2026_rerun.csv` (tidy coefficients, 233 rows,
all samples incl. the sensitivity ladder), `change_2025_2026_rerun_practice.csv`, this document.

*Caveat carried from §4.3: adoption is selected by struggle and parallel trends are violated,
so every adoption coefficient here is an upper bound on causal harm, not an estimate of it.*

**Sources.** [General Practice Workforce, 31 December 2024](https://digital.nhs.uk/data-and-information/publications/statistical/general-and-personal-medical-services/31-december-2024) ·
[General Practice Workforce, 31 December 2025](https://digital.nhs.uk/data-and-information/publications/statistical/general-and-personal-medical-services/31-december-2025)
