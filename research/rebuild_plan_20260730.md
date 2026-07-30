# 30 July 2026 rebuild — plan and reversible groundwork

_Prepared 30 Jul 2026. Executes NOTES_BATCH_DRAFT §D (items 1–11), the audit §5 fix list, and the
day's new data (GPAD/CBT/OC June 2026). Every claim below was re-verified against the on-disk files,
not taken from the notes. Nothing canonical was overwritten; all new outputs are in
`research/data/rebuild_20260730/` (and the pre-existing `research/data/staging_20260730/`)._

**Governing rule — vintage by purpose.** Explanatory/predictor models KEEP Mar 2025 workforce/census
inputs (the predictor must precede the Jan–Mar 2026 GPPS fieldwork). The latest census (May, and June
once ingested) belongs ONLY on the descriptive "compare my practice" surfaces. These two uses never
share a vintage. This is honoured throughout the plan.

---

## 1. Parquet / data freshness audit

Direct answer to "we must need to update parquets?": **Yes — five inputs, and only for the descriptive
tool + the two source-stale models. The explanatory predictor models need NO new-vintage parquet; by
design they stay on May-2026 phones / Mar-2025 staffing.** Verified latest periods on disk:

| File (models/tool dependency) | Latest on disk (verified) | Newer edition now exists? | Needs rebuild? | Why / for what |
|---|---|---|---|---|
| `panel_merged.parquet` (GPAD appts + OC merged) | May 2026 (max month `2026-05`, 39 months) | **GPAD June 2026 pub 30 Jul; OC June pub 30 Jul** | **Yes — for the tool's demand card + waits/substitution work** | Ingest June appts + June OC. Predictor models are spec'd on May (D.11 keeps single-May) so they don't require it, but the descriptive demand card should move to June. |
| `waits_panel.parquet` | May 2026 (max `2026-05`) | GPAD June 2026 (30 Jul) | **Yes** | Waits card on the tool + the §4.14 substitution rerun (D.8) want the June contract-metric edition. |
| `cbt_ivr_panel.csv` + `cbt_daytime_may.parquet` | May 2026 (18 months, Oct 2024–May 2026) | **CBT June 2026 pub 30 Jul 09:30 — first with practice-level call-waiting times (Table 4b)** | **Yes — highest-value new data** | June call-waiting times → phones card (D.4). Already extracted to `cbt_jun26/cbt_waiting_jun26_practice.csv` and staged as parquet (see §4). |
| `workforce_panel.parquet` | **Mar 2026** (max period `202603`) — NOT May/June | May 2026 (pub 25 Jun, raw in `data/gpw_may26/`, not ingested); June 2026 (pub 23 Jul) | **Yes — for descriptive pages only** | Ingest May/June so the capacity card's absolute FTE is current. Models keep Mar 2025 (period `202503`), which is already in the panel. |
| `panel_oc.csv` | **Mar 2026** (max month `2026-03`) — 2 releases behind merged panel | Apr + May 2026 already in `panel_merged`; June pub 30 Jul | **Yes — before re-running `did_anima.py`** | `did_anima.py` derives its Continuum/Anima adopter flag from `panel_oc`, so the flag is frozen at Mar 2026. Re-extend (or read supplier from the merged-panel source) first. |
| `xsec_master_2026.parquet` | Cross-section; workforce ×2 **fixed** (see §4) | — | **Yes — promote `xsec_master_rebuilt` after its 5 external cols are re-derived** | Prescribing cols (`abx/statins/items`) are Mar-2025 EPD and not source-reproducible; closure/merger need epraccur. Rebuilt recovers 126 practices (6,007→6,133). |
| `gpps_long.parquet` | 2026 wave (fieldwork Jan–Mar 2026) | 2026 is latest (next wave Jul 2027) | No | Current. |
| `fft_gp_panel.parquet` | May 2026 | May 2026 latest | No | Current. |
| `xsec_ext_payments2425.parquet` | 2024/25 | 2024/25 latest annual | No | Current. |
| `xsec_ext_fingertips2425.parquet` | 2024/25 | Locked to QOF 2024/25 until 27 Aug 2026 | No | Current (diary QOF 2025/26). |
| `xsec_ext_reg65_202503.parquet` | Mar 2025 (202503) | — | No (models) | Vintage-locked baseline for predictor models. |
| `xsec_ext_pcn_feb26.parquet` | Feb 2026 | — | No | Current. |
| `cvdprevent_practice.parquet`, `qof_prevalence_2425.parquet`, `nhs_app_mi.parquet`, `pomi_online_services_practice.parquet`, `practice_age_sex.parquet`, `practice_list_history.parquet`, `practice_weighted_list.parquet`, `acsc_emergency_icb.parquet`, `fingertips_cancer_emergency_practice.parquet` | per audit (Dec 2025 / 2024/25 / terminal Aug 2024 / Jul 2026) | mostly annual/terminal | No | New-but-unused or archival; fold QOF+CVDPREVENT into typology/unmet-need only. Recheck CVDPREVENT for a Mar 2026 extract first. |

