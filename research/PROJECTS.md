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

### Data sources to add (from the Arjus landscape review, 13 Jul)

Arjus (arjus.co.uk) aggregates ~18 public datasets as **descriptive dashboards** - no typology, no
interpretation; that gap is ours. Sources worth pulling for the axis:

- **QOF disease prevalence 2024/25** - DONE (`data/qof_prevalence_2425`). Morbidity axis.
- **CVDPREVENT** - granular cardiovascular management indicators (deeper morbidity/management).
- **Carr-Hill weighted list size** - need-adjusted denominator for work/capacity ratios (better than raw list).
- **Population-health / LSOA** - small-area deprivation, general health, disability, ethnicity, age (need axis).
- **NHS App Management Information** - OPEN, monthly, practice-level, current to Apr 2026; app-based
  appointment booking = live proxy for direct online booking (successor to dead POMI; covers 2025-26).
- **Full GPPS record-level** - needs application (Ipsos / NHS England / UK Data Service) for individual need x deflection.

---

## Projects

| # | Project | Output / audience | Status | Next action | Home |
|---|---------|-------------------|--------|-------------|------|
| 1 | **The tool** | Public explorer + practice page; GPs / practices | Live (~26+ users; 1st feedback in) | Quick wins (trim architecture detail; inline provenance); **T&Cs/privacy**; interpretation-first summary card; MCP decision | `explore.html`, `mypractice.html`, `predictors.html`, `PRACTICE_TOOL_DESIGN.md` |
| 2 | **Practice typology** (central) | Cluster on work/capacity/deprivation/morbidity -> "practices like you", should-you-triage guidance, comparison for movers | Spine exists (`practice_typology_k5`, `supply_typology_all6k`); needs morbidity axis | Fold QOF prevalence (+CVDPREVENT) into feature space; rebuild; validate | `data/*typology*`, (brief TBC) |
| 3 | **Access-model research** | The six-proposition critique; paper / policy | Mature | Fold in deflection-by-condition equity | `PANEL_NOTES.md` |
| 4 | **Online-triage substitution study** | Event study: what adopting total triage does (feeds tool + typology) | Exploratory, unhardened | Matched control + DiD + inference | `projects/triage-substitution-study.md` |
| 5 | **RCGP briefing** | 3-page policy brief; RCGP | Draft v0.3 (in notes, not a file yet) | Apply capacity amendment (`NOTES_BATCH_DRAFT` sec C) | (to be created) |

All five are facets of one goal: **decision-support for practices from public data.** The typology is the
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
