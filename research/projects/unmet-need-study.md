# Unmet-need study — project brief (v2, 13 Jul 2026)

_England, public data only. Cohort/relative; NO named-practice case studies. Data assembling; analysis not started._

## Positioning (checked against the literature 13 Jul)

The inverse care law and "deprived practices under-deliver relative to morbidity" are **thoroughly
established** — do NOT re-prove them, and this is NOT a funding formula (that lane is owned). The
contribution is to **measure the unmet-need layers the workload/funding literature assumes, patches, or
structurally cannot see** — the front-door mechanism and non-presentation — using GPPS (which reaches
registered non-attenders) plus the operational access data (deflection, telephony, OC).

### Established baseline (what we EXTEND, not re-prove)

- **McConnachie 2023** (BMJ Open, Scotland): delivered contact time vs LTC count -> deprived under-deliver at every morbidity level; +14% to equalise. Excludes non-attenders.
- **Gopfert 2021** (BJGP, England): consultation length by deprivation x multimorbidity.
- **de Dumast 2026** (BMJ Open): Carr-Hill under-weights morbidity; deprived practices LOSE under morbidity reweighting; residual widens = undermeasured need.
- **Anselmi 2025** (Health Policy): person-based workload formula; practice fixed-effects NEGATIVE in deprived deciles (deliver less than predicted) = supply/access constraint, corrected upward; explicitly zeros negative ethnicity coefficients as "indications of unmet need." Notes practice-level *interactions* aren't publishable nationally.
- **Rolewicz 2020** (BMJ Open): unmet need in multimorbidity using the 2018 GPPS.

**Common thread:** all measure workload/consultations = *met* demand; all find deprived under-delivery; all
handle the unmet/non-presentation problem crudely (exclude non-attenders; zero-out coefficients; interpret
the residual as supply). None measure the mechanism, and none the non-presentation. That is the open lane.

## The cascade (the design)

Treat the access journey as a multi-outcome cascade, each stage a GPPS item, each read by deprivation x
functional need:

1. **Present?** Q8 `gpcontactwhen` / Q17 `lastgpapptlengthgap` (incl. "never since registering") — the
   non-presentation layer only a population survey can see (admin data excludes non-attenders).
2. **Deflected?** Q12 `gpcontactnextstep`. [§4.18.1 owns this: deflection is need-targeted — worst for
   learning disability/autism/mental health, stacking with deprivation.]
3. **Diverted?** Q14 (pharmacy/111/UEC). [§4.18.1: diversion is need-NEUTRAL — appropriate signposting.]
4. **Needs met?** Q31 `lastgpapptneeds`.

Read as a CONDITIONAL cascade: each stage is among those who survived the last, so losses compound and hide
each other (lost early -> invisible later). That compounding IS the candidacy story, and why the admin
papers (which start at stage 2+) understate it.

## Methods

- **2nd comparator = Q41 limiting condition (a lot / a little / no)**, not age. A direct functional-need
  measure -> comparing same-limitation people across deprivation sidesteps the earlier-onset confound, and
  fits the GPPS tool's 2-comparator limit. (Anselmi couldn't do practice-level interactions nationally; the
  GPPS individual-level crosstab is the route around that.)
- **Stratify by age; never collapse to one age-standardised number.** Earlier onset is real need (show the
  need gradient un-adjusted); age is a behavioural confounder on the contact side (show contact-given-need
  within age/limitation). A single age-standardised figure would hide both.
- **Track the conditional denominator at every stage.**
- **Validate** against practice-level under-detection (CVDPREVENT undiagnosed: CVDP005HYP, 002/003CKD,
  003/005DM, 002NDH) and late diagnosis (`fingertips_cancer_emergency_practice`, `ca_em_rate`).

## Data

- **GPPS crosstabs** (`data/GPPS_National_Crosstab_11072026*.xlsx`, inventoried 13 Jul):
  - Q12 deflection x deprivation x {Q41 limiting, Q38 has-LTC, Q37 vulnerabilities, Q39 condition} — DONE.
  - All questions x deprivation one-way (file (5)). Q14 diversion x deprivation x ethnicity (file (4)).
  - Q16/Q26 experience x age/ethnicity/deprivation x condition.
- **National baseline:** `research/data/gpps_national_2026.csv` (all 71 Qs, national % + N).
- **Practice-level need/validation:** `qof_prevalence_2425`, `cvdprevent_practice` (incl. undiagnosed),
  `practice_age_sex`, `practice_weighted_list` (Carr-Hill — under-critique, use with raw+morbidity),
  `fingertips_cancer_emergency_practice`.
- **Operational:** `panel_merged`, `panel_oc`, `cbt_ivr_panel`; `xsec` deflection_2026, couldnt_contact_2026.

## Downloads still sensible (2-comparator tool; same structure as the deflection files)

- **Q8 (last contact) x Deprivation x Q41** — non-presentation layer. PRIORITY. [downloading 13 Jul]
- **Q31 (needs met) x Deprivation x Q41** — resolution layer. PRIORITY.
- Q14 (diversion) x Deprivation x Q41 — confirm need-neutral on the same measure. Nice-to-have.
- Optional: Q17 x Dep x Q41 (2nd contact measure); Q8 x Dep x Age (proves age isn't doing the work).

## Standing caveats

Registers under-record in deprived areas (censoring, less than consultations but real); GPPS last-contact =
repeated cross-section, not a cohort; the deepest candidacy layer (truly unrecognised need) is hard for any
survey to reach; ecological; descriptive, not causal.
