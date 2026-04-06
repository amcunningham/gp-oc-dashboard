# gp-oc-dashboard
Interactive dashboard analysing the online consultation platform market in English general practice, using NHS England, GPPS and IMD data.
# GP Online Consultation Market Dashboard

An interactive dashboard analysing the online consultation (OC) platform market
in English general practice, plus a searchable lookup of all ~6,100 active GP
practices with a concise data-driven pen portrait of each.

**Live site:** https://amcunningham.github.io/gp-oc-dashboard/

## What it covers

- Supplier market share over time (Accurx, eConsult, PATCHS, Anima, TPP, Footfall, etc.)
- Submission volumes and utilisation rates
- Variation by deprivation (IMD 2019 quintile)
- Variation by practice list size
- Variation by age profile (% registered patients aged 65+)
- GP Patient Survey 2024 vs 2025 satisfaction scores linked to OC supplier
- Practice-level lookup with pen portrait, OC use, GPPS scores and demographic context

## Data sources

- **OC submissions** — NHS England experimental statistics, *Submissions via OC Systems in General Practice*, August 2024 – February 2026
- **GP Patient Survey** — Ipsos for NHS England, 2024 and 2025 practice-level (weighted) results
- **Deprivation** — Index of Multiple Deprivation 2019, practice-level scores via OHID Fingertips
- **Age profile and list size** — NHS Digital, *Patients Registered at a GP Practice*, March 2026
- **Practice metadata** — NHS Digital ePraccur

## Disclaimer

This site reuses publicly available NHS data and is intended for information
only. It is not a recommendation, ranking or endorsement of any GP practice or
software supplier. Figures reflect the state of NHS published data at the time
of the most recent refresh and may contain errors or omissions in the
underlying source data.

## Refresh

The dashboard is refreshed monthly when NHS England publish new OC statistics.
Each refresh is committed to this repo and deployed automatically via
GitHub Pages.

## Author

Anne Marie Cunningham, GP. Built with assistance from Claude.
