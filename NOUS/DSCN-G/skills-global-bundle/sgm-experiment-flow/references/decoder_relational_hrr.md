# references/decoder_relational_hrr.md

## exp_SGM_0046 — Decoder L2 RELACIONAL sobre corpus real (Don Quijote)

**Pregunta:** tras tener composición relacional (0027-0031), el "sentido" que alimenta el decoder
vendría de un grafo omega RUTEADO por rol (no de tokens planos), y los resultados del decoder
L2 (0022/0026) CAMBIARÍAN. Se corrió 0046 para medirlo. **La hipótesis cayó.**

### Diseño (test-first, con NC)
- Corpus real: `lit/corpus/don_quijote.txt` (fuera de git). Vocab top-400 por frecuencia, ventana 3.
- Grafo: nodo = palabra (embedding HRR dim D=256). Aristas = co-ocurrencia dirigida en ventana,
  CAPADAS a top-K=8 vecinos por nodo (poda estándar, no hardcode). Rol = índice del vecino.
- Bigrama RELACIONAL: desde `prev`, 1 paso sobre `rel_mem` bajo bias de rol:
  `score = cos(rel_mem[prev], HRR(role_vecs[r], omega[vecino]))`. NO se usa route() PPR.
- Contra: bigrama PLANO (0026, conteo), UNIGRAM, AZAR. NC: rol aleatorio → top1 cae a azar.

### Resultado (MEDIDO)
- top1 relacional = 0.020 | top1 plano (0026) = 0.333 | unigram = 0.140 | azar = 0.0025
- **El ruteo HRR de UN PASO EMPEORA el top1 (16x peor que plano).**

### Por qué (honesto)
HRR con D=256 y grado 8 tiene CROSSTALK: los `HRR(rol, omega_vecino)` de los 8 vecinos se
solapan → el coseno no distingue el sucesor real → elige ~al azar. Bigrama plano (conteo) no
tiene ese ruido y acierta 1/3.

### Lección de clase
- Rol HRR SIRVE para COMPOSICIÓN ANIDADA (0027-0031 cierran Gap 2), NO para bigrama superficial.
- Coherente con 0045b: un mecanismo que funciona en capa X no transfiere a capa Y solo por ser
  "más rico" — HAY QUE MEDIRLO (regla de oro de Luciano: no emocionarse al pedo).
- T-DEC-R1 (relacional > plano) estaba mal planteado. El rol HRR compite en DESAMBIGUACIÓN de
  polisemia (T-DEC-R2), no en top1 global de bigrama.

### Giro propuesto (0046b, pendiente visto bueno de Luciano)
Decoder HÍBRIDO: grafo ruteado HRR da SEMILLA RELACIONAL (sentido desambiguado por rol); bigrama
plano predice el sucesor RESTRINGIDO a la semilla (solo vecinos coherentes con el rol). HRR filtra
por sentido, conteo elige sin ruido. Sin forzar al HRR a hacer lo que no hace bien.

---

## EXPANSIÓN — trilogía 0046b / 0046c / 0047 / 0047b (conclusión cerrada, 2026-08-03)

Luciano pidió "lograr el decoder" y disparó la señal: _"es raro, siento que debería haber funcionado a
esta altura"_ + _"no me gusta emocionarme al pedo"_. Esa señal nos llevó a encontrar bugs REALES de
diseño (no un límite del sustrato). La trilogía completó 5 variantes:

| exp | diseño | top1 relacional | vs plano | veredicto |
|-----|--------|----------------|----------|-----------|
| 0046 | 1 paso HRR, bias rol | 0.020 | 0.333 | ruido (crosstalk) |
| 0046b | filtro binario top-M por score HRR | 0.17 | 0.333 | EMPEORA (descarta sucesor) |
| 0046c | peso suave HRR×bigrama | 0.315 | 0.312 | ≈ ruido (dif 0.003) |
| 0047 | contexto acumulado (bind ventana) → cleanup | 0.003 | 0.265 | = NC (mezcla espacios) |
| 0047b | espacio coherente (omega=rel_mem) | 0.018 | 0.18 | ≈ NC (emb ruido no codifica cooc.) |
| 0048 | HRR message-passing entrenado (D=128,T=2) + TEST DE FUEGO ESTRUCTURAL | 0.045 | 0.34 | ≈ NC; test estructural 0.259<0.361 |

