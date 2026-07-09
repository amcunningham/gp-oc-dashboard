# GP same-day appointments × online consultation panel — build notes

Built 6 July 2026. Companion to amcunningham/gp-oc-dashboard (cross-sectional Feb 2026 analyses).

## Files

- `panel_merged.csv` — practice × month panel, Mar 2023 – May 2026 (FE analysis window Apr 2023 – Mar 2026 where OC data exists). ~223,700 practice-months, 6,376 practices.
- `gpad_agg/gpad_<release>.csv` — per-release GPAD aggregates (intermediate).
- `panel_oc.csv` — OC submissions panel, Apr 2023 – Mar 2026 (from Oct 2024 + Mar 2026 releases; Mar 2026 preferred where months overlap).
- `agg_duck2.py` (in /tmp of sandbox; logic reproduced in repo notes) — DuckDB aggregation of GPAD Practice_Level_Crosstab CSVs.

## Panel columns

month, gp_code, total, same_day, next_day, book_unknown, gp, gp_same_day, f2f, phone, online, dna, attended (GPAD counts); supplier, oc_total, oc_clinical, oc_admin, oc_rate_1k, list_size, oc_capability, oc_usage (OC publication); imd_score, imd_quintile (repo practice_imd.csv); oc_tertile_feb26, region (repo full_oc_tertiles.csv); same_day_pct, gp_same_day_pct (derived).

## Sources

- GPAD: Appointments in General Practice, practice-level crosstabs, 13 releases May 2023 → May 2026 (each carries 3 months). NHS England Digital.
- OC: Submissions via Online Consultation Systems in General Practice, Oct 2024 release (Apr 2023–Oct 2024) + Mar 2026 release (Sep 2024–Mar 2026).

## CORRECTION (6 Jul 2026, evening build)

An interrupted unzip truncated the Mar-2026 OC north-regions file in the first build, dropping
~60k practice-months (region×month chunks, mostly northern practices in recent months). All
figures below are from the corrected rebuild. Adoption landscape (corrected): Apr 2023 —
4,857/6,361 practices (76%) already had OC capability, 4,537 some use, 1,871 at ≥20/1k;
Mar 2026 — 6,099/6,143 (99%) capability, 6,023 any use, 4,834 at ≥20/1k. The event-study
"adopters" (n=2,202; 1,627 with ≥6 months pre+post) are only practices crossing a strict
low(<5/1k)→high(>20/1k) threshold WITHIN the window — most practices adopted before Apr 2023
and cannot appear as events.

Corrected headline numbers: two-way FE β = 0.0060 (SE 0.0009). Event study: pooled bump +0.5pp
at k=0 fading by ~k=+11, same pre-trend. Supplier split (mean of k=+6..+12 vs k=−1):
Accurx (n=669) +0.6pp, flat pre-trend; TPP/SystmConnect (n=148) +2.4pp sustained, steep
pre-trend from −6.5pp; eConsult (n=102) ~0, noisy.

## First results (prototype, 6 Jul 2026 — superseded by correction above; qualitative story unchanged)

Sample: practice-months with OC data and ≥200 appointments; n = 164,130; 6,305 practices.

- Two-way fixed effects (practice + month FE, SEs clustered by practice):
  same_day_pct on oc_rate_per_1k → **β = 0.0048 (SE 0.0010, p < 0.001)**.
  i.e. +100 submissions/1,000 patients/month ≈ +0.5 pp same-day. Median within-practice
  SD of OC rate is 16.6/1k → typical OC variation shifts same-day % by ~0.08 pp. Effectively nil.
- Pooled (month FE only, no practice FE): β = 0.0124 — the between-practice association is ~2.6× the
  within-practice one, and still modest.
- Interpretation: cross-sectional differences in same-day provision are a property of the practice's
  access model, not driven by changes in OC volume. Consistent with OC being usable for advance
  booking as much as same-day triage.

## Event-study feasibility

- 1,335 practices show a low→high OC adoption event (3-month max <5/1k → 3-month min >20/1k).
- 4,211 practices record >1 supplier over the period (check: supplier field may reflect multiple
  concurrent systems, not a clean switch).

## Known caveats

- GPAD is official statistics *in development*: no national data-entry standards; time-from-booking
  partly reflects slot configuration (same-day share reflects booking configuration and recording, not experienced speed (r~-0.1 with GPPS Q20); WHY they diverge is not established - recording/triage-logging and capacity differences are plausible but undemonstrated; NB triage/OC use does NOT imply same-day dominance (see OC findings; Exeter examples)).
- October same-day % dips every year (flu/COVID clinics booked in advance inflate denominator) —
  month FE absorbs national seasonality but not practice-specific vaccination volume.
  Consider excluding "Planned Vaccination" national category in a sensitivity build.
- Practice-level GPAD only from Oct 2022; pre-COVID comparison must use sub-ICB geography.
- OC participation is voluntary; ~73% of practice-months have OC data, growing over time —
  selection into the OC collection is itself non-random.
- Practice mergers: gp_code panel is unbalanced (6,373 → 6,139 practices); no successor-code
  handling yet (ODS epraccur/successor file needed).
- From 2026/27 the contract requirement to record clinically urgent same-day care will change
  recording behaviour — treat Apr 2026+ as a separate regime.

## Cross-sectional models (added 6 Jul 2026, evening)

Dataset `xsec_2025.csv` / `xsec_model_data.csv`: one row per practice. Exposure = same-day %
averaged Apr 2024–Mar 2025 (12m to end of GPPS 2025 fieldwork). Linked: GPPS 2025 practice
weighted CSV (gp-patient.co.uk) — `overallexp.pcteval` (satisfaction) and
`localgpservicesprefhpsee.pcteval` (continuity: % seeing/speaking to preferred HCP);
GP Workforce Mar 2025 practice high-level CSV (FTE by staff group per 10k);
NHS Payments 2024/25 practice CSV (rurality, dispensing); merger proxy = any month-on-month
list-size jump >15% during Apr 2023–Mar 2025 (n=150). GPPS sentinel codes (<0, e.g. −97
suppressed) set to missing. GPPS models weighted by responses, robust (HC1) SEs, region dummies.

