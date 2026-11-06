#!/usr/bin/env python3
"""
Did any practices change their OC opening pattern? Classify every practice in every month with
the OC Hours rules (scaled to each month's weekday / weekend-day counts), then follow practices
that moved from core-hours-only to 24/7, and compare their 8-10am shares before and after with
practices that stayed core-hours-only over the same months (difference in differences).

    python research/scripts/oc_hours_switchers.py --out research/data/oc_hours_sep26
"""
import argparse, glob, io, zipfile, os
import numpy as np, pandas as pd

p = argparse.ArgumentParser()
p.add_argument("--panel", default="research/data/panel")
p.add_argument("--oc-sep", default="research/data/oc_daytime_sep26.zip")
p.add_argument("--cbt-sep", default="research/data/cbt_daytime_sep26.zip")
p.add_argument("--list", default="research/data/list_jul26.csv")
p.add_argument("--out", required=True)
a = p.parse_args()
NIGHT = ["18:30 - 23:59", "00:00 - 05:59", "06:00 - 06:59", "07:00 - 07:59"]
R810 = ["08:00 - 08:59", "09:00 - 09:59"]
CORE_CBT = ["08:00-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:59", "16:00-17:59", "18:00-18:29"]

def load_oc():
    out = {}
    for f in sorted(glob.glob(f"{a.panel}/oc_daytime_*.parquet")):
        d = pd.read_parquet(f, columns=["gp_code", "date", "band", "CLINICAL", "TOTAL"])
        out[d.date.dt.strftime("%Y-%m").iloc[0]] = d
    fr = []
    with zipfile.ZipFile(a.oc_sep) as z:
        for n in z.namelist():
            if n.lower().endswith(".csv"):
                fr.append(pd.read_csv(io.BytesIO(z.read(n)), usecols=["DATE", "GP_CODE", "SUBMISSION_TIME", "CLINICAL", "TOTAL"]))
    d = pd.concat(fr).rename(columns={"DATE": "date", "GP_CODE": "gp_code", "SUBMISSION_TIME": "band"})
    d["date"] = pd.to_datetime(d.date)
    out["2026-09"] = d
    return out

def classify(d):
    wk = d.date.dt.dayofweek >= 5
    nwd = d.loc[~wk, "date"].nunique(); nwe = d.loc[wk, "date"].nunique()
    night = ~wk & d.band.isin(NIGHT); core = ~wk & ~d.band.isin(NIGHT)
    G = pd.DataFrame({"tot": d.groupby("gp_code").TOTAL.sum()})
    G["core"] = d[core].groupby("gp_code").TOTAL.sum()
    G["core_cl"] = d[core].groupby("gp_code").CLINICAL.sum()
    G["r810"] = d[~wk & d.band.isin(R810)].groupby("gp_code").TOTAL.sum()
    G["ooh"] = d[night | wk].groupby("gp_code").TOTAL.sum()
    G["wkend_days"] = d[wk & (d.TOTAL > 0)].groupby("gp_code").date.nunique()
    G["night_days"] = d[night & (d.TOTAL > 0)].groupby("gp_code").date.nunique()
    G["wkend_cl_days"] = d[wk & (d.CLINICAL > 0)].groupby("gp_code").date.nunique()
    G = G.fillna(0); G["nwd"] = nwd
    def g(r):
        if r.tot < 300: return None
        if r.wkend_days == 0 and r.night_days <= 3: return "A"
        if r.wkend_days <= 1 and r.night_days >= 0.8 * nwd: return "B"
        if r.wkend_days >= 0.85 * nwe and r.night_days >= 0.8 * nwd:
            if r.wkend_cl_days >= 0.75 * nwe: return "D"
            if r.wkend_cl_days <= 1 and r.core and r.core_cl / r.core >= 0.3: return "C"
        return None
    G["g"] = G.apply(g, axis=1)
    return G

oc = load_oc()
months = sorted(oc)
cls = {m: classify(oc[m]) for m in months}
grp = pd.DataFrame({m: cls[m].g for m in months})
grp.to_csv(f"{a.out}/monthly_groups.csv")
print("months:", months)
print("practices per group per month:"); print(grp.apply(lambda s: s.value_counts()).fillna(0).astype(int))

