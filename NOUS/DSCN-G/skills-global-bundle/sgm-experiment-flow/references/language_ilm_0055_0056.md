# ILM 0055–0056 — prior emergente de afinidad, inferencia de regla, y Gumbel-Softmax

Serie que AISLA variables UNA A UNA (Luciano: "vamos 1 por 1") sobre si el sustrato SGM
compone lenguaje, tras 0053 (HRR-celda = TopSim≈0, no lenguaje) y 0054b (ILM con bottleneck
da señal pero se estanca). Todos usan V=16 L=3, 24 referentes estructurados (region×distancia×tipo),
frac muestra 0.4, 3 seeds, TopSim de Spearman entre distancia-de-rasgos y distancia-de-mensaje.

## 0055a — prior de similitud INYECTADO (trampa potencial)
Aprendiz arranca code VACÍO, reconstruye de MUESTRA 40% del maestro (generación dura, no en vivo).
El sesgo "similares→señal similar" se inyecta a mano (overlap de rasgos → mismo mensaje).
Resultado: TopSim_full 0.30–0.40 SOSTENIDO en todas las generaciones. Confirma que el bottleneck
+ transmisión genera señal de estructura. PERO el prior fue hardcodeado → no cuenta como emergente.

## 0055b — SIN prior (control decisivo)
Mismo diseño pero el aprendiz NO usa sesgo: asigna msg nuevo aleatorio (hasta V) o reusa ciego.
Resultado: TopSim_full cae a 0.12–0.25, TopSim_unseen ~0 o NEGATIVO (−0.03..−0.09).
CONFIRMA: sin el sesgo de compresibilidad, HRR/bigrama NO compone. El bottleneck es
necesario pero NO suficiente (Kirby & Smith).

## 0055c — prior EMERGENTE de la AFINIDAD de SGM (cierra la duda de diseño)
Igual que 0055a PERO el sesgo de similitud se deriva de la AFINIDAD Eq.2 de SGM sobre los rasgos
de los referentes (no se inyecta). El aprendiz rellena no-vistos usando `affinity_similarity`
(ω de afinidad entre referentes que comparten rasgos). TopSim_full 0.30–0.42 SOSTENIDO.
HALLAZGO: el prior de compresibilidad NO es trampa si EMERGE del sustrato (afinidad que SGM ya
tiene = instinto/ADN legítimo). Composicionalidad DÉBIL pero real.

## 0055d — bottleneck más duro + 40 generaciones (plateau)
V=8 L=2 (64 combos para 24 referentes), 40 generaciones, sesgo por afinidad.
TopSim SE ESTANCA en ~0.30–0.37 (no sube a ~0.9). CONFIRMA gap fino: la afinidad AGRUPA por
rasgos pero NO INFERE reglas de combinación sistemática (lo que NN con Gumbel-Softmax sí hacen).

## 0056 — INFERENCIA DE REGLA (BANDERA ROJA 2026-08-04: regla INYECTADA, NO emergente)
El aprendiz INFERE el mapeo rasgo→símbolo de la MUESTRA y lo aplica sistemáticamente, dando
TopSim 0.86–1.00 (seed2/3 = 1.0). PERO al leer el script, la estructura (region→pos0, distancia→pos1,
tipo→pos2) está HARDCODEADA en `RuleLearner.infer_rule` (itera `reg_map[ra[0]][msg[0]]+=1`, etc.).
El aprendiz ya SABE buscar esa forma: el 1.0 es regla INYECTADA en el mecanismo del aprendiz,
MISMA falla que 0049d. Status en registry: ACLARACION_REQUERIDA (NO HALLAZGO_POSITIVO_FUERTE).
0056 y 0055a responden preguntas DISTINTAS:
  - 0055a = ¿emerge composición con aprendiz GENÉRICO? ~0.35, sí débil. Esa SÍ es evidencia honesta.
  - 0056 = ¿tiene el sustrato techo que impida composición plena SI se le da inferir la regla exacta?
          no, llega a 1.0. Pero la regla se la diste al aprendiz.
Citar el 1.0 de 0056 como "SGM compone pleno por emergencia" es el error de 0049d. Ver regla 5 y
ítem 12 de ANTI-PAPER-VISION en SKILL.md.

## 0056b — APRENDIZ GENÉRICO (contraste decisivo, 2026-08-04)
Mismo setup de 0056 (24 referentes, V=16 L=3, frac 0.4, 20 generaciones) PERO el aprendiz NO sabe
la estructura posicional: arranca code vacío, recibe muestra 40% del maestro, y rellena no-vistos
usando SOLO afinidad entre referentes (que sí emerge de SGM, no está inyectada). Status:
DECISIVO_NEGATIVO_CONTRASTE. Resultado: TopSim_full SOSTENIDO ~0.30–0.42 (seed1 0.388→0.300,
seed2 0.376→0.420, seed3 0.335→0.267). CONFIRMA que el 1.0 de 0056 venía de la regla inyectada:
el sustrato SGM compone DÉBILMENTE por afinidad (~0.35), no pleno sin estructura dada.
Evidencia honesta de composición emergente = 0055a / 0055c / 0056b (~0.35).

## Gumbel-Softmax vs HRR/bigrama (en criollo)
- Gumbel-Softmax (NN modernas): truco para elegir símbolos discretos y TODAVÍA entrenar con backprop
  (mezcla suave + ruido + temperatura). Canal estrecho + aprendiz que arranca de cero FUERZA compresión
  con reglas → llegan a ~0.9.
- HRR/bigrama (lo nuestro): HRR = vector opaco; bigrama = memoria estadística (no infiere regla).
  Por eso nos estancamos en 0.35: agrupa por afinidad pero no infiere regla.
- 0056 "demostró" composición plena sin GS, PERO era regla inyectada (ver bandera arriba). La lección
  honesta NO es "SGM compone pleno", sino "el sustrato compone débil por afinidad (~0.35); para
  sistematicidad plena el aprendiz debe inferir la regla SIN que se la des en el código".

## Regla de clase (para futuros claims de lenguaje en SGM)
1. ILM de Kirby exige: (a) bottleneck DURO de transmisión, (b) estructura en el espacio de
   referentes (rasgos, no ID opaco), (c) transmisión con pérdida entre generaciones.
2. El prior de compresibilidad debe EMERGERE del sustrato (afinidad), no inyectarse (0055a=trampa,
   0055c=legítimo). Si se inyecta, es hardcode y no cuenta.
3. Plateau en ~0.35 = germen composicional pero falta inferencia de regla.
4. NO citar TopSim alto de un aprendiz que conocía la estructura de mapeo como "composición emergente".
   Para afirmar emergencia, el aprendiz debe ser GENÉRICO (no saber la estructura posicional) y la
   estructura debe surgir de la transmisión (ver 0056b como control decisivo).
