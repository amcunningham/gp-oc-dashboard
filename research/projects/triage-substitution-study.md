# Online-triage substitution study — project brief

_Status: EXPLORATORY, not hardened. Findings below are first-pass; none are quotable until the
hardening pass is done. Created 13 Jul 2026._

## Question

When a practice adopts online / total triage (OC volume ramps up), what happens to: phone contact
volume, call answering, total contact, continuity, and patient experience? Is it substitution,
addition, or a trade-off — and does pushing to very high total triage cost continuity?

## Why it matters / audience

The empirical test of the "modern access model optimises the wrong layer" argument, and directly
relevant to live policy: the new GPC England chair (Clare Bannon) is campaigning on online-consultation
demand + safe working + continuity. Cohort-level evidence; **no named-practice case studies** (her own
practice, C85007, sits in this data — treat as sensitive, cohort only).

## Data (shared layer)

- OC submissions: `panel_oc` (Apr 2023–Mar 2026) and `panel_merged` (to May 2026). Normalised /1,000 patients.
- Phone: `cbt_ivr_panel` (inbound, answered, ivr_ended; Oct 2024–May 2026). **Starts after most first ramps.**
- Appointments: `panel_merged.total` (delivered; GPAD mode = f2f/phone/online-consultation medium, NOT booking channel).
- Direct online booking: **POMI** (Apr 2015–Aug 2024, then DISCONTINUED). Overlaps OC Apr 2023–Aug 2024 only —
  usable for early adopters' self-book-vs-triage substitution; no data for 2025 ramps. NHS App is the
  successor route but practice-level data is behind OKTA/smartcard (not open).

## Cohort definitions (as run)

- **OC riser**: baseline OC <40/1,000 (Oct–Dec 2024) AND a sustained jump in 2025 (first month OC > max(2×base, base+50)
  with next 2 months ≥ base+50). n=1,058; early rampers (Jan–May 2025) n=445 single-step.
- **Two-step**: a second sustained OC jump (>+100 over the post-first-ramp plateau). 11% of early risers.
- **High-triage tail**: OC ≥350/1,000 by early 2026 = 243 practices. Clean single-practice two-step-to-high = 190
  (excluded 19 at-scale orgs by name, 3 with implausible >800/1,000 denominators).

## Findings so far (exploratory)

1. **Phone falls immediately, no surge.** Indexed event study: phone flat pre-ramp, falls from month +1,
   plateaus ~−15–18% by month 2–4, durable to +12. Control (flat OC) ~flat. No double-running transition spike.
2. **Substitution is partial.** Answered calls fall only modestly (−42/1,000); OC rises far more (+185).
   Total inbound fall is disproportionately **unanswered** calls (−63 vs −42).
   **CAVEAT (AMC):** unanswered ≠ distinct unmet patients — could be the same person redialling; congestion
   inflates inbound. So "captured unmet demand" is NOT supportable, and distinct-demand change is unknowable
   from aggregate counts. Retracted.
3. **Answer rate improves, modestly and by selection.** Risers 78→84% vs control 86→87%; DiD +3pp. 75% of risers
   improve at all, only 30% by ≥10pp (Dove-Valley-scale is an outlier). Risers *start worse* (selection) and
   mostly don't catch up. Mechanism: rate rises because volume falls, not better answering. Mean-reversion not
   yet removed.
4. **First ramp additive, second ramp substitutive.** First step: total contact ~+13% (new online users).
   Second step (n≈188): phone −100, OC +90, **total ~flat** — balanced substitution, not addition. Dove Valley's
   total *falling* (over-substitution) is the atypical extreme, not the norm.
5. **Total contact is a fiction across mixed units** (call ≠ OC submission ≠ appointment). Contact counts show the
   *channel mix* shifted; they cannot settle whether demand rose/fell.

## Methods established

Per-practice pivot /1,000; ramp detection (thresholds above); event study indexed to pre-ramp mean (e−3..−1=100)
or absolute medians by event time; DiD vs placebo-ramp control. numpy WLS + HC1 (from `scripts/did_anima.py`).

## Hardening TODO (before anything is quotable)

- Matched control on size × deprivation × **baseline answer rate/phone** (removes mean-reversion + selection).
- Difference-in-differences on a **balanced** cohort (practices with data at every event month), clustered SEs, CIs.
- Sensitivity sweep on ramp thresholds (40 / 50 / ×2).
- Longer follow-up where data allows; time-varying list denominator.
- POMI early-adopter overlap (Apr 2023–Aug 2024): did direct self-booking fall as OC rose? (self-book vs triage split).
- Then: the OUTCOME — continuity & satisfaction change for the high-triage cohort vs OC intensity.

## Standing caveats

Units differ; inbound is redial/congestion-inflated; POMI gap for 2025; GPAD "online" = consultation mode not
booking channel; selection (adopters differ); single-practice illustrations are not evidence.