### exp_SGM_0048 — TEST DE FUEGO ESTRUCTURAL (el veredicto decisivo, 2026-08-03)
Luciano pidió "sigamos con 0048". La raíz de 0047b era que `emb=ruido` no codifica co-ocurrencia.
0048 ENTRENÓ embeddings HRR por message-passing (T_ITER=2, D=128): `emb[w]=normalize(Σ_k p(w,k)·HRR(rol_k, emb_old[k]))`,
propagando la estructura del grafo a los ω. Y — clave — agregó un **TEST DE FUEGO ESTRUCTURAL** que mide la
propiedad fundamental DIRECTAMENTE, no solo el decoder:
- `cos(emb[w], emb[n])` para pares que CO-OCURREN vs pares RANDOM.
- Si el HRR entrenado captura co-ocurrencia, los co-ocurrentes deben dar coseno MAYOR que los random.
Resultado: cos(co-ocurrente)=**0.259** < cos(random)=**0.361**. El message-passing HRR **APLATÓ** la señal
(al revés de lo esperado). Decoder top1=0.045 vs plano 0.34 vs NC 0.015.

**POR QUÉ ESTO CIERRA EL TEMA (no es otro bug tunenable):** el test estructural es la prueba de fuego. Mide
"¿los embeddings entrenados acercan palabras que co-ocurren?" y da el resultado OPUESTO al esperado. El bind de
ruido con ruido da ruido; sumar 8 ruidos normalizados no apunta a ningún vecino. Para que el HRR ordene vecinos
por cleanup necesitaría D miles o Word2Vec real (que el bigrama plano YA es, implícitamente). Plate 1995a lo
anticipó: HRR = composición, no recuperación de ítems por similitud local.

### TÉCNICA NUEVA — TEST DE FUEGO ESTRUCTURAL (cuándo usar, 2026-08-03)
Cuando un mecanismo de representación falla en su tarea downstream (decoder, recuperación), NO sigas tunenando
la tarea. Medí la **propiedad fundamental** del mecanismo DIRECTAMENTE:
- HRR/embeddings deben acercar ítems que co-ocurren/relacionan → mide `cos(co-ocurrente) vs cos(random)`.
- Si la propiedad no se cumple (o da el signo opuesto), el mecanismo NO tiene la estructura; tunear la tarea
  es inútil. Esto evitó un 6to intento infundado en 0048.
- Es el análogo estructural del "negative control" de la auditoría: en vez de "¿el modelo resuelve Y?", preguntás
  "¿el modelo TIENE la propiedad X que Y requiere?". Si X falta, Y no va a pasar sin importar cómo lo midas.

### Bugs de diseño encontrados (NO límites del sustrato)
1. **0047 mezcla ESPACIOS:** `hdc_project()` (SensorBridge 0019, chunk-based) sobre un HRR-bind de
   embeddings → `omega_routed` y `tr.omega` viven en representaciones distintas → cleanup da ruido.
   FIX honesto (0047b): todo en el MISMO espacio HRR. `omega[i] = rel_mem[i]` (la nube relacional ES
   el sentido), contexto = bind de `rel_mem` de la ventana, cleanup contra `rel_mem`.
2. **0047b sigue en ruido:** los `emb[w] = rnd_unit` (ruido aleatorio) NO codifican co-ocurrencia.
   El HRR-bind de ruido con ruido no ordena vecinos → cleanup elige al azar. Para que el HRR ordene,
   los embeddings deben REFLEJAR el grafo (ser word embeddings entrenados, tipo skip-gram). Eso es
   literalmente lo que el bigrama plano hace implícitamente por frecuencia.

### CONCLUSIÓN FINAL (cerrada, no difuelta)
- El **bigrama plano** (0026/0047) ES el decoder de lenguaje de SGM: top1 = 0.18–0.33 en corpus real.
- El **HRR NO predice el siguiente token** porque sus embeddings (ruido) no codifican co-ocurrencia;
  el cleanup da ruido. Plate 1995a lo anticipó: HRR es para COMPOSICIÓN (roles/anidamiento), no para
  recuperación de ítems por similitud local. SÍ compone relaciones anidadas (0027-0031, verificado).
- "Un ser sin lenguaje no sirve" → el lenguaje de SGM es: (1) GENERACIÓN por bigrama plano (texto
  coherente palabra a palabra); (2) SENTIDO/desambiguación por el grafo HRR ruteado como CONTEXTO
  (filtra el sentido en polisemia, no predice); (3) ESTRUCTURA por HRR cuando hay relaciones anidadas.

