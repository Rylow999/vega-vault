# CHANGELOG

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [2026-10-15] — Verificacion y hallazgo de auditoria

### Agregado
- `verification/verify_lambda2.py` — Lemma 4.1 (iii) verificado: lambda2 = 4
  EXACTO para m=3..16 (error < 1e-12; espectro exacto del Laplaciano
  circulante, sin diagonalizacion numerica aproximada). Primer artefacto
  numerico real del paper.
- `verification/verify_rg_consistency.py` — refit del exponente RG sobre las
  tablas impresas de QUANTUM (8.3) y COSMOS (4.3).
- `verification/verify_q1_bifurcation.py` — parte clasica de Q1: la rigidez
  K_eff = (eta R/2) cos(dphi) se anula exactamente en dphi = pi/2.

### Hallazgo (etiquetado, Metodo Integral)
- **La tabla alpha(m) de la seccion 8.3 NO sigue la ley declarada:**
  beta_fit = 0.26 vs 2pi/D = 2.094 (desviacion 87%), mientras el paper
  declara "0.00% error". La tabla de COSMOS 4.3 SI lo hace (2.0977, 0.16%).
  Seccion 8.3 marcada para revision.
- Gamma_dec ~ sin^2(dphi) (Lindblad): `NOT_REPRODUCIBLE_FROM_TEXT` — el
  operador L_k del Apendice H.2 no esta incluido en el markdown.

## [2026-10-11] — Auditoria Metodo Integral

### Corregido
- Q1/Q3 re-etiquetados de "Proven" a heuristicos/esbozos.
- "verified via Python" REMOVIDO del abstract (0 archivos Python en disco).
- lambda2 = 4 declarado como algebra exacta con verificacion numerica
  declarada PERO AUSENTE en disco (estado hasta 2026-10-15).

## [2026-06] — v9.1 (Verified Edition)

### Agregado
- Formalizacion cuantica: espacio de Hilbert por nodo, Hamiltoniano de tres
  terminos, Lindblad en forma GKLS correcta (correccion v7.0).
- Lemma 4.1 (gap espectral), Teorema 5.1 (D=3), mecanismo de Hagedorn
  corregido (l_coh en [2, 35] l_P), flujo RG logaritmico.
