# Continuity, appointment timing and patients’ experience of access

*Dr Anne Marie Cunningham, Clinical Lead for Data and Digital · Draft for RCGP internal use*

*This note examines the relationships between continuity, appointment timing, deprivation and patient experience using the 2026 GP Patient Survey and General Practice Appointments Data.*

## Summary

This analysis asks whether continuity and short appointment intervals are associated with different aspects of patient experience, and whether the apparent benefit of continuity can instead be explained by deprivation or by high-continuity practices providing faster appointments.

It distinguishes between:

- **continuity:** whether patients can see or speak to their preferred healthcare professional;
- **appointment interval:** the elapsed time before an appointment;
- **experienced access:** whether patients consider the wait for their appointment acceptable;
- **experience of care:** overall experience, needs met, confidence and trust, and involvement in decisions.

The principal analysis uses the 2026 GP Patient Survey. Continuity and patient-reported same/next-day timing are entered together, first in simple comparisons and then in models adjusting for deprivation, list size, age profile, rurality and dispensing status.

Because continuity, reported timing and the outcomes are all measured in GPPS, the analysis is repeated using General Practice Appointments Data. GPAD supplies a timing measure recorded independently in practice appointment systems. Its purpose here is not to provide a superior definition of access, but to test whether the continuity findings persist when appointment timing is measured from a different source.

The main findings are:

- Continuity has the larger association with overall experience, needs met, confidence and trust, and involvement in decisions.
- Shorter appointment intervals have their largest association with whether patients consider the wait acceptable.
- Continuity also retains an independent association with acceptable waiting.
- More deprived practices have lower achieved continuity and worse patient-experience results, despite more patients reporting that they have a preferred professional.
- The association between continuity and patient experience is present within every deprivation quintile and remains after adjustment for measured practice and population characteristics.
- The findings persist when GPAD is used as the independent appointment-timing measure.

The analysis is cross-sectional and at practice level. It identifies associations and does not establish causation.

## Data sources and linkage

Four published practice-level data sources were linked using the NHS GP practice code.

