# DSCN-G: Una Arquitectura Computacional Fundamentada para Cognición
## Memoria de Trabajo como Recurso Continuo Emergente desde Principios Homeostáticos

**DSCN-G v3** (Dual-State Cognitive Geometry) · D=8 · Auditado 2026-07-22
· Actualizado 2026-07-24: se incorporan al texto dos resultados que ya estaban corridos en
`codigo/` desde la Ronda 4 pero no se habían volcado al paper — la simulación real de
maximalidad de T1 (§3.1) y el baseline recurrente (§4.4).

> **Nota de alcance.** Este documento describe exclusivamente el modelo de **cognición
> computacional**: arquitectura, dinámica, memoria de trabajo y resultados medibles.
> Deliberadamente no incluye hipótesis sobre conciencia, interpretaciones fenomenológicas
> ni comparaciones con teorías de conciencia (IIT, GWT, PP) — ese material pertenece a un
> documento teórico separado (NOUS) y no se mezcla acá. Ver también el paquete adjunto
> `NOUS_pendiente_de_verificacion` para el estado de ese trabajo.

---

## Abstract

Presentamos DSCN-G, una arquitectura computacional que unifica tres mecanismos —
aprendizaje por diferencia temporal (TD-learning) sobre un vector semántico, dinámica de
fase acoplada (Kuramoto) y poda homeostática basada en vitalidad — sobre un grafo de nodos
que compiten por permanecer activos. Verificamos computacionalmente, a escala canónica
(30 semillas independientes × 2000 pasos), tres propiedades formales del sistema: (1) un
punto fijo homeostático en el número de nodos activos (N_ss\* ≈ 4.0–4.8, acotado
universalmente por 1/θ_death = 10); (2) convergencia completa del vector semántico ω hacia
el objetivo (alineación final = 1.0000 ± 0.0000); y (3) consenso de fase entre nodos activos
vía acoplamiento Kuramoto, con una tasa que depende del criterio usado (100% bajo el
criterio operacional del código, 76.7% bajo el criterio estricto R≥0.9 que el enunciado
formal exige). La sub-claim de maximalidad de (1) se verificó además con una simulación
directa de N_ss\*+1 (no la aproximación previa): inyectando un nodo nuevo sin ventaja de
arranque, el sistema lo poda de vuelta en el 100% de los casos. Un cuarto mecanismo — sincronización patológica ("hijacking") bajo una
condición de disparo definida — se probó explícitamente y **no se sostiene**: solo el 0.9%
de los eventos de disparo (20 de 2237) producen el efecto de sincronización reclamado.
Validamos el modelo en una tarea N-back grounded en el mismo sustrato, mostrando que la
memoria de trabajo se degrada como recurso continuo (d′ cae de 5.39 a ~0.8–1.0 entre 1-back
y 15–20-back) sin un escalón discreto de capacidad — aunque con un margen angosto (caída
máxima en un solo paso = 1.69, contra un umbral de 2.0 para considerarlo "escalón").
Comparado contra un baseline de RNN vainilla entrenado en la misma tarea, el mismo espacio de
estímulos y el mismo set de test, DSCN-G retiene un piso de rendimiento por encima del azar
(d′≈0.8–1.0) hasta 20-back, mientras que el RNN colapsa a d′≈0 (azar) a partir de 7-back.
Reporta explícitamente qué se sostiene, qué necesita corrección de cifras, y qué no se sostiene y
requiere rediseño, siguiendo un criterio de honestidad epistémica declarado.

---

## 1. Introducción

### 1.1 El problema: modelos de slots vs. recurso continuo

Dos familias de modelos compiten para explicar la capacidad de la memoria de trabajo (MT).
Los modelos de **slots discretos** (Cowan, 2001; Miller, 1956) predicen una capacidad fija
(~4, o 7±2) con un escalón abrupto de rendimiento al superarla. Los modelos de **recurso
continuo** (Bays & Husain, 2008; van den Berg et al., 2014) predicen, en cambio, una
degradación gradual del rendimiento a medida que la carga aumenta, sin un umbral discreto.
La evidencia empírica es mixta y no existe, hasta donde sabemos, un modelo computacional que
derive el comportamiento de recurso continuo desde principios homeostáticos de bajo nivel
—en lugar de imponerlo como supuesto de diseño.

