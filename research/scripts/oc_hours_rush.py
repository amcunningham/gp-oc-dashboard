#!/usr/bin/env python3
"""
Do practices that leave online consultation (OC) open 24/7 have less of an 8am rush?

Classifies practices by when OC submissions actually arrive (OC "By Day and Time" file),
then compares their time-of-day contact pattern with calls (CBT "By Day and Time").

    python research/scripts/oc_hours_rush.py \
        --oc  research/data/oc_daytime_jun26.zip \
        --cbt research/data/cbt_daytime_may.parquet --cbt-year 2026 \
        --out research/data/oc_hours

Groups (practices with >=300 OC submissions in the month):
  A core hours only      no weekend submissions, <=3 weekday nights with any out-of-hours submission
  B weekday early/late   >=18 weekday nights, <=1 weekend day (mostly a 7am opening)
  C 24/7 admin only      >=7 of 8 weekend days and >=18 nights, no clinical at weekends (<=1 day)
                         and >=30% of core-hours submissions coded clinical (excludes non-coding suppliers)
  D 24/7 incl. clinical  >=7 weekend days, >=18 nights, clinical on >=6 weekend days
"Nights" = weekday dates with any submission 18:30-23:59 or 00:00-07:59.
Thresholds assume a month with 22 weekdays and 8 weekend days (June 2026); adjust for others.

Outputs: practice-level file, group summary, OC and call rates per 1,000 per weekday by band,
and adjusted models (OLS, HC3) of 8-10am rush measures on group, OC volume, list, IMD, age, region.
"""
import argparse, io, zipfile, os
import numpy as np, pandas as pd

p = argparse.ArgumentParser()
p.add_argument("--oc", required=True)
p.add_argument("--cbt", required=True, help="CBT 'By Day and Time' zip as published, or a pre-aggregated parquet (gp_code,dow,tc,inbound,ivr_ended,answered,ndays[,yr])")
p.add_argument("--cbt-year", type=int, default=None)
p.add_argument("--list", default="research/data/list_jul26.csv")
p.add_argument("--xsec", default="research/data/xsec_master.parquet")
p.add_argument("--out", default="research/data/oc_hours")
p.add_argument("--min-oc", type=int, default=300)
p.add_argument("--bank-holidays", default="", help="comma-separated YYYY-MM-DD dates to drop from the CBT month")
a = p.parse_args()
os.makedirs(a.out, exist_ok=True)

# ---------------- OC
frames = []
with zipfile.ZipFile(a.oc) as z:
    for n in z.namelist():
        if n.lower().endswith(".csv"):
            frames.append(pd.read_csv(io.BytesIO(z.read(n)), usecols=["DATE", "GP_CODE", "SUPPLIER", "SUBMISSION_TIME", "CLINICAL", "ADMIN", "UNKNOWN_OTHER", "TOTAL"]))
oc = pd.concat(frames, ignore_index=True)
oc["d"] = pd.to_datetime(oc.DATE)
oc = oc.rename(columns={"GP_CODE": "gp", "SUPPLIER": "sup", "SUBMISSION_TIME": "t", "CLINICAL": "cl", "TOTAL": "tot"})
wd_dates = oc.loc[oc.d.dt.dayofweek < 5, "d"].nunique()
we_dates = oc.loc[oc.d.dt.dayofweek >= 5, "d"].nunique()
print(f"OC month: {oc.d.min():%Y-%m-%d}..{oc.d.max():%Y-%m-%d}; {wd_dates} weekdays, {we_dates} weekend days")
oc["wkend"] = oc.d.dt.dayofweek >= 5
CORE = ["08:00 - 08:59", "09:00 - 09:59", "10:00 - 10:59", "11:00 - 11:59", "12:00 - 12:59", "13:00 - 13:59",
        "14:00 - 14:59", "15:00 - 15:59", "16:00 - 16:59", "17:00 - 17:59", "18:00 - 18:29"]
