#!/usr/bin/env python3
"""
predictors_models.py -- one-command rerun of every model on predictors.html.

Reconstructs the 11 Jul 2026 final specification (PANEL_NOTES/NOTES_BATCH_DRAFT
sections 4.15-4.23, 4.31) from repo sources:

  outcomes   GPPS 2026: Q32 satisfaction_2026, Q16 access_satisfaction_2026,
             Q1 phone_easy_2026 (practices with gpps_n_2026 >= 30)
  reported   Q12 deflection_2026, Q7 continuity_2026, Q6 has_pref_hcp_2026
  phones     CBT May 2026 (>=200 inbound, IVR<95%): queue-answer rate
             answered/(inbound-IVR) capped 100, IVR share, Mon-Wed answering gap
             (Wed minus Mon, core hours), calls per 1,000 (xsec list)
  intake     OC submissions per 1,000/month, mean Feb-Apr 2026 (May flagged
             incomplete by NHSE); contacts per appointment (CBT inbound + OC
             May / GPAD appts May), sanity-filtered to <=5
  staffing   GP composition Mar 2025 detailed census (partners, salaried incl
             retainers, regular locums, trainees = registrar + foundation);
             training practice = registrar FTE > 0.25; nurse/DPC/admin from the
             same file; per-10k on the xsec 12m-average list
  structure  xsec: log list, IMD 2025, appts/1k/month, % 65+, % ethnic minority

Estimation: OLS, HC1 robust SEs, no region effects, no survey weights; every
predictor except the training flag z-scored within the estimation sample, so
coefficients are pp per SD. "Alone" = bivariate on the same sample. Models:
  A. three outcomes x (Alone / Together / + patients report), CBT sample
  B. all-practices combined model (phone measures dropped)
  C. continuity (Q7) as outcome, external spec
  D. validity: phone data alone -> phone ease / deflection / couldn't contact
  E. validity: everything external -> deflection
  F. descriptives: deflection deciles under pressure; answering by admin fifth

Usage:  python3 predictors_models.py <xsec_master csv> [--tag NAME]
        e.g.  python3 research/scripts/predictors_models.py research/data/xsec_master_2026.csv
        Data dir defaults to ../data relative to this script (override: GPOC_DATA env var).

Reconstructed 15 Jul 2026 from the published page + notes; reproduces the live
predictors.html tables to mean |diff| 0.07pp over 294 coefficients (see
research/projects/predictors-rerun-2026-07-15.md for the full three-way diff
against the rebuilt cross-section).
Writes: predictors_rerun_<tag>.csv (tidy coefficient table) + printed tables.
"""
import sys, argparse
import pandas as pd, numpy as np, statsmodels.api as sm
import os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('GPOC_DATA', os.path.normpath(os.path.join(HERE, '..', 'data')))

