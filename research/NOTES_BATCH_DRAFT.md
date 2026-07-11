# DRAFT for AMC review — notes batch, 10–11 July 2026

Nothing here is banked. On approval: sections 4.15–4.24 append to PANEL_NOTES.md, the
KEY_FINDINGS block goes into explore.html, the capacity amendment into the RCGP briefing,
and this file is deleted. Three numbers from the 10 July analyses are marked [CHECK] where
the draft was reconstructed from the session record rather than the original table.

---

## A. Explorer KEY_FINDINGS (14–17)

> 14. About a quarter of calls to practices end in the automated phone system (IVR) before
> reaching the hold queue — stable nationally (26–29%, Oct 2024–May 2026) but hugely variable
> between practices (median 24%, top decile above 36%, maximum 91%). Higher IVR-ended share is
> associated with worse patient experience on every measure (phone ease −3.3pp/SD, contact
> experience −1.8, told-to-contact-again +0.8) after adjusting for queue answering, capacity,
> staffing, online intake, deprivation, size and region. What predicts a heavy IVR: list size
> (+2.8pp/SD) and calls per patient (+2.7/SD, partly reverse-causal), with a residual ethnicity
> gradient (+0.7/SD net of deprivation); online-intake volume is unrelated (r=0.005). Structure
> explains under a fifth of the variation (R²=0.18) — heavy IVR use is largely a practice
> choice. Within the heaviest users, two patterns separate: most practices' IVR terminations
> run lower at 8–10am than off-peak (automation serving prescription-line traffic), but ~800
> practices terminate more at peak, and their termination tracks demand — Monday mornings
> exceed Wednesdays by about 5pp, roughly three times the gap in ordinary practices —
> consistent with capacity-triggered message changes turning the IVR into automated deflection
> at exactly the moments patients most seek appointments. National statistics count all of it
> as "dealt with": a caller who gives up during the menus counts as dealt-with-in-IVR; one who
> gives up in the queue counts as missed. The category blends automation that served the
> patient, diversion, and abandonment, indistinguishably.

> 15. Among calls that reach the queue, the share answered runs from 45% (bottom decile of
> practices) to 95% (top); phone ease runs 47% to 75% across those deciles. Queue answering is
> unrelated to admin staffing per patient (coefficient ≈0, p=0.98) and is predicted by list
> size (about −6pp per doubling), deprivation (−0.2/IMD point), online intake (+1.5/SD) and
> IVR share (−2.4/SD — heavy IVR and poor answering co-occur). Practices combining heavy IVR
> with poor answering (n=734, mean list 14,000) score 48% phone ease; light-IVR good answerers
> (n=749, mean list 7,500) score 77%.

> 16. What predicted a practice's 2025→2026 improvement, everything competing in one model
> (2,751 phone-data practices): the event of adopting triage-first intake (−1.8 to −2.3pp
> across experience measures — the transition itself, since marginal online volume is neutral
> once adoption is flagged); improvement in queue answering (+0.5pp contact experience, −0.2pp
> deflection — the broadest lever); falls in IVR share (+1.0pp phone ease specifically); and
> admin staffing growth (+0.5pp phone ease, surviving all controls). GP staffing changes show
> small effects within the year (+0.2–0.3pp/SD, fieldwork-aligned) and larger ones over seven
> years (+0.6pp/SD); nurse and other-role changes show none at either horizon. The adoption
> penalty shrinks with baseline deflection (interaction +0.75/SD, pre-specified): transitions
> cost most where the front door already worked. NHS England's public attribution of the 2026
> rise to expanding online access is not supported at practice level.

> 17. In cross-sectional models of the 2026 survey (three outcomes: overall experience Q32,
> most-recent-contact experience Q16, phone ease Q1; ~4,700 phone-data practices, replicated
> in all ~5,900), the strongest single term is patients reporting they were told to contact
> the practice again (−4.2 to −5.9pp/SD with everything controlled), and the strongest
> positive is patients getting to see their preferred clinician (+3.0 to +3.4). With these in
> the model, the disadvantages of practice size and of heavy online intake largely dissolve —
> and deprivation's disadvantage falls from −2.3 to −0.6: deprived-area practices score worse
> substantially because more of their patients report being turned away. Practices hosting a
> GP registrar score 1.7–2.7pp higher than their staffing and circumstances predict, on all
> three outcomes, despite slightly lower continuity (registrars rotate) — replicating
> Ahluwalia et al., BJGP 2014 (doi:10.3399/bjgp14X677545), from the 2012 survey. Same-day
> booking share, the Monday answering gap, and contacts-per-appointment show no independent
> relationship with what patients report once answering, call volume and continuity are
> accounted for. Validation: the phone systems alone predict 37% of practice-level variation
> in reported phone ease — machine telemetry and survey agree about which practices are which.
> Full tables: research/predictors.html.

---

## B. PANEL_NOTES sections

### 4.15 Calls ended within the IVR: the national layer, and deflection performed by a recording (10 Jul 2026)

