#!/usr/bin/env python3
"""
build_workforce_panel.py -- rebuild the practice workforce panel from the RAW NHSE
practice-level censuses, carrying the fully-qualified / trainee GP split throughout.

WHY
`workforce_panel.{csv,parquet}` carries only TOTAL GP FTE, and its nurse column
changes name between publication vintages (PANEL_NOTES sec 4.30 and the trap noted
in change_model_2526.py).  Neither limitation is in the source data: every NHSE
practice-level census from September 2015 onward publishes the full role breakdown.
This script rebuilds the panel from those files so downstream work never has to ask
which GP definition it is holding.

WHY IT MATTERS: over Dec 2024 -> Dec 2025 total GP FTE per 10,000 patients FELL 1.4%
while FULLY-QUALIFIED GP FTE ROSE 2.0%.  The two definitions disagree in sign; the
difference is trainee grades.  A panel that carries only the total silently forces
whichever answer the total happens to give.

THE VINTAGE BRIDGE (the reason this is not a two-line extract)
NHSE renamed the GP columns partway through the series:
    2015-2019 vintage   TOTAL_GP_EXR_FTE    excludes REGISTRARS only
                        TOTAL_GP_EXRL_FTE   excludes registrars and locums
                        TOTAL_GP_REG_ST1_4_FTE / TOTAL_GP_REG_F1_2_FTE  reported separately
    2020-2026 vintage   TOTAL_GP_EXTG_FTE   excludes ALL TRAINEE GRADES (registrars + F1/F2)
                        TOTAL_GP_EXTGL_FTE  excludes trainee grades and locums
EXR and EXTG are NOT the same measure: EXR still contains foundation doctors.  To get
one consistent series, fully-qualified is computed on the old vintage as
    TOTAL_GP_FTE - TOTAL_GP_REG_ST1_4_FTE - TOTAL_GP_REG_F1_2_FTE
which reproduces the EXTG definition, rather than by reading EXR and hoping.  The
`fq_source` column records which route each row took, so the join is auditable.

Nurses are `TOTAL_NURSES_FTE` in every vintage of the RAW file -- the alternating
`nurse_fte`/`nurses_fte` names were introduced by the old derived panel, not by NHSE.

BACKWARD COMPATIBILITY
Every column name in the existing panel is preserved and populated, so code reading
`workforce_panel` can point at the rebuild unchanged:
    period, prac, patients, gp_fte, gp_fte_fq, nurse_fte, dpc_fte, admin_fte,
    gp_exrl_fte, nurses_fte, date, gp_fte_fq_per10k
`nurse_fte` and `nurses_fte` are both populated with the same values, so neither
spelling can silently return nulls again.  New columns are added alongside:
    gp_trainee_fte, gp_fq_exlocum_fte, gp_locum_fte, and per-10k versions.

Usage:  python3 build_workforce_panel.py --src DIR [--out PREFIX]
        --src holds the downloaded GPW practice-level zips.
Source: NHS England, General Practice Workforce (practice-level CSVs).
        https://digital.nhs.uk/data-and-information/publications/statistical/
        general-and-personal-medical-services
"""
import os
import re
import glob
import zipfile
import argparse
import numpy as np
import pandas as pd

MONTHS = {m: i for i, m in enumerate(
    ['january', 'february', 'march', 'april', 'may', 'june', 'july',
     'august', 'september', 'october', 'november', 'december'], start=1)}

# columns wanted, by role. Values are candidate source names, first match wins.
DIRECT = {
    'prac': ['PRAC_CODE'],
    'patients': ['TOTAL_PATIENTS'],
    'gp_fte': ['TOTAL_GP_FTE'],
    'nurse_fte': ['TOTAL_NURSES_FTE'],
    'dpc_fte': ['TOTAL_DPC_FTE'],
    'admin_fte': ['TOTAL_ADMIN_FTE'],
}
# fully-qualified: modern column if present, else derived (see THE VINTAGE BRIDGE)
FQ_MODERN = 'TOTAL_GP_EXTG_FTE'
FQ_EXLOCUM_MODERN = 'TOTAL_GP_EXTGL_FTE'
FQ_EXLOCUM_OLD = 'TOTAL_GP_EXRL_FTE'
TRAINEE_PARTS = ['TOTAL_GP_REG_ST1_4_FTE', 'TOTAL_GP_REG_F1_2_FTE']
TRAINEE_PARTS_NEW = ['TOTAL_GP_TRN_GR_ST1_FTE', 'TOTAL_GP_TRN_GR_ST2_FTE',
                     'TOTAL_GP_TRN_GR_ST3_FTE', 'TOTAL_GP_TRN_GR_ST4_FTE',
                     'TOTAL_GP_TRN_GR_OTH_FTE', 'TOTAL_GP_TRN_GR_F1_2_FTE']
