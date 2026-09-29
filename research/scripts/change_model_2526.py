#!/usr/bin/env python3
"""
change_model_2526.py -- one-command rerun of the GPPS 2025 -> 2026 practice-level
change model ("what predicted the 2026 improvement").

Reconstructs the 10 Jul 2026 specification banked in PANEL_NOTES.md sections 4.2,
4.3, 4.16 and Explorer KEY_FINDING 16.  Until now that model existed only as prose
in the notes: no runner script was ever saved.  This closes the same reproducibility
gap that predictors_models.py closed for the cross-sectional page on 15 Jul.

WHAT IS ESTIMATED
  First-difference (within-practice) models of the change in patient-reported
  experience between the GPPS 2025 and GPPS 2026 waves, with the change in each
  operational exposure entered simultaneously.

  outcomes    d_satisfaction  Q32 overall experience
              d_access        Q16 experience of most recent contact
              d_phone         Q1  ease of getting through by phone
              d_deflection    Q12 told to contact the practice again  (lower = better)
              d_continuity    Q7  saw preferred clinician

  exposures   adopt           triage-first intake adoption EVENT: OC intake surge
                              >= +100 submissions/1,000/month between the two
                              fieldwork windows (supplier-agnostic, sec 4.3)
              d_oc_rate       marginal change in online intake volume (per 1,000/mo)
              d_queue_answer  change in queue-answer rate, CBT
              d_ivr_share     change in share of calls ended within the IVR
              d_admin         change in admin FTE per 10,000, Dec 2024 -> Dec 2025
              d_gp_fq         change in FULLY-QUALIFIED GP FTE per 10,000, Dec 2024 ->
                              Dec 2025, from the raw NHSE practice files
              d_trainee       change in trainee-grade GP FTE per 10,000, same window
              d_nurse,d_dpc   ditto nurses / other direct patient care

  controls    baseline outcome (mean reversion), baseline deflection, IMD 2025,
              log list size, baseline GP FTE per 10k, region fixed effects

  interaction adopt x baseline deflection (PRE-SPECIFIED, sec 4.16): does a
              transition cost more where the front door already worked?

WORKFORCE SOURCE (corrected 13 Aug 2026)
  Workforce comes from workforce_panel_rebuilt (build_workforce_panel.py, built from
  the raw NHSE practice-level censuses), NOT the old workforce_panel, which carries
  only total GP FTE (sec 4.30).  This matters: over this window total GP FTE per
  10,000 FELL 1.4% while fully-qualified ROSE 2.0% -- the two measures disagree in
  SIGN, and the gap is trainee grades.  Both are carried; fully-qualified is the
  headline, and the seven-year horizon now uses the same definition at both ends.

WINDOW ALIGNMENT (the methods lesson from sec 4.16 -- do not change casually)
  GPPS 2026 fieldwork ran 2 Jan - 13 Apr 2026; GPPS 2025 the equivalent window a
  year earlier.  Workforce is therefore read at Dec 2024 -> Dec 2025 (the quarterly
  census immediately preceding each fieldwork window), NOT Mar -> Mar.  The notes
  record that a misaligned 14-month window attenuated the GP effect from +0.23
  (p=0.036) to +0.15 (ns).  CBT waves are Mar+May 2025 vs Mar-May 2026, the months
  with usable coverage at both ends.

SAMPLE
  Two estimation samples are reported from one build, deliberately:
    CBT     practices with usable telephony at BOTH waves (the sec 4.16 sample).
    ALL     phone terms dropped, every practice with both GPPS waves.
  The CBT sample is capped by the cloud-telephony rollout, not by the survey: only
  ~3,100 practices reported CBT in spring 2025 against ~4,950 in spring 2026.  It is
  therefore SELECTED ON EARLY CBT ADOPTION, which tracks ICB procurement waves and
  practice size.  Any coefficient that holds in CBT but not in ALL should be read as
  describing early-migrating practices.  Reporting both is the point of this script.

Usage:  python3 change_model_2526.py [--data DIR] [--tag NAME]
        Data dir defaults to ../data relative to this script (override: GPOC_DATA).
Writes: change_2025_2026_<tag>.csv  (tidy coefficient table)
        change_2025_2026_<tag>_practice.csv  (the practice-level analysis file)
"""
import os
import argparse
import numpy as np
import pandas as pd
import statsmodels.api as sm
try:
    from linearmodels.iv import IV2SLS