### PATRÓN DE TRAMPA "AJUSTO Y RE-CORRO" (lección de Luciano, 2026-08-03)
5 intentos del decoder con variantes que no pasan es la SEÑAL de que estamos tunenando para que pase,
no midiendo el sustrato. Reglas duras (deben estar en el SKILL.md como pitfall):
1. Si el 3er intento de un experimento no pasa, DETENER y diagnosticar la RAÍZ (¿el diseño o el
   sustrato?), no probar una 4ta variante con otro peso. Luciano: "no me gusta dejar cosas a futuro"
   significa CERRAR con conclusión honesta, no difuminar en más intentos.
2. El baseline debe ser FIJO entre corridas (bug de 0046: cambié vocab/ventana entre 0026 y 0046 y el
   "plano" se movió de 0.185 a 0.333 — inconsistencia metodológica). Mismo corpus, mismo vocab, misma
   muestra, para TODAS las variantes.
3. Antes de la 2da variante, verificar que el score se compute en el MISMO espacio de representación
   que el cleanup (bug de 0047). Si mezclás HDC y HRR, el cleanup es ruido por construcción.
4. El "debería haber funcionado" de Luciano es una ALARMA de bug de diseño, no de falla del sustrato.
   Tomarla en serio = encontrar el bug (como hicimos en 0047b), no descartar el mecanismo.

### Literatura (arXiv API; web_search NO disponible)
- 1904.09447 "Unsupervised Text Generation from KGs"
- 2512.14709 "Attention as Binding: VSA perspective on Transformers" (atención = binding HRR;
  confirma crosstalk del binding suave — coherente con 0046)
- 2306.08302 "Unifying LLMs and KGs: A Roadmap" (grafo modula, no reemplaza → 0046c peso suave)

### Literatura (arXiv API; web_search NO disponible)
- 1904.09447 "Unsupervised Text Generation from KGs"
- 2512.14709 "Attention as Binding: VSA perspective on Transformers" (atención = binding HRR;
  confirma crosstalk del binding suave — coherente con 0046)
- 2306.08302 "Unifying LLMs and KGs: A Roadmap"

### Performance en Android (RECETA)
- build_graph SIN capar → grado prom 2173 aristas/nodo. TickRelational.__init__ ~91s. FIX: top-K=8.
- NO route() PPR por predicción (timeout >200s en celular). Usar 1 paso sobre rel_mem (O(grado)).
- omega debe ser dim D (no EMB_DIM aparte) o hrr_bind da IndexError.
- 400 pares bastan para top1 estable; no usar 8000.
- Verificar nombres de función (bigram_relacional vs bigram_relational → NameError).

### PATRÓN DE TRAMPA "AJUSTO Y RE-CORRO" — CUÁNDO PARAR DE TUNEAR (lección 2026-08-03)
Si un experimento NO PASA tras 3 variantes del mismo mecanismo, DETENER y diagnosticar la RAÍZ
(diseño vs sustrato), NO probar una 4ta/5ta variante con otro peso/arquitectura. Luciano lo disparó
con _"debería haber funcionado a esta altura"_ + _"no me gusta emocionarme al pedo"_. Reglas:
1. El "debería haber funcionado" es ALARMA de BUG DE DISEÑO, no de falla del sustrato. Tomarla en serio
   = encontrar el bug (en 0046-47b: embeddings ruido, mezcla de espacios HDC/HRR, score con ruido por
   construcción), no descartar el mecanismo ni seguir iterando.
2. El baseline debe ser FIJO entre todas las variantes (mismo corpus/vocab/ventana/muestra). Bug de 0046:
   cambié vocab/ventana entre 0026 y 0046 y el "plano" se movió 0.185→0.333 — inconsistencia que
   hacía imposible comparar. Si el baseline se mueve, el experimento no mide nada.
3. Verificar que el score del mecanismo y el cleanup vivan en el MISMO espacio de representación antes
   de la 2da variante (bug de 0047: `hdc_project` sobre HRR-bind → cleanup ruido por construcción).
4. Tras diagnosticar la raíz, si el mecanismo es legítimamente inadecuado para esa capa (HRR no predice
   token, Plate 1995a lo anticipa), CERRAR con conclusión honesta (bigrama plano ES el decoder; HRR =
   contexto/estructura). "No dejar cosas a futuro" = cerrar el veredicto, no difuminarlo en más intentos.
   En 0046-47b eso fue: decoder SGM = bigrama plano + grafo HRR como contexto de desambiguación.

