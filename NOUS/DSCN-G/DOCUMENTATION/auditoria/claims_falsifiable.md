# Claims Verificados y Criterios de Falsificación

> ⚠️ **Auditado 2026-07-22, actualizado 2026-07-23 (Ronda 4).** Cada claim
> se re-corrió con el código corregido (bugs de guardado de resultados y
> de sincronía de Kuramoto arreglados — ver `AUDIT_NOTES.md`) a escala
> canónica (seeds=30, steps=2000; N-back 1–15, 40 trials). Ronda 4 agregó
> simulación real de maximalidad de T1, rediseño de C3, una definición
> propuesta (no aprobada) de Φ_proxy con su primer resultado, y un
> baseline de RNN vainilla — ver `AUDIT_NOTES_ROUND4.md` para el detalle
> completo. Los veredictos de abajo reflejan la corrida real, no
> versiones anteriores de este documento.

## Claims VERIFICADOS (se sostienen con la corrida real)

### Claim 2: ω Alignment Convergence — ✅ VERIFICADO

**Evidencia (re-verificada):** alignment = 1.0000 ± 0.0000 (mejor que el 0.9998 reclamado originalmente)

**Mecanismo:** Broadcast neuromodulatorio (Eq. 1) + reward = alignment(ω, ω_ideal)

**Predicción:** Los vectores ω convergen al target independientemente de la fase

**Criterio de falsificación:**
- Si mean_alignment_final < 1 - 2β, el teorema es falso
- Si ω no converge a ω_ideal después de 2000 steps

**Resultado real:** ✅ alignment = 1.0000, threshold (1−2β) = 0.60 — converge en los 30/30 seeds

### Claim 6a: N_ss* empírico del N-back — ✅ VERIFICADO

**Evidencia (re-verificada):** N_ss* = 9.50 ± 1.02 (10 seeds), valores [9,10,11,9,11,10,8,9,8,10]

Se reproduce casi exacto respecto de lo reclamado.

### Claim 6b: WM sin escalón abrupto — ✅ VERIFICADO (forma cualitativa), ⚠️ valores puntuales NO