except ImportError:
    IV2SLS = None

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('GPOC_DATA', os.path.normpath(os.path.join(HERE, '..', 'data')))

# --- window definitions (see WINDOW ALIGNMENT in the docstring) --------------
CBT_2025 = ['2025-03', '2025-05']
CBT_2026 = ['2026-03', '2026-04', '2026-05']
OC_2025 = ['2025-01', '2025-02', '2025-03']
OC_2026 = ['2026-01', '2026-02', '2026-03']
WF_2024 = '2024-12-31'
WF_2025 = '2025-12-31'
WF_2019 = '2019-12-31'          # seven-year horizon
ADOPT_SURGE = 100.0             # subs/1,000/month, sec 4.3

# --- outcomes: (label, 2025 column, 2026 column) -----------------------------
OUTCOMES = {
    'd_satisfaction': ('Q32 overall experience', 'satisfaction', 'satisfaction_2026'),
    'd_access':       ('Q16 contact experience', 'access_satisfaction', 'access_satisfaction_2026'),
    'd_phone':        ('Q1 phone ease', 'phone_easy', 'phone_easy_2026'),
    'd_deflection':   ('Q12 told to contact again', 'deflection_2025', 'deflection_2026'),
    'd_continuity':   ('Q7 saw preferred clinician', 'continuity', 'continuity_2026'),
}

PHONE_TERMS = ['d_queue_answer', 'd_ivr_share']
CORE_TERMS = ['adopt', 'd_oc_rate', 'd_admin', 'd_gp_fq', 'd_trainee', 'd_nurse', 'd_dpc']
CONTROLS = ['base_outcome', 'base_deflection', 'imd_score', 'log_list', 'base_gp_fq']

LAB = {
    'adopt': 'Adopted triage-first intake (event)',
    'd_oc_rate': 'Change in online intake volume',
    'd_queue_answer': 'Change in queue-answer rate',
    'd_ivr_share': 'Change in IVR-ended share',
    'd_admin': 'Change in admin FTE per 10k',
    'd_gp_fq': 'Change in FULLY-QUALIFIED GP per 10k',
    'd_trainee': 'Change in trainee-grade GP per 10k',
    'd_gp_total': 'Change in total GP FTE per 10k',
    'd_nurse': 'Change in nurse FTE per 10k',
    'd_dpc': 'Change in other clinical FTE per 10k',
    'd_gp_fq_7yr': 'Change in FQ GP per 10k (7 year)',
    'base_outcome': 'Baseline level of the outcome',
    'base_deflection': 'Baseline deflection (Q12)',
    'imd_score': 'Deprivation (IMD 2025)',
    'log_list': 'Practice size (log list)',
    'base_gp_fq': 'Baseline fully-qualified GP per 10k',
    'adopt_x_defl': 'Adoption x baseline deflection',
}

rows = []


# ---------------------------------------------------------------- build -----
def cbt_wave(cbt, months):
    """Aggregate the CBT panel over a fieldwork-aligned window.

    Quality filters follow sec 4.15/4.18: >=200 inbound calls in the window and
    fewer than 95% of calls ending inside the IVR (a near-100% IVR share means the
    practice is not exposing a queue at all, so the answer rate is undefined).
    Queue-answer rate is answered / (inbound - ivr_ended), capped at 100.
    """
    s = (cbt[cbt.month.isin(months)]
         .groupby('gp_code')[['inbound', 'ivr_ended', 'answered']].sum())
    s = s[(s.inbound >= 200) & (s.ivr_ended < 0.95 * s.inbound)]
    out = pd.DataFrame({
        'queue_answer': (100 * s.answered / (s.inbound - s.ivr_ended)).clip(upper=100),
        'ivr_share': 100 * s.ivr_ended / s.inbound,
    })
    return out


