# v0.25 v13b — Modelo de transición explícita (bigramas + repetición guard)
Hallazgo: en corpus chico con templates fijos (~350 frases × 2 sentidos), un
modelo de transición explícito de orden 1 captura suficiente estructura para
generar texto coherente desde prompts reales.

Métrica clave obtenida:
- top1=0.630, top5=0.940 (n=200)
- Generaciones legibles desde prompts como “fue al banco”, “el banco aprobo”,
  “se tiro al banco”, con saltos entre sentidos coherentes dirigidos por la
  distribución aprendida.

Condiciones para replicar:
- Corpus: templates fijos con ground truth explícito por sentido.
- Vocab reducido (~70 tokens).
- predictor greedy con muestreo softmax sobre top_k=10, temperatura~0.4,
  no_repeat=3 para evitar loops.
- baseline recomendado: medir clasificador fuerte antes de afirmar loop útil.

Contraste directo con v12 (decoder por similitud de embeddings):
- top1=0.020, top5=0.095, generaciones sin coherencia en mismo corpus.
- LECCIÓN: en este régimen, la transición explícita supera a nearest-neighbor
  sobre embeddings locales.

Referencia en documentación: _README_ENGINE.md sección v13/v13b.
