# AUDIT NOTES — Ronda 5 (2026-07-23/24)

Continuación directa de Ronda 4. Punto de partida: la sesión anterior
terminó a mitad de una decisión de diseño en 3 partes (analogía
tálamo↔root, ver hilo de chat), con acuerdo en las 3 pero sin haber
guardado el código ni corrido los números finales. Esta ronda implementa
y corre esas 3 decisiones.

**Antes de citar nada de esta ronda:** igual que Φ_proxy en Ronda 4, la
partición root/periferia y la métrica TE-bottleneck de abajo son una
propuesta de diseño que armé para continuar el hilo donde quedó, no algo
que Delorien ya haya revisado y aprobado. Necesita luz verde antes de
entrar al paper.

## 0. Qué se implementó

1. `thalamic_model.py` — `ThalamicDSCN_G_v3(DSCN_G_v3)`: subclase que
   agrega `hub_boost`, reubicado en `_apply_hijack_pull` (el mecanismo
   que domina la dinámica del hijack), NO en la matriz de Kuramoto
   basal (donde se había puesto por error al final de Ronda 4 — ahí no
   tenía efecto observable porque `_apply_hijack_pull` es un tirón
   directo, aparte de la matriz, y la ignora). `eta_eff = min(1.0,
   eta_hijack·hub_boost)`. Núcleo (`verify_dscng_v3.py`) sin tocar.
   Smoke test: `hub_boost=1.0` reproduce `DSCN_G_v3` byte-a-byte
   (300 pasos, seed=0) — ✓ pasa.

2. `verify_phi_proxy_v3.py` — Φ_proxy rediseñado con partición
   root/periferia (en vez de mitades arbitrarias) y una métrica nueva,
   transfer entropy gaussiana (Geweke 1982) tomando el **mínimo** de las
   dos direcciones de flujo (root→periferia, periferia→root) como
   "integración genuina" — en vez de información mutua cruda. Se
   reportan ambas métricas (MI cruda de Ronda 4 y TE-bottleneck nueva)
   sobre la misma partición, comparando ventana pre-hijack vs.
   durante-hijack.

3. `verify_hub_boost_fix.py` — repite la comparación de Ronda 4
   ("¿el boost mueve el rise_rate de C3?") con el hub_boost ya reubicado.

## 1. Φ_proxy: MI cruda sube, TE-bottleneck baja — la distinción se sostiene

**Corrida canónica (seeds=15, steps=2000, ventana=300, 4 condiciones
iguales a las que se habían anunciado en el chat anterior):**

| Condición | ΔMI cruda | ΔTE-bottleneck |
|---|---|---|
| DSCN_G_v3 (baseline R4: θ=0.10, hijack=15, η=0.15) | **+0.119** (sube) | **−0.023** (baja) |
| DSCN_G_v3 (rediseño R4: θ=0.01, hijack=150, η=0.80) | **+3.837** (sube) | **−0.023** (baja) |
| Thalamic hub_boost=5.0 (baseline R4) | **+2.330** (sube) | **−0.017** (baja) |
| Thalamic hub_boost=5.0 (rediseño R4) | **+5.044** (sube) | **−0.023** (baja) |

Consistente en las 4 condiciones, con ventanas de hijack válidas (≥30
muestras) en 15/15 seeds en todos los casos. La MI cruda replica (y con
esta partición motivada estructuralmente, refuerza) el hallazgo
contraintuitivo de Ronda 4: sube durante el hijack en vez de caer. La
métrica TE-bottleneck, en cambio, **cae en las 4 condiciones** —
consistente con la hipótesis planteada al cierre de Ronda 4: lo que sube
es el arrastre (root dicta la fase de la periferia, por eso son muy
predecibles entre sí — MI alta), no la integración genuina (que exige
flujo de información significativo en ambas direcciones — y ahí el
"titiritero" no recibe nada de vuelta de la "marioneta", por eso el
mínimo de las dos direcciones colapsa).

**Lectura honesta:** esto es evidencia a favor de que la distinción
arrastre-vs-integración es real y medible en este modelo, no solo una
narrativa post-hoc — pero es sobre una métrica que yo definí esta misma
ronda, sin revisión previa, y con un solo diseño de partición (root vs.
periferia vía parámetro de orden de Kuramoto). No se probó robustez
frente a otras particiones o formulaciones de transfer entropy (p.ej.
condicionando en más lags, o normalizando distinto). Tampoco cambia el
veredicto de Claim 5 (C3) — el hallazgo es sobre una métrica nueva
propuesta para Claim 7, no rescata la claim original de "phase hijacking
= sincronización patológica del grupo completo".

## 2. hub_boost reubicado correctamente: aun así, CERO efecto en rise_rate — hallazgo de saturación, no bug

Se esperaba que, arreglado el lugar donde actúa el boost, subir
`hub_boost` sí moviera el rise_rate de C3 (a diferencia del intento
fallido de Ronda 4). **No fue así — y esta vez la razón es interesante,
no un error de ubicación:**

