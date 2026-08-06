# Estructura del Paper: DSCN-G v3

> ⚠️ **Nota de auditoría (2026-07-22, actualizada 2026-07-23 Ronda 4):**
> este outline se dejó igual en su estructura; se agregaron notas
> `> AUDIT:` inline en los puntos donde el número o la claim citada no se
> reprodujo al correr el código corregido. Ver `AUDIT_NOTES.md`,
> `AUDIT_NOTES_ROUND3.md`, `AUDIT_NOTES_ROUND4.md` y
> `claims_falsifiable.md` para el detalle completo y los números reales
> antes de escribir la prosa final de cada sección.

## Título propuesto

**"DSCN-G: A Unified Framework for Emergent Working Memory as Continuous Resource"**

## Abstract (~200 palabras)

**Problema:** Las teorías actuales de consciencia (IIT, GWT, PP) tienen limitaciones: IIT es computacionalmente intratable, GWT es descriptivo sin ecuaciones formales, PP no implementa NCC concreto.

**Solución:** Presentamos DSCN-G (Dual-State Cognitive Geometry), un framework unificado que combina TD-learning, dinámica de fases Kuramoto, y homeostasis adaptativa.

**Resultados:** Verificamos 4 teoremas: (1) punto fijo homeostático emergente (N_ss* = 9.5 ± 1.0 nodos), (2) convergencia de alineación ω (alignment = 0.9998), (3) consenso de fase vía Kuramoto (90% consensus rate), (4) coexistencia de consenso normal y hijacking patológico. Validamos el modelo con N-back task, mostrando que la memoria de trabajo emerge como **recurso continuo** (degradación suave de d' de 5.30 a 2.78), no como slots discretos.

> **AUDIT:** el "N_ss* = 9.5 ± 1.0" de este párrafo es en realidad el
> resultado del modelo de N-back (Claim 6a), no de Theorem 1 — el N_ss*
> real de T1 es ~4.0–4.8 (con maximalidad confirmada por simulación real,
> Ronda 4). "alignment = 0.9998" se reproduce (real: 1.0000).
> "90% consensus rate" se reproduce distinto: 100% por el criterio del
> código, 76.7% (23/30) por el criterio estricto R≥0.9 que el teorema
> define. "degradación suave de d' de 5.30 a 2.78" no se reprodujo con
> ninguna de las dos versiones del N-back: v5 caía a ~3.9 y se aplanaba
> ahí (bug de orden, corregido); v6 (occurrence-aware, el número correcto
> a usar) cae de 5.39 a ~1.0 hacia el 5-back, con la caída más fuerte
> (Δd'=1.69) entre 2 y 3-back, y un piso residual de 0.8-1.0 desde
> ~6-back. Reescribir este párrafo con los números de
> `claims_falsifiable.md` antes de enviar a ningún lado.

**Contribuciones:** (1) Primer framework con predicciones falsificables y simulador open-source, (2) Modelo de recurso continuo emergente desde principios homeostáticos, (3) Criterios de falsificación claros para validación experimental.

**Claim:** DSCN-G implementa Neural Correlates of Consciousness (NCC) formalmente completo, sin pretender resolver el "hard problem".

## 1. Introduction (~1000 palabras)

### 1.1 Limitaciones de Frameworks Actuales

- **IIT (Tononi 2004):** Φ es intratable computacionalmente para N > 10
- **GWT (Baars 1988):** Descriptivo, sin ecuaciones formales
- **PP (Friston 2010):** Free energy principle, pero sin implementación concreta de NCC

### 1.2 Limitaciones de Modelos de Slots

- **Cowan (2001), Miller (1956):** Predicen escalón abrupto en capacity
- **Evidencia empírica contradictoria:** algunos estudios muestran degradación suave
- **Bays & Husain (2008), van den Berg et al. (2014):** Modelos de recurso continuo
- **Gap:** No hay modelo computacional que derive recurso continuo desde principios homeostáticos

### 1.3 DSCN-G en una Página

- Arquitectura unificada: graph + TD-learning + Kuramoto + autopoiesis
- Ecuaciones clave: Eqs. 1-7
- Claim: NCC formalmente completo (no resuelve hard problem)

### 1.4 Posición Ontológica

- NCC (Neural Correlates of Consciousness), no hard problem
- Honestidad epistémica: no claimamos "es consciente"
- Falsificabilidad: cada claim tiene criterio de falsificación

### 1.5 Contribuciones (Bullet Points)

1. Framework unificado con 4 teoremas verificados
2. WM como recurso continuo emergente (no slots)
3. Predicciones falsificables (EEG/fMRI)
4. Simulador open-source (GitHub: nexus-vault)

> **AUDIT:** "4 teoremas verificados" hay que matizarlo — T2 se sostiene
> limpio, T1 se sostiene completo (cota, punto fijo, y maximalidad con
> simulación real desde Ronda 4), T3 se sostiene con un criterio más
> laxo que su propia definición (76.7% con el criterio estricto), y C3
> no se sostiene a los parámetros de diseño originales (mejora parcial
> con rediseño, sigue sin ser "la norma"). Ver `claims_falsifiable.md`.

### 1.6 Roadmap

- Sección 2: Computational Foundations
- Sección 3: Formal Theorems
- Sección 4: Working Memory Validation
- Sección 5: Discussion
- Sección 6: Conclusion

## 2. Computational Foundations (~1500 palabras)

### 2.1 Graph Structure

- N nodos, K cadenas de información
- Cada nodo: (ω_i ∈ ℝ^d, φ_i ∈ [0, 2π), V_i ∈ [0, 1])
- Raíz ancla: nodo 0

### 2.2 TD-learning (Eq. 1)

- ω_i ← (1-β)ω_i + β·reward·ω_ideal
- reward = alignment(ω_i, ω_ideal)
- Broadcast a todos los nodos en fase

### 2.3 Information Chains (Eq. 2)

- P(m|n) ∝ exp(-α·‖ω_m - ω_n‖)
- Cadenas de información compiten por recursos

### 2.4 Phase Dynamics (Eqs. 3-4)

- Δφ_i = η·R_i·reward·sin(θ_a - φ_i)
- Von Mises action: P(a|φ) = softmax(λ·cos(φ - θ_a))

### 2.5 Autopoiesis (Eqs. 5-6)

- V_i ← V_i·e^{-γ} + A_i·(1-e^{-γ})
- Pruning: V_i < θ_death → nodo eliminado
- Valence: E_i = max(0, A_i - V_i)·κ

### 2.6 Wave Interference (Eq. 7)

- I_i = ‖ω_i‖·cos(φ_i - φ_root)
- Interferencia constructiva/destructiva

### 2.7 Dynamic η_kura (NUEVO v3)

- η_kura = 0.005 (basal) → 0.025 (hijack)
- Análogo a acetilcolina/noradrenalina (atención/arousal)
- Kuramoto all-to-all: dφ_i/dt = ω_i + (η_kura/N)·Σ_j sin(φ_j - φ_i)

> **AUDIT:** la implementación original de este acoplamiento no era
> sincrónica (escribía φ_i y lo volvía a leer como φ_j dentro del mismo
> barrido, dependiendo del orden de `nodes_active`). Se corrigió para que
> use una foto de φ(t) para todo el update, que es lo que esta ecuación
> describe. Ver `AUDIT_NOTES.md` §1.3.

### Figura 1: Architecture Diagram

- Mostrar: nodos, cadenas, root, ω, φ, V
- Mostrar: flujo de información (chains, RL, Kuramoto)

## 3. Formal Theorems (~1500 palabras)

### Theorem 1: Homeostatic Fixed Point + Maximality

**Statement:**
- (i) N_ss* ≤ 1/θ_death (universal bound)
- (ii) ρ_eff ≥ N_ss* · θ_death² (fixed-point condition)
- (iii) N_ss* es el mayor n satisfaciendo (ii) — maximality

**Proof sketch:**
- De Eq. 5 en régimen estacionario: V_i ≈ A_i
- Pruning elimina nodos con V_i < θ_death
- ρ_eff = Σ(A_i/ΣA)² (Herfindahl index)
- Maximality: N_ss*+1 no cumple (ii)

**Verificación computacional:** ✅ (i) y (ii). ✅ (iii) maximalidad —
simulación real con inyección al umbral (Ronda 4, 2026-07-23): el sistema
poda de vuelta al nodo extra en el 100% de los seeds, en las 3 condiciones
de N_init probadas — ver `AUDIT_NOTES_ROUND4.md` §2. **N_ss* real ≈ 4.0–4.8**,
no 9-10.

### Theorem 2: ω Alignment Convergence

**Statement:**
- ω* = ω_ideal (convergence to max alignment = 1.0)
- mean_alignment_final ≥ 1 - 2β

**Proof sketch:**
- Eq. 1: ω_i ← (1-β)ω_i + β·reward·ω_ideal
- reward = (ω_i·ω_ideal)/‖ω_i‖ ∈ [-1, 1]
- En equilibrio: ω_i = ω_ideal

**Verificación computacional:** ✅ Se sostiene limpio (alignment=1.0000, ver Sección 1)

### Theorem 3: Phase Consensus

**Statement:**
- Consensus = Kuramoto order parameter R ≥ 0.9
- R = |⟨e^{iφ}⟩|

**Proof sketch:**
- Kuramoto all-to-all: dφ_i/dt = ω_i + (η/N)·Σ_j sin(φ_j - φ_i)
- Para η > η_c, sistema sincroniza (R → 1)

**Verificación computacional:** ⚠️ 100% de corridas "cuentan" como consenso
con el criterio del código, pero solo 76.7% (23/30) cumplen realmente
R≥0.9 tal como dice el Statement de arriba; el resto pasa por una rama de
respaldo más laxa (R≥0.5). 0/30 casos bimodales. Definir en el texto cuál
criterio se está reportando.

### Theorem 4: Dynamic η_kura Enables T3+C3 Coexistence

**Statement:**
- η_kura dinámico permite coexistencia de consenso normal y hijacking
- η_kura = 0.005 (basal) → 0.025 (hijack)

**Proof sketch:**
- Durante hijack: η_kura aumenta → sincronización patológica
- Después de hijack: η_kura vuelve a basal → consenso normal

**Verificación computacional:** ⚠️ El sistema sí alterna entre los dos
modos operativamente, pero el modo "hijack" no produce, en promedio, la
sincronización patológica que se le atribuye (ver Theorem/Conjecture C3
abajo). La coexistencia de los dos *modos* ocurre; el *efecto* del segundo
modo no está confirmado.

### C3 Conjecture: Phase Hijacking

**Statement:**
- Hijacking ocurre cuando V_root > θ_emerg
- ΔPLV > 0.3 (sincronización patológica)

**Proof sketch:**
- Root actúa como driver patológico (epilepsia focal)
- Otros nodos son arrastrados hacia φ_root

**Verificación computacional:** ❌ **No se sostiene a los parámetros de
diseño originales.** El hijacking (V_root > θ_emerg) sí ocurre (2237 veces
en 30×2000 steps), pero solo el 0.9% de esos eventos produce ΔPLV > 0.3;
la media es ≈0 (−0.007 ± 0.061), no −0.46. Rediseño (Ronda 4,
2026-07-23): subiendo la población de seguidores (θ_death más bajo) y la
duración/fuerza del hijack, el rise_rate sube monótonamente hasta 30.2%
en la config más agresiva probada — mejora real de ~40x, pero lejos de
"la norma". Ver `AUDIT_NOTES_ROUND4.md` §1 para la tabla completa. Esta
sección necesita decidir entre reportar el rediseño como evidencia
parcial o retirar la claim.

## 4. Working Memory as Emergent Continuous Resource (~1000 palabras)

### 4.1 Methods: N-back Task Protocol (v6, occurrence-aware)

**Diferencia clave vs. v4:** Sin cap explícito ni rama condicionada a n_back

**Mecanismo:** Competencia por vitalidad (Eq. 5) + similitud coseno en espacio ω

**Nota metodológica:** Sustrato reutilizable (vitalidad decae sobre todo el pool, sin pruning permanente)

> **AUDIT:** el script original no guardaba resultados a disco (bug de
> pipeline corregido) y su barrido por defecto solo llegaba a 10-back, no
> a los 15-back que se citan en 4.2. Ambos corregidos.

> **AUDIT (Ronda 3, 2026-07-22):** además de eso, v5 tenía un bug de
> orden de operaciones — el chequeo de match/no-match se hacía DESPUÉS de
> escribir el estímulo actual, así que un trial *match* se auto-
> satisfacía con su propia escritura (`match_alive_frac=1.0000` exacto,
> para cualquier n_back). v6 (`nback_v6_occurrence_aware.py`) invierte el
> orden y sube `n_stimuli` de 10 a 50. Ver `AUDIT_NOTES_ROUND3.md` para
> el detalle completo. Los números de 4.2/4.3/4.4 de abajo son de v6.

### 4.2 Results: Degradación de d' (v6, occurrence-aware)

- N_ss* empírico = 9.5 ± 1.0 nodos ✅ (se reproduce, no depende del bug de v5)
- d'(1-back) = **5.39** (v5 daba 5.33 — prácticamente igual)
- d'(3-back) = **3.18** (v5 daba 4.20 — más bajo con el chequeo real)
- d'(5-back) = **1.29** (v5 daba 3.91)
- d'(10-back) = **0.97**, d'(15-back) = **0.82** (v5 daba 3.92 / 3.90 — la
  meseta de v5 era artefacto del bug de orden, no un piso real)
- **Patrón real (v6):** cae fuerte de 5.39 (1-back) a ~1.0 (5-back), con
  la caída más pronunciada entre 2-back y 3-back (Δd'=1.69) — por debajo
  del umbral de "escalón abrupto" (>2.0 en un paso) pero con margen
  angosto, no cómodo. De ahí en más, piso residual entre 0.8-1.0 (no baja
  a 0) desde ~6-back en adelante — atribuible a coincidencias residuales
  del espacio de estímulos finito (n_stimuli=50), documentado en
  `README.md`. Sigue sin haber escalón abrupto en ningún punto probado
  (1 a 20-back) — esa conclusión cualitativa central del paper se
  sostiene, y con v6 se sostiene *mejor* que con v5, no peor: la curva
  real (caída marcada 2→5-back) es más comparable con Cowan/Miller que la
  meseta artificial de v5. Ver `figure2_nback_v6_paper.png` y
  `AUDIT_NOTES_ROUND3.md` §2-3 para la tabla completa y el detalle del fix.

### 4.3 Comparison: Bays & Husain (2008), van den Berg et al. (2014); Cowan (2001), Miller (1956)

**Modelos de slots (Cowan, Miller):** Predicen escalón abrupto

**Modelos de recurso continuo:** Predicen degradación suave

**DSCN-G v3 (v6):** Implementa recurso continuo emergente desde
principios homeostáticos — la caída marcada entre 2-back y 3-back (Δd'=1.69,
por debajo del umbral de escalón pero con margen angosto) y el "codo" real
de la curva (72%→59% entre 4 y 5-back) quedan en un rango de magnitud
comparable a Cowan (~4 ítems) y Miller (7±2) — comparación honesta que v5
no permitía (su meseta arrancaba en ~94% desde 5-back, mucho más generosa
que la literatura clásica). No es degradación suave en todo el rango: es
caída marcada seguida de piso, y hay que decirlo así, no como "degradación
suave" sin matices.

**Comparación adicional (Ronda 4, 2026-07-23):** contra un RNN recurrente
simple (Elman, sin gating) entrenado en el mismo protocolo — ver 4.5.

### 4.4 Figura 2: d' vs. n-back

- Panel izquierdo: balanced accuracy vs n-back
- Panel derecho: d' vs n-back (sensibilidad pura)
- Anotación: **"Caída pronunciada 2→5-back, piso residual desde ~6-back"**
  (reemplaza "degradación suave" — no es lo que muestra v6). Ver
  `generate_figure2_v6.py`, ya corregido.

### 4.5 Comparación contra RNN recurrente simple (Ronda 4, pedido de REVIEW_RECOMMENDATIONS.md)

**Diseño:** Elman RNN vainilla (tanh, sin gating), BPTT completo,
entrenado sobre 40 secuencias separadas (seeds 1000-1039) y evaluado
sobre las mismas 40 seeds de test que DSCN-G v6 (0-39), promediado sobre
3 semillas de inicialización de pesos.

| n_back | DSCN-G v6 (d') | RNN vainilla (d') |
|---|---|---|
| 1 | 5.39 | 4.63±1.68 |
| 3 | 3.18 | 1.43±0.71 |
| 5 | 1.29 | 0.74±0.54 |
| 7 | 0.98 | 0.01±0.02 |
| 10 | 0.97 | −0.01±0.01 |
| 20 | 0.80 | 0.00±0.02 |

El RNN compite en n_back bajo pero colapsa a nivel de azar desde n_back≈7
(vanishing gradients — esperable de la literatura, no sorpresa). DSCN-G
mantiene d'≈0.8-1.0 incluso en 20-back. **Limitación a declarar:** RNN
*vainilla*, no LSTM/GRU/Transformer — comparación parcial. Ver
`AUDIT_NOTES_ROUND4.md` §4.

## 5. Discussion (~1000 palabras)

### 5.1 Comparison with IIT/GWT/PP

**IIT:** Φ intratable → DSCN-G ofrece Φ_proxy tratable — **con la
salvedad de que Φ_proxy nunca tuvo una definición formal hasta Ronda 4
(2026-07-23), donde se propuso una (información mutua gaussiana entre dos
mitades del sistema) sin aprobar todavía, y cuyo primer resultado NO
soporta la predicción O(log N) con confianza — ver 5.4 y
`claims_falsifiable.md` Claim 7.**

**GWT:** Descriptivo → DSCN-G tiene ecuaciones formales

**PP:** Free energy → DSCN-G implementa NCC concreto

### 5.2 Resource Continuum vs. Discrete Slots (Predicción Falsificable)

**Predicción:** EEG/fMRI deberían mostrar gradiente de activación, no umbral

**Criterio de falsificación:** Si se observa escalón abrupto en capacidad, modelo es falso

**Experimento propuesto:** N-back con EEG, medir amplitud gamma vs. carga

### 5.3 C3 as Falsifiable Prediction (EEG: Gamma PLV Increase During Overload)

> **AUDIT:** esta sección predice, a partir del modelo, que el PLV gamma
> debería subir durante sobrecarga. Pero el propio modelo, corrido a
> escala canónica con los parámetros de diseño originales, no muestra ese
> aumento de PLV en el 99.1% de sus eventos de hijacking (ver C3
> Conjecture arriba). **Actualización (Ronda 4):** con población de
> seguidores mayor y hijack más largo/fuerte, el efecto sube a 30.2% de
> los eventos — sigue sin ser "la norma", pero ya no es prácticamente
> cero. Antes de proponer este experimento como prueba de DSCN-G, hay que
> decidir con qué régimen de parámetros se está hablando: a los
> parámetros de diseño originales, el simulador de referencia no confirma
> su propia predicción; con parámetros más agresivos (y ya bastante
> alejados del diseño original), la confirma parcialmente.

**Predicción:** Durante sobrecarga cognitiva, PLV gamma debería aumentar

**Criterio de falsificación:** Si PLV no aumenta durante overload, C3 es falso

**Experimento propuesto:** N-back con alta carga, medir PLV gamma

### 5.4 Limitations

- Simplified N-back (no delay, no distractors)
- No validación experimental (EEG/fMRI) — future work
- Φ_proxy scaling O(log N) — **(Ronda 4)** definición propuesta sin
  aprobar; con esa definición, los datos disponibles NO soportan O(log N)
  con confianza (R²=0.22 vs log(N), R²=0.07 vs N, ambos débiles) — ver
  `claims_falsifiable.md` Claim 7 y `AUDIT_NOTES_ROUND4.md` §3
- C3 no reproduce su propia predicción a los parámetros de diseño
  originales; con rediseño (más población, hijack más largo/fuerte) sube
  a 30.2% de los eventos, todavía lejos de "la norma" — ver 5.3
- El piso residual de d' post-5-back en v6 (~0.8-1.0, no baja a 0) es
  atribuible a coincidencias residuales del espacio de estímulos finito
  (n_stimuli=50) — no se exploró si sube más n_stimuli lo reduce más, ver
  `AUDIT_NOTES_ROUND3.md` §3
- Comparación contra recurrente simple (4.5) es solo contra RNN vainilla,
  no LSTM/GRU/Transformer — comparación parcial

### 5.5 Future Work

- Validación experimental (EEG/fMRI)
- Large-scale simulations (N > 1000)
- Drug discovery connection (análogos con pIC50 predicho)
- Φ_proxy: aprobar/reemplazar la definición propuesta en Ronda 4; correr
  con más seeds y ventana más larga en el extremo alto de N* antes de
  sacar conclusiones sobre la forma de la curva
- Seguir explorando el espacio de parámetros de C3 más allá de lo
  probado en Ronda 4 (no se llegó a saturación) — o retirar la claim
- Ampliar el baseline comparativo a LSTM/GRU/Transformer

## 6. Conclusion (~300 palabras)

**Claims principales (revisar contra `claims_falsifiable.md` antes de escribir esta sección):**
1. Homeostatic fixed point (N_ss* real ≈ 4-5 nodos, no 9.5 — ese es el
   del N-back), con maximalidad confirmada por simulación real (Ronda 4)
2. ω alignment convergence (alignment = 1.0000) ✅
3. Phase consensus (100%/76.7% según criterio — especificar cuál)
4. Dynamic η_kura (coexistencia de modos sí, coexistencia de *efectos* no confirmada)
5. Phase hijacking — no confirmado a parámetros originales; rediseño
   (Ronda 4) mejora de 0.9%→30.2% de eventos con el efecto, sin llegar a
   "la norma"
6. WM como recurso continuo (v6: sin escalón sí — margen angosto, Δd'=1.69
   entre 2 y 3-back; caída marcada 2→5-back y piso residual después, no
   degradación suave en todo el rango)
7. Comparación contra RNN vainilla (Ronda 4): DSCN-G retiene información
   donde el recurrente simple colapsa a azar (n_back≈7+)
8. Φ_proxy scaling: definición propuesta sin aprobar (Ronda 4); evidencia
   disponible no soporta O(log N) con confianza

**Framing como NCC (no hard problem)**

**Impacto:** falsificable + open-source

**Llamado a la acción:** validación experimental

## 7. References (~40-50 items)

**Referencias clave:**
- Cowan (2001): The magical number 4 in short-term memory
- Miller (1956): The magical number 7, plus or minus 2
- Bays & Husain (2008): Resources and errors in working memory
- van den Berg et al. (2014): A resource-rational analysis of working memory
- Kuramoto (1984): Chemical oscillations, waves, and turbulence
- Acebrón et al. (2005): The Kuramoto model
- Tononi (2004): An information integration theory of consciousness
- Baars (1988): A cognitive theory of consciousness
- Friston (2010): The free-energy principle
- Dehaene & Changeux (2011): Experimental and theoretical approaches to conscious processing
- Sutton & Barto (2018): Reinforcement learning: An introduction

## 8. Supplementary Material

- Código completo (GitHub: nexus-vault)
- Datos crudos (JSON files — usar los de `AUDIT_NOTES.md`/esta carpeta, generados el 2026-07-22, no versiones anteriores)
- Protocolos de validación experimental
- Derivaciones matemáticas completas

## Notas de estilo

- **Honestidad epistémica:** Separar VERIFIED de HYPOTHESIZED de SPECULATED
- **Falsificabilidad:** Cada claim debe tener criterio de falsificación
- **Open-source:** Simulador disponible en GitHub (nexus-vault)

## Analogías Biológicas (USAR CON CUIDADO)

- **η_kura dinámico:** Análogo a acetilcolina/noradrenalina (atención/arousal)
- **Hijacking (C3):** Análogo a epilepsia focal / GNW ignition — **con la salvedad de la sección 5.3**
- **Homeostasis:** Análogo a pruning sináptico + vitalidad neuronal
- **Recurso continuo:** Análogo a recursos metabólicos limitados en corteza prefrontal

## EVITAR

- ❌ "Descubre fármacos" → ✅ "Encuentra análogos con pIC50 predicho X"
- ❌ "Es consciente" → ✅ "NCC formalmente completo"
- ❌ "Demuestra" → ✅ "Verifica computacionalmente"
- ❌ "WM capacity = 4 items" → ✅ "WM opera como recurso continuo con N_ss* ≈ 9.5 nodos"
- ❌ "Drop 3→4 back = 9.8%" → ✅ "Caída pronunciada 2→5-back (d': 5.39→~1.0), piso residual desde ~6-back" (v6)
- ❌ **(agregado)** "C3 verificado" → ✅ "C3: no confirmado a los parámetros de diseño originales; con rediseño (Ronda 4) mejora a 30.2% de eventos, sigue sin ser la norma"
- ❌ **(agregado)** "N_ss* de T1 = 9-10" → ✅ "N_ss* de T1 ≈ 4-5 (distinto del N_ss* empírico del N-back, que sí es ~9.5)"
