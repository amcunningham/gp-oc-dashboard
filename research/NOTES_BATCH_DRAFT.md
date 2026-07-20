# Residual — items not yet banked (was NOTES_BATCH_DRAFT.md)

**Sections 4.15–4.34.1 were merged into PANEL_NOTES.md on 20 Jul 2026** (renumbered and de-duplicated) and removed from here. What remains below: two items still **pending AMC sign-off** (A, C), and two operational records kept for reference (D — the 30 July rebuild list; E/E2 — user feedback). **The RCGP capacity amendment (was section C) was moved to `drafts/rcgp-capacity-amendment.md` (gitignored, not public) on 20 Jul 2026.**

---

## A. Explorer KEY_FINDINGS (14–17)

> **PENDING AMC SIGN-OFF — not yet applied.**


> 14. About a quarter of calls to practices end in the automated phone system (IVR) before
> reaching the hold queue — stable nationally (26–29%, Oct 2024–May 2026) but hugely variable
> between practices (median 24%, top decile above 36%, maximum ~94%). Higher IVR-ended share is
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

---

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

## E2. Second user feedback (12 Jul 2026, colleague via WhatsApp/AMC) — explorer, in use on a client practice

Positive: "enjoying the use of your tool, just used to get some context on one of our new client
practices." Requests, triaged:
1. INLINE PROVENANCE per card — show exactly where each result's data came from *on the card*, not
   only in the end-of-page sources block. "in-line would assist with checking." (quick-ish; the answer
   pipeline already knows the source table/column — surface it per finding.)
2. EXPORT — print/download the output as PDF/Docx. (moderate; client-side print-to-PDF is the fast path.)
3. LESS WORDY — a high-level, ideally graphical, initial summary above the detail. "would feel easier."
4. FOOTER T&Cs / privacy policy linking to relevant docs, + a plain-English explainer. (product/legal
   decision — AMC call; needed before wider sharing.)
5. INFO HYGIENE — the "reading this page" card exposes architecture detail (reference to the MD/
   KEY_FINDINGS file). Not a security issue but unnecessary; trim. (quick.)
6. MCP — "would be lovely." Colleague flags Ben Haresign's tool (haresign.net/tools/) as prior art with
   an existing MCP — worth reviewing before building ours.

ACTIONS (proposed): #5 and #1 are quick wins; #2 is a print stylesheet; #3 is a summary-card redesign;
#4 is AMC's decision; #6 folds into the deferred MCP build (review Haresign first).