A. Predictors of same-day % (n=6,007, R²=0.067): deprivation +0.12pp/IMD point; rural −1.6pp;
log list +1.1; GP FTE/10k +0.10; nurse FTE/10k −0.22; recent merger −2.0pp; OC rate +0.016.
Low R² = structure/demographics explain little; access model looks like a practice choice.

B. Satisfaction ~ same-day %: unadjusted −0.096 (p=1e−12) → adjusted −0.032 (p=0.011).
10pp more same-day ≈ −0.3pp satisfaction. The published negative association largely reflects
confounding (size, deprivation); the residual effect is trivial.

C. Continuity ~ same-day %: unadjusted −0.236 → adjusted −0.147 (p=7e−15).
10pp more same-day ≈ −1.5pp continuity. Robust but modest. Continuity's dominant predictor is
practice size (−11.7 per log unit; small-vs-large quartile means 50.4% vs 34.3%); deprivation
−0.25/point; dispensing practices +4.8pp.

## Change models 2024→2025 (added 6 Jul 2026, late)

GPPS 2024 practice weighted CSV pulled (identical variable names to 2025; the 2023 wave used the
pre-redesign questionnaire and is NOT comparable for these measures — only 2024→2025 change
possible). `change_2024_2025.csv`, n=5,994. Exposure change: same-day % (Apr23–Mar24) →
(Apr24–Mar25), SD of change 5.3pp. Weighted by min(responses), HC1 SEs, region + covariates.

- Δsatisfaction ~ Δsame-day: +0.027 (p=0.21) — null.
- Δcontinuity ~ Δsame-day: −0.011 (p=0.77) — null.
- ΔOC rate predicts neither.

Read with the cross-section: the continuity–same-day association (−0.15) does not appear in
1-year within-practice changes. Candidate explanations: stable confounding (access model proxies
stable practice traits), effects too slow for a 1-year window, and attenuation from GPPS
practice-level sampling noise in difference scores. A 2026-wave extension (fieldwork Jan–Mar
2026, due ~Jul 2026) would give a 3-wave panel and better power.

## Analytic framework note (per AMC)

Cancer detection is an OUTCOME of the access model, not a predictor of same-day %. Framework:
predictors/structure (rurality, deprivation, list size, staffing mix, recent merger, OC/CBT
tooling) → access model (same-day %, triage, mode mix) → outcomes (satisfaction, continuity,
cancer detection/TWW conversion via Fingertips, potentially A&E attendance).

## Cancer outcomes + mode/volume (added 6 Jul 2026, late)

Fingertips (API, GP practice level, 2024/25): 91347 detection rate (% new cancers via USC
referral), 91845 conversion rate (% USC referrals → cancer), 91882 USC referral crude rate.
File `xsec_with_cancer.csv`. Weighted by indicator denominator, HC1, full controls as before.

- Detection rate (mean 52.7%): unadj −0.047 (p=9e−5) → adj −0.012 (p=0.29). NULL after controls.
- Conversion rate (mean 6.1%): unadj −0.027 → adj −0.0056 (p=0.023). 10pp same-day ≈ −0.06pp. Trivial.
- USC referral rate: unadj −13/100k → adj −3.2 (p=0.11). Null.
Raw negative associations are confounding (deprived/urban practices do more same-day and have
lower CDR). No evidence same-day access models help or harm cancer detection.

Mode & volume vs same-day % (cross-section, adjusted):
- phone share +0.146 per pp (r=+0.20); F2F share −0.214 per pp (r=−0.29) — same-day models are
  more telephone-based.
- consultation volume: +0.026pp same-day per appt/1k/mo (r=+0.20) — higher-volume practices do
  more same-day (or same-day capacity enables volume).
- DNA rate: strongly negative (adj −1.56 same-day pp per DNA pp; r=−0.12) — same-day models have
  fewer DNAs, plausibly mechanical (less time to forget).

## Wait-band (longer timescale) analyses (added 7 Jul 2026)

Re-aggregated all 13 GPAD releases with full booking-interval bands → `waits_agg/waits_<REL>.csv`,
39 continuous months 2023-03 → 2026-05. Cross-section `xsec_waits.csv` (12m to Mar 2025, n=6,007).

National trend (chart `wait_bands_trend.png`): polarisation. Same-day 43.2%→44.9%; >14-day waits
16.6%→18.3%; the 1–7-day middle squeezed (27.1%→23.7%). Practice-level corr(same-day %, 15+day %)
= −0.50.

Determinants of % waits 15+ days (R²=0.245 — far more structurally determined than same-day's
0.067): rural +2.0pp; log list +2.0; affluent (IMD −0.16/point); nurse FTE/10k +0.22;
recent merger −0.7; dispensing +0.7. Long-wait practices = rural, affluent, larger, nurse-heavy —
the booked-ahead model.

GPPS outcomes with BOTH extremes in the model (reference = 1–14 day middle):
- Continuity: same-day −0.205 (p=1e−20) AND 15+day −0.153 (p=2e−7) — both extremes worse than
  the middle. Continuity is highest where care is booked days-to-2-weeks ahead.
- Satisfaction: same-day −0.039 (p=0.007), 15+day −0.020 (p=0.29 ns).
Decile table: raw continuity falls monotonically with same-day % (47.3%→37.5% across deciles)
but deciles conflate falling long-wait share; the joint model separates the two.

## GP vs other-staff wait mix (added 7 Jul 2026)

Files: `gp_vs_other_waits_trend.csv` (national monthly), `xsec_gp_vs_other.csv` (12m to Mar-25).

