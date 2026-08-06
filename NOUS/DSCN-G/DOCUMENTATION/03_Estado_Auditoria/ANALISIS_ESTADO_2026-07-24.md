# DSCN-G — Análisis de estado (2026-07-24, cierre de Ronda 6)

Este documento resume, para todo el paquete `DSCN_G_Theory_Design_v1`,
qué está listo para escribirse en el paper tal cual, qué necesita
corrección de texto, qué se cayó, y qué sigue realmente pendiente.
No repite el detalle numérico completo — eso vive en
`02_Source_Round5/01_DSCN-G_Paper/auditoria/claims_falsifiable.md` y en
`AUDIT_NOTES_ROUND{1..6}.md`. Esto es el mapa para decidir dónde poner
el esfuerzo de escritura ahora.

---

## 1. Lo que tenemos (listo o casi listo para el paper)

### ✅ Verificado, citable tal cual
- **Claim 2 (ω Alignment):** alignment=1.0000, mejor que lo reclamado.
- **Claim 6a (N_ss* del N-back):** 9.50±1.02, reproduce casi exacto.
- **Claim 11b (baseline RNN vainilla):** DSCN-G sostiene d'≈0.8-1.0 hasta
  20-back; el RNN colapsa a azar desde ~7-back. Comparación pedida
  explícitamente por revisión externa — resuelta.
- **Claim 1, sub-claim (iii) — maximalidad de N\*:** verificada con
  simulación real (protocolo de inyección al umbral, 100% podado de
  vuelta en 3 condiciones de N_init). El resto de Claim 1 (N_ss* en
  función de N_init) también se sostiene, solo necesitaba corrección de
  qué cifra le pertenece a qué claim (ver más abajo).

### ⚠️ Correctos en el fondo, necesitan ajuste de texto (no de código)
- **Claim 1:** la cifra "N_ss*=9.5±1.0" que el paper le atribuía a T1 en
  realidad es de Claim 6a (N-back). El valor real de T1 es N_ss*≈4-4.8
  según N_init. Es un error de trasplante de cifra entre secciones, fácil
  de corregir en la prosa.
- **Claim 3 (consenso de fase T3):** 100% "consenso" solo si se cuenta
  una rama de respaldo laxa (R≥0.5) igual que la estricta (R≥0.9). La
  cifra estricta real es 76.7% (23/30). 0 casos bimodales (no 7% como
  decía). Hay que decidir qué criterio reportar y ajustar el texto — el
  fenómeno en sí no está en duda.
