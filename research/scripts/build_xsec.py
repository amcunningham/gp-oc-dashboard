import duckdb, pandas as pd
con = duckdb.connect()
con.execute("""
CREATE TABLE xsec AS
WITH sd AS (
  SELECT gp_code,
    SUM(same_day)*100.0/SUM(total) AS same_day_pct_12m,
    SUM(gp_same_day)*100.0/NULLIF(SUM(gp),0) AS gp_same_day_pct_12m,
    SUM(phone)*100.0/SUM(total) AS phone_pct_12m,
    SUM(f2f)*100.0/SUM(total) AS f2f_pct_12m,
    SUM(dna)*100.0/SUM(total) AS dna_pct_12m,
    AVG(oc_rate_1k) AS oc_rate_12m,
    AVG(list_size) AS list_size,
    MAX(imd_score) AS imd_score, MAX(imd_quintile) AS imd_quintile, MAX(region) AS region,
    SUM(total) AS appts_12m
  FROM read_csv_auto('panel_merged.csv')
  WHERE month BETWEEN '2024-04' AND '2025-03'
  GROUP BY 1 HAVING SUM(total) > 1000
),
merger AS (
  SELECT gp_code, MAX(jump) AS max_jump FROM (
    SELECT gp_code, list_size / NULLIF(LAG(list_size) OVER (PARTITION BY gp_code ORDER BY month),0) AS jump
    FROM read_csv_auto('panel_merged.csv') WHERE month BETWEEN '2023-04' AND '2025-03'
  ) GROUP BY 1
),
gpps AS (
  SELECT ad_practicecode AS gp_code,
    TRY_CAST("overallexp.pcteval" AS DOUBLE)*100 AS satisfaction,
    TRY_CAST("localgpservicesprefhpsee.pcteval" AS DOUBLE)*100 AS continuity,
    TRY_CAST("localgpservicesprefhp.pcteval" AS DOUBLE)*100 AS has_pref_hcp,
    TRY_CAST(received AS DOUBLE) AS gpps_n
  FROM read_csv('/tmp/gpps2025.csv', header=true, all_varchar=true)
),
wf AS (
  SELECT PRAC_CODE AS gp_code,
    SUM(CASE WHEN STAFF_GROUP='GP' AND MEASURE='FTE' THEN TRY_CAST(VALUE AS DOUBLE) ELSE 0 END) AS gp_fte,
    SUM(CASE WHEN STAFF_GROUP='Nurses' AND MEASURE='FTE' THEN TRY_CAST(VALUE AS DOUBLE) ELSE 0 END) AS nurse_fte,
    SUM(CASE WHEN STAFF_GROUP='Direct Patient Care' AND MEASURE='FTE' THEN TRY_CAST(VALUE AS DOUBLE) ELSE 0 END) AS dpc_fte,
    SUM(CASE WHEN STAFF_GROUP='Admin/Non-Clinical' AND MEASURE='FTE' THEN TRY_CAST(VALUE AS DOUBLE) ELSE 0 END) AS admin_fte
  FROM read_csv('/tmp/gpw/3 General Practice – March 2025 Practice Level - High level.csv', header=true, all_varchar=true)
  GROUP BY 1
),
pay AS (
  SELECT "Practice Code" AS gp_code, "Practice Rurality" AS rurality, "Dispensing Practice" AS dispensing
  FROM read_csv('/tmp/payments.csv', header=true, all_varchar=true)
)
SELECT sd.*, merger.max_jump, gpps.satisfaction, gpps.continuity, gpps.has_pref_hcp, gpps.gpps_n,
       wf.gp_fte, wf.nurse_fte, wf.dpc_fte, wf.admin_fte, pay.rurality, pay.dispensing
FROM sd LEFT JOIN merger USING (gp_code) LEFT JOIN gpps USING (gp_code)
LEFT JOIN wf USING (gp_code) LEFT JOIN pay USING (gp_code);
""")
con.execute("COPY xsec TO 'xsec_2025.csv' (HEADER)")
r = con.execute("""SELECT COUNT(*), COUNT(satisfaction), COUNT(continuity), COUNT(gp_fte), COUNT(rurality) FROM xsec""").fetchone()
print("practices:", r[0], "| with GPPS sat:", r[1], "| continuity:", r[2], "| workforce:", r[3], "| rurality:", r[4])
print(con.execute("SELECT rurality, COUNT(*) FROM xsec GROUP BY 1").fetchall())
