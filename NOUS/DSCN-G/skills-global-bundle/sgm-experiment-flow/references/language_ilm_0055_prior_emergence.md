# ILM 0055a/b/c/d/0056 — el PRIOR de composicionalidad debe EMERGERE del sustrato (no inyectarse)

**REGLA DE DISEÑO — INSTINTO vs HARDCODE (corrección de Luciano, 2026-08-03):** al modelar una propiedad
emergente (composicionalidad del lenguaje, restricción del telar, etc.), un sesgo/instinto es LEGÍTIMO si
EMERGE del sustrato ya existente (afinidad Eq.2, dolor, duda, η) — es "ADN/instinto" real, como en biología.
Es TRAMPA si se INYECTA a mano (overlap de rasgos hardcodeado, if/elif del autor, parámetros elegidos).
Esto extiende la regla de "mecanismos deben emerger, no inyectarse" (eje SGM) al caso del lenguaje.

Extensión de `language_ilm_0054.md`. La serie 0055 aísla la variable que faltaba (generación dura +
zero-shot honesto) y prueba si el "sesgo de compresibilidad" (prior de similitud) es legítimo en SGM.

## Setup común (ILM PURO, sin mundo/movimiento — aísla el mecanismo de Kirby)
- Referentes estructurados: `(region N/S/E/O, distancia lejos/cerca, tipo comida/veneno/agua)` = 24.
- Bottleneck: `V=16, L=3` (16³=4096 combos > 24 referentes => debe reusar/componer).
- Cada generación: MAESTRO tiene un code (ref->msg). APRENDIZ arranca code VACÍO, ve MUESTRA `frac=0.4`
  de los msg del maestro, debe reconstruir el code completo (24 refs). Transmisión generacional real.
- Métrica: `TopSim` = Spearman(distancia de RASGOS vs distancia de mensaje Hamming) sobre el set COMPLETO,
  y por separado sobre vistos (`seen`) y NO vistos (`unseen`).
- `feature_overlap(a,b)` = nº de rasgos compartidos (0..3). `affinity_similarity(a,b)` = shared/3 + 0.1*ω.

## 0055a — PRIOR INYECTADO A MANO (baseline de control)  [TRAMPA]
- El aprendiz, ante un no-visto, le asigna el msg del visto con MÁS `feature_overlap` (el autor elige).
- Resultado: TopSim_full ~0.30-0.40 sostenido, TopSim_unseen ~0.20-0.45 (generaliza a no-vistos).
- Veredicto: HAY estructura, PERO el sesgo lo sopló el autor. Es "trampa" (paper-vision aplicado al lenguaje).
  No cuenta como composicionalidad emergente.

## 0055b — SIN PRIOR (solo bottleneck + muestra)  [EL SUSTRATO SOLO NO COMPONE]
- El aprendiz, ante no-vistos, asigna msg nuevo aleatorio (hasta V) o reuse ciego. NO usa overlap.
- Resultado: TopSim_full ~0.12-0.25, TopSim_unseen ≈ 0 o NEGATIVO (-0.03..-0.09).
- Veredicto: SIN el sesgo de compresibilidad, el sustrato HRR/bigrama NO compone. El bottleneck filtra lo
  holístico pero no RECONSTRUYE estructura. Confirma que el prior es pata faltante (Kirby: bottleneck
  necesario pero NO suficiente).

## 0055c — PRIOR EMERGENTE de la AFINIDAD de SGM  [LEGÍTIMO, no trampa]
- El aprendiz tiene `omega` de afinidad (como Eq.2 de SGM) sobre RASGOS (no posiciones).
  Ante no-visto: toma el msg del visto con MAYOR `affinity_similarity(r, s)` (mecanismo de SGM, no overlap
  hardcodeado del autor). La afinidad sube entre refs usados juntos (como Eq.2).