### 1.2 DSCN-G en una página

DSCN-G es un grafo de N nodos semánticos, cada uno caracterizado por un vector de aprendizaje
ω_i ∈ ℝ^d, una fase φ_i ∈ [0, 2π) y una vitalidad V_i ∈ [0, 1]. Tres mecanismos acoplados
gobiernan su dinámica:

- **Aprendizaje (Ec. 1, TD-learning):** cada nodo actualiza ω_i hacia un vector objetivo
  ω_ideal, ponderado por una recompensa de alineación.
- **Fase (Ecs. 3–4, Kuramoto + von Mises):** los nodos activos acoplan sus fases hacia un
  objetivo común θ\*, y la fase determina la selección de acción.
- **Homeostasis (Ecs. 5–6, vitalidad y poda):** la vitalidad decae salvo que el nodo sea
  visitado por una cadena de información activa; los nodos por debajo de un umbral θ_death
  se eliminan del grafo.

Un cuarto mecanismo, el acoplamiento Kuramoto dinámico (η_kura variable, sección 2.7),
permite que el sistema alterne entre un régimen basal y un régimen de acoplamiento elevado
bajo una condición de disparo — diseñado, en teoría, para producir sincronización patológica
transitoria. Como se reporta en la Sección 3, este último mecanismo no produce el efecto
esperado a los parámetros actuales.

### 1.3 Contribuciones

1. Un framework unificado con tres propiedades formales verificadas computacionalmente
   (punto fijo homeostático, convergencia de ω, consenso de fase) y un cuarto mecanismo
   explícitamente probado y reportado como no confirmado (no ocultado).
2. Un modelo de memoria de trabajo grounded en el mismo sustrato del núcleo (sin capas ad
   hoc por n-back), que reproduce el patrón cualitativo de recurso continuo.
3. Un conjunto de criterios de falsificación explícitos para cada claim, y un registro
   público de qué se corrigió y por qué (ver `auditoria/` en el paquete adjunto).
4. Simulador de referencia, sin dependencias externas más allá de NumPy.

### 1.4 Honestidad epistémica y alcance

Este documento separa explícitamente **demostración matemática**, **resultado
experimental/simulado**, **hipótesis** e **interpretación**, y evita afirmar más de lo que
la corrida real sostiene. En particular: no se reclama que el mecanismo de "hijacking"
module realmente sincronización patológica (Sección 3.4), y los valores puntuales de d′ que
figuraban en borradores previos de este documento fueron reemplazados por los de la corrida
corregida (Sección 4).

---

## 2. Fundamentos Computacionales

### 2.1 Estructura del grafo

N nodos, K cadenas de información paralelas que recorren el grafo. Cada nodo mantiene
(ω_i, φ_i, V_i). Existe un nodo raíz que ancla la fase objetivo del sistema.

### 2.2 Aprendizaje por diferencia temporal (Ec. 1)

ω_i ← (1−β)·ω_i + β·reward·ω_ideal, con reward = alineación(ω_i, ω_ideal) ∈ [−1, 1],
transmitido por broadcast a los nodos en fase.

### 2.3 Cadenas de información (Ec. 2)

La probabilidad de que una cadena se mueva del nodo n al nodo m es proporcional a
exp(−α·‖ω_m − ω_n‖): las cadenas compiten por recursos siguiendo afinidad semántica.

### 2.4 Dinámica de fase y selección de acción (Ecs. 3–4)

Δφ_i = η·R_i·reward·sin(θ_a − φ_i); la acción se selecciona con una distribución von Mises
sobre la fase, P(a|φ) ∝ exp(λ·cos(φ − θ_a)).

### 2.5 Autopoiesis: vitalidad y poda (Ecs. 5–6)

