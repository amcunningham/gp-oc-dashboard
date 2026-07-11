# Cross-section rebuild proposal — `xsec_master_rebuilt.csv`

**Author:** reproducibility session, 2026-07-11
**Status:** PROPOSAL. No live file was modified. New files only:
`research/scripts/build_xsec_full.py`, `research/data/xsec_master_rebuilt.csv`, this document.

## 1. Problem

The live cross-section `research/data/xsec_master_2026.{csv,parquet}` (6,007 practices, 98
columns) was assembled by an earlier session against an **earlier GPAD appointments extract**.
When the inclusion rule (>1,000 GPAD appts Apr-2024–Mar-2025, has IMD, in GPPS 2025) is applied
against the **current corrected `panel_merged.parquet`**, **6,133** practices qualify — **126**
more than the live master. These were dropped spuriously by the stale extract (e.g. **A82071**,
Burnett Edgar Medical Ctr, 27,170 appts 2024/25, IMD 23.75 — present in the corrected panel,
absent from the live master, patched into `xsec_supplement.csv`).

`build_xsec_full.py` regenerates the cross-section from the current corrected sources, keyed on
`gp_code`, so those practices are included, and reproduces the 98-column schema as closely as
the in-repo sources allow.

## 2. Practice-count delta

| set | practices |
|---|---|
| live `xsec_master_2026` | 6,007 |
| **rebuild `xsec_master_rebuilt`** | **6,133** (+126) |
| current practices retained in rebuild | 6,007 / 6,007 (0 lost) |
| brand-new practices (the recovered set) | 126 |
| `xsec_supplement.csv` rows | 159 |
| supplement rows recovered by rebuild | **126** (incl. A82071) |
| supplement rows still excluded | 33 — all legitimately fail inclusion: 21 absent from the current panel, 4 with ≤1,000 appts, 8 with no IMD |

The "~134 recoverable" estimate in the brief resolves to **126** once every criterion is checked
against the corrected panel; the other 33 supplement practices do not meet inclusion and should
stay out (or be handled as explicit exceptions).

## 3. Provenance table (98 columns)

Legend for **Reproducible now**: **yes** = re-derived from a repo source, matches live master;
**yes\*** = re-derived, correlates 1.0 with live but a documented scale/level difference;
**backfill** = copied from a repo lookup (not the original upstream); **no** = upstream source is
not in the repo, emitted NULL.

