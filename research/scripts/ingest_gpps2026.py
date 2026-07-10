#!/usr/bin/env python3
"""
ingest_gpps2026.py  -- one-command ingest of the GPPS 2026 practice-level file.

Pipeline:  download/locate -> integrity (changelog) check -> sentinel clean
           -> extract our question set -> merge into xsec -> 3-wave change file.

Fieldwork Jan-Mar 2026, published ~9 Jul 2026 (gp-patient.co.uk). The practice-level
weighted CSV carries precomputed `<stem>.pcteval` (headline positive score, as a
fraction) and `<stem>_N.pct` (category-N share, fraction). See GPPS_2025_questions.md
for the full stem list and PANEL_NOTES.md sec. "Cross-sectional models" / "SESSION 3"
for the derived-column definitions this reproduces for the 2026 wave.

USAGE
  # once the file has dropped (download it from gp-patient.co.uk first):
  python3 ingest_gpps2026.py /path/to/GPPS_2026_Practice_weighted.csv
  # or pass a direct URL (script downloads it):
  python3 ingest_gpps2026.py "https://.../gpps_2026_practice.csv"
  # or drop the file anywhere under ~/Downloads and just run:
  python3 ingest_gpps2026.py            # auto-finds the newest matching CSV

Non-destructive: writes xsec_master_2026.{csv,parquet} and wave3_gpps.csv into
research/data/. Never overwrites xsec_master.*.

CAUTION (per PANEL_NOTES / AMC): a 2025->2026 comparison is only valid if the
questionnaire is unchanged. The integrity check below aborts the merge if any stem we
rely on (esp. Q32 overallexp, Q7 prefhpsee, Q12 gpcontactnextstep) is missing or renamed.
"""

import sys, os, glob, urllib.request, tempfile
import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
XSEC = os.path.join(DATA, "xsec_master.csv")          # 2025-wave master (read)
OUT_XSEC = os.path.join(DATA, "xsec_master_2026")      # written (.csv/.parquet)
OUT_WAVE3 = os.path.join(DATA, "wave3_gpps.csv")       # written

# ---------------------------------------------------------------------------
# Our question set: output column  ->  (source stem+suffix, needs_x100)
# pcteval / .pct fields are fractions in the source file, so *100 to match the
# existing xsec columns (which are stored as percentages). `received` is a raw count.
# ---------------------------------------------------------------------------
QSET = {
    # headline positive scores (.pcteval)
    "satisfaction_2026":        ("overallexp.pcteval",            True),   # Q32
    "continuity_2026":          ("localgpservicesprefhpsee.pcteval", True),# Q7
    "has_pref_hcp_2026":        ("localgpservicesprefhp.pcteval",  True),  # Q6
    "access_satisfaction_2026": ("gpcontactoverall.pcteval",       True),  # Q16
    "phone_easy_2026":          ("localgpservicesphone.pcteval",   True),  # Q1
    # category shares (_N.pct) -- N is 1-based position in the questionnaire options
    "pt_same_day_2026":         ("lastgpapptwhen_1.pct",           True),  # Q20 same day
    "deflection_2026":          ("gpcontactnextstep_3.pct",        True),  # Q12 "contact again another day"
    "couldnt_contact_2026":     ("gpcontactnextstep_4.pct",        True),  # Q12 "couldn't contact"
    "nextstep_immediate_2026":  ("gpcontactnextsteptiming_1.pct",  True),  # Q13 "there and then"
    "wait_too_long_2026":       ("lastgpapptwait_2.pct",           True),  # Q21 "took too long"
    # sample size
    "gpps_n_2026":              ("received",                       False),
}
KEY_STEM = "ad_practicecode"   # GPPS practice identifier -> joins to xsec.gp_code
# Stems whose disappearance/rename kills a 2025->2026 comparison outright:
CRITICAL = ["overallexp.pcteval", "localgpservicesprefhpsee.pcteval",
            "gpcontactnextstep_3.pct", KEY_STEM]