def _coalesce(s, *cols):
    """First non-null across alternately-named columns.

    TRAP (found 13 Aug 2026 while writing this script): workforce_panel.parquet
    switches column names between publication vintages.  Nurses are `nurse_fte`
    for 2018-03..2019-03 and again from 2025-09, but `nurses_fte` for the whole
    2019-06..2025-06 stretch.  Fully-qualified GPs are `gp_fte_fq` in some early
    vintages and `gp_exrl_fte` in others, and NEITHER is populated after 2021-03.
    Reading a single name silently yields an all-null difference -- which is what
    a naive Dec 2024 -> Dec 2025 nurse or FQ-GP delta produces.  Always coalesce.
    """
    out = None
    for c in cols:
        if c in s.columns:
            out = s[c] if out is None else out.fillna(s[c])
    return out


def wf_snapshot(wf, date):
    """Workforce per 10,000 registered patients at one quarterly census.

    Retained only for the SEVEN-YEAR total-GP comparison and as a cross-check on
    the raw-file build.  The panel's `gp_fte` is TOTAL GP FTE (sec 4.30); the
    in-year headline terms come from workforce_dec24_dec25.csv instead.
    """
    s = wf[wf.date == date].copy()
    s = s[s.patients > 0]
    per10k = 1e4 / s.patients
    return pd.DataFrame({
        'gp_code': s.prac.values,
        'gp': (s.gp_fte * per10k).values,
        'nurse': (_coalesce(s, 'nurse_fte', 'nurses_fte') * per10k).values,
        'dpc': (s.dpc_fte * per10k).values,
        'admin': (s.admin_fte * per10k).values,
    }).groupby('gp_code').mean()


def build(data=DATA):
    x = pd.read_parquet(f'{data}/xsec_master_2026.parquet')
    cbt = pd.read_csv(f'{data}/cbt_ivr_panel.csv')
    p = pd.read_parquet(f'{data}/panel_merged.parquet')

    # --- telephony change, fieldwork-aligned
    c25, c26 = cbt_wave(cbt, CBT_2025), cbt_wave(cbt, CBT_2026)
    dcbt = (c26 - c25).dropna()
    dcbt.columns = ['d_queue_answer', 'd_ivr_share']
    dcbt = dcbt.reset_index()

    # --- online intake change + the adoption event
    oc25 = p[p.month.isin(OC_2025)].groupby('gp_code').oc_rate_1k.mean().rename('oc_25')
    oc26 = p[p.month.isin(OC_2026)].groupby('gp_code').oc_rate_1k.mean().rename('oc_26')
    oc = pd.concat([oc25, oc26], axis=1).dropna()
    oc['d_oc_rate'] = oc.oc_26 - oc.oc_25
    oc['adopt'] = (oc.d_oc_rate >= ADOPT_SURGE).astype(float)
    oc = oc.reset_index()

    # --- workforce change Dec 2024 -> Dec 2025, from the RAW NHSE censuses.
    # Carries fully-qualified AND trainee grades separately, which the derived
    # panel cannot (sec 4.30). Build with: python3 build_workforce_dec.py
    wp = pd.read_parquet(f'{data}/workforce_panel_rebuilt.parquet')
    def snap(period):
        s_ = wp[wp.period == period].set_index('prac')
        return s_[['gp_fte_fq_per10k', 'gp_trainee_per10k', 'gp_per10k',
                   'nurse_per10k', 'dpc_per10k', 'admin_per10k']]
    a24, a25 = snap(202412), snap(202512)
    dwf = (a25 - a24).dropna(how='all')
    dwf.columns = ['d_gp_fq', 'd_trainee', 'd_gp_total', 'd_nurse', 'd_dpc', 'd_admin']
    dwf['base_gp_fq'] = a24.gp_fte_fq_per10k
    # seven-year FQ horizon on ONE consistent definition (Dec 2018 -> Dec 2025).
    # Dec 2018 sits just after the Jun-2018 total-GP series break, but the
    # fully-qualified series is continuous across it (see build_workforce_panel.py).
    a18 = snap(201812)
    dwf['d_gp_fq_7yr'] = a25.gp_fte_fq_per10k - a18.gp_fte_fq_per10k
    dwf = dwf.reset_index().rename(columns={'prac': 'gp_code'})


    d = (x.merge(dcbt, on='gp_code', how='left')
          .merge(oc[['gp_code', 'd_oc_rate', 'adopt']], on='gp_code', how='left')
          .merge(dwf, on='gp_code', how='left'))

    # --- outcome differences; both waves must clear the GPPS reporting threshold
    ok = (d.gpps_n >= 30) & (d.gpps_n_2026 >= 30)
    for dcol, (_, c25c, c26c) in OUTCOMES.items():
        d[dcol] = np.where(ok, d[c26c] - d[c25c], np.nan)
    d['base_deflection'] = d.deflection_2025
    return d