def build(xsec_path):
    x = pd.read_csv(xsec_path, low_memory=False)

    # --- CBT May 2026: queue-answer rate, IVR share, calls/1k (quality filters per notes 4.15/4.18)
    ivr = pd.read_csv(f'{DATA}/cbt_ivr_panel.csv')
    may = ivr[ivr.month == '2026-05'].copy()
    may = may[(may.inbound >= 200) & (may.ivr_ended < 0.95 * may.inbound)]
    may['queue_answer'] = (100 * may.answered / (may.inbound - may.ivr_ended)).clip(upper=100)
    may['ivr_share'] = 100 * may.ivr_ended / may.inbound
    cbt = may[['gp_code', 'inbound', 'queue_answer', 'ivr_share']]

    # --- Monday-Wednesday answering gap + morning IVR excess (May 2026 day/time file)
    dt = pd.read_parquet(f'{DATA}/cbt_daytime_may.parquet')
    core = dt[dt.tc.isin(['08:00-09:59', '10:00-11:59', '12:00-13:59',
                          '14:00-15:59', '16:00-17:59', '18:00-18:29'])]
    bydow = core.groupby(['gp_code', 'dow'])[['inbound', 'ivr_ended', 'answered']].sum().reset_index()
    bydow['ar'] = (100 * bydow.answered / (bydow.inbound - bydow.ivr_ended)).clip(upper=100)
    mon = bydow[bydow.dow == 1].set_index('gp_code').ar
    wed = bydow[bydow.dow == 3].set_index('gp_code').ar
    monwed = (wed - mon).rename('monwed_gap').reset_index()   # +ve = Monday answers worse

    # morning IVR tilt uses ALL time chunks as the comparator (incl. out-of-hours),
    # which reproduces the notes' median tilt of -4.1pp and the ~1-in-5 morning-heavy share
    morn = dt[dt.tc == '08:00-09:59'].groupby('gp_code')[['inbound', 'ivr_ended']].sum()
    rest = dt[dt.tc != '08:00-09:59'].groupby('gp_code')[['inbound', 'ivr_ended']].sum()
    ivx = (100 * morn.ivr_ended / morn.inbound - 100 * rest.ivr_ended / rest.inbound)
    ivx = ivx.rename('ivr_morning_excess').reset_index()

    # --- panel: May 2026 appointments + list, OC subs Feb-Apr 2026
    p = pd.read_parquet(f'{DATA}/panel_merged.parquet')
    pm = p[p.month == '2026-05'][['gp_code', 'total', 'oc_total']] \
        .rename(columns={'total': 'appts_may', 'oc_total': 'oc_may'})
    # list_size is null in the panel after Mar 2026; use the latest populated month
    lm = p[p.month == '2026-03'][['gp_code', 'list_size']].rename(columns={'list_size': 'list_may'})
    pm = pm.merge(lm, on='gp_code', how='left')
    oc = p[p.month.isin(['2026-02', '2026-03', '2026-04'])] \
        .groupby('gp_code').oc_rate_1k.mean().rename('oc_rate_febapr').reset_index()

    # --- GP composition Mar 2025 (per-10k on the xsec list denominator)
    comp = pd.read_csv(f'{DATA}/gp_composition_mar25.csv')

    d = (x.merge(cbt, on='gp_code', how='left')
          .merge(monwed, on='gp_code', how='left')
          .merge(ivx, on='gp_code', how='left')
          .merge(pm, on='gp_code', how='left')
          .merge(oc, on='gp_code', how='left')
          .merge(comp, on='gp_code', how='left', suffixes=('', '_comp')))

    L = d.list_size  # xsec 12-month GPAD-average list, the uniform per-10k denominator
    d['partner_per10k'] = 1e4 * d.partner_fte / L
    d['salaried_per10k'] = 1e4 * d.salaried_fte / L
    d['locum_per10k'] = 1e4 * d.locum_fte / L
    d['trainee_per10k'] = 1e4 * (d.registrar_fte + d.foundation_other_fte) / L
    d['training_flag'] = (d.registrar_fte > 0.25).astype(float)
    d['nurse10k_c'] = 1e4 * d.nurse_fte_comp / L
    d['dpc10k_c'] = 1e4 * d.dpc_fte_comp / L
    d['admin10k_c'] = 1e4 * d.admin_fte_comp / L
    d['fq_per10k'] = 1e4 * (d.partner_fte + d.salaried_fte + d.locum_fte) / L

    d['calls_per1k'] = 1e3 * d.inbound / d.list_size  # xsec 12m-average list (uniform denominator)
    d['contacts_per_appt'] = (d.inbound + d.oc_may.fillna(0)) / d.appts_may
    return d



OPS = ['queue_answer', 'ivr_share', 'monwed_gap', 'contacts_per_appt',
       'calls_per1k', 'oc_rate_febapr', 'same_day_pct_12m']
CIRC = ['log_list', 'imd_score', 'partner_per10k', 'salaried_per10k',
        'locum_per10k', 'trainee_per10k', 'training_flag', 'nurse10k_c',
        'dpc10k_c', 'admin10k_c', 'appts_percap', 'pct65plus', 'nonwhite_pct']
REP = ['deflection_2026', 'continuity_2026', 'has_pref_hcp_2026']
INTER = ['adm_x_size', 'adm_x_oc']
OUTCOMES = {'Q32 overall': 'satisfaction_2026',
            'Q16 contact': 'access_satisfaction_2026',
            'Q1 phone': 'phone_easy_2026'}

