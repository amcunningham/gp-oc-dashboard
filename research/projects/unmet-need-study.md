# Unmet-need study — project brief

_Status: NEW — data assembled 13 Jul 2026, analysis not started. England, public data only. Cohort/relative
only; NO named-practice case studies._

## Question

Which English practices are **not meeting their population's need**? Standard workload/funding models measure
*consultations* — i.e. **met** demand — so they can't see need that never converts into care, and they launder
the inverse care law into the maths. This strand measures the **gap** instead.

## The prompt for it (motivating paper)

de Dumast L, et al. *BMJ Open* 2026;16:e114094 (doi:10.1136/bmjopen-2025-114094). Findings: Carr-Hill
under-weights morbidity (partial R2 ~11%); consultation-workload model; morbidity reweighting is modest (~2.5%)
and **deprived practices still LOSE**; the residual (deprived deliver *less* workload than predicted) *widens*
when morbidity is added -> "supply-side constraints... undermeasurement of need". Their engine is consultations,
so they cannot observe unmet need. Our advance: anchor need on access-independent measures and measure under-delivery.

## Design — four angles

1. **Expected vs delivered activity.** Predict delivered activity (appointments/OC per 1,000) from **morbidity
   (QOF 21 registers + CVDPREVENT) + deprivation (IMD) + age**. Shortfall (high predicted, low actual) = candidate
   unmet need. **Never anchor need on activity itself — that is the paper's trap.**
2. **Access-failure (disambiguator).** Deflection (Q12), couldn't-contact, telephony answer rate, IVR share.
   Separates "shortfall = efficient" from "shortfall = unmet" — a shortfall with high deflection/poor answering is unmet.
3. **Under-detection (validation, practice-level).** CVDPREVENT undiagnosed/uncoded indicators:
   CVDP005HYP (undiagnosed hypertension), CVDP002CKD/CVDP003CKD, CVDP003DM/CVDP005DM, CVDP002NDH. Unmet need on its own terms.
4. **Late diagnosis (validation, practice-level).** Fingertips cancer-emergency (`fingertips_cancer_emergency_practice`,
   2024/25) + existing `ca_em_rate`. Emergency cancer presentation = missed/late primary-care diagnosis, inverse-care patterned.

**Identification caveat:** no practice fully meets need -> only RELATIVE unmet need (under-delivery vs peers at the
same morbidity/deprivation). Angles 3 & 4 rescue this because undiagnosed disease and emergency cancer are unmet
need absolutely, not relative to a benchmark.

## Data (all in shared `data/`, keyed on gp_code)

- Morbidity: `qof_prevalence_2425` (21 registers), `cvdprevent_practice` (32 indicators incl. undiagnosed).
- Capacity: `practice_weighted_list` (Carr-Hill weighted list) + `workforce_panel`. **CAUTION:** Carr-Hill is the
  very thing under critique — it under-captures deprivation workload — so use raw list + weighted + morbidity; do NOT treat weighted list as ground-truth need.
- Deprivation/demographics: `xsec_master_2026` (imd_score, imd_quintile), `practice_age_sex`.
- Delivered activity: `panel_merged` (appts), `panel_oc` (OC), `cbt_ivr_panel` (phone).
- Access-failure: `xsec` deflection_2026, couldnt_contact_2026; answer rate from `cbt_ivr_panel`.
- Validation outcomes: CVDPREVENT undiagnosed cols; `fingertips_cancer_emergency_practice`; `ca_em_rate`.
- Downstream ACSC/A&E: `acsc_emergency_icb` is **upper-tier LA level, 2020/21** only — coarse context, NOT practice-level.
  True practice-level ACSC/A&E needs HES via a DSA (application, not open) — future extension, not a blocker.

## First steps

1. Assemble one practice-level feature table (join sources on gp_code); weight by list size.
2. Model expected activity ~ morbidity + deprivation + age (WLS + HC1; helpers in `scripts/did_anima.py`). Residual = actual - expected.
3. Rank by residual; cross-tab residual x deflection x answer rate (the disambiguator).
4. Validate: does the high-need / low-delivery / high-deflection group have higher CVDPREVENT undiagnosed AND higher
   emergency cancer presentation? If yes, the residual is credible unmet need. Bank as a cohort finding.

## Standing caveats

QOF/CVDPREVENT registers themselves under-record in deprived areas (censoring — less than consultations, but present);
morbidity registers are imperfect; selection; single practice != evidence; ecological. Keep it descriptive.
