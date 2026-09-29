#!/usr/bin/env python3
"""
refresh_gpad_2526.py -- refresh the GPAD block of xsec_master_2026.{csv,parquet}
so operational measures cover April 2025 - March 2026 (matching GPPS 2026 fieldwork
Jan-Apr 2026), instead of the frozen April 2024 - March 2025 vintage that
ingest_gpps2026.py silently inherited from xsec_master.csv.

Refreshed (from panel_merged.parquet + waits_panel.parquet, window Apr25-Mar26):
  same_day_pct_12m, gp_same_day_pct_12m, phone_pct_12m, f2f_pct_12m, dna_pct_12m,
  list_size, log_list, size_q, appts_12m, appts_percap, sd_share, sd_percap,
  gp_share, gp_sd, oth_sd, sd_pct, d1_7_pct, d8_14_pct, d15plus_pct, gp_d15plus_pct,
  gp_15p, oth_15p, sd_share_prior_year (=Apr24-Mar25), max_jump (Apr24-Mar26 window),
  merged_recent, gp_per10k, nurse_per10k, dpc_per10k, admin_per10k, high80

Preserved (bit-for-bit copied from the existing xsec_master_2026):
  oc_rate_12m (kept as separate Apr24-Mar25 OC-submissions measure),
  raw workforce FTEs (gp_fte, nurse_fte, dpc_fte, admin_fte -- Mar 2025 vintage),
  GPPS 2024/2025/2026 outcomes + weights, IMD, region, deprivation, clinical,
  prescribing, names, geography, closure/merger flags, ae_*, phone_failed etc.

Practices with fewer than 12 GPAD months available in the Apr25-Mar26 window keep
their row but have the ENTIRE refreshed GPAD block nulled -- partial totals
must NOT be presented as annual totals or divided by 12.

Non-destructive: writes xsec_master_2026_refreshed.{csv,parquet} next to the
canonical files. Compare, then promote by copying over the originals in a
separate step.
"""
import os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
PM   = os.path.join(DATA, "panel_merged.parquet")
WAITS= os.path.join(DATA, "waits_panel.parquet")
CUR  = os.path.join(DATA, "xsec_master_2026.parquet")
OUT_CSV = os.path.join(DATA, "xsec_master_2026_refreshed.csv")
OUT_PQ  = os.path.join(DATA, "xsec_master_2026_refreshed.parquet")

WIN_CUR    = ('2025-04', '2026-03')   # 12m window for the refresh
WIN_PRIOR  = ('2024-04', '2025-03')   # prior-year same-day share
WIN_JUMP   = ('2024-04', '2026-03')   # 24m window for list-size jumps

# Columns whose values are refreshed from the panels; every practice's block is
# either fully refreshed (>=12 months) or fully NULL (<12 months).
GPAD_COLS = [
    'same_day_pct_12m','gp_same_day_pct_12m','phone_pct_12m','f2f_pct_12m','dna_pct_12m',
    'list_size','log_list','size_q','appts_12m','appts_percap',
    'sd_share','sd_percap','gp_share','gp_sd','oth_sd',
    'sd_pct','d1_7_pct','d8_14_pct','d15plus_pct','gp_d15plus_pct','gp_15p','oth_15p',
    'sd_share_prior_year','max_jump','merged_recent',
    'gp_per10k','nurse_per10k','dpc_per10k','admin_per10k','high80',
]


