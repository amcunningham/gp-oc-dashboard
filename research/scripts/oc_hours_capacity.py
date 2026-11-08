#!/usr/bin/env python3
"""
oc_hours_capacity.py -- does the size of the 8am peak relate to appointment capacity?

All practices with September 2026 OC, telephony and appointments data (not only the four OC-hours
groups). For each practice: share of weekday core-hours calls + OC arriving 08:00-09:59 ("comb_rush")
and calls only ("ph_rush"); appointments per 1,000 (GPAD Sep 2026), same-day share, appointments booked
ahead (not same day) per 1,000, GPs per 10,000 (xsec_master_2026). OC times corrected and UTC-shifted
call practices dropped as elsewhere (oc_timefix.py).

Outputs (in --out):
  capacity_rush_practice.csv   practice-level measures
  capacity_quintiles.csv       medians by fifth of booked-ahead appointments, total appointments, GPs per 10k
  capacity_models.csv          OLS (HC3), points of 8-10am share per SD of each capacity measure,
                               unadjusted and adjusted for IMD, % 65+, log list, region, contact volume, OC share

Usage:
  python research/scripts/oc_hours_capacity.py --oc research/data/oc_daytime_sep26.zip \
      --cbt research/data/cbt_daytime_sep26.zip --gpad research/data/gpad_crosstab_sep26.zip \
      --gpad-month Sep_26 --out research/data/oc_hours_sep26
"""
import argparse, io, os, sys, zipfile
import numpy as np, pandas as pd, duckdb
import statsmodels.formula.api as smf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oc_timefix

p = argparse.ArgumentParser()
p.add_argument("--oc", required=True)
p.add_argument("--cbt", required=True)
p.add_argument("--gpad", required=True)
p.add_argument("--gpad-month", default="Sep_26")
p.add_argument("--list", default="research/data/list_jul26.csv")
p.add_argument("--xsec", default="research/data/xsec_master_2026.csv")
p.add_argument("--out", default="research/data/oc_hours_sep26")
a = p.parse_args()
os.makedirs(a.out, exist_ok=True)

CORE_OC = ["08:00 - 08:59", "09:00 - 09:59", "10:00 - 10:59", "11:00 - 11:59", "12:00 - 12:59", "13:00 - 13:59",
           "14:00 - 14:59", "15:00 - 15:59", "16:00 - 16:59", "17:00 - 17:59", "18:00 - 18:29"]
CORE_CBT = ["08:00-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:59", "16:00-17:59", "18:00-18:29"]

# OC, weekday core hours
fr = []
with zipfile.ZipFile(a.oc) as z:
    for n in z.namelist():
        if n.lower().endswith(".csv"):
            fr.append(pd.read_csv(io.BytesIO(z.read(n)), usecols=["DATE", "GP_CODE", "SUPPLIER", "SUBMISSION_TIME", "TOTAL"]))
oc = pd.concat(fr, ignore_index=True)
oc["d"] = pd.to_datetime(oc.DATE)
sup = oc.drop_duplicates("GP_CODE").set_index("GP_CODE").SUPPLIER.fillna("").str.upper()
oc = oc_timefix.fix(oc, sup, gp="GP_CODE", date="d", band="SUBMISSION_TIME", vals=("TOTAL",), label="OC")
oc = oc[oc.d.dt.dayofweek < 5]
wd = oc.d.nunique()
c = oc[oc.SUBMISSION_TIME.isin(CORE_OC)]
P = pd.DataFrame({"oc_core": c.groupby("GP_CODE").TOTAL.sum(),
                  "oc_810": c[c.SUBMISSION_TIME.isin(CORE_OC[:2])].groupby("GP_CODE").TOTAL.sum()}).fillna(0)

# calls, weekday core hours
fr = []
with zipfile.ZipFile(a.cbt) as z:
    for n in z.namelist():
        if n.lower().endswith(".csv") and "unmapped" not in n.lower():
            x = pd.read_csv(io.BytesIO(z.read(n)), usecols=["Date", "PRACTICE_CODE", "Indicator", "Time_Category", "Value"])
            fr.append(x[x.Indicator == "CBT001"])
cb = pd.concat(fr, ignore_index=True)
cb["Date"] = pd.to_datetime(cb.Date)
utc = oc_timefix.cbt_utc_practices(cb, gp="PRACTICE_CODE", date="Date", band="Time_Category", val="Value", label="calls")
cb = cb[(cb.Date.dt.dayofweek < 5) & ~cb.PRACTICE_CODE.isin(utc)]
cb["tc"] = cb.Time_Category.str.replace(" ", "")
cc = cb[cb.tc.isin(CORE_CBT)]
P = P.join(pd.DataFrame({"calls_core": cc.groupby("PRACTICE_CODE").Value.sum(),
                         "calls_810": cc[cc.tc == CORE_CBT[0]].groupby("PRACTICE_CODE").Value.sum()}), how="inner")

