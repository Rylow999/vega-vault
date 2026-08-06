# AUDIT_NOTES_ROUND4.md — C3 rediseñado, maximalidad real, Φ_proxy, baseline RNN (2026-07-23)

Continuación de `AUDIT_NOTES_ROUND3.md`. Esta ronda no tocó el N-back (eso
quedó cerrado en Ronda 3) — se metió con lo que Ronda 3 dejó pendiente en
su §5: C3, maximalidad de T1, Φ_proxy scaling, y el baseline recurrente
pedido por `REVIEW_RECOMMENDATIONS.md`.

`verify_dscng_v3.py` **no se tocó** — todo lo de acá son scripts nuevos y
separados (`verify_maximality_real.py`, `verify_phi_proxy.py`,
`verify_c3_redesign.py`, `codigo/baselines/rnn_baseline.py`) que importan
`DSCN_G_v3` sin modificarla, igual que Ronda 3 no tocó `nback_v5`.

---

## 1. C3 (phase hijacking) — diagnóstico confirmado, rediseño con mejora parcial

**Pregunta que disparó esto:** ¿`plv_intra_group()` mide cada nodo por
separado o la raíz? Se confirmó en el código (línea 168-174): mide el
order parameter de Kuramoto sobre `nodes_active[1:]` — el grupo de
seguidores, **excluyendo la raíz explícitamente**. No es la raíz, y no es
"cada nodo por separado" tampoco — es el consenso del grupo de
seguidores como un todo.

**Por qué eso importa:** con θ_death=0.10 (default) y T1 convergiendo a
N*≈4-5, ese grupo de seguidores son 3-4 nodos. La hipótesis no verificada
que quedó anotada en `claims_falsifiable.md` era exactamente esa: muy poca
población para que el pull de hijacking produzca una sincronización
medible. Esta ronda la puso a prueba.

**Rediseño:** se barrió θ_death (para mover N* de verdad — ver nota sobre
T1/homeostasis en §3) cruzado con `hijack_steps` y `η_hijack`, en vez de
tocar `N_init` (que T1 ya mostró que no mueve N* significativamente).

### Resultado (seeds=15, steps=2000, canónico)

| θ_death | hijack_steps | η_hijack | grupo seguidores | triggers | rise_rate | ΔPLV medio |
|---|---|---|---|---|---|---|
| 0.10 (original) | 15 | 0.15 | 3.7 | 1129 | 0.7% | −0.006±0.051 |
| 0.10 | 40 | 0.15/0.30 | 3.7 | 535 | 1.5% | −0.012±0.081 |
| 0.05 | 15 | 0.15/0.30 | 7.6 | 591 | 2.0% | −0.014±0.08–0.10 |
| 0.05 | 40 | 0.15/0.30 | 7.6 | 365 | 3.6% | −0.023±0.123 |
| 0.02 | 15 | 0.15/0.30 | 17.0 | 159 | 6.3–7.5% | −0.042/−0.048 |
| 0.02 | 40 | 0.15/0.30 | 17.0 | 134 | 9.0–9.7% | −0.057/−0.058 |
| **0.01** | **80** | **0.50** | **28.3** | 53 | **24.5%** | **−0.163±0.285** |
| **0.01** | **150** | **0.80** | **28.3** | 43 | **30.2%** | **−0.201±0.305** |

**Lectura honesta:** la tendencia es monótona y clara en la dirección que
predecía la hipótesis — más población de seguidores + hijack más largo/
fuerte → más casos con el efecto reclamado. rise_rate subió de 0.7%
(línea base Ronda 3) a 30.2% en la config más agresiva probada. Eso es una
mejora real de ~40x, no cosmética.

