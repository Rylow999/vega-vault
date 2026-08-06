# v0.25 v2 / v2b / v2c — Integración Transformer + Root (2026-07-28)

## Contexto
v0.25 original asumió root=proyector de sentido sobre grafo rústico (v0.21 v8).
Pero v0.21 v8→v8f CERRARON que el grafo rústico no separa sentidos (acc_gt<=0.53,
azar), y v0.22 v2 confirmó que el root no aporta como proyector (root≈baseline).

v0.25 v2 re-define sobre la arquitectura CORRECTA (NOUS v4):
- TRANSFORMER = contexto/sentido (backprop, separa polisemia).
- ROOT/GRAFO = memoria/dolor/foco sobre el contexto (NO proyector de sentido).

## Experimentos

### v0.25 v2 — root con slots + vitalidad + Hebb (competencia sobre contexto)
- Transformer: acc_pred=0.907 (aprende, 0.907 >> 0.013 azar).
- Root (slots inicializados aleatoriamente + vitalidad decaimiento 0.85 + Hebb):
  acc_gt=0.546 (azar), foco_acc=0.546, dolor_max=0.884.
- Veredicto: CICLO NO FUNCIONAL para polisemia. Atracción temprana equivocada.

### v0.25 v2b — root sobre decisión del transformer (Wo)
- Root refuerza la decisión del transformer (Hebb sobre la decisión).
- acc_gt_root=0.544 (azar). El contexto promedio mezcla A/B → decisión azar.
- Veredicto: el root no refuerza el sentido correcto.

### v0.25 v2c — root refuerza la decisión del transformer REAL (Wo entrenado)
- Transformer decide A/B usando Wo (predice próximo token).
- acc_gt_root=0.544 (azar), dolor_en_duda=0.841, W_contrae=0.982.
- Veredicto: el root NO separa sentido PERO funciona como SISTEMA DE DUDA
  (detecta duda, contrae W).

## Veredicto final
- El TRANSFORMER separa sentidos POR SÍ SOLO (acc_pred=0.907).
- El ROOT no separa sentido (acc_gt≈azar en 4 experimentos: v0.22 v2, v0.25 v2,
  v2b, v2c) PERO funciona como SISTEMA DE DUDA (dolor_en_duda=0.841,
  W_contrae=0.982).
- COHERGENTE con NOUS v4: transformer=sentido, root=memoria/dolor/foco sobre
  el contexto. El root no es clasificador de sentido; es sistema de duda y foco.
- v0.25 v2 CIERRA: arquitectura correcta = transformer=sentido + root=memoria/dolor.
  El root aporta a MEMORIA (retención de contexto) y DOLOR (foco competitivo),
  NO a polisemia.

## Instrumento correcto usado
- Corpus sintético CON ground truth (sentido A/B por ocurrencia).
- acc_gt (bucket/slot vs ground truth), no solo "¿se separó?".
- Negative control: monosémicas (deben quedar en 1 bucket).
- Curva episodio a época.
- Smoke test antes de background.
- Baseline en condiciones idénticas.