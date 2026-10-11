# QUANTUM — Formalizacion Cuantica del Sustrato DSCN-G

**Paper:** `PAPER/dscn_g_quantum_v9_1_paper.md` (v9.1, re-etiquetado 2026-10-11).

**Estado (auditoria Metodo Integral):** paper CONCEPTUAL de arquitectura.
Sus claims de verificacion numerica estaban SIN artefactos (0 archivos
Python en disco) — re-etiquetados en el abstract. Lo que queda en pie:

- La ESTRUCTURA: Hilbert por nodo, Lindblad corregido v7.0, Hamiltoniano
  de tres terminos, seis axiomas declarados
- lambda_2 = 4 del circulante: ALGEBRA EXACTA (demostrable con teoria
  espectral de circulantes — eigenvalores de matrices circulares son
  suma de raices de la unidad, resultado clasico)
- D = 3, Hagedorn, flujo RG logaritmico: derivaciones internas del modelo

## Que le falta (por prioridad)

1. **Las simulaciones Python citadas** — no existen. lambda_2=4 es un
   script de 15 lineas (diagonalizar el circulante); la decoherencia de
   Lindblad es integracion ODE. Ambos son de una tarde.
2. Formalizacion de Q1/Q3 (los "proofs" son esbozos de mecanismo)
3. La derivacion alpha_0 (declarada DERIVED 2026-07-13 pero sin script)

## Referencias externas (verificadas 2026-10-11)

- Eigenvalores de circulantes: resultado clasico (Varga; teoria espectral
  de grafos — el espectro del circulante es suma de cosenos de raices
  de la unidad; lambda_2=4 sigue de 2-2cos(2*pi/N) con la S fractal)
- Lindblad 1976: la dinamistica de sistemas abiertos (el paper la usa
  correctamente en forma GKLS desde v7.0)
- Lieb-Robinson 1972: cotas de propagacion en reticulos — la aplicacion
  a cadenas es estandar; a circulantes fractales requiere adaptacion

