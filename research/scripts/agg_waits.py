import duckdb, sys, glob
out = sys.argv[1]
files = glob.glob(sys.argv[2])
assert files, "no files"
sql = """
COPY (
SELECT
  strftime(strptime(APPOINTMENT_MONTH_START_DATE, '%d%b%Y'), '%Y-%m') AS month,
  GP_CODE AS gp_code,
  SUM(n) AS total,
  SUM(CASE WHEN tb='Same Day' THEN n ELSE 0 END) AS same_day,
  SUM(CASE WHEN tb='1 Day' THEN n ELSE 0 END) AS d1,
  SUM(CASE WHEN tb LIKE '2%to 7%' THEN n ELSE 0 END) AS d2_7,
  SUM(CASE WHEN tb LIKE '8%to 14%' THEN n ELSE 0 END) AS d8_14,
  SUM(CASE WHEN tb LIKE '15%to 21%' THEN n ELSE 0 END) AS d15_21,
  SUM(CASE WHEN tb LIKE '22%to 28%' THEN n ELSE 0 END) AS d22_28,
  SUM(CASE WHEN tb='More than 28 Days' THEN n ELSE 0 END) AS d28plus,
  SUM(CASE WHEN tb LIKE 'Unknown%' THEN n ELSE 0 END) AS unk,
  SUM(CASE WHEN hcp='GP' THEN n ELSE 0 END) AS gp,
  SUM(CASE WHEN hcp='GP' AND tb LIKE '8%to 14%' THEN n ELSE 0 END) AS gp_d8_14,
  SUM(CASE WHEN hcp='GP' AND (tb LIKE '15%to 21%' OR tb LIKE '22%to 28%' OR tb='More than 28 Days') THEN n ELSE 0 END) AS gp_d15plus
FROM (
  SELECT APPOINTMENT_MONTH_START_DATE, GP_CODE, HCP_TYPE AS hcp,
         TIME_BETWEEN_BOOK_AND_APPT AS tb,
         TRY_CAST(COUNT_OF_APPOINTMENTS AS BIGINT) AS n
  FROM read_csv(FILELIST, header=true, all_varchar=true, union_by_name=true,
                quote='"', escape='"', strict_mode=false, ignore_errors=true)
  WHERE TRY_CAST(COUNT_OF_APPOINTMENTS AS BIGINT) IS NOT NULL
)
GROUP BY 1,2 ORDER BY 1,2
) TO 'OUTPATH' (HEADER, DELIMITER ',');
"""
sql = sql.replace("FILELIST", repr(files)).replace("OUTPATH", out)
duckdb.connect().execute(sql)
import subprocess
print(out, "done")