def agg_panel(pm, window):
    m = pm[(pm.month >= window[0]) & (pm.month <= window[1])].copy()
    g = m.groupby('gp_code')
    total = g['total'].sum()
    same_day = g['same_day'].sum()
    gp = g['gp'].sum()
    gp_same_day = g['gp_same_day'].sum()
    phone = g['phone'].sum()
    f2f = g['f2f'].sum()
    dna = g['dna'].sum()
    list_size = g['list_size'].mean()
    months = g['month'].nunique().rename('n_months')

    out = pd.DataFrame({
        'gp_code': total.index,
        'same_day_pct_12m': (100.0 * same_day / total).values,
        'gp_same_day_pct_12m': (100.0 * gp_same_day / gp.replace(0, np.nan)).values,
        'phone_pct_12m': (100.0 * phone / total).values,
        'f2f_pct_12m':   (100.0 * f2f   / total).values,
        'dna_pct_12m':   (100.0 * dna   / total).values,
        'list_size': list_size.values,
        'appts_12m': total.values,
        'gp_share': (100.0 * gp / total).values,
        'gp_sd':    (100.0 * gp_same_day / gp.replace(0, np.nan)).values,
        'oth_sd':   (100.0 * (same_day - gp_same_day) / (total - gp).replace(0, np.nan)).values,
        'sd_share': (100.0 * same_day / total).values,
        'sd_percap':    (1000.0 * same_day / 12 / list_size.replace(0, np.nan)).values,
        'appts_percap': (1000.0 * total    / 12 / list_size.replace(0, np.nan)).values,
        'n_months': months.reindex(total.index).values,
    })
    return out


def agg_waits(wp, window):
    m = wp[(wp.month >= window[0]) & (wp.month <= window[1])].copy()
    g = m.groupby('gp_code')
    total = g['total'].sum()
    gp = g['gp'].sum()
    same_day = g['same_day'].sum()
    d1 = g['d1'].sum(); d2_7 = g['d2_7'].sum(); d8_14 = g['d8_14'].sum()
    d15_21 = g['d15_21'].sum(); d22_28 = g['d22_28'].sum(); d28plus = g['d28plus'].sum()
    gp_d15plus = g['gp_d15plus'].sum()
    d15p = d15_21 + d22_28 + d28plus

    out = pd.DataFrame({
        'gp_code': total.index,
        'sd_pct':       (100.0 * same_day / total.replace(0, np.nan)).values,
        'd1_7_pct':     (100.0 * (d1 + d2_7) / total.replace(0, np.nan)).values,
        'd8_14_pct':    (100.0 * d8_14 / total.replace(0, np.nan)).values,
        'd15plus_pct':  (100.0 * d15p / total.replace(0, np.nan)).values,
        'gp_d15plus_pct': (100.0 * gp_d15plus / gp.replace(0, np.nan)).values,
        'gp_15p':       (100.0 * gp_d15plus / gp.replace(0, np.nan)).values,
        'oth_15p':      (100.0 * (d15p - gp_d15plus) / (total - gp).replace(0, np.nan)).values,
    })
    return out


def prior_sd_share(pm, window):
    m = pm[(pm.month >= window[0]) & (pm.month <= window[1])]
    g = m.groupby('gp_code')
    total = g['total'].sum()
    same_day = g['same_day'].sum()
    return pd.DataFrame({
        'gp_code': total.index,
        'sd_share_prior_year': (100.0 * same_day / total.replace(0, np.nan)).values,
    })


def jumps(pm, window):
    m = pm[(pm.month >= window[0]) & (pm.month <= window[1])].sort_values(['gp_code','month']).copy()
    m['lag_list'] = m.groupby('gp_code')['list_size'].shift(1)
    m['jump'] = m['list_size'] / m['lag_list'].replace(0, np.nan)
    j = m.groupby('gp_code')['jump'].max().rename('max_jump').reset_index()
    return j