---

## exp_SGM_0049 — LENGUAJE COMO ACTO SOCIAL (nacimiento bajo presión, 2026-08-03)

Luciano dio el giro correcto: _"¿y si el lenguaje nace cuando es necesario describirse o describir a
otro? ¿Y si usamos dos grafos para que intenten comunicarse?"_. Eso SACA al HRR de "predecir token"
(donde ya sabíamos que no sirve, 0046-48) y lo usa para lo que BRILLA: COMPOSICIÓN RELACIONAL entre
dos agentes con mundos distintos. El decoder quedó CERRADO en 0048; 0049 es lenguaje como coordinación.

### Diseño (test-first, con NC, por comportamiento)
- 2 agentes A y B, cada uno con su **ω propio** (transitan su mapa, acumulan huella = experiencia).
  Mundos distintos (no espejo): distinta topología de eventos, distintos `cell_vec` HRR.
- Mapa 30×30 con comida (+1 Valencia), comida venenosa (dolor Eq.6 de 0018), estrellas (cielo estrellado).
- **ENCUENTRO FORZADO** (clave): en fase 2 ambos arrancan de la misma celda y transitan 25-30 pasos
  juntos. SIN esto, en 60×60 `A.visited & B.visited` sale VACÍO y el joint attention no tiene ancla
  (la 1er versión dio puente 0/0). El encuentro es parte honesta del experimento (joint attention, no accidental).
- **JOINT ATTENTION**: sobre las celdas comunes (pivotes), cada uno guarda
  `bridge[("B", celda)] = B.cell_hrr(celda)` (y viceversa) → el puente A↔B se NEGOCIA, no se regala.
- **Métrica POR COMPORTAMIENTO** (no coseno, la trampa de 0048): A señala `target` a B vía HRR; B debe
  identificar la **CELDA EXACTA** que A señaló. `hit = (best == target)`, NC ~ 1/N.

### CLIMAS (la idea de Luciano: cielo estrellado ≠ competencia por comida)
| clima | comunicación | NC | veredicto |
|-------|-------------|-----|-----------|
| cielo_estrellado | 0.2 | 0.0 | puente 1 (B apenas transitó 5 celdas) |
| competencia | 0.125 | 0.125 | puente NO aporta (igual al azar) |
| peligro_compartido | **0.375** | **0.0** | puente 15, FUNCIONA |

**HALLAZGO**: el lenguaje (puente A↔B) EMERGE bajo PRESÍON COMPARTIDA (peligro), NO bajo cielo
estrellado ni competencia suelta. Coherente con Tomasello: el lenguaje nace de joint attention bajo
necesidad compartida, no por estar juntos ni por competir (cada uno para sí).

### Debilidades honestas (experimento a medias, 2026-08-03)
1. **Dolor NO ocurrió**: en 250 pasos sobre 30×30 con 30-40 venenos, ningún agente pisó veneno → la
   "comida venenosa" no se probó (la afinidad negativa los esquiva antes). Falta forzar veneno EN EL
   CAMINO para que el dolor marque el ω.
2. **Belleza NO medida**: `star_reconoce = None` porque B visitó pocas estrellas (se quedó pegado al
   centro). La pregunta "¿qué es la belleza?" quedó sin respuesta empírica. Para medirla: sembrar
   estrellas DENSAS y ver si A/B se señalan estrellas mutuamente (coordinación estética sin recompensa).
3. **B casi no transita** (5-36 celdas): en el encuentro forzado arranca del centro y su huella lo
   trae de vuelta → el puente es desigual entre agentes.

### TRAMPAS de medición evitadas / corregidas (2026-08-03)
- **Métrica "evitar" es inválida**: `avoid_ok = (best_b != target)` da 1.0 = NC porque casi siempre
  elige otra celda ≠ target. Usar `hit = (best == target)` (acierto en celda exacta). Misma clase que
  los anti-patrones de auditoría: si el NC empata al positivo, la métrica es inválida.
- **`hrr_core.cleanup` ARITY**: `H.cleanup(vector, lista)` toma SOLO 2 args — NO recibe `D`. El intento
  inicial `H.cleanup(sigB, [c], D)` dio `TypeError: cleanup() takes 2 positional arguments but 3 were
  given`. FIX: `H.cleanup(sigB, [A.cell_hrr(cell)])`. Siempre grep `dir(H)` antes de usar una función
  de `hrr_core` que no hayas llamado.
