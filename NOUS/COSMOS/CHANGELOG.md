# CHANGELOG

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
(versiones por fecha; este proyecto no usa semver).

## [2026-10-15] — Verificacion y auditoria de artefactos

### Agregado
- `verification/` con scripts reproducibles (stdlib puro) y outputs:
  - Predicciones (a)-(d) reproducidas en forma cerrada:
    (a) 3.49% (0.68 sigma), (c) 0.777 grados (0.40%), (d) 73.13 (0.09 sigma).
  - Refit del exponente RG sobre la tabla impresa 4.3: beta=2.0977
    (consistencia interna 0.16%).
- Etiquetado honesto: el Monte Carlo n=50.000 (sec 7 / Apendice J) queda
  `NOT_REPRODUCIBLE_FROM_TEXT` (modelo estocastico no especificado en el paper).

### Corregido
- README reescrito: separado el historial a este CHANGELOG; literatura DESI
  DR2 / H0DN / k-essence actualizada y verificada contra fuente.

## [2026-10-11] — Auditoria Metodo Integral

### Corregido
- "VERIFIED" re-etiquetado a "derivacion interna" (prediccion b).
- Claim "tests/" y "simulaciones" del Data Availability: removido (0 archivos
  Python en disco en ese momento).
- READMEs de COSMOS/QUANTUM/GAUGE reescritos con estado auditado.

## [2026-06] — v8.1 (Verified Edition)

### Agregado
- Unificacion EFT DM-DE (Yukawa-Poisson + quintaesencia slow-roll).
- Predicciones (a)-(d) contra CosmicFlows-4, DESI DR9 y SH0ES.
- Flujo RG logaritmico con beta = 2pi/D.
- alpha0 derivado (13-07-2026) via dH0 = f_coh * H_aux_scale (Gap G3).
