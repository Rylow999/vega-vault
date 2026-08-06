# Hallazgos medidos DSCN-G Language Engine (sesión 2026-07-25)

Estado de los experimentos corridos y validados. Cada uno escribió JSON en
`NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/v0.X_*/`.

## Qué se probó y el veredicto
- **v0.1** (concept proof, motor real de v0.1): N* (nodos activos) satura ~4.5
  sin importar N_init (4→5000). El grafo es MEMORIA DE TRABAJO, no masa.
  Falsa la hipótesis de "memoria escasa escalable". ✅ medido.
- **v0.2** (sweep K, θ_death a N=1000): el colapso es PARAMÉTRICO (N* sube con
  K / baja θ_death: K=3/θ=0.1→3.8, K=30/θ=0.003→166.8) pero SUBLINEAL (de
  1000 solo viven 17%). ✅ paramétrico, no estructural.
- **v0.3** (retrieval, ω→concepto): grafo RECUPERA el concepto correcto 100%
  (norma) / 91% (bits, tu idea de Pandora) a 256 conceptos. ✅ el grafo entiende.
- **v0.4** (β_eff contextual de Pandora): script escrito, sweep pesado N=1000
  corrió 40+ min; resultado no capturado en JSON (log vacío, proc soltado).
  PENDIENTE re-correr y guardar.
- **v0.5 / v0.5b** (decoder L2): v0.5 genera loop "el casa el casa...". v0.5b con
  ventana de contexto (penalizar repetición) ROMPE el loop → "el roja la corre...".
  ✅ el grafo habla (aunque sin gramática).
- **v0.6a** (next-token sobre Don Quijote, corpus real): accuracy 0.45%→10.11%.
  ✅ el grafo APRENDE de datos reales (next-token, estilo GPT-1 pero en grafo local).
- **v0.6b** (dolor post-hoc, castigo V): mejora 0.0. ✗ el dolor llega tarde.
- **v0.6b-bis** (Q-learning en aristas, dolor=error predicción): mejora -0.0012.
  ✗ redundante en supervisado (el corpus ya da la respuesta).
- **v0.7 / v0.7-bis / v0.7-final** (contexto): todos peores que v0.6a
  (5.89% / 0.49% / 3.85% vs 10.11%). ✗ con vocab chico el contexto no ayuda
  (la palabra previa ya tiene la info; tabla trigrama muy dispersa).
- **v0.8** (atención rústica ponderada): 8.64%, aún < 10.11%. ✗ mejor que tabla
  pero no supera bigrama con vocab=150.
- **v0.3 REAL v2** (hibernado sobre motor v0.1, corriendo al cierre de sesión):
  pendiente resultado. Debe mostrar N_total ~ N_init mientras N_active colapsa.
- **v0.9a** (dolor = señal de evasión + AUDIT + fallback, de SynapticCache):
  escrito, no lanzado (esperaba v0.3 REAL). Listo para correr.

## Corpus usado
- `donquijote.txt` (Project Gutenberg, 2.2MB, español real) bajado por urllib.
- Benjamin (argentinísimo) NO bajó: HF pide auth 401, no hay git en el equipo.
  Pendiente token de Luciano para corpus real argentino.
- Ideas de Luciano integradas: DB semántica en bits/puertas (v0.3 valida que
  recupera), hibernado (v0.3 REAL), etiquetas que mutan + historial, dolor por
  subsistencia (v0.9), dimensiones por abstracción (amor>rojo, pendiente v0.6c).

## Mapa honesto de capacidades del grafo rústico
FUERTE en local: recupera conceptos, aprende next-token, no colapsa si ajustás
parámetros. DÉBIL en: contexto largo (necesita atención/ambigüedad), dolor en
supervisado (redundante), feedback cualitativo real (pendiente v0.9c/entorno).
Perfil: "memoria de trabajo neuro-simbólica", no LLM. Para pseudoAGI hay que
hibridar con algo que aporte contexto/escala.

## Roadmap acordado (Luciano: "de a poco")
v0.3 REAL (hibernado) → v0.9a (dolor evasión) → v0.9b (etiquetas mutan) →
v0.10 (persistencia con SynapticCache 2.1/2.4) → v0.9c (subsistencia global) →
v0.6c (abstracción) → v0.12 (atención real) → v0.13 (entorno/dolor de mundo).
Repo GitHub público pendiente: Luciano debe dar usuario + token PAT (el vault
/sdcard no tiene git; el repo se arma en el home de la app).
