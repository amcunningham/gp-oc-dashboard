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
# ============================================================
# SESSION 4 (9 Jul 2026): THE 2026 SURVEY WAVE AND THE
# FOURTEEN-YEAR FILE. Written same-day. Every headline below
# was reshaped by AMC's challenges; her corrections are credited
# inline. Wealden Ridge is deliberately excluded from commentary
# in this session's notes (single identifiable practice).
# ============================================================

## 4.0 Plain-language summary

The 2026 patient survey (fieldwork 2 Jan - 13 Apr 2026, published 9 Jul) shows modest national
improvement: contacting practices got easier, and "call back tomorrow" fell from about 9 in 100
patients to 7 in 100. Improvement was slightly larger in deprived areas, which remain far behind.

Practices that moved to full online triage in the past year did worse than everyone else while
the country improved. This attaches to the intake model, not any one company's product. The
contact-experience penalty looks temporary (practices a year in have mostly recovered); the loss
of seeing your usual GP does not fade on average - BUT it is not inevitable: nearly half of
adopters IMPROVED continuity, some dramatically, across all suppliers. How the practice
configures routing matters more than the software. Adopters were also already struggling - their
survey scores had been sliding relative to peers for a decade before they switched - so the
switch cannot be cleanly blamed for their position, and almost none switch back.

The practices that deflect the most patients have been the hardest-to-contact practices since at
least 2012, worsening steadily, hit hardest by the post-COVID demand surge. About a hundred
escaped the deflection tail this year, with big satisfaction gains; escapers built up online and
phone intake. The two hundred still stuck are poorer-area practices. Meanwhile, the ~2,300
practices that closed over the decade were small (median 3,600 patients, half the size of
survivors) and scored close to the national average until the end: closure removes small,
adequate practices, while large struggling ones persist because their patients have nowhere to
go. Ordinary list growth does no measurable harm; the fastest-growing fifth (median +83%,
i.e. merger-scale growth) now scores worst.

## 4.1 Ingest and infrastructure

ingest_gpps2026.py ran on publication morning (integrity check passed). New xsec_master_2026
columns: *_2026 for satisfaction, continuity, access_satisfaction, phone_easy,
nextstep_immediate, wait_too_long, gpps_n; deflection_2026 and couldnt_contact_2026 (Q12
categories). deflection_2025/couldnt_contact_2025 banked retroactively from the re-downloaded
2025 raw file after AMC caught that the 2025 extraction had never been saved. pt_same_day_2026
QUARANTINED (r=0.33 with 2025; suspected Q20 category-mapping problem; excluded from explorer
schema). Fieldwork windows comparable (2025: 30 Dec 2024 - 1 Apr 2025).

The long file: gpps_long.csv/.parquet - 120,370 practice-wave rows, 2012-2023 (nine biannual
publications 2012-06..2016-07 + seven annual waves), satisfaction (Q28_12pct), phone_easy
(Q3_12pct), continuity (Q9_12pct), identified by chained practice-level correlations and
validated against published national figures (July 2016 matches the NHSE bulletin exactly:
85.2 / 70.1). Breaks documented: 2016->17 biannual->annual, 2017->18 sampling, 2024 = new
series (file deliberately stops at 2023). practice_list_history.csv/.parquet - real registered
list sizes, April snapshots 2013-2026, 98,277 rows, national totals validated (56.0M -> 63.7M),
includes since-closed practices. Both added to the explorer as views (history, lists) with
series-break and era-confounding guards in the schema prompt.

## 4.2 National picture 2026

Access satisfaction +2.6pp, phone ease +3.5pp, satisfaction +1.2pp, continuity +1.5pp on 2025.
Deflection 8.8% -> 7.1% (first true change reading; 2025 value banked this session). Change
pro-poor (most-deprived quintile d_acc +3.25 vs +2.54 least) but level gap ~7pp and deflection
still doubles across the IMD gradient (4.9% -> 9.7%). Largest practices improved most (+3.3 vs
+1.9 smallest) despite the size penalty in levels. SW and NE&Yorkshire lag on every delta.
Distributions NARROWED (satisfaction sd 11.3->10.8, access 13.5->12.4, deflection 6.7->5.6):
the year's improvement was the bottom tail shrinking, not the top pulling away. Candidate
mechanism (CBT rollout completion?) not yet tested.

