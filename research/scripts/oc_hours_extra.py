#!/usr/bin/env python3
"""
Follow-ups to oc_hours_rush.py (OC Hours page):
  1. 8-10am workload by day of week, with out-of-hours OC assigned to the morning it is handled
  2. Phone answering by OC-hours group (CBT, same month)
  3. GP Patient Survey 2026 by OC-hours group, groups classified on March 2026 OC (fieldwork Jan-Apr 2026)

    python research/scripts/oc_hours_extra.py --groups research/data/oc_hours_sep26/practice_groups.csv \
        --oc research/data/oc_daytime_sep26.zip --cbt research/data/cbt_daytime_sep26.zip \
        --oc-gpps research/data/panel/oc_daytime_2026-03.parquet --out research/data/oc_hours_sep26
"""
import argparse, io, os, zipfile
import numpy as np, pandas as pd
import statsmodels.formula.api as smf

p = argparse.ArgumentParser()
p.add_argument("--groups", required=True)
p.add_argument("--oc", required=True)
p.add_argument("--cbt", required=True)
p.add_argument("--oc-gpps", required=True, help="OC day/time panel parquet for the month used to classify practices for GPPS")
p.add_argument("--xsec", default="research/data/xsec_master_2026.parquet")
p.add_argument("--list", default="research/data/list_jul26.csv")
p.add_argument("--out", required=True)
p.add_argument("--gpad", default=None, help="GPAD 'Practice Level Crosstab' zip; uses the files for the OC month")
p.add_argument("--gpad-month", default=None, help="month tag in the crosstab filenames, e.g. Sep_26")
a = p.parse_args()
NAMES = {"A": "Core hours only", "B": "Weekday early/late", "C": "24/7 admin only", "D": "24/7 incl. clinical"}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri"]

def zcsv(path, cols):
    fr = []
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.lower().endswith(".csv") and "unmapped" not in n.lower():
                fr.append(pd.read_csv(io.BytesIO(z.read(n)), usecols=cols))
    return pd.concat(fr, ignore_index=True)

M = pd.read_csv(a.groups).set_index("gp_code")
X = pd.read_parquet(a.xsec).set_index("gp_code")

# ------------------------------------------------ 1. day-of-week 8-10am workload
oc = zcsv(a.oc, ["DATE", "GP_CODE", "SUBMISSION_TIME", "TOTAL"])
oc = oc[oc.GP_CODE.isin(M.index)]
oc["d"] = pd.to_datetime(oc.DATE)
month_days = pd.date_range(oc.d.min(), oc.d.max())
wdays = month_days[month_days.dayofweek < 5]
# the working day on which each submission is handled, and whether it lands in the 8-10am window
early = oc.SUBMISSION_TIME.isin(["00:00 - 05:59", "06:00 - 06:59", "07:00 - 07:59"])
late = oc.SUBMISSION_TIME == "18:30 - 23:59"
r810 = oc.SUBMISSION_TIME.isin(["08:00 - 08:59", "09:00 - 09:59"])
wk = oc.d.dt.dayofweek >= 5
oc["hday"] = oc.d                                                        # core hours and before 8am: same day
oc.loc[wk, "hday"] = oc.loc[wk, "d"] + pd.offsets.Week(weekday=0)         # Sat/Sun -> following Monday
oc.loc[late & ~wk, "hday"] = oc.loc[late & ~wk, "d"] + pd.offsets.BDay(1)  # weekday evening -> next weekday
oc["hday"] = pd.to_datetime(oc.hday)
oc["at810"] = r810 | early | late | wk
first = wdays.min()
# a handling day is complete only if its whole queue falls inside the month: drop the first weekday
# (its queue started last month) and days outside the month
valid = wdays[wdays > first]
oc = oc[oc.hday.isin(valid)]
o = oc.groupby(["GP_CODE", "hday"]).apply(lambda g: pd.Series({"oc_810": g.TOTAL[g.at810].sum(), "oc_day": g.TOTAL.sum()}), include_groups=False)

cb = zcsv(a.cbt, ["Date", "PRACTICE_CODE", "Indicator", "Time_Category", "Value"])
cb = cb[cb.PRACTICE_CODE.isin(M.index)]
cb["d"] = pd.to_datetime(cb.Date)
cb["tc"] = cb.Time_Category.str.replace(" ", "")
CORE = ["08:00-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:59", "16:00-17:59", "18:00-18:29"]
ci = cb[(cb.Indicator == "CBT001") & cb.tc.isin(CORE) & cb.d.isin(valid)]
c = ci.groupby(["PRACTICE_CODE", "d"]).apply(lambda g: pd.Series({"ph_810": g.Value[g.tc == CORE[0]].sum(), "ph_day": g.Value.sum()}), include_groups=False)
c.index.names = ["GP_CODE", "hday"]
idx = pd.MultiIndex.from_product([M.index, valid], names=["GP_CODE", "hday"])
D = pd.concat([o, c], axis=1).reindex(idx).fillna(0).reset_index()
D["dow"] = D.hday.dt.dayofweek
P = D.groupby(["GP_CODE", "dow"])[["oc_810", "oc_day", "ph_810", "ph_day"]].mean().reset_index()
P = P.join(M[["g", "list"]], on="GP_CODE")
P["load_810_pk"] = (P.oc_810 + P.ph_810) / P.list * 1000
P["share_810"] = (P.oc_810 + P.ph_810) / (P.oc_day + P.ph_day)
dowt = P.groupby(["g", "dow"]).agg(load_810_pk=("load_810_pk", "median"), share_810=("share_810", "median")).reset_index()
dowt["dow"] = dowt.dow.map(dict(enumerate(DOW)))
dowt.round(4).to_csv(f"{a.out}/dow_810_workload.csv", index=False)
print(f"handling days used: {len(valid)} ({valid.min():%d %b}-{valid.max():%d %b})")
print(dowt.pivot(index="dow", columns="g", values=["load_810_pk", "share_810"]).reindex(DOW).round(3).to_string())

