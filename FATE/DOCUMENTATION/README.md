# FATE — Documentación

FATE = aplicación de drug discovery (optimizador black-box) construida sobre
el sustrato cognitivo DSCN-G. Ver `../DSCNG_INTERFACE/DSCNG_INTERFACE.md`
para la relación con el núcleo.

## Contenido
- `ANALISIS_FATE_V6.md` — análisis completo y validación (benchmarks
  sintéticos, EGFR, escalabilidad, throughput, novedad científica).
- `FATE_v6_STATUS.md` — status de benchmarks v6 (Phase 1 completa, Phase 2
  parcial D=2048), protocolo EGFR y aspirina.

## Experiments
- `../EXPERIMENTS/Aspirina/` — BRICS + DSCN-G (random search, pendiente FATE real).
- `../EXPERIMENTS/EGFR_Benchmark/` — EGFR drug discovery (ChEMBL IC50).
- `../EXPERIMENTS/benchmarks/` — resultados crudos de benchmarks.

## Patch DSCN-G
- `../fate_dscng_patch/` — parche que reemplaza la capa cognitiva de FATE
  por dinámicas auditadas de DSCN-G v3.