## 4.3 Total-triage adoption (AMC reframe: "probably a function of total triage", not Anima)

Change models 2025->2026 (controls: baseline outcome, IMD, list, GP FTE, region).
Supplier-agnostic exposure - OC intake surge >=+100 subs/1k/month between fieldwork windows,
n=1,350: satisfaction -1.0, access -1.7, continuity -3.0 (all p<0.001) against a rising tide.
Per-platform between-wave adopters: Anima/Continuum (n=149) -1.6/-2.9/-5.0; SystmConnect access
-1.2; Accurx (n=284) and eConsult (n=42) null. Anima retains -2.6 access controlling for surge -
consistent with intensity-of-model (dose), though vendor effects can't be excluded.

EXPOSURE-DURATION SPLIT (prompted by AMC asking for the fieldwork dates): access penalty fades
with exposure (7-12m -0.8 / 4-9m -1.5 / 1-4m -2.2) = largely transitional; continuity penalty
does NOT fade (-2.1/-3.2/-2.9, flat). Anima's access penalty also does not fade (-3.15 at
7-12m).

PRE-TRENDS (the fourteen-year file): adopters were already declining -0.5 to -0.6pp/yr relative
to non-adopters across 2017-2023 (p<0.05), gap -2.0 (2017) -> -5.9 (2023, Anima cohort);
continuity gap -4 -> -7 pre-adoption. Parallel trends VIOLATED: adoption is selected by
struggle. The one-year penalty is ~3x the historical slope and shows as failure-to-bounce
given baselines, but all change estimates are UPPER BOUNDS on causal harm. Size decomposition
(AMC asked): adopters are bigger (13.2k vs 9.8k); size explains ~1pp of the 2023 gap of -5.8,
deprivation/region ~0.7pp; the divergence survives full adjustment (-0.35pp/yr, p=0.044).

BOUNCE-BACK (AMC): 2024->25 digital-heavy fallers (>=3pp) recovered in 2026 at the same rate as
all fallers (regression to the mean; adjusted recovery gap +0.5pp ns) and remain 2-3pp below
their 2024 baseline. DE-ADOPTION: of 1,350 surge adopters, 5 reversed - effectively a one-way
door; practice-level "try it and see" is not reversible in practice.

## 4.4 Continuity under triage is configurable (AMC: "triage might mean that people are
definitely matched to usual hcp - check")

She was right to challenge the mechanism claim. 46% of surge adopters IMPROVED continuity >2pp
(vs 49% of non-adopters) - the -3pp mean is a shifted distribution, not a universal effect.
Largest adopter gains are +38 to +51pp (from single-digit baselines to 51-81%), across Accurx,
PATCHS, Silicon AND one Anima practice - so no platform, including the worst-on-average one,
precludes rebuilding continuity. Adopter continuity-risers also gained MORE access satisfaction
(+4.6) than continuity-fallers (+1.1) - no observed trade-off. Caveats: risers had lower
baselines (29 vs 42; mean-reversion on a noisy conditional measure inflates extremes), and the
continuity question's denominator (patients with a preferred GP) can shift. Banked conclusion:
the average continuity loss under total triage is real but ROUTING-DEPENDENT - implementation
choices dominate the software.

## 4.5 Deflection: replication and the LLR test

The 3.5 inverse-care-law anatomy REPLICATES on the independently banked 2026 measure: IMD
+0.147/point (2025: +0.158), capacity -0.53/SD, GP FTE -0.69/SD, list +0.60/SD, corr with
access satisfaction -0.64. New: OC volume -0.83/SD - heavier online intake predicts LESS
deflection net of capacity. Now a two-wave replicated result.

