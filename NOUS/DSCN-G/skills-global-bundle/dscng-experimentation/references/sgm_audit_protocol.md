# Protocolo de Auditoría SGM — 6 Controles Obligatorios (2026-08-02)

Antes de cualquier experimento que produzca un resultado "✓ confirmado", debe pasar los 6 controles:

## (a) Supervised Baseline en Condiciones Idénticas
Correr el baseline (sin el mecanismo a testear) en LAS MISAS condiciones: mismo corpus, mismo V, mismas épocas, misma semilla. NUNCA comparar contra un número de otro experimento.

Ejemplo válido: v0.14d audit — base=0.0237 vs híbrido=0.0958 (mismo V=150, mismo corpus, mismos epochs).
Ejemplo inválido: v0.14d original comparaba 10.55% (V=150) vs 10.11% (V=200, otro corpus).

## (b) Permutation/Random Control
Shuffle las etiquetas/contextos/clusters al azar y contar cuántos "efectos" aparecen por puro ruido. Ese es tu false-positive rate. Si tu resultado no supera al control permutado, no es real.

## (c) Threshold Fijo y Justificado
NO cambiar el umbral entre runs para forzar el resultado. fijarlo ANTES (ej: cos<0.5 para separación de sentidos) y justificarlo (0.5 = ortogonalidad en espacio normalizado).

## (d) ≥3 Seeds + Varianza
Un solo número de una sola seed NO es un resultado. Correr ≥3 seeds, promediar, reportar varianza (std/desvío).

## (e) Smoke Test Antes de Background
```python
python3 -c "import run_vXX as m; o=m.build_graph([...], epochs=2); print(m.decode(o,...)); print(m.run_cycle(...))"
```
Si alguna función devuelve None o lanza → cuerpo/return roto → corregir ANTES del background.

## (f) Ground Truth (cuando disponible)
Usar acc_gt (bucket vs sentido real), no solo "¿se separó?". En polisemia, anotar manualmente qué sentido aparece en cada contexto del corpus y comparar contra la asignación del grafo.