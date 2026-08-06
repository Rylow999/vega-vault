# Claims Status — DSCN-G v1.0

> Resumen tabular. El detalle claim-por-claim, con criterios de
> falsificación y las 6 rondas de auditoría (2026-07-22/24), vive en
> `DOCUMENTATION/auditoria/claims_falsifiable.md` — este archivo no lo
> reemplaza, lo indexa.

| Afirmación | Categoría | Estado |
|---|---|---|
| T2 — ω alignment convergence (1.0000) | CORE | ✅ Validado |
| T1 — cota universal + punto fijo (N_ss*≤1/θ_death) | CORE | ✅ Validado |
| T1 — maximalidad (simulación real, inyección al umbral) | CORE | ✅ Validado |
| N-back v6 — N_ss* empírico = 9.50±1.02 | CORE | ✅ Validado |
| N-back v6 — WM sin escalón abrupto (forma cualitativa) | CORE | ✅ Validado |
| Comparación vs. RNN vainilla | CORE | ✅ Validado |
| T3 — consenso de fase (criterio estricto R≥0.9 = 76.7%) | CORE | ⚠️ Validado con matiz — reportar 76.7% estricto, no 100% laxo |
| N_ss* de T1 (~4–5, no ~9–10 — ese número es del N-back) | CORE | ⚠️ Corregido en el paper v3 |
| d′(10-back)=0.97, d′(15-back)=0.82 (valores v6, no v5) | CORE | ⚠️ Corregido en el paper v3 |
| C3 / Face Hijacking (Phase Hijacking) | EXTENSIÓN | ❌ No sostenido a params originales (0.9% triggers, ΔPLV≈0); rediseño llega a 30.2%, lejos de "la norma" |
| Φ_proxy — escalado O(log N) | EXTENSIÓN | ⚠️ Hipótesis — dos definiciones probadas (MI cruda, TE-bottleneck), ninguna sostiene la predicción |
| Φ_proxy — TE-bottleneck como métrica (arrastre vs. integración) | EXTENSIÓN | ✅ Métrica aprobada y útil, aunque no rescata el claim de escalado |
| Dinámica discreta — relación con el núcleo (Tríada disipativa) | EXTENSIÓN | ✅ Marco formalizado 2026-07-25: DSCN-G = capa cognitiva de la Tríada (fase φ_i + vector ω_i → vitalidad V_i). Conecta con DDSD/Collatz/NS/Riemann por disipación. Ver `EXTENSIONS/DISCRETE_DYNAMICS/README.md` y `/TRIADA_AUTORREGULACION/` |
| DSCN-G como NCC formalmente completo | ESPECULATIVO | ⚠️ Hipótesis — solo "correlaciona con consciencia", no "es consciente" |
| Drug discovery (conexión con FATE) | ESPECULATIVO | ⚠️ Hipótesis — "encuentra análogos con pIC50 predicho X", no "descubre fármacos" |
| Validación EEG/fMRI | FUTURO | 🔬 Investigación — pendiente, declarado en el paper §5.5 |
| Ablation studies, sensibilidad a parámetros | FUTURO | 🔬 Investigación — pendiente |
| Baseline LSTM/GRU/Transformer | FUTURO | 🔬 Investigación — pendiente (solo hay RNN vainilla) |

## Categorías

- **CORE** — parte del núcleo congelado v1.0, en el paper.
- **EXPERIMENTAL** — probado, resultado no concluyente o negativo.
- **EXTENSIÓN** — fuera del núcleo por diseño, en `EXTENSIONS/`.
- **ESPECULATIVO** — posición honesta declarada, no verificable con el
  método actual.
- **FUTURO** — investigación declarada, no bloquea el freeze.

## Resumen de conteo (auditoría Ronda 4–6)

6 claims se sostienen sin cambios · 3 necesitaron corrección de números
(ya aplicada en el paper v3) · 1 no se sostiene a params originales pero
mejora con rediseño sin llegar a la norma (C3) · 1 con evidencia
preliminar no concluyente (Φ_proxy, escalado).
