# Clasificación REAL sobre corpus (SGM Fase 7) — 056g/056h

Receta reutilizable para usar el sustrato HD + decoder entrenado como clasificador sobre texto real.
HALLAZGO METODOLÓGICO DURADERO: si un clasificador por-contexto da baseline, el problema suele ser el
ENCUADRE de la tarea (etiqueta léxica vs distribucional), NO el sustrato. Reformular la tarea, no declarar roto.

## Receta base (stdlib puro, sin nltk/spacy — no están en el celular)
- Corpus: Don Quijote español = **Gutenberg pg2000** (pg996 es INGLÉS). Bajar con urllib en CHUNKS de 65536
  (`.read()` entero da `IncompleteRead` en ~2.2 MB).
- Tokenizar: `re.findall(r"[a-záéíóúñü]+", text.lower())`.
- V~1500, N~256 HD bipolar. Contexto del objetivo = traza HD MENOS el binding del token objetivo (enmascarado).
- `BinDecoder`: regresión logística binaria, `sigmoid` con clip a ±30 (evita OverflowError en logits grandes),
  contexto NORMALIZADO a norma 1 antes de fit/pred (estabiliza W·x). sgd ~15 épocas.
- Baseline = clase mayoritaria. Reportar SIEMPRE acc + f1 (f1 revela si detecta la clase minoritaria).

## 056g — etiqueta LÉXICA (propio vs común por contexto enmascarado) → FALLA
- baseline 0.891; role-filler 0.840/f1 0.168; plana 0.890/f1 0.343.
- Por qué: "nombre propio" es propiedad de la PALABRA, no del contexto. Al enmascarar la palabra, el contexto
  no lleva la señal → no hay nada que clasificar. El role-filler empeora (el orden no correlaciona con "propio").

## 056h — etiqueta DISTRIBUCIONAL (género del sustantivo por el determinante precedente) → FUNCIONA
- gold = género del DET (el/la). baseline 0.553 (masc/fem ~50/50); role-filler 0.673/f1 0.718; plana 0.804/f1 0.836.
- El sustrato SÍ clasifica cuando la señal vive en el contexto. La PLANA le gana al role-filler porque el género
  es detectable por PRESENCIA del determinante (lexical en el contexto), no por POSICIÓN → BoW basta.

## Lección para próximos clasificadores en corpus real
- Elegir etiqueta DISTRIBUCIONAL (sintaxis, función, género, caso) antes que léxica (propio/común, sentido).
- Si el baseline no se rompe → diagnosticar ENCUADRE (¿la señal está en el contexto o en la palabra?) antes
  de tocar el sustrato. Evitó malgastar tiempo "afinando el decoder" en 056g.
- Conecta con 0056e (HD role-filler rompe techo de composición) y 0056f (memoria por contenido: top-1=1.0,
  role-filler no mejora recall temático porque el orden no discrimina tema). El rol ayuda cuando el ORDEN es
  la variable discriminativa, no cuando basta con presencia.