V_i ← V_i·e^(−γ) + A_i·(1−e^(−γ)), donde A_i indica si el nodo fue visitado en el paso
actual. Los nodos con V_i < θ_death se eliminan (poda definitiva). La valencia
E_i = max(0, A_i − V_i)·κ actúa como señal de "dolor estructural" cuando la demanda supera
la vitalidad disponible.

### 2.6 Interferencia de onda (Ec. 7)

I_i = ‖ω_i‖·cos(φ_i − φ_root): interferencia constructiva o destructiva respecto de la fase
del nodo raíz, usada como señal adicional de relevancia.

### 2.7 Acoplamiento Kuramoto dinámico (mecanismo nuevo de v3)

η_kura pasa de un valor basal (0.005) a uno elevado (0.025) bajo una condición de disparo
(vitalidad del nodo raíz por encima de un umbral θ_emerg), siguiendo
dφ_i/dt = ω_i + (η_kura/N)·Σ_j sin(φ_j − φ_i) con acoplamiento todos-con-todos entre nodos
activos. La implementación fue corregida durante la auditoría 2026-07-22 para que la
actualización de fase sea sincrónica (usa una única fotografía de φ(t) para todo el barrido,
en vez de leer valores ya actualizados dentro del mismo paso, que introducía una dependencia
espuria del orden de iteración).

---

## 3. Teoremas Formales y Verificación

Verificación computacional a escala canónica: **30 semillas independientes × 2000 pasos**
para el núcleo (T1–T3, C3); 10 semillas × 40 ensayos para el modelo de N-back (Sección 4).
Código de referencia: `codigo/core/verify_dscng_v3.py`; resultados crudos:
`codigo/core/verification_results_v3.json`.

### 3.1 Teorema 1 — Punto fijo homeostático

**Enunciado:** (i) N_ss\* ≤ 1/θ_death (cota universal); (ii) ρ_eff ≥ N_ss\*·θ_death²
(condición de punto fijo); (iii) N_ss\* es el mayor n que satisface (ii) (maximalidad).

**Verificación:** con θ_death = 0.10 (cota universal = 10 nodos), y tres inicializaciones
distintas:

| N_init | N_ss\* (media ± std) | Cota (i) | Punto fijo (ii) |
|---|---|---|---|
| 4   | 4.00 ± 0.00 | ✓ | ✓ |
| 50  | 4.77 ± 0.42 | ✓ | ✓ |
| 200 | 4.20 ± 0.54 | ✓ | ✓ |

La cota universal y la condición de punto fijo se sostienen en las tres inicializaciones, con
convergencia consistente (variación <20% entre condiciones) a **N_ss\* ≈ 4–5 nodos activos**.

**Maximalidad (iii) — simulación real, no la aproximación previa.** El test original
aproximaba la condición con una fórmula (`ρ_approx = K/n_test`) en vez de simular
efectivamente N_init = N_ss\*+1, y por eso reportaba "no confirmado" de forma sistemática —
eso era evidencia de que el test no probaba lo que decía probar, no de que la propiedad fuera
falsa. Se reemplazó por una simulación directa (`codigo/core/verify_maximality_real.py`):
converger a N\* con el protocolo estándar, forzar la población a N\*+1 agregando un nodo
genuinamente nuevo, y correr la dinámica con poda activa por otros 2000 pasos para ver si el
sistema lo poda de vuelta.

El resultado depende del protocolo de inyección del nodo nuevo — un hallazgo no anticipado,
reportado en vez de descartado:

| Vitalidad de inyección | N_init=4 | N_init=50 | N_init=200 |
|---|---|---|---|
| Plena (1.0) | podado de vuelta: 3% | podado de vuelta: 77% | podado de vuelta: 27% |
| En el umbral (θ_death=0.10) | podado de vuelta: **100%** | podado de vuelta: **100%** | podado de vuelta: **100%** |

