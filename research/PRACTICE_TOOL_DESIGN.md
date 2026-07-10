# Design note: "How does my practice compare?" — a practice-facing diagnostic

Originally framed as an access diagnostic; renamed when continuity emerged as the strongest
finding and the scope grew to contact, continuity and capacity together.

v1.0 as built, 10 July 2026 (supersedes draft v0.1, same date). Shipped as
[mypractice.html](mypractice.html). AMC approved v0.1 conceptually; v1.0 records what was
actually built after a day of iteration against real practices, and where it departs from
the draft.

## Overview

This tool is written for practices working under sustained pressure. The Royal College of
General Practitioners describes general practice as under "immense strain", with workforce and
workload challenges contributing to unsustainable workload and difficulties for patients in
accessing care ([RCGP, Future of general practice](https://www.rcgp.org.uk/campaign-home));
in RCGP polling this year, nearly three-quarters of GPs said excessive workload was
compromising patient safety
([RCGP, 2026](https://www.rcgp.org.uk/news/workload-concerns-polling)). The data in this
repository shows the same picture from the other side: more contact volume than delivered
capacity in most practices, and fewer fully-qualified full-time-equivalent GPs per patient
than in 2019.

The tool therefore does not treat a poor access measure as a verdict on effort. Its
comparisons are deliberately fair — a practice is set against practices of the same size and
deprivation, not against England — and the page states plainly which forces (size,
deprivation, GP numbers) are outside a practice's control. Where the findings point somewhere,
they point at reviewable operational specifics, not at working harder.

## Purpose

A web page where any English practice can see, in plain language with benchmarks, where its
access operations sit and where improvement is most associated with better patient experience.
Built entirely on the datasets and findings in this repository; all queries run in the browser
(DuckDB-WASM over the published parquet/CSV files), so nothing is uploaded and no practice data
leaves the user's machine. Lookup is by ODS code or name.

## Tier 1 — as shipped

The page leads with a verdict and holds the detail behind it.

**"What stands out for your practice."** Up to three flags, ranked by a fixed order reflecting
strength of association with patient experience: patients reporting being told to contact again
(strongest survey link), queue answering (strongest phone link), contacts per appointment,
calls ended within the IVR, the Monday answering gap, then capacity as context and channel
strategy as a conditional option. Each flag states the practice's figure, its comparator, one
sentence of what the national data shows, and — where the published data runs out — the
specific thing only the practice can check (what the menu plays at 8am on a Monday; what
reception offers when no slot is left; whether Monday staffing matches Monday call volumes).
Flags fire only past stated thresholds. Tempering is symmetric: a high deflection figure is
demoted when the practice's own patients report access as good as peers'; operational flags
are balanced by a paragraph noting when patients' reported experience is nonetheless strong.
A "What you are doing well" line closes the summary. Practices with nothing to flag are told so.

**Evidence sections** (collapsed, linked from each flag):

- *Phones* — May 2026 vs May 2025 (where the supplier reported then), against the typical
  practice and the typical practice of the same size fifth; distribution lines (bar = middle
  80%, notch = median, diamond = size-fifth median, dot = the practice). Day-of-week card:
  Monday vs Wednesday calls and queue-answer rates, both years; the practice's own IVR shares
  by rush vs rest of day and Monday-morning vs Wednesday-morning (the capacity-message clue);
  when the Monday gap exceeds 10 points, the practice's own Monday/Wednesday answer rate by
  time band — which distinguishes a morning-rush problem from an all-day one at n=1. Bank
  holiday Mondays excluded from both Mays.
- *Demand and delivery* — contacts (calls + online submissions) per appointment, May 2026 vs
  May 2025, with national median, p75 and middle-80% rows, and an explanation of ratios below 1
  (follow-ups, recalls, nurse clinics and direct online bookings are appointments without
  inbound contacts).
- *What your patients reported* — five GPPS measures, 2025/2026/England/"practices like yours",
  plus the 2012–2023 trajectory against England.
- *What shapes these scores* — for size, deprivation, GP staffing, appointment volume and
  same-day share: the range of patient-reported experience within the practice's own fifth
  (middle-80% bar, average notch, the practice's dot, one shared scale), a gradient table of
  lowest-vs-highest-fifth averages, and the similar-practices comparison.

**"Similar practices"** means the same twenty-fifth of England: the same fifth for list size
and the same fifth for deprivation — no weighting or modelling. Cell sizes vary (roughly 135 to
360) because size and deprivation are related: small practices cluster in deprived areas, large
ones in affluent areas.

## Departures from v0.1, and why

- **Verdict first.** v0.1 was a report; AMC's test drives showed a report does not help a
  practice decide anything. The ranked-flags summary replaced it.
- **No deciles, no per-SD coefficients on the page.** v0.1 planned decile badges and
  association coefficients. Both proved to be jargon in testing. Comparisons are now pictorial
  (distribution lines with the practice marked) and worded plainly ("practices your size
  typically answer 78%"); the regression evidence lives in PANEL_NOTES.md.
- **Own data over group tendencies.** Where v0.1 would have said what practices "like this one"
  typically do (e.g. "gaps above 10 usually persist all day"), the page now shows the
  practice's own hour-by-hour figures instead — testing revealed practices (e.g. a 17-point
  gap entirely confined to two Monday-morning hours) that the group tendency would have
  mischaracterised.
- **Survey attribution.** Everything survey-derived is phrased as what patients report, never
  as fact about the practice.
- **Consultant register.** Recommendations are phrased as reviews that would establish
  something, not as instructions or aphorisms.
- **May 2026 basis with year-before comparison** throughout (v0.1 assumed March); the ~3,100
  early-onboarded practices get May 2025 columns, others are told why not.

## Binding wording constraints (unchanged from v0.1)

All comparisons are associations, never predictions or guarantees, and the page says so. Small
denominators flagged (survey n<50; monthly calls <200). No composite score, no rating, no
traffic lights. The page states what each measure cannot distinguish (IVR endings blend
self-service, redirection and abandonment; contacts per appointment blends demand with repeat
calling). Nothing coined.

## Tier 2 — not built

Upload of a slot-level appointment-book export (EMIS/SystmOne), parsed locally in the browser,
adding what public data cannot do for one practice: supply flex against the practice's own call
curve; slot-exhaustion time overlaid on answering-by-hour (the direct n=1 test of "answering
stops when the slots run out"); same-day share against the practice's own Monday surge.
Requires a survey of real export formats first (three or four volunteer practices covering
EMIS and SystmOne variants), then roughly two sessions.

## Out of scope

Anything requiring patient-level data; workload measurement; comparisons of individual staff;
any output ranking named practices against each other.

## Open questions

Resolved: Tier 1 shipped before Tier 2 (yes); non-CBT practices get an explanation, not a
reduced page; refresh follows the three collections' monthly publication dates (next: 30 July
2026, when the CBT June edition adds practice-level call-waiting times — a natural addition to
the phones card and the summary).

Open: naming; whether this stays a page in this repository or is hosted elsewhere.
