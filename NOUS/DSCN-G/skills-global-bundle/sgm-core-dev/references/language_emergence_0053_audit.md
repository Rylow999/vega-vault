# AUDITORÍA DEL "NACIMIENTO DEL LENGUAJE" — 0049d re-interpretado (exp_SGM_0053)

Lección dura 2026-08-03 (crítica de Luciano + respuesta honesta del agente).

## El hallazgo que hay que mirar con lupa

La serie 0049-0050 ("nacimiento del lenguaje") tenía un agujero que Luciano detectó:

| Exp | Qué mide | comunicación (real) | NC (azar) |
|-----|----------|---------------------|-----------|
| 0049 | ~5-8 celdas posibles | 0.125-0.375 | 0.0-0.125 |
| 0049b | ídem, sesión larga | 0.0-0.25 | igual al NC |
| 0049c | ~890 celdas visitadas | 0.0 | 0.0 |
| 0049d | 15 celdas "alfabeto" pre-identificadas | 1.0 | 0.067 |

El salto 0049c (0.0, colapsado por crosstalk con 890 ítems) → 0049d (1.0) **NO vino de que el lenguaje "emergiera"**.
Vino de **reducir el problema a 15 símbolos fijos, previamente identificados como los puentes** entre los dos
agentes. Con D=256 y solo 15 ítems, **exp_0029 ya había demostrado que HRR recupera eso casi perfecto** (cleanup
memory, no evidencia de comunicación emergente). El 1.0 de 0049d mide "¿puede HRR codificar/decodificar 15 símbolos
conocidos de antemano?", pregunta ya respondida 3 experimentos atrás.

**Veredicto honesto:** 0049d NO es evidencia de lenguaje emergente. Es capacidad de cleanup de HRR sobre 15 símbolos
conocidos. El registry entry de 0049d se re-etiquetó a `HALLAZGO_PARCIAL_REINTERPRETADO`.

## Esto es una VARIANTE de la trampa anti-paper-vision (confound de CAPACIDAD)

No es hardcodear el control (anti-patrones 1-9 de sgm-experiment-flow). Es **medir la capacidad de un mecanismo ya
demostrado y presentarlo como un efecto nuevo**. Regla OBLIGATORIA al afirmar "X emergió":
- Preguntarse: "¿lo que acabo de medir es un EFECTO NUEVO o la CAPACIDAD YA DEMOSTRADA de un mecanismo conocido?"
- Si el mecanismo (HRR cleanup, D dado) ya probó aislar N ítems en exp_0029, entonces "aislar N ítems" NO es evidencia
  de nada nuevo. Hay que medir algo que 0029 NO cubría (generalización, composicionalidad, escala abierta).

## Los 3 tests decisivos (exp_SGM_0053) — patrón reusable de auditoría de "¿es lenguaje o memorización?"

1. **ZERO-SHOT:** entrenar el alfabeto compartido sobre un SUBconjunto de celdas (ej. 8 de 15); luego A señala celdas
   NUEVAS que B nunca vio en el alfabeto. Si B las identifica > NC → hay generalización (lenguaje). Si cae a azar →
   es memorización de 15 símbolos fijos.
2. **TopSim:** correlación de Spearman entre distancia ESPACIAL de celdas y distancia HRR de las señales
   (`1 - cosine`). TopSim alto → composicionalidad (la señal refleja la geometría). ~0 → memorización sin estructura.
   Da una medida OBJETIVA en vez de depender de la intuición.
3. **D ESCALADO (0049c abierto):** repetir la comunicación con D según la ley de capacidad de exp_0029, en vez de
   recortar el vocabulario. Si con D alto la comunicación en ~890 ítems sube > NC → el HRR SÍ resuelve escala abierta
   (solo faltaba D). Si sigue en 0 → el crosstalk no es solo D, es otro problema.

### Ley de capacidad de exp_0029 (para escalar D)
- D=128 → M_max_95 = 200 ítems; D=1024 → M_max_95 = 800 ítems (≈4x).
- Acierto a d=5: D=128→0.933, D≥256→1.0.
- Aprox: `M_max ≈ 200 × (D/128)^0.667`. Para 890 ítems: `(D/128)^0.667 ≥ 4.45` → `D ≈ 1200` → usar **D=1280**.

## Diseño de 0053 (sketch)
- `simular_clima`: 2 agentes BFS, build_alfabeto = celdas visitadas por ambos (joint attention).
- Zero-shot: `train_alf = alf[:8]`, `test_alf = alf[8:15]`; B recupera por cleanup contra alf COMPLETO.
- TopSim: `spearman(dist_espacial, 1-cosine_HRR)` sobre el alfabeto.
- D escalado: D=1280, 890 ítems, medir hit vs NC.
- Veredicto: si zero_shot ~ NC y TopSim ~0 → memorización de 15 fijos (0049d no era lenguaje). Si D escalado sube
  >> NC → HRR resolvía escala (faltaba D).

## Bug de ENSAMBLE que costó 3 corridas (transitorio, no durable)
Al armar `run_com_0053.py` con `cat T1 T2 >> HEAD` se DUPLICABA el contenido (el HEAD ya tenía el append previo) →
`World(seed, p)` aparecía 2 veces y el `simular_clima` con `,p` seguía. FIX: `rm -f HEAD; cat HEAD T1 T2 > DEST`
(en orden: header primero, luego Agent, luego simular — si el Agent usa `D=D` default, el header debe definir D antes).
No es lección durable (retry lo resolvió), pero recordá: al concatenar partes, usá `>` (no `>>`) y respetá el orden de
definiciones (D/World antes de Agent).
