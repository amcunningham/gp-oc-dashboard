# Continuity and appointment timing analysis workspace

This archive preserves the temporary files used for the practice-level GPPS and GPAD analysis.

## Source and derived data

| File | Description |
|---|---|
| `gpps_practice.csv` | GP Patient Survey 2026 practice-level data. |
| `gpps_vars.xlsx` | GPPS variable list/data dictionary downloaded with the practice data. |
| `gpad.zip` | Downloaded GPAD practice-level files for January, February and March 2026, plus practice mapping. |
| `gpad_agg.csv` | Derived practice-level GPAD counts for the January–February and March analysis periods. |
| `imd.csv` | National General Practice Profiles extract containing practice-level IMD 2025 scores. |
| `payments.csv` | NHS Payments to General Practice 2024/25 practice-level file used for rurality, dispensing status and registered-list size. |

## Analysis scripts

| File | Description |
|---|---|
| `replicate.py` | Initial adjusted GPPS model specification. |
| `replicate2.py` | Corrected GPPS weighted models, covariate construction and practice-level data linkage. |
| `gpad_models.py` | GPAD-only and combined GPPS–GPAD models, including January–February and January–March sensitivity measures. This script imports the setup section of `replicate2.py`. |

## Important notes

- Files are linked by NHS GP practice code.
- The results reported in the briefing use January–February 2026 GPAD measures.
- March was included in sensitivity models and made no material difference.
- `gpad_models.py` expects these files to be located under `/tmp`. To rerun elsewhere, change the paths at the top of the scripts or place the extracted files in the working directory and replace `/tmp/` with that directory.
- The scripts require Python with `pandas` and `numpy`.
- These are working analytical scripts rather than a final reproducible research package. Preserve the archive unchanged and work from a copy.
