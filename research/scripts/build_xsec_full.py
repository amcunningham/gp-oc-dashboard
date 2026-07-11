#!/usr/bin/env python3
"""
build_xsec_full.py -- reproducible rebuild of the English GP practice cross-section
(xsec_master_2026 schema) from the CURRENT corrected sources in this repo.

WHY: the live research/data/xsec_master_2026.{csv,parquet} (6,007 practices, 98 cols)
was assembled by an earlier session against an EARLIER GPAD extract. ~126-134 real
practices that meet every inclusion rule against the CORRECTED panel_merged.parquet
were dropped (e.g. A82071, 27,170 appts 2024/25). This script re-derives the
cross-section from panel_merged.parquet + the raw GPPS 2024/25/26 files + workforce
so those practices are included.

INCLUSION RULE (documented): keyed on gp_code; >1000 GPAD appts Apr2024-Mar2025 in the
current panel_merged, has an IMD score, and appears in GPPS 2025.

OUTPUT: research/data/xsec_master_rebuilt.csv  (NEW filename -- never overwrites masters)

Columns fall in three tiers, matching the 98-col xsec_master_2026 schema:
  * REPRODUCED  -- re-derived from repo sources (GPAD panel, waits panel, GPPS files, workforce)
  * BACKFILLED  -- copied from an existing repo lookup (geography from adoption_risk_2027.csv)
  * NULL        -- upstream source (NHS Payments, Fingertips API, NHSBSA EPD API, epraccur
                   closures, workforce age bands) is NOT in the repo; left NULL by design.
See research/XSEC_REBUILD_PROPOSAL.md for the full provenance table.
"""
import os, duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
RAW  = os.path.normpath(os.path.join(HERE, "..", "..", "data"))
PM   = os.path.join(DATA, "panel_merged.parquet")
WAITS= os.path.join(DATA, "waits_panel.parquet")
WF   = os.path.join(DATA, "workforce_panel.parquet")
GEO  = os.path.join(DATA, "adoption_risk_2027.csv")
G24  = os.path.join(RAW, "GPPS_2024_Practice_data_(weighted)_(csv)_PUBLIC.csv")
G25  = os.path.join(RAW, "GPPS_2025_Practice_data_(weighted)_(csv)_PUBLIC.csv")
G26  = os.path.join(RAW, "GPPS_2026_Practice_data_(weighted)_(csv)_PUBLIC.csv")
OUT  = os.path.join(DATA, "xsec_master_rebuilt.csv")

con = duckdb.connect()

def pe(col, x100=True):
    """clean a GPPS .pcteval / .pct value (sentinel <0 -> NULL), optionally *100"""
    b = f'TRY_CAST("{col}" AS DOUBLE)'
    s = f"CASE WHEN {b} < 0 THEN NULL ELSE {b} END"
    return f"({s})*100" if x100 else s

# ---------------------------------------------------------------- 1. GPAD panel (12m Apr24-Mar25)
con.execute(f"""
CREATE TABLE sd AS
SELECT gp_code,
  SUM(same_day)*100.0/SUM(total)                         AS same_day_pct_12m,
  SUM(gp_same_day)*100.0/NULLIF(SUM(gp),0)               AS gp_same_day_pct_12m,
  SUM(phone)*100.0/SUM(total)                            AS phone_pct_12m,
  SUM(f2f)*100.0/SUM(total)                              AS f2f_pct_12m,
  SUM(dna)*100.0/SUM(total)                              AS dna_pct_12m,
  AVG(oc_rate_1k)                                        AS oc_rate_12m,
  AVG(list_size)                                         AS list_size,
  MAX(imd_score)                                         AS imd_score,
  MAX(imd_quintile)                                      AS imd_quintile,
  MAX(region)                                            AS region,
  SUM(total)                                             AS appts_12m,
  SUM(gp)*100.0/SUM(total)                               AS gp_share,
  SUM(gp_same_day)*100.0/NULLIF(SUM(gp),0)               AS gp_sd,
  (SUM(same_day)-SUM(gp_same_day))*100.0/NULLIF(SUM(total)-SUM(gp),0) AS oth_sd,
  SUM(same_day)*100.0/SUM(total)                          AS sd_share,
  SUM(same_day)*1000.0/12/NULLIF(AVG(list_size),0)        AS sd_percap,
  SUM(total)*1000.0/12/NULLIF(AVG(list_size),0)           AS appts_percap
FROM read_parquet('{PM}')
WHERE month BETWEEN '2024-04' AND '2025-03'
GROUP BY 1 HAVING SUM(total) > 1000
""")