- **Claim 6b/6c (curva de d' del N-back):** la forma cualitativa
  ("sin escalón discreto") se sostiene. Los valores puntuales que citaba
  el borrador (d'(10-back)=3.12, d'(15-back)=2.78) no se reproducen — los
  reales son 3.92 y 3.90. Reemplazar cifras, no reescribir la conclusión.

### 🔬 Metodología nueva, aprobada, lista para citarse con sus salvedades
- **Φ_proxy_TE (TE-bottleneck, partición root/periferia, VAR(1)):**
  aprobada en Ronda 6 tras pasar una prueba de robustez de 3 particiones
  × 2 lags (el control negativo P1 muestra el patrón opuesto, lo cual
  es la evidencia que la valida). Útil para la distinción
  arrastre-vs-integración durante el hijack (ver Claim 5 más abajo) — no
  rescata Claim 7 (ver sección 3).

---

## 2. Lo que se cayó o se retiró (no citar en el paper)

- **Claim 5 (C3 / Phase Hijacking) a los parámetros de diseño
  originales:** ❌ no verificado. Mean ΔPLV≈−0.007 (no −0.46), 0.9% de
  triggers con el efecto reclamado (no 100%). Esto no cambió en ninguna
  ronda posterior — sigue siendo el veredicto de fondo.
- **Analogía "tálamo / hub_boost":** retirada formalmente en Ronda 6 por
  decisión explícita. No mostró efecto en ninguna configuración probada
  (0.7% y 30.2% de rise_rate, idéntico con y sin boost), y Ronda 5
  estableció la razón mecánica (techo de saturación de
  `plv_intra_group()` a 2-3 pasos de iniciado el hijack — no queda
  margen donde un pull más fuerte se pueda manifestar). El código
  (`thalamic_model.py`) se conserva en el repo por trazabilidad, pero no
  debe aparecer en el paper ni como mecanismo ni como analogía
  cualitativa.
- **Claim 7, predicción O(log N):** no se sostiene con NINGUNA de las
  dos definiciones de Φ_proxy probadas hasta ahora (MI cruda de Ronda 4,
  TE-bottleneck de Ronda 6 — ver sección 3). Esto no es "falta más
  evidencia" — son dos intentos independientes, con metodologías
  distintas, que apuntan al mismo lugar: la predicción tal como está
  planteada no tiene sustento en los datos.

---

## 3. Lo que queda pendiente, con la evidencia parcial que ya existe

### Rediseño de C3 — evidencia parcial, sin cerrar
El único mecanismo que demostradamente mueve el rise_rate es
población+duración (θ_death bajo + hijack largo): 0.7%→30.2% en la
config más agresiva probada. Sigue lejos de "la norma" del paper
original, y a esos parámetros (hijack_steps=150 = 10x el diseño
original) ya es dudoso que sea el mismo fenómeno. **Decisión pendiente**
de tu parte: (a) reportar el rediseño como evidencia parcial de que el
mecanismo "existe pero es débil", con Claim 5 sin cambiar de veredicto, o
(b) seguir explorando parámetros más agresivos (la curva no había tocado
techo cuando se dejó de barrer en Ronda 4).

### Claim 7 — qué hacer ahora que las dos definiciones fallan
Con TE-bottleneck (aprobada, la más confiable de las dos), el resultado
en ventana estacionaria es prácticamente plano y ruidoso en todo el
rango de N* (2.7 a 29.4) — ni siquiera hay la subida inicial que sí
mostraba la MI cruda. La razón de fondo, ya establecida por Ronda 5: sin
hijack activo, la raíz no tiene privilegio estructural sobre la
periferia, así que no hay mecanismo en el modelo que predijera
integración creciente con N en reposo. **Dos caminos, no exploramos
ninguno todavía:**
  - Retirar la predicción O(log N) del paper — es la opción más honesta
    dado que dos metodologías independientes coinciden en no sostenerla.
  - Reformular la pregunta: la MI cruda de Ronda 4 sí mostró estructura
    no-trivial (sube, meseta, cae) aunque no logarítmica — podría
    reportarse esa forma descriptivamente, sin forzarla a una ley de
    escala, si te interesa preservar algo de esta línea.

### Caveat técnico sin resolver
En la prueba de robustez de Ronda 6, la partición de control P1 dio
TE_baseline=0.0000±0.0000 exacto en casi todos los seeds — sospechoso de
ser un artefacto numérico del guard `du>dr` en covarianzas casi
simétricas, no señal real. No afecta ninguna conclusión ya sacada (la
lectura direccional de P1 se sostiene igual), pero si en algún momento
se quiere citar P1 con valores absolutos (no solo dirección), hay que
revisar el estimador para ese caso degenerado primero.

### Fuera de alcance de todas las rondas hasta ahora (sin tocar)
- Baselines LSTM/GRU y Transformer para el N-back (solo se comparó
  contra RNN vainilla — la comparación justa y completa los necesita).
- Validación EEG/fMRI (Claim 8) — ninguna ronda tocó esto, sigue siendo
  trabajo futuro puro.
- Claims 9 y 10 (NCC formalmente completo, conexión con drug discovery)
  — especulativos por diseño, sin pretensión de verificación empírica en
  este ciclo.

---

## 4. Resumen ejecutivo (una tabla)

| # | Claim | Estado | Qué falta, si algo |
|---|---|---|---|
| 1 | T1 homeostasis + maximalidad | ✅ / ⚠️ texto | corregir qué cifra va en qué sección |
| 2 | ω alignment | ✅ | nada |
| 3 | Consenso de fase T3 | ⚠️ texto | decidir criterio (23/30 vs 30/30) |
| 5 | C3 phase hijacking | ❌ (parámetros originales) | decisión: reportar rediseño parcial o seguir explorando |
| 6a | N_ss* N-back | ✅ | nada |
| 6b/6c | Curva d' N-back | ✅ forma / ⚠️ cifras | reemplazar valores puntuales |
| 7 | Φ_proxy O(log N) | ❌ (dos métricas independientes) | decisión: retirar predicción o reformular |
| 8 | EEG/fMRI | ❌ pendiente | fuera de alcance, trabajo futuro |
| 9 | NCC completo | ⚠️ especulativo | sin cambios, no pretende verificarse |
| 10 | Drug discovery | ⚠️ especulativo | sin cambios, no pretende verificarse |
| 11b | Baseline RNN | ✅ | agregar LSTM/GRU/Transformer sería un plus, no bloqueante |
| — | Tálamo/hub_boost | 🗑️ retirado | no debe entrar al paper |
| — | Φ_proxy_TE (metodología) | ✅ aprobada | citable con sus salvedades (propuesta propia, no canónica de IIT) |

**Lo más urgente para avanzar el paper:** las correcciones de texto
(Claims 1, 3, 6b/6c) son mecánicas y no requieren más cómputo — se pueden
aplicar ya. Las dos decisiones reales pendientes son C3 (§3, primer
párrafo) y Claim 7 (§3, segundo párrafo); ninguna de las dos necesita más
simulación para decidirse, son llamadas de juicio sobre qué tan lejos
seguir empujando un resultado parcial vs. cuándo cerrar la puerta.
