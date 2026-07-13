# Model & data-source currency audit — findings (13 Jul 2026)

_Executes the brief in `model-source-audit.md`. Diagnostic only: no model was re-run, no live page or
cross-section was modified. Every "latest available" below was verified on 13 Jul 2026 against the
NHSE / OHID / NHSBSA / MHCLG publication page (fetched, not assumed); verification notes at the end.
File-integrity check: on-disk byte counts of every notes/script/page file read for this audit matched
`git show HEAD:...` exactly — no OneDrive truncation affected this session's reads._

## 1. Currency / provenance table

Column meanings: **our version** = period covered by the file in the repo; **latest available** = most
recent published release as of 13 Jul 2026, with its publication date where verified.

| source | file we use | our version / date | latest available | current? | action |
|---|---|---|---|---|---|
| GPAD appointments | `panel_merged.{parquet,csv}`, `waits_panel.parquet` | Mar 2023 – May 2026 | May 2026 (pub 25 Jun 2026); June 2026 due **30 Jul 2026** | **Yes** | Refresh at the 30 Jul rebuild (June edition publishes that morning). CSV/parquet now agree (242,345 rows, 6,386 practices) — the §4.25 corrupt-CSV incident is repaired, but `build_xsec.py` still reads the CSV; switch it to the parquet at rebuild. |
| OC submissions | `panel_merged.oc_rate_1k`; `panel_oc.csv` | merged panel: to May 2026 (non-null for 6,128 practices); standalone `panel_oc`: **to Mar 2026** | April 2026 publication is live on NHSE Digital; May 2026 values are already present in the merged panel | **Split** | `panel_oc.csv` is two releases behind the merged panel. `did_anima.py` derives its adopter flag ("Continuum by latest month") from `panel_oc`, so the flag is as of Mar 2026. Re-extend `panel_oc` (or read supplier from the same source as the merged panel) before re-running the DiD. |
| Cloud-based telephony | `cbt_ivr_panel.csv` (+ rush/volumes/daytime files) | Oct 2024 – May 2026 | May 2026 (pub 25 Jun 2026); June edition due late Jul | **Yes** | June edition (first with practice-level call-waiting times per the rebuild list item 4) lands around the 30 Jul rebuild. |
| GPPS | `data/GPPS_2026_Practice_data...csv`; `*_2026` columns in xsec | 2026 wave (fieldwork Jan–Mar 2026) | 2026, published **9 Jul 2026** | **Yes** | Models confirmed on 2026 columns: `did_anima.py` outcomes use `*_2026`; `f2f_increasers.py` outcome is `satisfaction_2026`; predictors-page models (§4.22–4.23, §4.31) are on the 2026 wave. The xsec's unsuffixed GPPS columns are the 2025 wave by design (baseline), not staleness. |
| Workforce (NWRS) | xsec `gp_fte/nurse_fte/dpc_fte/admin_fte` + `*_per10k`; `workforce_panel.parquet` | xsec snapshot: **Mar 2025 (202503), doubled** (see §2); panel: 2018–Mar 2026; raw May 2026 CSVs downloaded to `data/gpw_may26/` but not ingested | 31 May 2026 (pub 25 Jun 2026); June due 23 Jul 2026 | **No** (bugged and 14 months old in xsec) | Fix the ×2 (see §2); ingest May 2026 (or June, out 23 Jul) into `workforce_panel`; at rebuild decide the xsec snapshot month, and split it by purpose (see the composition row and fix-list item 5): the vintage that "aligns with the fieldwork window" is what an explanatory model wants; the descriptive pages should show the latest census regardless. |
| GP composition (detailed census) | `gp_composition_mar25.csv` (drives §4.31 / §4.21 models and the predictors page tables) | Mar 2025 | May 2026 detailed practice file already downloaded (`gp_composition_may26.csv`, `data/gpw_may26/`) | **Split by purpose** | The published composition models pair Mar 2025 staffing with 2026 survey outcomes — which is *correct for an explanatory model*: the predictor (Mar 2025) precedes the Jan–Mar 2026 GPPS fieldwork, so keep those models on the pre-fieldwork vintage. Do **not** re-vintage them to May 2026 (that would put the predictor after the outcome). The May 2026 census belongs only on the *descriptive snapshot* surfaces (mypractice capacity card + factor section, explore), where a practice wants its current standing. Correction 14 Jul — see fix-list item 5; earlier drafts of this row wrongly said "re-run models on May 2026". |
| NHS Payments | `xsec_ext_payments2425.parquet`, `practice_weighted_list` | 2024/25 | 2024/25 (latest annual; classified Management Information) | **Yes** | Note for any payments work: PCN Leadership/Support/Workforce/IIF/Enhanced Access categories were removed from the 2024/25 report. |
| Registration / list size | `list_jul26.csv`, `practice_age_sex` (extract 1 Jul 2026); xsec `list_size` (GPAD-panel 12-month average) | Jul 2026 snapshot; xsec average Apr 2024–Mar 2025 | July 2026 (pub 9 Jul 2026) | **Yes** (snapshot files); xsec denominator is a different flavour — see §3 | Apply the PROJECTS.md denominator rule at rebuild. |
| IMD | `data/practice_imd.csv` → xsec `imd_score/imd_quintile` | **IMD 2025** (all 6,007 xsec values match the file exactly) | English Indices of Deprivation 2025, published 30 Oct 2025 | **Yes** | The brief's "2019 was latest" is out of date: IoD2025 exists and the repo is already on it. Provenance resolved 13 Jul (see §3a): the file is the Fingertips/NGPP practice-population deprivation score (indicator 94240), i.e. the value published for the practice's registered population — not a postcode lookup. `README.md` still describes the file as "IMD 2019 scores"; correct at rebuild. |
| QOF disease prevalence | `qof_prevalence_2425` (21 registers, 6,188 practices) | 2024/25 (pub 28 Aug 2025) | 2024/25; **2025/26 publishes 27 Aug 2026** (confirmed on its NHSE page) | **Yes** | New-but-unused: no model currently ingests it (xsec carries only `dm_prev`, which matches the 2024/25 file exactly, corr 1.0, diff 0). Fold into the typology feature space and the unmet-need study as planned. |
| CVDPREVENT | `cvdprevent_practice` (32 indicators) | extract to Dec 2025, pulled 13 Jul 2026 | Dec 2025 appears to be the latest quarterly extract (the 2025 annual report, pub 11 Dec 2025, uses March 2025 core data; no March 2026 extract was findable on 13 Jul 2026) | **Yes, with a caveat** | Could not verify the extract schedule directly (the data-tool API timed out); recheck for a March 2026 extract before the unmet-need study quotes under-detection figures. New-but-unused otherwise. |
| Fingertips | `xsec_ext_fingertips2425` (qof, dm_prev, cdr, conv, ref_rate, ca_em_rate/n), `fingertips_cancer_emergency_practice` | 2024/25, pulled 11–13 Jul 2026 | 2024/25 (annual; QOF-derived indicators cannot update before QOF 2025/26 on 27 Aug 2026) | **Yes** | None. Fingertips list-size remains banned as a denominator per the PROJECTS.md rule. |
| Prescribing (NHSBSA EPD) | xsec `abx_per1k`, `statins_per1k`, `items_per_pt` | single month **Mar 2025**, backfilled from the old master, not source-reproducible (XSEC_REBUILD_PROPOSAL §157) | EPD April 2026 (monthly, ~2-month lag) | **No** (13 months old and unreproducible) | Re-pull from the EPD API at rebuild. Two upstream changes to handle: SNOMED_CODE became a string field (11 May 2026) and from Apr 2026 the data reflect ICB mergers. Consider a 12-month window rather than a single month. |
| ODS epraccur | not in repo; xsec `closure_exposed`/`merger_recipient` backfilled from the old master | derivation not reproducible | epraccur is quarterly (a mid-2026 quarter is current) | **No** (source absent) | Pull epraccur at rebuild: it also supplies the practice-name source the §4.25 design principle requires (practices with no survey still render). |
| POMI | `pomi_online_services_practice` | Apr 2022 – Aug 2024 | collection **ended Aug 2024**; no successor open practice-level booking data | **Yes** (terminal) | None — archival. The PROJECTS.md correction stands: no open practice-level online-booking data after Aug 2024. |
| NHS App MI | `nhs_app_mi` | 2020–2026, pulled 13 Jul 2026 | ICB-level only | **Yes** | None; practice-level remains OKTA-gated. |
| FFT (GP) | `fft_gp_panel` | Jul 2022 – **May 2026** | May 2026 GP file (uploaded Jul 2026; the FFT landing page's "latest month = March 2026" banner lags its own file uploads — the Apr and May 2026 `.xlsm` files exist and are what `fetch_fft.py` ingested) | **Yes** | None. |

## 2. The workforce ×2 bug — verified live, and its blast radius

Re-verified from scratch: joining `xsec_master_2026` to `workforce_panel.parquet` (period 202503) on
practice code gives `gp_fte(xsec) / gp_fte(panel)` = 2.0000 for all 5,964 joinable practices (min
1.99999, max 2.00000). Spot value: A81001 xsec 7.41 vs panel 3.71. Cause as documented in
NOTES_BATCH_DRAFT §4.17 (companion numbering): the original build summed the workforce file's total
row and its component rows. (The brief cites "§4.17/§4.33"; no §4.33 exists in either notes file —
the second reference is dangling and should be corrected to the batch-draft §4.17.)

Where the doubled values do and do not matter:

- **Live pages: wrong numbers on screen.** `mypractice.html` and `explore.html` both read
  `xsec_master_2026` and display `gp_per10k` (and nurse/dpc per-10k). Every absolute staffing figure
  shown to the tool's ~26 users is 2× the true value. Not edited this session per the brief; this is
  the single highest-priority fix at the 30 Jul rebuild.
- **Standardised model coefficients: unaffected.** The predictors-page models report points per SD;
  uniform scaling leaves SD-standardised coefficients unchanged. The published §4.21–4.23 and §4.31
  coefficient tables do not need retraction. §4.31's composition variables come from
  `gp_composition_mar25.csv`, not the doubled xsec columns, so the partner/salaried/locum/trainee
  splits were never doubled.
- **Unstandardised uses: self-consistent but mislabeled.** `did_anima.py` and `f2f_increasers.py`
  include raw `gp_per10k` as a covariate; doubling a covariate halves only its own coefficient and
  leaves every other estimate, the propensity match, and the DiD effects unchanged. Conclusions
  stand; any quoted gp_per10k coefficient magnitude is half its true-scale value.
- **Cross-source comparisons: at risk.** Any figure that mixes xsec FTE with a correctly-scaled
  source (national FTE benchmarks, the composition file, §4.30's "GP FTE/10k rose 4.8→6.0" panel
  numbers) silently compares doubled with undoubled. The mypractice capacity card shows "GP mix vs
  the typical practice" — verify at rebuild which source each element reads.
- **`nurse_fte` has a second, separate defect:** the live master sourced it from a column that is
  empty at Mar 2025; the rebuilt cross-section uses the populated `nurses_fte` column (94.7%
  coverage). Carry that correction over.

Fix: use the corrected `workforce_panel` values (as `build_xsec_full.py` already does), never a
halving patch on the live file.

## 3. List-size denominators — one inconsistency to resolve

The four flavours (PROJECTS.md rule) are all present in the repo. Current usage:

- xsec `list_size` = 12-month average of the GPAD panel's monthly registered count (Apr 2024–Mar
  2025), and every xsec per-capita/per-10k metric (`gp_per10k`, `sd_percap`, `appts_percap`, etc.)
  divides by it. Internally consistent: no xsec metric was found dividing a count from one source by
  a denominator from another.
