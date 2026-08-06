# dscng_core.py — Core modular del Language Engine

Qué exporta `dscng_core.py` (estado 2026-07-31):
- funciones base: `dot`, `norm`, `cos`, `softmax`
- `MetricLogger` — emite SIEMPRE `acc_pred`, `acc_gt`, `dolor`, `foco_acc`, `W_actual`
- `SimpleTransformer` — transformer mínimo backprop puro para next-token / sentido
- `RootMemory` — memoria competitiva con vitalidad y Hebb local (foco + olvido)
- `LinearSenseClassifier` — clasificador lineal sobre embeddings skip-gram
- `SkipGram` — skip-gram puro, sin numpy, entrenable en corpus chico/mediano
- `build_polysemy_corpus()` — genera corpus sintético A/B con ground truth; acepta
  `n_per_sense`, `augmentation`, variación sistemática y palabras multi-sentido

Reglas duras:
- TODOS los experimentos nuevos deben importar desde `dscng_core.py`; no duplicar
  `dot/cos/norm/softmax/train_transformer/root_refuerza` en cada script.
- Antes de background: `py_compile`, smoke test import+llamada, grep de `def`+`return`.
- Resultados van a `results_<vx>.json` con métricas canónicas; el README se coteja
  contra esos JSON, no contra memoria.

Quedan por migrar: v3-v8, v10-v12 (revalidados pero aún inline). REGLA (2026-07-31):
no migrar experimentos viejos a menos que vayan a re-ejecutarse como baseline activo.
Migrar SOLO los componentes que alimentan el pipeline de coherencia: v13 (bigramas
por sentido) y v22 (coherencia de dominio). El resto queda documentado como
"revalidado sobre core (results_*_core.json) pero no migrado" — su comportamiento
ya está en results_*.json y references/.

PARADIGMA COHERENCIA > SEPARACIÓN A/B (2026-07-31). La métrica correcta no es
acc_gt sobre clasificación A/B interna, sino coherencia de generación externa
por dominio. v22: FUNCIONAL sobre sintético (score 0.895-0.915). v22b: NO
FUNCIONAL sobre Don Quijote (score=0.0). La tesis de Luciano ("no necesita saber
que banco tiene dos sentidos; necesita comportarse coherente") se valida sobre
sintético controlado. Próximo: embeddings reales + coherencia sobre corpus real.