def locate_input(argv):
    """Return a local path to the GPPS 2026 CSV (download URL / use arg / auto-find)."""
    if len(argv) > 1:
        arg = argv[1]
        if arg.startswith("http://") or arg.startswith("https://"):
            dst = os.path.join(tempfile.gettempdir(), "gpps2026_download.csv")
            print(f"[download] {arg}\n           -> {dst}")
            urllib.request.urlretrieve(arg, dst)
            return dst
        if not os.path.exists(arg):
            sys.exit(f"[fatal] file not found: {arg}")
        return arg
    # auto-find newest CSV in ~/Downloads that looks like the practice file
    downloads = os.path.expanduser("~/Downloads")
    cands = []
    for pat in ("*[gG][pP][pP][sS]*2026*.csv", "*GPPS*Practice*.csv", "*2026*ractice*.csv"):
        cands += glob.glob(os.path.join(downloads, pat))
    if not cands:
        sys.exit("[fatal] no file given and none auto-found in ~/Downloads.\n"
                 "        Pass the path or URL:  python3 ingest_gpps2026.py <path|url>")
    newest = max(cands, key=os.path.getmtime)
    print(f"[auto] using newest match in Downloads: {newest}")
    return newest


def integrity_check(present_cols):
    """Verify every required stem exists. Returns list of missing (empty == OK)."""
    required = [KEY_STEM] + [src for src, _ in QSET.values()]
    present = set(present_cols)
    missing = [c for c in required if c not in present]
    print("\n=== QUESTIONNAIRE-INTEGRITY (CHANGELOG) CHECK ===")
    for col in required:
        flag = "OK " if col in present else "MISSING"
        crit = "  <-- CRITICAL" if (col in CRITICAL and col not in present) else ""
        print(f"  [{flag}] {col}{crit}")
    if missing:
        print("\n[!] Missing/renamed columns above. GPPS may have re-worded items for 2026.")
        print("    Inspect the 2026 questionnaire changelog before trusting any 2025->2026")
        print("    comparison, then update QSET stems in this script to match.")
    else:
        print("\n[ok] All required stems present -- questionnaire stable vs 2025.")
    return missing


def clean(expr, x100):
    """Sentinel-safe cast: non-numeric -> NULL; GPPS negatives (e.g. -97) -> NULL."""
    base = f'TRY_CAST("{expr}" AS DOUBLE)'
    safe = f"CASE WHEN {base} < 0 THEN NULL ELSE {base} END"
    return f"({safe})*100" if x100 else safe


# Headline items to report as a respondent-weighted England figure (official convention).
HEADLINE = {
    "overallexp":               "overall experience",
    "localgpservicesphone":     "phone easy",
    "localgpserviceswebsite":   "website easy",
    "localgpservicesapp":       "NHS App easy",
    "localgpservicesprefhpsee": "continuity (see preferred)",
    "localgpservicesprefhp":    "has preferred HCP",
}


def national_figure(con, stem):
    """Respondent-weighted England headline for a GPPS item.

    Weights each practice's positive % (`.pcteval`) by its survey-weighted evaluative
    base (`.baseevalw`) -- i.e. each PATIENT counts equally, matching the official GPPS
    national figure. A plain mean across practices ("practice-mean") counts each PRACTICE
    equally and runs high on access items, where small practices score better.
    Returns (national_weighted_pct, practice_mean_pct).
    """
    pe, be = f'"{stem}.pcteval"', f'"{stem}.baseevalw"'
    q = f"""
      SELECT SUM(v*w)/NULLIF(SUM(w),0)*100 AS natw, AVG(v)*100 AS pmean
      FROM (SELECT TRY_CAST({pe} AS DOUBLE) v, TRY_CAST({be} AS DOUBLE) w FROM raw)
      WHERE v >= 0 AND w > 0
    """
    return con.execute(q).fetchone()