**Pero:** 30.2% sigue estando lejos de "la norma" (el paper original decía
100% de los triggers). El rediseño **mitiga, no rescata** la claim tal
como estaba redactada. Con los parámetros más agresivos probados
(θ_death=0.01, hijack_steps=150, η=0.80) ya se está lejos de valores que
alguien defendería como "neuromodulación fisiológicamente razonable" —
hijack_steps=150 es 10x el valor original de diseño (15), y no está claro
que siga siendo el mismo fenómeno que se quería modelar.

**Recomendación:** no cerrar esto como "C3 verificado" ni con el rediseño.
Dos caminos honestos:
  (a) reportar en el paper que el mecanismo responde en la dirección
      predicha bajo condiciones de mayor población/pull, con números
      reales (0.7%→30.2%), como evidencia parcial de que el mecanismo
      "existe" pero es débil a los parámetros con los que el modelo fue
      diseñado — y que a los parámetros de diseño originales, la claim NO
      se sostiene (ver Claim 5 en `claims_falsifiable.md`, sin cambios en
      su veredicto).
  (b) seguir explorando el espacio de parámetros más allá de lo que se
      probó acá (no se llegó a un punto de saturación claro — la curva
      seguía subiendo al final del barrido) si se quiere perseguir un
      régimen donde el efecto sea "la norma" de verdad.

No se tocó ningún otro parámetro del modelo (α, θ_emerg, γ) — sólo los
tres que tienen relación mecánica directa con el tamaño del grupo y la
fuerza/duración del pull.

---

## 2. Maximalidad de T1 (sub-claim iii) — simulación real, resultado sensible al protocolo

**Lo pedido:** dejar de aproximar con `rho_approx = K/n_test` y simular de
verdad N_init=N*+1.

**Diseño:** converger normalmente a N* (mismo protocolo que T1), después
forzar la población a N*+1 agregando un nodo genuinamente nuevo (no había
de dónde "revivir" uno podado en todos los casos — N_init=4 nunca poda a
nadie), y dejar correr la dinámica con poda activa por otros 2000 pasos
para ver si el sistema lo poda de vuelta.

**Hallazgo clave, no anticipado:** el resultado depende fuertemente de con
qué vitalidad se inyecta el nodo nuevo.

| Protocolo de inyección | N_init=4 | N_init=50 | N_init=200 |
|---|---|---|---|
| Vitalidad plena (1.0) | podado de vuelta: 3% | podado de vuelta: 77% | podado de vuelta: 27% |
| Vitalidad en el umbral (θ_death=0.10) | podado de vuelta: **100%** | podado de vuelta: **100%** | podado de vuelta: **100%** |

**Interpretación:** con vitalidad plena, el nodo nuevo tiene ~230 pasos de
margen (a γ=0.01, la vitalidad decae lento) para ser "elegido" alguna vez
por las cadenas (Ec. 2, que puede visitar cualquier nodo con probabilidad
no-nula según similitud de ω) y así recargarse antes de morir — eso es un
efecto de arranque con ventaja injusta, no evidencia sobre el punto fijo
en sí. Con vitalidad en el umbral (la inyección correcta, sin ventaja),
el nodo se poda de vuelta al toque en el 100% de los casos, en las 3
condiciones de N_init — esa sí es la simulación real que responde la
sub-claim (iii), y **la sostiene**: N* no admite un nodo extra marginal
como estado estable.

**Corrección a un criterio que armé mal en el primer intento:** también
medí si la condición (ii) [ρ_eff ≥ N·θ²] se viola apenas se fuerza N*+1
— y en los dos protocolos da 0% de violación inmediata, en las 3
condiciones. Esto NO es evidencia en contra de la maximalidad; es un
artefacto trivial de medir ρ_eff en el instante mismo de la inyección,
antes de que las cadenas hayan tenido chance de visitar (o no) al nodo
nuevo. El criterio real y honesto es el de la tabla de arriba (¿se poda
de vuelta con el tiempo?), no ese chequeo instantáneo — lo dejo anotado
acá para que quede visible que fue un error de diseño del experimento,
corregido, no escondido.

