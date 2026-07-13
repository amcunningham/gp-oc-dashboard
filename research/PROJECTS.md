# GP access work — portfolio map

**Overarching hypothesis:** publicly available English GP data can help practices make decisions —
above all, *whether moving to total triage is worth it* (most practices have NOT moved), and for
those who have, *how they compare to others*. The spine is a **work / capacity / deprivation /
morbidity** typology.

**Scope:** England, publicly available data only. One place to see all strands and pick any one up in
a fresh session. **Rule: separate projects by output/audience; keep ONE shared data layer.**
_(The NI / Bristol / Molly Dineen collaboration is separate work — out of scope here.)_

_Last updated: 13 Jul 2026._

---

## Shared foundation (do NOT fork)

Single source of truth for every project. If a project grows its own copy of the panels, they desync.

- `data/` panels: `xsec_master_2026` (cross-section + GPPS), `panel_merged` / `panel_oc` (GPAD appts + OC,
  2023-2026), `cbt_ivr_panel` (telephony, Oct 2024-May 2026), `workforce_panel` (2018-2026),
  `fft_gp_panel` (2022-2026), `qof_prevalence_2425` (**NEW** - 21 disease registers, 6,188 practices;
  the morbidity axis), external joins (NHS Payments, Fingertips, ODS).
- `scripts/` ingest + build; provenance in `PANEL_NOTES.md`, `XSEC_REBUILD_PROPOSAL.md`.
- Gaps: telephony starts Oct 2024; POMI (direct booking) ended Aug 2024; OC undercount where suppliers
  don't report (Medicus/Visiba, §4.26).
- **Registration / list-size denominator (all NHSE, not Fingertips) — DO NOT MIX:** four flavours differ by
  up to ~3% by date/method. `xsec.list_size` = 12-month AVG of the monthly GPAD-panel count; `practice_age_sex.total_list`
  = NHSE "Patients Registered at a GP Practice" (latest snapshot, Jul 2026); `practice_list_history` = annual;
  `practice_weighted_list.registered_patients` = NHS Payments 2024/25 (oldest, keep only for the Carr-Hill ratio).
  **Rule:** canonical source = NHSE "Patients Registered at a GP Practice"; for monthly rates use the matching
  month's list, for a cross-sectional denominator the latest snapshot; never take a count from one source and
  divide by a denominator from another. Fingertips list size is a lagged re-publication — don't use it.

### Data sources (from the Arjus landscape review, 13 Jul) — pulled 13 Jul

Arjus (arjus.co.uk) aggregates ~18 public datasets as **descriptive dashboards** - no typology, no
interpretation; that gap is ours. Sources for the axis:

- **QOF disease prevalence 2024/25** - DONE (`data/qof_prevalence_2425`, 21 registers). Morbidity axis.
- **CVDPREVENT** - DONE (`data/cvdprevent_practice`, 32 CV detection/management indicators, to Dec 2025). CV-management axis.
- **Carr-Hill weighted list** - DONE (`data/practice_weighted_list`, 2024/25). Need-adjusted capacity denominator (ratio ~1.0, range 0.4-4.0).
- **Practice age/sex structure** - DONE (`data/practice_age_sex`, Jul 2026). Age-band shares + %female; demographic need axis.
- **POMI online services** - DONE (`data/pomi_online_services_practice`, 2022-Aug 2024, practice-month). Direct online booking (`appts_online_transactions`) - the ONLY open practice-level booking source; ends Aug 2024; overlaps OC for the self-book-vs-triage question on early adopters.
- **NHS App MI** - PULLED but **ICB-level only** (`data/nhs_app_mi`, 2020-2026); has logins/registrations/prescriptions, NOT appointments-booked and NOT practice granularity. Practice-level app booking sits behind the OKTA-gated NHS App Dashboard. **Correction to earlier note:** no OPEN practice-level online-booking data exists after Aug 2024.
- **Fingertips cancer-emergency (practice)** - DONE (`data/fingertips_cancer_emergency_practice`, 2024/25). Emergency/late cancer presentation = unmet-need marker (late diagnosis).
- **CVDPREVENT under-detection** - in the cvdprevent file (CVDP005HYP, 002/003CKD, 003/005DM, 002NDH = undiagnosed/uncoded) = unmet-need marker (under-detection).
- **ACSC emergency admissions** - PULLED but **upper-tier LA level, 2020/21 only** (`data/acsc_emergency_icb`); NOT practice-level and stale. True practice-level ACSC/A&E needs HES via a DSA (application, not open).
- **LSOA population-health apportionment** - NOT pulled (bigger job: patients-by-LSOA x IMD/Census). Deferred.
- **Full GPPS record-level** - needs a data application (Ipsos / NHS England / UK Data Service); cannot be downloaded.