**Bottom line on parquets:** the five that need a rebuild are `panel_merged`, `waits_panel`, the CBT
files, `workforce_panel`, and `panel_oc`. Of these, only CBT June is genuinely new capability (adds a
metric that did not exist before). GPAD/OC/workforce June are routine monthly extensions. **No
predictor-model parquet needs re-vintaging** — that would break vintage-by-purpose.

---

## 2. Model rerun plan (predictor / f2f / deflection / DiD)

### Model scripts that exist
- `research/scripts/predictors_models.py` — **the runner for every table on `predictors.html`** (A: 3
  outcomes × alone/together/+report on the CBT sample; B: all-practices; C: continuity; D: phone-only
  validity; E: external→deflection; F: descriptives). Reconstructed 15 Jul, reproduces the page to
  mean |diff| 0.07pp.
- `research/scripts/f2f_increasers.py` — f2f→satisfaction confound cohort (outcome `satisfaction_2026`).
- `research/scripts/did_anima.py` — Anima/Continuum DiD (adopter flag from `panel_oc`).
- `research/scripts/build_xsec.py` (OLD; reads `panel_merged.csv` + `/tmp` paths) and
  `research/scripts/build_xsec_full.py` (NEW; **already reads `panel_merged.parquet`, `waits_panel.parquet`,
  `workforce_panel.parquet`** → writes `xsec_master_rebuilt.csv`). Also `models_xsec.py`,
  `change_model.py`, `event_study*.py`, `cancer_mode.py`.

### The `build_xsec.py` → parquet item, resolved
Audit fix-list item 2 ("switch `build_xsec.py` to the parquet") is **already satisfied by
`build_xsec_full.py`**, which reads the three parquets directly. The legacy `build_xsec.py` still points
at `panel_merged.csv` and `/tmp/*` staging files and should simply be retired/marked superseded — do
NOT resurrect it. Confirmed by reading both scripts.

### Inputs by vintage (the critical table)
| Input | Predictor/explanatory models | Descriptive tool |
|---|---|---|
| Workforce / GP composition | **Mar 2025** (`gp_composition_mar25.csv`, `workforce_panel` 202503) — KEEP | **May→June 2026** (`gp_composition_may26.csv`) |
| CBT phones | **May 2026** (spec; D.11 considers Mar–May averaging but default stays single-May) | **June 2026** (new call-waiting times) |
| OC submissions | **Feb–Apr 2026 mean** (May flagged incomplete) — KEEP | June 2026 (check partial-submission flags) |
| GPAD appts | **May 2026** (spec) | June 2026 |
| GPPS outcomes | **2026 wave** | 2026 wave |
| List denominator | xsec 12-month GPAD average (uniform) | `list_jul26.csv` (1 Jul 2026 snapshot) |

