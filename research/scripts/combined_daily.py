#!/usr/bin/env python3
"""
Combined daily analysis: telephone + online consultation as one demand series.

Run once the OC "Day and Time" file is available:

    python combined_daily.py --oc research/data/oc_daytime_jun26.zip \
                             --cbt research/data/cbt_jun26 \
                             --list research/data/list_jul26.csv \
                             --out research/data/combined

Step 1 inspects the OC file and reports whether it carries calendar dates or only day-of-week.
That determines which analysis runs, and the script says which one it chose. Column names are
detected rather than assumed, and the detection is printed so it can be checked.

Outputs, per practice and per list-size band:
  contact attempted = calls made + forms submitted
  contact received  = calls answered + forms submitted
  residual variability of each, about the practice's own day-of-week means
"""
import argparse, glob, io, os, re, sys, zipfile
import numpy as np
import pandas as pd

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
BANDS = [0, 6000, 12000, 30000, 1e9]
LABELS = ["<6k", "6-12k", "12-30k", "30k+"]
Z = 1.645


# ---------------------------------------------------------------- file loading
def read_any(path, pattern="*.csv", nrows=None):
    """Read csv(s) from a file, a zip, or a directory. Returns a concatenated frame."""
    frames = []
    if os.path.isdir(path):
        targets = sorted(glob.glob(os.path.join(path, "**", pattern), recursive=True))
        targets += sorted(glob.glob(os.path.join(path, "**", "*.zip"), recursive=True))
    else:
        targets = [path]
    for t in targets:
        if t.lower().endswith(".zip"):
            with zipfile.ZipFile(t) as z:
                for n in z.namelist():
                    if not n.lower().endswith(".csv") or "unmapped" in n.lower():
                        continue
                    with z.open(n) as h:
                        frames.append(pd.read_csv(io.BytesIO(h.read()), nrows=nrows, low_memory=False))
        elif t.lower().endswith(".csv") and "unmapped" not in os.path.basename(t).lower():
            frames.append(pd.read_csv(t, nrows=nrows, low_memory=False))
    if not frames:
        sys.exit(f"no csv found under {path}")
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------- column detection
def find_col(cols, *needles, exclude=()):
    for c in cols:
        lc = c.lower()
        if any(n in lc for n in needles) and not any(e in lc for e in exclude):
            return c
    return None


def classify_date_column(s):
    """Return 'date' if the column holds calendar dates spanning several days, else 'weekday'."""
    vals = s.dropna().astype(str).str.strip()
    if vals.empty:
        return None, None
    low = vals.str.lower()
    if low.isin(WEEKDAYS).mean() > 0.8:
        return "weekday", None
    parsed = pd.to_datetime(vals, errors="coerce", format="mixed", dayfirst=False)
    if parsed.notna().mean() < 0.8:
        return None, None
    n_days = parsed.dt.normalize().nunique()
    return ("date" if n_days > 3 else "weekday"), parsed


def inspect_oc(df):
    cols = list(df.columns)
    print("OC file columns:", cols)
    prac = find_col(cols, "practice_code", "gp_code", "practice") or find_col(cols, "code", exclude=("pcn", "icb", "region", "sub"))
    val = find_col(cols, "value", "count", "submissions")
    time = find_col(cols, "time_category", "time_of_day", "hour", "submission_time", "time", exclude=("date",))
    metric = find_col(cols, "metric", "category", "type")
    datec, kind, parsed = None, None, None
    for c in cols:
        if c == time:
            continue
        k, p = classify_date_column(df[c])
        if k:
            datec, kind, parsed = c, k, p
            break
    print(f"  practice column : {prac}")
    print(f"  date column     : {datec}  -> {kind}")
    print(f"  time column     : {time}")
    print(f"  metric column   : {metric}")
    print(f"  value column    : {val}")
    if not (prac and val and datec):
        sys.exit("could not identify the practice / date / value columns; inspect the file by hand")
    return dict(prac=prac, date=datec, kind=kind, parsed=parsed, time=time, metric=metric, val=val)