| Data source | Period used | Variables used in this analysis |
|---|---|---|
| [GP Patient Survey: 2026 results and practice-level data](https://gp-patient.co.uk/latest-survey/results) | Survey responses collected 2 January–13 April 2026; results published 9 July 2026 | Continuity; patient-reported same/next-day appointment interval; acceptable waiting; overall experience; needs met; confidence and trust; involvement in decisions; practice response weights; respondent age profile; and GPPS practice population size where required. |
| [General Practice Appointments Data: January 2026](https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice/january-2026) and [February 2026](https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice/february-2026) | Appointments taking place in January and February 2026 | Number of attended appointments taking place on the day they were booked or one day later, divided by attended appointments with a known booking interval. Measures were constructed for all attended appointments and, separately, for attended GP appointments. |
| [National General Practice Profiles](https://fingertips.phe.org.uk/profile/general-practice/data) | IMD 2025 | Practice population-weighted deprivation score: indicator 94240, “Deprivation score (IMD 2025)”. |
| [NHS Payments to General Practice, England 2024/25: practice-level data](https://digital.nhs.uk/data-and-information/publications/statistical/nhs-payments-to-general-practice/england-2024-25) | Financial year 2024/25 | Practice rurality, dispensing-practice status and average number of registered patients. |

The reported GPAD models use January and February 2026. March data were examined as a sensitivity analysis but are not included in the reported tables; adding March made no material difference to the coefficients or conclusions. The NHS England page records that publication of the January release was delayed from 26 February to 5 March because of technical issues. It does not identify a problem with the quality of the January appointment data.

### Construction of adjustment variables

- **Deprivation:** the 2025 population-weighted practice IMD score from National General Practice Profiles.
- **List size:** the average registered population in the Payments to General Practice practice-level file, log-transformed. GPPS practice population size was used where the payments value was unavailable.
- **Age profile:** the nine GPPS practice-level respondent age-band percentages, with one category omitted as the reference category in the regression models.
- **Rurality:** the Payments to General Practice rural/urban classification, represented as a binary rural indicator.
- **Dispensing status:** the Payments to General Practice dispensing-practice field, represented as a binary indicator.

Practices were linked by practice code. Models used complete cases for the outcome, exposure variables, model weight and adjustment variables. Weighting is stated separately for each model below. Robust standard errors and 95% confidence intervals were calculated for the weighted linear regressions.

## Measures

### Continuity

Among patients who had a preferred healthcare professional and had tried to contact them, the proportion who reported seeing or speaking to that professional:

- always or almost always; or
- a lot of the time.

### Patient-reported appointment interval

The proportion of patients who reported that their last appointment took place:

- on the same day; or
- on the day after they first contacted the practice.

The denominator includes patients who selected “I can’t remember”. The same/next-day numerator was constructed from the published weighted response counts, avoiding ambiguity where a very small published percentage was represented by the GPPS suppression code −98.

### Administratively recorded appointment interval

The proportion of attended appointments in General Practice Appointments Data that took place:

- on the same day; or
- one day after the appointment was booked.

The principal GPAD analysis included all attended practice appointments. Attended GP appointments were examined separately as a sensitivity analysis.

### Experienced access

The proportion of patients who said the wait for their appointment was “about right.”

Responses of “I don’t know” were excluded from the denominator.

### Other patient-experience outcomes

- Good overall experience of the practice.
- Needs met at the last appointment, excluding “I don’t know”.
- Confidence and trust in the healthcare professional, excluding “I don’t know or it didn’t apply”.
- Involvement as much as wanted in decisions about care and treatment, excluding “I can’t remember or it didn’t apply”.

## Comparison of practices with high and low continuity and short appointment intervals

There were valid, unsuppressed continuity results for 6,123 practices and valid patient-reported appointment-interval results for 6,144 practices in the analysed GPPS extract.

Practices were ranked separately on continuity and patient-reported same/next-day appointments. The highest and lowest 10% were compared, giving:

- 612 practices in each continuity group;
- 614 practices in each appointment-interval group.

Group sizes were calculated as 10% of valid practices and rounded to the nearest whole practice. The GPPS file contains 6,166 practice rows; suppressed results were excluded. The independently checked pooled results were unchanged by the very small differences produced by alternative suppression and decile-boundary conventions.

Results within each group were pooled using the published weighted favourable-response counts and eligible-response bases.

### Table 1. Patient experience in practices with the highest and lowest continuity and same/next-day appointment rates

| Measure | Continuity: top 10% | Continuity: bottom 10% | Same/next-day interval: top 10% | Same/next-day interval: bottom 10% |
|---|---:|---:|---:|---:|
| Good overall experience | **87.5%** | 67.6% | 81.9% | 72.5% |
| Wait considered acceptable | 80.0% | 61.9% | **83.5%** | 56.3% |
| Needs met | **94.4%** | 87.3% | 92.1% | 88.7% |
| Confidence and trust | **95.8%** | 90.1% | 93.7% | 91.7% |
| Involved as much as wanted in decisions | **95.3%** | 88.8% | 92.5% | 90.7% |

*Figures are pooled percentages calculated from the published weighted GPPS practice results.*

Practices in the highest continuity group had better results than practices in the highest same/next-day group for:

- overall experience;
- needs met;
- confidence and trust;
- involvement in decisions.

Practices in the highest same/next-day group had the better result for acceptable waiting.

The high-continuity group nevertheless had a relatively high acceptable-wait result: 80.0%.

## Continuity and deprivation

All deprivation analyses were conducted at practice level. Practices were divided into five equally sized groups using their population-weighted deprivation scores.

Patients registered with practices in the most deprived fifth were more likely to report having a preferred healthcare professional: 34.2% compared with 30.3% in the least deprived fifth.

However, among patients with a preferred professional who had tried to contact them, regular contact with that professional was lower in the most deprived fifth: 38.5% compared with 45.9%.

### Table 2. Having a preferred professional and achieving continuity, by practice deprivation

| Practice deprivation | Patients reporting a preferred professional | Patients regularly seeing or speaking to their preferred professional |
|---|---:|---:|
| Least deprived | 30.3% | 45.9% |
| Quintile 2 | 30.5% | 43.7% |
| Quintile 3 | 30.2% | 41.3% |
| Quintile 4 | 31.7% | 38.9% |
| Most deprived | 34.2% | 38.5% |
| Least-to-most-deprived difference | **+3.9 points** | **−7.4 points** |

*Practices were divided into deprivation quintiles using their population-weighted deprivation scores. Percentages were pooled using the published weighted favourable-response counts and weighted eligible-response bases. The second column is based on all eligible respondents. The third is restricted to patients who had a preferred professional and had tried to see or speak to them.*

The deprivation gradient is therefore different for preference and achieved continuity. Reported preference is higher in the most deprived fifth, while regular contact with the preferred professional is lower.

## Patient experience and deprivation

Continuity and all five patient-experience measures were lower in more deprived practices.

### Table 3. Continuity and patient experience by practice deprivation quintile

| Practice deprivation | Continuity | Good overall experience | Wait acceptable | Needs met | Confidence and trust | Involved in decisions |
|---|---:|---:|---:|---:|---:|---:|
| Least deprived | 45.5% | 81.5% | 73.6% | 92.7% | 94.6% | 93.9% |
| Quintile 2 | 44.4% | 80.0% | 72.0% | 91.5% | 93.6% | 92.8% |
| Quintile 3 | 42.4% | 77.9% | 70.8% | 90.4% | 92.6% | 91.5% |
| Quintile 4 | 40.6% | 76.4% | 69.1% | 89.3% | 91.8% | 90.6% |
| Most deprived | 40.1% | 75.0% | 68.1% | 88.4% | 91.3% | 89.9% |
| Least-to-most-deprived difference | −5.4 points | −6.5 points | −5.5 points | −4.3 points | −3.3 points | −4.0 points |

*Figures are response-weighted practice averages. The small difference between the continuity estimates in Tables 2 and 3 arises from the different aggregation methods and complete-case samples used for the two analyses.*

To examine whether the association between continuity and patient experience was confined to less deprived practices, separate weighted models were fitted within each deprivation quintile.

Each model included:

- continuity;
- patient-reported same/next-day appointment interval.

### Table 4. Association between continuity and patient experience within each deprivation quintile

| Outcome | Least deprived (n=1,229) | Quintile 2 (n=1,226) | Quintile 3 (n=1,226) | Quintile 4 (n=1,221) | Most deprived (n=1,221) |
|---|---:|---:|---:|---:|---:|
| Good overall experience | +2.85 [2.58, 3.11] | +3.35 [3.10, 3.60] | +3.34 [3.09, 3.60] | +3.36 [3.08, 3.63] | +3.27 [2.97, 3.57] |
| Wait acceptable | +2.48 [2.22, 2.75] | +2.91 [2.64, 3.18] | +2.96 [2.70, 3.22] | +2.83 [2.53, 3.13] | +2.93 [2.61, 3.24] |
| Needs met | +0.85 [0.72, 0.97] | +1.15 [1.01, 1.30] | +1.13 [0.99, 1.27] | +1.19 [1.02, 1.36] | +1.16 [0.97, 1.34] |
| Confidence and trust | +0.66 [0.54, 0.77] | +0.98 [0.85, 1.11] | +1.00 [0.87, 1.13] | +0.95 [0.80, 1.10] | +0.94 [0.78, 1.10] |
| Involved in decisions | +0.83 [0.71, 0.95] | +0.97 [0.84, 1.10] | +1.11 [0.97, 1.24] | +1.06 [0.90, 1.21] | +1.01 [0.83, 1.20] |

*Cells show the percentage-point difference associated with a 10-percentage-point increase in continuity [95% confidence interval]. Patient-reported same/next-day appointment interval was included in each model. Models were weighted by the total number of GPPS responses received by the practice. The n shown is the complete-case sample for each quintile.*

The association between continuity and every outcome was present in all five deprivation quintiles.

For overall experience, a 10-point increase in continuity was associated with an improvement of between 2.8 and 3.4 percentage points.

The associations with needs met, confidence and trust, and involvement in decisions in the more deprived quintiles were similar to or larger than the corresponding population-wide estimates from Model 1.

## Adjusted analysis

Weighted practice-level regression models were fitted separately for each outcome.

All fully adjusted models included:

- population-weighted deprivation score;
- log registered-list size;
- weighted patient age profile;
- rurality;
- dispensing status.

Different models were used to examine patient-reported and administratively recorded appointment intervals.

### Table 5. Variables included in each adjusted model

| Model | Continuity | GPPS-reported same/next-day interval | GPAD-recorded interval | Background adjustment variables |
|---|:---:|:---:|:---:|---|
| **Model 1: GPPS interval** | ✓ | ✓ | — | Deprivation, log list size, age profile, rurality and dispensing status |
| **Model 2a: GPAD, all appointments** | ✓ | — | All attended appointments | The same five variables |
| **Model 2b: GPAD, GP appointments** | ✓ | — | Attended GP appointments | The same five variables |
| **Model 3: Combined** | ✓ | ✓ | All attended appointments | The same five variables |

Models 2a and 2b were fitted separately. The all-appointment and GP-only GPAD measures were not entered in the same model.

Model-specific weighting and exact complete-case sample sizes are reported with Tables 6–8.

## Model 1: continuity and patient-reported appointment interval

Model 1 included:

> Continuity + GPPS same/next-day interval + deprivation + log list size + patient age profile + rurality + dispensing status.

### Table 6. Adjusted associations of continuity and patient-reported appointment interval with patient experience

| Outcome | 10-point increase in continuity | 10-point increase in GPPS-reported same/next-day appointments | Larger association |
|---|---:|---:|---|
| Good overall experience | **+3.03 [2.87, 3.19]** | +1.63 [1.44, 1.81] | Continuity |
| Wait acceptable | +2.52 [2.35, 2.68] | **+5.68 [5.50, 5.87]** | Shorter interval |
| Needs met | **+1.03 [0.95, 1.12]** | +0.65 [0.55, 0.75] | Continuity |
| Confidence and trust | **+0.88 [0.80, 0.96]** | +0.38 [0.29, 0.47] | Continuity |
| Involved in decisions | **+0.93 [0.85, 1.01]** | +0.33 [0.23, 0.42] | Continuity |

*Cells show the percentage-point difference associated with a 10-percentage-point increase in the relevant predictor [95% confidence interval], with the other model variables held constant. Model 1 used outcome-specific weighted eligible-response bases; n=6,109 complete practices for each outcome.*

Continuity had the larger association with overall experience and the three measures of the encounter. Patient-reported appointment interval had the larger association with acceptable waiting.

Continuity retained an independent association with acceptable waiting after patient-reported interval was included.

## Analysis using GPAD-recorded appointment intervals

The principal analysis uses GPPS for continuity, appointment timing and patient-experience outcomes. Associations between measures taken from the same survey may partly reflect shared reporting or wider perceptions of the practice.

GPAD was therefore introduced as a robustness test. It provides an appointment-timing measure recorded independently in practice appointment systems. The question is whether continuity retains its association with patient experience after the GPPS timing measure is replaced by an administrative measure derived from a different data source.

The analysis used GPAD for January and February 2026.

GPAD records the interval between the date an appointment was booked and the date it took place. It does not necessarily record the interval between the patient’s first attempt to seek care and the appointment.

The principal measure was the proportion of all attended appointments that took place on the same or next day after booking. A GP-only version was tested separately.

## Models 2a and 2b: continuity and GPAD-recorded interval

Model 2a included:

> Continuity + GPAD same/next-day interval for all attended appointments + deprivation + log list size + patient age profile + rurality + dispensing status.

Model 2b replaced the all-appointment GPAD measure with the same/next-day interval for attended GP appointments.

Neither model included the GPPS-reported appointment interval.

### Table 7. Adjusted associations of continuity and GPAD-recorded appointment interval with patient experience

| Outcome | Continuity: Model 2a | GPAD all appointments: Model 2a | Continuity: Model 2b | GPAD GP appointments: Model 2b |
|---|---:|---:|---:|---:|
| Good overall experience | **+3.13 [3.00, 3.27]** | +0.38 [0.19, 0.57] | **+3.15 [3.01, 3.29]** | +0.38 [0.24, 0.52] |
| Wait acceptable | +3.01 [2.84, 3.18] | **+3.23 [3.01, 3.46]** | +3.12 [2.96, 3.28] | +3.02 [2.85, 3.19] |
| Needs met | **+1.08 [1.00, 1.15]** | +0.20 [0.10, 0.31] | **+1.09 [1.01, 1.16]** | +0.19 [0.11, 0.27] |
| Confidence and trust | **+0.95 [0.88, 1.02]** | +0.11 [0.02, 0.21] | **+0.95 [0.89, 1.02]** | +0.11 [0.04, 0.18] |
| Involved in decisions | **+0.98 [0.91, 1.05]** | +0.05 [−0.05, 0.15] | **+0.98 [0.91, 1.05]** | +0.07 [0.00, 0.14] |

*Cells show percentage-point differences associated with a 10-percentage-point increase in continuity or the relevant GPAD same/next-day rate [95% confidence interval]. Models 2a and 2b were weighted by the total number of GPPS responses received; n=6,102 complete practices for each outcome.*

The GPAD appointment interval was associated with acceptable waiting. Its associations with overall experience, needs met, trust and involvement were small.

Continuity retained associations with all five outcomes. Results were similar using all appointments and GP-only appointments.

## Model 3: continuity and both appointment-interval measures

Patient-reported and GPAD-recorded appointment intervals were moderately correlated:

- approximately 0.45–0.49 using all GPAD appointments;
- approximately 0.56–0.61 using GP appointments.

Model 3 included:

> Continuity + GPPS same/next-day interval + GPAD same/next-day interval for all attended appointments + deprivation + log list size + patient age profile + rurality + dispensing status.

### Table 8. Combined adjusted associations of continuity, patient-reported interval and GPAD-recorded interval

| Outcome | 10-point increase in continuity | 10-point increase in GPPS-reported same/next-day appointments | 10-point increase in GPAD-recorded same/next-day appointments |
|---|---:|---:|---:|
| Good overall experience | **+2.99 [2.85, 3.12]** | +1.78 [1.60, 1.96] | −0.63 [−0.84, −0.41] |
| Wait acceptable | +2.56 [2.42, 2.69] | **+5.48 [5.31, 5.66]** | +0.14 [−0.07, 0.35] |
| Needs met | **+1.02 [0.95, 1.09]** | +0.71 [0.61, 0.81] | −0.20 [−0.32, −0.08] |
| Confidence and trust | **+0.91 [0.84, 0.98]** | +0.47 [0.38, 0.55] | −0.15 [−0.26, −0.04] |
| Involved in decisions | **+0.94 [0.87, 1.01]** | +0.43 [0.34, 0.53] | −0.20 [−0.31, −0.08] |

*Cells show percentage-point differences associated with a 10-percentage-point increase in the relevant predictor [95% confidence interval]. Model 3 was weighted by the total number of GPPS responses received; n=6,102 complete practices for each outcome.*

Continuity remained the largest positive association with overall experience, needs met, confidence and trust, and involvement in decisions.

Patient-reported appointment interval remained the largest association with acceptable waiting.

The GPAD interval contributed little additional positive association after the patient-reported interval was included. Possible explanations for the small negative coefficients include:

- differences between first contact and recorded booking date;
- planned and follow-up appointments;
- differences in appointment mix;
- variation in appointment-book configuration;
- entering two related interval measures in the same model.

## Interpretation

The findings separate the length of the appointment interval from patients’ assessment of whether the wait was acceptable.

Shorter patient-reported and administratively recorded intervals were associated with better acceptable-wait ratings. Patient-reported interval had the larger association.

Continuity was independently associated with acceptable waiting and had larger associations with:

- overall experience;
- needs met;
- confidence and trust;
- involvement in decisions.

The deprivation analysis showed that:

- patients registered with more deprived practices were more likely to report having a preferred professional;
- achieved continuity was lower in those practices;
- more deprived practices had worse results across all five patient-experience measures;
- the association between continuity and patient experience remained present within every deprivation quintile.

The results do not support using same/next-day appointment rates as a complete measure of access or service quality. Appointment timing, acceptable waiting and continuity describe different aspects of patients’ experience.

## Limitations

- The analysis is cross-sectional and cannot establish causation.
- It uses practice-level measures. Associations between practice averages cannot automatically be attributed to individual patients.
- Continuity and most outcomes were reported in the same survey, creating potential for shared reporting effects.
- The continuity measure applies only to patients who had a preferred professional and had tried to contact them.
- Patient-reported interval is subject to recall.
- Same/next-day rates do not distinguish urgent appointments from planned care or appointments deliberately booked for later.
- GPAD records the interval from booking rather than necessarily from first contact.
- GPAD includes planned reviews and follow-up care as well as appointments for new problems.
- Patients with repeated appointments contribute repeatedly to GPAD, whereas GPPS asks about the respondent’s last appointment.
- GPAD does not capture all general-practice activity.
- Appointment-system configuration and recording quality vary between practices.
- Residual confounding remains possible despite adjustment for major practice and population characteristics.
- Needs met, confidence and trust, and involvement are rated highly in most practices, limiting the absolute size of observable differences.

## Conclusions

Appointment timing and continuity are associated with different aspects of patient experience.

Shorter appointment intervals have their largest association with whether patients consider the wait acceptable. Continuity has larger associations with overall experience and the reported quality of the encounter.

Patients registered with more deprived practices are more likely to report having a preferred professional but less likely to achieve regular contact with that professional. The association between continuity and patient experience remains present across the deprivation distribution and after adjustment for measured population and practice characteristics.

These findings support reporting appointment interval, acceptable waiting and continuity as separate measures. They are not interchangeable: appointment interval has its strongest association with whether the wait is acceptable, while continuity has stronger associations with overall experience, needs met, confidence and trust, and involvement in decisions.

*Sources: GP Patient Survey 2026 practice-level weighted results, Ipsos for NHS England; NHS England General Practice Appointments Data, January–February 2026; National General Practice Profiles deprivation data; NHS Payments to General Practice practice-characteristics data. Analysis by Dr Anne Marie Cunningham. Full methods and model results available on request.*