# prior-year same-day share (Apr23-Mar24)
con.execute(f"""
CREATE TABLE prior AS
SELECT gp_code, SUM(same_day)*100.0/NULLIF(SUM(total),0) AS sd_share_prior_year
FROM read_parquet('{PM}') WHERE month BETWEEN '2023-04' AND '2024-03' GROUP BY 1
""")

# merger proxy: max month-on-month list-size jump Apr23-Mar25
con.execute(f"""
CREATE TABLE merger AS
SELECT gp_code, MAX(jump) AS max_jump FROM (
  SELECT gp_code, list_size/NULLIF(LAG(list_size) OVER (PARTITION BY gp_code ORDER BY month),0) AS jump
  FROM read_parquet('{PM}') WHERE month BETWEEN '2023-04' AND '2025-03'
) GROUP BY 1
""")

# ---------------------------------------------------------------- 2. Wait bands (12m Apr24-Mar25)
con.execute(f"""
CREATE TABLE wb AS
SELECT gp_code,
  SUM(same_day)*100.0/NULLIF(SUM(total),0)                        AS sd_pct,
  (SUM(d1)+SUM(d2_7))*100.0/NULLIF(SUM(total),0)                  AS d1_7_pct,
  SUM(d8_14)*100.0/NULLIF(SUM(total),0)                           AS d8_14_pct,
  (SUM(d15_21)+SUM(d22_28)+SUM(d28plus))*100.0/NULLIF(SUM(total),0) AS d15plus_pct,
  SUM(gp_d15plus)*100.0/NULLIF(SUM(gp),0)                         AS gp_d15plus_pct,
  SUM(gp_d15plus)*100.0/NULLIF(SUM(gp),0)                         AS gp_15p,
  (SUM(d15_21)+SUM(d22_28)+SUM(d28plus)-SUM(gp_d15plus))*100.0/NULLIF(SUM(total)-SUM(gp),0) AS oth_15p
FROM read_parquet('{WAITS}')
WHERE month BETWEEN '2024-04' AND '2025-03'
GROUP BY 1
""")

# ---------------------------------------------------------------- 3. GPPS 2025 (base wave)
con.execute(f"""
CREATE TABLE g25 AS
SELECT ad_practicecode AS gp_code,
  {pe('overallexp.pcteval')}              AS satisfaction,
  {pe('localgpservicesprefhpsee.pcteval')} AS continuity,
  {pe('localgpservicesprefhp.pcteval')}   AS has_pref_hcp,
  TRY_CAST(received AS DOUBLE)            AS gpps_n,
  {pe('gpcontactoverall.pcteval')}        AS access_satisfaction,
  {pe('localgpservicesphone.pcteval')}    AS phone_easy,
  {pe('localgpserviceswebsite.pcteval')}  AS website_easy,
  {pe('localgpservicesapp.pcteval')}      AS app_easy,
  100 - {pe('dv_ethnicityband_1.pct')}    AS nonwhite_pct,
  {pe('lastgpapptwhen_1.pct')}            AS pt_same_day,
  {pe('lastgpapptwait_2.pct')}            AS wait_too_long,
  {pe('gpcontactnextsteptiming_1.pct')}   AS nextstep_immediate,
  {pe('gpcontactnextstep_3.pct')}         AS deflection_2025,
  {pe('gpcontactnextstep_4.pct')}         AS couldnt_contact_2025,
  {pe('overallexp.baseevalw', False)}     AS satisfaction_basew,
  {pe('localgpservicesprefhpsee.baseevalw', False)} AS continuity_basew,
  {pe('gpcontactoverall.baseevalw', False)}          AS access_basew,
  {pe('localgpservicesphone.baseevalw', False)}      AS phone_basew
FROM read_csv('{G25}', header=true, all_varchar=true)
WHERE ad_practicecode IS NOT NULL
""")

# ---------------------------------------------------------------- 4. GPPS 2024 (prior wave)
con.execute(f"""
CREATE TABLE g24 AS
SELECT ad_practicecode AS gp_code,
  {pe('overallexp.pcteval')}               AS satisfaction_2024,
  {pe('localgpservicesprefhpsee.pcteval')} AS continuity_2024
FROM read_csv('{G24}', header=true, all_varchar=true)
WHERE ad_practicecode IS NOT NULL
""")