# history of September's 24/7 clinical practices
D = grp[grp["2026-09"] == "D"]
earlier = [m for m in months if m < "2026-09"]
hist = D[earlier].apply(lambda r: "".join((x if isinstance(x, str) else "-") for x in r), axis=1)
first = D[earlier[:3]].apply(lambda r: r.dropna().mode().iat[0] if r.notna().any() else "-", axis=1)
print("\nSeptember 24/7-clinical practices by their Dec-Feb pattern:"); print(first.value_counts())

# switchers: core-hours-only (A) in every classified month Dec-Feb, and D in Jun and Sep
def stable(row, ms, val): return all(row[m] == val for m in ms)
pre, post = earlier[:3], ["2026-06", "2026-09"]
sw = grp[grp.apply(lambda r: stable(r, pre, "A") and stable(r, post, "D"), axis=1)].index
ctl = grp[grp.apply(lambda r: stable(r, pre + post, "A"), axis=1)].index
print(f"\nA (Dec-Feb) -> D (Jun & Sep) switchers: {len(sw)}; stable A controls: {len(ctl)}")
# when did they switch?
sw_month = grp.loc[sw, earlier[3:] + ["2026-09"]].apply(lambda r: next((m for m, v in r.items() if v == "D"), None), axis=1)
print("first month classified 24/7 clinical:", sw_month.value_counts().sort_index().to_dict())

# outcomes per practice-month: OC 8-10 share of core weekday OC; OC per 1k; calls 8-10 share; combined share
L = pd.read_csv(a.list).set_index("gp_code").iloc[:, 0]
def cbt_month(m):
    if m == "2026-09":
        fr = []
        with zipfile.ZipFile(a.cbt_sep) as z:
            for n in z.namelist():
                if n.lower().endswith(".csv") and "unmapped" not in n.lower():
                    x = pd.read_csv(io.BytesIO(z.read(n)), usecols=["Date", "PRACTICE_CODE", "Indicator", "Time_Category", "Value"])
                    fr.append(x[x.Indicator == "CBT001"])
        x = pd.concat(fr).rename(columns={"Date": "date", "PRACTICE_CODE": "gp_code", "Time_Category": "band", "Value": "inbound"})
        x["date"] = pd.to_datetime(x.date); x["band"] = x.band.str.replace(" ", "")
    else:
        f = f"{a.panel}/cbt_daytime_{m}.parquet"
        if not os.path.exists(f): return None
        x = pd.read_parquet(f, columns=["gp_code", "date", "band", "inbound"])
    x = x[(x.date.dt.dayofweek < 5) & x.band.isin(CORE_CBT)]
    return pd.DataFrame({"calls_core": x.groupby("gp_code").inbound.sum(), "calls_810": x[x.band == CORE_CBT[0]].groupby("gp_code").inbound.sum(), "cbt_days": x.groupby("gp_code").date.nunique()})
rows = []
for m in months:
    G = cls[m]; C = cbt_month(m)
    ids = list(sw) + list(ctl)
    X = G.reindex(ids)[["core", "r810", "ooh", "tot", "nwd"]].copy()
    if C is not None: X = X.join(C)
    X["month"] = m; X["switcher"] = X.index.isin(sw)
    rows.append(X)
P = pd.concat(rows).reset_index().rename(columns={"index": "gp_code"})
P["list"] = P.gp_code.map(L)
P["oc_rush"] = P.r810 / P.core
P["oc_ooh_share"] = P.ooh / P.tot
P["oc_pk"] = P.core / P.nwd / P.list * 1000
P["ph_rush"] = P.calls_810 / P.calls_core
P["comb_rush"] = (P.calls_810 + P.r810) / (P.calls_core + P.core)
P.to_csv(f"{a.out}/switchers_panel.csv", index=False)
ys = ["oc_rush", "oc_ooh_share", "oc_pk", "ph_rush", "comb_rush"]
T = P.groupby(["switcher", "month"])[ys].median().round(3)
print("\nmedians by month (False = stable core-hours-only, True = switched to 24/7 clinical):"); print(T.to_string())
T.to_csv(f"{a.out}/switchers_monthly_medians.csv")
# difference in differences: practice-level change Dec-Feb mean -> Sep, switchers vs controls
pre_m = P[P.month.isin(pre)].groupby("gp_code")[ys].mean()
post_m = P[P.month == "2026-09"].set_index("gp_code")[ys]
ch = (post_m - pre_m).dropna(how="all"); ch["switcher"] = ch.index.isin(sw)
import statsmodels.formula.api as smf
res = []
for y in ys:
    d = ch.dropna(subset=[y])
    r = smf.ols(f"{y} ~ switcher", d).fit(cov_type="HC3")
    lo, hi = r.conf_int().loc["switcher[T.True]"]
    res.append(dict(outcome=y, did=r.params["switcher[T.True]"], lo=lo, hi=hi, n_switch=int(d.switcher.sum()), n_ctl=int((~d.switcher).sum()),
                    change_switch=d[d.switcher][y].median(), change_ctl=d[~d.switcher][y].median()))
