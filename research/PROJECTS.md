# GP access work — portfolio map

One place to see all the strands and pick any one up in a fresh session without carrying the
others. **Rule: separate projects by output/audience; keep ONE shared data layer.** Each project
runs as its own Cowork session with its own notes/handoff; this file is the index.

_Last updated: 13 Jul 2026._

---

## Shared foundation (do NOT fork)

**The data layer is the single source of truth for every project.** If a project grows its own
copy of the panels, they desync and the coherence is lost.

- `data/` — practice-month panels: `xsec_master_2026` (cross-section + GPPS), `panel_merged`
  (GPAD appts + OC, Mar 2023–May 2026), `panel_oc` (OC, Apr 2023–Mar 2026), `cbt_ivr_panel`
  (cloud telephony, Oct 2024–May 2026), `workforce_panel` (2018–2026), `fft_gp_panel` (2022–2026),
  external joins (NHS Payments, Fingertips, ODS).
- `scripts/` — ingest + build (`ingest_gpps2026.py`, `build_xsec_full.py`, `fetch_fft.py`, …).
- Provenance/decisions: `PANEL_NOTES.md` (canonical), `XSEC_REBUILD_PROPOSAL.md`.
- Known gaps: telephony starts Oct 2024; POMI (direct online booking) ends Aug 2024; OC undercount
  where suppliers don't report (Medicus/Visiba watch, PANEL_NOTES §4.26).

---

## Projects

| # | Project | Output / audience | Status | Next action | Home |
|---|---------|-------------------|--------|-------------|------|
| 1 | **The tool** | Public explorer + practice page; colleagues, GPs, curious public | Live (~26+ users; 1st external feedback in) | Quick wins (trim architecture detail; inline provenance); **T&Cs/privacy**; interpretation-first summary card; MCP decision | `explore.html`, `mypractice.html`, `predictors.html`, `PRACTICE_TOOL_DESIGN.md` |
| 2 | **Access-model research** | The six-proposition critique; paper / policy | Mature | Fold in deflection-by-condition equity; decide publication track | `PANEL_NOTES.md` |
| 3 | **Online-triage substitution study** | Event study: what adopting online/total triage does to phone, answering, continuity, experience | **Exploratory, unhardened** | Matched control + DiD + inference (see brief) | `projects/triage-substitution-study.md` |
| 4 | **RCGP briefing** | 3-page policy brief; RCGP | Draft v0.3 (in notes, not yet a standalone file) | Apply capacity amendment (`NOTES_BATCH_DRAFT` §C); consider deflection-equity ask | (to be created) |
| 5 | **NI protocol / Bristol** (optional) | Annex A for Molly Dineen; NI research | Parked | Await user decision on deflection exposure | HANDOFF notes |

---

## Cross-cutting threads (span more than one project)

- **Governance / privacy — settle before wider release.** The tool returns data on *named* practices,
  some newsworthy. Case in point: **C85007 Dove Valley = practice of Clare Bannon, new BMA GPC England
  chair** (Pulse, 10 Jul 2026). A public "tell me about this practice" tool + a named, political figure
  = a gotcha risk. Needs: plain-English explainer, T&Cs/privacy footer, and the "descriptive, not a
  league table" framing locked in. Applies to **Tool** and **Triage study**.
- **Do NOT use Dove Valley (or any named practice) as a case study** in public/notes outputs. Cohort-level only.
- **Notes reconciliation.** `PANEL_NOTES.md` is clean to §4.14; `NOTES_BATCH_DRAFT.md` holds §4.15–4.31
  + companion additions awaiting a single review/merge (three `[CHECK]` numbers cleared 13 Jul).
- **Interpretation is the moat.** Peer-relative + evidence-weighted salience (which metrics predict
  experience) is what no raw dashboard (Ben Haresign's, Keith's) can do. Both Tool and Research depend on it.

---

## How to resume any one strand

Open the repo, read this map, then read the project's home file(s). Work that strand only; update
its home notes; update the row above if status changes.
