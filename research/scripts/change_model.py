import duckdb, pandas as pd, numpy as np, statsmodels.formula.api as smf
con = duckdb.connect()
def gpps(path, yr):
    return con.execute(f"""
      SELECT ad_practicecode AS gp_code,
        TRY_CAST("overallexp.pcteval" AS DOUBLE)*100 AS sat_{yr},
        TRY_CAST("localgpservicesprefhpsee.pcteval" AS DOUBLE)*100 AS cont_{yr},
        TRY_CAST(received AS DOUBLE) AS n_{yr}
      FROM read_csv('{path}', header=true, all_varchar=true)""").df()
def sameday(m0, m1, yr):
    return con.execute(f"""
      SELECT gp_code, SUM(same_day)*100.0/SUM(total) AS sd_{yr}, AVG(oc_rate_1k) AS oc_{yr}
      FROM read_csv_auto('panel_merged.csv')
      WHERE month BETWEEN '{m0}' AND '{m1}' GROUP BY 1 HAVING SUM(total)>1000""").df()
g24, g25 = gpps('/tmp/gpps2024.csv','24'), gpps('/tmp/gpps2025.csv','25')
s24, s25 = sameday('2023-04','2024-03','24'), sameday('2024-04','2025-03','25')
x = pd.read_csv('xsec_model_data.csv')[['gp_code','rural','imd_score','log_list','gp_per10k','nurse_per10k','dpc_per10k','merged_recent','dispensing_f','region']]
d = g24.merge(g25,on='gp_code').merge(s24,on='gp_code').merge(s25,on='gp_code').merge(x,on='gp_code')
for c in ['sat_24','sat_25','cont_24','cont_25']:
    d.loc[(d[c]<0)|(d[c]>100), c] = np.nan
d['d_sat'] = d.sat_25-d.sat_24; d['d_cont'] = d.cont_25-d.cont_24
d['d_sd'] = d.sd_25-d.sd_24; d['d_oc'] = d.oc_25-d.oc_24
d['w'] = d[['n_24','n_25']].min(axis=1)
d = d.dropna(subset=['d_sat','d_cont','d_sd','w','region'])
print("n =", len(d), "| SD of change in same-day %:", round(d.d_sd.std(),1))
for y in ['d_sat','d_cont']:
    u = smf.wls(f'{y} ~ d_sd', data=d, weights=d.w).fit(cov_type='HC1')
    m = smf.wls(f'{y} ~ d_sd + d_oc + rural + imd_score + log_list + merged_recent + C(region)', data=d, weights=d.w).fit(cov_type='HC1')
    print(f"{y}: unadj {u.params['d_sd']:.4f} (p={u.pvalues['d_sd']:.1e}) | adj {m.params['d_sd']:.4f} (SE {m.bse['d_sd']:.4f}, p={m.pvalues['d_sd']:.1e}) | d_oc coef {m.params['d_oc']:.4f} (p={m.pvalues['d_oc']:.1e})")
d.to_csv('change_2024_2025.csv', index=False)
print("means: d_sat", round(d.d_sat.mean(),2), "d_cont", round(d.d_cont.mean(),2), "d_sd", round(d.d_sd.mean(),2))