DEFINITIONS (CBT metadata): CBT001 inbound; CBT002 ended within the IVR prior to joining the
queue (counted "dealt with"); CBT003 answered; CBT004 ended in the queue (counted "not dealt
with"); CBT005 callback requested. The abandonment boundary is the queue join: giving up in
the menus is a success statistic, giving up on hold is a failure statistic. Reconciliation:
April 2026 components sum to inbound within 1% for 100% of practices.

NATIONAL: share ended within IVR flat at 26–29% monthly (Oct 2024–May 2026) while coverage
grew from ~2,800 to ~5,300 practices. Practice distribution May 2026 (n=4,845 after quality
filters — ≥200 inbound, IVR<95% of inbound):

| p10 | median | p90 | max |
|---|---|---|---|
| 14.8% | 24.0% | 35.8% | 91% [CHECK max — from 10 Jul table] |

PREDICTORS of IVR share (one model, ~4,800): list size +2.8pp/SD; calls per patient +2.7/SD
(reverse-causality warning: heavy IVR may suppress or inflate measured calls); non-white %
+0.7/SD net of IMD; IMD itself non-monotonic (AMC's observation); OC volume null (r=0.005,
checked both raw and per-1,000). R²=0.18 — structure explains little; the residual is
configuration choice.

EXPERIENCE: adjusted for answering, capacity, staffing, OC, IMD, size, region: phone ease
−3.3pp/SD, contact experience −1.8, deflection +0.8. (Superseded scale: the 11 Jul final
specification, §4.22–4.23, retains an independent IVR term on all outcomes.)

TIME-OF-DAY (May 2026 day/time files, bank-holiday Mondays excluded): the typical practice
ends more calls in the IVR outside the 8–10am rush (median tilt −4.1pp) — the automation
signature. About one practice in five shows the opposite, morning-heavy pattern (>5pp excess
at 8–10). In that group the morning excess tracks demand: Monday-morning IVR share exceeds
Wednesday-morning by 2.9pp median (under 1pp elsewhere); in the original March analysis the
Monday premium was ~+4.9pp vs Wednesday in the 819 morning-excess practices [CHECK exact
March values]. Mid-morning message-switching was tested and refuted: IVR rates fall after the
rush rather than rising, deflection operates at 8am itself; secondary observations: a lunch
bump (12–14h) and an 18:00–18:30 spike of 33–36% [CHECK] within core hours. A fixed
prescription-line IVR has no reason to know what day it is; a message that changes when the
day's capacity is gone does. Capacity-responsive messaging is the parsimonious mechanism —
deflection performed by a recording, counted nationally as dealt with. Limits: outcomes
observed, not message content; confirmation would need mystery-calling or supplier data.
(11 Jul addendum: mypractice.html now invites morning-heavy practices to report what their
menus play; and §4.24 finds no same-day capacity difference in GPAD for this group.)

### 4.16 Queue answering, and what predicted the 2025→2026 improvement (10 Jul 2026)

LEVELS: queue-answer rate runs 45% (bottom practice decile) to 95% (top); phone ease 47→75%
across those deciles. Predictors: size −6pp per doubling; IMD −0.2/point; OC +1.5/SD; IVR
share −2.4/SD. Admin staffing per patient: null (β≈0, p=0.98), flat across the entire
staffing range (developed further 11 Jul, §4.18–4.19). Cross-tab: heavy-IVR poor-answerers
(n=734, mean list 14,000) 48% phone ease vs light-IVR good-answerers (n=749, mean list 7,500)
77%.

CHANGE 2025→26 (one model, 2,751 practices, Dec 2024–Dec 2025 workforce aligned to
fieldwork): adoption of triage-first intake −1.8 to −2.3pp (the event; marginal volume
neutral); Δanswering +0.5pp contact experience, −0.2pp deflection; ΔIVR −: +1.0pp phone ease;
Δadmin +0.5pp phone ease (survives all controls). ΔGP +0.2–0.3pp/SD in-year; 7-year ΔGP
+0.6pp/SD; nurses/DPC null at both horizons. Pre-specified interaction: adoption × baseline
deflection +0.75/SD — transitions cost most where the front door already worked.

METHODS LESSONS (AMC corrections): fieldwork alignment matters — the misaligned 14-month
window attenuated the GP effect (+0.15 ns → +0.23 p=0.036 when Dec–Dec aligned); admin
mediation — practices growing admin also answered better, and admin's satisfaction effect
collapses when Δanswering enters (+0.29 → +0.14 ns), while its phone-ease effect survives.

WORKFORCE CORRECTIONS (verified): fully-qualified GP FTE per patient −6.4% (2019→Mar 2025),
+2.5% (2025→May 2026), net −4.0% vs 2019; the rise recovers 37% of the fall in one year.
Sensitivity to September-2019 list denominators: −5.9/−3.6. 2019 figures are the archived-
methodology series. Withdrawn en route: a "4–6%" hedge and a "small uptick" characterisation
(2.5% against a 6.4% fall is not small).

ATTRIBUTION: NHSE's public claim that expanding online access drove the 2026 rise is
unsupported at practice level; operational phone changes and the rescue of previously-failing
practices carry the improvement.

### 4.17 Monday supply flex, contacts per appointment, and levels of inference (10 Jul 2026)

SUB-ICB DAILY (GPAD daily, sub-ICB only): Monday demand index 1.40 vs supply 1.12 (same-day
bookings 1.34 act as the shock absorber). Areas whose supply flexes least show the largest
Monday answering collapses (r=+0.41 with the flex gap); the chain does not reach area-level
satisfaction. Practices whose answering collapses run afternoon gaps of −14.5pp at 1.37×
volume (~3× national) — consistent with the exhaustion hypothesis (answering stops when slots
are gone); the discriminating data (slot exhaustion time) is unpublished.

CONTACTS PER APPOINTMENT (May 2026 build: CBT inbound + OC submissions ÷ GPAD appointments):
median 1.48 (Mar) / 1.47 (May); practice-level associations (−1.26 phone ease/SD) die at area
level. (11 Jul: in the final specification with calls per 1,000 separated, CPA shows no
independent relationship with any outcome — reclassified on mypractice.html from flag to
demand diagnostic; the capacity-proxy intent failed.)

PROVENANCE/LEVELS: CBT is practice×day; GPAD daily is sub-ICB only; GPAD practice data is
monthly; supply→answering inference is area-level only. Area aggregation validated: national
GPPS reproduced to 0.05pp with base weights; ICS approximate (36 rows = ICB mergers;
geography vintage ±1pp).

### 4.18 Admin staffing in levels: unrelated to answering; related to satisfaction only in small and medium practices (11 Jul 2026; AMC challenge)

[As approved in chat 11 Jul, with the amended reading]

DATA: May 2026 CBT (queue-answer = answered/(inbound−IVR), capped 100; ≥200 inbound,
IVR<95%); xsec admin_fte per 10,000 (GP Workforce Mar 2025); satisfaction_2026, gpps_n≥30.
Admin fifths (per 10,000): ≤17.5 / 17.5–21.7 / 21.7–25.3 / 25.3–30.0 / >30.0.

ANSWERING (median queue-answer rate; grid cells n=148–240):

| | Fewest admin | 2nd | Middle | 4th | Most | Most−fewest |
|---|---|---|---|---|---|---|
| All | 84.1 | 82.6 | 81.0 | 81.4 | 81.8 | −2.3 |
| Smallest fifth | 86.3 | 88.5 | 87.3 | 87.7 | 88.5 | +2.2 |
| 2nd | 85.8 | 84.7 | 83.2 | 85.3 | 81.6 | −4.2 |
| Middle | 82.5 | 82.0 | 82.0 | 83.2 | 80.1 | −2.4 |
| 4th | 82.4 | 81.7 | 80.0 | 78.5 | 79.1 | −3.3 |
| Largest | 79.5 | 77.2 | 73.1 | 69.5 | 70.1 | −9.4 |

SATISFACTION (mean % good overall experience; cells n=189–330):

| Size fifth | Fewest | 2nd | Middle | 4th | Most | Most−fewest |
|---|---|---|---|---|---|---|
| Smallest | 78.5 | 79.4 | 80.8 | 82.7 | 83.0 | +4.5 |
| 2nd | 77.8 | 78.9 | 78.7 | 80.8 | 81.9 | +4.1 |
| Middle | 76.3 | 77.6 | 77.5 | 79.5 | 79.1 | +2.8 |
| 4th | 75.4 | 77.4 | 77.1 | 77.0 | 76.6 | +1.2 |
| Largest | 74.2 | 76.3 | 76.7 | 74.6 | 73.9 | −0.3 |

WHAT HIGH-ADMIN LARGE PRACTICES ARE (largest fifth by admin fifth; medians, n=181–206):

| | Fewest | 2nd | Middle | 4th | Most |
|---|---|---|---|---|---|
| GPs/10k FTE | 9.1 | 11.1 | 11.9 | 12.1 | 12.5 |
| Nurses/10k | 3.0 | 4.2 | 5.2 | 5.9 | 7.3 |
| Other clinical/10k | 2.6 | 4.0 | 5.1 | 5.7 | 8.8 |
| Appts/1k/month | 386 | 442 | 464 | 490 | 539 |
| Inbound calls/1k/month | 384 | 414 | 438 | 450 | 486 |
| Callback requests % | 6.6 | 6.3 | 7.4 | 7.7 | 9.5 |
| IMD | 20.8 | 17.4 | 17.3 | 20.1 | 21.2 |
| Queue-answer rate | 79.5 | 77.2 | 73.1 | 69.5 | 70.1 |

READING: among the largest practices, admin staffing marks overall intensity — more staff of
every kind, more appointments, more calls per patient at similar deprivation. AMC's
substitution hypothesis (more admin, fewer doctors) is rejected by the first row. Their flat
satisfaction (−0.3) fits resources absorbed by demand. In smaller practices admin accompanies
satisfaction (+2.8 to +4.5) without accompanying answering — candidate channels (reception
interactions, administrative reliability, marker of resource) indistinguishable here.
CAVEATS: ecological; Mar 2025 census vs May 2026 phones; no role breakdown.

### 4.19 The admin residual: a null-hunt, and the scale question it opened (11 Jul 2026)

Conditional on co-staffing and circumstances, admin flips negative (alone +0.97/+0.85 →
combined −1.06/−1.11 on Q32/Q16; −0.39/−0.34 in the final specification with patient-reported
measures). Candidate explanations tested and rejected:

| Test | Result |
|---|---|
| Phone workload: add calls per 1,000 to model | admin −0.84 → −0.87 (unmoved); calls/1k itself +1.14 |
| Reception quality: Q4 helpfulness (median 87.3%, p10 73.9, p90 95.8) | admin→helpfulness +1.00 alone, −0.18 ns conditional; adding helpfulness moves admin −0.84 → −0.67 only |
| Admin × OC processing (AMC hypothesis) | ns on experience (−0.18/−0.09); marginal on answering only (−0.42, p=0.039, multiplicity), vanishes with calls/1k controlled |
| Admin × size | −0.29 (p=0.011) / −0.53 (p<0.001) — concentrated in large practices — but dissolves once continuity enters (§4.20: −0.01/−0.19 ns) |

Side-findings: conditional on answering, the strongest operational correlate of patients
calling the reception team helpful is the answer rate (+1.48); helpfulness↔overall experience
+7.9 (R² 0.26→0.69) is common-source and not treated as causal.

SCALE: the answering disadvantage of size (−6pp/doubling) is not attenuated by staffing,
call volume, or deprivation, and is present in practices without recorded local closure
exposure (weak proxy — ODS succession data is unusable; closure_exposed n=212, true absorbers
n=7; absorbed/exposed large practices answer worst of all — largest fifth 64.3% vs 74.1%
organic, n=49 vs 1,152 — but are too few to carry the gradient). Queueing theory predicts the
opposite at equal staff-to-demand ratios (pooled queues are more efficient; citation to be
verified before external use). Resolution came from §4.20: with continuity and the phone
measures controlled, size ≈ 0 — the scale disadvantage decomposes into lost continuity and
unanswered calls, and little else.

### 4.20 Continuity enters the models — and dissolves the size and online-intake disadvantages (11 Jul 2026; AMC: "we have lost continuity out")

Q6 "Is there a particular healthcare professional you usually prefer to see?" (% yes; median
32.4%) and Q7 "How often do you get to see or speak to your preferred healthcare professional
when you ask to?" (% always/a lot; median 41.5%, p10 20.9, p90 66.6).

| (Q32 / Q16) | Alone | In full model |
|---|---|---|
| Q7 see preferred clinician | +5.80 / +7.06 | +4.45 / +5.44 (pre-deflection spec) |
| Q6 have preferred clinician | +2.26 / +2.39 | +1.17 / +0.61 |
| R² | | 0.27/0.30 → 0.44/0.47 |

What moved: size −1.59/−2.24 → −0.28 ns/−0.78; OC −1.54/−2.10 → −0.38/−0.84; same-day share
flips positive (+0.38/+0.44); admin×size dissolves. Mediation reading (cautious): much of the
cost of being large, or of moving intake online, is the continuity that tends to be lost with
both — and continuity is an allocation choice (cross-ref event-study sections: 46% of
online-movers improved it, on every platform). Common-source caveat: Q6/Q7 share respondents
with the outcomes.

### 4.21 Training practices score higher than their circumstances predict (11 Jul 2026; AMC variable)

Derivation: trainee FTE = all-GP FTE − fully-qualified FTE, March 2025 census; "training
practice" = trainee FTE > 0.25 (59% of practices; a placement snapshot, not accreditation —
misses accredited practices between placements). GP staffing split into fully-qualified and
trainee per 10,000.

