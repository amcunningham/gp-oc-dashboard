# Predictors-page models — rerun and reproduction check (15 Jul 2026)

**What was run.** Every model behind `predictors.html`, rerun twice from repo sources:
once on the live `xsec_master_2026` (a reproduction check against the published page)
and once on `xsec_master_rebuilt` (the validation the source audit recommended:
corrected workforce values, nurse-FTE fix, 126 recovered practices). No live page or
data file was modified. New: `research/scripts/predictors_models.py` regenerates every
table on the page in one command — the page previously had no saved runner script.

**Headline: the page reproduces, and the rebuild barely moves it.**

- Live rerun vs published page: mean |difference| **0.066pp** across 294 coefficients
  (median 0.03, max 0.54). Sample sizes reproduce exactly where the page states them
  (CBT sample n=4,736; F2 admin table matches to 0.1pp) or within ~0.1% (all-practices
  5,918 vs 5,913; validity models 4,556/4,745 vs 4,550/4,722).
- Rebuilt vs live rerun: mean |difference| **0.055pp** (median 0.04, max 0.48). Every
  sign, significance call and substantive reading on the page survives: the deflection
  and continuity terms, the deprivation and size decompositions, the partner/salaried
  contrast, the trainee/training-practice pattern, the locum null, the admin residual,
  and the same-day sign flip. The audit's prediction — standardised coefficients should
  move little on the rebuilt table — is confirmed. n rises to 4,818 (CBT) / 6,039 (all).
- The only rebuilt-run movement worth a note: the **admin × size interaction attenuates**
  (Q16 −0.48 → −0.16; Q1 −0.68 → −0.20). It was already dissolved by the patient-reported
  measures in the published spec (§4.19/§4.20), so no page text rests on it, but the
  30 Jul rebuild should re-quote it from the new run.

**Spec as reconstructed** (no runner script existed; recovered from the page +
NOTES_BATCH_DRAFT §4.15–4.23, §4.31 and calibrated against the published tables):
OLS with HC1 SEs, no survey weights, no region effects; every predictor except the
training flag z-scored within the estimation sample; outcomes GPPS 2026 Q32/Q16/Q1,
practices with `gpps_n_2026` ≥ 30. Phones: CBT May 2026 (≥200 inbound, IVR <95%),
queue-answer = answered/(inbound−IVR) capped at 100; Mon–Wed gap = Wed−Mon core-hours
answer rate; morning IVR tilt = 8–10am IVR share minus all-other-hours (this, not
core-hours-only, reproduces the notes' −4.1pp median tilt and the −0.25 deflection
coefficient). Contacts per appointment = (CBT inbound + OC May)/GPAD appts May,
**sanity-filtered to ≤5** — this filter recovers the published n=4,736 exactly.
Online volume = mean `oc_rate_1k` Feb–Apr 2026. Staffing from `gp_composition_mar25.csv`
(trainees = registrar + foundation FTE; training flag = registrar FTE > 0.25), per-10k
on the xsec 12-month-average list. Calls per 1,000 uses the same list (panel list_size
is null after Mar 2026).

**Residual reconstruction gaps** (consistent across both reruns, so spec archaeology
rather than data drift; none changes a conclusion): the queue-answer coefficients on
Q1 sit ~0.4–0.5 below the page (+8.03 vs +8.54 alone; +6.19 vs +6.65 together) with
matching smaller offsets in the calls-per-1,000/contacts-per-appointment family —
most plausibly a small difference in the original answer-rate construction (callback
handling or the cap) or in the calls denominator; and the "Alone" column here is
computed on the common n=4,736 sample, where the page's alone values for the
patient-reported measures ran fractionally larger (−5.99 vs −6.23 deflection on Q32),
consistent with them having been fit on each variable's own maximal sample. Worth one
look at the original transcript before the 30 Jul rebuild if exact-match matters.

**Files.** `research/scripts/predictors_models.py` (runner; writes a tidy coefficient
CSV per run), this document (full three-way tables below), `predictors_rerun_live.csv`,
`predictors_rerun_rebuilt.csv` (not committed — regenerate with the script).

Columns below: **Page** (published 11 Jul), **Live rerun**, **Rebuilt**, and the two
deltas. ns markers are not carried into this diff; grey/ns status matched throughout
except where coefficients sit at the 0.05 boundary.

