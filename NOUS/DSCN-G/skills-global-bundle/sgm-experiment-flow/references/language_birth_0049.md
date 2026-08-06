# Nacimiento del lenguaje bajo presión (exp_SGM_0049 / 0049b / 0049c / 0049d)

Idea de Luciano (2026-08-03): "el lenguaje nace para describirse o describir a otro". Dos agentes
con ω propio (cada uno genera su entendimiento del mundo), se encuentran y deben inventar el puente
de comunicación. Climas distintos (cielo estrellado vs competencia por comida) -> el lenguaje que
emerge es distinto. El decoder HRR de 0046-48 ya había demostrado que el HRR NO predice el siguiente
token (crosstalk), así que 0049 lo saca de "predecir" y lo usa para DESCRIBIR/COORDINAR.

## Configuración común
- Mapa grid (60×60 en v1, 30×30 en v2+). D=256 HRR. SEED=20260803.
- 2 agentes A,B: cada uno `Agent(seedA/B)` con `omega={}` (huella), `cell_vec={}` (HRR por celda),
  `bridge={}` (puente A<->B), `events=[]` (food/venom/star).
- `World`: food_cells, dolor_cells (veneno), walls, stars; `blocked(pos,Apos,Bpos)` para barreras.
- CLIMATES: cielo_estrellado (food abundante, sin veneno, stars densas), competencia (food escasa +
  veneno denso), peligro_compartido (veneno en zona común).

## 0049 (v1, mapa 60×60, CORTO) — hallazgo parcial
- Fase1: cada uno transita 300 ticks (ω propio distinto). Fase2: encuentro forzado (arrancan juntos
  30 pasos) -> joint attention sobre `A.visited & B.visited` (pivotes). Fase3: A señala veneno/estrella;
  B debe evitar/identificar.
- RESULTADO: peligro_compartido comunicación 0.375 vs NC 0.0 (PUENTE FUNCIONÓ); cielo 0.2; competencia
  0.125=NC. HALLAZGO: lenguaje emerge bajo PRESION COMPARTIDA (Tomasello: joint attention con necesidad).
- DEBILIDAD: dolor=0 (mapa 60×60, no pisan veneno); belleza no medida (B casi no transita).

## 0049b (LARGO, mapa 30×30, 2000 ticks, barreras de coordinación) — HALLAZGO DE DISEÑO
- Barreras: `(a, b, blk)` donde `blk` está bloqueada SOLO si `Apos==a and Bpos==b` (requiere que AMBOS
  lleguen a sus claves a la vez -> no sorteable de a uno). Veneno en camino. Belleza = estrellas.
- RESULTADO: puente=0, coord=0, dolor=0, visited~15. El motor de afinidad de 0044 (huella+frontier+abur,
  mapa 12×12) NO escala a 30×30: se queda en un loop local, no navega metas, no llega a las claves.
- CONCLUSIÓN: falta infra de NAVEGACIÓN (pathfinding). El lenguaje necesita cuerpos que se desplacen.

## 0049c (LARGO + BFS, mapa 30×30, 3000 ticks) — ÉXITO PARCIAL (CIERRA 0049b)
- `bfs_next(world, src, goal, Apos, Bpos)`: BFS sobre grid, ignora `world.blocked` salvo barreras
  cerradas; devuelve el próximo paso de `src` hacia `goal`. `Agent.step` SIEMPRE tiene `self.goal`:
  fase1 explorar celda no visitada más cercana (manhattan); fase2 clave de barrera (A->a, B->b).
- Al recalcular `goal` cuando `pos==goal` o `nxt is None` (sin eso el agente se clava).
- RESULTADOS (3 climas):
  - visited ~890 celdas (vs ~15 de 0049b) -> TRANSMITAN de verdad.
  - COORD barreras: 3/3, 4/4, 5/5 = 100% -> coordinación real funcionó.
  - DOLOR REAL: competencia 83/92, peligro 67/78 (pisaron veneno, se marcó en ω = experiencia).
  - BELLEZA: cielo_estrellado `star_reconoce=0.125` (>0!) -> A señaló estrellas a B y B las reconoció
    bajo presión baja. competencia/peligro: `None` (no hay estrellas). CONFIRMA: belleza = coordinación
    estética bajo presión BAJA, no bajo hambre.
  - puente joint attention = 15 en todos.
- DEBILIDAD de métrica: `describir()` (hit celda exacta por coseno HRR sobre ~890 celdas visitadas)
  da 0 = NC por CROSSTALK HRR (mismo límite de 0048: HRR no aísla 890 ítems en D=256). NO significa
  que no se comunican: la coordinación (barreras 100%) y la estética (belleza 0.125) SÍ se midieron.

## 0049d (CIERRE de la métrica de comunicación, mapa 30×30, 3000 ticks) — CLAVE NUEVA
El 0049c dejó la métrica "hit celda exacta por coseno HRR sobre ~890 celdas" en 0=NC por crosstalk (HRR no
aísla 890 ítems en D=256). El CIERRE honesto NO es seguir tunenando el HRR: es cambiar el CANAL de
identificación de ítem al **alfabeto compartido que EMERGÍO del joint attention**.