| (Q32 / Q16 / Q1 phone ease) | Alone | Together | + patients report |
|---|---|---|---|
| Training practice | +1.68 / +0.76 / −4.09 | +2.37 / +2.65 / +2.66 | +1.86 / +1.96 / +1.94 |
| Trainee GPs per 10k | +1.49 / +1.36 / +0.90 | +0.37 / +0.30 ns / +0.29 ns | +0.69 / +0.60 / +0.66 |
| Fully-qualified GPs per 10k | +3.00 / +2.96 / +3.40 | +1.74 / +1.61 / +1.63 | +0.92 / +0.67 / +0.54 |

The alone/together reversal on phone ease (−4.09 → +2.66) is size: training practices are
large, and being large pulls raw scores down. Twist: trainee staffing predicts LOWER
continuity (−1.16/SD; fully-qualified +2.01) — the training advantage is not through
continuity but despite it. Reading: accreditation marks organisational quality the other
variables cannot see. Prior: Ahluwalia et al., BJGP 2014, doi:10.3399/bjgp14X677545 —
training status (29% of practices, 2011/12, accreditation-defined) predicted doctor-care and
overall-satisfaction GPPS domains. mypractice.html shows each practice its designation and
invites correction.

### 4.22 Deflection enters the models: the strongest term, and deprivation's disappearing act (11 Jul 2026)