## Alone — Q16 contact

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -8.01 | -7.69 | -7.69 | +0.32 | +0.01 |
| See preferred (Q7) | +7.06 | +7.00 | +6.98 | -0.06 | -0.02 |
| Have preferred (Q6) | +2.41 | +2.41 | +2.40 | -0.00 | -0.00 |
| Queue-answer rate | +4.12 | +3.86 | +3.88 | -0.26 | +0.02 |
| IVR share | -3.09 | -3.08 | -3.13 | +0.01 | -0.05 |
| Mon-Wed gap | -0.98 | -1.04 | -1.08 | -0.06 | -0.04 |
| Contacts/appt | -1.25 | -1.12 | -1.14 | +0.13 | -0.02 |
| Calls per 1,000 | +1.08 | +1.14 | +1.15 | +0.06 | +0.02 |
| Online subs per 1,000 | -2.59 | -2.57 | -2.56 | +0.02 | +0.01 |
| Same-day share | -0.77 | -0.76 | -0.77 | +0.01 | -0.01 |
| Size (log list) | -3.35 | -3.22 | -3.27 | +0.13 | -0.05 |
| IMD | -2.44 | -2.37 | -2.38 | +0.07 | -0.01 |
| Partners /10k | +2.60 | +2.40 | +2.38 | -0.20 | -0.02 |
| Salaried /10k | +0.79 | +0.78 | +0.86 | -0.01 | +0.08 |
| Locums /10k | -0.21 | -0.18 | -0.22 | +0.03 | -0.04 |
| Trainees /10k | +1.29 | +1.28 | +1.27 | -0.01 | -0.01 |
| Training practice | +1.06 | +1.00 | +0.98 | -0.06 | -0.02 |
| Nurses /10k | +0.78 | +0.70 | +0.79 | -0.08 | +0.10 |
| Other clin /10k | +1.00 | +0.97 | +0.98 | -0.03 | +0.00 |
| Admin /10k | +0.89 | +0.85 | +0.94 | -0.04 | +0.10 |
| Appts per 1,000 | +1.40 | +1.36 | +1.36 | -0.04 | -0.00 |
| 65+ % | +2.67 | +2.62 | +2.58 | -0.05 | -0.04 |
| Ethnic minority % | -2.53 | -2.49 | -2.50 | +0.04 | -0.01 |
| n | | 4736 | 4818 | | |

## Alone — Q1 phone ease

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -9.38 | -9.01 | -9.02 | +0.37 | -0.01 |
| See preferred (Q7) | +10.94 | +10.85 | +10.88 | -0.09 | +0.03 |
| Have preferred (Q6) | +4.63 | +4.61 | +4.64 | -0.02 | +0.03 |
| Queue-answer rate | +8.54 | +8.03 | +8.07 | -0.51 | +0.05 |
| IVR share | -6.00 | -6.00 | -6.10 | -0.00 | -0.10 |
| Mon-Wed gap | -2.26 | -2.52 | -2.63 | -0.26 | -0.11 |
| Contacts/appt | -1.05 | -0.70 | -0.69 | +0.35 | +0.01 |
| Calls per 1,000 | +3.26 | +3.31 | +3.37 | +0.05 | +0.06 |
| Online subs per 1,000 | -6.45 | -6.41 | -6.40 | +0.04 | +0.01 |
| Same-day share | -1.74 | -1.70 | -1.73 | +0.04 | -0.03 |
| Size (log list) | -8.41 | -8.14 | -8.25 | +0.27 | -0.12 |
| IMD | -1.81 | -1.76 | -1.75 | +0.05 | +0.01 |
| Partners /10k | +3.79 | +3.56 | +3.56 | -0.23 | -0.00 |
| Salaried /10k | -0.17 | -0.13 | +0.04 | +0.04 | +0.18 |
| Locums /10k | +0.47 | +0.42 | +0.37 | -0.05 | -0.06 |
| Trainees /10k | +0.73 | +0.71 | +0.71 | -0.02 | -0.00 |
| Training practice | -3.39 | -3.53 | -3.60 | -0.14 | -0.06 |
| Nurses /10k | +0.14 | +0.11 | +0.34 | -0.03 | +0.23 |
| Other clin /10k | +1.00 | +0.97 | +0.96 | -0.03 | -0.01 |
| Admin /10k | +0.93 | +0.90 | +1.08 | -0.03 | +0.18 |
| Appts per 1,000 | +1.32 | +1.27 | +1.31 | -0.05 | +0.04 |
| 65+ % | +2.52 | +2.47 | +2.41 | -0.05 | -0.05 |
| Ethnic minority % | -1.83 | -1.80 | -1.81 | +0.03 | -0.01 |
| n | | 4736 | 4818 | | |

