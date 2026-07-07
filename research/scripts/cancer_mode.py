import pandas as pd, numpy as np, statsmodels.formula.api as smf
def fp(path, name):
    d = pd.read_csv(path, low_memory=False)
    d = d[(d['Area Type']=='GPs') & (d['Time period']=='2024/25')]
    d = d[['Area Code','Value','Denominator']].rename(columns={'Area Code':'gp_code','Value':name,'Denominator':f'{name}_den'})
    return d
cdr = fp('/tmp/cdr.csv','cdr'); conv = fp('/tmp/conv.csv','conv'); refs = fp('/tmp/refs.csv','ref_rate')
x = pd.read_csv('xsec_model_data.csv')
d = x.merge(cdr,on='gp_code',how='left').merge(conv,on='gp_code',how='left').merge(refs,on='gp_code',how='left')
d['appts_per1k_mo'] = d.appts_12m/12/d.list_size*1000
ctrl = 'rural + imd_score + log_list + gp_per10k + nurse_per10k + dpc_per10k + merged_recent + dispensing_f + C(region)'
print("=== Cancer outcomes 2024/25 ~ same-day % (Apr24-Mar25) ===")
for y,w in [('cdr','cdr_den'),('conv','conv_den'),('ref_rate','ref_rate_den')]:
    dd = d.dropna(subset=[y,w,'same_day_pct_12m'])
    m = smf.wls(f'{y} ~ same_day_pct_12m + {ctrl}', data=dd, weights=dd[w]).fit(cov_type='HC1')
    u = smf.wls(f'{y} ~ same_day_pct_12m', data=dd, weights=dd[w]).fit(cov_type='HC1')
    print(f"{y:9s} n={len(dd):5d} mean={dd[y].mean():7.1f} | unadj {u.params['same_day_pct_12m']:+.4f} (p={u.pvalues['same_day_pct_12m']:.1e}) | adj {m.params['same_day_pct_12m']:+.4f} (SE {m.bse['same_day_pct_12m']:.4f}, p={m.pvalues['same_day_pct_12m']:.1e})")
print("\n=== Same-day % vs mode & volume (cross-section) ===")
for v in ['phone_pct_12m','f2f_pct_12m','appts_per1k_mo','dna_pct_12m']:
    dd = d.dropna(subset=[v,'same_day_pct_12m'])
    r = np.corrcoef(dd[v], dd.same_day_pct_12m)[0,1]
    m = smf.ols(f'same_day_pct_12m ~ {v} + {ctrl}', data=dd).fit(cov_type='HC1')
    print(f"{v:16s} r={r:+.3f} | adj beta {m.params[v]:+.4f} (p={m.pvalues[v]:.1e})")
d.to_csv('xsec_with_cancer.csv', index=False)
print("\nmode means: phone", round(d.phone_pct_12m.mean(),1), "f2f", round(d.f2f_pct_12m.mean(),1), "| appts/1k/mo", round(d.appts_per1k_mo.mean(),0))