Q12-derived: % told to contact the practice again another day.

| (Q32 / Q16) | Alone | Full model (with continuity + everything) |
|---|---|---|
| Deflection | −6.22 / −8.00 | −4.20 / −5.93 |
| R² of model | | 0.540 / 0.621 (n=4,715); all-practices 0.535/0.609 (n=5,871) |

DEPRIVATION COLLAPSE: IMD −2.29/−2.45 alone → −0.57/−0.77 with the patient-reported measures
in. Deprived-area practices score worse substantially because more of their patients report
being turned away — relocating much of the deprivation gap from demography to demand meeting
capacity. SIZE (final): −2.31/−3.33 alone → −0.38/−0.93.

NOT CAPACITY-DETERMINED: deflection spread among the most pressured practices:

| Reported deflection 2026 | p10 | median | p90 | n |
|---|---|---|---|---|
| All practices | 1.2% | 5.8% | 15.0% | 5,941 |
| Fewest-FQ-GPs fifth | 2.2% | 7.8% | 16.6% | 1,189 |
| Fewest GPs AND most deprived | 3.4% | 8.9% | 19.0% | 326 |

A tenth of the most pressured practices keep it below the national median; a tenth exceed
19%. What separates them is unmeasured (the survey does not record what is offered when no
slot is left).

### 4.23 Do patients' reports measure what the machines measure? (11 Jul 2026)

CONVERGENT VALIDITY — phone data alone (answering, IVR, morning pattern, calls/1k, size)
predicting each reported phone question (n=4,550):

| Outcome | R² | answering | IVR share |
|---|---|---|---|
| Phone ease (Q1) | 0.370 | +6.53 | −4.20 |
| Deflection (Q12) | 0.101 | −0.97 | +0.99 |
| Couldn't contact at all | 0.049 | −0.17 ns | +0.23 |

Phone ease is the survey's mirror of the telemetry — validating both datasets at once.
Couldn't-contact is floored (median practice 0.0%) and unusable at practice level. Deflection
is only weakly phone-shaped; everything external predicts R²=0.210 of it (full table on
predictors.html), led by IMD +1.10, answering −0.90, IVR +0.70, FQ GPs −0.47 — patients
partly report what the machines record, plus desk behaviour no dataset measures. Notable
sign: the morning-heavy IVR pattern predicts LESS reported deflection (−0.25), not more —
fits redirection rather than told-to-call-back.

OVER-ADJUSTMENT EXHIBIT: adding phone ease as a predictor of experience inverts the
operational coefficients (answering −0.75, IVR +0.46, size +0.78; R² 0.69/0.80) — absurd, and
diagnostic: it re-measures the phone construct, so it serves as an outcome, never an input.
Q12/Q7 predict legitimately because they record events no machine sees. R² caution: models
containing same-source reported measures roughly double R² (0.275→0.54+); the 0.275 from
purely external data is the demanding benchmark.

### 4.24 Morning-heavy IVR practices do not lack recorded same-day capacity (11 Jul 2026; AMC hypothesis, informative null)

| May 2026 medians | Morning-heavy (n=924) | Even (n=1,734) | Rest-of-day (n=2,212) |
|---|---|---|---|
| Same-day GP appts /1k | 107.7 | 103.0 | 107.5 |
| GP same-day share | 54.3% | 52.5% | 55.7% |
| All same-day /1k | 183.7 | 178.7 | 182.9 |
| Calls /1k /month | 549 | 473 | 538 |
| % calls at 8–10am | 27.6% | 24.2% | 27.0% |

Adjusted (size, IMD, GP staffing): morning excess ↔ same-day GP appts +0.005 SD (p=0.72);
Monday-morning IVR premium ↔ same: −0.004 (p=0.78). Either the messages are less
capacity-triggered than the timing suggests, or — more likely — GPAD measures appointments
DELIVERED, not slots OFFERED: a book exhausted at 8:40 and one with noon slots free deliver
identical same-day counts. The discriminating variable is slot-exhaustion time, which exists
only in practice appointment books: the first question this programme cannot answer from
public data, and the concrete case for Tier 2 of the practice tool.

---

### 4.25 Data-quality incident: the corrupt panel CSV and the 96 missing practices (11 Jul 2026; found via AMC's N81086 report)