National: GP appointments are majority same-day (55.4%→56.5%, stable) with ~12% at 15+ days
(stable). Other-staff appointments drive the national polarisation: same-day 31.9%→35.4% AND
15+ days 21.2%→23.3%. GPs do today's work; nurses/DPC hold the booked-ahead book.

GPPS outcomes with staff-specific wait mixes + GP share of appointments (n=6,000, weighted, HC1):
- Continuity: GP same-day −0.145 (p=6e−20); GP 15+ null; other-staff 15+ −0.128 (p=8e−7);
  GP share of all appointments +0.192 (p=5e−18). The continuity cost of same-day models lives
  specifically in the GP appointment mix; GP-delivered share is the strongest positive predictor.
- Satisfaction: GP 15+ POSITIVE +0.049 (p=0.004) — booked-ahead GP care associates with higher
  satisfaction; other-staff 15+ negative −0.046; GP share +0.083 (p=7e−8).

## No-booking cohort + QOF (added 7 Jul 2026)

Cohort: GP same-day % (12m to Mar-25) ≥80% → 332–342 practices (5.5%); ≥90% → 43; ≥70% → 17%.
Persistent trait: 163/342 at ≥80% in all three years; gp_sd correlates 0.77 two years apart.
Profile vs rest: smaller, more deprived (IMD 28 v 23), urban, Midlands/London-heavy, phone-heavy,
other-staff appts also more same-day. Unadjusted continuity −2.7pp, satisfaction −3.0pp.

QOF (Fingertips ind. 295, % points achieved, 2024/25, mean 93.9, ceiling-skewed): NULL on all
specifications. gp_sd continuous +0.0004 (p=0.92); high80 cohort +0.01pp (p=0.96); OR for
bottom-quartile QOF 0.89 (p=0.39). Raw 1pp gap (93.0 v 94.0) is entirely composition. QOF is
delivered via recall/booked systems regardless of access model. Caveats: ceiling effects,
personalised-care adjustments, partial income protection in recent years compress variation;
domain-level QOF might still differ. File `xsec_qof.csv`.

## Cancer emergency admissions (added 7 Jul 2026)

Fingertips 91355 (NDRS): emergency admissions WITH cancer, crude rate/100k registered, practice
level, 2024/25 (mean 522). NOTE: measures any emergency admission of a cancer patient — mixes
route-to-diagnosis with crisis care of known cancer; NOT the same as % diagnosed via emergency
presentation (not published at practice level). Added % 65+ (workforce census age bands) as
control — dominates (β≈20/100k per pp, model R²=0.48). File `xsec_cancer_em.csv`.

- GP same-day % : full model −0.36/100k per pp (p=0.03) — 10pp more GP same-day ≈ −3.6/100k
  (~0.7% of mean). Borderline, slightly favourable to same-day access; treat as null-to-marginal.
- No-booking cohort (high80): null (−3.8, p=0.71).
No evidence same-day-dominant models increase cancer emergency admissions.

General ED attendance/admissions NOT published below sub-ICB (patient side) / provider (hospital
side); ECDS holds GP_PRACTICE_CODE_TRACED so practice tabulations need DARS, OpenSAFELY, or CPRD.

## Critique: Jamieson, Gravelle & Santos (Health Policy 2025) — avoidable ED attendance (added 7 Jul 2026, per AMC)

Paper: 10.16M adult attendances, 144 Type 1 EDs, 2018/19 HES A&E (NOT ECDS), attendance-level
LPM/logit with ED fixed effects. Exposures include GPPS patient-reported "can book same-day"
(NOT GPAD). Finding: higher same-day proportion → attendance less likely avoidable.

AMC's critique (confirmed from deposited full text): both avoidability definitions are partly
DISPOSITION-BASED — admission ⇒ not avoidable (Disposal domain), ambulance arrival ⇒ urgent,
NHS definition also requires discharge home/GP + only minor treatments/investigations.
Consequences:
1. Circularity via ED behaviour: admission/investigation thresholds vary by bed pressure,
   4-hour-target management, and patient type. Older/deprived patients admitted at lower
   thresholds ⇒ mechanically "unavoidable" — their demographic gradients are partly artefact.
   ED fixed effects absorb between-ED threshold differences only, not within-ED differential
   handling.
2. Exposure can reach outcome through the wrong path: poor practice access → later, sicker
   presentation → admission → classified unavoidable → practice looks BETTER. Direction of
   bias on the same-day association is indeterminate.
3. Fragility: kappa between their own two definitions = 0.44.

Openings for our work / a York approach: (a) rates, not conditional-on-attendance shares;
(b) GPAD supply-side access measures vs their GPPS perception measure; (c) ECDS chief-complaint
data would allow a PROSPECTIVE avoidability definition (they name this as future work);
(d) GP clinical input on triage-recording artefacts. Pitch = complementary collaboration,
not correction.

## Perception vs supply + GPPS access-experience variables (added 7 Jul 2026)

Files `perception_vs_supply.csv`, `gpps_access_experience.csv`; questionnaire reference
`GPPS_2025_questions.md` + PDF. Key measurement finding: patient-experienced same-day
(Q20 lastgpapptwhen_1, mean 52%) correlates −0.10 with GPAD same-day SHARE and only +0.05 with
per-capita same-day supply; +0.18 with total appts per capita. share = percap/total, so the
three measures are near-collinear; clean spec = share + total capacity.

Clean spec results (z-outcome ~ z_share + z_capacity + controls, weighted, HC1, n≈6,000):
outcome              share      capacity
pt same-day (Q20)    −0.149***  +0.181***
wait too long (Q21)  −0.246***  −0.045**
next step immediate  −0.204***  −0.128***
contact fail (Q12)   +0.047***  −0.138***
phone failed (Q11)   +0.034*    −0.082***
A&E after fail (Q15_8, among failed) −0.034*  +0.004
A&E after fail, population approx    −0.015   −0.070***