## Alone — Q32 overall

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -6.23 | -5.99 | -5.98 | +0.24 | +0.00 |
| See preferred (Q7) | +5.81 | +5.76 | +5.75 | -0.05 | -0.01 |
| Have preferred (Q6) | +2.28 | +2.28 | +2.29 | +0.00 | +0.01 |
| Queue-answer rate | +2.82 | +2.65 | +2.67 | -0.17 | +0.02 |
| IVR share | -2.24 | -2.24 | -2.28 | +0.00 | -0.04 |
| Mon-Wed gap | -0.66 | -0.64 | -0.67 | +0.02 | -0.02 |
| Contacts/appt | -1.04 | -0.93 | -0.95 | +0.11 | -0.02 |
| Calls per 1,000 | +1.12 | +1.15 | +1.18 | +0.03 | +0.03 |
| Online subs per 1,000 | -1.91 | -1.89 | -1.88 | +0.02 | +0.01 |
| Same-day share | -0.66 | -0.65 | -0.65 | +0.01 | -0.00 |
| Size (log list) | -2.33 | -2.23 | -2.29 | +0.10 | -0.05 |
| IMD | -2.27 | -2.22 | -2.22 | +0.05 | +0.00 |
| Partners /10k | +2.55 | +2.35 | +2.32 | -0.20 | -0.03 |
| Salaried /10k | +0.93 | +0.92 | +0.98 | -0.01 | +0.06 |
| Locums /10k | -0.30 | -0.26 | -0.28 | +0.04 | -0.02 |
| Trainees /10k | +1.44 | +1.42 | +1.42 | -0.02 | -0.00 |
| Training practice | +1.93 | +1.90 | +1.89 | -0.03 | -0.01 |
| Nurses /10k | +1.00 | +0.90 | +0.95 | -0.10 | +0.06 |
| Other clin /10k | +0.92 | +0.90 | +0.90 | -0.02 | +0.00 |
| Admin /10k | +1.00 | +0.95 | +1.01 | -0.05 | +0.06 |
| Appts per 1,000 | +1.52 | +1.48 | +1.49 | -0.04 | +0.00 |
| 65+ % | +2.95 | +2.91 | +2.87 | -0.04 | -0.04 |
| Ethnic minority % | -2.75 | -2.72 | -2.73 | +0.03 | -0.01 |
| n | | 4736 | 4818 | | |

## Together — Q16 contact

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Queue-answer rate | +3.30 | +3.09 | +3.08 | -0.21 | -0.01 |
| IVR share | -1.69 | -1.67 | -1.72 | +0.02 | -0.05 |
| Mon-Wed gap | +0.05 | +0.04 | +0.02 | -0.01 | -0.02 |
| Contacts/appt | -0.25 | -0.48 | -0.64 | -0.23 | -0.17 |
| Calls per 1,000 | +1.12 | +1.34 | +1.51 | +0.22 | +0.17 |
| Online subs per 1,000 | -1.88 | -1.82 | -1.74 | +0.06 | +0.09 |
| Same-day share | -0.06 | -0.06 | -0.05 | +0.00 | +0.01 |
| Size (log list) | -2.29 | -2.16 | -2.19 | +0.13 | -0.03 |
| IMD | -2.27 | -2.18 | -2.18 | +0.09 | +0.00 |
| Partners /10k | +1.53 | +1.40 | +1.39 | -0.13 | -0.01 |
| Salaried /10k | +1.29 | +1.24 | +1.23 | -0.05 | -0.01 |
| Locums /10k | +0.21 | +0.19 | +0.14 | -0.02 | -0.05 |
| Trainees /10k | +0.09 | +0.17 | +0.17 | +0.08 | -0.00 |
| Training practice | +3.05 | +2.85 | +2.90 | -0.20 | +0.05 |
| Nurses /10k | +0.42 | +0.37 | +0.21 | -0.05 | -0.16 |
| Other clin /10k | +0.50 | +0.48 | +0.54 | -0.02 | +0.05 |
| Admin /10k | -1.15 | -1.13 | -1.09 | +0.02 | +0.04 |
| Appts per 1,000 | +0.67 | +0.51 | +0.33 | -0.16 | -0.18 |
| 65+ % | -0.37 | -0.31 | -0.36 | +0.06 | -0.05 |
| Ethnic minority % | -1.25 | -1.22 | -1.31 | +0.03 | -0.09 |
| Admin x size | -0.53 | -0.48 | -0.16 | +0.05 | +0.33 |
| Admin x online | +0.20 | +0.19 | +0.14 | -0.01 | -0.04 |
| R² | 0.305 | 0.304 | 0.304 | | |
| n | | 4736 | 4818 | | |

