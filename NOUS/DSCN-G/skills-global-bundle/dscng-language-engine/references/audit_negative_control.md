# Auditoría por NEGATIVE CONTROL (y contrastar contra GROUND TRUTH)

Técnica de auditoría de resultados circulares, distinta de SIGNAL-REMOVAL.
Nació de la auditoría v0.21 v8 (2026-07-28): un fix que PASÓ la auditoría de
signal-removal pero era circular porque el MECANISMO garantizaba la métrica por
construcción (repulsión incondicional aplicada a TODA palabra).

## Cuándo usarla
Cuando un experimento "pasa" con un resultado demasiado limpio Y el mecanismo
podría estar forzando la propiedad medida. Complementa (no reemplaza) a
signal-removal: corre LAS DOS antes de publicar "✓ confirmado".

## Pasos
1. IDENTIFICAR la población CONTROL: un subconjunto donde el efecto medido es
   FÍSICAMENTE IMPOSIBLE. Ej.: para "separación de sentidos" (polisemia), las
   palabras MONOSÉMICAS (un solo sentido por definición) son el control —si el
   mecanismo es genuino, NO deben separarse.
2. CORRER la MISMA métrica sobre la población control.
3. EXIGIR ASIMETRÍA: el fix genuino debe SEPARAR solo la población experimental
   (polisémicas) y DEJAR en 1 bucket dominante (>85%) a la control (monosémicas).
   Si la control TAMBIÉN "pasa" → el mecanismo produce el resultado, no el dato.
4. CONTRASTAR contra GROUND TRUTH cuando exista: si el corpus tiene etiquetas de
   sentido (A/B), verificar que el bucket asignado corresponda al sentido real
   (accuracy de desambiguación), no solo "¿hay 2 buckets?".
5. DECISIÓN: control limpia + ground truth correcto = GENUINO. Control contaminada
   = CIRCULAR (mismo peso que v0.9c/target-vector).

## Receta aplicada (v0.21 v8 → v0.21 v8b)
- `run_v21_v8_control.py` (PRUEBA DE CONTROL): reentrena v0.21 v8 REAL exacto
  (misma regla, mismo seed) y testa MONOSEMICAS vs POLISÉMICAS del Quijote.
  Resultado: quijote n=198 dom=0.55 sep=True; sancho n=202 dom=0.51 sep=True;
  caballero n=55 dom=0.82 sep=True; dijo n=154 dom=0.68 sep=True; casa n=21
  dom=1.00 sep=False. → 4/5 MONOSÉMICAS "separadas" ⇒ el 39/40 era artefacto.
- `run_v21_v8b.py` (RE-MEDICIÓN): corpus sintético CON ground truth (sentido A/B
  por palabra) + monosemicas de control; REPULSIÓN CONDICIONAL (repeler solo si
  cos(subnodo_k, subnodo_j) < 0.5, i.e. ya hubo contexto diverso). Test:
  acc_gt (bucket correcto vs sentido real), mono en 1 bucket, poli se reparte.
  Veredicto: GENUNO si mono_sep==0 y poli_sep>0 y acc_gt>0.7; ARTEFACTO si
  mono_sep >= 50%; PARCIAL en otro caso.

## Por qué no alcanza signal-removal solo
v0.21 v8 pasó signal-removal: al quitar el contexto, la repulsión seguía
separando (porque la repulsión era incondicional, no dependía del contexto).
El negative control la atrapa porque la población control NO PUEDE tener el
efecto —si el mecanismo lo produce igual, es circular por definición.

## Regla mnemotécnica
"Si tu prueba de polisemia también separa a 'quijote', no estás midiendo sentido."

## MATIZ 2026-07-28 (corpus REAL con contexto variable vs SINTÉTICO CONTROLADO)
El negative control en el Quijote REAL dio 4/5 monosémicas "separadas" (quijote,
sancho, caballero, dijo) — PERO en el sintético CONTROLADO (v0.21 v8b, contexto
FIJO para cada monosémica) dieron sep=False (0/3). ¿Por qué la diferencia?
- En corpus REAL, una palabra MONOSÉMICA aparece en contextos DISTINTOS a lo largo
  del libro ("quijote" cerca de "libro" a veces, de "dijo" otras). El embedding
  promedio por ocurrencia VARÍA → cae en buckets distintos → el criterio "2 buckets
  <85%" lo cuenta como "separado" por RUIDO DE CONTEXTO, no por sentido.
- En corpus SINTÉTICO CONTROLADO, la monosémica SIEMPRE viene con el MISMO
  contexto → sus ocurrencias son contextualmente idénticas → caen en 1 bucket.

LECCIÓN METODOLÓGICA: el criterio "¿hay 2 buckets con dominante <85%?" es FRÁGIL
en corpus real porque NO distingue separación por SENTIDO de separación por RUIDO
de contexto. Para un negative control LIMPIO hay que usar corpus SINTÉTICO
CONTROLADO (contexto fijo para la población control) donde el único eje de
variación es el sentido. El control en corpus real solo prueba que el criterio es
ruidoso, no que el mecanismo sea circular — hay que CRUZARLO con el sintético.

ADEMÁS: el veredicto "GENUNO/ARTEFACTO" debe basarse en acc_gt (bucket asignado vs
sentido REAL del ground truth), NO solo en "¿se separó?". v0.21 v8b dio acc_gt=0.74
(banco 1.0, mouse 0.95, llave 0.27 FALLA): el fix tiene SEÑAL PARCIAL, no es
"artefacto total" ni "genuino perfecto". El negative control da binario
(mono_sep), pero el ground truth da el GRADO. Usar AMBOS: mono_sep=0 (control
limpio) + acc_gt alto (señal real) = genuino con magnitud conocida.

FLUJO CORRECTO cuando el usuario encuentra el bug en CÓDIGO (no en resultados):
correr el negative control que él propone (acá: monosémicas del Quijote), confirmar
empíricamente, y luego re-medir con instrumento correcto (sintético+gt) para no
tirar el mecanismo entero si el problema era solo el instrumento de medición. Eso
es lo que separa "refutar el claim" de "refutar la idea": v0.21 v8 era circular en
su MEDICIÓN, pero anchor+repulsión como CONCEPTO siguió siendo válido tras medirlo
bien (v0.21 v8b). Ver references/oversmoothing_fix.md (nota de refutación).