Reading: CAPACITY protects — fewer failed contacts, fewer A&E fallbacks, more experienced
same-day. CONFIGURATION (high same-day share) conditionally reduces experienced same-day and
raises "come back tomorrow" contact failure (rationing signature) — BUT strongly reduces
"waited too long" among those seen. Tension between Q20 and Q21 worth exploring (expectation
management by triage systems? conditional-on-appointment speed?).
Policy point: the GPAD same-day % metric (2026/27 contract) tracks configuration, not the
capacity that actually predicts patient-experienced access and A&E avoidance.
NB: gpcontactoutcome = Q11 (phone outcome); gpcontacthandlerequest = Q14 (corrected mapping).

## Remaining covariates linked: ethnicity + ODS-validated mergers (added 7 Jul 2026)

Ethnicity: GPPS dv_ethnicityband_1 (White) → nonwhite % (survey respondents; skews older —
caveat). Mean 24.6%. Independently predicts lower continuity (−0.050/pp, p=2e−5) and
satisfaction (−0.056/pp, p=2e−11), partially attenuating IMD. Same-day coefficients survive
(continuity −0.141, satisfaction −0.026).

Mergers: ODS succ file useless for practices (44 practice rows ever). Built from epraccur
closures instead: 703 org closures Apr23–Mar26, 190 were practices seen in OC data with a PCN.
Flags: closure_exposed = same-PCN practice within ±2 months of a closure (n=212 in analysis
set); merger_recipient = closure_exposed AND ≥5% list jump (n=7 — tiny). Results:
closure_exposed → satisfaction −2.1pp (p=0.016), continuity −2.2pp (p=0.06);
merger_recipient → continuity −12.5pp (p=0.03) but n=7, fragile. The old 15%-jump proxy
(n=150) goes null once these are included — it was mostly noise (boundary/registration churn).
Local practice closure looks like a real patient-experience shock; needs the full closure list
(many closures absent from OC data) for a proper estimate.

## Workload / case-mix and prescribing (added 7 Jul 2026)

Sources: Fingertips 241 diabetes QOF prevalence (2024/25 via parent_area_type=66; mean 8.3%);
NHSBSA EPD API (datastore_search_sql, EPD_202503): antibacterial items (BNF 0501) and total
items per practice, Mar 2025. File `xsec_workload_rx.csv`. NB OpenPrescribing API is behind
Cloudflare — NHSBSA open-data API is the scriptable route.

Case-mix → access model: diabetes prevalence and items/patient strongly predict CAPACITY
(appts per capita: dm_prev +10.0/pp, items/pt +56.8, R²=0.30 — provision tracks need) but NOT
same-day SHARE (dm_prev p=0.63; R² unchanged at 0.06). Configuration is a choice; capacity is
need-driven.

Antibiotics (items/1k/month, age-adjusted with %65+, diabetes prevalence controlled; crude —
no STAR-PU): capacity +0.119*** (more consultations → more scripts, expected); same-day share
+0.080*** (10pp share ≈ +0.9% of mean — small but real: same-day-dominant models prescribe
slightly more abx); phone share −0.031** (remote-heavy practices prescribe slightly FEWER —
against the 'remote consulting drives antibiotics' concern). Caveat: prescription month
attribution, no STAR-PU, single month.

## GP staffing and cancer detection (added 7 Jul 2026, evening)

Direct model (prompted by explorer testing): cdr ~ gp_per10k + nurse_per10k + dpc_per10k +
IMD + %65+ + log list + rural + region (n~6,000, HC1). Raw corr 0.094 (negligible-to-weak).
Adjusted: GP FTE/10k +0.081pp detection (p=0.005) - SURVIVES adjustment, unlike the same-day
share associations; nurse staffing null (-0.098, p=0.17). Going from 9 to 15 GP FTE/10k ~
+0.5pp on mean CDR 52.7%. Fits the recurring pattern: GP-delivered care shows small positive
associations (satisfaction, continuity, detection) where nurse/DPC staffing does not.

## Nurse staffing and cancer pathway measures (added 7 Jul 2026, evening)