xsec_master_2026 silently excludes 96 practices with usable 2026 survey records (base ≥30) —
N81086/Wilmslow among them (overall experience 88.8% → 81.2%, full CBT and GPAD histories).
ROOT CAUSE: build_xsec.py reads panel_merged.CSV, not the parquet. The CSV was doubly broken:
~4,100 rows had unquoted commas in supplier names (splitting columns), and the file was stale
and truncated — at discovery it parsed to 83,870 rows / 2,208 practices against the parquet's
242,345 / 6,386. Practices whose exposure-window rows fell on broken lines dropped below the
build's 1,000-appointment threshold and out of the universe. All analyses in these notes used
the parquet directly and are unaffected; the damage is confined to cross-section membership
(all model n's ~2% short). ACTIONS: (a) CSV regenerated from the parquet with proper quoting,
11 Jul; (b) mypractice.html given a supplement file (xsec_supplement.csv, 159 practices from
the raw GPPS + panel) so affected practices get a reduced page with an honest banner instead
of an error; (c) at the 30 July rebuild, build_xsec.py switches to the parquet, the
cross-section is rebuilt survey-first with left joins, and the predictors page reruns.
LESSON: never maintain a CSV twin by separate writes; derive it from the parquet or not at all.
DESIGN PRINCIPLE (AMC): absence of a survey year is never a failure condition. The rebuilt
cross-section's universe is the union of sources (GPPS any year, GPAD, CBT, workforce, ODS),
with every join a left join and every comparison degrading gracefully. Practices with no
survey at all still get their operational page — which requires a practice-name source
independent of the survey files (ODS epraccur) in the rebuild.

### 4.26 Medicus joins Visiba: the invisible-supplier watch (11 Jul 2026; AMC local knowledge via N81086)

N81086/Wilmslow ran Accurx at 280–320 submissions/1,000/month (among the heaviest in England)
until May 2025, then shows "No Data" in the OC collection for twelve consecutive months —
coinciding, per AMC, with a move to Medicus. Over the same period their weekday calls per day
roughly halved (430→260 Mondays) and Monday queue answering rose 66.7%→81.7%: the substitution
signature of §4.14 operating at full strength while the national collection records zero.
The mechanism differs from Visiba's (AMC correction). Visiba is a dedicated OC platform that
never joined the OC collection. Medicus is a core clinical system — a named, participating
GPAD supplier alongside EMIS and TPP (GPAD May 2026: "EMIS, TPP, …, Medicus, Evergreen Life
and Archvale") — that includes OC functionality within the core system. Wilmslow's move was a
clinical-system migration, not an OC-platform switch, and their appointment data flowed
uninterrupted through it. The blind spot this exposes: as core systems absorb OC functionality, that
activity can leave the collection — the undercount growing with exactly the practices making
the deepest digital moves. It is not structural: TPP's built-in OC (SystmConnect) reports to
the collection and appears throughout our event studies (AMC's observation) — so core-system
OC is onboardable, and Medicus's absence is an onboarding gap, not an impossibility. Enumerating the Medicus estate needs a supplier-per-practice source;
check whether the GPAD practice files expose one at the 30 July release. NATIONAL SCAN:
practices with recorded OC in Jan–Apr 2025 and ≥7 of 8 dead months Sep 2025–Apr 2026 — 18
total, 6 of them previously ≥100/1,000 (5 ex-Accurx, 1 ex-Klinik at 323/1,000). Small so far,
but each such practice enters every model as zero online intake while actually running a heavy
online front door — a misclassification that attenuates OC coefficients and, at scale, would
corrupt the national series. WATCH: recount at each OC release; the tool's transition card and
OC covariates treat "No Data after recorded intake" as missing, not zero, from the rebuild.

### 4.27 Closure warning signs (10 Jul 2026; COMPANION SESSION — its figures, its transcript holds the tables)

Event study on gpps_long 2012–2023: practices that subsequently exited show a monotone,
widening satisfaction deficit over their final three years — −0.8pp → −2.1pp against the
same-year national figure (p<1e-16). Their phone-ease and continuity sit ABOVE national
(small-practice composition) but erode toward exit. This corrects an earlier "no warning
signs" result traced to a windowing bug. (Companion session proposed this as §4.15; renumbered
here to avoid collision with the IVR section.)

### 4.28 Practices raising f2f against the national tide gained satisfaction (10 Jul 2026; COMPANION SESSION)

Cohort n=884 (f2f_increaser_cohort.csv); windows Jan–Feb 2024 vs Jan–Feb 2026,
fieldwork-aligned. Satisfaction gains robust to Δappointments/patient AND ΔGP-FTE/10k
(corr(Δf2f, ΔGP-FTE) = −0.01 — not a staffing artefact); GP capacity retains its own separate
positive effect. Horse race: GP-delivered f2f +0.42/SD against other-staff f2f +0.28/SD, both
independently significant. Two-wave check (2025 vs 2026): driver set essentially unchanged
(GP FTE +, deprivation −, size −, phone-ease dominant; same-day share a non-predictor both
years); continuity +1.5pp nationally while has-preferred fell −0.9pp — the pool wanting
continuity is shrinking.

### 4.29 Anima/Continuum adoption DiD: selection on trajectory, not demonstrated harm (10 Jul 2026; COMPANION SESSION)

Three estimators (unadjusted / adjusted / propensity-matched; did_anima_results.csv). Matched
DiD suggested worse satisfaction/access/continuity, BUT parallel trends fail: adopters were
already declining pre-adoption (satisfaction PRE −1.6 vs POST −0.9; continuity PRE −1.9 vs
POST −2.8). Honest read: selection on trajectory; no demonstrated satisfaction harm;
continuity may take an incremental hit on an already-falling path. Adopter flag
(latest-month Continuum) likely misclassifies mixed-supplier practices — supplier-field
opacity again (cf. §4.26).

### 4.30 Workforce panel data note (10 Jul 2026; COMPANION SESSION)

workforce_panel.{csv,parquet}: per-practice GP/nurse/DPC/admin FTE + patients, 32 quarters
2018–2026, 7,352 practices. CAVEAT: its gp_fte is TOTAL GP FTE (including registrars and
locums); fully-qualified (EXRL) is captured only for 2018 (NHS renamed the column). National
total GP FTE/10k rose 4.8→6.0 over the panel — registrar-driven, consistent with §4.21. This
file is DISTINCT from practice_workforce_2019_latest.csv (used for §4.21's fully-qualified/
trainee split); do not mix their GP definitions. LOCUM BOUNDARY (11 Jul, AMC query): the
census's fully-qualified GP FTE — and therefore our models — INCLUDES regular locums (vacancy/
absence/other cover; ~580 FTE nationally, <2% of fully-qualified) and EXCLUDES ad-hoc locums
entirely, which NHS England reports only in national annexes. Ad-hoc locum reliance is
invisible at practice level in all published data. Optional test (detailed practice file has
TOTAL_GP_LOCUM_*_FTE): whether locum-heavy FTE predicts lower continuity per GP — 30 July list.

### 4.31 GP composition: partners, salaried, locums, trainees (11 Jul 2026; AMC — locum query led here)

DATA: March 2025 census detailed practice file. Partners = senior partners + partner/providers;
salaried incl. salaried-by-other-orgs + retainers; regular locums = vacancy/absence/other cover
(ad-hoc locums NOT published at practice level — invisible everywhere, §4.30); trainees = all
training grades. Medians per 10,000: partners 2.55, salaried 1.56, locums 0.00, trainees 0.90.
Only 10% of practices carry >0.25 FTE regular locum (median 0.73/10k where present).

ALONE (bivariate, CBT sample n=4,736):

| per SD FTE/10k | Q32 | Q16 | Q1 phone ease | Q7 continuity* |
|---|---|---|---|---|
| Partners | +2.55 | +2.60 | +3.79 | +3.68 |
| Salaried | +0.93 | +0.79 | −0.17 ns | −0.98 |
| Regular locums | −0.30 ns | −0.21 ns | +0.47 ns | +0.10 ns |
| Trainees | +1.44 | +1.29 | +0.73 | — |
(*continuity alones from the first-pass sample n=5,919)

FULL MODELS (page specification; Together = external only; +Report adds Q6/Q7/Q12):

| | Q32 Tog / +Rep | Q16 Tog / +Rep | Q1 Tog / +Rep |
|---|---|---|---|
| Partners | +1.68 / +0.55 | +1.53 / +0.31 | +1.71 / +0.32 ns |
| Salaried | +1.42 / +0.96 | +1.29 / +0.71 | +1.19 / +0.52 |
| Regular locums | +0.28 ns / +0.15 ns | +0.21 ns / +0.05 ns | +0.19 ns / +0.01 ns |
| Trainees | +0.12 ns / +0.65 | +0.09 ns / +0.63 | −0.00 ns / +0.70 |
| Training flag | +2.79 / +1.89 | +3.05 / +1.90 | +3.41 / +2.06 |
All-practices replication (n=5,913): same pattern throughout.

CONTINUITY (Q7) AS OUTCOME, full external spec (n=4,790, R²=0.233): partners +2.45, salaried
+1.03, locums +0.33 ns, trainees −2.07, training flag +2.16.

READINGS: (1) Regular locums null on every outcome in every specification — but a thin variable
with the ad-hoc invisibility caveat; absence of evidence. (2) Partners and salaried GPs
near-equal on experience gross but travel by different roads: partners' association collapses
when continuity is controlled (+1.68→+0.55) — partners deliver experience through being
seeable-again — while salaried persists (+1.42→+0.96). (3) Trainee FTE adds nothing beyond the
training flag externally; the flag was carrying the §4.21 trainee story. (4) The continuity
model's paradox: training practices are continuity-POSITIVE (+2.16) while trainee FTE drags it
(−2.07) — organisational quality showing twice. (5) Composition sentence for the wider
argument: as the workforce shifts from partners toward salaried and sessional models, the thing
specifically at risk is continuity — the strongest single correlate of overall experience.
PAGES: predictors.html rebuilt on the composition split (n=4,736/5,913); mypractice.html
capacity card now shows each practice its GP mix vs the typical practice.

---

## D. The 30 July 2026 rebuild list (consolidated, both sessions)

1. Rebuild xsec_master survey-first with left joins, reading the PARQUET panel (never the
   CSV); recovers the 96/159 orphaned practices (§4.25); add an ODS-derived practice-name
   source so no-survey practices still render on mypractice.html.
2. Rerun the predictors-page models on the rebuilt cross-section; refresh all page tables.
3. OC covariates and the tool's transition card: treat "No Data after recorded intake" as
   missing, never zero (§4.26); check whether GPAD practice files expose supplier-per-practice
   to enumerate the Medicus estate; recount the vanished-practice scan.
4. CBT June edition: practice-level call-waiting times → phones card, summary, and the test
   the phone-ease size gap is waiting for (§4.23); first contract-quarter read.
5. GPAD June edition: contract metrics at practice level (clinically-urgent same-day,
   non-urgent within 7/14 days) → candidate tool measures.
6. Ingest hygiene (companion session): fold website_easy/app_easy/deflection_2025/
   couldnt_contact_2025 into ingest_gpps2026.py's QSET and dedupe the two ingest versions
   before any re-run; optional EXRL (fully-qualified) column mapping post-2018 in
   workforce_panel; optional exact *_basew weighting for explorer benchmarks.
7. README: one-line description for adoption_risk_2027.csv (now deliberately public).
8. Re-run the §4.14 substitution analysis with waiting-time outcomes (standing diary item).
9. From first user feedback (see E): latest-census — DONE for the tool same day (31 May 2026
   census now drives the capacity card; the *models* still use March 2025 workforce inputs and
   should move to the latest census at the model rerun); evaluate FFT monthly
   practice data as a year-aggregated satisfaction comparator alongside GPPS; test
   waiting-time bands × continuity (the "our favourite GPs have longer waits" trade-off) at
   practice level; re-derive the model training flag as ST-registrar-only (67 practices
   reclassify; effect on coefficients expected negligible but must be verified).
   (Similar-practices staffing column: done same day.)
10. Refresh research/data/list_jul26.csv from the monthly Patients Registered publication at
    each rebuild (it is a 1st-of-month snapshot; the filename should probably become
    list_current.csv with a date column so the page label can be generated, not hard-coded).
11. Consider the March–May averaging window for the CBT terms in the predictors models too
    (the page benchmark now averages the quarter; the models still use single-May inputs).

## E. First user feedback (11 Jul 2026, via AMC) — and actions

A practice manager reviewing their page raised six points. Actioned same day:
training-practice designation wrongly counted foundation doctors (their practice hosts F1/F2
and students, no registrar) — flag re-derived as ST1–ST4 only, 67 practices reclassified,
foundation/other grades now a separate card row; nurse/other-clinical/admin rows failed for
cross-section orphans — all staffing now sourced from the census composition file; a
waiting-times card added (same-day / 1–7 / 8–14 / 15+ day bands vs the typical practice),
with the honest note that per-clinician waits are unpublished so the continuity-versus-speed
trade-off is invisible in national data. Deferred to the rebuild (D.9): census vintage,
similar-practices staffing comparators, FFT evaluation, waits × continuity. The feedback
channel works.

Second round (11 Jul 2026, same practice + A82071), actioned same day: **registered
population was stale and unlabelled** — the page showed the 2024/25 exposure-year *average*
list (A82071: 4,216 shown vs 4,099 registered on 1 July 2026 — "about 100 less", exactly as
the practice said). Fix: research/data/list_jul26.csv (6,139 practices, NHS Patients
Registered snapshot, 1 July 2026) is now the registered-population figure everywhere on the
page — identity line (with source and date shown), staffing rates, calls per 1,000, and all
size-fifth placements including peers' (COALESCE to the 24/25 average for the 21 practices
absent from the snapshot). The 15-month gap between the March 2025 staffing numerator and the
July 2026 list denominator is stated on the capacity card. **Phone measures were single-month
(May)** — one clinician's leave or a rota gap coloured the whole card. Fix: the phone
benchmark now averages March–May of each year (counts summed, so ratios are volume-weighted;
eligibility ≥200 inbound/month on average; n=4,930, of which 3,088 have a year-before
average). April 2025 is not in the published collection, so the 2025 column is a
March+May average — stated on the card. The day-of-week card stays May-only (it is about
within-week pattern); the demand card stays May-vs-May (its appointment and OC comparators
are May); the predictors models still use single-May CBT inputs (D.11).