**Evidencia (re-verificada):** máximo salto entre n-backs consecutivos = 0.75 (d', de 4-back a 5-back);
el resto de los saltos son ≤0.35. En ningún punto probado (1 a 15-back, y se
chequeó hasta 20-back) aparece un colapso tipo escalón.

**Pero:** los valores puntuales reclamados antes (d'(10-back)=3.12,
d'(15-back)=2.78) NO se reproducen. La curva real cae de 5.33 (1-back) a
~3.9 hacia el 5-back y **se aplana ahí** (3.89–3.95 hasta 20-back), en vez de
seguir bajando suavemente. La conclusión "no hay slots discretos con
escalón" se sostiene; la conclusión "degradación continua en todo el rango"
no es exacta — es "caída y luego meseta".

**Criterio de falsificación (sin cambios):**
- Si se observa escalón abrupto en d' (caída >2.0 en un solo step) → NO ocurrió
- Si d' cae a nivel de azar (≈0) en algún n_back < 15 → NO ocurrió (pero
  tampoco d' se acerca a 0 ni en 20-back, lo cual es en sí mismo un dato a
  discutir — ver nota metodológica sobre efecto de piso en README.md)

## Claims que NECESITAN CORRECCIÓN antes de citarse

### Claim 1: Homeostatic Fixed Point de T1 — ⚠️ CORREGIR

**Lo que decía antes:** "N_ss* = 9.5 ± 1.0 nodos" (esta cifra en realidad
pertenece al Claim 6a — el modelo de N-back, no T1)

**Evidencia real de T1 (re-verificada, 30 seeds, 2000 steps, θ_death=0.10):**
- N_init=4 → N_ss*=4.0±0.0
- N_init=50 → N_ss*=4.8±0.4
- N_init=200 → N_ss*=4.2±0.5

**Mecanismo:** Competencia por vitalidad (Eq. 5) + pruning adaptativo — esto sigue siendo correcto

**Criterio de falsificación:**
- Si N_ss* varía significativamente (>20%) con N_init → no ocurre (4.0/4.8/4.2 son consistentes)
- Si N_ss* > 1/θ_death (=10) → no ocurre, cota se cumple siempre

**Sub-claim de maximalidad (iii):** ✅ **VERIFICADO con simulación real
(2026-07-23, Ronda 4)**. El test original (`rho_approx = K/n_test`, una
fórmula) fue reemplazado por una simulación real: converger a N*, forzar
la población a N*+1 con un nodo nuevo, y correr la dinámica con poda
activa para ver si se poda de vuelta. **El resultado depende del
protocolo de inyección** — con el nodo nuevo arrancando en vitalidad
plena (1.0) sobrevive en la mayoría de los casos (3-77% podado de vuelta
según N_init, no sostiene maximalidad); con el nodo arrancando justo en
el umbral θ_death (la inyección correcta, sin ventaja injusta de
arranque) se poda de vuelta al toque en el **100%** de los seeds, en las
3 condiciones de N_init probadas. Con el protocolo correcto, la sub-claim
se sostiene: N* no admite un nodo extra marginal como estado estable. Ver
`AUDIT_NOTES_ROUND4.md` §2 para el detalle completo, incluida una
corrección de diseño propia que se documenta ahí sin esconder.

### Claim 3: Phase Consensus via Kuramoto (T3) — ⚠️ CORREGIR

**Lo que decía antes:** "90% consensus rate (27/30), 83% unimodal, 7% bimodal"

**Evidencia real (re-verificada):** 30/30 = 100% por el criterio que usa el
código, pero desglosado: 23/30 cumplen el criterio real del teorema (R≥0.9,
"unimodal"), 7/30 solo pasan una rama de respaldo más laxa (R≥0.5,
"weak_unimodal") que el código cuenta igual como "consenso" aunque no cumple
la definición que el teorema mismo establece. **0/30 casos bimodales** (no
7% como se decía).

**Implicación:** o se ajusta la definición de "consenso" en el texto del
paper para incluir explícitamente el criterio laxo (y se explica por qué),
o se reporta la cifra estricta (23/30 = 76.7%) como el verdadero consensus
rate y se elimina la mención a casos bimodales, que no aparecieron.

### Claim 6c: valores puntuales de d' — ⚠️ CORREGIR

d'(10-back) real = 3.92 (no 3.12); d'(15-back) real = 3.90 (no 2.78). Ver
Claim 6b arriba para la forma completa de la curva.

## Claims que NO SE SOSTIENEN — requieren rediseño o retirarse

### Claim 5: Phase Hijacking (C3) — ❌ NO VERIFICADO

**Lo que decía antes:** "ΔPLV = -0.46 (100% de triggers)"

**Evidencia real (re-verificada, 30 seeds, 2000 steps, código con el fix de
sincronía de Kuramoto):**
- 2237 hijack triggers (3.73% de los steps — no 9.37%)
- Solo **20/2237 triggers (0.9%)** muestran ΔPLV < −0.3 (no 100%)
- Mean ΔPLV = **−0.007 ± 0.061** (no −0.462 ± 0.089 — prácticamente cero)
- Max ΔPLV (más negativo) = −0.918 (hay casos extremos, pero no son la norma)

**Mecanismo declarado:** sincronización patológica cuando V_root > θ_emerg

**Criterio de falsificación (sin cambios):**
- Si hijacking no ocurre (0 triggers) → sí ocurre, pero...
- Si ΔPLV no muestra aumento de sincronización (>0.3) en la gran mayoría de
  los casos → **esto es lo que pasa**: en promedio, el mecanismo tal como
  está implementado NO produce el aumento de phase-locking que la claim
  describe.

**Hipótesis sobre la causa (no verificada por separado):** T1 converge a
~4-5 nodos activos con estos parámetros; `plv_intra_group()` mide consenso
sobre `nodes_active[1:]` (todos menos la raíz), es decir 3-4 nodos — muy
poca población para que el pull de hijacking (15 steps, η=0.15) produzca una
sincronización medible y estable frente al ruido. Hay tensión directa con el
propio equilibrio de T1.

**Recomendación:** no citar esta claim como verificada **a los parámetros
de diseño originales** (θ_death=0.10, hijack_steps=15, η_hijack=0.15) —
ahí el veredicto de arriba sigue sin cambios.

**Actualización (2026-07-23, Ronda 4) — rediseño del experimento:** se
confirmó la hipótesis de la causa (población de seguidores insuficiente:
`plv_intra_group()` mide consenso sobre `nodes_active[1:]`, es decir,
todos los nodos activos MENOS la raíz — con N*≈4-5 eso son 3-4 nodos). Se
rediseñó bajando θ_death (más nodos activos sobreviven) y aumentando
`hijack_steps`/`η_hijack`. Resultado: el rise_rate sube monótonamente de
0.7% (línea base) a **30.2%** en la config más agresiva probada
(θ_death=0.01 → grupo de ~28 seguidores, hijack_steps=150, η=0.80). Es una
mejora real de ~40x, pero **sigue lejos de "la norma"** que reclamaba el
paper original (100%). Además, esos parámetros ya están lejos de los
valores de diseño originales — hijack_steps=150 es 10x el valor con el
que se pensó el mecanismo. Ver `AUDIT_NOTES_ROUND4.md` §1 para la tabla
completa del barrido. **Veredicto sin cambios: sigue sin poder
citarse como verificada**, pero ahora hay evidencia real (no solo
hipótesis) de que el mecanismo responde en la dirección predicha bajo
condiciones más favorables — útil para decidir si vale la pena seguir
explorando parámetros o retirar la claim del todo.

**Actualización (2026-07-23/24, Ronda 5) — reforzar el pull individual
(hub_boost) no mueve la métrica:** se probó si un privilegio estructural
del root ("hub talámico", `hub_boost` escalando `η_hijack` hasta 5x, tope
1.0) subía el rise_rate más allá del 0.7%/30.2% de Ronda 4. Resultado:
**sin efecto medible, exactamente igual (0.7% y 30.2%) en hub_boost=1,
2 y 5**. No es el mismo bug de ubicación de Ronda 4 (esta vez el boost sí
actúa sobre `_apply_hijack_pull`, el mecanismo correcto — verificado con
smoke test) — es saturación: con solo 3-4 seguidores, `plv_intra_group()`
ya toca R≈1.0 a los 2-3 pasos de iniciado el hijack incluso sin boost, así
que no queda margen donde un pull más fuerte pueda mostrarse en la
métrica medida al final de la ventana. Refuerza el diagnóstico de Ronda 4
(el cuello de botella es población + duración, no fuerza de pull) y
añade que la fuerza del pull, aislada, es una palanca sin efecto
demostrado. Ver `AUDIT_NOTES_ROUND5.md` §2.

**Decisión (2026-07-24, Ronda 6) — analogía "tálamo/hub_boost" RETIRADA:**
Delorien decidió retirar la analogía de privilegio estructural talámico
(`hub_boost`, `thalamic_model.py`) del paper. No es solo que no mostró
efecto — Ronda 5 explicó por qué no puede mostrarlo dado el diseño actual
de la métrica (techo de saturación de `plv_intra_group()` a 2-3 pasos de
iniciado el hijack). El código (`thalamic_model.py`,
`verify_hub_boost_fix.py`) se conserva en el repositorio como evidencia
del intento y su resultado nulo, pero no debe citarse en el paper como
mecanismo ni como analogía cualitativa. Lo que sí se mantiene y se
desarrolla (ver Claim 7 más abajo) es la distinción arrastre-vs-
integración medida por Φ_proxy_TE, que es independiente de `hub_boost` y
no depende de privilegio estructural del root — es un patrón que ya
estaba presente en `DSCN_G_v3` sin modificar.

### Claim 11b: Comparación contra recurrente simple (N-back) — ✅ VERIFICADO (2026-07-23, Ronda 4)

**Pedido explícito de `REVIEW_RECOMMENDATIONS.md`** ("Incluir comparaciones
contra baselines simples... Comparación contra modelos recurrentes
simples").

**Evidencia:** Elman RNN vainilla (tanh, sin gating), entrenado con BPTT
sobre las mismas 40 seeds de test que DSCN-G v6, promediado sobre 3
semillas de entrenamiento:

| n_back | DSCN-G v6 (d') | RNN vainilla (d') |
|---|---|---|
| 1 | 5.39 | 4.63±1.68 |
| 3 | 3.18 | 1.43±0.71 |
| 5 | 1.29 | 0.74±0.54 |
| 7 | 0.98 | 0.01±0.02 |
| 10 | 0.97 | −0.01±0.01 |
| 20 | 0.80 | 0.00±0.02 |

El RNN compite en n_back bajo pero colapsa a nivel de azar desde n_back≈7
(vanishing gradients, esperable de la literatura). DSCN-G mantiene
d'≈0.8-1.0 incluso en 20-back.

**Limitación a declarar:** esto es contra un RNN *vainilla*, no LSTM/GRU
(con gating) ni Transformer (sin el problema de vanishing gradients).
Comparación parcial, no la más fuerte posible — ver
`AUDIT_NOTES_ROUND4.md` §4.

## Claims PENDIENTES de verificación (sin cambios)

### Claim 7: Φ_proxy Scaling O(log N)

**Estado:** ⚠️ **EVIDENCIA PRELIMINAR, NO CONCLUYENTE (2026-07-23, Ronda 4)**

**Aviso importante:** Φ_proxy nunca tuvo una fórmula definida en ningún
documento de este paquete — solo esta predicción, sin operacionalización.
La definición usada en Ronda 4 (información mutua gaussiana entre dos
mitades del sistema, embebiendo cada fase φ en (cos,sin) por su
circularidad) es una **propuesta**, no algo previamente acordado —
necesita revisión y aprobación antes de citarse como verificado, sea cual
sea el resultado.

**Predicción:** Φ_proxy escala logarítmicamente con N

**Corrección metodológica:** el criterio de falsificación original de
abajo sugiere barrer N_init. Eso no sirve — T1 ya demostró que N_init casi
no mueve N* (homeostasis). Lo que sí lo mueve es θ_death (T1: N*≤1/θ_death).
Ronda 4 barrió θ_death, no N_init.

**Resultado real (seeds=10, steps=2000, ventana=300, definición propuesta arriba):**

| θ_death | N* real | Φ_proxy |
|---|---|---|
| 0.20 | 2.70±0.46 | 0.39±0.31 |
| 0.10 | 4.60±0.49 | 12.35±0.32 |
| 0.05 | 8.80±0.40 | 12.86±1.05 |
| 0.02 | 18.00±0.63 | 9.49±3.22 |
| 0.01 | 29.71±0.88 | 9.77±4.44 |

R² vs log(N) = 0.22, R² vs N = 0.07 — **ninguno de los dos ajusta bien**.
La curva sube fuerte de N*=2.7 a 4.6, hace meseta hasta N*=8.8, y **cae**
un poco hacia N*=18-30 en vez de seguir subiendo. Con esta definición, la
evidencia disponible apunta **en contra** de O(log N), aunque con solo 5
puntos válidos y desviaciones grandes en el extremo alto no alcanza para
ser concluyente. Ver `AUDIT_NOTES_ROUND4.md` §3 para el detalle y las
limitaciones (varianza alta en N* grande, ventana quizás insuficiente
para ese régimen).

**Criterio de falsificación:**
- Si Φ_proxy escala linealmente (O(N)) o peor
- Si no hay correlación clara entre Φ_proxy y N

**Experimento propuesto (original, sin cambios):**
- Medir Φ_proxy para N = [10, 50, 100, 200, 500]
- Plot Φ_proxy vs log(N)
- Verificar linealidad

**Actualización (2026-07-23/24, Ronda 5) — segunda definición candidata,
resultados opuestos a la MI cruda:** no se repitió el barrido vs. N de
arriba, pero se probó una definición alternativa (partición root/periferia
en vez de mitades arbitrarias, transfer entropy de Geweke tomando el
mínimo de las dos direcciones de flujo en vez de MI cruda — "TE-bottleneck",
pensada para distinguir arrastre de integración genuina) comparando ventana
pre-hijack vs. durante-hijack en las 4 configuraciones de C3. Resultado
consistente en las 4: la MI cruda **sube** durante el hijack (replica y
refuerza el hallazgo de Ronda 4), pero el TE-bottleneck **baja** en las 4
— compatible con la lectura de que lo que aumenta es arrastre (root dicta
la fase de la periferia), no integración bidireccional genuina. Ninguna de
las dos definiciones (MI cruda de Ronda 4, TE-bottleneck de Ronda 5) fue
aprobada — siguen siendo propuestas. Queda pendiente repetir el barrido
Φ_proxy-vs-N (la pregunta original de esta claim, escalado O(log N)) con
la métrica TE-bottleneck en vez de MI cruda. Ver `AUDIT_NOTES_ROUND5.md` §1.

**Actualización (2026-07-24, Ronda 6) — TE-bottleneck aprobada tras
prueba de robustez; barrido O(log N) repetido, resultado sigue sin
soportar la predicción:**

*Robustez (previo a aprobar):* se probó la métrica TE-bottleneck (P0,
root/periferia) contra dos particiones adicionales — P1, un control
negativo (periferia partida en dos mitades SIN la raíz) y P2 (raíz contra
un solo seguidor, sin agregación) — y dos órdenes de VAR (lag=1, el
usado en Ronda 5, y lag=2). P0 y P2 reproducen el mismo patrón (MI sube /
TE baja) en ambos lags y en las dos configuraciones de C3 (baseline y
rediseño). El control P1 **no** reproduce el patrón — va en dirección
opuesta en baseline_R4 (MI baja, TE sube) — lo cual es la evidencia de
robustez que se buscaba: el colapso de integración es específico del rol
de la raíz como driver, no un artefacto de partir el sistema en dos
mitades cualquiera durante alta sincronía. Caveat: en P1 el TE_baseline
da 0.0000±0.0000 en casi todos los casos, probablemente un artefacto
numérico del guard `du>dr` con mitades simétricas — no invalida la
lectura direccional, pero esos valores absolutos no son confiables. Con
esta evidencia, **Delorien aprobó formalmente la definición TE-bottleneck
(P0, lag=1) como la definición operativa de Φ_proxy**, reemplazando la MI
cruda de Ronda 4. Ver `AUDIT_NOTES_ROUND6.md` §1 para el detalle completo
por partición/lag.

*Barrido O(log N) con la métrica ya aprobada (seeds=10, steps=2000,
ventana=300 estacionaria, sin hijack — mismos θ_death que Ronda 4 para
comparabilidad directa):*

| θ_death | N* real | Φ_proxy_TE |
|---|---|---|
| 0.50 | 1.00±0.00 | sin corridas válidas (N*<2, no hay periferia) |
| 0.20 | 2.70±0.46 | 0.0118±0.0076 (7/10 seeds válidas) |
| 0.10 | 4.60±0.49 | 0.0217±0.0136 |
| 0.05 | 8.80±0.40 | 0.0118±0.0081 |
| 0.02 | 18.00±0.63 | 0.0101±0.0078 |
| 0.01 | 29.40±0.92 | 0.0086±0.0080 |

R² vs log(N) = 0.337, R² vs N = 0.396 — **ninguno de los dos ajusta bien
tampoco con esta métrica**. A diferencia de la MI cruda de Ronda 4 (que
al menos mostraba una subida clara de N*=2.7 a 4.6), el TE-bottleneck en
ventana estacionaria (sin hijack) se mantiene prácticamente plano y
dentro del ruido (~0.01-0.02) en todo el rango de N* probado (2.7 a
29.4) — la desviación estándar es del mismo orden que la media en varios
puntos. **Lectura honesta: con la métrica ya aprobada, la predicción
O(log N) de Claim 7 sigue sin sostenerse — y esta vez ni siquiera hay una
tendencia visible a simple vista, a diferencia del resultado de Ronda 4.**
Esto es consistente con lo que ya se sabía de Ronda 5: en ausencia de
hijack, la raíz no tiene ventaja estructural sobre la periferia (por eso
retiramos `hub_boost`), así que no hay razón mecánica fuerte para esperar
que la integración root-periferia escale con N en estado estacionario —
el fenómeno de arrastre-vs-integración que sí es robusto (más arriba)
es específicamente un efecto del hijack, no del tamaño del sistema en
reposo. Ver `AUDIT_NOTES_ROUND6.md` §2.

**Veredicto actualizado:** Claim 7 (O(log N)) sigue sin poder citarse
como verificada, ahora con dos definiciones independientes (MI cruda,
TE-bottleneck) que no la sostienen. La definición TE-bottleneck en sí
misma queda aprobada y utilizable para otras afirmaciones del paper
(la distinción arrastre-vs-integración durante hijack), pero no rescata
la predicción de escalado logarítmico. Recomendación: o se retira la
predicción O(log N) del paper, o se reformula la pregunta (¿escala algo
más, como la MI cruda que sí mostró estructura no-trivial, aunque
tampoco logarítmica?) — pero no como estaba planteada originalmente.

### Claim 8: Validación Experimental EEG/fMRI

**Estado:** ❌ PENDIENTE (future work, sin cambios)

(predicciones EEG/fMRI sin cambios respecto de la versión anterior de este documento — no dependen del código auditado)

## Claims ESPECULATIVOS (sin cambios)

### Claim 9: DSCN-G como NCC Formalmente Completo — ⚠️ ESPECULATIVO

**Posición honesta:**
- ✅ Podemos claimar: "DSCN-G implementa mecanismos que correlacionan con consciencia"
- ❌ NO podemos claimar: "DSCN-G es consciente" o "resuelve el hard problem"

### Claim 10: Drug Discovery Connection — ⚠️ ESPECULATIVO

**Posición honesta:**
- ✅ Podemos claimar: "DSCN-G encuentra análogos con pIC50 predicho X"
- ❌ NO podemos claimar: "DSCN-G descubre fármacos efectivos"

## Resumen de honestidad epistémica (actualizado 2026-07-23, Ronda 4)

### Lo que PODEMOS claimar (VERIFICADO con la corrida real)

1. ✅ ω alignment convergence (alignment = 1.0000)
2. ✅ N_ss* empírico del N-back v6 = 9.50 ± 1.02 nodos (occurrence-aware,
   Ronda 3 — reemplaza el número de v5)
3. ✅ WM sin escalón abrupto (forma cualitativa, v6: caída máxima en un
   paso = 1.69 < 2.0, margen angosto pero real)
4. ✅ T1: cota universal (N_ss* ≤ 1/θ_death) y condición de punto fijo
   (ρ_eff ≥ N·θ²)
5. ✅ T1: sub-claim de maximalidad, con simulación real e inyección al
   umbral (Ronda 4) — 100% podado de vuelta en las 3 condiciones
6. ✅ Comparación contra RNN vainilla (Ronda 4) — DSCN-G retiene
   información en dependencias donde el RNN colapsa a azar

### Lo que hay que CORREGIR antes de citar

7. ⚠️ N_ss* de T1 es ~4-5, no ~9-10 (ese número es del N-back, no de T1)
8. ⚠️ T3: 100%/0% con el criterio del código (no 90%/7% bimodal) — y el
   criterio mismo es más laxo que la definición del teorema; el número
   riguroso es 23/30 = 76.7%, no 30/30
9. ⚠️ d'(10-back)=0.97, d'(15-back)=0.82 con v6 (no los números de v5) —
   la curva cae y se aplana con un piso residual, no sigue el patrón
   anterior

### Lo que NO SE SOSTIENE (a los parámetros de diseño originales)

10. ❌ C3 (phase hijacking) a θ_death=0.10/hijack_steps=15/η=0.15 — ΔPLV
    medio ≈ 0, no −0.46; 0.7% de triggers muestran el efecto, no 100%.
    Rediseñado en Ronda 4: sube a 30.2% con población/pull mucho mayores,
    pero sigue sin ser "la norma" — ver Claim 5.

### Evidencia preliminar, no concluyente

11. ⚠️ Φ_proxy scaling (Claim 7) — definición propuesta sin aprobar; con
    esa definición, los datos NO soportan O(log N) con confianza (R²
    bajo en ambos ajustes, curva no monótona)

### Lo que NO PODEMOS claimar (sin cambios)

12. ❌ "DSCN-G resuelve el hard problem" (explícitamente NO)
13. ❌ "Supera a todos los modelos" (comparamos con modelos de slots y un
    RNN vainilla — falta LSTM/GRU/Transformer)
14. ❌ Validación experimental (EEG/fMRI) — future work
15. ❌ "DSCN-G es consciente" (solo NCC)
16. ❌ "DSCN-G descubre fármacos" (solo predice pIC50)

## Principios de honestidad epistémica

1. **Separar VERIFIED de HYPOTHESIZED de SPECULATED**
2. **Cada claim debe tener criterio de falsificación**
3. **Declarar limitaciones explícitamente**
4. **No overclaimar (evitar "demuestra", "prueba", "resuelve")**
5. **Usar lenguaje preciso ("verifica computacionalmente", "sugiere", "es consistente con")**
6. **(Nuevo, 2026-07-22) Antes de marcar algo "✅ VERIFICADO", correr el código y confrontar los números — no basta con que el mecanismo esté bien descrito en prosa.**

## Analogías Biológicas (USAR CON CUIDADO) — sin cambios

### Uso apropiado

- ✅ "η_kura dinámico es análogo a acetilcolina/noradrenalina (atención/arousal)"
- ✅ "Hijacking (C3) es análogo a epilepsia focal / GNW ignition" — **con la
  salvedad de que, a estos parámetros, el modelo no reproduce el efecto que
  la analogía describe (Claim 5)**
- ✅ "Homeostasis es análoga a pruning sináptico + vitalidad neuronal"

### Uso inapropiado

- ❌ "η_kura ES acetilcolina"
- ❌ "Hijacking ES epilepsia"
- ❌ "DSCN-G ES un cerebro"

**Regla:** Las analogías son herramientas pedagógicas, no claims de identidad.

## Conclusión (actualizada, Ronda 4 — 2026-07-23)

DSCN-G v3 tiene **6 claims que se sostienen** con la corrida real (T2,
N_ss* del N-back v6, forma cualitativa de WM sin escalón, la cota/punto-
fijo de T1, la maximalidad de T1 con simulación real, y la comparación
contra RNN vainilla), **3 que necesitan corrección de números** antes de
publicarse (N_ss* de T1, desglose de T3, valores puntuales de d'), **1
que no se sostiene a los parámetros originales pero mejora sustancialmente
con rediseño sin llegar a "la norma"** (C3), y **1 con evidencia
preliminar no concluyente y una definición todavía sin aprobar**
(Φ_proxy). Ver `AUDIT_NOTES.md`, `AUDIT_NOTES_ROUND2.md`,
`AUDIT_NOTES_ROUND3.md` y `AUDIT_NOTES_ROUND4.md` para el detalle completo
de cada ronda.

**Per Aspera, Ad Astra.** 🚀
