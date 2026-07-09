#!/usr/bin/env python3
"""
f2f_increasers.py -- practices that RAISED face-to-face share against the national tide,
and whether their larger satisfaction gain survives a capacity control.

National f2f share fell ~70%->60% (2023->2026). Yet a countercultural minority raised it.
Q: did they gain more satisfaction because of in-person care, or is rising f2f just a MARKER
of recovering GP capacity (the strongest satisfaction predictor)?

Windows: early = 2023-04..2024-03, late = 2025-06..2026-05 (GPAD panel_merged, min 5000 appts/window).
Outcome: Δsatisfaction 2024->2026 (GPPS Q32). Weighted by GPPS 2026 responses, HC1 robust SE.
Nested models add capacity controls; if the Δf2f coefficient collapses, it was capacity all along.
Writes f2f_increaser_cohort.csv (Δf2f >= +5pp). Non-destructive.
"""
import os, math, sys
import numpy as np, pandas as pd, duckdb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from did_anima import wls_robust, zscore

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
PANEL = os.path.join(DATA, "panel_merged.parquet")
MASTER = os.path.join(DATA, "xsec_master_2026.csv")
OUT = os.path.join(DATA, "f2f_increaser_cohort.csv")

def pval(z): return 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))

def main():
    c = duckdb.connect()
    # per-practice trend: f2f share, GP-delivered share, appts-per-patient (capacity proxy)
    f = c.execute(f"""
    WITH e AS (SELECT gp_code,
                 SUM(f2f)*100.0/SUM(total) f2f_e, SUM(gp)*100.0/SUM(total) gpsh_e,
                 SUM(total)*1.0/SUM(list_size) apc_e, SUM(total) t_e
               FROM read_parquet('{PANEL}') WHERE month BETWEEN '2023-04' AND '2024-03' GROUP BY 1),
         l AS (SELECT gp_code,
                 SUM(f2f)*100.0/SUM(total) f2f_l, SUM(gp)*100.0/SUM(total) gpsh_l,
                 SUM(total)*1.0/SUM(list_size) apc_l, SUM(total) t_l
               FROM read_parquet('{PANEL}') WHERE month BETWEEN '2025-06' AND '2026-05' GROUP BY 1)
    SELECT e.gp_code, f2f_e, f2f_l, f2f_l-f2f_e AS d_f2f,
           gpsh_l-gpsh_e AS d_gpshare, apc_l-apc_e AS d_apc
    FROM e JOIN l USING(gp_code) WHERE t_e>5000 AND t_l>5000
    """).df()

    m = c.execute(f"""SELECT gp_code, gp_name, pcn_name, region, imd_score, list_size, log_list,
                             gp_per10k, satisfaction_2024, satisfaction, satisfaction_2026, gpps_n_2026
                      FROM read_csv_auto('{MASTER}')""").df()
    d = f.merge(m, on="gp_code").dropna(
        subset=["d_f2f", "satisfaction_2024", "satisfaction_2026", "gpps_n_2026",
                "gp_per10k", "d_apc", "log_list", "imd_score"])
    d["d_sat"] = d.satisfaction_2026 - d.satisfaction_2024
    reg = pd.get_dummies(d.region.astype(str), prefix="r", drop_first=True).astype(float)
    d = pd.concat([d, reg], axis=1); rc = list(reg.columns)

    print(f"n={len(d)} practices with f2f trend + satisfaction")
    print(f"Increasers: Δf2f>0 {int((d.d_f2f>0).sum())} | >=+5pp {int((d.d_f2f>=5).sum())} | >=+10pp {int((d.d_f2f>=10).sum())}\n")

    def run(controls, label):
        Zc = [zscore(d.d_f2f.values)] + [zscore(d[x].values) for x in controls]
        X = np.column_stack([np.ones(len(d))] + Zc + [d[rc].values])
        b, se = wls_robust(X, d.d_sat.values, d.gpps_n_2026.values)
        print(f"  {label:52s} Δf2f β = {b[1]:+.2f}pp/SD (SE {se[1]:.2f}, p={pval(b[1]/se[1]):.1e})")

    print("Δsatisfaction(24->26) ~ Δf2f, nested (all standardised, + region):")
    run(["satisfaction_2024"], "baseline only")
    run(["satisfaction_2024", "imd_score", "log_list"], "+ deprivation, size")
    run(["satisfaction_2024", "imd_score", "log_list", "gp_per10k"], "+ GP staffing LEVEL")
    run(["satisfaction_2024", "imd_score", "log_list", "gp_per10k", "d_apc"],
        "+ Δappts-per-patient (capacity/activity change)")
    run(["satisfaction_2024", "imd_score", "log_list", "gp_per10k", "d_apc", "d_gpshare"],
        "+ ΔGP-delivered share (full model)")

    # bank cohort
    inc = d[d.d_f2f >= 5].copy()
    inc["d_sat_24_26"] = inc.d_sat
    cols = ["gp_code", "gp_name", "pcn_name", "region", "imd_score", "list_size",
            "f2f_e", "f2f_l", "d_f2f", "d_apc", "gp_per10k",
            "satisfaction_2024", "satisfaction", "satisfaction_2026", "d_sat_24_26", "gpps_n_2026"]
    inc[cols].round(2).sort_values("d_f2f", ascending=False).to_csv(OUT, index=False)
    w = inc.gpps_n_2026
    print(f"\n[cohort] {len(inc)} practices (Δf2f>=+5pp) -> {OUT}")
    print(f"  weighted Δsat: increasers {np.average(inc.d_sat, weights=w):+.2f} vs "
          f"rest {np.average(d[d.d_f2f<5].d_sat, weights=d[d.d_f2f<5].gpps_n_2026):+.2f}")
    print(f"  profile: median list {inc.list_size.median():.0f}, median IMD {inc.imd_score.median():.1f}, "
          f"mean Δf2f {inc.d_f2f.mean():+.1f}pp")

if __name__ == "__main__":
    main()