# ------------------------------------------------ 2. phone answering
cc = cb[cb.tc.isin(CORE) & (cb.d.dt.dayofweek < 5)]
w = cc.pivot_table(index="PRACTICE_CODE", columns="Indicator", values="Value", aggfunc="sum")
w8 = cc[cc.tc == CORE[0]].pivot_table(index="PRACTICE_CODE", columns="Indicator", values="Value", aggfunc="sum")
ph = pd.DataFrame({"answer_rate": w.CBT003 / w.CBT001, "ivr_share": w.CBT002 / w.CBT001,
                   "answer_rate_810": w8.CBT003 / w8.CBT001,
                   "answer_rate_excl_ivr": w.CBT003 / (w.CBT001 - w.CBT002)})
ph = ph[(w.CBT001 >= 200)].clip(upper=1)
Q = M.join(ph, how="inner").join(X[["phone_easy_2026", "access_satisfaction_2026", "satisfaction_2026", "couldnt_contact_2026", "gpps_n_2026"]])
Q["loc"] = np.log(Q.oc_core_pk.clip(lower=.1)); Q["ll"] = np.log(Q.list)
Q["calls_pk"] = Q.calls_core_pk
res = []
def models(df, ys, tag, extra=""):
    d = df.dropna(subset=["imd_score", "pct65plus", "region"])
    for y in ys:
        dd = d.dropna(subset=[y])
        med = dd.groupby("g")[y].median()
        for spec, rhs in [("unadjusted", ""), ("adjusted", f"+ imd_score + pct65plus + ll + C(region) + loc + I(loc**2){extra}")]:
            r = smf.ols(f"{y} ~ C(g) {rhs}", dd).fit(cov_type="HC3")
            for gk in "BCD":
                t = f"C(g)[T.{gk}]"
                res.append(dict(analysis=tag, outcome=y, spec=spec, group=gk, coef=r.params[t], lo=r.conf_int().loc[t, 0],
                                hi=r.conf_int().loc[t, 1], p=r.pvalues[t], n=int(r.nobs), median_A=med.get("A"), median_g=med.get(gk)))
models(Q, ["answer_rate", "answer_rate_810", "ivr_share", "answer_rate_excl_ivr"], "phone (Sep 2026)", "+ np.log(calls_pk)")
print("\nphone medians"); print(Q.groupby("g")[["answer_rate", "answer_rate_810", "ivr_share", "answer_rate_excl_ivr"]].median().round(3))

# ------------------------------------------------ 3. GPPS 2026, groups from the fieldwork period
g3 = pd.read_parquet(a.oc_gpps)
g3["wk"] = g3.date.dt.dayofweek >= 5
nwd = g3.loc[~g3.wk, "date"].nunique(); nwe = g3.loc[g3.wk, "date"].nunique()
night = (~g3.wk) & g3.band.isin(["18:30 - 23:59", "00:00 - 05:59", "06:00 - 06:59", "07:00 - 07:59"])
core = (~g3.wk) & ~night
G = pd.DataFrame({"tot": g3.groupby("gp_code").TOTAL.sum()})
G["core"] = g3[core].groupby("gp_code").TOTAL.sum(); G["core_cl"] = g3[core].groupby("gp_code").CLINICAL.sum()
G["wkend_days"] = g3[g3.wk & (g3.TOTAL > 0)].groupby("gp_code").date.nunique()
G["night_days"] = g3[night & (g3.TOTAL > 0)].groupby("gp_code").date.nunique()
G["wkend_cl_days"] = g3[g3.wk & (g3.CLINICAL > 0)].groupby("gp_code").date.nunique()
G = G.fillna(0)
def grp(r):
    if r.tot < 300: return None
    if r.wkend_days == 0 and r.night_days <= 3: return "A"
    if r.wkend_days <= 1 and r.night_days >= 0.8 * nwd: return "B"
    if r.wkend_days >= 0.85 * nwe and r.night_days >= 0.8 * nwd:
        if r.wkend_cl_days >= 0.75 * nwe: return "D"
        if r.wkend_cl_days <= 1 and r.core and r.core_cl / r.core >= 0.3: return "C"
    return None
