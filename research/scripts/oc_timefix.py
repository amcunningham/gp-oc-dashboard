"""
Correct OC submission times for suppliers that report in UTC during British Summer Time.

Found Nov 2026: Continuum Health (Anima) practices' weekday OC peak moves from 8-9am to 7-8am on the
exact day the clocks change (29 March 2026), and late-afternoon submissions shift an hour earlier, i.e.
times are recorded in UTC, not UK clock time. eConsult does the same in some months (Apr-Jun 2024,
Sep 2026) but not others (Apr-Jun 2026). So detection is done per supplier and month from the data:
a supplier-month is flagged when, on BST weekdays, >15% of its single-supplier practices' OC falls in
the 07:00-07:59 band (UK practices are typically ~3%; flagged supplier-months are 18-28%).

For flagged rows (BST date, practice's only supplier is the flagged one) hourly bands are moved one
hour later. UTC 17:00-17:59 (= 18:00-18:59 local) is split half to 18:00-18:29 and half to
18:30-23:59. The 00:00-05:59 band is left in place (volumes are tiny).
Practices with more than one supplier listed are not corrected.

Old-format files (2-hour bands, 2024-25) cannot be shifted by one hour: use flag_old() to drop
flagged supplier-months instead.
"""
import io, os, zipfile
import numpy as np, pandas as pd

BST = [("2024-03-31", "2024-10-27"), ("2025-03-30", "2025-10-26"), ("2026-03-29", "2026-10-25")]
NEXT = {"06:00 - 06:59": "07:00 - 07:59", "07:00 - 07:59": "08:00 - 08:59", "08:00 - 08:59": "09:00 - 09:59",
        "09:00 - 09:59": "10:00 - 10:59", "10:00 - 10:59": "11:00 - 11:59", "11:00 - 11:59": "12:00 - 12:59",
        "12:00 - 12:59": "13:00 - 13:59", "13:00 - 13:59": "14:00 - 14:59", "14:00 - 14:59": "15:00 - 15:59",
        "15:00 - 15:59": "16:00 - 16:59", "16:00 - 16:59": "17:00 - 17:59",
        "18:00 - 18:29": "18:30 - 23:59", "18:30 - 23:59": "18:30 - 23:59", "00:00 - 05:59": "00:00 - 05:59"}
SPLIT = "17:00 - 17:59"


def in_bst(dates):
    d = pd.to_datetime(dates)
    m = np.zeros(len(d), bool)
    for a, b in BST:
        m |= ((d >= a) & (d < b)).to_numpy()
    return m


def supplier_lookup(month, sep_zip="research/data/oc_daytime_sep26.zip", jun_zip="research/data/oc_daytime_jun26.zip",
                    panel="research/data/panel_merged.parquet"):
    """gp_code -> upper-case supplier string for a month (YYYY-MM)."""
    z = {"2026-09": sep_zip, "2026-06": jun_zip}.get(month)
    if z and os.path.exists(z):
        fr = []
        with zipfile.ZipFile(z) as zz:
            for n in zz.namelist():
                if n.lower().endswith(".csv"):
                    fr.append(pd.read_csv(io.BytesIO(zz.read(n)), usecols=["GP_CODE", "SUPPLIER"]).drop_duplicates())
        s = pd.concat(fr).drop_duplicates("GP_CODE").set_index("GP_CODE").SUPPLIER
        return s.fillna("").str.upper()
    pm = pd.read_parquet(panel, columns=["month", "gp_code", "supplier"])
    m = month if month in set(pm.month) else max(x for x in pm.month.unique() if x <= month)
    return pm[pm.month == m].set_index("gp_code").supplier.fillna("").str.upper()


def _single(sup):
    return ~sup.str.contains(",")


def flagged_suppliers(df, sup, gp="gp_code", date="date", band="band", val="TOTAL", thresh=0.15):
    """Suppliers (single-supplier practices) whose BST weekday OC has >thresh in 07:00-07:59."""
    s = sup.reindex(df[gp]).to_numpy()
    d = pd.to_datetime(df[date])
    keep = in_bst(d) & (d.dt.dayofweek < 5).to_numpy() & pd.Series(s).fillna(",").pipe(_single).to_numpy()
    x = pd.DataFrame({"sup": s[keep], "early": (df[band].to_numpy()[keep] == "07:00 - 07:59") * df[val].to_numpy()[keep], "v": df[val].to_numpy()[keep]})
    if x.empty:
        return set(), pd.Series(dtype=float)
    r = x.groupby("sup").agg(early=("early", "sum"), v=("v", "sum"))
    r = r[r.v >= 2000]
    share = r.early / r.v
    return set(share[share > thresh].index), share.sort_values(ascending=False)


