# GP Online Consultation Dashboard & Analysis

Interactive dashboard analysing the online consultation (OC) platform market in English general practice, plus three deep-dive analyses exploring what higher OC adoption means for the 8am rush, workforce, appointments, and patient satisfaction.

**Live site:** https://amcunningham.github.io/gp-oc-dashboard/

## Pages

- **[Dashboard](https://amcunningham.github.io/gp-oc-dashboard/)** — Interactive overview of the OC platform market: practice lookup, supplier shares, volume trends, deprivation patterns (~6,100 practices)
- **[8am Rush](https://amcunningham.github.io/gp-oc-dashboard/rush_analysis.html)** — Does OC end the morning phone rush? Cloud-based telephony and OC submission patterns (4,306 practices)
- **[Workforce & Appointments](https://amcunningham.github.io/gp-oc-dashboard/workforce_appts.html)** — Staffing, appointment modes, GP workload per session, lead times, DNA rates (6,018 practices)
- **[Satisfaction](https://amcunningham.github.io/gp-oc-dashboard/satisfaction.html)** — Patient experience by OC intensity, with deprivation stratification and regression (6,018 practices)

## Data

The `data/` folder contains derived datasets used in the analysis:

- `full_oc_tertiles.csv` — Tertile assignments for 6,018 practices (GP_CODE, OC rate, tertile, region, supplier)
- `practice_imd.csv` — Practice-level Index of Multiple Deprivation 2019 scores
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
