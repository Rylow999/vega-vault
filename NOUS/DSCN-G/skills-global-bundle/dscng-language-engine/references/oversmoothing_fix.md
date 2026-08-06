# Oversmoothing fix (v0.21 v8) — receta y resultados

> ⚠️ REFUTADO 2026-07-28 (AUDITORÍA DE NEGATIVE CONTROL). v0.21 v8 PASÓ la
> auditoría de signal-removal pero era CIRCULAR: la repulsión se aplicaba
> INCONDICIONALMENTE a TODA palabra, así que el criterio "¿se separan los 2
> sub-embeddings?" daba SÍ para cualquier palabra —incluidas las MONOSÉMICAS.
> Control empírico (run_v21_v8_control.py): quijote/sancho/caballero/dijo
> (monosémicas) también dieron "separadas" (4/5). El "39/40 Don Quijote real"
> era RUIDO CON FORMA DE SEÑAL, misma familia circular que v0.9c. El CONCEPTO
> de anchor+repulsion sigue siendo válido para oversmoothing, pero el INSTRUMENTO
> de medición original era inválido. Re-medición honesta en curso: v0.21 v8b
> (repulsión CONDICIONAL + ground truth + control monosémico). Ver
> `references/audit_negative_control.md`. NO cites "39/40" como confirmado.

Diagnóstico de Luciano (2026-07-28), el aporte teórico clave de la noche.

## El problema (propiedad del operador, no del sustrato)
La regla Hebb pura `ω[a] = (1-β)·ω[a] + β·ω[b]` es DIFUSIÓN de grafo = power
iteration de una cadena de Markov. Converge al autovector dominante. La
separación de sentidos es el componente de ALTA frecuencia del espectro del
operador: un filtro pasa-bajos lo mata PRIMERO, sin importar D/épocas/corpus.
Por eso v0.21 v1→v7 daba separación SIEMPRE transitoria y luego colapso a 0.

## Los dos arreglos (SIN backprop, O(K·D), solo dot products)
1. ANCHOR / RESTART (APPNP): `ω[a] = α·ω0[a] + (1-α)·[(1-β)·ω[a] + β·ω[b]]`.
   ω0 copia inicial inerosionable → rompe la convergencia al autovector dominante.
2. REPULSIÓN SIBLING: `ω[a][k] -= β_rep·(ω[a][j]/|ω[a][j]|)` (j=1-k). Evita que
   los dos sentidos de una palabra se fundan en uno.

## Resultados ORIGINALES (v0.21 v8 — REFUTADOS, ver banner)
- Sintético contrastivo: α 0.05/0.10/0.20 → 3/3 estable ep1–ep15.
- Don Quijote REAL: ep1 39/40 … ep8 39/40 estable.
ESTOS NÚMEROS YA NO SON VÁLIDOS COMO EVIDENCIA: el criterio "2 buckets <85%"
no contrastaba con ground truth y la repulsión era incondicional (ver banner).

## Re-medición honesta (v0.21 v8b, EN CURSO 2026-07-28)
Instrumento CORRECTO: corpus sintético CON ground truth (sentido A vs B);
palabras MONOSÉMICAS de control (quijote, sancho, caballero) en contexto fijo;
REPULSIÓN CONDICIONAL (solo repeler si los 2 buckets ya recibieron contexto
DIVERGENTE, cos<0.5); test (1) ¿bucket = sentido real? (acc_gt), (2) ¿monosémicas
en 1 bucket?, (3) ¿polisémicas se reparten? Si mono queda en 1 bucket y poli se
separa CON bucket correcto → fix GENUINO y se reanuda v0.22+ sobre base honesta.

## REGLA de oro
Si la regla de update es un filtro pasa-bajos (difusión), el fix es ANCHOR +
REPULSIÓN. PERO el instrumento de medición debe usar NEGATIVE CONTROL
(monosémicas NO deben separarse) y GROUND TRUTH, no solo "¿se separó?".

## Archivos en el repo
- `v0.21_fractal/run_v21_v8.py` — anchor+repulsion, barrido de α, sintético.
- `v0.21_fractal/run_v21_v8_real.py` — Don Quijote real (REFUTADO).
- `run_v21_v8_control.py` — PRUEBA DE CONTROL monosémica (4/5 monosemicas "separadas").
- `run_v21_v8b.py` — re-medición con instrumento correcto (en curso).