Raw corr nurse FTE/10k vs TWW conversion = +0.27, vs referral rate +0.17. Both collapse with
adjustment (conv: +0.012, p=0.26; ref_rate: -10.0, p=0.08). Mechanism is age confounding:
nurse-heavy practices serve older lists (r=0.36 with %65+), and %65+ correlates 0.57 with
conversion (older patients' urgent referrals are more often cancer). Nurse staffing also null
for detection rate. Contrast: GP staffing vs detection survives adjustment (+0.081, p=0.005).

## Method note: the explorer as a hypothesis-generating loop (added 7 Jul 2026)

The NL-to-SQL explorer (explore.html) has functioned as more than an access layer. The working
loop during development: the tool surfaces a raw association -> a clinically-informed reader
challenges it (wrong variable, wrong frame, confounding suspected) -> the adjusted model is run
-> the result is added to these notes and to the tool's grounding summary -> both the query and
narrative routes of the tool improve. Three findings in these notes (GP staffing vs detection;
nurse staffing vs conversion = age confounding; capacity vs configuration glossary) originated
as explorer questions. Failure modes observed and fixed during testing are documented in the
prompt design: nulls spun as support, findings transplanted across exposure-outcome pairs,
variables misdefined by guess, units guessed, direction left ambiguous. The general lesson:
LLM interfaces over health data need (a) visible, editable SQL; (b) a grounding summary of
adjusted findings scoped to exact exposure-outcome pairs; (c) an independent second route
(notes-based) that can audit the first; (d) a sceptical domain expert in the loop.

## Covariate linkage status (all planned covariates now linked)

- Rural/urban: ONS Rural-Urban Classification via practice postcode (epraccur → LSOA → RUC).
- Staffing: GP Workforce practice-level monthly (FTE GP/nurse/DPC per 1,000).
- Mergers/closures: ODS epraccur close dates + successor organisation file.
- Satisfaction: GPPS practice-level (annual) — overall experience, access items.
- Fingertips: ethnicity of practice population, cancer detection (TWW conversion/detection rates) —
  annual, practice-level, via fingertips API.

# ============================================================
# SESSION 3 FINDINGS (added 8 Jul 2026, evening block)
# Written retrospectively; every result below was prompted by
# AMC's questions and survived her adversarial review.
# SAMPLE LEDGER (applies throughout): "full sample" = ~6,000
# practices with GPPS 2025 (gpps_n>=50 where survey outcomes
# used); "CBT sample" = ~3,970 practices also reporting cloud
# telephony (larger, less deprived [-0.4 SD], more southern,
# heavier OC [+0.4 SD]; access-model variables representative).
# Anything involving rush shapes, call volumes or answer rates
# is CBT-sample only.
# ============================================================

## 3.1 Satisfaction anatomy (full sample)

New columns: access_satisfaction (GPPS Q16, % good experience of
contacting the practice, mean 71.8) and phone_easy (Q1, % easy to
get through by phone). Q32 overall satisfaction correlates:
Q16 +0.90, phone ease +0.78, waited-too-long -0.71, contact
failure -0.68, continuity +0.60, experienced same-day (Q20) +0.32
[all same-survey; shared-source inflation, ordering robust].
Cross-source (uninflated): GP FTE/10k +0.27, appts per capita
+0.16, GP-delivered share +0.10, same-day share -0.10.
Q16 itself: phone ease +0.87, Q20 +0.31, capacity +0.13, share
-0.10. Reading: overall satisfaction is dominated by access
experience, then continuity; configuration irrelevant; of hard
measures GP staffing leads. NB Q20 is a behavioural report (last
appt was same-day), NOT access satisfaction - distinct constructs
(AMC point); Q16 is the purpose-built access-satisfaction item.

## 3.2 The two 8am rushes vs experience (CBT sample)

Phone-rush concentration (rush_pct, % of weekday calls 8-10am)
is UNRELATED to satisfaction measures (+0.03..+0.07). OC-rush
concentration (oc_rush_pct) is negative throughout: raw -0.21
satisfaction, -0.25 access satisfaction, -0.31 phone ease.
Population-adjusted (IMD, age, ethnicity, rurality, size, region
- deliberately EXCLUDING downstream access-model variables per
over-adjustment risk, AMC): -2.3 / -3.2 / -5.3 pp per SD, all
p<0.001; adding capacity changes nothing; adding OC VOLUME to the
model: volume null on satisfaction and access satisfaction (mild
negative on phone ease only, -1.4/SD), rush shape keeps full
effect. THE PENALTY FOLLOWS THE SHAPE OF INTAKE, NOT THE TOOL OR
THE VOLUME.

Mechanism candidates tested:
- Platform caps: morning concentration is near-identical across
  recorded suppliers (34-37%) -> not a platform default; but ALL
  platforms can be closed at capacity (AMC), so practice-
  configured windows remain candidate. Discriminating test
  proposed: code practices' published OC opening hours from their
  websites vs oc_rush_pct.
- Under-capacity: oc_rush_pct is orthogonal to every supply and
  demand observable (GP FTE +0.02, capacity +0.07, calls -0.07,
  dm_prev +0.07, IMD 0.00) -> looks like intake DESIGN/behaviour,
  not resourcing. BUT see 3.6: the under-capacity reading is
  vindicated for the rush's toxic OUTPUT (deflection), which IS
  resource- and need-patterned.
- Allocation rule: BOTH rushes carry the same provision
  signature - same-day allocation models (gp same-day share
  ~+0.20 each; null vs volume/staffing/booked-ahead). AMC
  formulation adopted: where today's care is allocated today,
  early submission is RATIONAL; the perception "get in early or
  miss out" tracks the allocation rule, not scarcity.

## 3.3 Resolution timing (Q13; CBT sample; NB Q13 is asked only
of respondents who GOT a next step - the race's losers are
routed past it to Q15)

"Knew next step there and then": phone rush +0.28 (adjusted
+1.2/SD) - the phone race resolves instantly; OC rush -0.22
(-2.0/SD); OC VOLUME -0.66 raw / -9.1pp per SD - the largest
activity correlation in the project, but largely definitional
(forms are asynchronous). Full Q13 distribution: OC volume's
loss of "there and then" reappears almost entirely as "later the
SAME day" (+0.63), modest leakage to next-day (+0.31). OC-rush
practices' same-day resolution (cat 1+2) is +0.08 - normal.
So: OC limbo is hours not days and is NOT the harm (volume is
satisfaction-null); the OC-rush harm is not slow verdicts but
MORE OUTRIGHT LOSERS (see 3.4). Mediation NOT modelled
(satisfaction ~ rush + Q13 rejected as over-adjustment: Q13 is
downstream; controlling a mediator amputates the pathway and
invites collider bias).

## 3.4 Failure decomposition (full sample; contact_fail was a
composite - AMC required the split)

Q12_3 "told to contact again another day" (DEFLECTION, mean
8.7%) vs Q12_4 "couldn't contact at all" (mean 1.2%).
- Deflection: OC volume -0.19 (forms accept the request), OC
  rush +0.21, phone rush +0.16 (both races deflect); vs access
  satisfaction -0.70 (largest same-survey weight found).
- Couldn't-contact: OC volume +0.15 (phone deprioritised /
  digitally excluded tail), vs access satisfaction -0.37.
Patients punish the ANSWERED REJECTION far more than the
unanswered phone. Heavy OC trades deflection down for a smaller
excluded tail - first clearly pro-OC experience finding.