| column(s) | source / derivation | repro now |
|---|---|---|
| `same_day_pct_12m, gp_same_day_pct_12m, phone_pct_12m, f2f_pct_12m, dna_pct_12m, oc_rate_12m, list_size, imd_score, imd_quintile, region, appts_12m` | GPAD panel `panel_merged.parquet`, aggregated Apr2024–Mar2025, HAVING SUM(total)>1000 (per `build_xsec.py`) | **yes** (corr 1.0, mad 0) |
| `gp_share, gp_sd, oth_sd` | panel_merged: GP share, GP same-day %, other-staff same-day % | **yes** |
| `sd_share, sd_share_prior_year` | panel_merged same-day share ×100 (prior_year = Apr2023–Mar2024) | **yes** |
| `sd_percap, appts_percap` | panel_merged same-day / total per 1,000 patients per month (×1000/12) | **yes** |
| `max_jump` | max month-on-month list-size ratio, Apr2023–Mar2025 | **yes** |
| `sd_pct, d1_7_pct, d8_14_pct, d15plus_pct, gp_d15plus_pct, gp_15p, oth_15p` | wait-band panel `waits_panel.parquet`, 12m to Mar2025 | **yes** |
| `satisfaction, continuity, has_pref_hcp, gpps_n, access_satisfaction, phone_easy, website_easy, app_easy, nonwhite_pct, pt_same_day, wait_too_long, nextstep_immediate` | GPPS 2025 file `data/GPPS_2025_...PUBLIC.csv` (`.pcteval`/`.pct` stems; nonwhite = 100−White band); sentinel <0 → NULL | **yes** |
| `deflection_2025, couldnt_contact_2025` | GPPS 2025 Q12 `gpcontactnextstep_3/_4.pct` | **yes** |
| `satisfaction_basew, continuity_basew, access_basew, phone_basew` | GPPS 2025 `.baseevalw` stems | **yes\*** (corr 0.88–0.99; not exact — likely different row filter in original) |
| `satisfaction_2024, continuity_2024` | GPPS 2024 file `data/GPPS_2024_...PUBLIC.csv` | **yes** |
| `satisfaction_2026 … app_easy_2026` (13 cols) + `gpps_n_2026` | GPPS 2026 file `data/GPPS_2026_...PUBLIC.csv` (logic per `ingest_gpps2026.py`) | **yes** |
| `gp_fte, nurse_fte, dpc_fte, admin_fte, gp_per10k, nurse_per10k, dpc_per10k, admin_per10k` | `workforce_panel.parquet` period 202503 (nurse from `nurses_fte` col; per10k = 10000·FTE/list) | **yes\*** — see §5: live master values are **exactly 2× these**; rebuild uses corrected single values |
| `log_list, merged_recent, size_q, high80, rural†, dispensing_f†` | derived (log list; max_jump>1.15; list quartile; gp_sd≥80) | **yes** (rural/dispensing_f need §below source → NULL) |
| `gp_name, postcode, icb_name` | epraccur/ODS (not in repo) — **backfilled** from `adoption_risk_2027.csv` | **backfill** (66% coverage) |
| `pcn_name, sub_icb_name` | epraccur/ODS | **no** (no full repo lookup) |
| `rurality, dispensing, rural, dispensing_f` | NHS Payments 2024/25 practice CSV | **no** (file not in repo) |
| `closure_exposed, merger_recipient` | epraccur closure list (±2 months same-PCN; +≥5% jump) | **no** (epraccur not in repo) |
| `cdr, conv, ref_rate` | Fingertips API 91347 / 91845 / 91882, 2024/25 (`cancer_mode.py`) | **no** (API) |
| `qof` | Fingertips ind. 295, 2024/25 | **no** (API) |
| `ca_em_rate, ca_em_n` | Fingertips 91355 (cancer emergency admissions) | **no** (API) |
| `dm_prev` | Fingertips 241 (diabetes QOF prevalence) | **no** (API) |
| `abx_per1k, items_per_pt, statins_per1k` | NHSBSA EPD API, Mar 2025 (BNF 0501 / total / statins) | **no** (API) |
| `pct65plus` | GP Workforce census age bands | **no** (age bands not in `workforce_panel.parquet`) |
| `contact_fail` | GPPS 2025 — **stem unresolved** (best guess `gpcontactnextstep_4` correlates only 0.44 with live) | **no** (emitted NULL pending correct mapping) |
| `phone_failed, ae_after_fail, ae_pop` | GPPS 2025 Q11/Q15 composite derivations (scripts not in repo) | **no** |

† `rural`/`dispensing_f` are derived from `rurality`/`dispensing`, which are not reproducible, so
they are NULL in the rebuild.

## 4. Validation

**(a) Retention + key-column fidelity** — all 6,007 live practices are present in the rebuild
(0 lost). On the shared 6,007, the five key columns match the live master **exactly**:

| column | n | corr | mean abs diff |
|---|---|---|---|
| satisfaction_2026 | 6,007 | 1.000000 | 0.000000 |
| continuity_2026 | 5,996 | 1.000000 | 0.000000 |
| same_day_pct_12m | 6,007 | 1.000000 | 0.000000 |
| imd_score | 6,007 | 1.000000 | 0.000000 |
| list_size | 6,007 | 1.000000 | 0.000000 |