# ---------------------------------------------------------------- metrics
def resid_metrics(df, unit, datecol, valcol, min_mean=5):
    """Residual variability about the unit's own day-of-week means."""
    d = df.copy()
    d["dow"] = d[datecol].dt.dayofweek
    d = d[d.dow < 5]
    nw = d[datecol].nunique()
    out = []
    for u, g in d.groupby(unit):
        if g[datecol].nunique() != nw or g[valcol].min() <= 0 or g[valcol].mean() < min_mean:
            continue
        y = g[valcol].to_numpy(float)
        m = y.mean()
        dm = g.groupby("dow")[valcol].transform("mean").to_numpy(float)
        rss = ((y - dm) ** 2).sum()
        rv = rss / max(len(y) - g.dow.nunique(), 1)
        out.append({unit: u, "mean": m, "resid_cv": np.sqrt(rv) / m, "disp": rv / m})
    return pd.DataFrame(out), nw


def contrast(t, col, lo=(5000, 7000), hi=25000, seed=0):
    rng = np.random.default_rng(seed)
    a = t[(t.list_size >= lo[0]) & (t.list_size < lo[1])][col].to_numpy()
    b = t[t.list_size >= hi][col].to_numpy()
    if len(a) < 20 or len(b) < 10:
        return None
    boot = [np.median(rng.choice(b, len(b))) - np.median(rng.choice(a, len(a))) for _ in range(4000)]
    return dict(lo=np.median(a) * 100, hi=np.median(b) * 100,
                diff=(np.median(b) - np.median(a)) * 100,
                lo_ci=np.percentile(boot, 2.5) * 100, hi_ci=np.percentile(boot, 97.5) * 100,
                n_lo=len(a), n_hi=len(b))


def band_table(t, cols):
    t = t.copy()
    t["band"] = pd.cut(t.list_size, BANDS, labels=LABELS)
    g = t.groupby("band", observed=True)
    out = pd.DataFrame({"n": g.size(), "list": g.list_size.median().round(0)})
    for c, nm in cols:
        out[nm] = (g[c].median() * (100 if "cv" in c else 1)).round(2)
    return out


# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--oc", required=True, help="OC Day and Time zip/csv/dir")
    p.add_argument("--cbt", required=True, help="CBT durations zip/csv/dir (CBT001 + CBT003)")
    p.add_argument("--list", dest="lst", required=True, help="practice list size csv (gp_code, list_*)")
    p.add_argument("--out", default="combined_out")
    a = p.parse_args()
    os.makedirs(a.out, exist_ok=True)

    print("=" * 70)
    print("STEP 1  what granularity is the online consultation file?")
    print("=" * 70)
    oc_head = read_any(a.oc, nrows=5000)
    spec = inspect_oc(oc_head)

    if spec["kind"] != "date":
        print("\nThe file is aggregated to day of week, not calendar date.")
        print("Combined day-to-day analysis is not possible from it. It supports within-day and")
        print("day-of-week questions only. Stopping here.")
        return

    print("\nCalendar dates present. Running the combined analysis.\n")
    oc = read_any(a.oc)
    spec2 = inspect_oc(oc.head(5000))
    oc = oc.rename(columns={spec2["prac"]: "gp_code", spec2["val"]: "value", spec2["date"]: "date"})
    oc["date"] = pd.to_datetime(oc["date"], errors="coerce", format="mixed")
    oc = oc.dropna(subset=["date", "gp_code", "value"])

    # keep total submissions only: drop any metric breakdown that would double count
    if spec2["metric"]:
        m = spec2["metric"]
        vals = oc[m].astype(str).str.upper().str.strip()
        total_like = vals.str.contains("TOTAL")
        if total_like.any():
            print(f"  using {m} == TOTAL rows ({total_like.sum():,} of {len(oc):,})")
            oc = oc[total_like]
        else:
            print(f"  summing across all {m} values (no TOTAL row present)")
    ocd = oc.groupby(["gp_code", "date"], as_index=False)["value"].sum().rename(columns={"value": "oc"})
    print(f"  OC daily rows: {len(ocd):,}  practices {ocd.gp_code.nunique():,}  dates {ocd.date.nunique()}")

    print("\n" + "=" * 70)
    print("STEP 2  telephone daily series")
    print("=" * 70)
    cbt = read_any(a.cbt)
    cbt.columns = [c.strip() for c in cbt.columns]
    cbt = cbt.rename(columns={"PRACTICE_CODE": "gp_code", "Date": "date", "Value": "value"})
    cbt["date"] = pd.to_datetime(cbt["date"], errors="coerce")
    # CBT003 appears in both the Durations file and the Calls Answered file. If both were read,
    # keep only the Durations rows (which carry a Duration value) so answered calls are not doubled.
    if "Duration" in cbt.columns:
        if "Wait_Time" in cbt.columns:
            print("  both Durations and Calls Answered files present; using Durations only")
        cbt = cbt[cbt.Duration.notna()]
    inb = (cbt[(cbt.Indicator == "CBT001") & (cbt.get("Duration", "TOTAL") == "TOTAL")]
           .groupby(["gp_code", "date"], as_index=False)["value"].sum().rename(columns={"value": "inbound"}))
    ans = (cbt[cbt.Indicator == "CBT003"]
           .groupby(["gp_code", "date"], as_index=False)["value"].sum().rename(columns={"value": "answered"}))
    for nm, fr in [("CBT001 inbound", inb), ("CBT003 answered", ans)]:
        col = fr.columns[-1]
        print(f"  {nm}: {fr[col].sum():,.0f} total")
    tel = inb.merge(ans, on=["gp_code", "date"])
    print(f"  telephone daily rows: {len(tel):,}  practices {tel.gp_code.nunique():,}  dates {tel.date.nunique()}")

    print("\n" + "=" * 70)
    print("STEP 3  combine")
    print("=" * 70)
    d = tel.merge(ocd, on=["gp_code", "date"], how="inner")
    d["attempted"] = d.inbound + d.oc
    d["received"] = d.answered + d.oc
    print(f"  practices with both routes on the same dates: {d.gp_code.nunique():,}")
    print(f"  date range: {d.date.min().date()} to {d.date.max().date()}")

    lst = pd.read_csv(a.lst)
    lcol = [c for c in lst.columns if c != "gp_code"][0]
    lst = lst.rename(columns={lcol: "list_size"})

    results = {}
    for col, nm in [("attempted", "contact attempted"), ("received", "contact received"),
                    ("inbound", "calls made"), ("answered", "calls answered"), ("oc", "forms submitted")]:
        m, nw = resid_metrics(d, "gp_code", "date", col)
        m = m.merge(lst, on="gp_code").dropna(subset=["list_size"])
        results[col] = m
        print(f"\n--- {nm}  ({nw} weekdays, n={len(m):,}) ---")
        print(band_table(m, [("mean", "per day"), ("resid_cv", "variability %"), ("disp", "overdispersion")]).to_string())
        c = contrast(m, "resid_cv")
        if c:
            print(f"    5-7k {c['lo']:.2f}%   25k+ {c['hi']:.2f}%   difference {c['diff']:+.2f}pp "
                  f"(95% CI {c['lo_ci']:+.2f} to {c['hi_ci']:+.2f})   n={c['n_lo']}/{c['n_hi']}")
        m.to_csv(os.path.join(a.out, f"metrics_{col}.csv"), index=False)

    try:
        d.to_parquet(os.path.join(a.out, "daily_combined.parquet"))
    except Exception:
        d.to_csv(os.path.join(a.out, "daily_combined.csv"), index=False)
    print(f"\nwritten to {os.path.abspath(a.out)}")
    print("\nThe row that answers the question is 'contact received': it is the combined measure,")
    print("and its 5-7k versus 25k+ difference is the estimate that replaces the telephone-only one.")


if __name__ == "__main__":
    main()