### Steps
1. **Complete `xsec_master_rebuilt` external columns from source** (currently NULL for the 126
   recovered practices — verified: `abx_per1k` 5,993/6,133 non-null, `statins/closure/merger`
   6,007/6,133): pull EPD Apr 2026 (mind SNOMED-string change 11 May 2026 + ICB mergers from Apr 2026;
   consider a 12-month window) and epraccur (closure/merger flags + the ODS practice-name source that
   §4.25 needs so no-survey practices still render). Fold these merges into `build_xsec_full.py` so the
   table regenerates in one command. **Write to a NEW path** (e.g. `rebuild_20260730/xsec_master_rebuilt_v2.csv`),
   never over the existing `xsec_master_rebuilt.csv`.
2. **Rerun predictor models** on the completed rebuilt table:
   `python3 research/scripts/predictors_models.py <rebuilt_v2.csv> --tag rebuilt`. Keep all vintage
   inputs as spec'd (Mar 2025 staffing, May 2026 CBT). Expected: n rises 4,736→~4,818 (CBT sample) /
   5,918→~6,039 (all); standardised coefficients move <0.1pp. Re-quote the admin×size interaction from
   the new run (Q16 −0.48→−0.16, Q1 −0.68→−0.20 in the staged rerun).
3. **Re-extend `panel_oc` past Mar 2026, then rerun `did_anima.py`** so the adopter flag is current.
4. **Rerun `f2f_increasers.py`** on the rebuilt cross-section (outcome unchanged).
5. Refresh `predictors.html` tables from the new coefficient CSV; refresh page n's and the admin×size
   line.

**Groundwork already done (see §4):** the before/after predictor rerun on live vs rebuilt is staged and
shows deltas ≤0.04pp on the key coefficient families — the rebuild does not move any conclusion.

---

## 3. Compare-my-practice page update plan

### What `mypractice.html` reads (verified by grep)
`xsec_master_2026.parquet`, `xsec_supplement.csv`, `panel_merged.parquet`, `waits_panel.parquet`,
`gpps_long.parquet`, `fft_gp_panel.parquet`, `cbt_ivr_panel.csv`, `cbt_daytime_may.parquet`,
`gp_composition_may26.csv`, `list_jul26.csv`. (`explore.html` reads a similar set plus
`practice_list_history.parquet`, `rush_both_sameday.csv`, `xsec.parquet`.)

### What needs the June refresh
| Card | Current source | Action for 30 Jul |
|---|---|---|
| **Phones** | `cbt_ivr_panel.csv` (→May 2026) + `cbt_daytime_may.parquet` | **Add CBT June call-waiting times** (`% answered <2 min`, total/core/8–10am) — a metric that did not exist before June. Staged parquet ready (§4). Update the card + summary + the size-gap narrative (§4.23 test: answering speed accounts for ~28% of the phone-ease size gap; a −6.5pp size penalty survives). |
| **Capacity / staffing** | `gp_composition_may26.csv` (latest census — already moved off Mar 2025 on 14 Jul) | Move to **June 2026 census** once `workforce_panel`/composition June is ingested (pub 23 Jul). Descriptive surface, so latest census is correct here. |
| **Demand & delivery** | `panel_merged.parquet` May 2026 | Move contacts/appt comparator to **June 2026** appts + OC after the merged-panel rebuild. |
| **Waits** | `waits_panel.parquet` May 2026 | Refresh to June 2026 GPAD edition. |
| **Registered population / identity** | `list_jul26.csv` (1 Jul 2026 snapshot) | Refresh at the monthly Patients-Registered publication (D.10); consider renaming to `list_current.csv` + date column so the page label is generated, not hard-coded. |
| **What patients reported** | `gpps_long.parquet` 2026 | No change (2026 is latest wave). |

### Concrete steps
1. Ingest CBT June into a phones-card source (staged parquet in `rebuild_20260730/` is ready to point at
   or fold into `cbt_ivr_panel`/a new `cbt_waiting` file).
