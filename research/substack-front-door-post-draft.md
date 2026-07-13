# The inverse care law is not at the front door

*Draft v0.1 — 13 Jul 2026 — NOT for publication until reviewed. Numbers verified against `data/GPPS_National_Crosstab_13072026*.xlsx` and `GPPS_National_Crosstab_11072026 (9).xlsx`; admin corroboration computed from `research/data/panel_merged.csv` + `cbt_volumes_panel.csv` + `xsec_master_2026.csv` (Oct 2024–Mar 2026, practices in both panels, list-size-weighted; robust to practice-level medians).*

---

In 1971 Julian Tudor Hart wrote that the availability of good medical care tends to vary inversely with the need of the population served. Fifty-five years on, the usual mental picture of the inverse care law in general practice is a closed front door: poorer, sicker patients who cannot get an appointment, or who give up before asking.

The 2026 GP Patient Survey lets us test that picture, because since a 2024 redesign it asks patients what happened at each step of their last attempt to contact their practice — not just whether they were satisfied at the end. Following those steps gives a different answer. The sickest patients in the most deprived areas contact their practices just as much as their counterparts in the least deprived areas, and once they are actually seen, the gap in whether their needs were met is two percentage points. The loss happens in the middle of the journey: after they make contact but before they are seen, they are substantially more likely to be told to contact the practice again another day, or to be sent to a pharmacy, NHS 111 or urgent care instead.

## The data

The GP Patient Survey is run by Ipsos for NHS England; the 2026 wave has 651,257 responses from patients aged 16 or over registered with an English practice, weighted to the registered population. NHS England's online analysis tool cross-tabulates any question by deprivation quintile (Index of Multiple Deprivation) and by other questions. Everything below is national, from that tool.

To focus on the patients the inverse care law is about, I restrict most of the analysis to the sickest group the survey identifies: people who say a health condition reduces their ability to carry out day-to-day activities "a lot" (question 41). In the most deprived fifth of the country that is a weighted 25,090 respondents; in the least deprived fifth, 10,009 — bases large enough that the percentage differences below are not sampling noise.

The survey traces a journey: whether you tried to contact your practice in the last year (Q8); whether, once you contacted them, you knew the next step or were instead "told to contact my practice again another day, as they couldn't help that day" (Q12); how the practice dealt with the request — booked an appointment, or told you to go to a pharmacy, contact NHS 111, or get urgent care (Q14); and, for those who had an appointment, whether your needs were met (Q31).

## The cascade

Among patients limited "a lot" by their conditions, comparing the most deprived fifth with the least deprived fifth:

| Stage of the journey | Most deprived | Least deprived | Gap |
|---|---|---|---|
| Didn't contact the practice in the last 12 months | 4% | 3% | +1pp |
| Told to contact the practice again another day | 12% | 7% | +5pp |
| Sent to pharmacy, NHS 111 or urgent care | 13% | 7% | +6pp |
| Needs not met (of those who had an appointment) | 17% | 15% | +2pp |

*Each row has its own denominator: everyone (row 1); those who contacted the practice (row 2); those whose request was dealt with (row 3); those who had an appointment, excluding "don't know" (row 4). Percentages are as displayed by the analysis tool, rounded to whole points.*

The first row is the front door, and it is nearly flat. Very sick patients contact their practice at almost identical rates whether they live in the poorest or the richest areas — 92% and 93% respectively had contacted within six months. Whatever is producing unequal care, it is not that deprived patients fail to ask.

The last row is the consultation itself, and the deprivation gap there is 2 percentage points. Small — but note the level: 17% of the sickest patients in deprived areas say the appointment did not meet their needs at all.

The middle two rows are where the inverse care law actually shows up, and each behaves differently.

## Being told to come back another day tracks need — most strongly in deprived areas

"Told to contact the practice again another day" is the survey's measure of a request that was neither dealt with nor redirected: the patient made contact and was asked to start again. Among the sickest patients it happens to 12% of contacts in the most deprived fifth against 7% in the least — and within every area, it rises with how sick you are. In the most deprived fifth the rate is 12% for those limited a lot, 11% limited a little, 7% not limited; in the least deprived fifth, 7%, 6% and 4%. The penalty for being sick is therefore larger in deprived areas (5 points) than in affluent ones (3 points).

The pattern by condition is starker. Cross-tabulating the same question by long-term condition, the highest come-back-another-day rates in the most deprived fifth are for people with a learning disability (13.1%), autism, kidney or liver disease, and neurological and mental health conditions; the lowest rate anywhere in the table is for people with cancer in the least deprived fifth (4.4%). The conditions with the highest rates are those that make contacting a practice and starting again hardest; the survey records the pattern, not the reason for it.

## Being sent elsewhere tracks area, not sickness

