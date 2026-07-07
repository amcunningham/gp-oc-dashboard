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
  SUM(CASE WHEN TIME_BETWEEN_BOOK_AND_APPT='Same Day' THEN n ELSE 0 END) AS same_day,
  SUM(CASE WHEN TIME_BETWEEN_BOOK_AND_APPT='1 Day' THEN n ELSE 0 END) AS next_day,
  SUM(CASE WHEN TIME_BETWEEN_BOOK_AND_APPT LIKE 'Unknown%' THEN n ELSE 0 END) AS book_unknown,
  SUM(CASE WHEN HCP_TYPE='GP' THEN n ELSE 0 END) AS gp,
  SUM(CASE WHEN HCP_TYPE='GP' AND TIME_BETWEEN_BOOK_AND_APPT='Same Day' THEN n ELSE 0 END) AS gp_same_day,
  SUM(CASE WHEN APPT_MODE='Face-to-Face' THEN n ELSE 0 END) AS f2f,
  SUM(CASE WHEN APPT_MODE='Telephone' THEN n ELSE 0 END) AS phone,
  SUM(CASE WHEN APPT_MODE IN ('Online','Video/Online','Video Conference/Online') THEN n ELSE 0 END) AS online,
  SUM(CASE WHEN APPT_STATUS='DNA' THEN n ELSE 0 END) AS dna,
  SUM(CASE WHEN APPT_STATUS='Attended' THEN n ELSE 0 END) AS attended
FROM (
  SELECT APPOINTMENT_MONTH_START_DATE, GP_CODE, HCP_TYPE, APPT_MODE,
         TIME_BETWEEN_BOOK_AND_APPT, APPT_STATUS,
         TRY_CAST(COUNT_OF_APPOINTMENTS AS BIGINT) AS n
  FROM read_csv(FILELIST, header=true, all_varchar=true, union_by_name=true,
                quote='"', escape='"', strict_mode=false, ignore_errors=true)
  WHERE TRY_CAST(COUNT_OF_APPOINTMENTS AS BIGINT) IS NOT NULL
)
GROUP BY 1,2 ORDER BY 1,2
) TO 'OUTPATH' (HEADER, DELIMITER ',');
"""
sql = sql.replace("FILELIST", repr(files)).replace("OUTPATH", out)
con = duckdb.connect()
con.execute(sql)
n = con.execute("SELECT COUNT(*), COUNT(DISTINCT month) FROM read_csv_auto('" + out + "')").fetchone()
print(out, "rows:", n[0], "months:", n[1])
