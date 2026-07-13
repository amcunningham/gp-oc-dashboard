# Handoff — 13 Jul 2026 evening session (source audit + OneDrive move)

_For the next session. Repo's new home: `C:\GitHub\gp-oc-dashboard` (moved OUT of OneDrive today —
connect `C:\GitHub` or `C:\GitHub\gp-oc-dashboard`, never the old OneDrive path, which is deleted)._

## 1. What this session produced

**The model & data-source currency audit is done and committed:**
`research/projects/model-source-audit-findings-2026-07-13.md` — per-source currency table (every
"latest" verified against the NHSE/OHID/NHSBSA/MHCLG publication pages on 13 Jul), findings, and the
ordered fix list for the 30 Jul rebuild. Key commits: 882cf11 (audit), 110c9e2 (IMD provenance §3a),
f4af355 (README IMD fix), 3ffc7ba (recovered page edits). All pushed.

**Headline audit findings** (details in the findings file):
- **Workforce ×2 bug re-confirmed live**: xsec `gp_fte` etc. are exactly 2.0000× the corrected
  `workforce_panel` (n=5,964). mypractice.html and explore.html display the doubled per-10k figures.
  Standardised model coefficients unaffected; absolute displayed staffing wrong. **This is the next
  piece of work** (fix list item 2, item 1 now done).
- Stale: xsec workforce snapshot Mar 2025 (May 2026 published; raw in `data/gpw_may26/`); composition
  models on Mar 2025 census (`gp_composition_may26.csv` already downloaded); xsec prescribing = EPD
  Mar 2025 and not source-reproducible (latest EPD Apr 2026); `panel_oc.csv` ends Mar 2026 (Apr 2026
  published; merged panel already has OC to May 2026) — did_anima's adopter flag reads panel_oc.
- Current: GPAD/waits/CBT/FFT to May 2026; GPPS 2026 wave; QOF prev 2024/25 (2025/26 due 27 Aug);
  NHS Payments 2024/25; registered list Jul 2026; Fingertips 2024/25; CVDPREVENT Dec 2025 extract
  (couldn't fully verify schedule — recheck).
- **IMD resolved (user question)**: `data/practice_imd.csv` = Fingertips NGPP indicator **94240**
  "Deprivation score (IMD 2025)" — registered-population weighted, NOT postcode-derived (0/677
  same-postcode pairs share a score; API sample matches 304/307 to 2dp). Already latest (IoD2025).
- Recommendation: switch models to `xsec_master_rebuilt` at the 30 Jul rebuild AFTER re-deriving its
  5 backfilled columns from source (EPD ×3, epraccur ×2).

## 2. The OneDrive move (done today, after repeated live corruption)

- OneDrive was actively truncating repo files and corrupting `.git/index` during the session (caught
  and repaired: README, PROJECTS.md, explore.html, mypractice.html, about.html, worker files; several
  commits had captured stale snapshots — all reconciled and pushed).
- Whole `Documents\GitHub` folder was **copied** to **`C:\GitHub`** and the OneDrive original deleted.
  OneDrive was never actually paused; the deletion synced, so the old copy sits in the onedrive.com
  recycle bin ~30 days (not needed).
- **Everything verified in the new location**: gp-oc-dashboard fsck clean, 124 tracked files
  byte-identical to HEAD, all commits pushed, 1.5GB gitignored `data/` complete (45 files; CSVs
  structurally checked, all 22 xlsx/pptx/zip pass CRC tests). `data/Unconfirmed 819145.crdownload`
  is junk, safe to delete.
- Other repos in `C:\GitHub`: myvaccs / nhshd judge / ni-prescribing-explorer clean+pushed;
  **incubator has 25 uncommitted modified files** and **bin-collection-northern-ireland has 1** (all
  verified genuine edits, not corruption — commit & push them); `gpip-medication-review` and
  `hle-decomposition` are empty scaffolds (git init + remote, zero commits, zero files — confirmed
  same on onedrive.com; use or delete).

## 3. Loose ends for the next session

1. **GitHub Desktop still points at the old paths** — for each repo: click it in the left list →
   "Can't find repository" → Locate → same repo under `C:\GitHub`. (A computer-use attempt to do
   this stalled on the permission dialog; do manually or retry.)
2. Commit & push incubator (25 files) and bin-collection (1 file).
3. Claude projects/sessions: remove old OneDrive folder connections; connect `C:\GitHub`.
4. **Next substantive work: the workforce ×2 hotfix** — regenerate the 8 workforce columns in
   `xsec_master_2026` from the corrected `workforce_panel` (period 202503; use `nurses_fte` for
   nurse FTE), refresh the staffing figures the live pages display, redeploy. Then the rest of the
   fix list in the findings file §5.
5. Git hygiene notes that no longer apply post-move: index null-sha1/lock corruption was OneDrive;
   `git config user.email` is set. The OneDrive byte-check hazard is obsolete for `C:\GitHub`.
