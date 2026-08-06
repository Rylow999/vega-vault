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

## v0.1 — Concept Proof
- Dinámica: Ec.2 (afinidad de cadena, exp(-α·‖ω_m−ω_n‖)) + Ec.5 (poda V<θ_death).
- `run_v01.py`: Python puro (sin numpy) — fiel al motor real en lo que gobierna N*.
- Kuramoto omitido: no afecta el punto fijo de poda (recalcula φ, no V ni visitas).
- Barrido: N_init ∈ {4,10,50,200,1000,5000,10000}, 20 seeds × 2000 pasos.
- Métricas: N*_mean/std, ρ (Herfindahl de concentración de cadenas),
  cota universal N* ≤ 1/θ_death, condición de punto fijo ρ ≥ N*·θ_death².

## Criterio de falsación
- SI N* crece ~lineal/sublineal con N_init → hay arquitectura de memoria escasa que explotar.
- SI N* satura (~4–5) para todo N_init → la homeostasis colapsa el grafo; DSCN-G
  no sostiene vocabulario masivo sin rediseñar la dinámica de poda (θ_death, K, γ).

## Estado
- 2026-07-25: corrida v0.1 lanzada. Resultado parcial (N_init≤200): N*≈4.4 ± 0.5
  (saturado). Pendiente confirmar en 1000–10000.