Same day, AMC: "why are we using March 2025 staffing?" — no reason; the census is monthly.
The capacity card now uses the **31 May 2026 census** (gp_composition_may26.csv; raw
publication files kept locally in data/gpw_may26/, gitignored), so staffing, appointments and
phone data share a vintage and the July 2026 list denominator is five weeks away rather than
15 months. Training designation is now **registrar in post in either March 2025 or May 2026**
(>0.25 FTE ST1–ST4): rotations mean a single month can miss a genuine training practice, and
the either-rule catches 243 practices the May census alone would misclassify. National share
under the either-rule: 61% (card updated from "56% do"). Reconciliation: practice-file FTE
totals come in slightly under the bulletin (37,975 vs 38,821 GP FTE) because the
practice-level CSV excludes fully-estimated records — expected, per the publication notes.
A82071 under the new census: 0.93 partner + 0.57 salaried + 1.07 foundation FTE, no
registrar, not training — matching the practice's own description (F1/F2 and students, no
registrars).

---

## C. RCGP briefing capacity amendment (replaces the current bullet's final sentences)

> Fully qualified GP capacity per patient fell about 6% between 2019 and early 2025, then
> rose 2.5% in the year to May 2026 — recovering over a third of the loss in a single year
> and leaving capacity about 4% below its 2019 level. Changes in a practice's GP and
> administrative staffing, measured at survey fieldwork, show small positive associations
> with experience change within the year; operational changes to phone systems carry effects
> three to four times larger over the same period; and seven-year staffing change predicts
> experience durably. The 2026 improvement is operational in character; the workforce turn,
> if sustained, is what the longer-run evidence says will consolidate it.