## 3.5 Deflection determinants (full sample) - THE INVERSE CARE
LAW, LOCATED

Adjusted, pp per SD on mean 8.7%: capacity -0.95, GP FTE -0.83,
GP same-day share +0.63, deprivation +0.158/IMD point (~+2pp
across IQR); all p<1e-14. Unlike the rush shapes, deflection IS
need meeting resources - deprivation drives it net of supply,
i.e. unmet demand invisible to supply measures shows up as
rejections (AMC's under-capacity hypothesis vindicated HERE).
The most-deflected are the least equipped to re-race tomorrow.

## 3.6 Call volumes and answering (CBT sample)

Call volume/1k = the missing DEMAND proxy: +0.32 diabetes
prevalence, +0.26 IMD, +0.20 age65+; unrelated to same-day share
(-0.01); OC substitution -0.33; satisfaction mildly POSITIVE
adjusted (+0.43/SD) - busy phones are a reachable practice in
use, not distress. AMC: total inbound conflates demand with
redial frustration -> split via CBT indicators (inferred:
CBT001 inbound, CBT003 answered, CBT004 abandoned-in-queue;
VERIFY vs metadata xlsx before publication).
ANSWER RATE (mean 60%): +0.49 with patient-reported phone ease
(strongest cross-source correlation in project), +0.38 access
satisfaction, +0.30 satisfaction, -0.28 deflection; UNRELATED to
deprivation (-0.04), GP staffing (+0.04), capacity in every
decomposition (all-staff, GP-delivered, other-staff), OC use,
AND admin/non-clinical FTE per 10k (-0.01 raw; -0.13/SD adj, ns;
caveat: category lumps receptionists with secretaries/managers;
deployment unmeasured). LIST SIZE -10.0pp per log unit
(p=1e-156), ~-7pp answer rate per doubling, NOT explained by
admin per capita. Answering = operations, degraded by scale.

## 3.7 Anima / Continuum Health (full sample; AMC identified
Continuum = Anima's company name, from practice websites:
Rushden + Higham Ferrers = Anima, The Mounts = Accurx, all
total-triage front doors; all three in the bottom-20 continuity
list, a Northamptonshire cluster)

Cohort: 313 practices with Continuum/Anima recorded supplier by
Mar 2026. Their GPPS-2025 scores: satisfaction -5.0pp, continuity
-5.7pp, access satisfaction -6.0pp adjusted (all p<1e-7),
highest contact-fail (11.9%), despite affluent profile.
CRITICAL TIMING: only ONE practice carried the label by the
GPPS-2025 fieldwork window -> these are PRE-ADOPTION baselines.
Reading: struggling-access practices adopt Anima (selection),
not (yet) platform effect. Residual: adoption date vs
reporting-start date indistinguishable in the supplier field
(Wealden Ridge held Continuum with zero submissions), so some
true adopters may predate fieldwork - calibrate with website/
announcement dates.
PROSPECTIVE DESIGN READY: 313 identified adopters, pre-scores
banked (GPPS 2025), post-scores due imminently (GPPS 2026,
fieldwork Jan-Mar 2026): adopters vs matched non-adopters DiD on
satisfaction/access/continuity/contact-fail. Effectively
pre-registered by this note.

## 3.8 Continuity extremes (full sample, gpps_n>=50)

ELITE (>=80% continuity): 143 practices
(continuity_elite_80plus.csv). Profile of top-100: list 6,000 vs
10,300; 50% rural; 50% dispensing; IMD 18 vs 24; 65+ 24% vs 18%;
same-day share LOWER (36 vs 43); satisfaction 93.2 vs 76.9.
23 elite practices are urban AND IMD Q4-5 - mostly tiny personal
lists (eponymous single-handers). Two refute the same-day/
continuity trade-off outright: Moss Way L11 (IMD 49, 72.9%
same-day, 84.7 continuity, 90.6 satisfaction) and Dr Kulshrestha
B18 (IMD 51, 69.7% same-day, 82.8, 96.1). At personal-list scale
same-day and continuity are the same thing.
DESERTS (<15%): 288 practices. Bottom-100 profile: list 15,000;
OC 88.5/1k (heaviest of any cohort, an UNDERCOUNT given 3.7);
GP share 41.9 vs 46.7; deprivation IDENTICAL to average (23.7 vs
23.5) - continuity destruction is ORGANISATIONAL, not social
(contrast deflection, 3.5). Zeros (5 practices at 0.0%) carry
small Q7 bases and some entrants are atypical access services -
manual clean needed before publication. Satisfaction in the
basement spans 33-86: Wish Park (Hove) 0% continuity / 79%
satisfaction - convenience clientele; forgiveness flows both
ways (see 3.9).
Response-rate note: Reeth 60.1% response (highest in England;
mean 29.1) but resprate is demographics (age +0.85, nonwhite
-0.76, IMD -0.60, rural +0.51) - GPPS hears affluent old rural
England loudest; deflection gradients likely UNDERSTATED.

## 3.9 Case studies