Across **all** reproduced numeric columns, correlation with the live master is 1.0000 and mean
absolute difference 0.0000, except: workforce (corr 1.0, level ×2 — §5), `.baseevalw` (corr
0.88–0.99), and `contact_fail` (nulled).

**(b) Recovered practices** — the 126 new practices are exactly the recoverable subset of
`xsec_supplement.csv`, including **A82071** (confirmed present). The 33 non-recovered supplement
rows all fail inclusion legitimately (see §2).

**(c) Columns not reproduced** (23 all-NULL in the rebuild): `rurality, dispensing, rural,
dispensing_f, closure_exposed, merger_recipient, qof, ca_em_rate, ca_em_n, pct65plus,
ae_after_fail, ae_pop, contact_fail, phone_failed, dm_prev, abx_per1k, items_per_pt,
statins_per1k, cdr, conv, ref_rate, pcn_name, sub_icb_name`. Geography `gp_name/postcode/icb_name`
are backfilled at 66% coverage only.

## 5. Notable discrepancy: workforce is doubled in the live master

For every practice, the live master's `gp_fte`, `nurse_fte`, `dpc_fte`, `admin_fte` are **exactly
2×** the values in the corrected `workforce_panel.parquet` (period 202503) — correlation 1.0,
ratio 2.00 with zero residual. The rebuild uses the **single (corrected) `workforce_panel`
values**, which match the raw GP-workforce file. Additionally, the live master's `nurse_fte` was
sourced from a column that is empty at Mar-2025 in `workforce_panel` (`nurse_fte`); the rebuild
draws nurse FTE from the populated `nurses_fte` column instead (94.7% coverage). **Consequence:**
`gp_fte/nurse_fte/dpc_fte/admin_fte` and their `*_per10k` derivatives will NOT match the live
master 1:1 — by design, because the live values appear to double-count. This should be confirmed
against the original workforce ingest before switching over.

## 6. Recommendation

**The rebuild is ready to switch over for the appointment-, GPPS-, and wait-band-derived columns
(≈68 of 98), which reproduce the live master exactly while correctly adding the 126 dropped
practices.** It is the right base for a reproducible pipeline and fixes the core defect (stale
GPAD extract).

**Do not switch over wholesale yet.** Before it can replace the live master, backfill the columns
whose upstream sources are not in the repo, and resolve two build questions:

1. **Add the missing upstream sources** (then re-run): NHS Payments 2024/25 (rurality, dispensing);
   epraccur (closures → closure_exposed/merger_recipient; geography → pcn_name, sub_icb_name, full
   gp_name/postcode/icb_name; age bands → pct65plus); Fingertips API (cdr, conv, ref_rate, qof,
   ca_em_rate/n, dm_prev); NHSBSA EPD API (abx_per1k, items_per_pt, statins_per1k).
2. **Resolve `contact_fail`** — its GPPS 2025 stem is unknown (guess correlates only 0.44). Recover
   the original mapping (and the `phone_failed`/`ae_after_fail`/`ae_pop` Q11/Q15 derivations) from
   the original build scripts, which are not in the repo.
3. **Reconcile the workforce ×2 doubling** — decide whether the live master (doubled) or the
   rebuild (corrected single values) is correct; almost certainly the rebuild. Adjust downstream
   models that used the doubled `gp_per10k` accordingly.

Recommended path: keep `xsec_master_rebuilt.csv` as the reproducible base, port the API/epraccur
linkage steps into `build_xsec_full.py` (or a companion enrichment script) so the ~30 not-yet-
reproducible columns are regenerated too, then re-validate and promote.

## 7. How to run

```
python3 research/scripts/build_xsec_full.py
# -> research/data/xsec_master_rebuilt.csv   (6,133 practices, 98 cols)
```
Inputs (all in-repo): `research/data/panel_merged.parquet`, `waits_panel.parquet`,
`workforce_panel.parquet`, `adoption_risk_2027.csv`; `data/GPPS_2024/2025/2026_...PUBLIC.csv`.