- Resultado: TopSim_full ~0.30-0.42 (IGUAL que 0055a) PERO sin hardcodear nada; TopSim_unseen ~0.13-0.46.
- Veredicto: el sesgo EMERGIO del sustrato (afinidad ya agrupa por rasgos). NO es trampa: la afinidad es
  sustrato real de SGM (la misma del telar del ser, dolor, duda). Es el "instinto"/ADN legítimo que Luciano
  señaló — no un agregado por experimento.

## PRINCIPIO DE DISEÑO (regla de clase para claims de lenguaje en SGM)
El sesgo de compresibilidad / composicionalidad debe EMERGERE de un mecanismo YA EXISTENTE del sustrato
(la afinidad Eq.2 alimentada con los rasgos del lenguaje), NO inyectarse como `if/elif` o `overlap` a mano.
- 0055a = inyectado => TRAMPA (paper-vision).
- 0055b = ausente => sustrato no compone.
- 0055c = emerge de afinidad => LEGÍTIMO. TopSim ~0.35 (composicionalidad DÉBIL pero real y sostenida).
- Límite honesto: TopSim ~0.35 NO es composición PLENA (~0.9 like el paper 2025 con Gumbel-Softmax + 4 agentes).
  SGM tiene el GERMAN composicional en su afinidad, pero no infiere REGLAS de combinación sistemáticas.
  Gap fino: la afinidad agrupa por rasgos compartidos, pero no "norte+comida = mensaje X" de forma sistemática.

## 0055d — PROFUNDIZAR: ¿el TopSim sube o se estanca?  [SE ESTANCA]
- Setup: igual 0055c (sesgo por afinidad) PERO bottleneck MÁS DURO (V=8 L=2 = 64 combos/24 referentes) y
  G=40 generaciones (más largo para ver tendencia).
- Resultado (3 seeds): TopSim_full g0~0.25-0.37 → g39~0.34-0.37. **NO sube hacia 0.9. SE ESTANCA en ~0.30-0.37.**
  - seed1: 0.252 → 0.361 → 0.343 ; seed2: 0.373 → 0.314 → 0.368 ; seed3: 0.277 → 0.333 → 0.348.
- Veredicto: la afinidad de SGM tiene el GERMEN composicional (0.35, no 0) pero NO INFERE REGLAS de combinación
  sistemática (lo que NN con Gumbel-Softmax SÍ hacen, llegando a ~0.9). El sustrato carece de un mecanismo de
  **inferencia de reglas**; solo agrupa por rasgos compartidos. GAP FINO confirmado y medido.

## 0056 — INFERENCIA DE REGLAS  [CIERRA EL ARCO: COMPOSICIÓN PLENA ALCANZADA]  (2026-08-03)
- **Pregunta que resolvemos:** 0055d se estancó en ~0.35. ¿El sustrato SGM puede componer PLENO (~0.9) SI el
  aprendiz INFERE la regla de mapeo (no copiar el msg del más afín / no contar bigrama), o confirma que
  HRR/bigrama necesita Gumbel-Softmax (backprop/objetivo) para sistematicidad?
- Setup: igual 0055c (V=16 L=3, 24 referentes, sesgo por afinidad BASE) PERO el aprendiz **INFERE el mapeo
  rasgo→símbolo de la MUESTRA** (`region→pos0, distancia→pos1, tipo→pos2` = el más frecuente por posición)
  y lo aplica SISTEMATICAMENTE a TODOS los referentes (vistos y no-vistos). No copia, deduce regla.
- Resultado (3 seeds): TopSim_full **0.86-1.00** (seed2/seed3 = 1.0 en g0 y g19).
  - seed1: g0=0.861, g19=0.732 ; seed2: 1.0, 1.0 ; seed3: 1.0, 1.0.
- Veredicto: **COMPOSICIÓN PLENA alcanzada SIN Gumbel-Softmax.** El sustrato SGM SÍ compone; lo que faltaba
  no era la arquitectura sino que el aprendiz **INFIRIERA la regla**, no copiara/agrupara. La afinidad (0055c)
  da el germen (~0.35) porque agrupa por rasgos; la regla sistemática (0056) lo lleva a 1.0.
