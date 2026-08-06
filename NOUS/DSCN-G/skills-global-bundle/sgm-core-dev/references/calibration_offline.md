# Calibración offline de umbrales (exp_SGM_0024, Fase 6)

## Cuándo usar
La spec SGM v1.4 §2.5 (uso 2) propone FATE (`fate-v6-modular`) para calibrar
`θ_novelty, θ_refut, min_duration, θ_window_frac` contra la suite T-INF. Pero:
- FATE **NO está** en el vault/repo (no hay `fate-v6-modular` instalado).
- La propia spec §2.5 es honesta: FATE PIERDE contra CMA-ES en BAJA dimensión (D=10), y
  los 4 umbrales son exactamente baja dimensión (3-5 params).

→ La calibración offline HONESTA disponible es **grid search** contra una suite T-INF con
casos controlados (ground truth + negative control, regla #7 del roadmap). Documentar
explícitamente que FATE se omitió (no instalado + §2.5 honesto).

## Suite T-INF (4 casos controlados, sintéticos, reproducibles)
| Caso | Señal | Expect (stagnation) | Expect (refut) |
|------|-------|---------------------|----------------|
| C1 real estancamiento | novelty 0.20 ×6 ticks | True | False |
| C2 negative control | novelty 0.40 ×6 ticks | False | False |
| C3 real contradicción | novelty 0.40 ×6, pain 2.2 | False | True |
| C4 negative control | novelty 0.40 ×6, pain 1.5 | False | False |

Funciones:
- `check_stagnation(nov_traj, θ_novelty, min_duration, θ_window_frac)`: cuenta ticks
  consecutivos con `nov < θ_novelty`; si llega a `min_duration` → True.
- `verify_contradiction(pain_accum, θ_refut)`: `pain_accum > θ_refut`.

## Rangos de barrido (baja dimensión, pocos valores para legibilidad)
- θ_novelty ∈ {0.15, 0.30, 0.45}
- min_duration ∈ {3, 5, 7}
- θ_refut ∈ {1.5, 2.0, 2.5}
- θ_window_frac ∈ {0.3, 0.5, 0.7}
→ 3×3×3×3 = 81 combinaciones.

## Métrica (IMPORTANTE: evitar el bug de sub-checks)
Por cada config se evalúan 2 sub-checks por caso (stagnation + refut) × 4 casos = **8 unidades**.
- `passed` = count de sub-checks correctos (0..8).
- `margin` = separación entre el valor usado y el umbral (qué tan claro es el disparo).
- El CRITERIO de PASS debe comparar `best_pass == 8` (NO == 4). Decidir el denominador una
  vez y reusarlo en el contador Y en el gate. Imprimir "X / 8".

## Selección
`best = argmax(passed)`, desempate por `margin`. Reportar la config y que el barrido muestra
VARIACIÓN (n_configs_8/8 < 81 y n_configs_0/8 < 81) → calibración no trivial.

## Resultado 2026-08-02
Mejor config: θ_novelty=0.30, min_duration=3, θ_refut=1.5, θ_window_frac=0.3 → 8/8, 12 de 81
configs pasan todo. NOTA: más sensible que defaults de spec (5 / 2.0) porque la suite es
mínima; con corpus real (Don Quijote) podría requerir los valores conservadores.