| Config | hub_boost | eventos | ΔPLV_mean | rise_rate |
|---|---|---|---|---|
| baseline R4 (θ=0.10, hijack=15, η=0.15) | — (sin boost) | 1129 | −0.006 | 0.7% |
| baseline R4 | 1.0 (control) | 1129 | −0.006 | 0.7% |
| baseline R4 | 2.0 | 1129 | −0.006 | 0.7% |
| baseline R4 | 5.0 | 1129 | −0.006 | 0.7% |
| rediseño R4 (θ=0.01, hijack=150, η=0.80) | — | 43 | −0.201 | 30.2% |
| rediseño R4 | 1.0 / 2.0 / 5.0 | 43 | −0.201 | 30.2% |

Idéntico al tercer decimal en todos los niveles de boost — no es azar.
Diagnóstico (ver `/tmp` diagnóstico de esta ronda, reproducible):
`plv_intra_group()` (sincronía ENTRE seguidores, sin la raíz) ya alcanza
R≈0.96–1.0 a los 2-3 pasos de iniciado el hijack incluso con
`hub_boost=1.0` (η_eff=0.15) — el grupo de seguidores es tan chico
(3-4 nodos en la config baseline) que converge a consenso casi
instantáneo bajo cualquier pull coherente hacia un blanco común (la fase
de la raíz), y con `hub_boost=5.0` converge todavía más rápido pero al
mismo techo (R≈1.0). Como `plv_after` se mide recién al FINAL de la
ventana de hijack (15 o 150 pasos), y ambos casos ya llegaron al techo
mucho antes de esa marca, no hay margen donde el boost pueda mostrarse en
la métrica.

**Esto profundiza el diagnóstico de Ronda 4, no lo contradice:** ya se
sabía que la población insuficiente era el cuello de botella. Este round
agrega que **ni siquiera la fuerza del pull importa una vez que hay
población — el techo se toca casi de inmediato**. La única palanca que
demostradamente mueve el rise_rate es la que ya se había encontrado en
Ronda 4: más población activa (θ_death más bajo) + ventana de hijack más
larga (para que el evento tenga tiempo de ocurrir y ser sostenido, no
para que el pull "alcance" — ya alcanza altísimo casi de inmediato).
Aumentar `hub_boost` por sí solo, con población y duración fijas, es una
palanca sin efecto demostrado.

## 3. Qué significa esto para el paper (recomendación, no aplicado a claims_falsifiable.md todavía)

- Claim 5 (C3): veredicto sin cambios (❌ no verificado a los parámetros
  originales; ✓ el rediseño de Ronda 4 sigue siendo la única palanca
  demostrada). Agregar una línea: "reforzar el pull sobre seguidores
  individuales (hub_boost) no mueve la métrica una vez fijados
  población/duración — el techo de sincronía se toca casi de inmediato
  incluso sin boost."
- Claim 7 (Φ_proxy): sigue sin poder citarse como verificado — pero ahora
  hay dos definiciones candidatas con resultados opuestos (MI cruda sube,
  TE-bottleneck baja) más una tercera pregunta abierta (¿cuál es la
  "correcta" para lo que el paper quiere decir con Φ?). Vale la pena
  decidir esto antes de seguir puliendo el número, no después.
- La analogía "hijacking talámico" queda parcialmente sostenida: el
  patrón cualitativo (arrastre sube, integración cae) es exactamente lo
  que predice la neurociencia de crisis de ausencia — pero el modelo NO
  necesitó privilegio estructural real del root (`hub_boost`) para
  mostrarlo; el efecto ya estaba presente en `DSCN_G_v3` sin tocar nada.
  Eso es, si acaso, una buena noticia (el mecanismo es más robusto de lo
  que parecía necesitar), pero también significa que "tálamo" como
  privilegio estructural queda sin evidencia de que agregue algo — habría
  que decidir si se menciona como analogía puramente cualitativa o se
  retira.

## 4. Qué queda pendiente después de esta ronda

- Aprobar o reemplazar la definición TE-bottleneck de Φ_proxy antes de
  usarla en cualquier parte citable del paper (igual que la MI de Ronda
  4, nunca fue aprobada formalmente).
- Repetir el barrido de Ronda 4 (Φ_proxy vs. N, la pregunta original de
  Claim 7 sobre escalado O(log N)) con la métrica TE-bottleneck en vez de
  MI cruda — no se hizo esta ronda, solo se comparó pre/durante-hijack.
- Probar si alguna otra palanca (más follower group, hijack sostenido
  pero con población intermedia entre baseline y rediseño extremo) mueve
  el techo de saturación encontrado en §2, o si es un techo estructural
  del modelo (Kuramoto con pull hacia un único blanco converge rápido
  casi por diseño, independientemente de N pequeño).
- Todo lo que ya estaba pendiente de Ronda 4 sigue igual (LSTM/GRU y
  Transformer como baselines adicionales; validación EEG/fMRI; decidir
  si "tálamo" se queda como analogía cualitativa o se retira del todo).