ST LEONARDS PRACTICE, Exeter (L83042; the Pereira Gray
continuity practice): highest continuity in its PCN (60.1 vs
54.8) and RISING (+6.8pp yr-on-yr) while same-day share ROSE
44->52% - within-practice refutation of reading the cross-
sectional trade-off causally. Model: Accurx-heavy morning OC
funnel (61% of OC 8-10am), 51% phone delivery, 34% more
capacity than PCN peers, easiest contact (1.7% fail) - but
lowest PCN satisfaction (71.8 vs 83.5, improving) and highest
waited-too-long. Phone-first same-day triage organised FOR
continuity; satisfaction penalty plausibly mode/expectations.
WEALDEN RIDGE (G81088; AMC's origin practice, Visiba-linked):
prediction test - AMC guessed few deflections; WRONG in an
instructive way: deflection 13.7% (vs 8.7) with 0.0% couldn't-
contact, 72.8% instant verdicts, no morning race either channel,
below-avg capacity, booked-ahead model. Access satisfaction 66
(below avg) yet OVERALL satisfaction 90: the 0.90 access/overall
coupling DECOUPLES where in-room strengths dominate - full GPPS
profile shows health-confidence +1.28 SD (their most distinctive
score), records/being-known +0.78, listening +0.44, preferred-
professional +0.44; weakest: WEBSITE -0.81 (= the digital front
door, plausibly Visiba UX), care-planning, mental wellbeing.
Their triage traffic is essentially invisible in national OC
data (Continuum record, zero submissions; token Accurx) - the
hidden-workload thesis embodied. Calls 470/1k (37th pct), rush
19% - flat, orderly, analogue-preferred.

## 3.10 Typologies and the cross-tabulation

SUPPLY TYPOLOGY (k-means, k=5, CBT sample n=3,964; features =
what practices DO: gp_sd, oth_sd, d15plus, phone share, GP
share, log OC rate, both rush shapes, answer rate; outcomes and
demographics excluded by design). Silhouette 0.11-0.12 at all k:
practices are a CONTINUUM; types are map segments, not species
(relativises the BJGP two-cluster paper). Types (satisfaction
order): Bookable (n=1091; most booked-ahead, rural-ish; 78.8 /
continuity 43.0); GP-answers-today (1009; GP share 58%, phone-
first, best answer rate 65%; 77.7/41.5); Engaged-tone (570;
minimal OC, worst answer rate 47%, biggest call rush; 76.1/37.6);
MDT triage (750; GP share 33%, heavy OC, biggest lists;
75.8/37.1); 8am form race (544; OC 104/1k, OC rush 56%;
72.9/33.7). Both worst types share contact-fail 12.1 - the two
failure modes. Demographics near-flat across types: organisational
speciation, not population sorting. HONESTY: eta-squared of type
on outcomes 3.0-4.4%; within-type SD ~11 vs between-type range
~6 - types differ reliably in aggregate, predict individual
practices poorly. Non-CBT practices allocated by nearest centroid
on 6 shared features (supply_typology_all6k.csv): engaged-tone
share doubles (14->33%) in the analogue third (label there =
"low-digital"); profiles replicate out-of-sample (form race
72.3/33.7).

PATIENT-EYE TYPOLOGY (k=5, full sample n~5,530; features = what
patients REPORT: contact-channel mix Q10, channel ease Q1-3,
verdict timing Q13, failure Q12, experienced same-day Q20, wait
verdict Q21; satisfaction EXCLUDED from clustering). Better
separation (silhouette 0.16-0.23). Types: Phone-works (1297;
76% phone, everything functions; satisfaction 88.3, continuity
56.8, lists 7.4k); Digital-works (654; 35% online; 81.5/42.2);
Phone-adequate (1891; 78.1/40.4); Digital-fails (768; 67.5/29.0;
biggest lists); Unanswerable-phone (920; fail 20%; 63.5/28.8;
most deprived 27.5). Channel x functioning: functioning dominates
(same-channel pairs differ ~20pp satisfaction; same-functioning
cross-channel ~5pp). Circularity caveat: types built partly from
experience items; satisfaction gaps partly constructed; the
continuity gradient (57->29) is the non-circular signal.

CROSS-TAB (supply x patient types; full sample n=5,526; Cramer's
V=0.20): every configuration produces every experience; odds
differ ~2x at extremes. Form race: 7% phone-works, 47% failing
front doors (28% digital-fails, highest cell). Bookable: 33%
phone-works. MDT triage: most likely digital-works (21-25%).
Engaged-tone: 24-26% unanswerable, ~1-2% digital-works (nowhere
to fail into but the queue). HEADLINE: configuration doubles or
halves the odds of a working front door and never settles them.

## 3.11 Files added this session

cbt_answer_rates.csv; continuity_elite_80plus.csv;
practice_typology_k5.csv (CBT); supply_typology_all6k.csv;
patient_typology_k5.csv; rush_both_sameday.csv (earlier);
xsec_master gains: access_satisfaction, phone_easy,
satisfaction_2024, continuity_2024, sd_share_prior_year,
statins_per1k, cdr/conv/ref_rate, geography columns.
TO DO: cohort files + typologies into repo data/ and explorer
schema; verify CBT indicator labels vs metadata; GPPS 2026 DiD
(3.7) on release; OC window-policy website survey (3.2);
Northants cluster local history; manual clean of desert cohort;
letter to NHSE OC publication team re supplier-field opacity
(Anima-as-Continuum, Visiba invisibility).

## 3.12 Late-evening additions (8 Jul 2026): demand levers, antibiotics, long-interval composition

EMPOWERMENT: healthconfidence (GPPS Q42) vs IMD -0.52 raw; adjusted -0.30pp/IMD point
(p~1e-153) net of age/ethnicity/rurality/region - the self-management reserve is scarcest where
demand pressure is highest. Confidence -> calls/1k -7.3 per SD (p=.049, cross-source) - the only
demand-side lever with the predicted sign vs a machine-measured outcome. Continuity showed NO
demand reduction in delivered appointments (throughput-capped instrument - delivered volume
cannot reveal demand under capacity constraint; patient-level literature unchallenged).

ANTIBIOTICS vs CONTINUITY (counter-literature, robust): practice-level +1.06..+1.15 items/1k/mo
per SD continuity, p<1e-17, surviving: full age bands (85+, 75-84, 65+, 0-4), diabetes
prevalence, deprivation, ethnicity, dispensing, urban-only restriction. AMC: %85+ never a
volume driver (small population share). DISPLACEMENT test: deflection -0.84 (p=4e-11) with
continuity +0.75 in same model - consistent with low-access practices EXPORTING prescriptions
to OOH/ED (practice-attributed data blind to them); continuity practices capture their own
infections. Candidate explanations ranked: displacement; ecological reversal (within-practice
continuity may still reduce prescribing - Simpson); residual case-mix/care homes; NOT dispensing
or rurality (tested). Person-level adjudication = NI GPIP (see protocol annex).

LONG-INTERVAL COMPOSITION (AMC challenge: '28-day bookings may be reviews = continuity'):
CONFIRMED - planned-category share rises monotonically with booking interval: 7.3% (same-day)
-> 54.3% (>28 days; Planned Clinics + Procedures + SMR top the band); May 2026 release.
Long-interval growth CANNOT be read as queue inflation; honest horizon-drift gauge = growth in
UNPLANNED long-interval bookings only (requires category-kept re-aggregation - TODO).
Two-gauge capacity dashboard rev.2: deflection rate + unplanned-horizon drift.

RACE-AS-CHOICE demoted to unresolved: oc_rush orthogonal to measured supply/need BUT correlates
+0.21 with deflection (the imbalance thermometer); invisible imbalance cannot be excluded;
adjudication = window-policy ground truth (PACT access-systems questionnaire > website scrape).

NI PROTOCOL LINKAGE: AMC's prior protocol v0.7 (funding/deprivation/continuity/unplanned care;
GPIP consultation-level with clinician IDs; HBS linkage) receives England-derived pre-specified
hypotheses via Annex A (drafted 8 Jul 2026): displacement (all-source antimicrobial
attribution); within- vs between-practice continuity-antibiotic association; continuity as
contact-demand efficiency (GPIP observes contacts, not throughput); access-model exposure gap
patched by PACT questionnaire census (~316 practices; NO booking timestamps in GPIP -
consultation-recorded, per AMC). PACT Accessing Continuity (Dineen/Mahoney, Bristol) =
complementary ground-truth instrument; collaboration email drafted.

