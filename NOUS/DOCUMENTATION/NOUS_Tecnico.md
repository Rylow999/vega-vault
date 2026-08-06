# NOUS / DSCN-G — Compendio Técnico (Estado Actualizado al 2026-07-25)

> Este archivo es el ÍNDICE ACTUALIZADO del compendio. La versión completa de
> ecuaciones/teoremas vive en `v4.0/NOUS_Tecnico_v4.md` (1777 líneas). Este
> documento refleja los cambios de la auditoría Ronda 6 (2026-07-24) y la
> sesión de la Tríada (2026-07-25), y marca qué ecuaciones/claims cambian.

## Estado de los Claims (post-Ronda 6, autoritativo)

| Claim | Estado | Nota |
|-------|--------|------|
| T1 — cota universal + punto fijo (N_ss*≤1/θ_death) | ✅ Validado | N_ss* empírico ≈ 4–5 (NO 9–10; ese número es del N-back v6, no de T1) |
| T1 — maximalidad (simulación real) | ✅ Validado | |
| T2 — ω alignment (1.0000) | ✅ Validado | |
| T3 — consenso de fase | ⚠️ Validado con matiz | Reportar **76.7% estricto** (R≥0.9), NO 100% laxo. El v4.0 dice "100%" — CORREGIR a 76.7% |
| N-back v6 N_ss* = 9.50±1.02 | ✅ Validado | Es del N-back, no de T1 |
| d′(10-back)=0.97, d′(15-back)=0.82 | ✅ Validado | valores v6, no v5 |
| C3 / Phase-Hijacking (Face Hijacking) | ❌ NO SOSTENIDO | Retirado Ronda 6: 0.9% triggers a params originales, ΔPLV≈0. Rediseño llega a 30.2%, lejos de "la norma". El v4.0 lo presenta como "Predicción central" — ERRONEO, marcar RETIRADO |
| Φ_proxy — escalado O(log N) | ⚠️ Hipótesis caída | Dos definiciones probadas (MI cruda, TE-bottleneck), ninguna sostiene la predicción. El "Φ" real de DSCN-G es la Vitalidad V_i (Ec. 5), no el proxy de info integrada |

## Las 12 Ecuaciones NO cambian

Las Ecuaciones 1–12 (DSCN-G v7.2 + NOUS v2.0) siguen siendo las mismas fórmulas.
La corrección de Ronda 6 es de NÚMEROS y STATUS, no de fórmulas. El "resto de
ecuaciones" (1–7 fase/vector/vitalidad, 8–12 contexto/tiempo) queda IGUAL.

## Nuevo: DSCN-G en la Tríada de Autorregulación Disipativa (2026-07-25)

DSCN-G es la capa COGNITIVA de una arquitectura común de 3 capas (ver
`/TRIADA_AUTORREGULACION/`):
- Dinámica A: fase φ_i (Ec. 3, Kuramoto)
- Dinámica B: vector ω_i (Ec. 1, TD-Learning)
- 3ra dinámica (reguladora): Vitalidad V_i (Ec. 5–6, poda homeostática)

La vitalidad V_i es la cantidad que autorregula la competencia fase↔vector,
confinando el grafo a N_ss*≤~5 (T1). Análogo cognitivo del "Tercer Motor" de
Navier-Stokes (curvatura espectral G) y del balance f_P de Collatz.

CALIFICACIÓN en el criterio operacional del amigo (Punto 2):
- C1 (fase/vector compiten): ✅
- C2 (V_i acotada por poda): ✅
- C3 (cota por ESTRUCTURA, no variable externa): ✅ → no es sistema estable genérico

ESTADO: DSCN-G CONFIRMADO en la Tríada como marco de principios (disipación que
confina). NO es unificación de constantes (tests A/B/C/M negativos). La predicción
cuantitativa cruzada DSCN-G↔Collatz/NS sigue NEGATIVA (bounds independientes).

## Qué modifica en el resto de ecuaciones

NADA en las fórmulas. Lo que cambia es el STATUS de lectura:
- C3 (Ec. 6, θ_emerg=0.30): dejar de usarlo como predicción central. La valencia
  E_i sigue siendo válida como señal de sobreactivación, pero el "phase-hijacking
  antipodal" NO se sostiene a params originales.
- T3 (Ec. 3, bloqueo de fase): reportar 76.7% estricto, no 100%.
- T1 (Ec. 5, confinamiento por vitalidad): aclarar N_ss*≈4–5, no 9–10.

Ver también: `NOUS/DSCN-G/EXTENSIONS/DISCRETE_DYNAMICS/README.md` (actualizado
2026-07-25 con la conexión Tríada).
