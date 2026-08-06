# Grid bottleneck / obstacle-avoidance (exp_SGM_0032 → 0033 → 0033b)

Camino A = closed loop in a 2D world. Receta que pasó, con los errores que costaron re-runs.

## HRR positional embedding COLLAPSES collinear cells (lección dura 0033b)
`pos_embed(r,c) = normalize([r/Ht, c/W, sin(2π r/Ht), cos(2π c/W), noise])` y también la versión
lineal `normalize([r/Ht, c/W])` **colapsan** todas las celdas de una misma fila/columna en el MISMO
vector (desde el origen, puntos colineales tienen coseno 1.0 idéntico con la meta). El agente no
distingue (0,1) de (0,3) y rebota sin avanzar (bounce entre (0,1)↔(0,2)). El coseno-desde-un-origen
es degenerado para control fino de locomoción.

**Fix honesto:** separar "memoria relacional gruesa" (HRR/embedding, para relaciones) de "control fino"
(usar DISTANCIA MÉTRICA directa al objetivo). El agente elige el vecino que minimiza:
`dist(nb, meta) + K_DOLOR * dolor_count.get(nb, 0)`.
- `dist` = Manhattan (o Euclidiana) a la meta → gradiente que avanza siempre.
- `dolor_count[cell]` = memoria de dolor ACUMULADA (se incrementa al pisar la celda de dolor); PERSISTE
  entre episodios → es la semilla de identidad (el agente "recuerda" dónde le dolió).
- `K_DOLOR` ~10: con 1-3 pisadas el costo supera la distancia extra del rodeo y el agente desvía.

Esto es obstacle-avoidance estándar (value/cost gradient), NO un hack para aprobar. Documentar el
límite del embedding HRR de posición explícitamente en notes (no maquillar).

## Diseño del bottleneck (0033b) — cuello de botella real
- Pared en columna 4 completa; DOS gaps: `(0,4)` = DOLOR (en el camino corto B→G por fila 0), `(9,4)` = LIMPIO (ruta larga por abajo).
- K=5 viajes B→G→B...; ω y `dolor_count` NO se resetean entre viajes (memoria persistente = identidad).
- CON dolor: viaje 1 pasa por (0,4) y lo penaliza; viajes 2-5 toman la ruta larga. → pisadas [1,0,0,0,0].
- ABIERTO (sin dolor): siempre el camino corto → [1,1,1,1,1] (5 total).
- RW: vaga → ~16 pisadas.
- Tests: T1 = CON_total < ABIERTO_total; T2 = CON llega siempre; T3 = CON_viaje1 > CON_viaje5
  (mejora con memoria); NC = ABIERTO no aprende (ABIERTO >= CON). Todos PASS.

## Measurement pitfalls (costaron 4 rediseños en 0032/0033/0033b)
1. **No cuentes dolor por flag interno** (`use_dolor` solo setea el flag si aprende). Contar por
   **posición ground-truth**: `if ag.pos == pain_cell`. El control (loop abierto, sin aprender) pisa
   la celda pero no setea el flag → si cuentas por flag da 0 y rompes T1/T3.
2. **El control válido de "no aprende" es RANDOM WALK, NO el agente determinista sin dolor.** El agente
   determinista sin dolor puede esquivar la zona por su ruta fija al azar (da 0.0 pisadas) → control
   inválido. RW sí no aprende y pisa.
3. **Dolor en celda ÚNICA no se mide** (el agente la rodea sin pisarla o la pisa 1 vez igual en ambos
   casos → sin diferencia). Usar ZONA de dolor en la ruta que la afinidad prefiere, o (mejor) bottleneck
   con el dolor en el ÚNICO camino corto forzado.
4. **No pongas el dolor en paredes** (el bloque central del 0033 tapaba la diagonal → 0 pisadas en todos).
   Verificar con BFS que la ruta pasa por la zona antes de afirmar.
5. **Timeout por bucle infinito:** el loop de viajes debe tener tope `MAX_TICKS` por viaje; si el agente
   no llega, cuenta el viaje como fallido y sigue. Sin tope se cuelga (exit 124).

## Resultado honesto 0033b
Evasión fuerte REAL + memoria entre episodios (identidad). CON 1 pisada total vs ABIERTO 5 vs RW 16.
El embedding HRR no sirve para locomoción fina; el gradiente métrico + costo de dolor sí. Esto CONECTA
con el próximo paso: identidad (self-state persistente a través de resets) y curiosidad (drive intrínseco).

Ver también `references/grid_agent_caminoA.md` (0032, maze aleatorio estándar) y
`references/grid_dolor_obstacle_notes.md` (0033, dolor-zona).