def fix(df, sup, gp="gp_code", date="date", band="band", vals=("TOTAL",), verbose=True, label=""):
    """Return df with bands shifted one hour later for flagged supplier rows on BST dates."""
    flags, share = flagged_suppliers(df, sup, gp, date, band, vals[0])
    if verbose:
        print(f"[timefix {label}] flagged suppliers: {sorted(flags) or 'none'}")
    if not flags:
        return df
    s = sup.reindex(df[gp]).fillna("").to_numpy()
    rows = in_bst(df[date]) & np.isin(s, list(flags))
    out = df.copy()
    a = out[~rows]
    b = out[rows].copy()
    sp = b[b[band] == SPLIT]
    b = b[b[band] != SPLIT]
    b[band] = b[band].map(NEXT).fillna(b[band])
    h1 = sp.copy(); h2 = sp.copy()
    for v in vals:
        if v in sp:
            h1[v] = np.ceil(sp[v] / 2); h2[v] = sp[v] - h1[v]
    h1[band] = "18:00 - 18:29"; h2[band] = "18:30 - 23:59"
    res = pd.concat([a, b, h1, h2], ignore_index=True)
    if verbose:
        print(f"[timefix {label}] shifted {rows.sum()} rows for {pd.Series(s[rows]).nunique()} supplier(s), "
              f"{df.loc[rows, gp].nunique()} practices")
    return res


def flag_old(df, thresh=0.15):
    """Old format (MONTH, WEEKDAY, SUBMISSION_TIME 2-hour bands, VALUE, SUPPLIER): return set of
    (month, supplier) to drop, where a BST-month supplier has >thresh of weekday OC in 06:00-07:59
    (UTC-shifted 8am peak; GMT months run ~6%)."""
    d = df.copy()
    d["m"] = d.MONTH.astype(str).str[:7]
    d["sup"] = d.SUPPLIER.fillna("").str.upper()
    d = d[d.WEEKDAY.isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]) & ~d.sup.str.contains(",")]
    d = d[in_bst(pd.to_datetime(d.m + "-15"))]
    if d.empty:
        return set(), pd.Series(dtype=float)
    d["early"] = (d.SUBMISSION_TIME == "06:00 - 07:59") * d.VALUE
    g = d.groupby(["m", "sup"])[["early", "VALUE"]].sum().rename(columns={"VALUE": "v"})
    g = g[g.v >= 2000]
    sh = g.early / g.v
    return set(sh[sh > thresh].index), sh.sort_values(ascending=False)


# ---------------------------------------------------------------- telephony (CBT)
# Found Nov 2026: about 110 practices (mostly sub-ICBs 15E Birmingham & Solihull and 15F Leeds, so
# probably one telephony provider) record call times in UTC during BST: their 06:00-07:59 share of
# weekday calls jumps from ~4% to ~27% on the clock-change day and 08:00-09:59 falls from ~34% to
# ~21%. CBT bands are two hours wide, so the shift cannot be undone; affected practices are left out
# of time-of-day call measures in BST months.
_CBT_BASE = None


def _cbt_shares(df, gp="gp_code", date="date", band="band", val="inbound"):
    d = df[pd.to_datetime(df[date]).dt.dayofweek < 5]
    b = d[band].astype(str).str.replace(" ", "")
    tot = d.groupby(gp)[val].sum()
    e = d[b == "06:00-07:59"].groupby(gp)[val].sum() / tot
    r = d[b == "08:00-09:59"].groupby(gp)[val].sum() / tot
    return pd.DataFrame({"e": e, "r": r, "n": tot}).fillna({"e": 0, "r": 0})


def cbt_baseline(panel="research/data/panel"):
    """Practice-level 6-8am and 8-10am call shares in GMT (Jan, Feb, 1-28 Mar 2026)."""
    global _CBT_BASE
    if _CBT_BASE is None:
        fr = []
        for m in ["2026-01", "2026-02", "2026-03"]:
            f = f"{panel}/cbt_daytime_{m}.parquet"
            if os.path.exists(f):
                x = pd.read_parquet(f, columns=["gp_code", "date", "band", "inbound"])
                fr.append(x[~in_bst(x.date)])
        _CBT_BASE = _cbt_shares(pd.concat(fr))
    return _CBT_BASE


def cbt_utc_practices(df, gp="gp_code", date="date", band="band", val="inbound", verbose=True, label=""):
    """Practices whose calls on BST dates look UTC-shifted relative to their own GMT baseline:
    6-8am share up >10 points and 8-10am share down >5 points. Practices with no GMT baseline are
    flagged when their 6-8am share exceeds both their 8-10am share and 25%."""
    d = df[in_bst(df[date])]
    if d.empty:
        return set()
    s = _cbt_shares(d, gp, date, band, val)
    s = s[s.n >= 500]
    base = cbt_baseline()
    base = base[base.n >= 500]
    j = s.join(base, rsuffix="_gmt", how="inner")
    flag = set(j.index[((j.e - j.e_gmt) > 0.10) & ((j.r - j.r_gmt) < -0.05)])
    # Practices with no GMT baseline (e.g. about 17 Black Country practices, codes M87/M88/M91/M92, whose
    # call data start in April 2026): flag when 6-8am calls outnumber 8-10am calls and are >25% of the
    # weekday total. In GMT months only 8 of 4,915 practices have more 6-8am than 8-10am calls.
    nb = s[~s.index.isin(base.index)]
    flag_nb = set(nb.index[(nb.e > nb.r) & (nb.e > 0.25)])
    if verbose:
        print(f"[timefix CBT {label}] {len(flag)} practices with UTC-shifted call times "
              f"(+{len(flag_nb)} with no GMT baseline) left out of time-of-day call measures")
    return flag | flag_nb
