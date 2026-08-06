# DSCN-G Language Engine v0.6 — next-token + dolor (2026-07-25 noche)

## Contexto
Tras v0.5b (loop roto con ventana de contexto), el usuario pidió v0.6a Y v0.6b y aportó
ideas clave: (a) usar un CORPUS EXISTENTE real, no frases hechas a mano; (b) aprender por
SUBSISTENCIA / "dolor" = baja de vitalidad por uso incorrecto; (c) etiquetas lingüísticas
(núcleo/verbo/conector) que MUTAN por uso y guardan HISTORIAL; (d) conceptos abstractos
tienen más dimensiones que concretos (amor > rojo). El usuario además planteó el marco de
"pseudoAGI" y pidió comparar Transformer vs grafo.

## Corpus
- NO hay `web_search` en este entorno; se usa terminal + `urllib` (hay red).
- Bajado DON QUIJOTE (gutenberg.org/files/2000/2000-0.txt, 2.2MB, español real, dominio
  público) a home y copiado al vault LANGUAGE_ENGINE/.
- Benjamin (corpus argentino de pysentimiento) NO bajó: HF pide auth 401, no hay `git`
  en el dispositivo, rutas de GitHub 404. Quedó PENDIENTE (requiere token HF del usuario).
- DECISIÓN DEL USUARIO: usar corpus ARGENTINO. Mientras tanto v0.6a corrió sobre Don Quijote
  (español real) + textos criollos del vault. El Benjamin real se conecta cuando el usuario
  cree el token HF.

## GPT-1 paper
- Bajado: https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf
  → vault LANGUAGE_ENGINE/gpt1_paper.pdf. pdfminer falla por dependencia `cryptography`
  ausente; citar hechos estándar (12-layer decoder-only, 117M params, next-token log-likelihood).

## v0.6a — next-token supervisado (estilo GPT-1) — DONE
- Vocabulario top-V=200 de Don Quijote; cada palabra = nodo con ω (D=8). Por cada par
  (w_i, w_{i+1}), ω de w_i aprende acercarse a ω de w_{i+1} (objetivo = palabra REAL, no
  ω_ideal fijo). Es next-token prediction en representación LOCAL de grafo (ajusta 200 ω,
  no 117M params).
- Resultado REAL (run_v06a.py, 241.443 palabras, 3 epochs):
    accuracy ANTES: 0.0045   |   DESPUÉS: 0.1011   |   mejora 22x
- El grafo APRENDE next-token de datos reales. 10% es bajo (vocab chico, 3 epochs, sin
  contexto global) pero el punto está probado.
- BUG y FIX: en `predict()` arrancaba `best,bests=-1,None` → `s>bests` comparaba float>None
  (TypeError). Fix: `best,bests=-1,-1.0`. Relanzado OK.
- Vault: LANGUAGE_ENGINE/v0.6_next_token/{run_v06a.py, results_v06a.json}.

## v0.6b — dolor (RL/RLHF) + etiquetas mutantes — DISEÑADO/CORRIENDO
- run_v06b.py lanzado en background al cierre. Misma corpus. Dolor HARDCODEADO (Opción A):
  transición inválida = dos sustantivos seguidos (S-S, diccionario mini SUST/VERB/CONN) →
  baja V (V-=0.05) y aleja ω de la transición; válida → sube V (+0.01). ETIQUETA se anota en
  HISTORIAL de aplicaciones. Métrica: tasa de transiciones inválidas ANTES vs DESPUÉS.
- Al reiniciar: leer results_v06b.json (v0.6b seguía corriendo al cierre). El dolor hardcodeado
  es placeholder; el dolor REAL debe venir de CONSECUENCIA EN EL MUNDO (entorno), no de regla.

## v0.6c — dimensiones por abstracción (idea Luciano, PENDIENTE)
- Hipótesis: abstractos (amor) necesitan más grados de libertad / más vecinos que concretos
  (rojo). Medible como GRADO DEL NODO (vecinos con afinidad>umbral) tras entrenar.

## Marco Transformer vs Grafo
- Transformer: UNA matriz W (117M params) por backprop sobre TODO el corpus (O(params));
  "gato→come" vive EN LOS PESOS (difusa). POR ESO usa tanta potencia.
- Grafo DSCN-G: conexión = arista real entre nodos; ajusta SOLO nodos tocados (O(~4.5)) →
  barato. MISMA dinámica (minimizar error next-token) pero el "peso" es el ω del nodo.
- Tensión: Transformer paga potencia por ESCALA (50k palabras vivas); grafo barato PERO
  colapsa a ~4 sin HIBERNADO. El ahorro no es "despilfarro" del Transformer.

## "PseudoAGI" — distancia honesta
- YA tenemos (medido): marco auditado; grafo recupera (v0.3); no colapsa si ajustás params
  (v0.2); decoder habla (v0.5b); aprende next-token de corpus real (v0.6a). Es un SUSTRATO
  COGNITIVO RÚSTICO neuro-simbólico, pieza legítima de ruta a AGI.
- FALTAN 4 gaps: (1) CONTEXTO global (W(t) Pandora); (2) DOLOR real desde entorno; (3)
  ABSTRACCIÓN/dimensiones (v0.6c); (4) PERSISTENCIA real (hibernado v0.3b no mergeado).
- Veredicto: pseudoAGI de laboratorio ALCANZABLE en meses; AGI completa es otro orden.

## Estado al cierre
- v0.4 (β contextual): seguía corriendo (sweep N=1000, 43+ min). Relanzar y leer results_v04.json.
- v0.6a: DONE. v0.6b: CORRIENDO (leer results_v06b.json).
- Pendiente: Benjamin (token HF), v0.6b resultado, v0.6c, merge hibernado v0.3b.
