#!/usr/bin/env python3
"""
did_anima.py -- pre-registered DiD: does adopting Anima/Continuum change patient experience?

Design (PANEL_NOTES sec 3.7). Treatment = practices with Continuum Health (Anima) recorded
as an OC supplier by Mar 2026. Only ~1 carried the label during GPPS-2025 fieldwork (Jan-Mar
2025), so GPPS 2025 = PRE-adoption, GPPS 2026 (fieldwork Jan-Mar 2026) = POST. Adopters were
~5pp WORSE than average at baseline (selection: struggling-access practices adopt total triage).
DiD asks whether they moved DIFFERENTLY from 2025->2026, net of that starting gap.

Outcomes:  satisfaction, access_satisfaction, continuity, contact_fail
           (contact_fail composite = "told to contact another day" + "couldn't contact";
            2026 rebuilt as deflection_2026 + couldnt_contact_2026 to match the 2025 column.)

Three estimators, weakest->strongest control for confounding:
  1. Unadjusted DiD      -- mean change(adopters) - mean change(controls)
  2. Adjusted DiD (WLS)  -- + IMD, log list, GP/10k, OC rate, region; HC1 robust SE
  3. Matched DiD (ATT)   -- propensity match on those covariates AND the 2025 baseline level,
                            so controls start from the same score. This is the estimate that
                            guards against mean-reversion (adopters started low; low scores
                            drift up on their own). Treat #3 as the headline.

Weights = min(GPPS responses 2025, 2026). Numpy only (no scipy/statsmodels).
Writes did_anima_results.csv. Non-destructive.
"""
import os, math
import numpy as np, pandas as pd, duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
MASTER = os.path.join(DATA, "xsec_master_2026.csv")
PANEL_OC = os.path.join(DATA, "panel_oc.csv")
OUT = os.path.join(DATA, "did_anima_results.csv")

OUTCOMES = {  # label -> (2025 col, 2026 expression on the dataframe)
    "satisfaction":        ("satisfaction",        lambda d: d["satisfaction_2026"]),
    "access_satisfaction": ("access_satisfaction", lambda d: d["access_satisfaction_2026"]),
    "continuity":          ("continuity",          lambda d: d["continuity_2026"]),
    "contact_fail":        ("contact_fail",        lambda d: d["deflection_2026"] + d["couldnt_contact_2026"]),
}
COVS = ["imd_score", "log_list", "gp_per10k", "oc_rate_12m"]  # + region dummies

def norm_p(z):
    return 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))

def wls_robust(X, y, w):
    """WLS point estimate with HC1 heteroskedasticity-robust SE. Returns beta, se."""
    sw = np.sqrt(w)
    Xs, ys = X * sw[:, None], y * sw
    XtX = Xs.T @ Xs
    XtXi = np.linalg.pinv(XtX)
    beta = XtXi @ (Xs.T @ ys)
    e = ys - Xs @ beta
    n, k = Xs.shape
    meat = Xs.T @ (Xs * (e**2)[:, None])
    V = XtXi @ meat @ XtXi * (n / (n - k))
    return beta, np.sqrt(np.diag(V))

def logit_irls(X, y, iters=50):
    """Logistic regression via IRLS with tiny ridge for stability. Returns coefs."""
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = np.clip(X @ b, -30, 30)
        p = 1 / (1 + np.exp(-eta))
        W = np.clip(p * (1 - p), 1e-6, None)
        z = eta + (y - p) / W
        XtW = X.T * W
        b_new = np.linalg.pinv(XtW @ X + 1e-6 * np.eye(X.shape[1])) @ (XtW @ z)
        if np.max(np.abs(b_new - b)) < 1e-8:
            b = b_new; break
        b = b_new
    return b

def zscore(a):
    return (a - np.nanmean(a)) / (np.nanstd(a) + 1e-9)