# ---------------------------------------------------------------- 5. GPPS 2026 (new wave)
con.execute(f"""
CREATE TABLE g26 AS
SELECT ad_practicecode AS gp_code,
  {pe('overallexp.pcteval')}               AS satisfaction_2026,
  {pe('localgpservicesprefhpsee.pcteval')} AS continuity_2026,
  {pe('localgpservicesprefhp.pcteval')}    AS has_pref_hcp_2026,
  {pe('gpcontactoverall.pcteval')}         AS access_satisfaction_2026,
  {pe('localgpservicesphone.pcteval')}     AS phone_easy_2026,
  {pe('lastgpapptwhen_1.pct')}             AS pt_same_day_2026,
  {pe('gpcontactnextstep_3.pct')}          AS deflection_2026,
  {pe('gpcontactnextstep_4.pct')}          AS couldnt_contact_2026,
  {pe('gpcontactnextsteptiming_1.pct')}    AS nextstep_immediate_2026,
  {pe('lastgpapptwait_2.pct')}             AS wait_too_long_2026,
  TRY_CAST(received AS DOUBLE)             AS gpps_n_2026,
  {pe('localgpserviceswebsite.pcteval')}   AS website_easy_2026,
  {pe('localgpservicesapp.pcteval')}       AS app_easy_2026
FROM read_csv('{G26}', header=true, all_varchar=true)
WHERE ad_practicecode IS NOT NULL
""")

# ---------------------------------------------------------------- 6. Workforce (March 2025 = 202503)
con.execute(f"""
CREATE TABLE wf AS
SELECT prac AS gp_code,
  MAX(gp_fte) AS gp_fte, MAX(nurses_fte) AS nurse_fte,
  MAX(dpc_fte) AS dpc_fte, MAX(admin_fte) AS admin_fte
FROM read_parquet('{WF}') WHERE period = 202503 GROUP BY 1
""")

# ---------------------------------------------------------------- 7. Geography backfill (repo lookup)
con.execute(f"""
CREATE TABLE geo AS
SELECT gp_code, ANY_VALUE(gp_name) AS gp_name, ANY_VALUE(postcode) AS postcode,
       ANY_VALUE(icb_name) AS icb_name
FROM read_csv_auto('{GEO}') GROUP BY 1
""")

# ---------------------------------------------------------------- 8. Assemble, inclusion filter
con.execute("""
CREATE TABLE x AS
SELECT sd.*, prior.sd_share_prior_year, merger.max_jump,
       wb.sd_pct, wb.d1_7_pct, wb.d8_14_pct, wb.d15plus_pct, wb.gp_d15plus_pct, wb.gp_15p, wb.oth_15p,
       g25.satisfaction, g25.continuity, g25.has_pref_hcp, g25.gpps_n,
       g25.access_satisfaction, g25.phone_easy, g25.website_easy, g25.app_easy,
       g25.nonwhite_pct, g25.pt_same_day, g25.wait_too_long, g25.nextstep_immediate,
       g25.deflection_2025, g25.couldnt_contact_2025,
       g25.satisfaction_basew, g25.continuity_basew, g25.access_basew, g25.phone_basew,
       g24.satisfaction_2024, g24.continuity_2024,
       g26.satisfaction_2026, g26.continuity_2026, g26.has_pref_hcp_2026,
       g26.access_satisfaction_2026, g26.phone_easy_2026, g26.pt_same_day_2026,
       g26.deflection_2026, g26.couldnt_contact_2026, g26.nextstep_immediate_2026,
       g26.wait_too_long_2026, g26.gpps_n_2026, g26.website_easy_2026, g26.app_easy_2026,
       wf.gp_fte, wf.nurse_fte, wf.dpc_fte, wf.admin_fte,
       geo.gp_name, geo.postcode, geo.icb_name
FROM sd
LEFT JOIN prior  USING (gp_code)
LEFT JOIN merger USING (gp_code)
LEFT JOIN wb     USING (gp_code)
JOIN      g25    USING (gp_code)          -- inclusion: must be in GPPS 2025
LEFT JOIN g24    USING (gp_code)
LEFT JOIN g26    USING (gp_code)
LEFT JOIN wf     USING (gp_code)
LEFT JOIN geo    USING (gp_code)
WHERE sd.imd_score IS NOT NULL            -- inclusion: must have IMD
""")