2. Ingest June GPAD/OC into a new `panel_merged` edition; ingest workforce June into `workforce_panel`
   + a `gp_composition_jun26.csv`.
3. Point the capacity/demand/waits cards at the June editions; leave GPPS as-is.
4. Verify the capacity card mixes no doubled/undoubled FTE sources (audit §2, blast-radius bullet):
   confirm each element reads the corrected composition file, not a legacy xsec column.
5. Re-run any hard-coded national/size-fifth benchmarks off the refreshed files.

---

## 4. Reversible groundwork actually done this session (all non-destructive)

1. **Workforce ×2 bug — verified FIXED.** Joined `xsec_master_2026` to a **deduped** `workforce_panel`
   (period 202503; confirmed no duplicate rows — 6,219 rows = 6,219 distinct practices, so the brief's
   "dedupe before checking" caveat does not currently bite). `gp_fte(xsec)/gp_fte(panel)` = **1.00000
   for all 5,964 joinable practices** (min 1.00000, max 1.00000). Spot: A81001 xsec `gp_fte` = 3.7067,
   `gp_per10k` = 9.53 (not the doubled 7.41). The **nurse-FTE fix is also carried into live xsec**:
   A81001 `nurse_fte` = 0.52 = panel `nurses_fte` (the empty `nurse_fte` column was replaced). The
   descriptive pages therefore already show correct absolute FTE. No fix needed; the bug is closed.
2. **CBT June practice-level waiting times staged** to
   `research/data/rebuild_20260730/cbt_waiting_jun26_practice.parquet` (from the already-extracted CSV):
   **5,061 rows, 4,965 distinct practices**, median 62.2% answered <2 min (total) / 55.5% at 8–10am —
   matches the June national figures. Ready to fold into the phones card. Nothing overwritten.
3. **Rebuilt-vs-live cross-section counts confirmed:** live `xsec_master_2026` = 6,007 rows; rebuilt =
   6,133 (+126 recovered practices). The 5 external backfill columns are **still NULL for the 126
   recovered practices** (verified) — so the "re-derive external columns from source before promotion"
   step (§2 step 1) is genuinely outstanding, exactly as the audit states.
4. **Staged predictor before/after rerun already present** in `research/data/staging_20260730/`
   (`rerun_numpy.py`, `predictors_rerun_before_after.csv`, `key_coef_before_after.csv`): live
   `xsec_master_2026` vs `xsec_master_rebuilt`, spec copied verbatim from `predictors_models.py`,
   vintage held (Mar 2025 staffing, May 2026 phones). **Coefficient deltas are tiny** — e.g. Q1 phone
   queue-answer 6.188→6.168 (−0.02), Q1 deflection −5.789→−5.809 (−0.02), Q16 IMD −0.73→−0.751
   (−0.021); max |delta| across the key families ≈0.04pp. Conclusion: promoting the rebuilt table moves
   no finding, only n (+126) and the admin×size interaction.
5. **Latest-period audit** of every core panel run and tabulated in §1 (panel_merged/waits/CBT = May
   2026; workforce = Mar 2026; panel_oc = Mar 2026).

Files created this session (both under gitignored `research/data/`, no canonical file touched):
`research/data/rebuild_20260730/cbt_waiting_jun26_practice.parquet` and this plan.

---

## 5. Risks / blockers / decisions needed

- **OC June partial-submission flag (blocker for OC use).** OC May 2026 was flagged incomplete by NHSE
  for Blinx, Evergreen Life, iPlato, Silicon and PATCHS — the models already drop May and use Feb–Apr.
  **June must be checked for the same flags before it is used** anywhere (tool demand card or a re-extended
  `panel_oc`). Not verifiable without downloading the June OC edition (not yet downloaded). **User
  decision:** proceed to download GPAD/OC June now, or defer.
