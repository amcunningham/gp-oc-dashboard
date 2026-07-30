#!/usr/bin/env python3
"""
Staged, non-destructive rerun of the predictors/explanatory models honouring
vintage-by-purpose (staffing KEPT at Mar 2025; phones May 2026; OC Feb-Apr 2026).
numpy HC1 OLS (statsmodels absent). Build logic copied verbatim from
research/scripts/predictors_models.py so the spec is identical.
Writes a tidy key-coefficient CSV to the staging dir.
"""
import sys, os
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..'))   # research/data


def build(xsec_path):
    x = pd.read_csv(xsec_path, low_memory=False)
    ivr = pd.read_csv(f'{DATA}/cbt_ivr_panel.csv')
    may = ivr[ivr.month == '2026-05'].copy()
    may = may[(may.inbound >= 200) & (may.ivr_ended < 0.95 * may.inbound)]
    may['queue_answer'] = (100 * may.answered / (may.inbound - may.ivr_ended)).clip(upper=100)
    may['ivr_share'] = 100 * may.ivr_ended / may.inbound
    cbt = may[['gp_code', 'inbound', 'queue_answer', 'ivr_share']]

    dt = pd.read_parquet(f'{DATA}/cbt_daytime_may.parquet')
    core = dt[dt.tc.isin(['08:00-09:59', '10:00-11:59', '12:00-13:59',
                          '14:00-15:59', '16:00-17:59', '18:00-18:29'])]
    bydow = core.groupby(['gp_code', 'dow'])[['inbound', 'ivr_ended', 'answered']].sum().reset_index()
    bydow['ar'] = (100 * bydow.answered / (bydow.inbound - bydow.ivr_ended)).clip(upper=100)
    mon = bydow[bydow.dow == 1].set_index('gp_code').ar
    wed = bydow[bydow.dow == 3].set_index('gp_code').ar
    monwed = (wed - mon).rename('monwed_gap').reset_index()

    morn = dt[dt.tc == '08:00-09:59'].groupby('gp_code')[['inbound', 'ivr_ended']].sum()
    rest = dt[dt.tc != '08:00-09:59'].groupby('gp_code')[['inbound', 'ivr_ended']].sum()
    ivx = (100 * morn.ivr_ended / morn.inbound - 100 * rest.ivr_ended / rest.inbound)
    ivx = ivx.rename('ivr_morning_excess').reset_index()

    p = pd.read_parquet(f'{DATA}/panel_merged.parquet')
    pm = p[p.month == '2026-05'][['gp_code', 'total', 'oc_total']] \
        .rename(columns={'total': 'appts_may', 'oc_total': 'oc_may'})
    lm = p[p.month == '2026-03'][['gp_code', 'list_size']].rename(columns={'list_size': 'list_may'})
    pm = pm.merge(lm, on='gp_code', how='left')
    oc = p[p.month.isin(['2026-02', '2026-03', '2026-04'])] \
        .groupby('gp_code').oc_rate_1k.mean().rename('oc_rate_febapr').reset_index()

    comp = pd.read_csv(f'{DATA}/gp_composition_mar25.csv')

    d = (x.merge(cbt, on='gp_code', how='left')
          .merge(monwed, on='gp_code', how='left')
          .merge(ivx, on='gp_code', how='left')
          .merge(pm, on='gp_code', how='left')
          .merge(oc, on='gp_code', how='left')
          .merge(comp, on='gp_code', how='left', suffixes=('', '_comp')))

    L = d.list_size
    d['partner_per10k'] = 1e4 * d.partner_fte / L
    d['salaried_per10k'] = 1e4 * d.salaried_fte / L
    d['locum_per10k'] = 1e4 * d.locum_fte / L
    d['trainee_per10k'] = 1e4 * (d.registrar_fte + d.foundation_other_fte) / L
    d['training_flag'] = (d.registrar_fte > 0.25).astype(float)
    d['nurse10k_c'] = 1e4 * d.nurse_fte_comp / L
    d['dpc10k_c'] = 1e4 * d.dpc_fte_comp / L
    d['admin10k_c'] = 1e4 * d.admin_fte_comp / L
    d['fq_per10k'] = 1e4 * (d.partner_fte + d.salaried_fte + d.locum_fte) / L
    d['calls_per1k'] = 1e3 * d.inbound / d.list_size
    d['contacts_per_appt'] = (d.inbound + d.oc_may.fillna(0)) / d.appts_may
    return d


OPS = ['queue_answer', 'ivr_share', 'monwed_gap', 'contacts_per_appt',
       'calls_per1k', 'oc_rate_febapr', 'same_day_pct_12m']
CIRC = ['log_list', 'imd_score', 'partner_per10k', 'salaried_per10k',
        'locum_per10k', 'trainee_per10k', 'training_flag', 'nurse10k_c',
        'dpc10k_c', 'admin10k_c', 'appts_percap', 'pct65plus', 'nonwhite_pct']
