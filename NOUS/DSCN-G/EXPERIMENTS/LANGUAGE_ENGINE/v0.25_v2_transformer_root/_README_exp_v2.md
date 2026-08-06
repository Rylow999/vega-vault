# DSCN-G Language Engine — Experimentos

Propuesta: reemplazar (o hibridar) el paradigma Transformer por una arquitectura
basada en DSCN-G como sustrato cognitivo (nodos semánticos ω/φ/V + memoria
dinámica con poda homeostática).

## Estructura
- `v0.1_concept_proof/` — Experimento base: ¿el punto fijo de homeostasis permite un grafo de lenguaje?
- `baselines/` — Transformer / RNN / LSTM para comparar (scaling de memoria y contexto).
- `decoder/` — Capa generadora de lenguaje (Opción A: DSCN-G + mini-decoder).
- `results/` — JSON crudos de cada corrida.

## Hipótesis de la propuesta (GPT + Luciano)
"El sistema converge a pocos nodos activos mediante homeostasis → arquitectura
de memoria escasa escalable O(nodos_activos), vs O(n²) de la atención Transformer."

## Pregunta científica real
¿N* (nodos activos en estado estacionario) crece con N_init, o satura en un
pequeño punto fijo independiente de N_init? Si satura, el claim de "memoria
escasa escalable" es FALSO con la dinámica actual y hay que cambiar la poda.

## v0.1 — Concept Proof  [COMPLETADO 2026-07-25]
- Dinámica: Ec.2 (afinidad de cadena, exp(-α·‖ω_m−ω_n‖)) + Ec.5 (poda V<θ_death).
- `run_v01.py`: Python puro (sin numpy en este entorno) — fiel al motor real en
  lo que gobierna N* (el Kuramoto omitido no afecta el punto fijo de poda).
- `dscng_engine.py`: copia del motor real verify_dscng_v3.py (para reference).
- Barrido: N_init ∈ {4,10,50,200,1000,5000}, 20 seeds × 2000 pasos (menos en
  los grandes por costo), params α=5, β=0.20, γ=0.01, θ_death=0.10, d=8, K=3.

### Resultados (results_v01.json)
| N_init | N* mean | N* std | ρ (Herfindahl) | fp? | bound? |
|--------|---------|--------|----------------|-----|--------|
| 4      | 4.00    | 0.00   | 0.444          | ✓   | ✓      |
| 10     | 4.80    | 0.40   | 0.467          | ✓   | ✓      |
| 50     | 4.60    | 0.49   | 0.511          | ✓   | ✓      |
| 200    | 4.20    | 0.60   | 0.511          | ✓   | ✓      |
| 1000   | 3.88    | 0.78   | 0.472          | ✓   | ✓      |
| 5000   | 3.33    | 0.47   | 0.407          | ✓   | ✓      |

Cota universal N* ≤ 1/θ_death = 10: respeta en todos. Condición de punto fijo
ρ ≥ N*·θ_death²: ✓ en todos.

### Conclusión del v0.1
**La hipótesis de "memoria escasa escalable" QUEDA FALSADA** (en su forma
ingenua). N* SATURA en ~4.3 nodos y DECRECE levemente con N_init (3.33 a 5000),
en vez de crecer. El punto fijo homeostático colapsa cualquier vocabulario
masivo a ~4 nodos vivos. No es "memoria escasa eficiente"; es un colapso
amnésico: un grafo de 100.000 conceptos muere hasta 4.

Esto NO mata la idea de usar DSCN-G como motor cognitivo, pero descarta el
argumento de eficiencia "O(nodos_activos) escalable" TAL CUAL está formulado.
El punto fijo de ~4–5 es compatible con una MEMORIA DE TRABAJO (working set),
no con un almacén de vocabulario. Coincide con el diseño Ring-0/1/2/3 del v4:
DSCN-G como memoria de trabajo cognitiva, no como base de conocimiento total.

## Camino a v0.2 (rediseño de poda)
Para que DSCN-G sostenga vocabulario masivo, la dinámica de poda debe cambiar.
Tres hipótesis a testear:
1. **Poda por predicción única** (predictive coding): un nodo sobrevive si
   aporta información predictiva distinta, no solo si es visitado por una cadena.
2. **Más cadenas / menor θ_death**: subir K y bajar θ_death para mantener más
   nodos vivos (cuesta más cómputo de afinidad).
3. **Memoria de masa vs memoria de trabajo**: separar el vocabulario total
   (V latente, no se poda) del subgrafo activo de ~N* (working set).

## Criterio de falsación (global)
- SI N* crece sublineal con N_init tras el rediseño → hay arquitectura de
  memoria escasa explotable.
- SI N* sigue saturando en ~4–5 sin importar N_init → DSCN-G es memoria de
  trabajo, no reemplazo de la base de parámetros del Transformer.

## Estado
- 2026-07-25: v0.1 completado. N* satura ~4.3 (falsa "memoria escasa escalable").
  Siguiente: v0.2 rediseño de poda.
