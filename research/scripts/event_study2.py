import pandas as pd, numpy as np
from linearmodels.panel import PanelOLS
df = pd.read_csv('panel_merged.csv')
df = df[(df.month>='2023-04')&(df.month<='2026-03')].copy()
df['mnum'] = pd.to_datetime(df.month).dt.year*12 + pd.to_datetime(df.month).dt.month

def find_t0(g):
    g = g.sort_values('mnum'); r = g.oc_rate_1k.values; m = g.mnum.values
    if len(r)<12 or np.isnan(r).all(): return np.nan
    lo_end=-1
    for i in range(2,len(r)):
        w=r[i-2:i+1]
        if np.isnan(w).any(): continue
        if w.max()<5: lo_end=i
        if w.min()>20 and lo_end>=0 and i-2>lo_end: return m[i-2]
    return np.nan

t0 = df.dropna(subset=['oc_rate_1k']).groupby('gp_code').apply(find_t0, include_groups=False).dropna().rename('t0')
df = df.merge(t0, on='gp_code', how='left')
df['k'] = df.mnum-df.t0
obs = df[df.k.notna()].groupby('gp_code').k.agg(['min','max'])
keep = obs[(obs['min']<=-6)&(obs['max']>=6)].index
df.loc[df.k.notna() & ~df.gp_code.isin(keep),'k']=np.nan
df['kb']=df.k.clip(-12,12)

# supplier at adoption (modal in k 0..3)
sup = df[(df.k>=0)&(df.k<=3)].dropna(subset=['supplier']).groupby('gp_code')['supplier'] \
        .agg(lambda s: s.mode().iloc[0]).rename('sup_t0')
def bucket(s):
    s=str(s).upper()
    if 'ECONSULT' in s: return 'eConsult'
    if 'ACCURX' in s: return 'Accurx'
    if 'TPP' in s or 'SYSTM' in s: return 'TPP/SystmConnect'
    if 'ANIMA' in s: return 'Anima'
    if 'PATCHS' in s or 'ADVANCED' in s: return 'PATCHS'
    return 'Other'
sup = sup.map(bucket)
print(sup.value_counts().to_string())
df = df.merge(sup, on='gp_code', how='left')

d = df.dropna(subset=['same_day_pct']); d = d[d.total>=200].copy()
d['t']=pd.to_datetime(d.month)

def run_es(sub, label):
    dd = sub.copy()
    for k in range(-12,13):
        if k==-1: continue
        dd[f'ev_{k+12}']=((dd.kb==k)).astype(float)
    evcols=[f'ev_{k+12}' for k in range(-12,13) if k!=-1]
    ddd=dd.set_index(['gp_code','t'])
    res=PanelOLS.from_formula('same_day_pct ~ '+' + '.join(evcols)+' + EntityEffects + TimeEffects',
                              data=ddd).fit(cov_type='clustered', cluster_entity=True)
    return pd.DataFrame({'grp':label,'k':[k for k in range(-12,13) if k!=-1],
                         'beta':[res.params[c] for c in evcols],'se':[res.std_errors[c] for c in evcols]})

controls = d[d.t0.isna()]
rows=[]
for g in ['Accurx','eConsult','TPP/SystmConnect','Anima']:
    n = d[(d.sup_t0==g)&(d.k.notna())].gp_code.nunique()
    if n<80: print('skip',g,n); continue
    sub = pd.concat([d[d.sup_t0==g], controls])
    rows.append(run_es(sub,g)); print(g,'adopters:',n,'done')
pd.concat(rows).to_csv('event_study_supplier.csv', index=False)
print('saved')