R = pd.DataFrame(res).round(4); R.to_csv(f"{a.out}/switchers_did.csv", index=False)
print("\nchange Dec-Feb -> Sep, switchers minus controls:"); print(R.to_string())

# ---- looser definition: core-hours-only in most classified Dec-Feb months, group X in September
def mostly(row, ms, val):
    v = [row[m] for m in ms if isinstance(row[m], str)]
    return len(v) >= 2 and sum(x == val for x in v) >= len(v) - (0 if len(v) < 3 else 1)
base = grp.apply(lambda r: mostly(r, pre, "A"), axis=1)
ctl2 = grp.index[base & (grp["2026-09"] == "A")]
out = []
for X in "BCD":
    swx = grp.index[base & (grp["2026-09"] == X)]
    first_m = grp.loc[swx, earlier[3:] + ["2026-09"]].apply(lambda r: next((m for m, v in r.items() if v == X), None), axis=1)
    rows = []
    for m in months:
        G = cls[m]; C = cbt_month(m)
        Z = G.reindex(list(swx) + list(ctl2))[["core", "r810", "ooh", "tot", "nwd"]].copy()
        if C is not None: Z = Z.join(C)
        Z["month"] = m; Z["sw"] = Z.index.isin(swx); rows.append(Z)
    Q = pd.concat(rows).reset_index().rename(columns={"index": "gp_code"})
    Q["list"] = Q.gp_code.map(L)
    Q["oc_rush"] = Q.r810 / Q.core; Q["oc_ooh_share"] = Q.ooh / Q.tot; Q["oc_pk"] = Q.core / Q.nwd / Q.list * 1000
    Q["calls_pk"] = Q.calls_core / Q.cbt_days / Q.list * 1000
    Q["ph_rush"] = Q.calls_810 / Q.calls_core; Q["comb_rush"] = (Q.calls_810 + Q.r810) / (Q.calls_core + Q.core)
    pre_m = Q[Q.month.isin(pre)].groupby("gp_code")[ys + ["calls_pk"]].mean()
    post_m = Q[Q.month == "2026-09"].set_index("gp_code")[ys + ["calls_pk"]]
    ch = (post_m - pre_m); ch["sw"] = ch.index.isin(swx)
    for y in ys + ["calls_pk"]:
        d = ch.dropna(subset=[y])
        if d.sw.sum() < 3: continue
        r = smf.ols(f"{y} ~ sw", d).fit(cov_type="HC3"); lo, hi = r.conf_int().loc["sw[T.True]"]
        out.append(dict(to=X, outcome=y, n_switch=int(d.sw.sum()), n_ctl=int((~d.sw).sum()),
                        pre_switch=pre_m.loc[pre_m.index.isin(swx), y].median(), post_switch=post_m.loc[post_m.index.isin(swx), y].median(),
                        pre_ctl=pre_m.loc[pre_m.index.isin(ctl2), y].median(), post_ctl=post_m.loc[post_m.index.isin(ctl2), y].median(),
                        did=r.params["sw[T.True]"], lo=lo, hi=hi))
    print(f"\ncore-hours-only Dec-Feb -> {X} in Sep: {len(swx)} practices; first month in new group: {first_m.value_counts().sort_index().to_dict()}")
O = pd.DataFrame(out).round(3); O.to_csv(f"{a.out}/switchers_did_loose.csv", index=False)
print(O.to_string())