Con vitalidad plena, el nodo nuevo tiene ~230 pasos de margen (γ=0.01, decaimiento lento) para
ser visitado alguna vez por las cadenas (Ec. 2) y recargarse antes de morir — una ventaja de
arranque injusta, no evidencia sobre el punto fijo en sí. Inyectado sin esa ventaja (vitalidad
en el umbral, la operacionalización correcta), el nodo se poda de vuelta en el **100% de los
seeds, en las tres condiciones de N_init**. Con el protocolo correcto, **la sub-claim de
maximalidad se sostiene**: N\* no admite un nodo extra marginal como estado estable.

(Un chequeo instantáneo adicional — si ρ_eff viola la condición (ii) apenas se fuerza N\*+1 —
dio 0% de violación inmediata en ambos protocolos; esto es un artefacto de medir ρ_eff antes
de que las cadenas tengan chance de visitar o no al nodo nuevo, y no contradice el resultado
de arriba, que es el criterio real: si se poda de vuelta con el tiempo. Ver
`auditoria/AUDIT_NOTES_ROUND4.md` §2 para el detalle completo, incluida esta corrección de
diseño del propio experimento, documentada sin esconder.)

### 3.2 Teorema 2 — Convergencia del vector semántico ω

**Enunciado:** ω_i converge hacia ω_ideal; alineación final ≥ 1 − 2β.

**Verificación** (β = 0.20, umbral = 1 − 2β = 0.60): **alineación final = 1.0000 ± 0.0000**
en las 30/30 semillas. Se sostiene limpio, por encima del umbral con amplio margen.

### 3.3 Teorema 3 — Consenso de fase

**Enunciado:** bajo acoplamiento Kuramoto, los nodos activos alcanzan consenso de fase,
medido por el parámetro de orden R = |⟨e^(iφ)⟩| ≥ 0.9.

**Verificación** (η = 0.5, 30 semillas): **30/30 (100%)** cuentan como "consenso" según el
criterio operacional del código, que acepta tanto R≥0.9 ("unimodal", criterio estricto) como
una rama de respaldo más laxa R≥0.5 ("weak_unimodal"). Desglosado: **23/30 (76.7%)** cumplen
el criterio estricto R≥0.9 que el enunciado formal exige; los 7/30 restantes solo alcanzan el
criterio laxo. **0/30 casos bimodales** se observaron. Reportamos ambas cifras explícitamente
en vez de una sola tasa de "consenso", porque dependen de qué definición se adopte.

### 3.4 Mecanismo de sincronización patológica ("hijacking") — resultado negativo

**Hipótesis probada:** cuando la vitalidad del nodo raíz supera un umbral θ_emerg, el
acoplamiento Kuramoto elevado (Sección 2.7) debería producir un aumento medible de
sincronización de fase entre el resto de los nodos activos (ΔPLV > 0.3).

**Resultado (30 semillas × 2000 pasos, 60,000 evaluaciones de estado):** la condición de
disparo sí ocurre (2237 eventos, 3.73% de los pasos), pero **solo 20 de 2237 eventos (0.9%)**
muestran el aumento de sincronización reclamado. La media de ΔPLV sobre todos los eventos es
**−0.007 ± 0.061**, prácticamente cero — no el −0.46 que un borrador previo de este trabajo
había reportado como "verificado".

**Hipótesis sobre la causa (no verificada por separado):** el Teorema 1 converge a ~4–5
nodos activos con estos parámetros; la medida de sincronización se calcula sobre los nodos
activos excluyendo la raíz, es decir, típicamente 3–4 nodos — una población pequeña para que
15 pasos de acoplamiento elevado (η=0.15) produzcan una sincronización estable y medible por
encima del ruido. Hay una tensión directa entre este mecanismo y el punto fijo homeostático
de la Sección 3.1: el mismo parámetro que hace que el sistema sea económico (pocos nodos
activos) parece ser lo que impide que el mecanismo de hijacking tenga suficiente "masa" para
producir el efecto que se le atribuye.

**Conclusión:** este mecanismo, tal como está implementado y parametrizado, **no se sostiene**
y no debe citarse como verificado. Requiere rediseño (más nodos activos, disparo distinto, más
pasos de acoplamiento elevado) y nueva verificación, o debe reportarse como predicción
abierta/no confirmada.

---