# ---------------------------------------------------------------- fit -------
def zfit(m, terms):
    """z-score continuous terms within the estimation sample.

    `adopt` stays binary so its coefficient reads in percentage points, matching
    how sec 4.16 reports it ("-1.8 to -2.3pp"), and the interaction is built from
    the binary flag times the z-scored baseline, so it reads as pp per SD.
    """
    m = m.copy()
    for v in terms:
        if v == 'adopt':
            m['z_adopt'] = m.adopt
        else:
            sd = m[v].std()
            m['z_' + v] = (m[v] - m[v].mean()) / sd if sd > 0 else 0.0
    if 'adopt' in terms and 'base_deflection' in terms:
        m['z_adopt_x_defl'] = m.z_adopt * m.z_base_deflection
    return m


def ols(m, y, preds):
    X = pd.get_dummies(m[['region']], drop_first=True, dtype=float)
    X = pd.concat([m[['z_' + p for p in preds]], X], axis=1)
    return sm.OLS(m[y], sm.add_constant(X)).fit(cov_type='HC1')


def bank(sample, outcome, r, preds):
    for p in preds:
        rows.append({'sample': sample, 'outcome': outcome, 'predictor': p,
                     'label': LAB.get(p, p), 'coef': r.params['z_' + p],
                     'se': r.bse['z_' + p], 'p': r.pvalues['z_' + p]})
    rows.append({'sample': sample, 'outcome': outcome, 'predictor': '_R2',
                 'label': 'R-squared', 'coef': r.rsquared, 'se': np.nan, 'p': np.nan})
    rows.append({'sample': sample, 'outcome': outcome, 'predictor': '_n',
                 'label': 'n practices', 'coef': int(r.nobs), 'se': np.nan, 'p': np.nan})


def fmt(v, p):
    return f'{v:+.2f}' + ('' if p < 0.05 else ' ns')


def run(d, sample, terms, tag_note):
    preds_base = terms + CONTROLS
    need = [c for c in preds_base if c != 'base_outcome'] + ['region']
    print(f'\n{"=" * 78}\n{sample}: {tag_note}\n{"=" * 78}')
    fitted = {}
    for dcol, (label, base_col, _) in OUTCOMES.items():
        # baseline level of THIS outcome -- the mean-reversion control
        m = d.assign(base_outcome=d[base_col]).dropna(subset=need + [dcol, base_col])
        m = zfit(m, preds_base)
        preds = preds_base + (['adopt_x_defl'] if 'adopt' in terms else [])
        r = ols(m, dcol, preds)
        bank(sample, dcol, r, preds)
        fitted[dcol] = (r, preds, int(r.nobs))

    order = (terms + ['adopt_x_defl'] if 'adopt' in terms else terms) + CONTROLS
    order = [o for o in order if o in fitted['d_satisfaction'][1]]
    head = ' '.join(f'{lbl.split()[0]:>10s}' for lbl, _, _ in OUTCOMES.values())
    print(f'{"predictor":38s} {head}')
    for p in order:
        cells = []
        for dcol in OUTCOMES:
            r, _, _ = fitted[dcol]
            cells.append(f'{fmt(r.params["z_" + p], r.pvalues["z_" + p]):>10s}')
        print(f'{LAB[p]:38s} ' + ' '.join(cells))
    print(f'{"R-squared":38s} ' + ' '.join(
        f'{fitted[c][0].rsquared:>10.3f}' for c in OUTCOMES))
    print(f'{"n":38s} ' + ' '.join(f'{fitted[c][2]:>10d}' for c in OUTCOMES))