---
## COMPANION-SESSION ADDITIONS — pending merge into section B (from PANEL_NOTES, 11 Jul 2026)

These were appended directly to PANEL_NOTES by the companion session before this draft's staging
workflow was known; moved here for the single review. On review, RENUMBER into section B and DEDUPE:
- '4.15 Warning signs before practice exit' overlaps the stubbed draft 4.27 (closure) -- merge, keep the table below.
- '4.16 FFT monthly layer' is NET-NEW (no FFT section in the draft yet).
- '4.17 data-quality / rebuild' overlaps draft 4.25/4.30 and section D -- the WORKFORCE-DOUBLING (2x) finding,
  the contact_fail = deflection+couldnt composite, and ae_pop = ae_after_fail x contact_fail/100 are NET-NEW.
- '4.18 / 4.18.1' (deprivation gradient; deflection-by-condition; deflection vs diversion) is NET-NEW and
  complements draft 4.22 (which is the regression-model version) -- the individual-level equity crosstabs.

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

## 4.18 The deprivation gradient: deflection + diversion, and a need-vs-capacity decomposition (11 Jul 2026)

Individual-level national crosstabs (GPPS analysis tool, by IMD quintile) + practice-level decomposition.
Purpose: decide which experience items are worth showing (see 4.16/decision) AND probe the access-model equity story.

DEPRIVATION-GRADIENT MAP (individual-level, most vs least deprived, GPPS 2026, all 27 questions screened):
- Service-experience measures uniformly but MODESTLY worse in deprived (~3-7pp): website +7, contact exp +6,
  continuity +6, reception +5, listening +5, overall exp +5, involved +5, phone/app +3, trust/info +3.
- The BIG gaps are patient need/capability, NOT service: confidence to self-manage +13 (71 v 84),
  enough support to manage conditions +11 (64 v 75), conditions-limit-daily-life -18 (71 v 53; more in
  deprived = the morbidity gradient itself).
- Mental wellbeing (Q26) FLAT (75 v 75) -- cross-validates the practice-level r=-0.03; the one experience
  item not deprivation-confounded (see 4.16: the fair item to feature).