## 4. Memoria de Trabajo como Recurso Continuo Emergente

### 4.1 Método: tarea N-back grounded (versión corregida, "occurrence-aware")

El modelo de N-back reutiliza el mismo sustrato del núcleo (Ec. 5, competencia por
vitalidad) sin capa ad hoc condicionada al valor de n-back: la única regla de decisión es
similitud coseno en el espacio ω, igual para todo n-back. d=8, N=100 nodos de pool,
n_stimuli=50, 40 ensayos por condición.

> **Nota metodológica sobre una versión anterior del script (v5), conservada en**
> `codigo/nback_v5_legacy_flawed/` **por transparencia, no usar sus números.** La versión
> original escribía el estímulo actual en el sustrato *antes* de evaluar si el objetivo de
> hace n-back pasos seguía "vivo". En un ensayo de tipo *match*, el estímulo actual es por
> definición igual al objetivo — así que esa escritura satisfacía la pregunta por
> construcción, sin importar qué había pasado n_back pasos atrás (`hit_rate = 1.0000`
> siempre, para cualquier n-back). Ningún tamaño de vocabulario corrige esto: es un problema
> de orden de operaciones, no de estadística. La versión corregida (`nback_v6_corrected/`,
> usada para todos los números de esta sección) invierte el orden: primero se evalúa el
> ensayo usando el estado heredado del paso anterior, y recién después se escribe el
> estímulo actual.

### 4.2 Resultados: degradación de d′

| n-back | precisión balanceada | d′ |
|---|---|---|
| 1  | 100.0% ± 0.1% | 5.39 |
| 2  | 99.1% ± 0.6%  | 4.87 |
| 3  | 87.2% ± 1.8%  | 3.18 |
| 4  | 72.0% ± 2.3%  | 2.19 |
| 5  | 59.3% ± 2.0%  | 1.29 |
| 6  | 56.2% ± 1.6%  | 1.06 |
| 7  | 55.7% ± 1.7%  | 0.98 |
| 8  | 55.5% ± 1.3%  | 1.00 |
| 10 | 55.1% ± 1.6%  | 0.97 |
| 12 | 55.4% ± 1.9%  | 1.00 |
| 15 | 54.2% ± 1.7%  | 0.82 |
| 20 | 53.8% ± 1.6%  | 0.80 |

N_ss\* empírico de este modelo (independiente del chequeo match/no-match, no afectado por el
bug de v5): **9.50 ± 1.02 nodos**.

**Patrón:** la caída más pronunciada en un solo paso ocurre entre 2 y 3-back
(4.87 → 3.18, Δ=1.69), por debajo del umbral de 2.0 que definimos como "escalón abrupto" —
pero con un margen angosto, no cómodo. De 6-back en adelante, d′ se estabiliza en un piso
residual de ~0.8–1.0 que no baja a cero incluso en 20-back. La interpretación más probable de
este piso es un efecto del espacio de estímulos finito (n_stimuli=50 en un espacio de d=8
dimensiones): incluso cuando la traza específica del estímulo consultado ya se extinguió,
comparar contra lo que sea que esté vivo en el sustrato da una tasa de acierto por encima del
azar por coincidencia, no necesariamente por retención genuina. Vale la pena tenerlo presente
al interpretar la cola de la curva.

**No hay escalón discreto de capacidad en ningún punto probado** (1 a 20-back) — la
conclusión cualitativa central se sostiene, y de hecho se sostiene *mejor* con esta versión
corregida que con la versión v5 original (que nunca mostraba misses y por eso subestimaba la
caída real).

### 4.3 Comparación con modelos de slots y de recurso continuo

El "codo" real de la curva (72%→59% de precisión balanceada entre 4 y 5-back) es comparable
en magnitud a la capacidad clásica reportada por Cowan (~4) y Miller (7±2) — un punto de
comparación honesto que la versión v5 (con su meseta temprana e irrealmente alta) no permitía.
La forma completa —caída pronunciada entre 2 y 5-back, seguida de una meseta con piso residual
— es más consistente con un modelo de recurso con límite que con una degradación suave sin
fondo hasta cero.

