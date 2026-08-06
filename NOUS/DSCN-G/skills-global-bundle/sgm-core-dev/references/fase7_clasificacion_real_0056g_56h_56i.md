# Clasificación real sobre corpus (exp_SGM_0056g / 0056h / 0056i)

Línea de experimentos que lleva el sustrato HD (role-filler, 0056e) a CLASIFICACIÓN REAL sobre
corpus real (Don Quijote, Gutenberg pg2000 = ESPAÑOL; pg996 = INGLÉS). Responde la pregunta de toda
la fase 7: ¿el sustrato SGM clasifica sobre texto real? La respuesta matizada es: DEPENDE de si la
etiqueta vive en el CONTEXTO o en la PALABRA.

## Receta de descarga de corpus real (Android, sin nltk/spacy)
- `web_search` NO disponible. Descargar vía `urllib.request` a Gutenberg.
- **`.read()` entero FALLA con `IncompleteRead` en ~2.2 MB** → leer en chunks:
  ```python
  resp = urllib.request.urlopen(req, timeout=60, context=ctx)
  chunks = []; total = 0
  while True:
      b = resp.read(65536)
      if not b: break
      chunks.append(b); total += len(b)
  data = b"".join(chunks).decode("utf-8","ignore")
  ```
- Tokenizar manual con stdlib: `re.findall(r"[a-záéíóúñü]+", text.lower())`.
- Quitar marcadores Gutenberg (`*** START/END ***`) y dividir en oraciones por `[.!?]+`.
- Corpus queda en `/data/user/0/com.hermesagent.android/files/home/donquijote_es.txt` (local, NO pushear;
  agregar `lit/corpus/` a `.gitignore`).

## Taxonomía de tareas (clave del hallazgo)
Al armar clasificación sobre texto real, elegir la etiqueta según DÓNDE vive la señal:
- **LÉXICA**: la etiqueta está en la PALABRA misma (ej. "¿es nombre propio?" por mayúscula). Al
  enmascarar la palabra, el CONTEXTO no lleva señal → el decoder no supera el baseline (0056g).
- **DISTRIBUCIONAL (por presencia)**: la etiqueta vive en marcadores del contexto (ej. "¿género del
  sustantivo?" por el determinante el/la que lo precede). El contexto SÍ lleva señal → ambos > baseline,
  la plana suele ganar porque basta con presencia del marcador (0056h).
- **POSICIONAL PURA (orden)**: la etiqueta es la POSICIÓN (ej. "¿es la 1ª palabra de contenido?").
  El BoW plano NO puede saber qué hueco dejó la palabra ausente; el role-filler SÍ ve el hueco. El rol
  capta el orden (f1 > plana) pero un decoder lineal binario sobre contexto mezclado no alcanza para
  vencer el baseline (0056i). Requiere decodificación por rol explícita (unbind por posición).

## Resultados (ejecutados de verdad, Don Quijote es)
| Exp | Tarea | Etiqueta | baseline | role-filler | plana BoW | Veredicto |
|-----|-------|----------|----------|-------------|-----------|-----------|
| 0056g | propio vs común | LÉXICA (mayúscula) | 0.891 | 0.840 / f1 0.168 | 0.890 / f1 0.343 | NO > baseline (ctx no lleva señal) |
| 0056h | género masc/fem | DISTRIBUCIONAL (el/la) | 0.553 | 0.673 / f1 0.718 | 0.804 / f1 0.836 | SÍ > baseline; plana gana (presencia basta) |
| 0056i | 1ª palabra contenido | POSICIONAL (orden) | 0.716 | 0.627 / f1 0.202 | 0.679 / f1 0.127 | rol f1>plana (capta orden) pero decoder lineal no alcanza |

## Arquitectura del clasificador (reutilizable)
- `BinDecoder`: regresión logística binaria sobre contexto HD, SGD manual stdlib (sin numpy).
  `W` libre, `lr=0.3`, épocas 15, sigmoid con clamp a ±30 (evita `math overflow`).
- Contexto = oración SIN el objetivo: role-filler resta el `bind(rol, wordvec)` del objetivo; plana
  resta `wordvec` del objetivo. Normalizar contexto a norma 1 para que `W·x` no explote.
- Muestreo: cap de muestras (8000), balancear positivos/negativos, 70/30 split.
- Métrica honesta: accuracy AND f1 (la plana puede "ganar" accuracy solo por colapsar a la clase
  mayoritaria; el f1 revela si detecta la clase positiva — en 0056i el rol tiene f1 superior).

## Lecciones para futuros experimentos de clasificación
1. Elegir la etiqueta según la taxonomía arriba. Si es léxica, NO esperes que el contexto la resuelva
   (0056g). Si es distribucional/posicional, el HD SÍ aprende (0056h/56i).
2. El role-filler ayuda SOLO cuando el ORDEN es la variable discriminativa (0056i). Para presencia de
   marcador (género), la plana basta. Esto CONECTA con 0056e (role-filler rompe el techo de composición
   sistemática) y 0056f (role-filler no mejora recall temático): el rol importa donde la ESTRUCTURA
   (orden/rol) es el canal, no cuando basta el contenido léxico.
3. Para vencer el baseline en tarea puramente posicional con rol, usar decodificación por rol explícita
   (unbind por posición y ver cuál hueco falta), no un clasificador lineal sobre el contexto sumado.
4. No confundir "memoria" con "comprensión": 0056f top-1 cosine = 1.0 (recuerda la oración) pero eso
   no es clasificación ni razonamiento.