def errors_in_variables(d, data):
    """Correct the mean-reversion control for sampling error in the GPPS baseline.

    THE PROBLEM (resolved 14 Aug 2026).  Controlling a difference score for its own
    baseline is the standard guard against regression to the mean, but it assumes the
    baseline is measured WITHOUT error.  A GPPS practice score is a sample statistic --
    a few hundred respondents per practice -- so it is not.  Controlling for a noisy
    baseline OVER-corrects: some of the coefficient is soaking up sampling noise rather
    than real starting level, and any exposure correlated with the baseline is
    attenuated with it.

    THE FIX.  The 2024 wave is an independent noisy measurement of the same underlying
    practice level, so it instruments the 2025 baseline: the sampling errors are drawn
    from different surveys and are uncorrelated, while the true levels are shared.
    Comparing the baseline coefficient with and without the instrument quantifies how
    much of the apparent mean reversion was measurement error.

    RESULT: for contact experience (Q16) the baseline coefficient moves from -4.84 to
    -1.28 when instrumented, and the queue-answering effect moves from +0.22 (ns) to
    +0.50 (p=0.003) -- reproducing the figure banked in sec 4.16.  The uncorrected
    specification, not the banked one, was the wrong reading.

    ASSUMPTION worth stating: the 2024 score affects the 2025->2026 change only through
    the 2025 level.  Practice-specific trends would violate that; the first stage is
    strong (t>30) and the direction of the correction is what classical measurement
    error predicts, but this is an assumption, not a proof.

    Needs gpps_2024_extra.csv (Q16/Q1 2024 columns; see ingest_gpps2024_extra.py).
    """
    if IV2SLS is None:
        print('\n[skip] errors-in-variables pass needs `pip install linearmodels`')
        return
    try:
        extra = pd.read_csv(f'{data}/gpps_2024_extra.csv')
    except FileNotFoundError:
        extra = pd.DataFrame(columns=['gp_code'])
    m0 = d.merge(extra, on='gp_code', how='left')
    pairs = [('d_satisfaction', 'satisfaction', 'satisfaction_2024', 'd_queue_answer'),
             ('d_access', 'access_satisfaction', 'access_satisfaction_2024', 'd_queue_answer'),
             ('d_phone', 'phone_easy', 'phone_easy_2024', 'd_ivr_share'),
             ('d_continuity', 'continuity', 'continuity_2024', 'd_queue_answer')]
    terms = CORE_TERMS + PHONE_TERMS + [c for c in CONTROLS if c != 'base_outcome']
    print(f'\n{"=" * 78}\nERRORS-IN-VARIABLES: 2025 baseline instrumented by the 2024 wave'
          f'\n{"=" * 78}')
    print(f'{"outcome / exposure":38s} {"no base":>9s} {"base raw":>9s} {"base IV":>9s} '
          f'{"base coef raw->IV":>19s}')
    for dcol, b25, b24, tgt in pairs:
        if b24 not in m0.columns:
            print(f'{dcol:38s} (2024 column not available)')
            continue
        mm = m0.dropna(subset=terms + ['region', dcol, b25, b24]).copy()
        for v in terms + [b25, b24]:
            mm['z_' + v] = mm[v] if v == 'adopt' else (mm[v] - mm[v].mean()) / mm[v].std()
        mm['z_adopt_x_defl'] = mm.z_adopt * mm.z_base_deflection
        R = pd.get_dummies(mm[['region']], drop_first=True, dtype=float)
        X = pd.concat([mm[['z_' + v for v in terms] + ['z_adopt_x_defl']], R], axis=1)
        y = mm[dcol]
        a = sm.OLS(y, sm.add_constant(X)).fit(cov_type='HC1')
        b = sm.OLS(y, sm.add_constant(pd.concat([X, mm[['z_' + b25]]], axis=1))).fit(cov_type='HC1')
        c = IV2SLS(y, sm.add_constant(X), mm[['z_' + b25]], mm[['z_' + b24]]).fit(cov_type='robust')
        for nm, r in [('EIV_nobase', a), ('EIV_baseraw', b), ('EIV_baseIV', c)]:
            rows.append({'sample': nm, 'outcome': dcol, 'predictor': tgt, 'label': LAB[tgt],
                         'coef': float(r.params['z_' + tgt]), 'se': float(r.std_errors['z_' + tgt])
                         if hasattr(r, 'std_errors') else float(r.bse['z_' + tgt]),
                         'p': float(r.pvalues['z_' + tgt])})
        f = lambda r: (f"{float(r.params['z_' + tgt]):+.2f}"
                       + ('' if float(r.pvalues['z_' + tgt]) < 0.05 else '*'))
        print(f'{dcol + " / " + tgt:38s} {f(a):>9s} {f(b):>9s} {f(c):>9s} '
              f'{float(b.params["z_" + b25]):+.2f} -> {float(c.params["z_" + b25]):+.2f}'.rjust(9))
    print('* = not significant at p<0.05.  Banked in sec 4.16: Q16/answering +0.50.')