## Together — Q1 phone ease

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Queue-answer rate | +6.65 | +6.19 | +6.17 | -0.46 | -0.02 |
| IVR share | -3.39 | -3.33 | -3.41 | +0.06 | -0.07 |
| Mon-Wed gap | -0.10 | -0.15 | -0.20 | -0.05 | -0.05 |
| Contacts/appt | -0.15 | -0.69 | -0.87 | -0.54 | -0.17 |
| Calls per 1,000 | +2.60 | +3.02 | +3.26 | +0.42 | +0.24 |
| Online subs per 1,000 | -4.22 | -4.07 | -3.92 | +0.15 | +0.14 |
| Same-day share | -0.50 | -0.48 | -0.48 | +0.02 | +0.00 |
| Size (log list) | -4.86 | -4.66 | -4.77 | +0.20 | -0.11 |
| IMD | -3.23 | -3.10 | -3.09 | +0.13 | +0.01 |
| Partners /10k | +1.71 | +1.62 | +1.61 | -0.09 | -0.01 |
| Salaried /10k | +1.19 | +1.17 | +1.09 | -0.02 | -0.08 |
| Locums /10k | +0.19 | +0.18 | +0.10 | -0.01 | -0.08 |
| Trainees /10k | -0.00 | +0.10 | +0.11 | +0.10 | +0.00 |
| Training practice | +3.41 | +3.09 | +3.19 | -0.32 | +0.10 |
| Nurses /10k | +0.56 | +0.49 | +0.25 | -0.07 | -0.23 |
| Other clin /10k | +1.07 | +1.02 | +1.10 | -0.05 | +0.07 |
| Admin /10k | -1.47 | -1.44 | -1.38 | +0.03 | +0.06 |
| Appts per 1,000 | +1.06 | +0.68 | +0.48 | -0.38 | -0.20 |
| 65+ % | -1.45 | -1.37 | -1.49 | +0.08 | -0.12 |
| Ethnic minority % | -1.01 | -0.99 | -1.14 | +0.02 | -0.15 |
| Admin x size | -0.73 | -0.68 | -0.20 | +0.05 | +0.48 |
| Admin x online | +0.51 | +0.52 | +0.45 | +0.01 | -0.06 |
| R² | 0.475 | 0.475 | 0.475 | | |
| n | | 4736 | 4818 | | |

## Together — Q32 overall

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Queue-answer rate | +2.36 | +2.21 | +2.21 | -0.15 | -0.00 |
| IVR share | -1.14 | -1.13 | -1.16 | +0.01 | -0.03 |
| Mon-Wed gap | -0.01 | +0.04 | +0.03 | +0.05 | -0.00 |
| Contacts/appt | -0.35 | -0.45 | -0.62 | -0.10 | -0.16 |
| Calls per 1,000 | +1.18 | +1.29 | +1.45 | +0.11 | +0.16 |
| Online subs per 1,000 | -1.32 | -1.30 | -1.23 | +0.02 | +0.07 |
| Same-day share | -0.08 | -0.09 | -0.08 | -0.01 | +0.01 |
| Size (log list) | -1.64 | -1.56 | -1.61 | +0.08 | -0.05 |
| IMD | -1.64 | -1.57 | -1.56 | +0.07 | +0.01 |
| Partners /10k | +1.68 | +1.54 | +1.53 | -0.14 | -0.01 |
| Salaried /10k | +1.42 | +1.37 | +1.43 | -0.05 | +0.06 |
| Locums /10k | +0.28 | +0.25 | +0.23 | -0.03 | -0.02 |
| Trainees /10k | +0.12 | +0.17 | +0.17 | +0.05 | -0.00 |
| Training practice | +2.79 | +2.67 | +2.73 | -0.12 | +0.06 |
| Nurses /10k | +0.28 | +0.24 | +0.15 | -0.04 | -0.10 |
| Other clin /10k | +0.16 | +0.15 | +0.19 | -0.01 | +0.04 |
| Admin /10k | -1.11 | -1.09 | -1.08 | +0.02 | +0.01 |
| Appts per 1,000 | +0.53 | +0.45 | +0.29 | -0.08 | -0.16 |
| 65+ % | +0.36 | +0.40 | +0.34 | +0.04 | -0.06 |
| Ethnic minority % | -1.26 | -1.23 | -1.31 | +0.03 | -0.09 |
| Admin x size | -0.27 | -0.26 | -0.02 | +0.01 | +0.24 |
| Admin x online | -0.03 | -0.03 | -0.06 | +0.00 | -0.03 |
| R² | 0.277 | 0.276 | 0.276 | | |
| n | | 4736 | 4818 | | |

