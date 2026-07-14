# The access cascade: where the inverse care law acts — findings (14 Jul 2026)

Source: GP Patient Survey 2026 national crosstabs (Q8 contact, Q12 deflection, Q14 diversion, Q31 needs-met)
by deprivation quintile × functional limitation (Q41) and × age (Q54).
Files: `data/GPPS_National_Crosstab_13072026*.xlsx`. National, descriptive, associations — not causal.

## Headline

Deprived, high-need patients **present equally** and, once seen, fare only **slightly worse**. The inverse
care law lives in the **middle of the journey** — they are disproportionately **deflected** ("contact us again
another day") and **diverted** (pharmacy/111/urgent care) before or instead of being seen. Separately, the
sickest have high unmet need **regardless of deprivation** — a complexity gradient, not an access one.

## The cascade (patients limited "a lot"; most vs least deprived)

| Stage | Most dep | Least dep | gradient |
|---|---|---|---|
| Didn't present (last contact >12mo / never) | 4% | 3% | +1pp (flat) |
| Deflected (told to contact again) | 12% | 7% | **+5pp** |
| Diverted (pharmacy / 111 / urgent) | 13% | 7% | **+6pp** |
| Needs not met (of those seen) | 17% | 15% | +2pp |

## Detail

- **Presentation is flat by deprivation, once need is held constant** (~1pp across all Q41 levels). Age-stratified,
  the deprived actually contact *more* within each age band (+3-5pp last-3-months at 16-24 and 55-64) — consistent
  with earlier-onset morbidity driving more presentation. So there is **no under-presentation / candidacy** at the
  "did you contact" level: high-need people come.
- **Deflection is need-targeted.** Within the most deprived it runs 12% (a lot) / 11% (a little) / 7% (none) — a
  +5pp need gap; in the least deprived that gap is only +3pp. So it lands hardest on the sickest, and the sickest-
  penalty is steeper in deprived areas. Age-stratified: +2 to +5pp deprivation gradient within *every* age band.
- **Diversion is need-neutral.** ~13/11/11% across need levels in the most deprived (only ~2pp need gap) — rises
  with deprivation (capacity) but doesn't single out the sickest; signposting, not rationing of the sickest.
  Age-stratified: +1 to +8pp deprivation gradient within every age band (strongest in young/working age).
- **Needs-not-met is need-patterned, not deprivation-patterned.** 17% of "a lot" limited say needs unmet vs 8% of
  the unlimited — and 15% even in the *least* deprived. Complex needs are hard to fully meet everywhere; deprivation
  adds only ~2pp on top.

## Robustness

Holds stratified by functional need (Q41) AND by age (deflection/diversion deprivation gradient positive within
every age band). Reproduces PANEL_NOTES §4.18.1 (deflection need-targeted; diversion need-neutral) on a fresh cut.
Because presentation is flat by deprivation, the conditional denominators at the downstream stages are comparable
across deprivation — so the deflection/diversion gradients are not selection artefacts.

## Caveats

Self-reported survey; associations not causation; each respondent's *last* contact (repeated cross-section, not a
cohort flow); national, not per-practice. Q8 "contact for yourself or someone else, any reason" is a low bar —
catches total non-contact, not under-contact relative to need (GPPS has recency, not frequency).

## Prior work / positioning

Established already: deprived practices under-deliver relative to morbidity (McConnachie 2023; Gopfert 2021);
funding formulae (de Dumast 2026; Anselmi 2025 Health Policy + 2026 BJGP e434) measure *met* demand and patch
unmet need by fiat ("no available measures" for capacity-to-engage). GPPS unmet-need by multimorbidity (Rolewicz
2020, 2018 survey). NEW here: the 2024 GPPS redesign added the deflection question, so *where in the journey* the
loss happens is newly measurable — and it's in the sorting behind the front door, not at it. Stage-4 corroborates
Rolewicz (need-driven); stages 2-3 are the contribution.