def sensitivity(d):
    """Why the telephony coefficients do not reproduce sec 4.16 (13 Aug 2026).

    Sec 4.3 states the change models control for the BASELINE OUTCOME (the standard
    mean-reversion control on a difference score).  Sec 4.16's banked telephony
    coefficients only reproduce when that control is ABSENT: with it, the queue-
    answering effects roughly halve and fall out of significance.  The two notes
    sections are therefore internally inconsistent, and the "broadest lever"
    reading of queue answering rests on the weaker of the two specifications.
    The ladder below is printed every run so the choice stays visible.
    """
    ladder = {
        'full (headline)': CORE_TERMS + PHONE_TERMS + CONTROLS,
        'no baseline outcome': CORE_TERMS + PHONE_TERMS
                               + [c for c in CONTROLS if c != 'base_outcome'],
        'no baseline deflection': CORE_TERMS + PHONE_TERMS
                                  + [c for c in CONTROLS if c != 'base_deflection'],
        'no adoption event': [c for c in CORE_TERMS if c != 'adopt']
                             + PHONE_TERMS + CONTROLS,
        'phone terms + controls': PHONE_TERMS + CONTROLS,
        'phone terms alone': PHONE_TERMS,
    }
    targets = [('d_access', 'Q16', 'd_queue_answer'),
               ('d_deflection', 'Q12', 'd_queue_answer'),
               ('d_phone', 'Q1', 'd_ivr_share')]
    print(f'\n{"=" * 78}\nSENSITIVITY: telephony terms vs the mean-reversion control\n{"=" * 78}')
    print(f'{"specification":26s} {"dAnswer->Q16":>13s} {"dAnswer->Q12":>13s} '
          f'{"IVRfall->Q1":>12s} {"n":>6s}')
    print(f'{"banked in sec 4.16":26s} {"+0.50":>13s} {"-0.20":>13s} {"+1.00":>12s} {2751:>6d}')
    for name, terms in ladder.items():
        cells, n = [], 0
        for dcol, _, tgt in targets:
            base_col = OUTCOMES[dcol][1]
            need = [c for c in terms if c != 'base_outcome'] + ['region', dcol, base_col]
            m = d.assign(base_outcome=d[base_col]).dropna(subset=need)
            m = zfit(m, terms)
            extra = ['adopt_x_defl'] if ('adopt' in terms and 'base_deflection' in terms) else []
            r = ols(m, dcol, terms + extra)
            coef, pv, n = r.params['z_' + tgt], r.pvalues['z_' + tgt], int(r.nobs)
            rows.append({'sample': f'SENS:{name}', 'outcome': dcol, 'predictor': tgt,
                         'label': LAB[tgt], 'coef': coef, 'se': r.bse['z_' + tgt], 'p': pv})
            # IVR is reported as the effect of a FALL, to match the notes' wording
            cells.append(f'{-coef if tgt == "d_ivr_share" else coef:+.2f}'
                         + ('' if pv < 0.05 else '*'))
        print(f'{name:26s} {cells[0]:>13s} {cells[1]:>13s} {cells[2]:>12s} {n:>6d}')
    print('* = not significant at p<0.05. Last column = effect of a FALL in IVR share.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default=DATA)
    ap.add_argument('--tag', default='rerun')
    a = ap.parse_args()

    d = build(a.data)

    # coverage note -- the sample story, printed every run so it cannot be lost again
    n_gpps = d.dropna(subset=['d_satisfaction']).shape[0]
    n_cbt = d.dropna(subset=['d_satisfaction', 'd_queue_answer']).shape[0]
    print(f'\n[coverage] both GPPS waves (n>=30): {n_gpps}')
    print(f'[coverage] + usable CBT at both waves: {n_cbt}'
          f'  ({100 * n_cbt / n_gpps:.0f}% -- capped by the 2025 telephony rollout,'
          f' not by the survey)')
    print(f'[coverage] adoption events (OC surge >= +{ADOPT_SURGE:.0f}/1k/mo): '
          f'{int(d.adopt.sum())}')

    run(d, 'CBT', CORE_TERMS + PHONE_TERMS,
        'phone terms in; sec 4.16 sample; selected on early CBT migration')
    run(d, 'ALL', CORE_TERMS,
        'phone terms dropped; every practice with both GPPS waves')

    # seven-year GP horizon, reported separately in sec 4.16
    print(f'\n{"=" * 78}\nSeven-year FULLY-QUALIFIED GP horizon (Dec 2018 -> Dec 2025), all practices\n{"=" * 78}')
    for dcol, (label, base_col, _) in OUTCOMES.items():
        terms = ['adopt', 'd_oc_rate', 'd_gp_fq_7yr'] + CONTROLS
        need7 = [c for c in terms if c != 'base_outcome']
        m = d.assign(base_outcome=d[base_col]).dropna(subset=need7 + ['region', dcol, base_col])
        m = zfit(m, terms)
        r = ols(m, dcol, terms + ['adopt_x_defl'])
        bank('7YR', dcol, r, terms + ['adopt_x_defl'])
        print(f'{label:38s} {fmt(r.params.z_d_gp_fq_7yr, r.pvalues.z_d_gp_fq_7yr):>10s}'
              f'   (n={int(r.nobs)})')

    sensitivity(d)
    errors_in_variables(d, a.data)

    out = pd.DataFrame(rows)
    out.to_csv(f'change_2025_2026_{a.tag}.csv', index=False)
    keep = ['gp_code', 'gp_name', 'region', 'imd_score', 'log_list', 'list_size',
            'adopt', 'd_oc_rate', 'd_queue_answer', 'd_ivr_share', 'd_admin',
            'd_gp_fq', 'd_trainee', 'd_gp_total', 'd_nurse', 'd_dpc',
            'd_gp_fq_7yr', 'base_gp_fq',
            'base_deflection'] + list(OUTCOMES)
    d[[c for c in keep if c in d.columns]].to_csv(
        f'change_2025_2026_{a.tag}_practice.csv', index=False)
    print(f'\n[written] change_2025_2026_{a.tag}.csv ({len(out)} rows)')
    print(f'[written] change_2025_2026_{a.tag}_practice.csv')


if __name__ == '__main__':
    main()