LAB = {'deflection_2026': 'Told to contact again (Q12)',
       'continuity_2026': 'See preferred clinician (Q7)',
       'has_pref_hcp_2026': 'Have preferred clinician (Q6)',
       'queue_answer': 'Queue-answer rate (May 2026)',
       'ivr_share': 'Calls ended within IVR %',
       'monwed_gap': 'Mon-Wed answering gap',
       'contacts_per_appt': 'Contacts per appointment',
       'calls_per1k': 'Calls received per 1,000',
       'oc_rate_febapr': 'Online subs per 1,000 (Feb-Apr)',
       'same_day_pct_12m': 'Same-day share %',
       'log_list': 'Practice size (log list)',
       'imd_score': 'Deprivation (IMD)',
       'partner_per10k': 'GP partners per 10k',
       'salaried_per10k': 'Salaried GPs per 10k',
       'locum_per10k': 'Regular locum GPs per 10k',
       'trainee_per10k': 'Trainee GPs per 10k',
       'training_flag': 'Training practice',
       'nurse10k_c': 'Nurses per 10k',
       'dpc10k_c': 'Other clinical per 10k',
       'admin10k_c': 'Admin per 10k',
       'appts_percap': 'Appointments per 1,000',
       'pct65plus': 'Patients 65+ %',
       'nonwhite_pct': 'Ethnic minority %',
       'adm_x_size': 'Admin x size',
       'adm_x_oc': 'Admin x online volume',
       'ivr_morning_excess': 'Morning-heavy IVR pattern',
       'fq_per10k': 'Fully-qualified GPs per 10k'}

rows = []   # tidy output


def zfit(m, extra_z=()):
    """z-score every model variable within the estimation sample."""
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


def ols(m, y, preds):
    X = sm.add_constant(m[['z_' + p for p in preds]])
    return sm.OLS(m[y], X).fit(cov_type='HC1')


def bank(model_name, outcome, r, preds):
    for p in preds:
        rows.append({'model': model_name, 'outcome': outcome, 'predictor': p,
                     'coef': r.params['z_' + p], 'se': r.bse['z_' + p],
                     'p': r.pvalues['z_' + p]})
    rows.append({'model': model_name, 'outcome': outcome, 'predictor': '_R2',
                 'coef': r.rsquared, 'se': np.nan, 'p': np.nan})
    rows.append({'model': model_name, 'outcome': outcome, 'predictor': '_n',
                 'coef': int(r.nobs), 'se': np.nan, 'p': np.nan})


