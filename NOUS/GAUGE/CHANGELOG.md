# CHANGELOG

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [2026-10-15] — Reproduccion cruzada del Monte Carlo

### Agregado
- `verification/gauge_mc_output_2026-10-15.txt` — segunda corrida
  independiente del `gauge_mc.py` original (sin modificaciones), en otro
  host: plaquette -0.02 -> 0.87 con beta, Wilson loops crecientes.
  Reproduce la corrida del 2026-10-11 (misma estructura cualitativa).

### Corregido
- README: explicitado que el MC actual NO establece area law (la plaquette
  satura ~0.87 en beta=10 y los loops no decaen con el area en este rango);
  la senal de confinamiento queda demostrada solo en los regimenes
  asintoticos del paper (character expansion / aproximacion gaussiana).

## [2026-10-11] — Auditoria Metodo Integral + primer run real

### Agregado
- `gauge_mc.py` extraido del Apendice A del paper (antes vivia solo como
  texto dentro del markdown) y EJECUTADO por primera vez.

## [2026-06] — Paper original

### Agregado
- Formulacion SU(2) sobre C_N(S); conjeturas G1-G3; teoremas 4.1/4.4.2 en
  regimenes asintoticos; taxonomia de tres regimenes (Tipo I/II/III).