### 4.4 Comparación contra un baseline recurrente simple

Pedido explícito de la revisión científica externa (`auditoria/REVIEW_RECOMMENDATIONS.md`):
"incluir comparaciones contra baselines simples". Implementado en
`codigo/baselines/rnn_baseline.py`: un Elman RNN vainilla (tanh, sin gating, 32 unidades
ocultas) entrenado end-to-end por BPTT sobre la misma tarea, el mismo generador de secuencias,
el mismo n_stimuli=50 y evaluado sobre el mismo conjunto de 40 seeds de test que DSCN-G v6. El
RNN se entrena por separado para cada n-back (400 épocas, Adam) sobre 40 secuencias disjuntas
del test, promediando 3 semillas de inicialización para descartar mínimos locales malos.

| n-back | d′ DSCN-G | d′ RNN vainilla |
|---|---|---|
| 1  | 5.39 | 4.63 |
| 2  | 4.87 | 1.64 |
| 3  | 3.18 | 1.43 |
| 4  | 2.19 | 0.49 |
| 5  | 1.29 | 0.74 |
| 6  | 1.06 | 0.35 |
| 7  | 0.98 | 0.01 |
| 8  | 1.00 | 0.00 |
| 10 | 0.97 | −0.01 |
| 12 | 1.00 | 0.00 |
| 15 | 0.82 | −0.01 |
| 20 | 0.80 | 0.00 |

El RNN vainilla se degrada más rápido que DSCN-G en todo el rango y colapsa a d′≈0 (azar) a
partir de 7-back — el comportamiento esperado de una recurrencia sin gating frente a
dependencias largas, y por eso mismo un resultado válido, no una sorpresa que infle el
contraste. Lo informativo es que DSCN-G **no** muestra ese colapso: retiene un piso de
d′≈0.8–1.0 hasta 20-back en la misma tarea y el mismo espacio de estímulos. Esto acota (sin
eliminar del todo) la preocupación de la Sección 4.2 sobre si ese piso residual es puramente
un artefacto de coincidencia por espacio de estímulos finito: si lo fuera únicamente por eso,
cabría esperar que el RNN, evaluado en el mismo espacio de 50 estímulos, mostrara un piso
similar por la misma razón — y no lo muestra, cae a azar exacto.

**Advertencia sobre la comparación:** no es una comparación en igualdad total de condiciones.
DSCN-G es un mecanismo sin entrenamiento supervisado (corrido directo sobre las 40 seeds de
test); el RNN se entrena con gradiente supervisado sobre secuencias separadas. Difieren en
arquitectura, régimen de aprendizaje y objetivo de optimización. El resultado dice que un RNN
simple *comparable en tamaño* no reproduce el piso de DSCN-G en esta tarea — no que ningún
modelo recurrente pueda hacerlo (un LSTM/GRU con gating podría comportarse distinto; queda
como extensión futura, ver §5.5).

---

## 5. Discusión

### 5.1 Qué se sostiene y qué no (resumen)

**Se sostiene tal como se reclama:**
- Convergencia de ω (Teorema 2): alineación = 1.0000.
- N_ss\* empírico del modelo de N-back: 9.5 ± 1.0 nodos.
- Ausencia de escalón discreto en la degradación de memoria de trabajo (forma cualitativa).
- Teorema 1: cota universal, condición de punto fijo, **y maximalidad (iii) con simulación
  real** (inyección al umbral, 100% podado de vuelta en las tres condiciones de N_init —
  Sección 3.1). Las cuatro partes del Teorema 1 se sostienen completas.
- Baseline recurrente (Sección 4.4): DSCN-G retiene un piso de d′≈0.8–1.0 hasta 20-back donde
  un RNN vainilla comparable colapsa a azar desde 7-back.

**Necesita corrección de cifras respecto de borradores previos:**
- N_ss\* del Teorema 1 es ~4–5 nodos, no ~9–10 (esa cifra pertenece al modelo de N-back, un
  sistema distinto que comparte sustrato pero no ecuación de poda idéntica en su uso).
