#!/usr/bin/env python3
"""
refresh_supplement_gpad_2526.py -- bring the GPAD-derived fields of
data/xsec_supplement.csv onto the same April 2025 - March 2026 window as the
canonical xsec_master_2026 (see refresh_gpad_2526.py and the September 2026
correction in PANEL_NOTES.md).

Why: xsec_supplement.csv (159 practices missing from the main cross-section, used by
mypractice.html for its "reduced" page) was built on 11 Jul 2026 from the panel with
the April 2024 - March 2025 window. After the 29 Sep 2026 correction those practices
were being compared against peers whose figures cover April 2025 - March 2026.

Refreshed (same definitions as refresh_gpad_2526.py):
  list_size     12-month mean of the monthly panel list count, Apr25-Mar26
  appts_percap  1000 * total appointments / 12 / list_size
  sd_share      100 * same-day appointments / total appointments
  gp_per10k     rescaled to the new list_size with the implied GP FTE held fixed
                (FTE = old gp_per10k * old list_size / 10,000), mirroring the master,
                which keeps March 2025 FTEs and recomputes rates on the refreshed list

Rule: a practice with fewer than 12 GPAD months in the window has all four fields set
to missing (partial totals are never annualised), as in the master.

Unchanged: every other column (survey outcomes, IMD, names, geography), row order.
Run from anywhere:  python3 research/scripts/refresh_supplement_gpad_2526.py
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SUP = os.path.join(DATA, "xsec_supplement.csv")
PM = os.path.join(DATA, "panel_merged.parquet")
WIN = ("2025-04", "2026-03")
BLOCK = ["list_size", "appts_percap", "sd_share", "gp_per10k"]


def main():
    # Keep the file's original text for every non-refreshed column (no float round-trip).
    raw = pd.read_csv(SUP, dtype=str, keep_default_na=False)
    s = pd.read_csv(SUP, dtype={"gp_code": str})
    shape0, cols0 = s.shape, list(s.columns)
    pm = pd.read_parquet(PM, columns=["gp_code", "month", "total", "same_day", "list_size"])
    m = pm[(pm.month >= WIN[0]) & (pm.month <= WIN[1])]
    g = m.groupby("gp_code")
    agg = pd.DataFrame({
        "n_months": g["month"].nunique(),
        "total": g["total"].sum(),
        "same_day": g["same_day"].sum(),
        "ls_new": g["list_size"].mean(),
    })

    old_ls = s["list_size"].where(s["list_size"] > 0)
    gp_fte = s["gp_per10k"] * old_ls / 10000.0

    j = s[["gp_code"]].join(agg, on="gp_code")
    ok = j["n_months"].eq(12)
    ls = j["ls_new"].where(j["ls_new"] > 0)

    new = pd.DataFrame(index=s.index)
    new["list_size"] = ls
    new["appts_percap"] = 1000.0 * j["total"] / 12 / ls
    new["sd_share"] = 100.0 * j["same_day"] / j["total"].replace(0, np.nan)
    new["gp_per10k"] = 10000.0 * gp_fte / ls
    new.loc[~ok, BLOCK] = np.nan

    before = s[BLOCK].notna().sum()
    for c in BLOCK:
        s[c] = new[c]
        raw[c] = new[c].map(lambda v: "" if pd.isna(v) else repr(float(v)))

    assert s.shape == shape0 and list(s.columns) == cols0 and list(raw.columns) == cols0
    print(f"[window] {WIN[0]}..{WIN[1]}; practices with 12 months: {int(ok.sum())} of {len(s)}")
    print("[non-missing before -> after]")
    for c in BLOCK:
        print(f"   {c:13s} {int(before[c]):4d} -> {int(s[c].notna().sum()):4d}")
    raw.to_csv(SUP, index=False)
    print(f"[write] {SUP}")


if __name__ == "__main__":
    main()