G["g"] = G.apply(grp, axis=1)
L = pd.read_csv(a.list).set_index("gp_code").iloc[:, 0].rename("list")
S = G[G.g.notna()].join(L).join(X[["imd_score", "pct65plus", "region", "phone_easy_2026", "access_satisfaction_2026",
                                   "satisfaction_2026", "couldnt_contact_2026", "gpps_n_2026"]])
S = S[S.list.notna()]
S["oc_core_pk"] = S.core / nwd / S.list * 1000
S["loc"] = np.log(S.oc_core_pk.clip(lower=.1)); S["ll"] = np.log(S.list)
print(f"\nGPPS classification month: {g3.date.min():%Y-%m}; {nwd} weekdays, {nwe} weekend days")
print(S.g.value_counts().sort_index().to_dict())
print("stability vs Sep groups:"); print(pd.crosstab(S.g, M.g.reindex(S.index).fillna("-"), margins=True))
ys = ["satisfaction_2026", "access_satisfaction_2026", "phone_easy_2026", "couldnt_contact_2026"]
print(S.groupby("g")[ys].median().round(1))
models(S, ys, "GPPS 2026 (groups from Mar 2026 OC)")
R = pd.DataFrame(res).round(4); R.to_csv(f"{a.out}/phone_gpps_models.csv", index=False)
print(R[R.group == "D"][["analysis", "outcome", "spec", "coef", "lo", "hi", "n", "median_A", "median_g"]].to_string())

# ------------------------------------------------ 4. appointments (GPAD), same month as the OC groups
if a.gpad:
    import duckdb
    tmp = os.path.join(a.out, "_gpad_tmp"); os.makedirs(tmp, exist_ok=True)
    with zipfile.ZipFile(a.gpad) as z:
        names = [n for n in z.namelist() if a.gpad_month in n and n.lower().endswith(".csv")]
        for n in names: z.extract(n, tmp)
    files = [os.path.join(tmp, n) for n in names]
    print(f"\nGPAD files: {names}")
    q = f"""
    SELECT GP_CODE AS gp_code, SUM(n) AS total,
      SUM(CASE WHEN TIME_BETWEEN_BOOK_AND_APPT='Same Day' THEN n ELSE 0 END) AS same_day,
      SUM(CASE WHEN HCP_TYPE='GP' THEN n ELSE 0 END) AS gp,
      SUM(CASE WHEN HCP_TYPE='GP' AND TIME_BETWEEN_BOOK_AND_APPT='Same Day' THEN n ELSE 0 END) AS gp_same_day,
      SUM(CASE WHEN APPT_MODE='Face-to-Face' THEN n ELSE 0 END) AS f2f
    FROM (SELECT GP_CODE, HCP_TYPE, APPT_MODE, TIME_BETWEEN_BOOK_AND_APPT, TRY_CAST(COUNT_OF_APPOINTMENTS AS BIGINT) AS n
          FROM read_csv({files!r}, header=true, all_varchar=true))
    WHERE n IS NOT NULL GROUP BY 1"""
    ap = duckdb.sql(q).df().set_index("gp_code")
    for f in files: os.remove(f)
    A = M.join(ap, how="inner")
    A = A[A.total >= 200].copy()
    A["sd_pct"] = A.same_day / A.total * 100
    A["gp_sd_pct"] = A.gp_same_day / A.gp.replace(0, np.nan) * 100
    A["appts_pk"] = A.total / A.list * 1000
    A["sd_pk"] = A.same_day / A.list * 1000
    A["gp_pk"] = A.gp / A.list * 1000
    A["f2f_pct"] = A.f2f / A.total * 100
    A["loc"] = np.log(A.oc_core_pk.clip(lower=.1)); A["ll"] = np.log(A.list)
    ys = ["sd_pct", "gp_sd_pct", "appts_pk", "sd_pk", "gp_pk", "f2f_pct"]
    med = A.groupby("g")[ys].median().round(2); med["n"] = A.g.value_counts()
    med.to_csv(f"{a.out}/appointments_by_group.csv")
    print(med)
    d = A.dropna(subset=["imd_score", "pct65plus", "region"])
    R = []
    for y in ys:
        for spec, rhs in [("unadjusted", ""), ("adjusted", "+ imd_score + pct65plus + ll + C(region)"),
                          ("adjusted + OC volume", "+ imd_score + pct65plus + ll + C(region) + loc + I(loc**2)")]:
            dd = d.dropna(subset=[y]); r = smf.ols(f"{y} ~ C(g) {rhs}", dd).fit(cov_type="HC3")
            for gk in "BCD":
                t = f"C(g)[T.{gk}]"
                R.append(dict(outcome=y, spec=spec, group=gk, coef=r.params[t], lo=r.conf_int().loc[t, 0], hi=r.conf_int().loc[t, 1], n=int(r.nobs)))
    R = pd.DataFrame(R).round(3); R.to_csv(f"{a.out}/appointments_models.csv", index=False)
    print(R[R.group == "D"].to_string())