# appointments
tmp = os.path.join(a.out, "_gpad_tmp"); os.makedirs(tmp, exist_ok=True)
with zipfile.ZipFile(a.gpad) as z:
    names = [n for n in z.namelist() if a.gpad_month in n and n.lower().endswith(".csv")]
    for n in names: z.extract(n, tmp)
files = [os.path.join(tmp, n) for n in names]
ap = duckdb.sql(f"""
  SELECT GP_CODE AS gp, SUM(n) AS total,
         SUM(CASE WHEN TIME_BETWEEN_BOOK_AND_APPT='Same Day' THEN n ELSE 0 END) AS same_day
  FROM (SELECT GP_CODE, TIME_BETWEEN_BOOK_AND_APPT, TRY_CAST(COUNT_OF_APPOINTMENTS AS BIGINT) AS n
        FROM read_csv({files!r}, header=true, all_varchar=true))
  WHERE n IS NOT NULL GROUP BY 1""").df().set_index("gp")
for f in files: os.remove(f)

L = pd.read_csv(a.list).set_index("gp_code").iloc[:, 0].rename("list")
X = pd.read_csv(a.xsec).set_index("gp_code")[["imd_score", "pct65plus", "region", "gp_per10k"]]
D = P.join(ap, how="inner").join(L, how="inner").join(X, how="inner")
D = D[(D.total >= 200) & (D.calls_core >= 500) & (D.list >= 1000)].copy()
k = 1000 / D.list
D["comb_rush"] = (D.calls_810 + D.oc_810) / (D.calls_core + D.oc_core)
D["ph_rush"] = D.calls_810 / D.calls_core
D["appts_pk"] = D.total * k
D["sd_pct"] = D.same_day / D.total * 100
D["booked_ahead_pk"] = (D.total - D.same_day) * k
D["contacts_pk"] = (D.calls_core + D.oc_core) / wd * k
D["oc_share"] = D.oc_core / (D.calls_core + D.oc_core)
D["ll"] = np.log(D.list)
D = D[D.appts_pk.between(100, 1500) & D.contacts_pk.between(3, 150)]
D.index.name = "gp_code"
D.to_csv(f"{a.out}/capacity_rush_practice.csv")
print(f"practices: {len(D)}")

Q = []
for var, lab in [("booked_ahead_pk", "Appointments booked ahead per 1,000"), ("appts_pk", "Appointments per 1,000"),
                 ("gp_per10k", "GPs per 10,000")]:
    s = D.dropna(subset=[var])
    q = pd.qcut(s[var].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    g = s.groupby(q, observed=True).agg(value=(var, "median"), comb_rush=("comb_rush", "median"), ph_rush=("ph_rush", "median"),
                                        sd_pct=("sd_pct", "median"), n=(var, "size")).reset_index(names="fifth")
    g.insert(0, "measure", lab); Q.append(g)
Q = pd.concat(Q).round(4)
Q.to_csv(f"{a.out}/capacity_quintiles.csv", index=False)
print(Q.to_string())

d = D.dropna(subset=["imd_score", "pct65plus", "region", "gp_per10k"]).copy()
d["cr"] = d.comb_rush * 100; d["pr"] = d.ph_rush * 100
for v in ["appts_pk", "booked_ahead_pk", "sd_pct", "gp_per10k", "contacts_pk", "oc_share"]:
    d["z_" + v] = (d[v] - d[v].mean()) / d[v].std()
ADJ = "+ imd_score + pct65plus + ll + C(region) + z_contacts_pk + z_oc_share"
R = []
for y, ylab in [("cr", "calls + OC"), ("pr", "calls only")]:
    for spec, rhs in [("appointments", "z_appts_pk"), ("booked ahead + same-day share", "z_booked_ahead_pk + z_sd_pct"),
                      ("appointments + same-day share + GPs", "z_appts_pk + z_sd_pct + z_gp_per10k")]:
        for adj in ["unadjusted", "adjusted"]:
            r = smf.ols(f"{y} ~ {rhs} {ADJ if adj == 'adjusted' else ''}", d).fit(cov_type="HC3")
            for t in [x.strip() for x in rhs.split("+")]:
                R.append(dict(outcome=ylab, model=spec, spec=adj, term=t[2:], sd=d[t[2:]].std(), coef=r.params[t],
                              lo=r.conf_int().loc[t, 0], hi=r.conf_int().loc[t, 1], n=int(r.nobs), r2=r.rsquared))
R = pd.DataFrame(R).round(3)
R.to_csv(f"{a.out}/capacity_models.csv", index=False)
print(R.to_string())