Redirection to pharmacy, NHS 111 or urgent care also roughly doubles with deprivation (13% v 7% among the sickest). But unlike come-back-another-day, it barely rises with sickness: in the most deprived fifth it is 13% for those limited a lot and 11% for those not limited at all; in the least deprived, 7% against 5%. That pattern is consistent with practices signposting by the presenting request — a minor ailment goes to the pharmacy whoever brings it — rather than turning away their sickest patients. The survey cannot distinguish appropriate from inappropriate redirection, so I would read this row as a capacity and signposting gradient, not as rationing targeted at the sick.

## What this does and doesn't show

Both gradients hold within every age band: comparing most and least deprived fifths band by band, from 16–24 up to 85 and over, come-back-another-day is 2 to 5 points higher in the deprived fifth in all eight bands, and redirection 1 to 8 points higher. Neither is an artefact of deprived areas being younger.

Because the survey asks only about the last attempted contact, this is a repeated cross-section of contacts, not a cohort of patients followed through. The downstream rows have conditional denominators, which could in principle bias comparisons if different kinds of patients reached each stage — but the near-flat first row limits that concern: roughly the same share of sick patients enters the pipeline in both areas. All figures are self-reported, national rather than practice-level, and associations rather than causal estimates. Q14 allows multiple answers, so the redirection row sums three overlapping options. And a request that ends in "book a routine appointment next week" can be entirely appropriate; the objection is not to any individual decision but to a pattern in which the frequency of the decision tracks the patient's sickness and postcode.

The survey is also self-reported — but administrative records show the same wedge from the practice side. Combining monthly cloud-telephony records (October 2024 to March 2026), online-consultation submissions and the national appointment dataset for the 4,967 practices with telephony data: practices in the most deprived fifth receive 35% more inbound calls per registered patient than those in the least deprived (721 versus 535 per 1,000 patients per month) and answer 32% more (394 versus 300). Online submissions run lower in deprived areas (94 versus 119), leaving total patient-initiated contacts 17% higher (489 versus 418). Appointments delivered per registered patient are the same in both fifths (492 per 1,000 per month) — for populations that are younger (14% versus 21% aged 65 or over) but carry half again as much diabetes (9.7% versus 6.6% recorded prevalence). Per registered patient, contact volume rises with deprivation; appointment volume does not. Three caveats on this check: the telephony data cover only practices using participating cloud phone systems (73% of the most deprived fifth, 86% of the least); repeat calls about the same problem are counted each time — though generating repeat contact is part of the mechanism at issue; and total appointments include planned and recall care, so this compares scale, not conversion of contacts into appointments.

None of the background is new. That deprived-area patients get less consultation and contact time for their level of morbidity is established (Gopfert et al., BJGP 2021; McConnachie et al., BMJ Open 2023), and Rolewicz et al. (BMJ Open 2020) showed with the 2018 survey that unmet need after an appointment is patterned by the person — age, frailty, ethnicity — more than by the practice. The final row above corroborates that: needs-not-met roughly triples with functional limitation within the least deprived fifth (15% v 5%) while the deprivation gap among the sickest is 2 points.

What is new is the middle of the journey. The come-back-another-day question has only existed since the 2024 questionnaire redesign, so the mechanism — where between contact and consultation the loss occurs, and for whom — is newly measurable. That matters for the current funding debate. The formula-reform work informing the Carr-Hill review (Anselmi et al., 2025 and 2026; de Dumast et al., 2026) is built on utilisation — care that happened — and its authors are explicit that need which never converts into a consultation currently has no available measure and must be handled by assumption. These survey questions are a direct, if imperfect, measure of exactly that layer. The two approaches are complements: one prices the care delivered, the other counts the requests that didn't become care.

In these national figures, the inverse care law is not a door that fails to open. Patients present, and are let in; the loss comes afterwards, when the sickest patients in the poorest places are disproportionately asked to start the process again.

---

## Title options (pick one / edit)

1. The inverse care law is not at the front door
2. Come back tomorrow: where the inverse care law actually operates
3. Equally likely to ask, more likely to be turned away
4. What 650,000 patients say happens after they call the GP
5. The revolving door: deflection, diversion and the inverse care law

## Pre-publication checklist (delete before posting)

- [ ] Confirm whether the analysis tool's IMD quintile is assigned by patient postcode or practice — the workbook doesn't say; wording above stays neutral ("deprivation quintile (IMD)").
- [ ] Anselmi/de Dumast 2026 citations taken from PANEL_NOTES/brief; verify exact references and the "no available measures" quote before linking.
- [ ] Decide whether to keep the condition-level sentence (learning disability 13.1% / cancer 4.4%) or hold it for the access-model paper (Project 3 earmarks deflection-by-condition).
- [ ] OC undercount: suppliers that don't report (Medicus/Visiba, §4.26) depress oc_total — the online-submissions comparison (94 v 119) may be affected if non-reporting suppliers skew by deprivation; check before publishing.
- [ ] Final word count ~1,420 excluding tables/checklist — over the ~1,200 target; trim candidates: the Q-number detail in "The data", or shorten the literature paragraph.
