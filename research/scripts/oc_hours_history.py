#!/usr/bin/env python3
"""
Long-run history of OC opening patterns (2024 onwards), using a rule that works on both the
old (weekday x 2-hour band, month totals, no clinical split; to ~2025) and new (daily, hourly,
clinical/admin; Dec 2025 on) OC 'By Day and Time' files.

Harmonised measures per practice-month (OC submissions):
  wkend_share  = weekend / all
  night_share  = weekday 00:00-07:59 / all   (old bands 00-06 + 06-08; new 00-06,06-07,07-08)
  late_share   = weekday 18:00-23:59 / all   (old band includes 18:00-18:29, so new files are collapsed the same way)
  r810_share   = weekday 08:00-09:59 / weekday 08:00-17:59
Harmonised groups (practices with >=300 submissions):
  'core'  : wkend_share < 0.2% and night_share < 0.5%
  '24/7'  : wkend_share >= 1.5% and night_share >= 1%   (cannot split clinical/admin before Dec 2025)
  other   : everything else (incl. early/late weekday)
Thresholds are checked against the full new-format rules on January 2026.

    python research/scripts/oc_hours_history.py --old research/data/oc_daytime_apr-jun24.zip \
        research/data/oc_daytime_jan25.zip --out research/data/oc_hours_sep26
"""
import argparse, glob, io, os, zipfile
import numpy as np, pandas as pd

p = argparse.ArgumentParser()
p.add_argument("--old", nargs="+", required=True, help="old-format OC csv/zip files (MONTH, WEEKDAY, SUBMISSION_TIME, VALUE)")
p.add_argument("--panel", default="research/data/panel")
p.add_argument("--oc-sep", default="research/data/oc_daytime_sep26.zip")
p.add_argument("--groups", default="research/data/oc_hours_sep26/monthly_groups.csv")
p.add_argument("--out", required=True)
a = p.parse_args()
WKD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def read_old(path):
    fr = []
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                if n.lower().endswith(".csv"): fr.append(pd.read_csv(io.BytesIO(z.read(n))))
    else: fr.append(pd.read_csv(path))
    d = pd.concat(fr)
    out = {}
    for m, g in d.groupby(d.MONTH.astype(str).str[:7]):
        g = g[g.SUBMISSION_TIME != "Unknown"]
        out[m] = harmon(g.GP_CODE, g.WEEKDAY.isin(WKD), g.SUBMISSION_TIME, g.VALUE)
    return out

def harmon(gp, is_wkd, band, val):
    b = band.str.replace(" ", "")
    night = is_wkd & b.isin(["00:00-05:59", "06:00-07:59", "06:00-06:59", "07:00-07:59"])
    late = is_wkd & b.isin(["18:00-23:59", "18:00-18:29", "18:30-23:59"])
    r810 = is_wkd & b.isin(["08:00-09:59", "08:00-08:59", "09:00-09:59"])
    day = is_wkd & ~night & ~late
    df = pd.DataFrame({"gp": gp.values, "v": val.values, "wk": (~is_wkd).values, "night": night.values, "late": late.values, "r810": r810.values, "day": day.values})
    G = pd.DataFrame({"tot": df.groupby("gp").v.sum()})
    for k in ["wk", "night", "late", "r810", "day"]:
        G[k] = df[df[k]].groupby("gp").v.sum()
    G = G.fillna(0)
    G["wkend_share"] = G.wk / G.tot; G["night_share"] = G.night / G.tot; G["late_share"] = G.late / G.tot
    G["r810_share"] = G.r810 / G.day.replace(0, np.nan)
    G["h"] = np.select([G.tot < 300, (G.wkend_share < .002) & (G.night_share < .005), (G.wkend_share >= .015) & (G.night_share >= .01)],
                       [None, "core", "24/7"], default="other")
    G.loc[G.tot < 300, "h"] = None
    return G

def read_new(d):
    d = d.rename(columns={"GP_CODE": "gp_code", "DATE": "date", "SUBMISSION_TIME": "band"})
    d["date"] = pd.to_datetime(d.date)
    return harmon(d.gp_code, d.date.dt.dayofweek < 5, d.band, d.TOTAL)

H = {}
for f in a.old: H.update(read_old(f))
for f in sorted(glob.glob(f"{a.panel}/oc_daytime_*.parquet")):
    d = pd.read_parquet(f, columns=["gp_code", "date", "band", "TOTAL"]).rename(columns={"gp_code": "GP_CODE", "date": "DATE", "band": "SUBMISSION_TIME"})
    H[d.DATE.dt.strftime("%Y-%m").iloc[0]] = read_new(d)
fr = []
with zipfile.ZipFile(a.oc_sep) as z:
    for n in z.namelist():
        if n.lower().endswith(".csv"): fr.append(pd.read_csv(io.BytesIO(z.read(n)), usecols=["DATE", "GP_CODE", "SUBMISSION_TIME", "TOTAL"]))
H["2026-09"] = read_new(pd.concat(fr))
months = sorted(H)
print("months:", months)