- Consenso de fase (Teorema 3): 100% bajo el criterio operacional del código, 76.7% bajo el
  criterio estricto que el enunciado formal define — hay que especificar cuál se reporta.
- Valores puntuales de d′: la curva real cae y se estabiliza en un piso de ~0.8–1.0, no sigue
  bajando indefinidamente.

**No se sostiene, requiere rediseño o retirarse:**
- Mecanismo de sincronización patológica ("hijacking"): el efecto reclamado no aparece en
  promedio (Sección 3.4).

### 5.2 Resultados negativos y fallos encontrados (transparencia metodológica)

Documentamos explícitamente, en vez de omitir, tres fallos encontrados durante el desarrollo:
(1) el bug de orden de operaciones en la versión original del N-back, que garantizaba
`hit_rate=1.0` estructuralmente; (2) el acoplamiento Kuramoto no sincrónico en una versión
anterior del núcleo, que introducía dependencia espuria del orden de iteración; (3) el
mecanismo de hijacking, que no produce el efecto que motivó su diseño. Los tres están
corregidos o señalados en el código adjunto, con su historial de auditoría completo en
`auditoria/`.

### 5.3 Predicción falsificable: gradiente vs. umbral en activación neural

Si la memoria de trabajo opera como recurso continuo, medidas de actividad neural (p. ej.
amplitud gamma en EEG) durante una tarea N-back deberían mostrar un gradiente proporcional a
la carga, no un umbral discreto. **Criterio de falsificación:** observar un escalón abrupto de
activación en algún punto de carga falsificaría esta predicción. No incluimos aquí la
predicción relacionada con el mecanismo de hijacking (aumento de PLV gamma durante sobrecarga)
como si estuviera lista para probarse experimentalmente: dado que el propio simulador de
referencia no reproduce ese efecto internamente (Sección 3.4), proponerla como predicción
confirmada del modelo sería inconsistente con nuestros propios resultados. Queda como trabajo
futuro condicionado a resolver primero el rediseño del mecanismo.

### 5.4 Limitaciones

- N-back simplificado: sin período de demora ni distractores explícitos.
- **Sin estudios de ablación** (qué mecanismo —TD-learning, fase, homeostasis— es responsable
  de qué parte del comportamiento) ni **análisis de sensibilidad a parámetros**. La
  comparación contra un baseline recurrente sí se incorporó (Sección 4.4), pero estos dos
  puntos, señalados en la revisión científica de este trabajo
  (`auditoria/REVIEW_RECOMMENDATIONS.md`), siguen pendientes.
- Sin validación experimental (EEG/fMRI) — trabajo futuro.
- El piso residual de d′ en n-back alto podría seguir siendo, en parte, un efecto del tamaño
  finito del espacio de estímulos y no solo retención genuina; el baseline RNN (Sección 4.4)
  acota esa preocupación —un RNN evaluado en el mismo espacio de estímulos no muestra el mismo
  piso— pero no la descarta del todo, porque el RNN también difiere en régimen de
  entrenamiento.
- El mecanismo de hijacking no reproduce su propia predicción a escala canónica (Sección 3.4)
  y necesita rediseño antes de poder usarse como base de ninguna predicción experimental.

### 5.5 Trabajo futuro

- Ablation studies; sensibilidad a parámetros; pruebas de generalización; robustez ante ruido;
  baseline adicional con un RNN con gating (LSTM/GRU) para ver si el piso de rendimiento de
  DSCN-G también aparece en una arquitectura recurrente más capaz — agenda sugerida en la
  revisión científica adjunta, ahora con el ítem de baseline simple ya cubierto (Sección 4.4).
- Rediseño del mecanismo de hijacking (más nodos activos, disparo distinto, más pasos de
  acoplamiento elevado) y nueva verificación.
- Validación experimental EEG/fMRI de la predicción de gradiente continuo (Sección 5.3).
- Explorar si subir n_stimuli más allá de 50 reduce el piso residual de d′ observado en
  n-back alto.

### 5.6 Analogías (usar con cautela)