LLR/Shepherd hypothesis (AMC: LLR ICB weighted funding toward deprived practices - is their
deflection-deprivation gradient flatter?): NO on 2026 data - level +2.4pp higher than expected
(p=0.07), gradient interaction ns, rank 31/42 ICBs; proxies agreed. Caveats: implementation
date unknown; ICB funding may not reach practice level; survey response bias. Re-test as a
gradient TREND when the 2027 wave lands.

## 4.6 The deflection tail: escape and the fourteen-year arc

Of 421 practices deflecting >=20% in 2025: 108 escaped (<10% in 2026), 200 stuck (>=15%).
Escape flow was one-directional (108 out, 15 in) - the year's improvement was tail-drainage.
Escapers vs stuck (within-tail logit): OC growth OR 1.58/SD, established OC base OR 1.64/SD,
cloud telephony OR 2.15; raw appointment growth ns once intake controlled. Escapers gained
d_acc +12.2 / d_sat +7.0 vs stuck +5.3 / +2.5 (mean-reversion inflates both; the escaped-vs-
stuck contrast is the fair one). HETEROGENEITY NOTE: OC surges predict worse experience overall
(4.3) but escape and large gains within the failing tail - digital intake helps where the front
door was already failing, and coincides with harm where it wasn't.

The stuck are more deprived than escapers (IMD 32.7 vs 27.9). Fourteen-year arc: today's stuck
cohort was already -8.4pp phone ease in June 2012, eroding monotonically every wave to -14.6
(2016), -16 (2017), -25 (2022) - no kink, a steady slide through the funding squeeze, then the
2022 demand shock landed disproportionately on them. Escapers by contrast held a FLAT mild
deficit (-4.8 to -6.6) until 2022 shocked them into the tail, and dug out in 2025-26.
LEVEL TELLS YOU WHO IS IN THE TAIL; TRAJECTORY TELLS YOU WHO GETS OUT. 194/200 stuck and
106/108 escaped trace to 2012 - the history is near-complete.

## 4.7 Whole-population trajectories

Per-practice 12-year slope of phone-ease gap vs national (>=10 of 16 waves, n=5,964): the
distribution is polarised - 2,180 practices in steep relative decline (<-0.5pp/yr), 2,619 in
steep relative rise, only ~1,150 stable. Twelve-year trajectory correlates +0.40 with 2026
satisfaction and -0.28 with deflection - among the strongest single predictors of present-day
experience we have. Steep decliners are bigger (12.0k vs 8.9k) and slightly more deprived.
Being big predicts decline (-0.85pp/yr per log-list); becoming big does not explain it (4.8).

## 4.8 Closures and growth, on real list sizes

Registered-list history (April 2013-2026) replaced the invalid survey-based size proxy (see
4.9). CLOSURES: 2,304 practices present in June 2012 no longer exist. They were SMALL - median
3,608 patients in 2013 vs 7,114 for survivors; 68% under 5k vs 29% - and their size at final
April (median 3,552) was essentially unchanged from 2013: they did not wither. Their survey
event-time profile: satisfaction gap -0.24 four years pre-disappearance, -2.0 at last
observation; phone ease ABOVE average (+3.5 -> +1.3) throughout. Practices that vanish are
small and near-average; the fourteen-year decliners persist. Failure has no exit in this
system - it accumulates in large practices that cannot close - while closure removes small,
adequate ones. (Why they closed is not observable here.)

GROWTH: 2013->2023 real list growth has no adverse association with trajectory across four of
five quintiles (shrank/flat/modest/strong all fine); only the top quintile (median +83% -
merger-scale growth) declines (traj -0.44pp/yr) and now scores worst (satisfaction 75.8,
continuity 40.2). Linear: -0.034pp/yr per +10% growth (p=6e-9) - small. The being-big gradient
survives growth control (-0.83 -> -0.75), so scale's penalty is mostly not a legacy of growing.

## 4.9 Corrections and retractions ledger (this session)

