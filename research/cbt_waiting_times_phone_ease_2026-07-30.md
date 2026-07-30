# CBT June 2026 call-waiting times and the phone-ease size gap (§4.23 test)

Data added 30 Jul 2026 from the Cloud Based Telephony June 2026 edition (NHS England Digital,
published 30 Jul 2026 09:30), the first edition with practice-level call-waiting metrics
(new Summary Table 4b). Extracted to `data/cbt_jun26/cbt_waiting_jun26_practice.csv`
(5,061 practices, 5,057 with waiting-time values). Metric: percentage of cloud-based
telephony calls answered after waiting under two minutes, split Total / core hours
(8am–6:30pm) / morning peak (8–10am).

National (June 2026): 60.4% of answered calls picked up under 2 minutes overall; 60.5%
across core hours; **55.0% at the 8–10am peak** — the morning scramble visible in the
answering speed. Practice medians reproduce it: 62.2% / 62.3% / 55.5%.

## The §4.23 test — does answering speed explain why big practices have worse phone ease?

Outcome: `phone_easy_2026` (% who find it easy to get through by phone), weighted by GPPS
base, HC1 SEs, standardised predictors, region fixed effects; controls: deprivation, age 65+,
non-white %, diabetes prevalence, GP FTE per 10k.

| Model | list-size coef | waiting-time coef | n |
|---|--:|--:|--:|
| 1. size gap only | **-9.08*** | - | 4,844 |
| 2. + % answered <2 min (all day) | **-6.50*** | +6.58*** | 4,844 |
| 3. + % answered <2 min (8-10am) | -7.50*** | +5.38*** | 4,844 |

Descriptive: phone ease runs **71.4% (small practices) vs 53.3% (large)** - an 18-point gap;
calls answered under 2 minutes runs **68.8% vs 54.1%** across the same size tertiles.

**Finding.** Answering speed is a strong, independent predictor of reported phone ease
(+6.6 points per SD), and it accounts for roughly **28% of the size gap** - adding it shrinks
the list-size coefficient from -9.08 to -6.50. So part of the reason large practices'
patients find it harder to get through is simply that large practices answer more slowly
(54% vs 69% under 2 minutes). But a substantial size penalty survives (-6.50, still highly
significant): waiting time is not the whole story. Something else about large practices -
IVR menu depth, call routing, sheer inbound volume, or perception independent of measured
wait - keeps phone-ease lower even at equal answering speed. The all-day metric explains
more of the gap than the 8-10am-only metric.

First contract-quarter read; single cross-section (June 2026). Coverage 85.5% of practices
(the CBT participating estate), so this conditions on practices with cloud telephony data.