## + patients report — Q16 contact

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -5.94 | -5.70 | -5.70 | +0.24 | -0.00 |
| See preferred (Q7) | +3.37 | +3.35 | +3.34 | -0.02 | -0.01 |
| Have preferred (Q6) | +0.71 | +0.73 | +0.73 | +0.02 | +0.00 |
| Queue-answer rate | +1.78 | +1.66 | +1.64 | -0.12 | -0.02 |
| IVR share | -0.82 | -0.79 | -0.81 | +0.03 | -0.02 |
| Mon-Wed gap | +0.08 | +0.01 | +0.01 | -0.07 | -0.00 |
| Contacts/appt | -0.00 | -0.07 | -0.16 | -0.07 | -0.09 |
| Calls per 1,000 | +1.37 | +1.43 | +1.53 | +0.06 | +0.10 |
| Online subs per 1,000 | -1.55 | -1.51 | -1.44 | +0.04 | +0.07 |
| Same-day share | +0.61 | +0.59 | +0.59 | -0.02 | -0.00 |
| Size (log list) | -0.97 | -0.88 | -0.90 | +0.09 | -0.03 |
| IMD | -0.77 | -0.73 | -0.75 | +0.04 | -0.02 |
| Partners /10k | +0.31 | +0.27 | +0.29 | -0.04 | +0.02 |
| Salaried /10k | +0.71 | +0.68 | +0.72 | -0.03 | +0.03 |
| Locums /10k | +0.05 | +0.04 | +0.03 | -0.01 | -0.01 |
| Trainees /10k | +0.63 | +0.70 | +0.69 | +0.07 | -0.01 |
| Training practice | +1.90 | +1.67 | +1.72 | -0.23 | +0.06 |
| Nurses /10k | +0.31 | +0.27 | +0.23 | -0.04 | -0.04 |
| Other clin /10k | +0.23 | +0.22 | +0.25 | -0.01 | +0.03 |
| Admin /10k | -0.37 | -0.36 | -0.34 | +0.01 | +0.02 |
| Appts per 1,000 | +0.09 | +0.06 | -0.05 | -0.03 | -0.11 |
| 65+ % | -0.42 | -0.38 | -0.44 | +0.04 | -0.07 |
| Ethnic minority % | -0.63 | -0.63 | -0.67 | -0.00 | -0.04 |
| Admin x size | -0.14 | -0.14 | -0.02 | -0.00 | +0.13 |
| Admin x online | +0.14 | +0.14 | +0.12 | -0.00 | -0.02 |
| R² | 0.620 | 0.619 | 0.619 | | |
| n | | 4736 | 4818 | | |

## + patients report — Q1 phone ease

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -6.05 | -5.79 | -5.81 | +0.26 | -0.02 |
| See preferred (Q7) | +4.96 | +4.92 | +4.91 | -0.04 | -0.01 |
| Have preferred (Q6) | +0.49 | +0.50 | +0.52 | +0.01 | +0.02 |
| Queue-answer rate | +4.90 | +4.55 | +4.51 | -0.35 | -0.04 |
| IVR share | -2.41 | -2.36 | -2.39 | +0.05 | -0.04 |
| Mon-Wed gap | -0.04 | -0.16 | -0.20 | -0.12 | -0.04 |
| Contacts/appt | +0.07 | -0.27 | -0.37 | -0.34 | -0.10 |
| Calls per 1,000 | +2.86 | +3.09 | +3.25 | +0.23 | +0.16 |
| Online subs per 1,000 | -3.64 | -3.51 | -3.38 | +0.13 | +0.13 |
| Same-day share | +0.30 | +0.29 | +0.28 | -0.01 | -0.01 |
| Size (log list) | -3.17 | -3.03 | -3.13 | +0.14 | -0.10 |
| IMD | -1.52 | -1.45 | -1.47 | +0.07 | -0.01 |
| Partners /10k | +0.32 | +0.33 | +0.36 | +0.01 | +0.03 |
| Salaried /10k | +0.52 | +0.52 | +0.49 | +0.00 | -0.03 |
| Locums /10k | +0.01 | +0.00 | -0.03 | -0.01 | -0.04 |
| Trainees /10k | +0.70 | +0.79 | +0.79 | +0.09 | +0.00 |
| Training practice | +2.06 | +1.73 | +1.83 | -0.33 | +0.10 |
| Nurses /10k | +0.45 | +0.39 | +0.30 | -0.06 | -0.09 |
| Other clin /10k | +0.72 | +0.68 | +0.74 | -0.04 | +0.05 |
| Admin /10k | -0.56 | -0.55 | -0.51 | +0.01 | +0.04 |
| Appts per 1,000 | +0.42 | +0.20 | +0.06 | -0.22 | -0.14 |
| 65+ % | -1.38 | -1.33 | -1.48 | +0.05 | -0.15 |
| Ethnic minority % | -0.12 | -0.14 | -0.24 | -0.02 | -0.10 |
| Admin x size | -0.25 | -0.25 | -0.01 | -0.00 | +0.24 |
| Admin x online | +0.41 | +0.43 | +0.39 | +0.02 | -0.04 |
| R² | 0.665 | 0.665 | 0.664 | | |
| n | | 4736 | 4818 | | |