def main():
    src = locate_input(sys.argv)
    con = duckdb.connect()

    # load raw as varchar so suppression markers ('*', '.', etc.) don't break the read
    con.execute(f"CREATE TABLE raw AS SELECT * FROM read_csv('{src}', header=true, all_varchar=true)")
    present_cols = [r[1] for r in con.execute("PRAGMA table_info('raw')").fetchall()]
    print(f"[load] {src}\n       {con.execute('SELECT COUNT(*) FROM raw').fetchone()[0]} rows, "
          f"{len(present_cols)} columns")

    missing = integrity_check(present_cols)
    if any(c in CRITICAL for c in missing):
        sys.exit("\n[abort] a CRITICAL stem is missing -- refusing to merge. Fix QSET, re-run.")

    # build the extracted 2026 table (skip any non-critical missing cols gracefully)
    selects = [f'"{KEY_STEM}" AS gp_code']
    for out, (src_col, x100) in QSET.items():
        if src_col in present_cols:
            selects.append(f"{clean(src_col, x100)} AS {out}")
        else:
            selects.append(f"CAST(NULL AS DOUBLE) AS {out}   -- {src_col} absent")
    con.execute(f"CREATE TABLE g26 AS SELECT {', '.join(selects)} FROM raw WHERE {KEY_STEM} IS NOT NULL")

    n = con.execute("SELECT COUNT(*) FROM g26").fetchone()[0]
    print(f"\n[extract] {n} practices. Non-null coverage:")
    for out in QSET:
        c = con.execute(f"SELECT COUNT({out}) FROM g26").fetchone()[0]
        mean = con.execute(f"SELECT ROUND(AVG({out}),2) FROM g26").fetchone()[0]
        print(f"    {out:26s} n={c:<6d} mean={mean}")

    # respondent-weighted England headlines (official convention) vs the practice-mean.
    # Quote the 'national' column publicly; the practice-mean is QC only and runs high.
    print("\n[national headline] respondent-weighted (each patient counts equally):")
    for stem, label in HEADLINE.items():
        if f"{stem}.pcteval" in present_cols and f"{stem}.baseevalw" in present_cols:
            natw, pmean = national_figure(con, stem)
            if natw is not None:
                print(f"    {label:28s} national={natw:5.1f}   (practice-mean={pmean:4.1f})")

    # merge onto the 2025 master (non-destructive; adds *_2026 cols)
    con.execute(f"CREATE TABLE xsec AS SELECT * FROM read_csv_auto('{XSEC}')")
    con.execute("CREATE TABLE merged AS SELECT xsec.*, "
                + ", ".join(f"g26.{c}"                            for c in list(QSET.keys()))
                + " FROM xsec LEFT JOIN g26 USING (gp_code)")
    con.execute(f"COPY merged TO '{OUT_XSEC}.csv' (HEADER)")
    con.execute(f"COPY merged TO '{OUT_XSEC}.parquet' (FORMAT parquet)")
    matched = con.execute("SELECT COUNT(gpps_n_2026) FROM merged").fetchone()[0]
    with_sat = con.execute("SELECT COUNT(satisfaction_2026) FROM merged").fetchone()[0]
    total = con.execute("SELECT COUNT(*) FROM merged").fetchone()[0]
    print(f"\n[merge] {matched}/{total} xsec practices matched a 2026 GPPS row "
          f"({with_sat} with a non-suppressed satisfaction score).")
    print(f"        -> {OUT_XSEC}.csv / .parquet")

    con.execute(f"""
        COPY (
          SELECT gp_code,
                 satisfaction_2024 AS sat_24, continuity_2024 AS cont_24,
                 satisfaction      AS sat_25, continuity      AS cont_25,
                 satisfaction_2026 AS sat_26, continuity_2026 AS cont_26,
                 (satisfaction_2026 - satisfaction)      AS d_sat_25_26,
                 (continuity_2026   - continuity)        AS d_cont_25_26,
                 gpps_n AS n_25, gpps_n_2026 AS n_26,
                 deflection_2026, access_satisfaction_2026, pt_same_day_2026,
                 imd_score, rural, region
          FROM merged
        ) TO '{OUT_WAVE3}' (HEADER)
    """)
    print(f"[wave3] 3-wave satisfaction/continuity panel -> {OUT_WAVE3}")


if __name__ == "__main__":
    main()
 (HEADER)
    """)
    print(f"[wave3] 3-wave satisfaction/continuity panel -> {OUT_WAVE3}")

    print("\n[done] Next: run the pre-registered four on xsec_master_2026 "
           "(Anima/Continuum DiD, admin-only cohort deltas, Wealden Ridge 2026, refresh machinery).")


if __name__ == "__main__":
    main()
