# GP Access Research Dataset

Practice-level open-data research on how English general practices organise appointment access
— same-day vs booked-ahead models — and what that means for patients. Built July 2026 from
publicly available NHS data. Companion to the [GP OC Dashboard](https://amcunningham.github.io/gp-oc-dashboard/).

**Analysis notes and full findings:** [PANEL_NOTES.md](PANEL_NOTES.md)
**GPPS 2025 question/variable reference:** [GPPS_2025_questions.md](GPPS_2025_questions.md)

## Ask the data in plain English

**[explore.html](https://amcunningham.github.io/gp-oc-dashboard/research/explore.html)** — a
natural-language interface: your question is translated to SQL by a language model (Claude API
key, or a local Ollama model — nothing to install on any server), the SQL is always shown and
editable, and queries run entirely in your browser via DuckDB-WASM. Interpretation caveats are
built into the prompt.

The explorer has three model options: a **shared demo** (rate-limited, questions logged
anonymously — see `worker/SETUP.md` for how it's run), your own Anthropic API key (nothing
logged), or a local Ollama model (fully offline).

## Query this data without downloading anything

All tables are plain CSV/Parquet, so they can be queried in the browser:

**DuckDB shell** ([shell.duckdb.org](https://shell.duckdb.org)) — paste, for example:

```sql
SELECT month, ROUND(100.0*SUM(same_day)/SUM(total),1) AS same_day_pct
FROM 'https://raw.githubusercontent.com/amcunningham/gp-oc-dashboard/main/research/data/waits_panel.parquet'
GROUP BY 1 ORDER BY 1;
```

**Datasette-Lite** — explore the practice cross-section with a point-and-click UI:
`https://lite.datasette.io/?csv=https://raw.githubusercontent.com/amcunningham/gp-oc-dashboard/main/research/data/xsec_master.csv`

**Python/R** — `pd.read_parquet(url)` / `arrow::read_parquet(url)` on any of the raw URLs.

## Core tables

### `data/xsec_master_2026.csv` / `.parquet` — practice cross-section (n=6,007, 90 columns)
One row per practice. Exposure year Apr 2024–Mar 2025 unless noted. This is the file the
explorer serves; `xsec_master.*` is the frozen pre-2026-wave version. Key column groups:

| Group | Columns | Source |
|---|---|---|
| Identity | `gp_code`, `region` | NHS England |
| Access model (GPAD, 12m) | `same_day_pct_12m`, `sd_share`, `sd_percap`, `appts_percap`, `phone_pct_12m`, `f2f_pct_12m`, `dna_pct_12m`, `appts_12m` | Appointments in General Practice |
| GP vs other staff | `gp_sd`, `oth_sd`, `gp_15p`, `oth_15p`, `gp_share`, `high80` (no-booking cohort flag) | GPAD |
| Wait bands (12m) | `sd_pct`, `d1_7_pct`, `d8_14_pct`, `d15plus_pct`, `gp_d15plus_pct` | GPAD |
| Online consultation | `oc_rate_12m`, `oc_tertile_feb26` | OC Submissions publication |
| Structure | `list_size`, `log_list`, `rural`, `dispensing_f`, `imd_score`, `imd_quintile`, `pct65plus`, `nonwhite_pct` | NHS Payments 24/25, IMD, GP Workforce census, GPPS |
| Workforce | `gp_per10k`, `nurse_per10k`, `dpc_per10k`, `gp_fte`, `nurse_fte`, `dpc_fte`, `admin_fte` | GP Workforce Mar 2025 |
| Mergers/closures | `merged_recent` (list-jump proxy — superseded), `closure_exposed`, `merger_recipient` | ODS epraccur + panel |
| Patient experience (GPPS 2025) | `satisfaction` (Q32), `continuity` (Q7), `pt_same_day` (Q20), `wait_too_long` (Q21), `nextstep_immediate` (Q13), `contact_fail` (Q12), `phone_failed` (Q11), `ae_after_fail`/`ae_pop` (Q15), `deflection_2025`/`couldnt_contact_2025` (Q12 categories), `gpps_n` | GP Patient Survey 2025 |
| Patient experience (GPPS 2026, fieldwork Jan–Apr 2026) | `satisfaction_2026`, `continuity_2026`, `access_satisfaction_2026`, `phone_easy_2026`, `nextstep_immediate_2026`, `wait_too_long_2026`, `deflection_2026`, `couldnt_contact_2026`, `gpps_n_2026` (`pt_same_day_2026` present but unverified — low year-on-year correlation suggests a category-mapping issue) | GP Patient Survey 2026 |
| Clinical outcomes | `qof` (% points 24/25), `cdr` (cancer detection), `conv` (TWW conversion), `ref_rate` (USC referrals), `ca_em_rate` (cancer emergency admissions) | QOF, Fingertips/NDRS |
| Workload & prescribing | `dm_prev` (diabetes prevalence 24/25), `items_per_pt`, `abx_per1k` (Mar 2025) | Fingertips, NHSBSA EPD |

### `data/panel_merged.parquet` — practice × month panel (223,707 rows)
Mar 2023 – May 2026. GPAD counts (`total`, `same_day`, `next_day`, `gp`, `gp_same_day`, `f2f`,
`phone`, `online`, `dna`, `attended`) + monthly OC metrics (`oc_total`, `oc_clinical`,
`oc_admin`, `oc_rate_1k`, `oc_capability`, `oc_usage`, `supplier`, `list_size`) + IMD, region,
derived `same_day_pct`, `gp_same_day_pct`.

### `data/waits_panel.parquet` — practice × month wait bands (~229k rows)
Mar 2023 – May 2026: `same_day`, `d1`, `d2_7`, `d8_14`, `d15_21`, `d22_28`, `d28plus`, `unk`,
plus GP-specific `gp`, `gp_d8_14`, `gp_d15plus`.

### Supporting tables
`panel_oc.csv` (OC submissions panel Apr 23–Mar 26) · `change_2024_2025.csv` (GPPS change
models) · `event_study_main.csv` / `event_study_supplier.csv` (OC adoption event-study
coefficients) · `gp_vs_other_waits_trend.csv` (national monthly GP vs other-staff wait mix) ·
`rush_both_sameday.csv` (8–10am call & OC concentration vs same-day %) ·
`merger_ods_validated.csv` (closure-exposure flags).

## Scripts

`scripts/` contains the full build pipeline: GPAD release aggregation (`agg_duck2.py`,
`agg_waits.py`, `fetch_all_gpad.sh`), panel/cross-section assembly (`build_xsec.py`),
and the analysis models (`models_xsec.py`, `event_study*.py`, `change_model.py`,
`cancer_mode.py`). All use DuckDB + pandas/statsmodels.

## Sources and licences

All inputs are open data published under the [Open Government Licence v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/):
NHS England (Appointments in General Practice; Submissions via Online Consultation Systems;
Cloud Based Telephony; General Practice Workforce; NHS Payments to General Practice; QOF; ODS),
GP Patient Survey (NHS England/Ipsos), OHID Fingertips (NDRS cancer indicators, QOF prevalence),
NHSBSA English Prescribing Data, MHCLG IMD.

Derived dataset released under CC0, consistent with the repository licence. If you use it,
please cite this repository and the underlying NHS England sources.

## Known caveats (read before using)

- GPAD is official statistics *in development*: no national data-entry standards; time-from-
  booking partly reflects appointment-system configuration (total-triage practices may book
  everything same-day). The same-day **share** is a configuration measure, not a patient-
  experience measure — see PANEL_NOTES for the perception-vs-supply analysis.
- OC participation is voluntary and grew over the period; supplier field may reflect multiple
  concurrent systems.
- GPPS is a sample survey (weighted practice estimates; respondents skew older); sentinel codes
  (< 0) must be treated as missing — already cleaned in these tables.
- Practice codes are not longitudinally stable through mergers; closure flags are approximate.
- From 2026/27 the GP contract requires clinically urgent care to be recorded as same-day —
  treat Apr 2026+ GPAD as a new recording regime.

## Author

Anne Marie Cunningham, GP. Built with assistance from Claude (Anthropic).
The analysis and any errors are mine.