## + patients report — Q32 overall

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -4.22 | -4.05 | -4.06 | +0.17 | -0.01 |
| See preferred (Q7) | +2.99 | +2.96 | +2.95 | -0.03 | -0.01 |
| Have preferred (Q6) | +1.24 | +1.25 | +1.26 | +0.01 | +0.01 |
| Queue-answer rate | +1.16 | +1.09 | +1.07 | -0.07 | -0.02 |
| IVR share | -0.48 | -0.47 | -0.48 | +0.01 | -0.00 |
| Mon-Wed gap | -0.01 | -0.01 | -0.00 | +0.00 | +0.01 |
| Contacts/appt | -0.21 | -0.17 | -0.28 | +0.04 | -0.11 |
| Calls per 1,000 | +1.36 | +1.33 | +1.43 | -0.03 | +0.09 |
| Online subs per 1,000 | -0.85 | -0.86 | -0.80 | -0.01 | +0.05 |
| Same-day share | +0.52 | +0.50 | +0.50 | -0.02 | -0.00 |
| Size (log list) | -0.46 | -0.41 | -0.46 | +0.05 | -0.04 |
| IMD | -0.54 | -0.52 | -0.52 | +0.02 | -0.01 |
| Partners /10k | +0.55 | +0.50 | +0.52 | -0.05 | +0.02 |
| Salaried /10k | +0.96 | +0.91 | +1.00 | -0.05 | +0.09 |
| Locums /10k | +0.15 | +0.13 | +0.14 | -0.02 | +0.01 |
| Trainees /10k | +0.65 | +0.69 | +0.68 | +0.04 | -0.01 |
| Training practice | +1.89 | +1.75 | +1.82 | -0.14 | +0.06 |
| Nurses /10k | +0.22 | +0.19 | +0.18 | -0.03 | -0.01 |
| Other clin /10k | -0.03 | -0.03 | -0.02 | -0.00 | +0.02 |
| Admin /10k | -0.45 | -0.43 | -0.43 | +0.02 | -0.00 |
| Appts per 1,000 | +0.06 | +0.10 | -0.00 | +0.04 | -0.10 |
| 65+ % | +0.23 | +0.24 | +0.17 | +0.01 | -0.07 |
| Ethnic minority % | -1.02 | -1.01 | -1.06 | +0.01 | -0.05 |
| Admin x size | +0.04 | +0.02 | +0.11 | -0.02 | +0.09 |
| Admin x online | -0.09 | -0.07 | -0.08 | +0.02 | -0.01 |
| R² | 0.539 | 0.538 | 0.539 | | |
| n | | 4736 | 4818 | | |

## All practices — Q16 contact

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -6.16 | -6.18 | -6.19 | -0.02 | -0.01 |
| See preferred (Q7) | +3.58 | +3.58 | +3.64 | +0.00 | +0.05 |
| Have preferred (Q6) | +0.70 | +0.69 | +0.72 | -0.01 | +0.03 |
| Online subs per 1,000 | -1.97 | -1.97 | -1.90 | +0.00 | +0.07 |
| Same-day share | +0.54 | +0.54 | +0.56 | -0.00 | +0.03 |
| Size (log list) | -1.75 | -1.71 | -1.69 | +0.04 | +0.02 |
| IMD | -0.50 | -0.49 | -0.46 | +0.01 | +0.03 |
| Partners /10k | +0.40 | +0.40 | +0.41 | +0.00 | +0.00 |
| Salaried /10k | +0.78 | +0.78 | +0.78 | -0.00 | -0.00 |
| Locums /10k | +0.04 | +0.03 | +0.00 | -0.01 | -0.03 |
| Trainees /10k | +0.67 | +0.73 | +0.78 | +0.06 | +0.04 |
| Training practice | +1.59 | +1.41 | +1.45 | -0.18 | +0.04 |
| Nurses /10k | +0.31 | +0.31 | +0.28 | +0.00 | -0.03 |
| Other clin /10k | +0.12 | +0.12 | +0.20 | +0.00 | +0.08 |
| Admin /10k | -0.36 | -0.36 | -0.30 | +0.00 | +0.05 |
| Appts per 1,000 | +0.27 | +0.27 | +0.01 | +0.00 | -0.26 |
| 65+ % | -0.20 | -0.19 | -0.15 | +0.01 | +0.04 |
| Ethnic minority % | -0.65 | -0.65 | -0.66 | -0.00 | -0.00 |
| Admin x size | -0.13 | -0.13 | +0.05 | -0.00 | +0.18 |
| Admin x online | -0.11 | -0.11 | -0.13 | +0.00 | -0.02 |
| R² | 0.608 | 0.608 | 0.607 | | |
| n | | 5918 | 6039 | | |