(1) "436 practices record all OC as admin" (first census) - WRONG, caught by AMC ("all labeled
0 for admin"): the file has an UNKNOWN_OTHER category I ignored; 409 practices report NO
clinical/admin split at all (Evergreen 183, Silicon/FootFall 130 - supplier pipeline gap);
only 22 have a real split that is admin-dominant. 9.4% of national weekday submissions are
uncategorised; "% clinical" is 65.9% of total but 72.8% of categorised.
(2) "Anima effect" - reframed to total-triage/intake-model effect after AMC's challenge;
per-platform tests confirmed (4.3).
(3) "Queue doesn't know your doctor" mechanism - WRONG as universal claim; AMC's challenge led
to 4.4 (continuity configurable).
(4) Surveys-distributed as size proxy - INVALID (AMC queried the "floor" claim; distributed is
~constant across all list sizes, r=-0.04 with list size; probably tracks response-rate
targeting). The interim "growth dilution dead" and "growth buys the destination penalty"
claims from that measure are both WITHDRAWN and replaced by 4.8 on real lists.
(5) 2025 deflection extraction had never been banked - now saved (4.1).

## 4.10 Files added this session

xsec_master_2026.{csv,parquet} (90 cols; explorer now serves this), wave3_gpps.csv,
gpps_long.{csv,parquet}, practice_list_history.{csv,parquet}, admin_only_oc_cohort.csv
(431 rows, two-cohort category column), did_anima_results.csv, ingest_gpps2026.py.
Explorer: six views, 2026 schema + KEY_FINDINGS 9-11, portrait template with both waves and
deflection, series-break/era-confounding guards, example chips incl. AMC's closure and merger
questions. PENDING: KEY_FINDINGS 9 amendment (exposure fade + pre-trend caveat) drafted,
awaiting AMC sign-off; CBT/phone-ease mechanism test; graveyard cause-of-closure unknowable
from these data; 2027 wave: LLR gradient trend, adopter stabilisation test (does the adopters'
gap stop widening).

## 4.11 Adoption is selected, vintage-graded, and forecastable (10 Jul 2026) - PUBLICATION TRACK

Mutually exclusive adoption waves (OC intake >=100 subs/1k/month; panel starts Apr 2023 so
pioneer adoption timing is left-censored): pioneers by Apr 2023 (n=434), surged 2023-24 (344),
2024-25 (594), 2025-26 (1,173), never (3,500). Full values in data/adoption_waves_summary.csv.

VINTAGE GRADIENT. Pioneers: large (median 11.5k), urban (90%), continuity-poor since 2012
(~31 vs never-adopters' 39) but NOT access-distressed in 2019 - predicted by structure (list
size OR 1.44/SD, urban, low continuity OR 0.77/SD; AUC 0.66), not by satisfaction gaps or
slide. Later waves flip to distress selection: the 2025-26 wave arrived with deflection 11.3%
(vs 8.5 never), phones -6.8, slide -0.4/yr. The 2023-24 wave is the anomaly - most affluent
(IMD 19.9), least declining. Two adoption regimes: workflow-for-scale first, lifeline later.
GP workforce does NOT distinguish waves: FQ GP/10k ~4.7-5.0 (2019) and ~4.5-4.8 (2026) in
every group, all losing 4-6% - adoption is about intake failure, not staffing differentials.
Within-wave variance is UNIFORM (Levene p=0.94): waves differ in means (1-3pp) not spreads
(sd ~10) - shifted distributions, not tribes; vintage says little about any single practice.

PIONEER STEADY STATE. 370/434 still heavy users (median 225/1k). Their 2026 adjusted outcomes
sit almost exactly on their pre-adoption trajectory (extrapolated -4.2, observed -4.0
satisfaction) - long-run trend-neutral - EXCEPT deflection -1.8pp better than expectation:
the one durable observable dividend of the model, landing on the worst-weighted experience.

PREDICTION (out-of-time validated). Logit trained on the 2024-25 transition (features
available beforehand: 2023 survey gaps, 2012-23 slide, real list size, IMD, GP FTE, OC base)
predicts the UNSEEN 2025-26 adopters at AUC 0.692 (train 0.668 - no overfit); decile adoption
rates 5.8% -> 50.7%. Stable drivers: list size OR ~1.5, OC-base headroom ~0.5, poor phones
~0.8. Deprivation unstable across specs - earlier "affluent adopt first" claim WITHDRAWN.
Base rate accelerating: 10.5% of pool (24-25) -> 24.0% (25-26). QRISK-style reading applies:
reliable for populations/deciles, a coin flip for individuals; better at ruling out.
data/adoption_risk_2027.csv scores all 4,057 not-yet-adopters (rank robust; absolute p
assumes next year resembles last). NOT for the public repo - internal/RCGP first.

PRE-REGISTERED DESIGN for the 2027 wave (recorded before adopters are known):
(1) 2026-27 adopters will concentrate in the top predicted deciles of adoption_risk_2027.csv.
(2) Naive adopter-vs-rest comparisons on GPPS 2027 will show deficits largely attributable
    to selection; the fair estimate matches each adopter to non-adopters with similar
    predicted probability (propensity) and similar 2012-26 trajectory.
(3) Expected under our model: year-one access-satisfaction dip attenuating with exposure;
    continuity effect heterogeneous (routing-dependent, per 4.4); deflection improvement
    concentrated in high-deflection adopters.
(4) Also due with 2027 wave: LLR deflection-gradient trend; do pioneer/early-adopter gaps
    stop widening (stabilisation test).

LITERATURE POSITION (checked 10 Jul 2026): existing work is cross-sectional GPPS x OC
(JMIR 2024), patient-level usage (OpenSAFELY 2024), single-system trend-adjusted evaluation
(NIHR). Nothing found on decade-trajectory selection into adoption, adoption vintages,
validated adoption risk scores, or pre-registered selection-corrected designs. Candidate
venues: BMJ Quality & Safety (methods/selection angle) or BJGP (substantive). AMC to lead;
analyses reproducible from repo scripts + public data.

ADDENDUM to 4.11 (10 Jul 2026, evening): practices have been contractually required to keep
online consultation tools open throughout core hours since 1 OCTOBER 2025 (25/26 access
changes) - inside the between-waves adoption window. Part of the 2025-26 surge cohort is
therefore mandate-nudged rather than purely distress-selected; the 26/27 contract (same-day
urgent duty, call-back ban, no capping) will push further. Selection regimes: structural
(pioneers) -> distress (2024-26) -> compliance (Oct 2025 onward, accelerating 2026-27).
NHSE publicly attributed the 2026 satisfaction rise to expanding online access on publication
day (Pulse, 9 Jul 2026) - a between-year national correlation credited to a tool without
adjustment for who adopted; our change models contradict the general claim and support it
only within the former high-deflection group.

## 4.12 Weighting conventions and late additions (10 Jul 2026)

WEIGHTING: published national GPPS headlines weight each PATIENT equally (survey-weighted
evaluative bases). AMC upgraded ingest_gpps2026.py to extract these bases (*_basew columns);
weighting practice estimates by gpps_n (responses) instead runs ~1.5pp HIGH vs published
figures (e.g. satisfaction 78.3 response-weighted vs 76.7 published, 2026). Use *_basew for
any figure quoted against national publications. Same-day press check: GPonline reported the
2025 baseline correctly (75.4); Pulse attributed the 2024 figure (73.9) to 2025, doubling the
apparent one-year improvement.

LATE ADDITIONS: website_easy and app_easy banked for both waves (Q2/Q3 pcteval; England means
52.1->57.6 website, 52.2->56.6 app - the survey's largest movers alongside phones, and the
items NHSE's public attribution of the 2026 improvement leans on). deflection_2025/
couldnt_contact_2025 re-banked after the ingest re-run regenerated xsec_master_2026 (the
ingest script does not yet carry them - add to QSET if re-running). Practice workload from
always-open online intake is NOT observable in any dataset here - patient experience and
practice workload need separate evidence; noted in briefing v1.1.

## 4.13 Deprecation: the "no-booking cohort" (high80) as any kind of model marker (10 Jul 2026)

The tool's notes route cited the high80 cohort (>=80% GP same-day) when a visitor asked what
proportion of practices run total triage. AMC: wrong adjacency - same-day dominance is a
booking-pattern outcome that neither implies nor is implied by triage-first working (heavy-
triage practices can book ahead extensively; recording practices can produce high80 without
any triage at all). high80 removed from the explorer schema and deprecated in the README;
retained in the data file and in earlier notes sections as historical record. The honest
answer to triage prevalence, added as KEY_FINDINGS 12: no national data identifies the model;
nearest proxy is online-intake volume (2,771/6,144 practices at >=100 subs/1k/month, Jan-Mar
2026; 58% at >=50, 29% at >=200), which misses telephone-based triage and includes non-triage
heavy users. The contract's request-level data provisions (26/27 para 15) are the first
mechanism that could make the question answerable.

AMENDMENT to 4.13: per AMC, prevalence framing reworked from arbitrary thresholds to TERTILES
(her Substack convention, consistent with oc_tertile_feb26). Jan-Mar 2026, n=6,144: low third
<33 subs/1k/month (median 15), middle 33-178 (median 76), high >178 (median 257). Presented
as a continuum, not a classification. KEY_FINDINGS 12 updated accordingly.

## 4.14 Online intake and phone volumes: partial substitution, concentrated in the 8-10am
window (10 Jul 2026; AMC's hypothesis and qualifications)

DATA: cbt_rush_panel.csv (weekday inbound calls + 8-10am calls per practice-month, Oct 2024 -
May 2026, from CBT By Day and Time files; 2024-11 and 2025-04 missing - corrupt at source) and
cbt_volumes_panel.csv (monthly totals, all 19 months). The CBT PUBLICATION began Oct 2025 but
NHSE's supplementary "historic practice level data" release extends the practice-level series
back to Oct 2024 (AMC challenged this - verified against published Oct 2025 totals, 31.44M
match). Early months cover ~2,800-3,100 practices vs ~5,000 now: the analysis sample is the
EARLY-ONBOARDED CBT estate, a supplier-patterned selection.

DESIGN: within-practice change, seasonally matched year-pairs (Jan-Mar 2025 vs Jan-Mar 2026,
n=2,839; replication Apr 2025 vs Apr 2026, n=3,005). Window choice was forced by OC data
availability at first run and retained for the seasonal match and GPPS-window alignment; the
April pair became possible when the May 2026 OC release (25 Jun) supplied the full back-series.
Exposure: OC intake tertile shift / continuous change. Controls: baseline calls/1k, IMD, list,
region.

RESULTS: tertile-up practices' weekday calls fell 81/1k/month (Jan-Mar pair; 96 April pair)
more than stable practices; tertile-down practices' calls ROSE (+20 / +8) - substitution runs
in both directions. Over half the excess fall is in the 8-10am window (-43 of -81) from a
window carrying 29% of calls; morning-rush share fell 3.1pp in tertile-up practices. Dose:
-58.6 (Jan-Mar) and -58.5 (April) calls per +100 submissions/1k - identical to one decimal.

AMC'S QUALIFICATION (central): substitution is ~0.6:1 overall and ~0.3:1 in the morning window
- roughly 40 of every 100 additional submissions are NET ADDITIONAL recorded contact volume,
not displaced calls. Cannot distinguish previously unmet demand, induced demand, and shifted
walk-ins. This is the quantitative footing for the practice-workload concern about always-open
intake, and rhymes with Newbould 2017 (telephone-first: 12-fold phone rise, +28% total
consultations). Mechanism links: explains the escape route from the high-deflection tail (3.6/
4.6), and contributes to national phone-ease improvement (+3.5pp) without workforce growth.

VISIBA WATCH: the May 2026 OC release's supplier field contains NO Visiba entry anywhere -
the platform remains wholly absent from the national collection >1 year after first
documented, while the collection has broadened (Rapid Health, Sensely now present). Wealden
Ridge shows only Accurx at 7-9 subs/1k. May 2026 OC data flagged incomplete by NHSE for Blinx,
Evergreen Life, iPlato, Silicon and PATCHS (partial submissions) - avoid May as an exposure
month.

DIARY: 30 Jul 2026 - CBT June edition adds the two contract call-waiting metrics with
practice-level time series; next OC release same week. Re-run substitution with waiting-time
outcomes; first contract-quarter read.

## 4.15 Warning signs before practice exit: a pre-closure satisfaction slide (11 Jul 2026)

Event study on gpps_long (2012-2023 per-practice satisfaction/phone/continuity). 1,987 practices
exited (last year present < 2023; closure OR merger OR sub-threshold). Gap vs same-year national
approaching exit: satisfaction -0.8 (t-3) -> -0.6 -> -1.4 -> -2.1 (final year, p<1e-16) — a monotone,
widening deficit. Phone (+3.3->+1.6) and continuity (+2.8->+0.9) sit ABOVE national throughout
(exiters are small; small = easier phones / better continuity) but erode toward exit. The satisfaction
slide runs AGAINST the small-practice advantage, so it is robust. Corrects an LLM "no warning signs"
result that was a windowing bug: the national mean was computed AFTER the group filter, so each group's
gap was a deviation from its own mean -> 0.0 by construction (survivors ~= national ~= 0). Complements
closure_exposed (neighbour-shock, sec 4-ish / line ~266): this is the exiting practice's OWN trajectory.
Consistent with the 2025->2026 spot check (gone-by-2026 practices -4.1pp satisfaction, p=0.02).
Caveats: exit pools closure/merger/list-recode; population-level signal, not an individual predictor;
gpps_long has no list size (size inferred).

## 4.16 Friends & Family Test monthly layer (11 Jul 2026)

Built fft_gp_panel (296k practice-months, 6,502 practices, Jul 2022-May 2026) from the monthly GP FFT
xlsm files (england.nhs.uk; scripts/fetch_fft.py pulls 47 months, layout-robust parser). Per practice:
fft_pct_positive (% would-recommend), fft_responses, fft_pos_roll3 (3-mo rolling); peer line =
same size-fifth x IMD-fifth over xsec UNION xsec_supplement (so supplement practices get a peer);
eng line; all response-weighted. DELIBERATELY OUT of the analytical model: self-selected, ceiling-bound
(England ~92%), gameable, ~39% of practice-months non-submission (nulls kept as gaps, never interpolated),
correlates only ~0.4 with GPPS satisfaction (0.45 at >=50 responses). Use = timeliness/monitoring between
annual GPPS waves. England %positive 87.2 (Jul22) -> 92.3 (May26), mirroring the GPPS access recovery.
Surfaced in explore.html (fft view + schema paragraph) and mypractice.html (SVG trend: you/similar/England).

## 4.17 Data-quality findings from the reproducible cross-section rebuild (11 Jul 2026)

Rebuilt the cross-section from CURRENT corrected sources (scripts/build_xsec_full.py -> data/xsec_master_rebuilt.csv;
see XSEC_REBUILD_PROPOSAL.md). Three findings:
1. WORKFORCE FTE DOUBLED in the live xsec_master: gp_fte / dpc_fte / admin_fte are EXACTLY 2x the corrected
   workforce_panel (Mar 2025 — A81001: 7.41 vs true 3.71). Original build summed the workforce file's total
   AND its component rows. So gp_per10k/nurse_per10k/etc. and any displayed staffing figure are ~2x too high;
   standardised model coefficients are unaffected (uniform scaling) but absolute staffing is wrong.
   FIX: use the corrected workforce_panel values (or halve).
2. contact_fail provenance PINNED: contact_fail = deflection_2025 + couldnt_contact_2025 (Q12_3 "told to
   contact again another day" + Q12_4 "couldn't contact at all"); corr 1.0, mean 9.9, zero diff.
3. CROSS-SECTION BUILD GAP: ~159 practices sit in xsec_supplement rather than the main master. 126 are
   spurious drops (incl A82071 Burnett Edgar) recoverable by rebuilding against the corrected panel_merged
   (the original build used a stale GPAD extract); 33 legitimately fail inclusion (21 absent from the current
   panel, 4 <=1000 appts, 8 no IMD). The rebuild reproduces 72/98 columns EXACTLY (corr 1.0); 26 columns
   need external re-linkage (NHS Payments, Fingertips, NHSBSA EPD, ODS epraccur) — in progress; not switched over.