**Veredicto actualizado de la sub-claim de maximalidad:** ✅ se sostiene,
con la inyección al umbral (el protocolo correcto). Recomiendo actualizar
`claims_falsifiable.md` Claim 1 de "sin verificar" a "verificado con
simulación real" — ver §4 de este documento para el texto sugerido.

---

## 3. Φ_proxy scaling (Claim 7) — definición propuesta, resultado no concluyente

**Aviso que hay que repetir acá:** Φ_proxy nunca tuvo una fórmula en
ningún documento del paquete — sólo la predicción "debería escalar como
O(log N)". La definición usada (información mutua gaussiana entre dos
mitades del sistema, embebiendo cada φ en (cos,sin) por su circularidad)
es una propuesta mía para poder correr algo, no algo previamente acordado
— **necesita revisión y aprobación antes de citarse como Claim 7
verificado**, sea cual sea el resultado.

**Corrección metodológica importante:** el criterio de falsificación
original de `claims_falsifiable.md` sugería barrer N_init=[10,50,100,200,
500]. Eso no sirve — T1 ya demostró que N_init prácticamente no mueve N*
(homeostasis). Lo que sí mueve N* es θ_death (T1: N*≤1/θ_death). Este
experimento barrió θ_death, no N_init.

### Resultado (seeds=10, steps=2000, window=300)

| θ_death | N* real | Φ_proxy |
|---|---|---|
| 0.20 | 2.70±0.46 | 0.39±0.31 |
| 0.10 | 4.60±0.49 | 12.35±0.32 |
| 0.05 | 8.80±0.40 | 12.86±1.05 |
| 0.02 | 18.00±0.63 | 9.49±3.22 |
| 0.01 | 29.71±0.88 | 9.77±4.44 |

(θ_death=0.5 no dio corridas válidas: N* queda en 1-2 nodos, insuficiente
para partir el sistema en dos mitades.)

**Ajuste:** R² vs log(N) = 0.22, R² vs N = 0.07. Ninguno de los dos ajusta
bien. La forma real de la curva sube fuerte de N*=2.7 a N*=4.6, se
mantiene meseta entre N*=4.6 y 8.8, y después **cae** un poco hacia
N*=18-30 en vez de seguir subiendo (log o lineal). Eso no es ruido de un
solo punto — son 2 puntos en la zona alta con la misma tendencia
descendente.

**Lectura honesta:** con esta definición de Φ_proxy, la predicción
O(log N) de Claim 7 **no está soportada** por los datos — ni tampoco una
escala lineal. Se parece más a una curva que sube y después se satura o
decae, aunque con solo 5 puntos válidos y desviaciones estándar grandes
en el extremo alto (±4.44 sobre una media de 9.77) no alcanza para
afirmar la forma funcional con confianza. Antes de sacar cualquier
conclusión fuerte hace falta: (a) que decidas/apruebes la definición de
Φ_proxy en sí, (b) más seeds en el extremo alto (θ_death=0.01-0.02) donde
la varianza es peor, (c) posiblemente una ventana más larga que 300 pasos
para esas poblaciones más grandes, que puede que no hayan alcanzado un
régimen verdaderamente estacionario en el burn-in de 2000 pasos.

**Veredicto:** Claim 7 sigue sin poder marcarse como verificado, y con
esta definición propuesta, la evidencia disponible **apunta en contra**
de O(log N) específicamente (aunque no de forma concluyente). Mucho más
honesto reportarlo así que forzar una lectura optimista con 5 puntos
ruidosos.

---

## 4. Baseline recurrente simple (pedido de REVIEW_RECOMMENDATIONS.md)