---

## Projects

| # | Project | Output / audience | Status | Next action | Home |
|---|---------|-------------------|--------|-------------|------|
| 1 | **The tool** | Public explorer + practice page; GPs / practices | Live (~26+ users; 1st feedback in) | Quick wins (trim architecture detail; inline provenance); **T&Cs/privacy**; interpretation-first summary card; MCP decision | `explore.html`, `mypractice.html`, `predictors.html`, `PRACTICE_TOOL_DESIGN.md` |
| 2 | **Practice typology** (central) | Cluster on work/capacity/deprivation/morbidity -> "practices like you", should-you-triage guidance, comparison for movers | Spine exists (`practice_typology_k5`, `supply_typology_all6k`); needs morbidity axis | Fold QOF prevalence (+CVDPREVENT) into feature space; rebuild; validate | `data/*typology*`, (brief TBC) |
| 3 | **Access-model research** | The six-proposition critique; paper / policy | Mature | Fold in deflection-by-condition equity | `PANEL_NOTES.md` |
| 4 | **Online-triage substitution study** | Event study: what adopting total triage does (feeds tool + typology) | Exploratory, unhardened | Matched control + DiD + inference | `projects/triage-substitution-study.md` |
| 5 | **RCGP briefing** | 3-page policy brief; RCGP | Draft v0.3 (in notes, not a file yet) | Apply capacity amendment (`NOTES_BATCH_DRAFT` sec C) | (to be created) |
| 6 | **Unmet-need study** | Which practices are NOT meeting need: expected need (morbidity+deprivation+age) vs delivered activity + access-failure, validated by under-detection & late-diagnosis. Attacks the de Dumast/Carr-Hill blind spot (consultations = met demand) | New (data assembled 13 Jul) | Build expected-vs-delivered residual; validate vs CVDPREVENT undiagnosed + cancer-emergency | `projects/` (brief TBC) |

All six are facets of one goal: **decision-support for practices from public data.** The typology is the
spine; the tool is its delivery; the research and triage study are the evidence; the briefing is one output.

---

## Cross-cutting threads

- **Governance / privacy - settle before wider release.** The tool returns data on *named* practices, some
  newsworthy. Case in point: **C85007 Dove Valley = practice of Clare Bannon, new BMA GPC England chair**
  (Pulse, 10 Jul 2026). Needs plain-English explainer, T&Cs/privacy footer, and "descriptive, not a league
  table" framing locked. **Do NOT use any named practice as a case study** - cohort-level only.
- **Interpretation is the moat.** Peer-relative + evidence-weighted salience (which metrics predict experience)
  is what Arjus / Ben Haresign / a raw dashboard cannot do.
- **Notes reconciliation.** `PANEL_NOTES.md` clean to sec 4.14; `NOTES_BATCH_DRAFT.md` holds sec 4.15-4.31 +
  companion additions awaiting a single review/merge (three `[CHECK]` numbers cleared 13 Jul).

---

## How to resume any one strand

Open the repo, read this map, then the project's home file(s). Work that strand only; update its notes;
update the row above if status changes.