# calibration against full rules
full = pd.read_csv(a.groups, index_col=0)
for m in ["2026-01", "2026-09"]:
    x = pd.DataFrame({"full": full[m], "harm": H[m].h}).dropna()
    print(f"\ncalibration {m} (rows = full rules, cols = harmonised):"); print(pd.crosstab(x.full, x.harm))

hg = pd.DataFrame({m: H[m].h for m in months})
hg.to_csv(f"{a.out}/history_groups.csv")
print("\npractices per harmonised group:"); print(hg.apply(lambda s: s.value_counts()).fillna(0).astype(int).to_string())

# trajectories of September's 24/7-clinical practices
D = full.index[full["2026-09"] == "D"]
print(f"\nSeptember 24/7 clinical practices (n={len(D)}): harmonised group in each month")
print(hg.reindex(D).apply(lambda s: s.value_counts(dropna=False)).fillna(0).astype(int).to_string())
traj = hg.reindex(D)
first24 = traj.apply(lambda r: next((m for m in months if r[m] == "24/7"), None), axis=1)
print("first month seen open 24/7:", first24.value_counts().sort_index().to_dict())

# national share of practices open 24/7, and 8-10am share, by month
S = pd.DataFrame({m: {"n_classified": H[m].h.notna().sum(), "pct_core": (H[m].h == "core").mean() * 100 / H[m].h.notna().mean(),
                      "pct_24_7": (H[m].h == "24/7").mean() * 100 / H[m].h.notna().mean(),
                      "wkend_share_all": H[m].wk.sum() / H[m].tot.sum() * 100,
                      "r810_share_all": H[m].r810.sum() / H[m].day.sum() * 100} for m in months}).T.round(1)
S.to_csv(f"{a.out}/history_national.csv"); print("\nnational:"); print(S.to_string())

# switchers: practices that changed between core and 24/7 across the long run, and their 8-10am share before/after
rows = []
for gp, r in hg.iterrows():
    seq = [(m, r[m]) for m in months if isinstance(r[m], str)]
    for (m1, g1), (m2, g2) in zip(seq, seq[1:]):
        if {g1, g2} == {"core", "24/7"}:
            rows.append(dict(gp=gp, from_m=m1, to_m=m2, frm=g1, to=g2,
                             r810_before=H[m1].r810_share.get(gp), r810_after=H[m2].r810_share.get(gp)))
Sw = pd.DataFrame(rows); Sw.to_csv(f"{a.out}/history_switches.csv", index=False)
if len(Sw):
    Sw["change"] = Sw.r810_after - Sw.r810_before
    print("\nswitches between core-hours-only and 24/7 (consecutive available months):")
    print(Sw.groupby(["frm", "to"]).agg(n=("gp", "size"), practices=("gp", "nunique"), r810_before=("r810_before", "median"), r810_after=("r810_after", "median"), change=("change", "median")).round(3))
    # comparison: practices staying core across the same month pairs
    comp = []
    for (m1, m2), g in Sw.groupby(["from_m", "to_m"]):
        st = hg.index[(hg[m1] == "core") & (hg[m2] == "core")]
        comp.append(dict(from_m=m1, to_m=m2, n_switch=len(g), stay_core_change=(H[m2].r810_share.reindex(st) - H[m1].r810_share.reindex(st)).median()))
    print(pd.DataFrame(comp).round(3).to_string())

# difference in differences for each switch: change in 8-10am share minus the median change among
# practices that stayed in the starting group over the same pair of months
if len(Sw):
    did = []
    for _, s in Sw.iterrows():
        st = hg.index[(hg[s.from_m] == s.frm) & (hg[s.to_m] == s.frm)]
        base = (H[s.to_m].r810_share.reindex(st) - H[s.from_m].r810_share.reindex(st)).median()
        did.append(dict(gp=s.gp, frm=s.frm, to=s.to, from_m=s.from_m, to_m=s.to_m, change=s.r810_after - s.r810_before, stayers_change=base, n_stayers=len(st)))
    Dd = pd.DataFrame(did); Dd["did"] = Dd.change - Dd.stayers_change
    Dd.to_csv(f"{a.out}/history_switches_did.csv", index=False)
    import statsmodels.api as sm
    print("\nswitch effect on 8-10am share of weekday daytime OC (change minus stayers' change):")
    for (f, t), g in Dd.groupby(["frm", "to"]):
        g = g.dropna(subset=["did"])
        r = sm.OLS(g.did.values, np.ones(len(g))).fit(cov_type="HC3")
        print(f"  {f} -> {t}: n={len(g)}  median {g.did.median():+.3f}  mean {r.params[0]:+.3f} (95% CI {r.conf_int()[0][0]:+.3f} to {r.conf_int()[0][1]:+.3f})")
    print("  by period:"); print(Dd.groupby(["frm", "to", Dd.from_m.str[:4] + "->" + Dd.to_m.str[:4]]).did.agg(["size", "median"]).round(3).to_string())