## All practices — Q1 phone ease

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -6.85 | -6.87 | -6.90 | -0.02 | -0.03 |
| See preferred (Q7) | +5.48 | +5.48 | +5.56 | -0.00 | +0.08 |
| Have preferred (Q6) | +0.54 | +0.53 | +0.58 | -0.01 | +0.04 |
| Online subs per 1,000 | -4.35 | -4.34 | -4.22 | +0.01 | +0.12 |
| Same-day share | +0.15 | +0.14 | +0.19 | -0.01 | +0.05 |
| Size (log list) | -5.47 | -5.42 | -5.48 | +0.05 | -0.06 |
| IMD | -1.10 | -1.09 | -1.07 | +0.01 | +0.01 |
| Partners /10k | +0.42 | +0.43 | +0.44 | +0.01 | +0.01 |
| Salaried /10k | +0.59 | +0.59 | +0.51 | -0.00 | -0.08 |
| Locums /10k | +0.08 | +0.05 | +0.06 | -0.03 | +0.00 |
| Trainees /10k | +0.91 | +0.97 | +1.03 | +0.06 | +0.06 |
| Training practice | +1.81 | +1.63 | +1.73 | -0.18 | +0.10 |
| Nurses /10k | +0.27 | +0.27 | +0.25 | -0.00 | -0.02 |
| Other clin /10k | +0.46 | +0.46 | +0.55 | -0.00 | +0.10 |
| Admin /10k | -0.58 | -0.57 | -0.50 | +0.01 | +0.07 |
| Appts per 1,000 | +0.70 | +0.70 | +0.43 | -0.00 | -0.27 |
| 65+ % | -1.37 | -1.36 | -1.38 | +0.01 | -0.02 |
| Ethnic minority % | -0.48 | -0.49 | -0.50 | -0.01 | -0.01 |
| Admin x size | -0.28 | -0.28 | +0.01 | +0.00 | +0.29 |
| Admin x online | +0.05 | +0.05 | +0.02 | +0.00 | -0.03 |
| R² | 0.599 | 0.599 | 0.598 | | |
| n | | 5918 | 6039 | | |

## All practices — Q32 overall

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Told to contact again (Q12) | -4.30 | -4.31 | -4.34 | -0.01 | -0.03 |
| See preferred (Q7) | +3.16 | +3.16 | +3.20 | -0.00 | +0.05 |
| Have preferred (Q6) | +1.23 | +1.22 | +1.27 | -0.01 | +0.04 |
| Online subs per 1,000 | -1.29 | -1.29 | -1.23 | +0.00 | +0.06 |
| Same-day share | +0.47 | +0.47 | +0.51 | -0.00 | +0.04 |
| Size (log list) | -1.08 | -1.06 | -1.03 | +0.02 | +0.03 |
| IMD | -0.32 | -0.31 | -0.26 | +0.01 | +0.04 |
| Partners /10k | +0.62 | +0.62 | +0.60 | +0.00 | -0.02 |
| Salaried /10k | +1.03 | +1.03 | +1.08 | -0.00 | +0.05 |
| Locums /10k | +0.15 | +0.14 | +0.14 | -0.01 | -0.00 |
| Trainees /10k | +0.67 | +0.71 | +0.75 | +0.04 | +0.04 |
| Training practice | +1.77 | +1.66 | +1.73 | -0.11 | +0.07 |
| Nurses /10k | +0.23 | +0.23 | +0.22 | -0.00 | -0.00 |
| Other clin /10k | -0.12 | -0.12 | -0.05 | -0.00 | +0.07 |
| Admin /10k | -0.38 | -0.38 | -0.33 | -0.00 | +0.06 |
| Appts per 1,000 | +0.32 | +0.32 | +0.03 | -0.00 | -0.29 |
| 65+ % | +0.37 | +0.37 | +0.45 | +0.00 | +0.07 |
| Ethnic minority % | -1.02 | -1.03 | -1.02 | -0.01 | +0.01 |
| Admin x size | +0.03 | +0.03 | +0.17 | -0.00 | +0.14 |
| Admin x online | -0.18 | -0.18 | -0.21 | +0.00 | -0.03 |
| R² | 0.535 | 0.534 | 0.533 | | |
| n | | 5918 | 6039 | | |

