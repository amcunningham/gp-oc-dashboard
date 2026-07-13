# Substack post — "the inverse care law is behind the front door" — session brief

_Deliverable: one Substack post (~1,200 words, markdown file in `research/`). Descriptive national data,
no named practices. Created 13 Jul 2026. Part of the unmet-need strand's outputs._

## Framing (agreed defaults — AMC can adjust)

- **Hook / spine:** *locate* the inverse care law — "it's not at the front door." Lead with the finding.
- **Stakes folded in:** the funding debate (Carr-Hill review in the 10-Year Plan; de Dumast/Anselmi) measures
  MET demand and patches unmet need by fiat; this shows the layer directly. Position as *complementing*, not attacking.
- **Length:** ~1,200 words. One clean cascade table, 2-3 headline stats, disciplined on method, a proper caveats paragraph.
- **Audience:** bridge — a GP nods, a policy reader follows. Explain deflection/GPPS lightly; don't dumb down.
- **Register:** descriptive — "what the national numbers show," associations, not causal claims. **No named practices.**

## The finding (the spine of the piece)

> Deprived, high-need patients **present equally**, and once seen fare only **slightly worse**. The inverse care
> law lives in the **middle of the journey** — they are disproportionately **deflected** ("contact us again another
> day") and **diverted** (pharmacy/111/urgent care) before or instead of being seen. Separately, the sickest have
> high unmet need **regardless of deprivation** — a complexity gradient, not an access one.

Cascade, most vs least deprived, among patients limited "a lot" (GPPS 2026):

| Stage | Most dep | Least dep | gradient |
|---|---|---|---|
| Didn't present (>12mo/never) | 4% | 3% | **+1pp** (flat) |
| Deflected (told to come back) | 12% | 7% | **+5pp** |
| Diverted (pharmacy/111/urgent) | 13% | 7% | **+6pp** |
| Needs not met (of those seen) | 17% | 15% | **+2pp** |

- **Deflection is need-targeted** (worst for the sickest; the need-penalty is steeper in deprived areas) — the ICL, located.
- **Diversion is need-neutral** (rises with deprivation but not with sickness) — capacity/signposting, not rationing of the sickest.
- **Needs-not-met is need-patterned, not deprivation-patterned** (17% of "a lot" limited vs 8% unlimited, even in the least deprived) — complexity.
- **Robust**: holds stratified by need (Q41) AND by age (deflection/diversion gradient positive within every age band); reproduces PANEL_NOTES §4.18.1.

## Literature positioning (be honest about what's new)

- **Not new:** deprived practices under-deliver relative to morbidity (McConnachie 2023 BMJ Open, contact time, +14%,
  *excludes non-attenders*; Gopfert 2021 BJGP, consultation length); funding formulae (de Dumast 2026 BMJ Open; Anselmi
  2025 Health Policy + 2026 BJGP e434). Rolewicz 2020 (BMJ Open) already did GPPS *needs-met/support by multimorbidity*.
- **New here:** the 2024 GPPS redesign added the **deflection** question — so the *access mechanism* (deflect/divert),
  and *where in the journey* the loss happens, is newly measurable. Anselmi 2026 states in print there are
  "currently no available measures" for the capacity-to-engage/unmet-need layer and patches it by zeroing coefficients —
  this measures it. And the stage-4 result **corroborates Rolewicz** (need-driven, not deprivation-driven), while
  stages 2-3 are the new contribution.

## Data & caveats (for the post's honesty box)

- Source: GP Patient Survey 2026 national crosstabs (Q8 contact, Q12 deflection, Q14 diversion, Q31 needs-met) × deprivation
  quintile × functional limitation (Q41) and × age (Q54). Files: `data/GPPS_National_Crosstab_13072026*.xlsx`; national
  reference `research/data/gpps_national_2026.csv`.
- Caveats: self-reported survey; associations not causation; each respondent's *last* contact (repeated cross-section, not a
  cohort flow); cascade denominators are conditional (deflection among contacters, needs-met among the seen) — but presentation
  being flat by deprivation means those downstream gradients aren't selection artefacts. National, not per-practice.

## Method / skills

- **Read `evidence-writing` skill** (style + rigour for evidence-based writing) before drafting. If a `my-writing-style`
  skill exists, use it; if not, aim for a clear GP-researcher voice and offer to learn AMC's style from samples.
- Numbers can be re-derived from the crosstab files (see the analysis session's parser approach) — verify the table before publishing.
- Save as a markdown file in `research/`; show AMC the draft before anything goes public. End by offering a title options list.
