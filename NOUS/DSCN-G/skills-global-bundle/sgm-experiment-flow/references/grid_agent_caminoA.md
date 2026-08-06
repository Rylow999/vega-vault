# Grid Agent — Camino A (loop cerrado en entorno 2D) · exp_SGM_0032

Primera vez que SGM deja de medir una mecánica aislada y opera un CUERPO en un mundo: el agente
transita un grid, deja huella (ω se actualiza al pisar), y navega hasta la meta por afinidad sobre
su memoria de posición. Esto es el salto de "mecanismo" a "agente situado".

## CORRECCIÓN DE DISEÑO (clave de la sesión)
El primer intento armó el laberinto A MEDIDA para que el test dé verde (atajo inalcanzable rodeado
de paredes, dolor fuera de camino, 8×8 casi abierto). Eso dio falso negativo Y falso positivo a la
vez (el plano también llegaba 1.0 porque el mapa era trivial). Luciano frenó: _"No tenés que pensar
cómo hacerlo para que pase, si no hacerlo bien. Buscá algún test típico que se utilice en estos
casos. Tal vez el mapa es muy simple para el sistema."_

REDISENO a **benchmark estándar GridWorld/MiniGrid** — no a medida:
- Maze aleatorio 10×10 (p_wall=0.30) generado por semilla `random.Random(SEED)`.
- **BFS para garantizar conectividad B→G**; si no conecta, regenerar (hasta 200 intentos).
- **Baseline RANDOM WALK** (caminante aleatorio) por trial — comparación honesta, no "a medida".
- Variable discriminante: tasa de llegada SGM (afinidad sobre ω de posición) vs random walk.
- Resultado: SGM **0.9** / random walk **0.05** → navegación situada validada (T-GRID-01 + NC PASS).

## Diseño técnico que funciona
- `omega[celda] = EMBEDDING LINEAL MÉTRICO en (r,c)`: `v[0]=r; v[1]=c; resto ruido*0.01; normalize`.
  Celdas cercanas en grid → ω cercanos → el vecino que acerca a la meta tiene mayor coseno con
  `pos_embed(meta)`. (El embedding `[r/Ht, c/W, sin, cos]` NO es métrico → cuerpo clavado en (0,0).)
- `sense()` = `pos_embed(meta) + ruido` (apunta a dónde quiere ir, no describe vecinos).
- `choose_move()`: vecino con mayor `cos(ω[vecino], ω[meta])`.
- Huella: al pisar, reforzar ω de la celda (memoria de travesía).
- Dolor (no concluido aquí): penalizar ω de la celda pisada (como 0025). En maze puro el camino
  corto BFS suele ser ÚNICO → no hay dónde esquivar → diferido a 0033 con mapa de bifurcación.

## Regla general (aplica a TODOS los experimentos, no solo grid)
**No tunees el ENTORNO para forzar PASS.** Si el mapa/mundo lo armás a mano para que tu mecanismo
dé verde, el test no mide nada.
1. Usá un benchmark estándar del área (maze aleatorio + BFS + random-walk baseline para navegación;
   unigram para lenguaje; loop abierto para aprendizaje). No inventes escenario a medida.
2. Si el entorno es tan simple que hasta el baseline (plano/aleatorio) pasa, el mecanismo no se
   está ejercitando → agrandalo hasta que el baseline falle y tu mecanismo lo supere. Esa es la
   señal de que medís algo real.
3. Si un sub-test no se puede medir en el entorno elegido, separalo a otro experimento con el mapa
   adecuado. No maquilles el FAIL a PASS.

## Variables (test-first + NC)
- T-GRID-01: llegada SGM > llegada random walk (navega mejor que al azar).
- T-GRID-02: con dolor, pisadas de la celda de dolor < que loop abierto (NO concluyó en maze puro → 0033).
- T-GRID-NC: random walk llega menos que SGM (benchmark honesto, no trivial).

## Rendimiento en celular
- D=128 (ya 1.0 en 0029), TRIALS=8. ~80s. Sin cacheo / D=256 / TRIALS=12 → pasaba 200s (timeout).

## Siguiente (Luciano: "luego vamos mejorando la simulación de a poco")
- 0033: mapa con BIFURCACIÓN explícita para medir "aprende a esquivar dolor" (estándar GridWorld
  obstacle-avoidance). NC: loop abierto (sin dolor) pisa la celda.
- ASCII+JSON en vivo (indicadores: tick#, pos, dist meta, valencia E, dolor, masa PPR, huella) +
  HTML canvas para demo portable.
- 0034+: atajo relacional EN grid (maze con dos rutas, una es atajo empaquetado HRR).
