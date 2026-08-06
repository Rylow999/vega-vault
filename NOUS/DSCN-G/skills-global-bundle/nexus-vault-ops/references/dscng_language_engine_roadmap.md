# DSCN-G Language Engine — Roadmap v0.1→v0.5

Versioned experiment pipeline under `NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/`.
Goal: test whether DSCN-G can be a language-engine substrate, ending in a rustic
L2 (ω→text) decoder. Goal is to reach the decoder DE A POCO (user's words), not
in one giant step.

## Layout created (2026-07-25)
```
LANGUAGE_ENGINE/
  README.md                      # roadmap + estado
  PANDORA_Resumen.md             # resumen-critica del proyecto PANDORA (propio de Luciano)
  v0.1_concept_proof/
    run_v01.py                   # Eq.2+Eq.5 pure-python (no numpy en este host)
    results_v01.json             # datos reales
    dscng_engine.py              # copia del motor real verify_dscng_v3.py
  baselines/  decoder/  results/ # vacios, para v0.5
```

## Hypothesis → falsification lineage
- v0.1 (HECHO): "DSCN-G converge a pocos nodos => memoria escasa escalable O(N*)".
  FALSADO. N* satura ~4.3 (N_init 4→5000). Cota universal N*≤1/θ_death=10 respeta.
  Conclusión: DSCN-G = memoria de TRABAJO, no base de masa. El claim de eficiencia
  era una trampa (poco activo PORQUE la poda mata todo, no por eficiencia).
- v0.2 (CORRIENDO 2026-07-25, sweep K/θ_death @ N_init=1000): ¿el colapso es
  PARAMÉTRICO (N*_max≈(K+1)/θ_death, se arregla subiendo K / bajando θ) o
  ESTRUCTURAL (la afinidad siempre lo manda al piso)?
- v0.3 (ESCRITO, HELD): HIBERNADO. Regla v0.1 borra ω en V<θ_death; v0.3 lo mueve
  a lista dormida preservando ω. Mide N_active+N_hibernado = N_total_mass. Valida
  si la masa sobrevive ~N_init. Une TU idea de DB semántica + PANDORA HIBERNADO.
- v0.4 (plan): β_eff = β(1+ρ) (tasa contextual, de PANDORA). Barato, reutilizable.
- v0.5 (plan): L2 RÚSTICO = proyección lineal ω→vocab, corpus chiquito. EL cuello
  de botella real (PANDORA y GPT coinciden). Decide: decoder lineal puro vs
  retrieval+decoder (recuperar conceptos desde la masa primero). Sin L2 el grafo
  es mudo.

## PANDORA convergence (por qué v0.3 no es aire)
PANDORA es proyecto PROPIO de Luciano (grafo semántico + L2 lineal, resumido por
otra IA). Su regla de ciclo de vida: V>0.30 ACTIVO, 0.10<V≤0.30 DURMIENTE,
V≤0.10 HIBERNADO (ω preservado, NO se borra), V≤0.10 por >100 intentos MUERTO.
Eso es EXACTAMENTE la corrección que v0.1 pidió (no borrar, separar masa de working
set). Y TU idea de "DB semántica: nodos en bits+puertas lógicas, memoria dividida
en tipos/relaciones" llega al mismo lugar por otro camino. Dos caminos distintos
→ mismo fix = señal de validación, no casualidad.

Otras piezas de PANDORA reutilizables: ventana de contexto dinámica
W(t) = W_base / (1+κ_W·E_root(t)) (se contrae bajo estrés), y el "Generative XOR"
(nodo hijo por co-resonancia) que es solo ecuación en el doc, no implementado.

## Running recipe (Android host, no numpy)
- Plain `python3` (3.13.13) in HERMES TERMINAL works for home-only scripts.
- Run FROM HOME, write JSON to home, then `su -c 'cp ... /sdcard/Hermes/...'`.
- Background: `terminal(background=true, notify_on_complete=true)`.
- NEVER concurrent heavy sims (single CPU saturates). Hold v0.3 until v0.2 ends.
- Cost probe first: 1000×3×600 ≈ 44s ⇒ 10000 infeasible in pure python; N_init
  up to 1000 already enough to falsify saturation.
