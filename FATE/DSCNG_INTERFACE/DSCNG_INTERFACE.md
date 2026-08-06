# FATE ← DSCN-G: Interfaz y dependencias

> Documentación de la relación entre FATE (aplicación de drug discovery)
> y DSCN-G (núcleo teórico / motor cognitivo). FATE es una aplicación
> CONSTRUIDA SOBRE DSCN-G; está desacoplada del núcleo teórico.

## Qué componentes de DSCN-G utiliza FATE

FATE v6 reemplaza su "capa cognitiva" original (que tenía solo el nombre
de DSCN-G pero ninguna relación real con sus ecuaciones) por las dinámicas
**auditadas** de DSCN-G v3:

- **Acoplamiento de fase Kuramoto real** → coordinación de la población de
  candidatos (antes: `resonance` por similitud coseno, ad-hoc).
- **Homeostasis por vitalidad real** → densidad de visitas / pods
  ACTIVE/DORMANT/HIBERNATE (antes: `state_weight` por conteo simple).
- **ω (vector semántico)** → EWMA de campeones con dinámica de convergencia
  auditada (T2: alineación 1.0000).

El parche está en `FATE/fate_dscng_patch/` (fate_engine.c.diff,
fate_engine.h.diff, dscng_smoke_test.c, README.md). Se aplica sobre
`fate-v6-modular` (commit 2026-07-19).

## Qué partes son propias de FATE (NO vienen de DSCN-G)

- El optimizador black-box (batch protocol, escapes CTEG/Collatz, ULTRA_CHROMO).
- Los oráculos (similarity-based sobre ChEMBL, fingerprints moleculares).
- La representación química (BRICS, SMILES, fingerprints).
- El benchmark (moving peaks, rastrigin, schwefel, EGFR, Aspirina).

## Dependencias / contrato

- FATE consume de DSCN-G la **topología de fase** (ω, φ) como motor de
  diversidad y escape de estancamiento. No consume T1/T3 verificados del
  núcleo teórico salvo por el mecanismo de coordinación (Kuramoto) y la
  homeostasis (vitalidad).
- C3 / Face Hijacking y Φ_proxy NO se usan en FATE (son extensión abierta,
  ver NOUS/DSCN-G/EXTENSIONS/).
- El claim de drug discovery (Claim 10 del paper DSCN-G) vive aquí, en FATE,
  no en el núcleo DSCN-G.

## Caveat de versión (abierto, no bloquea freeze)

`Master-Document/DSCN-G_Master_Document.md` (NOUS Paper 0) y
`SHARED/ontology/notes/DSCN-G_Master_Document.md` citan **FATE v4/v5**
(TNSEngine, CTEGCtrl, TabuMem, TopoMap, ULTRA_CHROMO, USE_COG) como la
versión validada. Esta interfaz documenta **FATE v6**
(`FATE/DOCUMENTATION/ANALISIS_FATE_V6.md`, `FATE_v6_STATUS.md`), que
reemplaza la capa cognitiva ad-hoc de v5 por las dinámicas auditadas de
DSCN-G v3 descritas arriba. Los dos documentos NO están actualizados entre
sí — pendiente decidir si se actualiza el Master-Document a v6 o se marca
v4/v5 como benchmark histórico. Ver `../../ROADMAP.md`, Bloque C.

## Estado de validación

- FATE v6: ver `FATE/DOCUMENTATION/ANALISIS_FATE_V6.md` y
  `FATE/DOCUMENTATION/FATE_v6_STATUS.md` (benchmarks sintéticos + EGFR +
  escalabilidad hasta D=1024).
- NOTA de rigor: los .md de FATE v6 llevan fecha 2026-07-19 y citan FATE
  v4/v5 en el paper DSCN-G como validación; FATE v6 es la versión modular
  GPU-accelerated. El patch cita `verify_dscng_v2.py` / `DSCN_G_v2` por
  haberse escrito antes del rename a v3 — el mecanismo es el mismo (v3).