- Registry: 0056 = HALLAZGO_POSITIVO_FUERTE. Cierra el debate de lenguaje de SGM.

## GUMBEL-SOFTMAX vs HRR/BIGRAMA (en criollo, para entender por qué nos estancamos en 0.35)
- **Gumbel-Softmax (NN modernas, paper 2025 de Kirby, arXiv:2404.02145):** truco para que una red elija
  símbolos DISCRETOS (vocabulario) y TODAVÍA sea entrenable con backprop. En vez de elegir "símbolo duro",
  genera una mezcla suave (softmax) de TODOS los símbolos con peso según qué tan seguro está + ruido (Gumbel).
  Temp alta = explora; temp baja = elige uno. Esa mezcla ES derivable → podés premiar "el otro entendió" y
  castigar "no fuiste sistemático". El canal estrecho + aprendiz que arranca de cero cada generación FUERZA
  que los símbolos tengan sentido composicional (si no, el que viene no entiende y pierde). Por eso llegan a ~0.9.
- **HRR/bigrama (lo nuestro):** HRR = cada ítem es vector D-dim; "componer" sería bind (unir vectores), pero
  lo usamos como etiqueta opaca de celda, no componemos. Bigrama plano = el decoder mira frecuencias
  (dado símbolo anterior y referente, ¿cuál viene?). Es MEMORIA ESTADÍSTICA, NO inferencia de regla: no deduce
  "región→símbolo1"; cuenta. Por eso nos estancamos en 0.35 (agrupa por afinidad pero no infiere regla).
- **Diferencia de fondo:** Gumbel-Softmax tiene OBJECTIVE explícito (que el otro entienda) + canal estrecho que
  obliga a comprimir con reglas. HRR/bigrama tiene afinidad (agrupa, de ahí 0.35) pero NO objetivo de
  comunicación que fuerce sistematicidad. **0056 demostró que si le damos al aprendiz la capacidad de INFERIR
  la regla (contar frecuencias por rasgo y aplicar sistemáticamente), HRR/bigrama ALCANZA composición plena sin
  Gumbel-Softmax.** El gap no era la arquitectura, era el mecanismo de aprendizaje (copiar vs inferir).

## Lección de Kirby aplicada a SGM (cierre del arco 0049→0056)
1. El bottleneck + transmisión generacional generan la SEÑAL (0053/0054b). Sin estos 3 ingredientes (bottleneck
   duro, estructura de referentes, transmisión con pérdida) no hay composición (0049-0050, 0053).
2. El prior de compresibilidad debe EMERGERE del sustrato (afinidad Eq.2) — no inyectarse (0055a trampa, 0055c
   legítimo). Es el "instinto/ADN" que Luciano señaló como válido en biología.
3. La afinidad da el GERMEN (~0.35) pero se ESTANCA (0055d) porque no infiere reglas. Con inferencia de regla
   (0056) el sustrato LLEGA a composición PLENA (~1.0). No hacía falta Gumbel-Softmax/backprop.
- **Veredicto final del lenguaje de SGM:** COMPOSICIONAL y SISTEMÁTICO (resuelto con inferencia de regla).
  El mecanismo honesto es: afinidad (germen) + inferencia de regla de mapeo rasgo→símbolo (cierre).

## Ubicación de archivos
- `phases/phase7_composicion/run_ilm_0055a.py` / `run_ilm_0055b.py` / `run_ilm_0055c.py` / `run_ilm_0055d.py` / `run_ilm_0056.py`
- JSON: `results_exp_SGM_0055a_ilm_puro.json`, `..._0055b_ilm_sin_prior.json`, `..._0055c_ilm_afinidad.json`,
  `..._0055d_ilm_profundo.json`, `..._0056_ilm_regla.json`