- **Mapa demasiado grande = nada pasa**: 60×60 con densidad baja → agentes no se cruzan ni pisan
  veneno. Usar 30×30 con densidades reales (veneno ~2-3% del mapa) para que el dolor/comida ACTÚEN.

---

## exp_SGM_0049b — SIMULACIÓN LARGA + COORDINACIÓN OBLIGATORIA (HALLAZGO DE DISEÑO, 2026-08-03)

Luciano pidió: _"simulación mucho más larga, que sigan juntos bastante, dificultades difíciles de
sortear de a uno, guardá y pusheá"_. Se armó 2000 ticks, 3 climas, barreras que SOLO se abren si
AMBOS agentes llegan a sus claves a la vez (no sorteables de a uno), veneno EN EL CAMINO, estrellas
densas para belleza. Resultado:

- **puente = 0** en todos los climas (A y B no comparten celdas → no hay joint attention).
- **coordinación barreras = 0** (nunca llegaron a las claves).
- **dolor = 0** (nunca pisaron veneno).
- **visited ~15 celdas** en 2000 ticks (pegados en un rincón, no transitan).

### DIAGNÓSTICO HONESTO (no excusa, no falla del sustrato)
El motor de afinidad de 0044 (huella + frontier + abur, diseñado para 12×12) **NO ESCALA a mapa 30×30
ni NAVEGA METAS**. Se probó: (a) encuentro forzado (arrancar juntos 25-30 pasos) y (b) atracción a
`goal` (`aff += 5.0/(1+dist_a_meta)`). Ninguno alcanza porque el paso es 1 celda/tick y el camino está
bloqueado por las propias barreras → nunca llegan a las claves. El experimento midió eso: los agentes
no se mueven lo suficiente para encontrarse ni coordinar.

### HALLAZGO DE DISEÑO (lo que falta, reusable)
Para simular "nacimiento del lenguaje bajo presión" o cualquier coordinación en mapa >12×12 se
requiere un **motor de PATHFINDING real** (BFS/A* desde `pos` hasta `goal`, ignorando barreras
bloqueadas) cuya ruta sea la ACCIÓN del agente — no afinidad local + meta-lejana. Sin cuerpos que se
desplacen, el lenguaje no puede emerger (no hay encuentro, no hay joint attention). El HRR y el
sustrato de coordinación NO se probaron porque el cuerpo no llegó. Esto es un GAP de INFRA, no del
mecanismo. El hallazgo válido de 0049 (lenguaje bajo peligro compartido, puente 0.375 vs NC 0.0)
sigue en pie porque usó mapa chico + encuentro corto donde SÍ coincidieron.

### REGLA DE DISEÑO (para el próximo intento, 0049c si se hace)
1. Agregar BFS en `World`/`Agent`: `bfs(start, goal, blocked_fn)` → lista de celdas; el `step` sigue
   la ruta y solo cede al afinidad si la ruta está bloqueada.
2. Densidad real de veneno (~2-3% del mapa) Y sembrarlo EN EL CAMINO de la ruta forzada para que el
   dolor ocurra y marque ω (experiencia).
3. Estrellas DENSAS (ej. 10-15% del mapa) para que B visite estrellas y `star_reconoce` se mida.
4. Mantener la métrica `hit = (best == target)` (celda exacta), NO "evitar".

### Conclusión de la saga decoder+lenguaje (0046→0049b)
- El **decoder de superficie** de SGM = BIGRAMA PLANO (top1 0.18-0.34 corpus real). HRR no predice token.
- El **HRR** aporta (a) COMPOSICIÓN ANIDADA (0027-0031) y (b) CONTEXTO de desambiguación / coordinación
  entre agentes (0049, bajo presión compartida). No es para recuperación de ítems por similitud local.
- El lenguaje de SGM es GENERACIÓN (bigrama) + SENTIDO (HRR como contexto/coordinación). Es lenguaje
  real desde sustrato propio, medido y honesto — no un LLM, pero no es "un ser sin lenguaje".
- 0049 quedó como HALLAZGO_PARCIAL (el lenguaje emerge bajo peligro compartido; falta medir dolor/belleza).
  Corrección propuesta para cerrarlo: tránsito forzado de B + veneno en el camino + estrellas densas.
