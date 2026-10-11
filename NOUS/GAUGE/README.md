# GAUGE — Confinamiento No-Abeliano en Circulantes Fractales

**Paper:** `PAPER/DSCN_G_Gauge.md` — SU(2) sobre C_N(S) fractal.

**Estado epistemico (auditoria Metodo Integral, 2026-10-11):** modelo de
juguete bien fundado; honestamente declarado como NO-prueba del Milenio.
Teoremas 4.1/4.4.2 en regimenes asintoticos; Conjeturas G1-G4 abiertas y
etiquetadas como tales.

## Artefactos verificados

- `gauge_mc.py` (2026-10-11): extraido del Apendice A del paper y EJECUTADO
  con exito — N=16, SU(2), Metropolis, barrido beta 0.1-10:
  plaquette -0.02 → 0.87, Wilson loops crecientes. Resultado PRELIMINAR
  honesto (el propio paper declara: N=16 muy chico, se requiere N>=64 con
  heat bath Kennedy-Pendleton para G1 cuantitativo).

## Que le falta

1. N=64 + heat bath (trabajo declarado como proximo paso por el propio paper)
2. Extraccion de sigma(beta) via Creutz ratios con errores < 5% (mas sweeps)
3. La herencia lambda_2=4 es re-etiquetado del sustrato, no teorema propio

## Referencias externas verificadas (2026-10-11)

- Creutz 1980 (citado en el paper): Metropolis for SU(2) lattice gauge
- Kennedy-Pendleton heat bath: el algoritmo que falta para el paso siguiente

