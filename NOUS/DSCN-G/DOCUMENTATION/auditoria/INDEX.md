# DSCN-G v3 — Paper Kit (con 6 rondas de auditoría, 2026-07-22/24)

**Si vas a leer un solo archivo, que sea `AUDIT_NOTES_ROUND6.md`** — tiene
el estado más reciente: TE-bottleneck pasó la prueba de robustez (3
particiones, incluido un control negativo que sí distingue el resultado
de un artefacto genérico) y quedó **aprobada** como definición operativa
de Φ_proxy; la analogía "tálamo/hub_boost" quedó **retirada** del paper;
y el barrido O(log N) de Claim 7, repetido con la métrica ya aprobada,
**sigue sin sostener la predicción** (esta vez el resultado es
prácticamente plano/ruidoso en todo el rango de N*, no solo un mal
ajuste como en Ronda 4).

## Orden de lectura recomendado

1. `AUDIT_NOTES.md` — ronda 1: bugs de pipeline (Kuramoto no sincrónico,
   N-back no guardaba resultados) y primer chequeo reclamado-vs-reproducido
   de T1/T2/T3/C3 y N-back.
2. `AUDIT_NOTES_ROUND2.md` — ronda 2: reproducción independiente de la
   ronda 1 (confirmada, byte a byte) + hallazgo del bug de diseño en el
   N-back (identidad vs. ocurrencia) + dos fixes menores de código.
3. `AUDIT_NOTES_ROUND3.md` — ronda 3: rediseño del N-back (opción 3 sola
   no alcanzó, se implementó la opción 1 combinada con 3) + números finales
   + qué texto reemplazar en el paper.
4. `AUDIT_NOTES_ROUND4.md` — ronda 4: simulación real de la maximalidad
   de T1 (sostenida, con el protocolo de inyección correcto), rediseño de
   C3 (mejora parcial, 0.9%→30.2%, sigue sin ser la norma), primera
   definición propuesta de Φ_proxy (no aprobada, evidencia no concluyente)
   y baseline de RNN vainilla contra el N-back (pedido de
   `REVIEW_RECOMMENDATIONS.md`).
5. `AUDIT_NOTES_ROUND5.md` — ronda 5: modelo "talámico" (`hub_boost`)
   reubicado correctamente (`_apply_hijack_pull`, no la matriz de
   Kuramoto) — aun así sin efecto en el rise_rate de C3, por saturación
   de la métrica, no por el bug de ubicación de Ronda 4. Φ_proxy
   rediseñado con partición root/periferia + transfer entropy
   (Geweke, mínimo de las dos direcciones) en vez de MI cruda: la MI
   sube durante el hijack (refuerza Ronda 4) pero el TE-bottleneck baja
   en las 4 configuraciones — evidencia de que lo que sube es arrastre,
   no integración genuina.
6. `AUDIT_NOTES_ROUND6.md` — ronda 6: retiro formal de la analogía
   "tálamo/hub_boost" (Claim 5, sin cambio de veredicto); prueba de
   robustez de TE-bottleneck contra 2 particiones adicionales (una de
   ellas control negativo) y 2 lags de VAR — el patrón de Ronda 5 se
   sostiene en root-vs-periferia y root-vs-1-seguidor, y el control
   negativo va en dirección opuesta (evidencia de que no es un
   artefacto genérico); con eso, TE-bottleneck queda **aprobada**. Se
   repite el barrido O(log N) de Claim 7 con la métrica ya aprobada:
   sigue sin sostener la predicción, y esta vez el resultado es
   prácticamente plano en todo el rango de N* probado.
7. `claims_falsifiable.md` y `paper_structure.md` — ya actualizados con
   los números de las 6 rondas, listos para usarse como fuente al
   escribir la prosa final del paper.

## Estructura de carpetas

- **`core/`** — El núcleo (`verify_dscng_v3.py`, teoremas T1/T2/T3 + C3).
  Sin cambios desde la ronda 1 — todo lo nuevo de la ronda 4
  (`verify_maximality_real.py`, `verify_phi_proxy.py`,
  `verify_c3_redesign.py`) son scripts separados que lo importan sin
  tocarlo, igual que v6 no tocó v5 del N-back.
  `verification_results_v3.json` son los resultados de T1/T2/T3/C3
  (fórmula aproximada), reproducidos de forma independiente en la ronda 2.
  `maximality_real_results.json`, `phi_proxy_scaling_results.json` y
  `c3_redesign_results.json` son los resultados nuevos de la ronda 4.

- **`baselines/`** (nueva en ronda 4) — `rnn_baseline.py`, comparación
  contra un RNN recurrente simple en el N-back, pedido explícito de
  `REVIEW_RECOMMENDATIONS.md`. `rnn_baseline_results.json` son los
  resultados.

- **Nueva en ronda 5** (en `core/`) — `thalamic_model.py` (subclase
  `ThalamicDSCN_G_v3` con `hub_boost`, núcleo sin tocar; analogía
  retirada del paper en Ronda 6, código conservado por trazabilidad),
  `verify_phi_proxy_v3.py` (Φ_proxy con partición root/periferia +
  transfer entropy, resultado en `phi_proxy_v3_results.json`),
  `verify_hub_boost_fix.py` (repite el chequeo de Ronda 4 con el boost
  ya reubicado, resultado en `hub_boost_fix_results.json`).

- **Nueva en ronda 6** (en `core/`) — `verify_te_bottleneck_robustness.py`
  (3 particiones × 2 lags, resultado en
  `te_bottleneck_robustness_results.json`; incluye P1, el control
  negativo que justifica aprobar la métrica), `verify_te_bottleneck_scaling.py`
  (repite el barrido O(log N) de Ronda 4 con TE-bottleneck ya aprobada,
  resultado en `te_bottleneck_scaling_results.json`). Ninguno de los dos
  toca `verify_dscng_v3.py`, `thalamic_model.py` ni `verify_phi_proxy_v3.py`.

- **`nback_v5_legacy_flawed/`** — La versión original del N-back, con los
  fixes de código de la ronda 2 (import no usado, corrección de d')
  aplicados, pero **con el bug de diseño de fondo sin corregir**
  (`hit_rate=1.0` siempre — ver `AUDIT_NOTES_ROUND2.md` §2). Se conserva
  por transparencia/trazabilidad, **no usar sus números en el paper.**

- **`nback_v6_corrected/`** — La versión corregida (occurrence-aware). **Es
  la que hay que usar para escribir la Sección 4 del paper.** Ver
  `AUDIT_NOTES_ROUND3.md` para la tabla completa y el texto sugerido.

- Nivel superior: `README.md` (original, con la advertencia de ronda 1),
  `run_pipeline.sh` (corre el núcleo + N-back v5 legacy — no incluye v6
  todavía, correrlo aparte con
  `python3 nback_v6_corrected/nback_v6_occurrence_aware.py`),
  `analyze_results.py` (lee los JSON de `nback_v5_legacy_flawed/` por
  default — pasarle la ruta de `nback_v6_corrected/nback_v6_paper_ready.json`
  a mano si se quiere analizar la versión corregida).