# ---------------------------------------------------------------- telephony for the switchers
# monthly calls: cbt_rush_panel.csv (Oct 2024 - May 2026) + daily panel (Jun 2026) + Sep 2026 zip
def wd_count(m):
    d = pd.date_range(m + "-01", periods=1, freq="MS")[0]
    days = pd.date_range(d, d + pd.offsets.MonthEnd(0))
    return int((days.dayofweek < 5).sum())
T = {}
rp = pd.read_csv("research/data/cbt_rush_panel.csv")
for m, g in rp.groupby("month"):
    T[m] = g.set_index("gp_code")[["inbound_wd", "inbound_wd_810"]]
f = f"{a.panel}/cbt_daytime_2026-06.parquet"
if os.path.exists(f) and "2026-06" not in T:
    x = pd.read_parquet(f, columns=["gp_code", "date", "band", "inbound"]); x = x[x.date.dt.dayofweek < 5]
    T["2026-06"] = pd.DataFrame({"inbound_wd": x.groupby("gp_code").inbound.sum(), "inbound_wd_810": x[x.band == "08:00-09:59"].groupby("gp_code").inbound.sum()})
cbt_sep = "research/data/cbt_daytime_sep26.zip"
if os.path.exists(cbt_sep):
    fr = []
    with zipfile.ZipFile(cbt_sep) as z:
        for n in z.namelist():
            if n.lower().endswith(".csv") and "unmapped" not in n.lower():
                x = pd.read_csv(io.BytesIO(z.read(n)), usecols=["Date", "PRACTICE_CODE", "Indicator", "Time_Category", "Value"]); fr.append(x[x.Indicator == "CBT001"])
    x = pd.concat(fr); x["Date"] = pd.to_datetime(x.Date); x = x[x.Date.dt.dayofweek < 5]
    T["2026-09"] = pd.DataFrame({"inbound_wd": x.groupby("PRACTICE_CODE").Value.sum(), "inbound_wd_810": x[x.Time_Category.str.replace(" ", "") == "08:00-09:59"].groupby("PRACTICE_CODE").Value.sum()})
Lst = pd.read_csv("research/data/list_jul26.csv").set_index("gp_code").iloc[:, 0]

def outcomes(m):
    if m not in T: return None
    O = H[m][["tot", "wk", "r810"]].join(T[m], how="inner")
    O = O[O.inbound_wd >= 500]
    O["oc_wd"] = O.tot - O.wk
    nwd = wd_count(m); L = Lst.reindex(O.index)
    O["ph_rush"] = O.inbound_wd_810 / O.inbound_wd
    O["comb_rush"] = (O.inbound_wd_810 + O.r810) / (O.inbound_wd + O.oc_wd)
    O["calls_pk"] = O.inbound_wd / nwd / L * 1000
    O["oc_pk"] = O.tot / nwd / L * 1000          # all OC (incl. weekend) per weekday, per 1,000
    O["contacts_pk"] = (O.inbound_wd + O.tot) / nwd / L * 1000
    O["oc_share"] = O.tot / (O.tot + O.inbound_wd)
    return O
OUT = {m: outcomes(m) for m in months}
ys = ["ph_rush", "comb_rush", "calls_pk", "oc_pk", "contacts_pk", "oc_share"]
res = []
if len(Sw):
    for _, s in Sw.iterrows():
        A_, B_ = OUT.get(s.from_m), OUT.get(s.to_m)
        if A_ is None or B_ is None or s.gp not in A_.index or s.gp not in B_.index: continue
        st = hg.index[(hg[s.from_m] == s.frm) & (hg[s.to_m] == s.frm)]
        st = st[st.isin(A_.index) & st.isin(B_.index)]
        row = dict(gp=s.gp, frm=s.frm, to=s.to, from_m=s.from_m, to_m=s.to_m, n_stayers=len(st))
        for y in ys:
            row[y + "_before"] = A_.at[s.gp, y]; row[y + "_after"] = B_.at[s.gp, y]
            row[y + "_did"] = (B_.at[s.gp, y] - A_.at[s.gp, y]) - (B_.loc[st, y] - A_.loc[st, y]).median()
        res.append(row)
P = pd.DataFrame(res); P.to_csv(f"{a.out}/history_switches_phone.csv", index=False)
print("\nswitchers with telephony in both months:", P.groupby(["frm", "to"]).size().to_dict())
import statsmodels.api as sm
summ = []
for (f_, t_), g in P.groupby(["frm", "to"]):
    for y in ys:
        v = g[y + "_did"].dropna()
        if len(v) < 5: continue
        r = sm.OLS(v.values, np.ones(len(v))).fit(cov_type="HC3")
        summ.append(dict(change=f"{f_} -> {t_}", outcome=y, n=len(v), before=g[y + "_before"].median(), after=g[y + "_after"].median(),
                         effect_median=v.median(), effect_mean=r.params[0], lo=r.conf_int()[0][0], hi=r.conf_int()[0][1]))
S2 = pd.DataFrame(summ).round(4); S2.to_csv(f"{a.out}/history_switches_phone_summary.csv", index=False)
print(S2.to_string())
