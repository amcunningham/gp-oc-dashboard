import pandas as pd, numpy as np
df = pd.read_csv('panel_merged.csv')
df = df[(df.month>='2023-04')&(df.month<='2026-03')].copy()
df['mnum'] = pd.to_datetime(df.month).dt.year*12 + pd.to_datetime(df.month).dt.month

# adoption month per practice: first month of sustained (3m) rate>20 occurring after sustained (3m) rate<5
def find_t0(g):
    g = g.sort_values('mnum')
    r = g.oc_rate_1k.values; m = g.mnum.values
    if len(r) < 12 or np.isnan(r).all(): return np.nan
    lo_end = -1
    for i in range(2, len(r)):
        w = r[i-2:i+1]
        if np.isnan(w).any(): continue
        if w.max() < 5: lo_end = i
        if w.min() > 20 and lo_end >= 0 and i-2 > lo_end - 2:
            if i-2 > lo_end:  # hi run starts after lo run ends
                return m[i-2]
    return np.nan

t0 = df.dropna(subset=['oc_rate_1k']).groupby('gp_code').apply(find_t0, include_groups=False)
t0 = t0.dropna().rename('t0')
print("adopters:", len(t0))

df = df.merge(t0, on='gp_code', how='left')
df['k'] = df.mnum - df.t0   # event time; NaN for never-adopters
# require adopters to have >=6 pre and >=6 post months observed
obs = df[df.k.notna()].groupby('gp_code').k.agg(['min','max'])
keep = obs[(obs['min']<=-6)&(obs['max']>=6)].index
df.loc[df.k.notna() & ~df.gp_code.isin(keep), 'k'] = np.nan
print("adopters with >=6 pre & post:", df[df.k.notna()].gp_code.nunique())

# bin event time to [-12,12]
df['kb'] = df.k.clip(-12,12)
d = df.dropna(subset=['same_day_pct']).copy()
d = d[d.total>=200]

from linearmodels.panel import PanelOLS
d['t'] = pd.to_datetime(d.month)
# event dummies, ref k=-1; never-adopters have all dummies 0 (pure controls)
for k in range(-12,13):
    if k==-1: continue
    d[f'ev_{k+12}'] = ((d.kb==k)).astype(float)
evcols = [f'ev_{k+12}' for k in range(-12,13) if k!=-1]
dd = d.set_index(['gp_code','t'])
form = 'same_day_pct ~ ' + ' + '.join(evcols) + ' + EntityEffects + TimeEffects'
res = PanelOLS.from_formula(form, data=dd).fit(cov_type='clustered', cluster_entity=True)
out = pd.DataFrame({'k':[k for k in range(-12,13) if k!=-1],
                    'beta':[res.params[c] for c in evcols],
                    'se':[res.std_errors[c] for c in evcols]})
out.to_csv('event_study_main.csv', index=False)
print(out.round(2).to_string(index=False))
