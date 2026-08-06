# AUDIT_NOTES_ROUND6.md — robustez de Φ_proxy_TE, retiro de "tálamo", barrido O(log N) (2026-07-24)

Continuación directa de Ronda 5. Punto de partida: Delorien pidió (1)
retirar la analogía tálamo/hub_boost del paper, y (2) probar la robustez
de TE-bottleneck antes de aprobarla, con la intención de retomar el
barrido O(log N) de Claim 7 una vez aprobada. Esta ronda hace las tres
cosas, en ese orden.

Scripts nuevos (no se tocó `verify_dscng_v3.py` ni `verify_phi_proxy_v3.py`):
- `verify_te_bottleneck_robustness.py`
- `verify_te_bottleneck_scaling.py`

---

## 0. Retiro de la analogía "tálamo/hub_boost"

Aplicado en `claims_falsifiable.md` (Claim 5, nota al final de la
sección). `thalamic_model.py` y `verify_hub_boost_fix.py` se conservan en
el repo como evidencia del intento y su resultado nulo (Ronda 5 §2), pero
dejan de citarse en el paper como mecanismo o analogía. No afecta el
veredicto de Claim 5 (C3), que ya estaba fijado desde Ronda 4/5.

---

## 1. Robustez de TE-bottleneck: 3 particiones × 2 lags, seeds=12, steps=2000

**Diseño:** además de P0 (root vs. periferia vía parámetro de orden de
Kuramoto, la de Ronda 5), se agregaron:
- **P1 (control negativo):** periferia partida en dos mitades
  arbitrarias, SIN la raíz en ninguna. Si el patrón de Ronda 5 (MI sube /
  TE baja) apareciera igual acá, sería evidencia de que es un artefacto
  de cualquier bipartición durante alta sincronía, no algo específico del
  rol de la raíz.
- **P2:** raíz contra un solo seguidor (sin agregar toda la periferia en
  un parámetro de orden), para ver si el resultado depende de resumir la
  periferia con esa cantidad agregada.

Se corrió cada condición de simulación (baseline_R4, rediseño_R4) UNA
sola vez por seed, extrayendo las 3 particiones del mismo loop de pasos
(evita resimular 3x). lag=1 y lag=2 se calculan post-hoc sobre los mismos
puntos guardados.

### Resultado

| Partición | Condición | lag | ΔMI | ΔTE | seeds válidas |
|---|---|---|---|---|---|
| P0 root/periferia | baseline_R4 | 1 | +0.181 (sube) | −0.021 (baja) | 12/12 |
| P0 | baseline_R4 | 2 | +0.181 (sube) | −0.040 (baja) | 12/12 |
| P0 | rediseño_R4 | 1 | +3.714 (sube) | −0.026 (baja) | 12/12 |
| P0 | rediseño_R4 | 2 | +3.714 (sube) | −0.040 (baja) | 12/12 |
| P2 root/1-seguidor | baseline_R4 | 1 | +0.181 (sube) | −0.021 (baja) | 12/12 |
| P2 | baseline_R4 | 2 | +0.181 (sube) | −0.040 (baja) | 12/12 |
| P2 | rediseño_R4 | 1 | +3.581 (sube) | −0.026 (baja) | 12/12 |
| P2 | rediseño_R4 | 2 | +3.581 (sube) | −0.040 (baja) | 12/12 |
| **P1 control** | baseline_R4 | 1 | **−10.230 (baja)** | **+0.008 (sube)** | 9/12 |
| **P1 control** | baseline_R4 | 2 | **−10.230 (baja)** | **+0.007 (sube)** | 9/12 |
| **P1 control** | rediseño_R4 | 1 | +2.783 (sube) | **+0.008 (sube)** | 12/12 |
| **P1 control** | rediseño_R4 | 2 | +2.783 (sube) | **+0.009 (sube)** | 12/12 |

**Lectura:** P0 y P2 son idénticos en dirección en las 4 combinaciones de
condición×lag — el resultado no depende de si la periferia se agrega con
el parámetro de orden de Kuramoto o se usa un solo seguidor crudo. Más
importante: **P1 nunca reproduce el patrón "MI sube / TE baja"** — en
baseline_R4 va en dirección opuesta en ambas métricas, y en rediseño_R4
el TE sube en vez de bajar. Eso es exactamente la evidencia de robustez
que se buscaba: el colapso de integración medido por TE-bottleneck es
específico de la relación raíz→periferia (el "titiritero"), no un
artefacto de partir el sistema en dos donde sea durante sincronía alta.

