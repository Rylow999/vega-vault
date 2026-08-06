# VALIDATION

Responde: **¿Qué evidencia existe?**

## RESULTS/

- `verification_results_v3.json` — salida cruda de `verify_theorem_1/2/3` y
  `verify_c3` (30 seeds, 2000 steps, escala canónica de la Ronda 4 de auditoría).
- `maximality_real_results.json` — salida de la sub-claim de maximalidad de T1
  (simulación real de inyección de nodo, no la fórmula `rho_approx` original).

## Documentos

- [`CONSISTENCY_CHECK.md`](./CONSISTENCY_CHECK.md) — verificación de que
  código, documentación y experimentos son coherentes entre sí (paso 4 de la
  guía de congelación).

## Evidencia completa (fuera de CORE, no duplicada aquí)

El detalle claim-por-claim, con criterios de falsificación y las 6 rondas de
auditoría, vive en `../../DOCUMENTATION/auditoria/` (no se copia aquí para
evitar que las dos versiones diverjan). El resumen tabular está en
`../../CLAIMS_STATUS.md`. Los experimentos de N-back, comparación con RNN,
sincronización y ablaciones están en `../../EXPERIMENTS/` (son evidencia del
núcleo pero corridas más grandes que no viven dentro de CORE/).
