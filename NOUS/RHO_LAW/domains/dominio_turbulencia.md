# Dominio: Turbulencia (Navier-Stokes) — análogo de la ley ρ

**Fuente:** LOGOS/NAVIER_STOKES/sddf_v3 (SDDF, curvatura espectral G[u])

## El patrón

El observable es G[u] = ∫ (d ln E/d ln k)² d ln k sobre el espectro de energía.

- El escalamiento teórico es G* ~ (25/12)·ln Re — crece suavemente con Re.
- Cuando el espectro se **mide con grilla discreta**, el error de truncamiento
  NO decae monótonamente con N: oscila.
- Un cambio de variable mal elegido (Pao vs Pope, quimera) desplaza el offset
  b(δ) sin que el prefactor 25/12 cambie.

**Análogo de la ley ρ:** el observador (grilla/ventana) tiene un límite de
resolución. Cerca de ese límite, la medición deja de ser fiel al sustrato — 
no porque el flujo "no tenga" más estructura, sino porque el instrumento no la
resuelve.

**Experimento posible:** tomar los CSV de SDDF (`03_sensibilidad_umbral.csv`,
`07_convergencia_grilla.csv`) y mostrar que el "error de observador" sigue la
misma forma: una región estable, una singularidad, y recuperación.

**Pregunta clave:** ¿el error de truncamiento tiene un "ρ" (razón entre frecuencias
representadas y puntos de grilla) donde la medición se rompe de forma puntual?
