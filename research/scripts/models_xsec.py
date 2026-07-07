import pandas as pd, numpy as np, statsmodels.formula.api as smf
d = pd.read_csv('xsec_2025.csv')
d['rural'] = (d.rurality=='Rural').astype(float)
d['dispensing_f'] = (d.dispensing=='Yes').astype(float)
d['log_list'] = np.log(d.list_size)
for c in ['gp_fte','nurse_fte','dpc_fte','admin_fte']:
    d[c.replace('_fte','_per10k')] = 10000*d[c]/d.list_size
d['merged_recent'] = (d.max_jump>1.15).astype(float)
d = d.replace([np.inf,-np.inf],np.nan)
d = d.dropna(subset=['same_day_pct_12m','imd_score','log_list','gp_per10k','rural','region'])
d = d[(d.gp_per10k<50)&(d.list_size>1000)]
print("n =", len(d), "| merged_recent:", int(d.merged_recent.sum()))

ctrl = 'rural + imd_score + log_list + gp_per10k + nurse_per10k + dpc_per10k + merged_recent + dispensing_f + C(region)'
mA = smf.ols(f'same_day_pct_12m ~ oc_rate_12m + {ctrl}', data=d).fit(cov_type='HC1')
print('\n=== A: what predicts same-day % ===')
print(mA.params.drop([p for p in mA.params.index if 'region' in p]).round(3).to_string())
print('p-values:'); print(mA.pvalues.drop([p for p in mA.pvalues.index if 'region' in p]).round(4).to_string())
print('R2:', round(mA.rsquared,3))

for y in ['satisfaction','continuity']:
    dd = d.dropna(subset=[y,'gpps_n'])
    m = smf.wls(f'{y} ~ same_day_pct_12m + {ctrl}', data=dd, weights=dd.gpps_n).fit(cov_type='HC1')
    b = m.params['same_day_pct_12m']; se = m.bse['same_day_pct_12m']
    print(f'\n=== {y} ~ same-day % (weighted by GPPS n, n={len(dd)}) ===')
    print(f'beta same_day_pct: {b:.3f} (SE {se:.3f}, p={m.pvalues["same_day_pct_12m"]:.2e})')
    print('  -> 10pp higher same-day share ->', round(10*b,2), 'pp change in', y)
    print(m.params.drop([p for p in m.params.index if 'region' in p]).round(3).to_string())
d.to_csv('xsec_model_data.csv', index=False)