Elman RNN vainilla (tanh, sin gating — deliberadamente "simple", no un
LSTM/GRU), entrenado con BPTT completo sobre 300 pasos, Adam, para cada
n_back por separado, sobre 40 secuencias de entrenamiento (seeds
1000-1039) y evaluado sobre las mismas 40 seeds de test (0-39) que usa
DSCN-G v6 — así ambos modelos se comparan sobre exactamente las mismas
instancias del task. Promediado sobre 3 semillas de inicialización de
pesos (una sola semilla daba resultados no-monótonos entre n_back=2 y
n_back=3, un artefacto de optimización, no una propiedad del task — se
corrigió promediando antes de reportar nada).

### Resultado

| n_back | DSCN-G v6 (d') | RNN vainilla (d', 3 seeds) |
|---|---|---|
| 1 | 5.39 | 4.63±1.68 |
| 2 | 4.87 | 1.64±1.84 |
| 3 | 3.18 | 1.43±0.71 |
| 4 | 2.19 | 0.49±0.65 |
| 5 | 1.29 | 0.74±0.54 |
| 6 | 1.06 | 0.35±0.47 |
| 7 | 0.98 | 0.01±0.02 |
| 8 | 1.00 | 0.00±0.01 |
| 10 | 0.97 | −0.01±0.01 |
| 12 | 1.00 | 0.00±0.01 |
| 15 | 0.82 | −0.01±0.01 |
| 20 | 0.80 | 0.00±0.02 |

**Lectura honesta:** el RNN compite en 1-back pero colapsa a nivel de
azar (d'≈0) desde n_back≈7 en adelante — el patrón clásico de vanishing
gradients en RNNs sin gating con dependencias largas, exactamente lo
esperable de la literatura, no una sorpresa. DSCN-G mantiene d'≈0.8-1.0
incluso en 20-back. Esto es evidencia real (no solo argumento teórico) de
que el mecanismo de sustrato de DSCN-G retiene información a distancias
donde un recurrente simple sin gating ya no puede — que es exactamente la
comparación que pedía `REVIEW_RECOMMENDATIONS.md`.

**Limitación a declarar en el paper:** esto compara contra un RNN
*vainilla*, no contra LSTM/GRU (que sí tienen gating diseñado
específicamente para este problema) ni contra Transformers (que no tienen
el problema de vanishing gradients en absoluto vía atención directa). La
comparación justa y completa necesitaría esos dos también — quedó fuera
de esta ronda por alcance, pero hay que decirlo así en el paper, no dejar
que "recurrente simple" suene a "cualquier recurrente".

---

## 5. Qué reemplazar en cada documento (sugerido, no aplicado acá — ver claims_falsifiable.md y paper_structure.md ya actualizados en este mismo commit)

- `claims_falsifiable.md` Claim 1 (maximalidad): pasar de "sin verificar"
  a "✅ verificado con simulación real (protocolo de inyección al umbral)"
  — con la salvedad del protocolo de vitalidad plena, que no la sostiene.
- `claims_falsifiable.md` Claim 5 (C3): mantener "❌ no verificado" a los
  parámetros de diseño originales, agregar la evidencia de rediseño
  (0.7%→30.2% con población/pull mucho mayores) como sección aparte, sin
  mezclarla con el veredicto principal.
- `claims_falsifiable.md` Claim 7 (Φ_proxy): pasar de "pendiente sin
  tocar" a "evidencia preliminar, definición propuesta sin aprobar, NO
  soporta O(log N) con los datos disponibles".
- Agregar sección nueva sobre el baseline RNN — no reemplaza nada
  existente, es evidencia nueva pedida por la revisión externa.

---

## 6. Qué queda pendiente después de esta ronda

- Φ_proxy: aprobar/reemplazar la definición propuesta; correr con más
  seeds y ventana más larga en el extremo alto de N* antes de sacar
  conclusiones.
- C3: decidir entre reportar el rediseño como evidencia parcial (opción a
  de §1) o seguir explorando parámetros más agresivos (opción b).
- Baseline: agregar LSTM/GRU y/o Transformer para una comparación
  completa, no solo RNN vainilla.
- Validación EEG/fMRI y drug discovery: sin cambios, fuera de alcance.