REP = ['deflection_2026', 'continuity_2026', 'has_pref_hcp_2026']
INTER = ['adm_x_size', 'adm_x_oc']
OUTCOMES = {'Q32_overall': 'satisfaction_2026',
            'Q16_contact': 'access_satisfaction_2026',
            'Q1_phone': 'phone_easy_2026'}


def zfit(m, extra_z=()):
    m = m.copy()
    for v in set(OPS + CIRC + REP + ['ivr_morning_excess', 'fq_per10k']) | set(extra_z):
        if v in m.columns and v != 'training_flag':
            m['z_' + v] = (m[v] - m[v].mean()) / m[v].std()
    if 'training_flag' in m.columns:
        m['z_training_flag'] = m.training_flag
    if 'admin10k_c' in m.columns:
        m['z_adm_x_size'] = m['z_admin10k_c'] * m['z_log_list']
        if 'oc_rate_febapr' in m.columns:
            m['z_adm_x_oc'] = m['z_admin10k_c'] * m['z_oc_rate_febapr']
    return m


def ols_hc1(m, y, preds):
    cols = ['z_' + p for p in preds]
    X = np.column_stack([np.ones(len(m))] + [m[c].values for c in cols])
    yv = m[y].values.astype(float)
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ (X.T @ yv)
    resid = yv - X @ beta
    n, k = X.shape
    # HC1
    S = (X * resid[:, None])
    meat = S.T @ S
    cov = XtX_inv @ meat @ XtX_inv * (n / (n - k))
    se = np.sqrt(np.diag(cov))
    yhat = X @ beta
    r2 = 1 - np.sum(resid**2) / np.sum((yv - yv.mean())**2)
    names = ['const'] + preds
    params = dict(zip(names, beta))
    ses = dict(zip(names, se))
    return params, ses, r2, n


rows = []


def run_file(path, tag):
    d = build(path)
    d = d[d.gpps_n_2026 >= 30]
    allv = OPS + CIRC + REP + list(OUTCOMES.values())
    cbt = d.dropna(subset=allv)
    cbt = cbt[cbt.contacts_per_appt <= 5]
    cbt = zfit(cbt)
    for oname, y in OUTCOMES.items():
        for spec, preds in [('together', OPS + CIRC + INTER),
                            ('plusreport', OPS + CIRC + INTER + REP)]:
            params, ses, r2, n = ols_hc1(cbt, y, preds)
            for p in preds:
                rows.append(dict(tag=tag, model=spec, outcome=oname, predictor=p,
                                 coef=round(params[p], 3), se=round(ses[p], 3)))
            rows.append(dict(tag=tag, model=spec, outcome=oname, predictor='_R2',
                             coef=round(r2, 4), se=np.nan))
            rows.append(dict(tag=tag, model=spec, outcome=oname, predictor='_n',
                             coef=n, se=np.nan))
    # Continuity model C
    cvars = OPS + CIRC + ['continuity_2026']
    cm = d.dropna(subset=cvars)
    cm = cm[cm.contacts_per_appt <= 5]
    cm = zfit(cm)
    params, ses, r2, n = ols_hc1(cm, 'continuity_2026', OPS + CIRC + INTER)
    for p in ['partner_per10k', 'salaried_per10k', 'trainee_per10k', 'training_flag']:
        rows.append(dict(tag=tag, model='C_continuity', outcome='continuity_2026',
                         predictor=p, coef=round(params[p], 3), se=round(ses[p], 3)))
    rows.append(dict(tag=tag, model='C_continuity', outcome='continuity_2026',
                     predictor='_n', coef=n, se=np.nan))
    print(f'[{tag}] done, CBT n reported per outcome')


run_file(f'{DATA}/xsec_master_2026.csv', 'before_live')
run_file(f'{DATA}/xsec_master_rebuilt.csv', 'after_rebuilt')

out = pd.DataFrame(rows)
out.to_csv(f'{HERE}/predictors_rerun_before_after.csv', index=False)
print('[written] predictors_rerun_before_after.csv', len(out), 'rows')

# Key-coefficient before/after pivot for the 6 requested families
KEY = {'deflection_2026': 'Told to contact again (Q12)',
       'continuity_2026': 'See preferred clinician (Q7)',
       'has_pref_hcp_2026': 'Have preferred clinician (Q6)',
       'queue_answer': 'Queue-answer rate',
       'imd_score': 'Deprivation (IMD)'}
piv = out[out.predictor.isin(KEY)].pivot_table(
    index=['model', 'outcome', 'predictor'], columns='tag', values='coef', aggfunc='first')
piv['delta'] = (piv['after_rebuilt'] - piv['before_live']).round(3)
piv.to_csv(f'{HERE}/key_coef_before_after.csv')
print(piv.to_string())
