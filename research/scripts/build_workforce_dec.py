#!/usr/bin/env python3
"""
build_workforce_dec.py  [SUPERSEDED by build_workforce_panel.py, 13 Aug 2026 --
that script builds the whole 2015-2026 panel on this same basis. Kept because
it is the minimal two-census extract and is quicker to eyeball.] -- practice-level workforce at Dec 2024 and Dec 2025,
including FULLY-QUALIFIED GP FTE, from the raw NHSE practice-level files.

WHY THIS EXISTS
`workforce_panel.{csv,parquet}` carries only TOTAL GP FTE (registrars and locums
included) -- see PANEL_NOTES sec 4.30: "fully-qualified (EXRL) is captured only for
2018 (NHS renamed the column)".  That is a limitation of the DERIVED panel, not of
the source: every quarterly NHSE practice-level detailed CSV carries the full role
breakdown.  This script pulls the two censuses the 2025->2026 change model needs
(Dec 2024 and Dec 2025, the quarters immediately preceding each GPPS fieldwork
window) and writes a small per-practice file with both GP definitions.

COLUMN MEANINGS (NHSE detailed practice-level file)
  TOTAL_GP_FTE          all GPs, including trainee grades and locums
  TOTAL_GP_EXTG_FTE     excluding TRAINEE GRADES  = NHSE "fully qualified".
                        Includes regular locums (vacancy/absence/other cover);
                        excludes ad-hoc locums entirely, which are published only
                        in national annexes (sec 4.30, AMC locum-boundary query).
  TOTAL_GP_EXTGL_FTE    excluding trainee grades AND locums
  trainee (derived)     TOTAL_GP_FTE - TOTAL_GP_EXTG_FTE

THE TWO GP MEASURES MOVE IN OPPOSITE DIRECTIONS OVER THIS WINDOW
  per 10,000 patients, Dec 2024 -> Dec 2025:
      total GP        5.855 -> 5.775   (-1.4%)
      fully qualified 4.390 -> 4.477   (+2.0%)
  so which column you read decides the sign of the in-year GP story.  Do not
  substitute one for the other.

Usage:  python3 build_workforce_dec.py [--src DIR] [--out FILE]
        --src holds GPWPracticeCSV.122024.zip / .122025.zip (or the unzipped dirs).
Source: NHS England, General Practice Workforce, 31 December 2024 / 31 December 2025.
        https://digital.nhs.uk/data-and-information/publications/statistical/
        general-and-personal-medical-services/31-december-2025
"""
import os
import glob
import zipfile
import argparse
import pandas as pd

WANT = {
    'PRAC_CODE': 'gp_code',
    'TOTAL_PATIENTS': 'patients',
    'TOTAL_GP_FTE': 'gp_total',
    'TOTAL_GP_EXTG_FTE': 'gp_fq',
    'TOTAL_GP_EXTGL_FTE': 'gp_fq_exlocum',
    'TOTAL_NURSES_FTE': 'nurse',
    'TOTAL_DPC_FTE': 'dpc',
    'TOTAL_ADMIN_FTE': 'admin',
}
WAVES = {'24': '122024', '25': '122025'}


def load(src, stamp):
    """Find (unzipping if needed) and read one census's detailed practice file."""
    d = os.path.join(src, f'GPWPracticeCSV.{stamp}')
    if not os.path.isdir(d):
        z = os.path.join(src, f'GPWPracticeCSV.{stamp}.zip')
        if not os.path.exists(z):
            raise SystemExit(f'[fatal] neither {d}/ nor {z} found')
        with zipfile.ZipFile(z) as zf:
            zf.extractall(d)
    hits = glob.glob(os.path.join(d, '1 *Detailed.csv'))
    if not hits:
        raise SystemExit(f'[fatal] no detailed practice CSV inside {d}')
    # the BOM on the first header cell is why every read strips '﻿'
    df = pd.read_csv(hits[0], low_memory=False,
                     usecols=lambda c: c.lstrip('﻿') in WANT)
    df.columns = [WANT[c.lstrip('﻿')] for c in df.columns]
    missing = [v for v in WANT.values() if v not in df.columns]
    if missing:
        raise SystemExit(f'[fatal] {stamp}: columns missing/renamed: {missing}')
    for c in df.columns:
        if c != 'gp_code':
            df[c] = pd.to_numeric(df[c], errors='coerce')
    # one row per practice (the file can carry more than one source row)
    # min_count=1: an all-missing group must stay NaN. Without it pandas returns
    # 0.0, which silently turns 'this practice did not report nurses' into
    # 'this practice has no nurses' and inflates every downstream sample.
    return df.groupby('gp_code', as_index=False).sum(numeric_only=True, min_count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='.')
    ap.add_argument('--out', default='workforce_dec24_dec25.csv')
    a = ap.parse_args()

    frames = {}
    for tag, stamp in WAVES.items():
        df = load(a.src, stamp)
        frames[tag] = df
        print(f'[load] Dec 20{tag}: {len(df):,} practices | national FTE '
              f'total GP {df.gp_total.sum():,.0f}  FQ {df.gp_fq.sum():,.0f}')

    m = frames['24'].merge(frames['25'], on='gp_code', suffixes=('_24', '_25'))
    roles = ['gp_total', 'gp_fq', 'gp_fq_exlocum', 'nurse', 'dpc', 'admin']
    for r in roles:
        for y in ('24', '25'):
            m[f'{r}_per10k_{y}'] = 1e4 * m[f'{r}_{y}'] / m[f'patients_{y}']
        m[f'd_{r}'] = m[f'{r}_per10k_25'] - m[f'{r}_per10k_24']
    # trainee grades = all GPs minus fully-qualified
    for y in ('24', '25'):
        m[f'trainee_per10k_{y}'] = m[f'gp_total_per10k_{y}'] - m[f'gp_fq_per10k_{y}']
    m['d_trainee'] = m.trainee_per10k_25 - m.trainee_per10k_24

    print('\n[national] FTE per 10,000 patients, Dec 2024 -> Dec 2025:')
    for r in roles:
        a24 = 1e4 * m[f'{r}_24'].sum() / m.patients_24.sum()
        a25 = 1e4 * m[f'{r}_25'].sum() / m.patients_25.sum()
        print(f'    {r:14s} {a24:6.3f} -> {a25:6.3f}  ({100 * (a25 / a24 - 1):+.1f}%)')
    print('    NOTE: total GP falls while fully-qualified rises -- the gap is'
          ' trainee grades.')

    keep = (['gp_code', 'patients_24', 'patients_25']
            + [c for c in m.columns if 'per10k' in c or c.startswith('d_')])
    m[keep].to_csv(a.out, index=False)
    print(f'\n[written] {a.out}  ({len(m):,} practices matched across both censuses)')


if __name__ == '__main__':
    main()