def main():
    print(f"[read] {CUR}")
    x = pd.read_parquet(CUR)
    print(f"       shape: {x.shape}")
    assert list(x.columns).count('gp_code') == 1

    print(f"[read] {PM}")
    pm = pd.read_parquet(PM)
    print(f"[read] {WAITS}")
    wp = pd.read_parquet(WAITS)

    print(f"\n[compute] GPAD panel aggregates for {WIN_CUR[0]}..{WIN_CUR[1]}")
    a = agg_panel(pm, WIN_CUR)
    print(f"[compute] waits-band aggregates for {WIN_CUR[0]}..{WIN_CUR[1]}")
    w = agg_waits(wp, WIN_CUR)
    print(f"[compute] prior-year sd_share for {WIN_PRIOR[0]}..{WIN_PRIOR[1]}")
    prior = prior_sd_share(pm, WIN_PRIOR)
    print(f"[compute] max_jump over {WIN_JUMP[0]}..{WIN_JUMP[1]}")
    j = jumps(pm, WIN_JUMP)

    # Merge everything on gp_code
    ref = a.merge(w, on='gp_code', how='left') \
           .merge(prior, on='gp_code', how='left') \
           .merge(j, on='gp_code', how='left')

    # Restrict to the 6,007 practices already in the master (in-place refresh)
    ref = ref.merge(x[['gp_code']], on='gp_code', how='right')
    print(f"[merge] refreshed rows for master practices: {ref.shape[0]}")

    # Fill in workforce-per-10k using EXISTING FTEs (unchanged) and NEW list_size
    ref = ref.merge(
        x[['gp_code','gp_fte','nurse_fte','dpc_fte','admin_fte']],
        on='gp_code', how='left',
    )
    ls = ref['list_size'].where(ref['list_size'] > 0)
    ref['gp_per10k']    = 10000 * ref['gp_fte']    / ls
    ref['nurse_per10k'] = 10000 * ref['nurse_fte'] / ls
    ref['dpc_per10k']   = 10000 * ref['dpc_fte']   / ls
    ref['admin_per10k'] = 10000 * ref['admin_fte'] / ls

    # Derived
    ref['log_list']      = np.log(ls)
    ref['merged_recent'] = ((ref['max_jump'] > 1.15).astype('float')).where(ref['max_jump'].notna())
    ref['high80']        = ((ref['gp_sd'] >= 80).astype('float')).where(ref['gp_sd'].notna())

    # Identify incomplete practices: < 12 months in the current window
    incomplete = ref['gp_code'][(ref['n_months'].isna()) | (ref['n_months'] < 12)].tolist()
    print(f"\n[incomplete] {len(incomplete)} practices with <12 GPAD months in {WIN_CUR[0]}..{WIN_CUR[1]}")
    for c in sorted(incomplete):
        n = ref.loc[ref.gp_code == c, 'n_months'].iloc[0]
        print(f"    {c}  n_months={0 if pd.isna(n) else int(n)}")

    # Null GPAD block for incomplete practices (do NOT scale partial totals)
    mask = ref['gp_code'].isin(incomplete)
    for col in GPAD_COLS:
        ref.loc[mask, col] = np.nan

    # size_q: quartiles of list_size among the complete practices only, with the
    # original master's string labels (small / q2 / q3 / large).
    valid_ls = ref['list_size'].where(~mask)
    ranked = valid_ls.rank(method='first', na_option='keep')
    n_valid = ranked.notna().sum()
    q_int = np.ceil(ranked / n_valid * 4)
    label = {1: 'small', 2: 'q2', 3: 'q3', 4: 'large'}
    ref['size_q'] = q_int.map(label).astype('object')

    # Non-GPAD columns: keep EXACTLY what the master already had
    keep_cols = [c for c in x.columns if c not in GPAD_COLS]
    out = x[keep_cols].merge(ref[['gp_code'] + GPAD_COLS], on='gp_code', how='left')

    # Restore original column order
    out = out[list(x.columns)]

    # Sanity checks
    assert out.shape == x.shape, f"shape drift: {out.shape} vs {x.shape}"
    complete_years = out.dropna(subset=['same_day_pct_12m','list_size','appts_12m']).shape[0]
    print(f"\n[verify] shape:            {out.shape}  (expected {x.shape})")
    print(f"[verify] complete rows:    {complete_years}  (expected 5994)")
    print(f"[verify] missing GPAD:     {out.shape[0] - complete_years}  (expected 13)")

    # Column-order preserved?
    assert list(out.columns) == list(x.columns)

    print(f"\n[write] {OUT_CSV}")
    out.to_csv(OUT_CSV, index=False)
    print(f"[write] {OUT_PQ}")
    out.to_parquet(OUT_PQ, index=False)

    print("\n[done] Compare the refreshed file to the canonical, then promote.")


if __name__ == '__main__':
    main()