## Continuity model — Q7 continuity

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Partners /10k | +2.45 | +2.24 | +2.11 | -0.21 | -0.13 |
| Salaried /10k | +1.03 | +1.00 | +0.88 | -0.03 | -0.12 |
| Locums /10k | +0.33 | +0.30 | +0.24 | -0.03 | -0.06 |
| Trainees /10k | -2.07 | -1.98 | -2.00 | +0.09 | -0.02 |
| Training practice | +2.16 | +2.04 | +2.10 | -0.12 | +0.06 |
| R² | 0.233 | 0.230 | 0.233 | | |
| n | | 4791 | 4874 | | |

## Phone-only validity — Couldn’t contact

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Queue-answer rate | -0.17 | -0.17 | -0.17 | +0.00 | -0.00 |
| IVR share | +0.23 | +0.23 | +0.23 | -0.00 | -0.00 |
| R² | 0.049 | 0.048 | 0.048 | | |
| n | | 4556 | 4636 | | |

## Phone-only validity — Q12 deflection

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Queue-answer rate | -0.97 | -0.99 | -0.99 | -0.02 | +0.00 |
| IVR share | +0.99 | +0.97 | +0.98 | -0.02 | +0.01 |
| R² | 0.101 | 0.100 | 0.101 | | |
| n | | 4556 | 4636 | | |

## Phone-only validity — Q1 phone ease

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| Queue-answer rate | +6.53 | +6.58 | +6.58 | +0.05 | +0.01 |
| IVR share | -4.20 | -4.14 | -4.17 | +0.06 | -0.03 |
| R² | 0.370 | 0.369 | 0.375 | | |
| n | | 4556 | 4636 | | |

## External -> deflection — Q12 deflection

| Predictor | Page | Live rerun | Rebuilt | live−page | rebuilt−live |
|---|---:|---:|---:|---:|---:|
| IMD | +1.10 | +1.12 | +1.09 | +0.02 | -0.03 |
| Queue-answer rate | -0.90 | -0.91 | -0.91 | -0.01 | -0.00 |
| IVR share | +0.70 | +0.69 | +0.71 | -0.01 | +0.02 |
| FQ GPs /10k | -0.47 | -0.48 | -0.43 | -0.01 | +0.05 |
| Ethnic minority % | +0.47 | +0.44 | +0.44 | -0.03 | -0.00 |
| Appts per 1,000 | -0.44 | -0.35 | -0.23 | +0.09 | +0.12 |
| Calls per 1,000 | +0.36 | +0.18 | +0.13 | -0.18 | -0.05 |
| Online subs per 1,000 | -0.30 | -0.34 | -0.35 | -0.04 | -0.01 |
| Contacts/appt | +0.29 | +0.40 | +0.48 | +0.11 | +0.08 |
| Same-day share | +0.26 | +0.25 | +0.22 | -0.01 | -0.03 |
| Morning IVR pattern | -0.25 | -0.22 | -0.23 | +0.03 | -0.01 |
| Size (log list) | +0.23 | +0.23 | +0.20 | +0.00 | -0.04 |
| 65+ % | -0.04 | -0.03 | -0.08 | +0.01 | -0.05 |
| R² | 0.210 | 0.207 | 0.204 | | |
| n | | 4745 | 4829 | | |

## Coefficients that moved most

| Model | Outcome | Predictor | Page | Live | Rebuilt |
|---|---|---|---:|---:|---:|
| Alone | Q1 phone ease | Queue-answer rate | +8.54 | +8.03 | +8.07 |
| Together | Q16 contact | Admin x size | -0.53 | -0.48 | -0.16 |
| Together | Q1 phone ease | Queue-answer rate | +6.65 | +6.19 | +6.17 |
| Together | Q1 phone ease | Contacts/appt | -0.15 | -0.69 | -0.87 |
| Together | Q1 phone ease | Calls per 1,000 | +2.60 | +3.02 | +3.26 |
| Together | Q1 phone ease | Admin x size | -0.73 | -0.68 | -0.20 |