NIGHT = ["18:30 - 23:59", "00:00 - 05:59", "06:00 - 06:59", "07:00 - 07:59"]
oc["core"] = ~oc.wkend & oc.t.isin(CORE)
oc["night"] = ~oc.wkend & oc.t.isin(NIGHT)
oc["deep"] = ~oc.wkend & (oc.t == "00:00 - 05:59")
oc["r810"] = ~oc.wkend & oc.t.isin(CORE[:2])
g = oc.groupby("gp")
P = pd.DataFrame({"tot": g.tot.sum(), "sup": g.sup.agg(lambda s: s.mode().iat[0])})
for k in ["core", "night", "deep", "wkend", "r810"]:
    P[k] = oc[oc[k]].groupby("gp").tot.sum()
    P[k + "_cl"] = oc[oc[k]].groupby("gp").cl.sum()
P["wkend_days"] = oc[oc.wkend & (oc.tot > 0)].groupby("gp").d.nunique()
P["night_days"] = oc[oc.night & (oc.tot > 0)].groupby("gp").d.nunique()
P["deep_days"] = oc[oc.deep & (oc.tot > 0)].groupby("gp").d.nunique()
P["wkend_cl_days"] = oc[oc.wkend & (oc.cl > 0)].groupby("gp").d.nunique()
P = P.fillna(0)
P["cat_share"] = P.core_cl / P.core.replace(0, np.nan)

def grp(r):
    if r.tot < a.min_oc: return None
    if r.wkend_days == 0 and r.night_days <= 3: return "A"
    if r.wkend_days <= 1 and r.night_days >= 18: return "B"
    if r.wkend_days >= 7 and r.night_days >= 18:
        if r.wkend_cl_days >= 6: return "D"
        if r.wkend_cl_days <= 1 and r.cat_share >= 0.3: return "C"
    return None
P["g"] = P.apply(grp, axis=1)
NAMES = {"A": "Core hours only", "B": "Weekday early/late", "C": "24/7 admin only", "D": "24/7 incl. clinical"}

# ---------------- CBT
WE_CALLS = None
if a.cbt.lower().endswith(".zip"):
    # raw publication: Date, PRACTICE_CODE, Indicator, Time_Category, Value (one csv per region)
    fr = []
    with zipfile.ZipFile(a.cbt) as z:
        for n in z.namelist():
            if n.lower().endswith(".csv") and "unmapped" not in n.lower():
                d = pd.read_csv(io.BytesIO(z.read(n)), usecols=["Date", "PRACTICE_CODE", "Indicator", "Time_Category", "Value"])
                fr.append(d[d.Indicator.isin(["CBT001", "CBT002", "CBT003"])])
    raw = pd.concat(fr, ignore_index=True)
    raw["Date"] = pd.to_datetime(raw.Date)
    hol = pd.to_datetime(a.bank_holidays.split(",")) if a.bank_holidays else pd.DatetimeIndex([])
    raw = raw[~raw.Date.isin(hol)]
    days = pd.Series(pd.date_range(raw.Date.min().replace(day=1), raw.Date.max() + pd.offsets.MonthEnd(0)))
    days = days[~days.isin(hol)]
    nd = days.dt.dayofweek.value_counts()          # weekday dates per dow (0=Mon)
    print(f"CBT month: {days.min():%Y-%m}; weekday dates by dow (0=Mon): {nd.sort_index().to_dict()}")
    raw["dow0"] = raw.Date.dt.dayofweek
    wk = raw[(raw.dow0 >= 5) & (raw.Indicator == "CBT001")]
    WE_CALLS = wk.groupby("PRACTICE_CODE").Value.sum() / nd.reindex([5, 6]).fillna(0).sum()   # per weekend day
    raw = raw[raw.dow0 < 5]
    c = raw.pivot_table(index=["PRACTICE_CODE", "dow0", "Time_Category"], columns="Indicator", values="Value", aggfunc="sum").reset_index()
    c = c.rename(columns={"PRACTICE_CODE": "gp_code", "Time_Category": "tc", "CBT001": "inbound", "CBT002": "ivr_ended", "CBT003": "answered"})
    c["ndays"] = c.dow0.map(nd)
    c["dow"] = c.dow0 + 1
    c["tc"] = c.tc.str.replace(" ", "")
else:
    c = pd.read_parquet(a.cbt)
    if a.cbt_year is not None and "yr" in c:
        c = c[c.yr == a.cbt_year]