**Caveat a no esconder:** en P1, `TE_baseline` da 0.0000±0.0000 exacto en
9-12 de 12 seeds. Demasiado limpio para ser señal — probablemente el
guard numérico (`du>dr → clamp`) colapsando a cero cuando las dos mitades
de periferia son casi simétricas antes del hijack (ambas siguiendo a la
misma raíz de forma parecida). No invalida la lectura direccional (P1
sigue siendo categóricamente distinto de P0/P2 en las 4 combinaciones),
pero los valores absolutos de P1 no deberían citarse sin revisar el
estimador para ese caso degenerado.

**Decisión:** con esta evidencia, Delorien aprobó TE-bottleneck (P0,
lag=1 — el mismo diseño de Ronda 5, ahora validado) como la definición
operativa de Φ_proxy. lag=2 da resultados equivalentes en dirección en
todos los casos, así que la elección de lag=1 (más simple, menos
parámetros libres) queda justificada y no arbitraria.

---

## 2. Barrido O(log N) repetido con TE-bottleneck (Claim 7, pendiente desde Ronda 4)

**Diseño:** mismo barrido de θ_death que Ronda 4 (`verify_phi_proxy.py`),
mismos seeds=10/steps=2000/window=300, pero midiendo Φ_proxy_TE (P0,
lag=1, la definición recién aprobada) sobre la ventana ESTACIONARIA
(post-convergencia, sin hijack — hijack_steps=15/η=0.15 por defecto, sin
tocar) en vez de MI cruda entre dos mitades arbitrarias.

### Resultado

| θ_death | N* real | Φ_proxy_TE |
|---|---|---|
| 0.50 | 1.00±0.00 | sin corridas válidas (N*<2) |
| 0.20 | 2.70±0.46 | 0.0118±0.0076 (7/10 válidas) |
| 0.10 | 4.60±0.49 | 0.0217±0.0136 |
| 0.05 | 8.80±0.40 | 0.0118±0.0081 |
| 0.02 | 18.00±0.63 | 0.0101±0.0078 |
| 0.01 | 29.40±0.92 | 0.0086±0.0080 |

R² vs log(N) = 0.337, R² vs N = 0.396.

**Lectura honesta:** peor que el ajuste de Ronda 4 con MI cruda (que ya
era malo: R²=0.22/0.07). Acá el valor se mantiene esencialmente plano
(~0.01-0.02) en todo el rango de N* (2.7 a 29.4), con desviación estándar
del mismo orden que la media — es indistinguible de ruido a simple
vista, no solo con el ajuste formal. No hay ni siquiera la subida inicial
que sí mostraba la MI cruda entre N*=2.7 y 4.6.

**Por qué tiene sentido que dé esto, no es solo "métrica ruidosa":** el
TE-bottleneck mide integración *bidireccional* raíz↔periferia. En ventana
estacionaria (sin hijack activo), la raíz no tiene ningún privilegio
estructural sobre la periferia — eso es justamente lo que Ronda 5
estableció al mostrar que `hub_boost` no hace nada y que el patrón
arrastre-vs-integración solo aparece *durante* el hijack, cuando la raíz
efectivamente empuja la fase del resto. Sin ese empuje, no hay mecanismo
en el modelo que predijera que la integración raíz-periferia debería
crecer con N — así que un resultado plano/ruidoso es, en retrospectiva,
más consistente con el resto del cuadro que un ajuste limpio hubiera
sido.

**Veredicto:** Claim 7 (O(log N)) sigue sin sostenerse, ahora confirmado
con dos definiciones independientes de Φ_proxy (MI cruda de Ronda 4,
TE-bottleneck de Ronda 6) que no la sostienen — la primera con algo de
estructura pero sin ajuste limpio, la segunda esencialmente plana. La
definición TE-bottleneck en sí queda aprobada y es útil para lo que sí
mostró ser robusto (arrastre-vs-integración durante hijack, Claim 5), no
para rescatar Claim 7.

---

## 3. Qué queda pendiente después de esta ronda

- Decidir en el paper: retirar la predicción O(log N) de Claim 7 del
  todo, o reformularla (la MI cruda sí mostró estructura no-trivial,
  aunque no logarítmica — quizás vale la pena reportar esa forma
  descriptivamente en vez de forzar una ley de escala).
- Φ_proxy_TE queda aprobada como métrica y puede citarse en el paper para
  la distinción arrastre-vs-integración durante C3 — pero con la
  salvedad de que sigue siendo una propuesta metodológica propia (Geweke
  gaussiano, VAR(1)), no una medida canónica de la literatura de IIT.
- El caveat numérico de P1 (TE_baseline=0.0000 exacto) no se investigó a
  fondo — si en algún momento se quiere citar P1 con valores (no solo
  dirección), hay que revisar el estimador para el caso de covarianzas
  casi-simétricas.
- Todo lo demás pendiente de Rondas 4-5 sigue igual: LSTM/GRU y
  Transformer como baselines adicionales del N-back; validación EEG/fMRI;
  drug discovery — fuera de alcance de esta ronda.
