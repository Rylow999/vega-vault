# CHANGELOG

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [2026-10-25] — N=64: primera corrida a mayor tamano

### Agregado
- `verification/gauge_mc_N64_output_2026-10-25.txt` — MC Metropolis en N=64
  (|S|=6, 352 aristas, 320 plaquettes), seed 42, 500 termalizacion + 500
  medicion, 11 betas 0.1-10 (fino cerca de beta_c~2.5). Reproduce la
  estructura cualitativa de N=16: plaquette 0.029 -> 0.863, loops crecientes,
  saturacion ~0.86 en beta=10.

### Nota honesta
- El area law SIGUE sin establecerse por MC: en beta=10 la plaquette satura
  0.863 (no ~1) y W(2,2) ~ W(1,1) (los loops NO decaen con el area en este
  rango). La senal de confinamiento queda demostrada solo en los regimenes
  asintoticos del paper (character expansion / gaussiana). Pendiente:
  heat bath Kennedy-Pendleton y ratios de Creutz con errores < 5% en el
  lado de acoplamiento fuerte (beta < beta_c), donde la extraccion de
  sigma(beta) es viable.

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