c["pd"] = c.inbound / c.ndays
c["apd"] = c.answered / c.ndays
BANDS = sorted(c.tc.unique())
CBT_CORE = ["08:00-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:59", "16:00-17:59", "18:00-18:29"]
idx = pd.MultiIndex.from_product([c.gp_code.unique(), range(1, 6), BANDS], names=["gp_code", "dow", "tc"])
cb = c.set_index(["gp_code", "dow", "tc"])[["pd", "apd"]].reindex(idx).fillna(0).groupby(["gp_code", "tc"]).mean()
calls = cb.pd.unstack()
ans = cb.apd.unstack()

L = pd.read_csv(a.list).set_index("gp_code").iloc[:, 0].rename("list")
X = pd.read_parquet(a.xsec).set_index("gp_code")[["imd_score", "region", "pct65plus"]]
M = P.join(L).join(X)
M = M[M.g.notna() & M.list.notna() & M.index.isin(calls.index)]
k = 1000 / M.list
M["calls_810_pk"] = calls.loc[M.index, "08:00-09:59"] * k
M["calls_core_pk"] = calls.loc[M.index, CBT_CORE].sum(axis=1) * k
M["calls_24h_pk"] = calls.loc[M.index].sum(axis=1) * k
M["ans_810_pk"] = ans.loc[M.index, "08:00-09:59"] * k
if WE_CALLS is not None:
    M["calls_wkend_pk_day"] = WE_CALLS.reindex(M.index).fillna(0) * k
M = M[M.calls_core_pk.between(0.01, 200)]
k = 1000 / M.list
M["oc_core_pk"] = M.core / wd_dates * k
M["oc_810_pk"] = M.r810 / wd_dates * k
M["oc_night_pk"] = M.night / wd_dates * k
M["oc_wkend_pk_day"] = M.wkend / we_dates * k
M["ph_rush"] = M.calls_810_pk / M.calls_core_pk
M["oc_rush_core"] = M.r810 / M.core
M["comb_rush"] = (M.calls_810_pk + M.oc_810_pk) / (M.calls_core_pk + M.oc_core_pk)
M["comb_810_pk"] = M.calls_810_pk + M.oc_810_pk
M["day24_pk"] = M.calls_24h_pk + M.oc_core_pk + M.oc_night_pk
M.index.name = "gp_code"
M.to_csv(f"{a.out}/practice_groups.csv")
print(M.g.value_counts().sort_index())

# ---------------- pooled rates by band (per 1,000 per weekday)
OCBAND = {"00:00 - 05:59": "00:00-05:59", "06:00 - 06:59": "06:00-07:59", "07:00 - 07:59": "06:00-07:59",
          "08:00 - 08:59": "08:00-09:59", "09:00 - 09:59": "08:00-09:59", "10:00 - 10:59": "10:00-11:59",
          "11:00 - 11:59": "10:00-11:59", "12:00 - 12:59": "12:00-13:59", "13:00 - 13:59": "12:00-13:59",
          "14:00 - 14:59": "14:00-15:59", "15:00 - 15:59": "14:00-15:59", "16:00 - 16:59": "16:00-17:59",
          "17:00 - 17:59": "16:00-17:59", "18:00 - 18:29": "18:00-18:29", "18:30 - 23:59": "18:30-23:59"}
o = oc[~oc.wkend & oc.gp.isin(M.index)].copy()
o["band"] = o.t.map(OCBAND)
o["g"] = o.gp.map(M.g)
LG = M.groupby("g").list.sum()
ocr = o.groupby(["g", "band"]).tot.sum().unstack(0).div(LG).mul(1000 / wd_dates).fillna(0)
cr = calls.loc[M.index].mul(1).groupby(M.g).sum().T.div(LG).mul(1000)
bands = pd.concat({"oc": ocr, "calls": cr}, axis=1).round(3)
bands.to_csv(f"{a.out}/rates_by_band.csv")