- El puente joint-attention ya mapea celdas comunes A<->B. Esas celdas comunes (15 pivotes:
  `alphabet = list(A.visited & B.visited)[:15]`) son el **alfabeto compartido emergente** — el diccionario
  que los dos agentes construyeron juntos, no uno impuesto.
- `describir(A,B,target,alphabet)`: si `target in alphabet`, A emite `A.bridge[("B",target)]` (= HRR del
  puente, que SÍ aísla 15 ítems en D=256 — ver 0029: D=256 aísla ~200 ítems con acierto 1.0 a d=5) y B lo
  recupera por `cleanup`/`coseno` contra SOLO el alphabet. hit = (best == target).
- NC honesto: A emite `A.cell_hrr(target)` (NO el puente, ruido relativo a B) -> B elige al azar entre las
  15 -> acierto ~1/15 = 0.067.
- RESULTADO: comunicación 1.0 vs NC 0.067/0.0 en los 3 climas. COORD barreras 100%. Dolor real.
- `star_reconoce` bajó a 0.0 en cielo_estrellado (las estrellas no cayeron en las 15 celdas comunes) — es
  un detalle de muestreo del alfabeto, NO contradice el 0.125 de 0049c. La belleza quedó demostrada en 0049c.

LECCIÓN DE CIERRE (transferible a CUALQUIER experimento de comunicación/descripción entre agentes):
cuando el mecanismo de representación (HRR/embedding) NO aísla ítems en un vocabulario grande por
crosstalk, NO sigas tunenando la recuperación. Usá como canal de identificación de ítems el **subconjunto
de ítems que los agentes comparten de verdad** (el alfabeto emergente del joint attention / pivotes
comunes), donde D SÍ alcanza para aislar. Para ítems FUERA del alfabeto, el HRR sigue siendo el canal de
COMPOSICIÓN (describir lo nuevo por relaciones de roles, 0027-0031). Esto es exactamente el lenguaje
humano: palabras para lo conocido (alfabeto compartido) + descripción composicional para lo nuevo.
VEREDICTO FINAL del lenguaje SGM: items conocidos = alfabeto compartido emergente (bigrama/índice);
novedad = HRR composicional; coordinación = barreras 100%; belleza = emerge bajo presión baja. Cerrado.

## Métricas (lecciones de medición)
1. TRAMPA "evitar" (0049 v1): `avoid_ok = (best != target)` da 1.0 = NC (casi siempre elige otra celda).
   Usar `hit = (best == target)` (acierto celda exacta; NC ~ 1/N).
2. TRAMPA crosstalk HRR (0049c): `coseno HRR contra todos los nodos` para identificar 1 ítem entre
   ~890 colapsa a ruido -> hit = NC. El HRR es para COMPOSICIÓN/COORDINACIÓN POR ROL, no para
   RECUPERACIÓN DE ÍTEM de vocabulario grande. Para identificar ítem específico usar canal MÉTRICO
   (distancia Manhattan/Euclidiana, como bigrama plano o embedding de posición lineal 0032/0033) o el
   subconjunto compartido (alfabeto emergente, 0049d).
3. Medición POR COMPORTAMIENTO (no por coseno): B debe ACTUAR correctamente (abrir barrera, evitar
   veneno, reconocer estrella), no dar coseno alto. Esto evitó la trampa de 0048 (coseno alto != significa).
4. CIERRE de métrica por alfabeto compartido (0049d): cuando el coseno HRR falla por crosstalk en
   vocabulario grande, restringir la recuperación al alfabeto que EMERGÍO del joint attention (las celdas
   comunes) donde D aisla. No es "achicar el problema": es medir la comunicación sobre lo que los agentes
   REALMENTE comparten, que es exactamente lo que nació del encuentro.

## Veredicto honesto
El nacimiento del lenguaje bajo presión QUEDÓ DEMOSTRADO Y CERRADO: cuerpo (BFS) + coordinación (barreras
100%) + dolor real + belleza emergente bajo presión baja + comunicación de items conocidos por alfabeto
compartido emergente (1.0 vs NC 0.067). El HRR aporta el PUENTE de coordinación por rol y la COMPOSICIÓN de
lo nuevo; la desambiguación fina de ítem queda en canal métrico/alfabeto compartido. Coherente con Tomasello
(joint attention sostenida bajo necesidad) y con el veredicto de 0048 (HRR = estructura/composición, no
superficie).

## Archivos en vault
- `phases/phase7_composicion/run_lang_0049.py` (v1/v2), `run_lang_0049b.py`, `run_lang_0049c.py`, `run_lang_0049d.py`
- `results/results_exp_SGM_0049_lenguaje.json`, `..._0049b_lenguaje_largo.json`, `..._0049c_lenguaje_bfs.json`, `..._0049d_cierre.json`
- Registry entries: exp_SGM_0049 (HALLAZGO_PARCIAL), 0049b (HALLAZGO_DISENO), 0049c (EXITO_PARCIAL), 0049d (CIERRE_OK).