LOCUM_PARTS = ['TOTAL_GP_LOCUM_VAC_FTE', 'TOTAL_GP_LOCUM_ABS_FTE',
               'TOTAL_GP_LOCUM_OTH_FTE']


def period_from_name(name):
    """(YYYYMM, date) parsed from a census filename, or None if not a data file."""
    base = os.path.basename(name)
    if 'definition' in base.lower() or 'metadata' in base.lower():
        return None
    m = re.search(r'(' + '|'.join(MONTHS) + r')[ _]+(\d{4})', base, re.I)
    if m:
        mm, yy = MONTHS[m.group(1).lower()], int(m.group(2))
    else:  # e.g. "... Mar 2018 ..."
        m = re.search(r'\b([A-Z][a-z]{2})[ _]+(\d{4})', base)
        if not m:
            return None
        cand = [k for k in MONTHS if k.startswith(m.group(1).lower())]
        if not cand:
            return None
        mm, yy = MONTHS[cand[0]], int(m.group(2))
    return yy * 100 + mm, pd.Timestamp(yy, mm, 1) + pd.offsets.MonthEnd(0)


def pub_vintage(zipname):
    """YYYYMM of the PUBLICATION a file came from.

    Several editions ship a cumulative back-series (the Dec 2019 and Dec 2021
    archives each republish every earlier period), so most practice-periods appear
    in more than one zip.  NHSE revises figures between editions, so the correct
    tie-break is "most recently published wins" -- not filename order, which is
    meaningless.  This extracts the publication stamp so that rule can be applied.
    """
    b = os.path.basename(zipname)
    m = re.search(r'\.(\d{2})(\d{4})\.zip$', b)          # GPWPracticeCSV.122024.zip
    if m:
        return int(m.group(2)) * 100 + int(m.group(1))
    m = re.search(r'\.(\d{2})(\d{2})\.zip$', b)          # GPWPracticeCSV.1219.zip
    if m:
        return (2000 + int(m.group(2))) * 100 + int(m.group(1))
    p = period_from_name(b.replace('%20', ' '))          # e.g. "... Mar 2018 ..."
    return p[0] if p else 0


def pick(cols, names):
    for n in names:
        if n in cols:
            return n
    return None