## 3.13 OC submission timing: caps do not exist, the race is clinical, and the clinical/admin split is broken for whole platforms (8 Jul 2026, night)

Source: OC Submissions day/time supplementary file, Mar 2026 (per-practice weekday x hour-band
counts, CLINICAL/ADMIN/TOTAL). All results weekday-only, practices with >=100 weekday submissions
(n=5,054) unless stated.

**Noon-cap census (AMC: "which practices cap ie receive no OC after 12pm... cause i don't think
that is happening").** She was right. Only 2 of 4,402 practices receive <2% of submissions after
noon; median practice receives 40% after noon. Hard morning windows essentially do not exist in
the data. The morning concentration documented in 3.2 is therefore BEHAVIOURAL (patient response),
not an imposed cap. Consequence: briefing v0.2 language about "morning-capped windows" / "intake
design" was wrong and removed in v0.3. Working hypothesis: where today's care is allocated today,
early submission is rational - a scarcity response, mirroring the 8am phone race.

**Clinical vs admin time-of-day split.** Clinical requests race, admin requests don't: 42.9% of
clinical submissions arrive 8-10am vs 27.7% of admin. Joint model (access satisfaction on both
rush measures + usual controls): clinical-rush -2.16pp/SD vs admin-rush -1.20pp/SD. The
experience association attaches to the clinical race specifically - consistent with the
scarcity-response reading, since admin requests face no same-day allocation pressure.

**Wealden Ridge re-check.** All 163 weekday submissions are ADMIN, zero clinical, evening-peaked
(18:00 band = 17%). No race because no clinical intake is recorded at all - the Visiba triage
activity is invisible at origin, confirming 3.9's data-completeness case at the practice itself.

**"Next to no clinical digital" census (AMC) - CORRECTED after AMC caught my error.** First
pass reported 436 practices as "admin-only". AMC opened the file and spotted that adm was also
0 ("so confused cause all labled 0 for admin") - correct: I had ignored the file's fourth
category column, UNKNOWN_OTHER. The corrected picture splits into two very different cohorts:

(1) NO-SPLIT REPORTERS (n=409, >=90% of submissions uncategorised): whole platforms return no
clinical/admin code at all - Evergreen Health Solutions 183 (Wigan/Gtr Manchester cluster),
Silicon Practice Ltd / FootFall 130. Near-average OC volumes; a supplier data-pipeline gap, not
a practice behaviour. Nationally 899k of 9.5M weekday submissions (9.4%) are uncategorised, so
"% clinical" is 65.9% of total but 72.8% of categorised - denominator matters.

(2) ADMIN-DOMINANT WITH REAL SPLIT (n=22, <10% clinical of categorised, >=100 categorised):
the true "invisible clinical triage" cohort - the split is populated but contains almost no
clinical. Wealden Ridge (Accurx, 163 admin / 0 clinical) sits here, alongside a visible Klinik
Healthcare cluster (Stratford Health Centre, The Forest Practice, The Simpson Centre - all
0 clinical) and several Accurx practices. These are practices where clinical triage demonstrably
happens on a platform but is recorded as zero.

Implications: (a) 3.2's clinical-rush models excluded cohort 1 via the clinical-volume filter,
so results stand but under-represent Evergreen/FootFall practices; (b) the NHSE data-
completeness letter now has three named failure modes - platform invisible entirely
(Visiba/Wealden's triage arm), platform present but returning no categorisation (Evergreen,
Silicon), and split populated but clinical recorded as zero (Accurx and Klinik at specific
practices). File: data/admin_only_oc_cohort.csv (431 rows, category column distinguishes the
two cohorts).

**GPPS 2026 note:** publication announced for 9 Jul 2026 - the morning after this session.
Pre-registered intentions (see 3.7): Anima/Continuum DiD on 2025->2026 change using adoption
timing; deflection and access-satisfaction deltas for the admin-only cohort; refresh of banked
KEY_FINDINGS in explore.html once practice-level file lands.