- The rule names NHSE "Patients Registered at a GP Practice" as canonical. The GPAD panel's monthly
  list is NHSE-derived and close, but it is not the canonical snapshot; the two differ by up to ~3%.
  At rebuild, either (a) re-derive per-10k metrics from the matching-month canonical registered
  list, or (b) document the GPAD-average as the deliberate xsec denominator and keep it uniform.
  Option (a) matches the written rule; whichever is chosen, `practice_age_sex.total_list` (Jul 2026
  snapshot) must not be mixed into 2024/25-window rates.
- `practice_weighted_list.registered_patients` (NHS Payments 2024/25) is correctly quarantined to
  the Carr-Hill ratio.

## 3a. IMD provenance — resolved: published-for-practice, not postcode-derived (added 13 Jul, follow-up)

Question (AMC): is `practice_imd.csv` the value published for the practice (registered-population
weighted) or an assignment from the practice's postcode LSOA? Answer: **published for the practice.**
Three tests, run 13 Jul 2026:

1. **Same-postcode test.** 677 pairs of practices share a postcode (payments-file postcodes); in 0 of
   677 pairs do the two practices share an IMD_2025 score. A postcode→LSOA assignment would give
   identical scores to every such pair, so that method is excluded.
2. **Source match.** Fingertips National General Practice Profiles carries "Deprivation score
   (IMD 2025)", indicator **94240** (GP-practice level, data source MHCLG, uploaded 25 Nov 2025 in
   the NGPP December 2025 update; successor to indicator 93553, which remains IMD 2019). A fetched
   sample of 308 practices from the Fingertips API matches `practice_imd.csv` to 2dp for 304/307
   overlapping practices, the other 3 differing by exactly 0.005 (rounding boundary): our file is
   the Fingertips value rounded to 2dp. NGPP derives this score by population-weighting LSOA-level
   IoD2025 scores across each practice's registered patients (NGPP user guide, v8.3, Dec 2025).