def read_one(zf, name, cols_cache):
    """Read one census CSV into the canonical schema."""
    with zf.open(name) as fh:
        head = fh.readline().decode('utf-8-sig', 'replace')
    cols = [c.strip().strip('"') for c in head.split(',')]

    take, ren = [], {}
    for out, cands in DIRECT.items():
        src = pick(cols, cands)
        if src is None:
            return None, f'missing {out}'
        take.append(src)
        ren[src] = out

    fq_src = FQ_MODERN if FQ_MODERN in cols else None
    parts = [p for p in (TRAINEE_PARTS if fq_src is None else []) if p in cols]
    if fq_src is None and not parts:
        parts = [p for p in TRAINEE_PARTS_NEW if p in cols]
    if fq_src is None and not parts:
        return None, 'no route to fully-qualified'
    take += ([fq_src] if fq_src else []) + parts
    exl = pick(cols, [FQ_EXLOCUM_MODERN, FQ_EXLOCUM_OLD])
    if exl:
        take.append(exl)
    locum = [c for c in LOCUM_PARTS if c in cols]
    take += locum

    with zf.open(name) as fh:
        df = pd.read_csv(fh, usecols=lambda c: c.strip().strip('"').lstrip('﻿') in take,
                         low_memory=False, encoding='utf-8-sig')
    df.columns = [c.strip().strip('"').lstrip('﻿') for c in df.columns]
    for c in df.columns:
        if c != 'PRAC_CODE':
            df[c] = pd.to_numeric(df[c], errors='coerce')

    if fq_src:
        df['gp_fte_fq'] = df[fq_src]
        src_label = 'EXTG'
    else:
        df['gp_fte_fq'] = df[DIRECT['gp_fte'][0]] - df[parts].sum(axis=1)
        src_label = 'derived(total-trainees)'
    df['gp_fq_exlocum_fte'] = df[exl] if exl else np.nan
    df['gp_locum_fte'] = df[locum].sum(axis=1) if locum else np.nan
    df = df.rename(columns=ren)
    keep = ['prac', 'patients', 'gp_fte', 'gp_fte_fq', 'gp_fq_exlocum_fte',
            'gp_locum_fte', 'nurse_fte', 'dpc_fte', 'admin_fte']
    out = df[keep].groupby('prac', as_index=False).sum(min_count=1)
    out['fq_source'] = src_label
    cols_cache.append(len(cols))
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='.')
    ap.add_argument('--out', default='workforce_panel_rebuilt')
    a = ap.parse_args()

    frames, skipped, widths = [], [], []
    for z in sorted(glob.glob(os.path.join(a.src, '*.zip'))):
        with zipfile.ZipFile(z) as zf:
            csvs = [n for n in zf.namelist() if n.lower().endswith('.csv')]
            # where a vintage ships both, the Detailed file carries the role split
            detailed = [n for n in csvs if 'Detailed' in n]
            for n in (detailed or csvs):
                pd_ = period_from_name(n)
                if pd_ is None:
                    continue
                period, date = pd_
                df, err = read_one(zf, n, widths)
                if df is None:
                    skipped.append((os.path.basename(z), period, err))
                    continue
                df['period'], df['date'] = period, date
                df['pub_vintage'] = pub_vintage(z)
                frames.append(df)

    panel = pd.concat(frames, ignore_index=True)
    # a period can appear in more than one publication (revisions / the cumulative
    # 2021 archive). Keep the LAST published value for each practice-period.
    dupes = panel.duplicated(['prac', 'period'], keep=False).sum()
    # most recently PUBLISHED value wins (see pub_vintage)
    panel = (panel.sort_values(['prac', 'period', 'pub_vintage'])
                  .drop_duplicates(['prac', 'period'], keep='last')
                  .sort_values(['period', 'prac']))

    # derived: trainee grades, and the per-10k series
    panel['gp_trainee_fte'] = panel.gp_fte - panel.gp_fte_fq
    per10k = 1e4 / panel.patients.where(panel.patients > 0)
    for src, dst in [('gp_fte', 'gp_per10k'), ('gp_fte_fq', 'gp_fte_fq_per10k'),
                     ('gp_trainee_fte', 'gp_trainee_per10k'),
                     ('nurse_fte', 'nurse_per10k'), ('dpc_fte', 'dpc_per10k'),
                     ('admin_fte', 'admin_per10k')]:
        panel[dst] = panel[src] * per10k

    # backward compatibility with the old panel's alternating names
    panel['nurses_fte'] = panel.nurse_fte          # both spellings, same values
    panel['gp_exrl_fte'] = panel.gp_fq_exlocum_fte

    order = ['period', 'date', 'prac', 'patients', 'gp_fte', 'gp_fte_fq',
             'gp_trainee_fte', 'gp_fq_exlocum_fte', 'gp_exrl_fte', 'gp_locum_fte',
             'nurse_fte', 'nurses_fte', 'dpc_fte', 'admin_fte', 'gp_per10k',
             'gp_fte_fq_per10k', 'gp_trainee_per10k', 'nurse_per10k',
             'dpc_per10k', 'admin_per10k', 'fq_source', 'pub_vintage']
    panel = panel[order]
    panel.to_csv(f'{a.out}.csv', index=False)
    panel.to_parquet(f'{a.out}.parquet', index=False)

    periods = sorted(panel.period.unique())
    print(f'[built] {len(panel):,} practice-periods | {panel.prac.nunique():,} practices '
          f'| {len(periods)} periods {periods[0]} .. {periods[-1]}')
    print(f'[dupes] {dupes:,} practice-period rows appeared in more than one edition; '
          f'kept the most recently published')
    if skipped:
        print('[skipped]')
        for s in skipped:
            print('   ', s)
    print('\n[fq_source by period]')
    tab = panel.groupby(['period', 'fq_source']).size().unstack(fill_value=0)
    print(tab.to_string())
    print(f'\n[written] {a.out}.csv / .parquet')


if __name__ == '__main__':
    main()