def fmt(v, p):
    s = f'{v:+.2f}'
    return s + (' ns' if p >= 0.05 else '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xsec')
    ap.add_argument('--tag', default='live')
    a = ap.parse_args()

    d = build(a.xsec)
    d = d[d.gpps_n_2026 >= 30]

    # ---------- A. headline tables (CBT sample) ----------
    allv = OPS + CIRC + REP + list(OUTCOMES.values())
    cbt = d.dropna(subset=allv)
    cbt = cbt[cbt.contacts_per_appt <= 5]
    cbt = zfit(cbt)
    print(f'\n=== A. CBT sample: n = {len(cbt)} ===')
    for oname, y in OUTCOMES.items():
        print(f'\n--- {oname} ({y}) ---')
        print(f'{"predictor":34s} {"Alone":>9s} {"Together":>9s} {"+Report":>9s}')
        tog = ols(cbt, y, OPS + CIRC + INTER)
        rep = ols(cbt, y, OPS + CIRC + INTER + REP)
        bank('A_together', y, tog, OPS + CIRC + INTER)
        bank('A_plusreport', y, rep, OPS + CIRC + INTER + REP)
        for p in REP + OPS + CIRC + INTER:
            if p in INTER:
                al = ''
            else:
                r1 = ols(cbt, y, [p])
                bank('A_alone', y, r1, [p])
                al = fmt(r1.params['z_' + p], r1.pvalues['z_' + p])
            tg = '' if p in REP else fmt(tog.params['z_' + p], tog.pvalues['z_' + p])
            rp = fmt(rep.params['z_' + p], rep.pvalues['z_' + p])
            print(f'{LAB[p]:34s} {al:>9s} {tg:>9s} {rp:>9s}')
        print(f'{"R2":34s} {"":>9s} {tog.rsquared:>9.3f} {rep.rsquared:>9.3f}')

    # ---------- B. all-practices model (no phone measures) ----------
    nophone = [v for v in OPS if v not in
               ('queue_answer', 'ivr_share', 'monwed_gap', 'contacts_per_appt', 'calls_per1k')]
    bvars = nophone + CIRC + REP + list(OUTCOMES.values())
    allp = zfit(d.dropna(subset=bvars))
    preds_b = REP + nophone + CIRC + INTER
    print(f'\n=== B. All practices, single combined model: n = {len(allp)} ===')
    print(f'{"predictor":34s} {"Q32":>9s} {"Q16":>9s} {"Q1":>9s}')
    rs = {}
    for oname, y in OUTCOMES.items():
        rs[y] = ols(allp, y, preds_b)
        bank('B_allpractices', y, rs[y], preds_b)
    for p in preds_b:
        print(f'{LAB[p]:34s} ' + ' '.join(
            f'{fmt(rs[y].params["z_" + p], rs[y].pvalues["z_" + p]):>9s}'
            for y in OUTCOMES.values()))
    print(f'{"R2":34s} ' + ' '.join(f'{rs[y].rsquared:>9.3f}' for y in OUTCOMES.values()))

    # ---------- C. continuity (Q7) as outcome, external spec ----------
    cvars = OPS + CIRC + ['continuity_2026']
    cm = d.dropna(subset=cvars)
    cm = cm[cm.contacts_per_appt <= 5]
    cm = zfit(cm)
    rc = ols(cm, 'continuity_2026', OPS + CIRC + INTER)
    bank('C_continuity', 'continuity_2026', rc, OPS + CIRC + INTER)
    print(f'\n=== C. Continuity (Q7) from full external model: n = {len(cm)}, R2 = {rc.rsquared:.3f} ===')
    for p in ['partner_per10k', 'salaried_per10k', 'locum_per10k', 'trainee_per10k', 'training_flag']:
        print(f'{LAB[p]:34s} {fmt(rc.params["z_" + p], rc.pvalues["z_" + p]):>9s}')

    # ---------- D. validity: phone data alone ----------
    phone_preds = ['queue_answer', 'ivr_share', 'ivr_morning_excess', 'calls_per1k', 'log_list']
    dvars = phone_preds + ['phone_easy_2026', 'deflection_2026', 'couldnt_contact_2026']
    dm = zfit(d.dropna(subset=dvars))
    print(f'\n=== D. Phone data alone -> reported phone questions: n = {len(dm)} ===')
    print(f'{"outcome":28s} {"R2":>6s} {"answering":>10s} {"IVR":>8s}')
    for y in ['phone_easy_2026', 'deflection_2026', 'couldnt_contact_2026']:
        r = ols(dm, y, phone_preds)
        bank('D_phoneonly', y, r, phone_preds)
        print(f'{y:28s} {r.rsquared:>6.3f} '
              f'{fmt(r.params.z_queue_answer, r.pvalues.z_queue_answer):>10s} '
              f'{fmt(r.params.z_ivr_share, r.pvalues.z_ivr_share):>8s}')

    # ---------- E. validity: everything external -> deflection ----------
    ext = ['imd_score', 'queue_answer', 'ivr_share', 'fq_per10k', 'nonwhite_pct',
           'appts_percap', 'calls_per1k', 'oc_rate_febapr', 'contacts_per_appt',
           'same_day_pct_12m', 'ivr_morning_excess', 'log_list', 'pct65plus']
    em = d.dropna(subset=ext + ['deflection_2026'])
    em = em[em.contacts_per_appt <= 5]
    em = zfit(em)
    re_ = ols(em, 'deflection_2026', ext)
    bank('E_ext_deflection', 'deflection_2026', re_, ext)
    print(f'\n=== E. External data -> deflection (Q12): n = {len(em)}, R2 = {re_.rsquared:.3f} ===')
    for p in ext:
        print(f'{LAB[p]:34s} {fmt(re_.params["z_" + p], re_.pvalues["z_" + p]):>9s}')

    # ---------- F. descriptives ----------
    print('\n=== F1. Deflection (Q12) distribution under pressure ===')
    full = d.dropna(subset=['deflection_2026'])
    fq_cut = d.fq_per10k.quantile(0.2)
    imd_cut = d.imd_score.quantile(0.8)
    sets = {'All practices': full,
            'Fewest-FQ-GPs fifth': full[full.fq_per10k <= fq_cut],
            'Fewest GPs AND most deprived': full[(full.fq_per10k <= fq_cut) & (full.imd_score >= imd_cut)]}
    for k, s in sets.items():
        q = s.deflection_2026.quantile([.1, .5, .9])
        print(f'{k:32s} p10 {q[.1]:4.1f}  med {q[.5]:4.1f}  p90 {q[.9]:4.1f}  n {len(s)}')

    print('\n=== F2. Median queue-answer rate by admin-staffing fifth ===')
    f2 = d.dropna(subset=['queue_answer', 'admin10k_c'])
    f2 = f2.assign(fifth=pd.qcut(f2.admin10k_c, 5, labels=['Fewest', '2nd', 'Middle', '4th', 'Most']))
    print(f2.groupby('fifth', observed=True).queue_answer.median().round(1).to_string())

    out = pd.DataFrame(rows)
    out.to_csv(f'predictors_rerun_{a.tag}.csv', index=False)
    print(f'\n[written] predictors_rerun_{a.tag}.csv ({len(out)} rows)')


if __name__ == '__main__':
    main()