3. **Lineage.** Git history: the file was Fingertips indicator 93553 (IMD 2019, same
   registered-population method) until commit 26016b7 ("update with imd2025", 12 Apr 2026) replaced
   it; the new values correlate 0.97 with the old 93553 values across 6,127 practices, consistent
   with an index revision rather than a method change.

Caveats: the API comparison covers one parent area (307 practices), not all 6,148; and OHID states
there are no plans to update the NGPP profile again in its current form, so the refresh route for
future IMD revisions is uncertain. Fix-list item 9's "record the provenance" is discharged by this
section; the remaining housekeeping is the stale `README.md` line ("IMD 2019").

## 4. xsec_master_2026 vs xsec_master_rebuilt — recommendation

Switch the models to `xsec_master_rebuilt` at the 30 Jul rebuild, **after** its five remaining
backfilled columns are re-derived from source. Grounds (all re-checked against
XSEC_REBUILD_PROPOSAL): the rebuild reproduces 72/98 columns exactly (corr 1.0, mad 0), corrects the
workforce doubling and the nurse-FTE empty-column defect, and restores 126 practices the live master
dropped by building against a stale GPAD extract (all 6,007 live practices retained; the 33
non-recovered supplement rows fail inclusion legitimately). Outstanding before promotion:
`abx_per1k`, `statins_per1k`, `items_per_pt` (EPD pull — currently NULL for the 126 recovered
practices), `closure_exposed`, `merger_recipient` (epraccur derivation), and folding the external
merges into `build_xsec_full.py` so the whole table regenerates in one command. Re-running the
predictors models on the rebuilt table will shift n by ~2% and absolute staffing by ×0.5;
standardised coefficients should move little, which is itself a useful validation check.

