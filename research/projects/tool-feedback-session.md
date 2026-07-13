# Tool feedback session — brief (mypractice provenance + info-hygiene)

_Scope: pick up the colleague feedback quick-wins on the practice page. Part of Project #1 (the tool).
Created 13 Jul 2026._

## Do (this session)

1. **Inline data-source provenance (feedback #1).** Right now sources sit in one "Reading this page"
   block (`mypractice.html` ~line 93-109) and as scattered `PANEL_NOTES.md` links — the reviewer wants to
   see, *on each card/metric*, where that number came from, "to assist with checking." So: attach a short
   source tag to each result card/metric (e.g. phone measures -> "Cloud-Based Telephony, Mar-May"; GPPS
   measures -> "GP Patient Survey 2026, Qn"; workforce -> "NWRS"; QOF/morbidity -> "QOF 2024/25"). A small
   inline label or hover, per card, not a wall of text. Do the same for `explore.html` answers if cheap
   (the answer pipeline already knows the source table).

2. **Trim architecture/internal detail (feedback #5).** The "Reading this page" card and various links
   expose the build internals (`PANEL_NOTES.md`, `KEY_FINDINGS`, "the models behind this page", MD files).
   The reviewer: "reveals how you've architected the model... probably unnecessary details." Keep an honest
   short methods note + a link to the public GitHub/README, but drop the internal-file plumbing from the
   user-facing card. (Don't delete PANEL_NOTES links that the explore.html *findings* fetch needs to
   function — line ~854; just stop surfacing them as user chrome.)

3. **(Optional, needs AMC sign-off) Footer T&Cs / privacy + one-line plain-English explainer (feedback #4).**
   Scaffold the footer + placeholder copy only; the actual privacy wording is AMC's call (the tool logs
   questions and returns *named* practices — see governance below). Flag, don't finalise.

## Do NOT (this session)

- **The graphical / high-level summary card (feedback #3).** AMC is deferring the visual redesign — do not
  build the snapshot/peer-band card or restructure the page layout. Provenance + hygiene only.
- Export to PDF (#2) and the MCP (#6) — later.
- Don't touch other projects, `research/data/` schema, or the analysis notes.

## Technical notes / hazards

- Files: `research/mypractice.html` (86 KB), `research/explore.html` (61 KB), `PRACTICE_TOOL_DESIGN.md`.
- Data loads via `DATA_BASE` (GitHub raw when opened as `file://`, local `data/` when on localhost).
- Any charts must be **server-/pre-drawn SVG, not client-JS-generated** (some viewers don't run widget JS).
- **OneDrive truncation hazard:** these repo files sync via OneDrive and have come back truncated before.
  Before editing, check on-disk size vs `git show HEAD:research/mypractice.html | wc -c`. Prefer editing via
  bash heredoc / targeted `sed`/python replace, or restore from `git show HEAD:...` if a read looks short.
- **Git index null-sha1** (recurring): if `git add` fails with `unable to read <null-sha1>`, run
  `git read-tree HEAD` to rebuild the index, then re-add. Set `git config user.email` locally to commit.

## Governance (carry, don't act on)

The tool returns data on *named* practices, some newsworthy (C85007 = practice of the new GPC England chair;
see PROJECTS.md). Provenance/hygiene edits are safe; do NOT widen release or add features that expose more
per-practice detail without AMC deciding the T&Cs/privacy question first.