# ---------------- group summary incl. "work facing the team 8-10am"
S = []
for gk in "ABCD":
    oc_c, cl = ocr[gk], cr[gk]
    core_calls = cl[CBT_CORE].sum(); core_oc = oc_c[CBT_CORE].sum()
    ooh_oc = oc_c[["00:00-05:59", "06:00-07:59", "18:30-23:59"]].sum()
    wk_oc = M[M.g == gk].wkend.sum() / LG[gk] * 1000 / (we_dates / 2)   # per weekend (2 days)
    wk_calls = (2 * (M[M.g == gk].calls_wkend_pk_day * M[M.g == gk].list).sum() / LG[gk]) if "calls_wkend_pk_day" in M else np.nan
    num = 5 * (cl["08:00-09:59"] + oc_c["08:00-09:59"] + ooh_oc) + wk_oc
    den = 5 * (core_calls + core_oc + ooh_oc) + wk_oc
    S.append(dict(group=gk, name=NAMES[gk], practices=int((M.g == gk).sum()),
                  median_oc_core_pk=M[M.g == gk].oc_core_pk.median(), median_list=M[M.g == gk].list.median(),
                  comb_810_pk=cl["08:00-09:59"] + oc_c["08:00-09:59"], comb_core_pk=core_calls + core_oc,
                  share_arriving_810=(cl["08:00-09:59"] + oc_c["08:00-09:59"]) / (core_calls + core_oc),
                  contacts_24h_pk_weekday=cl.sum() + oc_c.sum(),
                  contacts_per_week_pk=5 * (cl.sum() + oc_c.sum()) + wk_oc,
                  weekend_calls_per_week_pk=wk_calls, weekend_oc_per_week_pk=wk_oc,
                  share_facing_team_810=num / den,
                  oc_share_facing_team_810=(5 * (oc_c["08:00-09:59"] + ooh_oc) + wk_oc) / (5 * (core_oc + ooh_oc) + wk_oc)))
S = pd.DataFrame(S).round(4)
S.to_csv(f"{a.out}/group_summary.csv", index=False)
print(S.to_string())

# ---------------- adjusted models
try:
    import statsmodels.formula.api as smf
    d = M.dropna(subset=["imd_score", "pct65plus", "region"]).copy()
    d["loc"] = np.log(d.oc_core_pk.clip(lower=.1)); d["ll"] = np.log(d.list)
    R = []
    for y in ["ph_rush", "oc_rush_core", "comb_rush", "comb_810_pk", "day24_pk"]:
        r = smf.ols(f"{y} ~ C(g) + loc + I(loc**2) + ll + imd_score + pct65plus + C(region)", d).fit(cov_type="HC3")
        for gk in "BCD":
            t = f"C(g)[T.{gk}]"
            R.append(dict(outcome=y, group=gk, coef=r.params[t], lo=r.conf_int().loc[t, 0], hi=r.conf_int().loc[t, 1], p=r.pvalues[t], n=int(r.nobs)))
    pd.DataFrame(R).round(4).to_csv(f"{a.out}/adjusted_models.csv", index=False)
    # 24h contacts: add adjustments one at a time, to see what deprivation and age explain
    steps = [("none", ""), ("+imd", "+ imd_score"), ("+imd+age", "+ imd_score + pct65plus"),
             ("+imd+age+list+region", "+ imd_score + pct65plus + ll + C(region)"),
             ("+all incl OC volume", "+ imd_score + pct65plus + ll + C(region) + loc + I(loc**2)")]
    R = []
    for nm, rhs in steps:
        r = smf.ols(f"day24_pk ~ C(g) {rhs}", d).fit(cov_type="HC3")
        for gk in "BCD":
            t = f"C(g)[T.{gk}]"
            R.append(dict(adjusted_for=nm, group=gk, coef=r.params[t], lo=r.conf_int().loc[t, 0], hi=r.conf_int().loc[t, 1], n=int(r.nobs)))
    pd.DataFrame(R).round(3).to_csv(f"{a.out}/day24_stepwise.csv", index=False)
    d["imdq"] = pd.qcut(d.imd_score, 5, labels=[1, 2, 3, 4, 5])
    d.groupby(["imdq", "g"], observed=True).day24_pk.agg(["median", "size"]).unstack().round(2).to_csv(f"{a.out}/day24_by_imd_quintile.csv")
except ImportError:
    print("statsmodels not installed; skipping models")