## 5. Ordered fix list for the 30 July rebuild

1. **Workforce ×2** — rebuild on corrected `workforce_panel` values (and `nurses_fte`); regenerate
   every displayed staffing figure on mypractice/explore. Highest priority: wrong numbers are
   currently on public pages.
2. **Switch `build_xsec.py` to the parquet** (never the CSV) and adopt the rebuilt cross-section as
   base, survey-first with left joins (§4.25 design principle).
3. **Complete the rebuilt table's external columns from source**: EPD (Apr 2026, mind the SNOMED
   string change and ICB mergers), epraccur (closure flags + practice names), then promote
   `xsec_master_rebuilt` and re-run the predictors models.
4. **Refresh time-anchored inputs to the editions publishing that week**: GPAD June 2026 (30 Jul),
   CBT June 2026 (~23–30 Jul, first call-waiting times), workforce June 2026 (23 Jul), and re-extend
   `panel_oc` past Mar 2026 before re-running `did_anima.py` (its adopter flag is otherwise four
   months stale against a May-2026 merged panel).
5. **Vintage by purpose, not uniformly** (corrected 14 Jul; supersedes the original "re-run models on
   May 2026"). Two jobs need two vintages: (a) the *explanatory* composition/predictor models keep the
   pre-fieldwork vintage — Mar 2025 staffing precedes the Jan–Mar 2026 GPPS fieldwork, so it is a
   legitimate baseline predictor; re-vintaging them to May 2026 would place the predictor *after* the
   outcome and weaken them. (b) The *descriptive snapshot* surfaces (mypractice capacity card + factor
   section, explore) should show the latest census a practice would compare itself against — May 2026
   now, June 2026 once out (23 Jul). Done 14 Jul: mypractice's factor-section GP/10k was moved to the
   May 2026 composition snapshot (matching its capacity card); the models were deliberately left on
   Mar 2025.
6. **Settle the denominator**: adopt the canonical "Patients Registered" list for per-10k metrics or
   document the GPAD-average exception; audit mypractice's capacity card for mixed workforce sources.
7. **Integrate the new-but-unused sources** into the models they were pulled for: QOF 21-register
   prevalence and CVDPREVENT into the typology + unmet-need study; weighted list as the
   need-adjusted capacity denominator; age/sex structure as the demographic axis. Recheck for a
   CVDPREVENT March 2026 extract first.
8. **Diary the post-rebuild refreshes**: QOF 2025/26 on 27 Aug 2026 (prevalence file and every
   QOF-derived Fingertips indicator), and the GPPS 2027 wave next July.
9. **Housekeeping**: correct the dangling "§4.33" reference in the audit brief to batch-draft §4.17;
   IMD provenance now recorded (§3a: Fingertips NGPP indicator 94240, registered-population weighted);
   update the stale `README.md` description of `practice_imd.csv` from "IMD 2019" to IMD 2025 / 94240.

## 6. Verification notes (how "latest" was established)

Fetched 13 Jul 2026: NHSE Digital series pages for Appointments in General Practice (latest May
2026, June due 30 Jul), General Practice Workforce (latest 31 May 2026, June due 23 Jul), Patients
Registered at a GP Practice (July 2026 due 9 Jul, now out — repo holds the 1 Jul 2026 extract), QOF
2025/26 page (explicit "Publication Date: 27 Aug 2026, upcoming"), NHS England FFT data page (landing
page shows March 2026 but the Apr/May 2026 GP files exist at their upload URLs). Web-searched with
publication-page confirmation: GPPS 2026 (published 9 Jul 2026), NHS Payments 2024/25 (latest
annual), IoD/IMD 2025 (gov.uk, published 30 Oct 2025), NHSBSA EPD (April 2026 latest, monthly),
OC submissions (April 2026 page live; May 2026 values present in the merged panel). Not directly
verifiable: the CVDPREVENT quarterly extract schedule (site API timed out; inference from the annual
report cycle) — flagged in the table rather than asserted.

Local checks run this session: GPAD parquet vs regenerated CSV row/practice counts equal; workforce
ratio test (§2); xsec `imd_score` = `practice_imd.csv` IMD2025 for 6,007/6,007; xsec `dm_prev` =
QOF-2024/25 file exactly (corr 1.0); `panel_merged.oc_rate_1k` non-null through May 2026;
`fft_gp_panel` populated through May 2026 (6,180 practices, 902k responses in the May file).
