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

### 4.25 Data-quality note: 96 practices missing from the cross-section (11 Jul 2026; found via AMC's N81086 report)

xsec_master_2026 silently excludes 96 practices that have usable 2026 survey records (base
≥30), N81086 among them (overall experience 88.8% → 81.2%, full CBT and GPAD histories) — an
inner-join casualty in the build pipeline. All practice-level model n's are correspondingly
~2% short, direction of any bias unknown but plausibly against newer/recoded practices. FIX
SCHEDULED: rebuild the cross-section survey-first with left joins at the 30 July refresh and
rerun the predictors page in the same pass. Until then mypractice.html tells affected
practices plainly that the gap is ours, not theirs.

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