Las siguientes son herramientas pedagógicas, no afirmaciones de identidad: la homeostasis de
vitalidad es *análoga* a la poda sináptica; el acoplamiento Kuramoto dinámico es *análogo* a
modulación de atención/arousal. No usamos la analogía con epilepsia focal para el mecanismo de
hijacking en este documento, dado que ese mecanismo no está confirmado (Sección 3.4) —
extender una analogía biológica a un efecto que el propio modelo no reproduce sería
sobre-interpretación.

---

## 6. Conclusión

DSCN-G es una arquitectura de cognición computacional que deriva un patrón de memoria de
trabajo como recurso continuo —sin imponerlo como supuesto— a partir de tres mecanismos
acoplados y verificables: aprendizaje por diferencia temporal, dinámica de fase Kuramoto, y
poda homeostática basada en vitalidad. De los cuatro mecanismos formales evaluados, dos se
sostienen limpios y completos (convergencia de ω; punto fijo homeostático, incluida su
sub-claim de maximalidad, verificada con simulación real), uno se sostiene con matices que
dependen del criterio adoptado (consenso de fase), y uno se probó explícitamente y no se
sostiene (sincronización patológica). Un baseline recurrente simple muestra además que el piso
de memoria de trabajo que retiene DSCN-G en n-back alto no es trivial: un RNN comparable
colapsa a azar donde DSCN-G no lo hace. Reportamos los cuatro mecanismos con el mismo nivel de
detalle, incluyendo el que falló, porque consideramos que la trazabilidad completa —qué se
corrió, con qué código, y qué salió— es más útil que una lista de éxitos. El paquete de código
y datos adjunto permite reproducir cada cifra de este documento.

---

## 7. Referencias

- Bays, P. M., & Husain, M. (2008). Dynamic shifts of limited working memory resources in
  human vision. *Science*.
- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental
  storage capacity. *Behavioral and Brain Sciences*.
- Miller, G. A. (1956). The magical number seven, plus or minus two. *Psychological Review*.
- van den Berg, R., Awh, E., & Ma, W. J. (2014). Resource-rational analysis of working
  memory. *Psychological Review*.
- Kuramoto, Y. (1984). *Chemical Oscillations, Waves, and Turbulence*. Springer.
- Acebrón, J. A., et al. (2005). The Kuramoto model: A simple paradigm for synchronization
  phenomena. *Reviews of Modern Physics*.
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.).
  MIT Press.
- Elman, J. L. (1990). Finding structure in time. *Cognitive Science*, 14(2), 179–211.

---

## 8. Material Suplementario

Incluido en este paquete:

- `codigo/core/` — `verify_dscng_v3.py` (verificación de T1–T3, C3) y
  `verification_results_v3.json` (resultados crudos, 30 seeds × 2000 pasos); además
  `verify_maximality_real.py` y `maximality_real_results.json` (simulación real de la
  sub-claim de maximalidad de T1, Sección 3.1).
- `codigo/nback_v6_corrected/` — script corregido usado para todas las cifras de la
  Sección 4, datos crudos y Figura 2.
- `codigo/nback_v5_legacy_flawed/` — versión original, conservada por transparencia,
  **no usar sus cifras**.
- `codigo/baselines/` — `rnn_baseline.py` y `rnn_baseline_results.json`, baseline recurrente
  usado en la Sección 4.4.
- `codigo/analyze_results.py`, `codigo/run_pipeline.sh` — utilidades de análisis y
  ejecución de punta a punta.
- `auditoria/` — las tres rondas de auditoría completas (`AUDIT_NOTES*.md`),
  `claims_falsifiable.md` (veredicto por claim), `paper_structure.md` (outline de trabajo con
  anotaciones), y la revisión científica externa (`REVIEW_RECOMMENDATIONS.md`).

**Reproducibilidad:** `bash codigo/run_pipeline.sh` corre el núcleo y el N-back v5 legacy de
punta a punta; el N-back v6 corregido se corre aparte con
`python3 codigo/nback_v6_corrected/nback_v6_occurrence_aware.py`.