def main():
    con = duckdb.connect()
    df = con.execute(f"SELECT * FROM read_csv_auto('{MASTER}')").df()

    # adopter flag: Continuum recorded in the LATEST OC month per practice (i.e. by Mar 2026)
    adopt = con.execute(f"""
        WITH last AS (
          SELECT gp_code, supplier,
                 ROW_NUMBER() OVER (PARTITION BY gp_code ORDER BY month DESC) rn
          FROM read_csv_auto('{PANEL_OC}')
        )
        SELECT DISTINCT gp_code FROM last WHERE rn=1 AND upper(supplier) LIKE '%CONTINUUM%'
    """).df()["gp_code"].tolist()
    df["adopter"] = df["gp_code"].isin(adopt).astype(int)

    # region dummies (drop first)
    reg = pd.get_dummies(df["region"].astype(str), prefix="reg", drop_first=True).astype(float)
    df = pd.concat([df, reg], axis=1)
    reg_cols = list(reg.columns)

    rows = []
    print(f"Adopters (Continuum by Mar 2026): {df['adopter'].sum()}  |  controls: {(df['adopter']==0).sum()}\n")
    print(f"{'outcome':20s}{'base_adopt':>11s}{'base_ctrl':>10s}{'DiD_unadj':>11s}"
          f"{'DiD_adj':>10s}{'(p)':>9s}{'DiD_match':>11s}{'(p)':>9s}")

    for label, (c25, f26) in OUTCOMES.items():
        d = df.copy()
        d["y25"] = d[c25]
        d["y26"] = f26(d)
        d["dy"] = d["y26"] - d["y25"]
        d["w"] = np.minimum(d["gpps_n"], d["gpps_n_2026"])
        keep = ["adopter", "y25", "y26", "dy", "w"] + COVS + reg_cols
        d = d[keep].replace([np.inf, -np.inf], np.nan).dropna()
        d = d[d["w"] > 0]
        A, C = d[d.adopter == 1], d[d.adopter == 0]
        base_a = np.average(A.y25, weights=A.w); base_c = np.average(C.y25, weights=C.w)
        dA = np.average(A.dy, weights=A.w); dC = np.average(C.dy, weights=C.w)

        # 1. unadjusted DiD
        X1 = np.column_stack([np.ones(len(d)), d.adopter.values])
        b1, se1 = wls_robust(X1, d.dy.values, d.w.values)
        did_un, se_un = b1[1], se1[1]

        # 2. adjusted DiD (covariates + region), HC1 robust
        Xc = np.column_stack([np.ones(len(d)), d.adopter.values,
                              d[COVS].values, d[reg_cols].values])
        b2, se2 = wls_robust(Xc, d.dy.values, d.w.values)
        did_adj, se_adj = b2[1], se2[1]
        p_adj = norm_p(did_adj / se_adj)

        # 3. propensity-matched DiD (match on covariates + BASELINE level -> reversion guard)
        pv = np.column_stack([np.ones(len(d)),
                              np.column_stack([zscore(d[c].values) for c in COVS + ["y25"]]),
                              d[reg_cols].values])
        ps_b = logit_irls(pv, d.adopter.values.astype(float))
        d = d.assign(lp=np.clip(pv @ ps_b, -30, 30))  # linear predictor (logit propensity)
        cal = 0.2 * np.std(d.lp.values)
        ctrl = d[d.adopter == 0].copy(); used = set()
        mi = []
        for _, a in d[d.adopter == 1].iterrows():
            cand = ctrl[~ctrl.index.isin(used)]
            diff = (cand.lp - a.lp).abs()
            near = diff[diff <= cal].nsmallest(3)  # up to 3 nearest within caliper
            if len(near):
                for idx in near.index:
                    used.add(idx); mi.append((a.name, idx))
        ma = d.loc[[m[0] for m in mi]]; mc = d.loc[[m[1] for m in mi]]
        if len(ma):
            did_m = np.average(ma.dy, weights=ma.w) - np.average(mc.dy, weights=mc.w)
            # SE via WLS on stacked matched sample
            ms = pd.concat([ma.assign(t=1), mc.assign(t=0)])
            Xm = np.column_stack([np.ones(len(ms)), ms.t.values])
            bm, sem = wls_robust(Xm, ms.dy.values, ms.w.values)
            did_m, se_m = bm[1], sem[1]; p_m = norm_p(did_m / se_m)
            n_matched_c = len(set(m[1] for m in mi))
        else:
            did_m = se_m = p_m = np.nan; n_matched_c = 0

        print(f"{label:20s}{base_a:>11.1f}{base_c:>10.1f}{did_un:>+11.2f}"
              f"{did_adj:>+10.2f}{p_adj:>9.1e}{did_m:>+11.2f}{p_m:>9.1e}")
        rows.append(dict(outcome=label, n_adopt=int(len(A)), n_ctrl=int(len(C)),
                         base_adopter=round(base_a,2), base_control=round(base_c,2),
                         d_adopter=round(dA,2), d_control=round(dC,2),
                         did_unadj=round(did_un,3), se_unadj=round(se_un,3),
                         did_adj=round(did_adj,3), se_adj=round(se_adj,3), p_adj=p_adj,
                         did_matched=round(did_m,3) if not np.isnan(did_m) else None,
                         se_matched=round(se_m,3) if not np.isnan(did_m) else None,
                         p_matched=p_m if not np.isnan(did_m) else None,
                         n_matched_ctrl=n_matched_c))

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nwritten -> {OUT}")
    print("\nReading: base_adopter << base_control confirms selection (adopters start worse).")
    print("Positive DiD on satisfaction/access = adopters improved MORE than controls;")
    print("negative DiD on contact_fail = failures fell MORE for adopters. The MATCHED column")
    print("(controls with the same baseline score) is the reversion-guarded headline.")

if __name__ == "__main__":
    main()