- Reversed: appointment-was-remote HIGHER in deprived (29 v 23) -- deprived get more remote, less f2f.
- Dental strongly inverse-care (got appt +9, experience +8) -- pattern spans services the GP does not run,
  supporting the pharmacy/dental-as-respondent-disposition control idea.

DEFLECTION + DIVERSION (practice-level, by IMD quintile): "booked an appointment" is FLAT (72->73, r+0.05)
despite ~1.5x morbidity. The shortfall is rationed two ways, BOTH ~doubling with deprivation:
  DIVERSION (told pharmacy/111/urgent care) 6.5 -> 13.5% (r +0.37);
  DEFLECTION (told to contact the practice again another day) 5.0 -> 9.8% (r +0.31).
Combined deflect+divert 11.5 -> 23.3% (least -> most deprived). Self-care advice 12.6->16.2, prescribing
19.5->24.1 also rise. Least-deprived diversion is likely OFF-survey (private care), so the true gradient is
if anything understated.

NEED-vs-CAPACITY DECOMPOSITION of deflection (practice-level, n=5,558): corr(deflection, deprivation)=+0.30,
corr(deflection, diabetes prevalence)=+0.25 (deprivation~morbidity 0.49). BOTH survive partialling:
morbidity|deprivation +0.13, deprivation|morbidity +0.21. Joint standardised model: deprivation +1.11,
morbidity +1.06, GP-FTE/10k -0.61, appts-per-capita -0.83. => deflection is the pressure valve that opens
when NEED (morbidity + deprivation, each independent) outruns CAPACITY (GPs, appointments). ECOLOGICAL
caveat: cannot show whether LTC patients THEMSELVES are deflected vs the practice deflecting everyone when
swamped -- needs the individual crosstab Q12 x deprivation x LTC status (Q38/Q41). PENDING.

NEED vs SUPPLY context (practice-level, by IMD quintile): diabetes 6.7->10.0% (1.5x) but appts/capita 1.01x
and GP-FTE/10k 0.89x (corrected) -- supply flat/lower where need highest. Deprived populations are YOUNGER
(65+ 22->13%) yet SICKER. Equal provision for unequal need = the inverse care law. And deprived PRACTICES do
MORE care planning (Q44/Q45 reversed at practice level, QOF-driven) yet deprived PATIENTS report LESS
confidence/support (Q42/Q43): more activity, still less met need.

NOVELTY: the general inverse-care-law-in-general-practice literature is deep (Tudor Hart 1971; Mercer/Watt
Deep End; Health Foundation "Tackling the inverse care law"; consultation-length BJGP 2021). Under-explored
and likely novel here: the DEFLECTION metric (GPPS Q12, added only in the 2024 questionnaire redesign)
quantified by deprivation; the paired deflection+diversion mechanism; and pharmacy/dental ratings as a
respondent-disposition control for GP satisfaction (practice GP-sat correlates +0.27/+0.37 net of deprivation
with pharmacy/OOH -- a ~halo component the practice does not control). VERIFY with a proper scoping search
before claiming novelty in the briefing/a paper.

## 4.18.1 Deflection is need-targeted; diversion is not (individual-level, 11 Jul 2026) — RESOLVES the 4.18 pending item

GPPS analysis-tool crosstabs, national, exact rates computed from count/base (the tool rounds display to
1dp; bases are tens of thousands per cell -> reliable). "Deflection" = Q12 "told to contact the practice
again another day". "Diversion" = Q14 told pharmacy + 111/other NHS + urgent care.

DEFLECTION x deprivation x NEED — the sickest, in the poorest areas, are deflected most, and the need-penalty
CONCENTRATES in deprived areas:
- has-any-LTC (Q38): most-deprived 9.82% (LTC) vs 7.62% (no LTC), gap +2.19; least-deprived 5.15 vs 4.71,
  gap +0.44. So the LTC penalty is ~5x larger in the most-deprived fifth than the least.
- limiting condition (Q41): gap +2 to +4pp, bigger than any-LTC -> SEVERITY drives it.
- vulnerabilities (Q37), most-deprived: two-or-more-falls 15%, feeling isolated 14%, mobility 11%, none 8%.

DEFLECTION x CONDITION (Q39) — the pattern is the headline. Ranked deflection %:
  learning disability 11.0 (most-dep 13.1), autism 9.4, mental health 8.7, kidney/liver 8.5, neurological 8.3,
  lung 7.9 ... vs no-LTC 6.5, high BP 6.4, heart 6.7, dementia 6.0 (small base), CANCER 5.5 (lowest).
  => the COGNITIVE / COMMUNICATION / MENTAL-HEALTH conditions (learning disability, autism, mental health) are
  deflected MOST; clear-cut acute physical (cancer) LEAST. The patients least able to navigate phone triage /
  "call back tomorrow", and who most need relational continuity, are the ones most often turned away. Worst
  cell in the whole analysis: learning disability x most-deprived = 13.1%, vs cancer x least-deprived 4.4% (~3x).
  Deprivation stacks within every condition. Caveat: Q39 multi-response (conditions co-occur, not isolated);
  per-contact rate; "come back" is occasionally an appropriate "book a proper appointment", but that can't
  explain why it is worst for learning disability/autism specifically.

DIVERSION x deprivation x need (Q41): diversion RISES with deprivation (least ~4.3 -> most ~8.5, ~doubles) BUT
is NOT need-targeted -- limiting vs non-limiting gap is ~0-1pp and ESSENTIALLY ZERO in the most-deprived
(8.52 vs 8.40). So diversion tracks area/capacity (and request type) but is blind to patient morbidity --
consistent with appropriate signposting (pharmacy suits the presenting minor ailment, not the person's LTCs).

CONCLUSION for the briefing: do NOT lump deflection and diversion. DEFLECTION is the discriminatory mechanism
-- it lands specifically on the highest-need patients (learning disability, autism, mental health, limiting
conditions), hardest in deprived areas. DIVERSION is need-neutral and largely appropriate triage. The access
model's inequity is concentrated in "come back another day", not in "go to the pharmacy".