- **EPD + epraccur pulls are the gate on promoting the rebuilt cross-section.** Until the 5 external
  columns are re-derived (EPD Apr 2026 with the SNOMED-string/ICB-merger caveats; epraccur closures +
  names), the 126 recovered practices carry NULLs. Predictor models can run on the rebuilt table now
  (those columns aren't in the predictor spec), but a public promotion of `xsec_master_2026` should wait.
- **Do not re-vintage predictor inputs.** The single largest correctness risk in this rebuild is moving
  the composition/predictor models onto the May/June census. Keep them on Mar 2025.
- **`did_anima.py` will silently use a stale adopter flag** unless `panel_oc` is re-extended first —
  sequencing matters.
- **CBT conditions on the participating estate** (~85.5% of practices); the phones-card June metric and
  the size-gap finding are conditional on cloud-telephony practices — state this on the card.
- **Denominator decision still open** (audit §3): adopt canonical "Patients Registered" for per-10k
  metrics, or document the GPAD-average as the deliberate xsec denominator. Needs an AMC call.
- **Housekeeping** (audit §5.9): correct README's "IMD 2019" line to IMD 2025 (Fingertips NGPP 94240);
  fix the dangling "§4.33" reference to batch-draft §4.17.

---

## Follow-up 30 Jul: June data + waiting-time model + phones note

_Executed same day. All new data written to `research/data/rebuild_20260730/`; no canonical file touched;
the one HTML edit is additive and uncommitted._

### A. June data ingest — status

| Task | Result |
|---|---|
| **OC June 2026 download** | Done. `rebuild_20260730/downloads/oc_jun26.zip` (CSV zip, north+south region files, Jan 2025–Jun 2026, 1,001,790 long rows) + `oc_jun26_summary.xlsx`. |
| **GPAD June 2026 download** | **BLOCKED — not yet published.** The series page still lists **May 2026 as "Latest statistics"** and June 2026 under **"Upcoming publications … (Upcoming, not yet published)"**; no resource/file URL exists on the June page. Scheduled 30 Jul 2026 but not live at time of run. No URL to `curl` — not guessed. |
| **panel_merged → June** | **BLOCKED on GPAD June** (appointment columns are GPAD-derived). Not built; would be misleading with null appt counts. Rerun once GPAD June publishes. |
| **waits_panel → June** | **BLOCKED on GPAD June** (same reason). Not built. |
| **panel_oc → June** | **Done** → `rebuild_20260730/panel_oc_to_jun26.parquet`. Canonical schema matched exactly (10 cols). Before: 225,046 rows, max month **2026-03**. After: **243,514 rows, max month 2026-06** (appended Apr 6,168 / May 6,155 / Jun 6,145 practice-months from the June release; history ≤2026-03 kept from canonical). Pivot mapping validated vs canonical on 2026-01/02/03: supplier match 99.9%, oc_total mean abs diff <1 for Jan/Feb (49.9 for Mar = expected retrospective revision). |
| **CBT waiting parquet (1c)** | Confirmed loads: `rebuild_20260730/cbt_waiting_jun26_practice.parquet` — **5,061 rows, 4,965 distinct practices**, month 2026-06. `pct_u2_total` median **62.2%**, mean 61.2% (SD 18.5); `pct_u2_810` (8–10am) median 55.5%. Cols: gp_code, gp_name, inb/ans/pct_u2 × total/core/810. |

**OC June supplier caveats (Table 1 notes, `oc_jun26_summary.xlsx`).** June differs from May:
- **Note 9 (June):** *"Partial submissions have been received from Blinx, Evergreen Life, and EConsult Health Ltd for June 2026, so data for practices using these systems will be incomplete."* — **EConsult is a dominant supplier**, so June OC is materially more affected than May.
- **Note 7:** no submission since **late April 2026 from iPlato** (so iPlato practices missing from May onward).
- **Note 6:** no submission since **mid-March 2026 from Doctaly**.
- Silicon and PATCHS (flagged for May) are **not** flagged for June; the May-specific flag was Blinx + Silicon (note 8).
- Net: June incomplete/absent suppliers = **Blinx, Evergreen Life, EConsult (partial); iPlato, Doctaly (absent).** Treat June OC as incomplete for EConsult/Blinx/Evergreen/iPlato/Doctaly practices before any demand-card or model use.

### B. Waiting-time model — June `pct_u2_total` (% answered <2 min) → GPPS 2026 outcomes

WLS, weight = `gpps_n_2026`, HC1 robust SE, region fixed effects, predictors z-scored within sample;
`pct_u2_total` joined from the CBT June parquet to `xsec_master_2026.csv`; practices with gpps_n_2026 ≥ 30.
Coefficients are **survey points per 1 SD** of the answering-speed measure.

| Outcome | Region-FE only (coef/SD, SE) | + controls (coef/SD, SE, p) | n | Survives controls? |
|---|---|---|---|---|
| **phone_easy_2026** (primary) | +9.18 (0.23) | **+6.80 (0.23), p≈4e-193 \*\*\*** | 4,846 | Yes |
| access_satisfaction_2026 | +4.55 (0.17) | **+3.50 (0.17), p≈3e-93 \*\*\*** | 4,846 | Yes |
| satisfaction_2026 | +3.18 (0.15) | **+2.39 (0.15), p≈4e-56 \*\*\*** | 4,846 | Yes |
| deflection_2026 (told to contact again; lower=better) | −1.09 (0.08) | **−0.93 (0.08), p≈6e-31 \*\*\*** | 4,791 | Yes |

Controls: log_list, imd_score, gp_per10k, pct65plus, nonwhite_pct (+ region FE).

- **Confirms the prior §4.23 finding on phone ease** (+6.6/SD*** → reproduced at **+6.80/SD***).
- **Size-gap absorption (phone_easy):** z_log_list coefficient moves **−8.99 → −6.34** when answering
  speed is added = **29.5% of the practice-size penalty absorbed** (confirms the ~28% prior).
- The association is highly significant and survives the full control set for **all four** outcomes; better
  phone answering-speed → higher phone ease, higher contact/overall satisfaction, and less deflection.

### C. Drafted phones note (mypractice.html) — for AMC sign-off

**Placement:** inside the `<details id="d-phones">` "Phones — the evidence" block, immediately after the
`#daytime` card and before `</details>` (research/mypractice.html, after line 81). Additive `<p class="ev"
id="callwaiting-note">`, wrapped with a `DRAFT … pending AMC sign-off` HTML comment. **Git-tracked,
uncommitted (+9 lines), fully reversible** (`git diff research/mypractice.html`).

**Exact inserted text (draft):**
> **Call-waiting times (draft note — pending sign-off).** The national call-waiting figures now published
> for June 2026 — the share of calls answered within two minutes — come after this year's patient survey
> fieldwork (January to March 2026), so they describe how the phones are running now and cannot explain the
> survey scores above. Across practices, answering a higher share of calls within two minutes goes with
> better patient-reported phone ease (about 6.8 points higher for each standard-deviation improvement), and
> this accounts for roughly 30% of why larger practices tend to score worse on getting through by phone. As
> elsewhere on this page these are associations across practices, not a promise that faster answering will
> move your own score.

### Blockers / decisions
- **GPAD June not yet published** → `panel_merged`/`waits_panel` June extension deferred; rerun the two
  `agg_*.py` aggregations + merge once the June `Practice_Level_Crosstab_Jun_26.zip` URL appears on the
  publication page. (OC June already staged, so the merge input is ready.)
- **OC June is materially incomplete for EConsult (major supplier) + Blinx/Evergreen/iPlato/Doctaly** —
  models that use OC should keep dropping the affected months/suppliers (predictor spec already uses
  Feb–Apr mean; do not adopt June OC for the demand card without excluding these suppliers).
- **Phones note wording is a DRAFT** — numbers are load-bearing (6.8 pts/SD, ~30% size-gap) and verified,
  but the prose needs AMC's sign-off before it goes live.
