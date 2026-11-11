# GP Online Consultation Dashboard & Analysis

Interactive dashboard analysing the online consultation (OC) platform market in English general practice, plus three deep-dive analyses exploring what higher OC adoption means for the 8am rush, workforce, appointments, and patient satisfaction.

**Live site:** https://amcunningham.github.io/gp-oc-dashboard/

## Pages

- **[Dashboard](https://amcunningham.github.io/gp-oc-dashboard/)** — Interactive overview of the OC platform market: practice lookup, supplier shares, volume trends, deprivation patterns (~6,100 practices)
- **[8am Rush](https://amcunningham.github.io/gp-oc-dashboard/rush_analysis.html)** — Does OC end the morning phone rush? Cloud-based telephony and OC submission patterns (4,306 practices)
- **[OC Hours](https://amcunningham.github.io/gp-oc-dashboard/oc_hours.html)** — Do practices that keep OC open 24/7 have less of an 8am rush? Practices grouped by when OC submissions arrive (OC, telephony and appointments, September 2026), with a before-and-after comparison for practices that changed their hours. To reproduce, run from the repo root in this order (outputs go to `research/data/oc_hours_sep26/`):
  1. `python research/scripts/oc_hours_rush.py --oc research/data/oc_daytime_sep26.zip --cbt research/data/cbt_daytime_sep26.zip --out research/data/oc_hours_sep26` — groups, timing, total contacts, adjusted comparisons
  2. `python research/scripts/oc_hours_extra.py --groups research/data/oc_hours_sep26/practice_groups.csv --oc research/data/oc_daytime_sep26.zip --cbt research/data/cbt_daytime_sep26.zip --oc-gpps research/data/panel/oc_daytime_2026-03.parquet --gpad research/data/gpad_crosstab_sep26.zip --gpad-month Sep_26 --out research/data/oc_hours_sep26` — day of week, phone answering, GP Patient Survey, appointments
  3. `python research/scripts/oc_hours_switchers.py --out research/data/oc_hours_sep26` — monthly groups and practices that switched
  4. `python research/scripts/oc_hours_history.py --old research/data/oc_daytime_jan25.zip --out research/data/oc_hours_sep26` — trend since January 2025 and before-and-after with calls
  5. `python research/scripts/oc_hours_capacity.py --oc research/data/oc_daytime_sep26.zip --cbt research/data/cbt_daytime_sep26.zip --gpad research/data/gpad_crosstab_sep26.zip --gpad-month Sep_26 --out research/data/oc_hours_sep26` — morning peak against booked-ahead appointments, total appointments and GPs, all practices
  6. Broader groups (check): steps 1 and 2 again with `--grouping broad` and `--out research/data/oc_hours_sep26_broad` (step 2 also with `--groups research/data/oc_hours_sep26_broad/practice_groups.csv`) — core hours absorbs practices with a trickle of out-of-hours requests, and all 24/7 practices form one group

  All use `research/scripts/oc_timefix.py`, which corrects OC submission times recorded in UTC during British Summer Time and leaves out practices whose call times are recorded in UTC.
- **[Workforce & Appointments](https://amcunningham.github.io/gp-oc-dashboard/workforce_appts.html)** — Staffing, appointment modes, GP workload per session, lead times, DNA rates (6,018 practices)
- **[Satisfaction](https://amcunningham.github.io/gp-oc-dashboard/satisfaction.html)** — Patient experience by OC intensity, with deprivation stratification and regression (6,018 practices)

## Data

The `data/` folder contains derived datasets used in the analysis:

- `full_oc_tertiles.csv` — Tertile assignments for 6,018 practices (GP_CODE, OC rate, tertile, region, supplier)
- `practice_imd.csv` — Practice-level Index of Multiple Deprivation 2025 scores (Fingertips NGPP indicator 94240: IoD2025 population-weighted across each practice's registered patients; replaced the IMD 2019 indicator 93553 export in Apr 2026)
- `practice_feb26.json` — Cloud-based telephony practice-level summary (February 2026)

### Original data sources (not included due to size)

All source data is publicly available from NHS England:

- **OC submissions:** [Submissions via Online Consultation Systems in General Practice, February 2026](https://digital.nhs.uk/data-and-information/publications/statistical/submissions-via-online-consultation-systems-in-general-practice/february-2026)
- **Appointments:** [Appointments in General Practice, February 2026](https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice)
- **Workforce:** [General Practice Workforce Census, February 2026](https://digital.nhs.uk/data-and-information/publications/statistical/general-and-personal-medical-services)
- **CBT:** [Cloud Based Telephony, February 2026](https://digital.nhs.uk/data-and-information/publications/statistical/cloud-based-telephony)
- **GPPS:** [GP Patient Survey 2025](https://gp-patient.co.uk/)
- **IMD:** [Index of Multiple Deprivation 2019](https://fingertips.phe.org.uk/) (indicator 93553)

## Method

The deep-dive analyses group practices into tertiles by OC submission rate per 1,000 registered patients per day. This is a cross-sectional comparison — it shows differences between practices at different levels of OC use, not changes over time. Association does not imply causation.

## Disclaimer

This site reuses publicly available NHS data and is intended for information only. It is not a recommendation, ranking or endorsement of any GP practice or software supplier. Figures reflect the state of NHS published data at the time of the most recent refresh and may contain errors or omissions in the underlying source data.

## Author

Anne Marie Cunningham, GP. Built with assistance from Claude (Anthropic). The analysis and any errors are mine.
