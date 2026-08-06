# v0.25 loop integration failure pattern
Online loop experiments v0.25 v8→v11b repeatedly showed that putting validated
components in a closed transformer→root→memory→decoder loop can destroy the
baseline those components individually achieved.

## Result table
- v8 baseline transformer-only: 0.758 → loop: 0.550 → without decoder: 0.417
- v10 skip-gram embeddings: linear classifier baseline 0.766 → loop: 0.490
- v11 conservative variant (skip-gram + threshold + context-node update): synthetic
  baseline 0.559 → loop 0.697 (first positive), but on perfect synthetic embeddings
  (baseline 1.000) for 'llave'/'banco' loop dropped to 0.500/0.447
- v9 synthetic skip-gram: baseline 0.328 → loop 0.500 (positive on weak baseline,
  but low absolute performance)

## Core finding
The loop does NOT preserve pre-learned signal even when the signal is strong and
the components are individually valid. The failure is structural in the loop
dynamics, not calibratable by hyperparameter sweep.

## Robust path forward (if retrying loop integration)
- Freeze focal omega during loop. Train a separate context state or context-node
  embeddings only.
- Threshold gating: only apply root/memory updates when
  `|cos(ctx,A) - cos(ctx,B)|` is large. Do NOT update on ambiguous context.
- Evaluate loop vs supervised baseline in identical conditions. A loop that
  cannot preserve component performance is not integration.
- Do not iterate more variants on the same loop design; change the loop
  architecture itself (e.g. eliminate focal omega update, or replace
  `foco*(A-B)` with a learning-rate-scaled update on context embeddings only).

## Related skill references
`dscng-experimentation` SKILL.md: "Online loop omega-update ... corrupts separation"
+ "Online-loop integration is NOT achieved by superposition of validated components"