# ---------------------------------------------------------------- 9. Derived columns
con.execute("""
CREATE TABLE xf AS
SELECT *,
  LN(list_size)                       AS log_list,
  10000*gp_fte/NULLIF(list_size,0)    AS gp_per10k,
  10000*nurse_fte/NULLIF(list_size,0) AS nurse_per10k,
  10000*dpc_fte/NULLIF(list_size,0)   AS dpc_per10k,
  10000*admin_fte/NULLIF(list_size,0) AS admin_per10k,
  CASE WHEN max_jump > 1.15 THEN 1.0 ELSE 0.0 END AS merged_recent,
  NTILE(4) OVER (ORDER BY list_size)  AS size_q,
  CASE WHEN gp_sd >= 80 THEN 1.0 ELSE 0.0 END AS high80,
  -- columns whose upstream source is NOT in the repo -> NULL by design
  CAST(NULL AS VARCHAR) AS rurality, CAST(NULL AS VARCHAR) AS dispensing,
  CAST(NULL AS DOUBLE)  AS rural,     CAST(NULL AS DOUBLE)  AS dispensing_f,
  CAST(NULL AS DOUBLE)  AS closure_exposed, CAST(NULL AS DOUBLE) AS merger_recipient,
  CAST(NULL AS DOUBLE)  AS qof, CAST(NULL AS DOUBLE) AS ca_em_rate, CAST(NULL AS DOUBLE) AS ca_em_n,
  CAST(NULL AS DOUBLE)  AS pct65plus, CAST(NULL AS DOUBLE) AS ae_after_fail, CAST(NULL AS DOUBLE) AS ae_pop,
  CAST(NULL AS DOUBLE)  AS phone_failed, CAST(NULL AS DOUBLE) AS contact_fail, CAST(NULL AS DOUBLE) AS dm_prev, CAST(NULL AS DOUBLE) AS abx_per1k,
  CAST(NULL AS DOUBLE)  AS items_per_pt, CAST(NULL AS DOUBLE) AS statins_per1k,
  CAST(NULL AS DOUBLE)  AS cdr, CAST(NULL AS DOUBLE) AS conv, CAST(NULL AS DOUBLE) AS ref_rate,
  CAST(NULL AS VARCHAR) AS pcn_name, CAST(NULL AS VARCHAR) AS sub_icb_name
FROM x
""")

# ---------------------------------------------------------------- 10. Emit in xsec_master_2026 order
ORDER = ['gp_code','same_day_pct_12m','gp_same_day_pct_12m','phone_pct_12m','f2f_pct_12m','dna_pct_12m',
 'oc_rate_12m','list_size','imd_score','imd_quintile','region','appts_12m','max_jump','satisfaction',
 'continuity','has_pref_hcp','gpps_n','gp_fte','nurse_fte','dpc_fte','admin_fte','rurality','dispensing',
 'rural','dispensing_f','log_list','gp_per10k','nurse_per10k','dpc_per10k','admin_per10k','merged_recent',
 'size_q','closure_exposed','merger_recipient','nonwhite_pct','gp_sd','oth_sd','gp_15p','oth_15p','gp_share',
 'sd_pct','d1_7_pct','d8_14_pct','d15plus_pct','gp_d15plus_pct','qof','high80','ca_em_rate','ca_em_n',
 'pct65plus','pt_same_day','sd_share','sd_percap','appts_percap','ae_after_fail','ae_pop','contact_fail',
 'phone_failed','nextstep_immediate','wait_too_long','dm_prev','abx_per1k','items_per_pt','gp_name',
 'pcn_name','sub_icb_name','icb_name','postcode','cdr','conv','ref_rate','satisfaction_2024',
 'continuity_2024','sd_share_prior_year','statins_per1k','access_satisfaction','phone_easy',
 'satisfaction_2026','continuity_2026','has_pref_hcp_2026','access_satisfaction_2026','phone_easy_2026',
 'pt_same_day_2026','deflection_2026','couldnt_contact_2026','nextstep_immediate_2026','wait_too_long_2026',
 'gpps_n_2026','satisfaction_basew','continuity_basew','access_basew','phone_basew','deflection_2025',
 'couldnt_contact_2025','website_easy','app_easy','website_easy_2026','app_easy_2026']

con.execute(f"COPY (SELECT {', '.join(ORDER)} FROM xf ORDER BY gp_code) TO '{OUT}' (HEADER)")

n, ns, nc = con.execute("SELECT COUNT(*), COUNT(satisfaction_2026), COUNT(gp_fte) FROM xf").fetchone()
print(f"[done] {OUT}")
print(f"       practices: {n} | with satisfaction_2026: {ns} | with workforce gp_fte: {nc}")
a82 = con.execute("SELECT COUNT(*) FROM xf WHERE gp_code='A82071'").fetchone()[0]
print(f"       A82071 present: {a82}")
