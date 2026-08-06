---
name: sgm-experiment-flow
description: Flujo repetible para el proyecto SGM-CORE (Synaptic Graph Model) en el vault nexus-vault. Cubre (1) hygiene del repo y unificación de registries, (2) crear/correr un experimento exp_SGM_00XX test-first con negative control, (3) registrar en el registry canónico de results/, (4) actualizar README + roadmap, (5) pushear a GitHub Rylow999/SGM-CORE vía github_push_sgm.py. Usar cuando Luciano pida "seguir con el próximo experimento", "documentá y pushea", o tareas de hygiene del repo SGM.
---

# SGM Experiment Flow (Nexus Vault)

Proyecto: SGM-CORE en `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/`.
Repo GitHub: `Rylow999/SGM-CORE`. Push vía `/data/user/0/com.hermesagent.android/files/home/github_push_sgm.py`
(la CLI `git` NO está instalada en el Android; todo se hace por API GitHub con token por mensaje, NO persistir).

## Entorno crítico (Android)
- El `read_file`/`patch` de Hermes NO leen `/sdcard` (FUSE). Para leer/editar archivos del vault usar SIEMPRE
  `su -c 'cat ...'` / `sed` / `python3` por terminal. `patch` de Hermes SÍ funciona en
  `/data/user/0/com.hermesagent.android/files/home/`.
- Python: `export LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib; PY=/data/data/com.hermesagent.android/files/usr/bin/python3`
  (sin eso da "libandroid-support.so not found").
- Token GitHub aparece como `ghp_...E` — NUNCA incluirlo en archivos ni en salida del usuario; pasarlo por env `GH_TOKEN`
  o como arg efímero del push script. Reemplazar con [REDACTED] en cualquier transcript.
- PDFs y corpus van en `lit/papers/` y `lit/corpus/` — AMBOS en `.gitignore` (fuera de git). El `.gitignore` NO
  retrocede lo ya subido por API PUT; para borrar del remoto hay que DELETE por API.

## Regla de oro de auditoría (Luciano exige: "no emocionarse al pedo")
TODO experimento debe tener: ground truth + baseline idéntico + negative control + smoke test antes de afirmar PASS.
Verificar el `pass` en el JSON de resultado, no creer el print. Si un test falla, es fallo honesto, no se maquilla.

## ANTI-PAPER-VISION: el negative control y la comparación DEBEN ejecutar cómputo real (lección dura, auditoría 0030/0028/0021/0018/0019)
Luciano detectó (y el agente confirmó contra el código) que VARIOS experimentos "pasaban" porque la comparación
o el control negativo estaban HARDCODEADOS, no medidos. Esto es el "paper-vision trap" que el user odia: el resultado
positivo se sostiene por una línea de código que GARANTIZA el veredicto, no por cómputo. No es lo mismo que un bug de
diseño del mundo (embedding no métrico, etc.); es una FRAUDE de medición. Reglas OBLIGATORIAS:

1. **El "plano" / "baseline sin la propiedad" debe ser un MODELO REAL que corra el mismo pipeline**, no un `return False`.
   - ANTI-PATRÓN (0030 `tick_relational_core.plan_from`): `if not use_roles: return False` → el "tick plano no puede"
     queda garantizado por construcción, NO por cómputo. El HRR+roles SÍ funciona de verdad, pero la afirmación
     "el plano no puede" es FALSA hasta que le des un `plan_from_plano()` real (distancia Euclidiana, como 0023) y lo midas.
   - ANTI-PATRÓN (0028 `recover_nested_3`): `if not use_roles: return None` → `acc_plano` queda 0.0 por el `return None`,
     no porque el plano falle. El `if acc_plano is not None` nunca se cumple → 0 por construcción.
   - FIX: implementar la variante plana REAL y medir. Si de verdad falla → el resultado se sostiene por cómputo. Si resuelve
     → el "B" es más débil y se reporta así. NUNCA dejar `return False`/`return None` como "resultado" del control.

2. **Los scores de los casos de control NO se asignan a mano.** ANTI-PATRÓN (0021 Caso B aislamiento):
   `scoreB = 0.0` escrito a mano, luego `aislamiento_ok = (scoreB == 0.0)` → tautología. Los Casos A/C/D SÍ llaman
   `attraction_local`; el B no. FIX: calcular `scoreB` con la MISMA función sobre el nodo aislado (sin aristas) y que dé ~0
   por cómputo, no por asignación.

3. **Los "frenos" / "marcas a fuego" no son tablas de reglas `if nombre_mutación=="x"`.** ANTI-PATRÓN (0018 Casos C/D):
   `apply_mutation` devuelve `(s, False, "borrar tipo de arista (IRREVERSIBLE...)")` sin ejecutar nada; luego
   `marca_fuego = (not revC)` → True por construcción. Caso D: el propio código pone `THETA_REFUT=999` y luego pregunta
   `THETA_REFUT>=999`. Los Casos A/B (sí corren `evaluate` real) son legítimos; C/D son placeholder. FIX: `apply_mutation`
   EJECUTA la mutación sobre el spec vivo y un `check_invariants(spec)` EVALÚA el spec resultante; la marca a fuego y el
   freno deben EMERGIR de chequear el spec mutado, no de `if mutation=="delete_edge_type"`.

4. **Las "señales internas" no se hardcodean.** ANTI-PATRÓN (0019 T-SEN-02): `intero(E_root, ...)` con `E_root` puesto a
   mano (0.2 y 0.9) → `if E_root > 0.8` solo confirma que un if branchea. No hay nada "emergente". FIX: derivar `E_root`
   de una señal REAL (energía/saturación del ω del root, dolor acumulado, etc.) y medir que la política reacciona a ESA señal.

5. **CHECKLIST de auditoría antes de afirmar PASS (correr SIEMPRE al revisar un experimento ajeno o propio):**
   - grep del código del experimento por: `return False`, `return None`, `= 0.0` asignado a una variable de "score/éxito",
     `if <nombre_cadena> ==`, y valores numéricos metidos a mano en la función de métrica.
   - **TRAMPA DE REGLA INYECTADA EN EL APRENDIZ (variante de la regla 10, caso exp_SGM_0056, 2026-08-04):**
     cuando el experimento mide "composición emergente bajo ILM / presión de transmisión", revisar si el
     método del aprendiz (`infer_rule`, `learn`, etc.) CONOCE LA ESTRUCTURA DE MAPEO. ANTI-PATRÓN: el aprendiz
     itera `reg_map[ra[0]][msg[0]]+=1` (región→posición 0, distancia→posición 1, tipo→posición 2) → la
     gramática composicional está HARDCODEADA en el método del aprendiz, no la descubre. El TopSim 1.0 resultante
     es regla INYECTADA, MISMA falla que 0049d (la respuesta estaba en el mecanismo, no emergió de la presión).
     El cómputo es real y el aprendiz "infiere", PERO la FORMA de la inferencia (qué rasgo va en qué posición)
     se la diste. FIX: el aprendiz debe ser GENÉRICO (no sepa la estructura posicional) y la estructura debe
     EMERGIR de la transmisión, o el resultado se etiqueta ACLARACION_REQUERIDA / PROPUESTA_DE_DISENO_NO_SUSTRATO,
     no HALLAZGO_POSITIVO_FUERTE. Citar ese 1.0 como "el sistema compone pleno por emergencia" es el error de 0049d.
     Nota: 0056 y 0055a responden preguntas DISTINTAS (0055a=¿emerge con aprendiz genérico? ~0.35; 0056=¿tiene el
     sustrato techo si le das inferir la regla exacta? no, 1.0). Son complementarios; no confundir.
   - Para cada "control negativo", preguntarse: ¿corre el mismo pipeline que el caso positivo? Si la respuesta es "no,
     devuelve X fijo", el control es inválido.
   - Re-correr y verificar que el número del control sale del cómputo, no de una constante.
   Ver `references/audit_pass_by_construction.md` para la receta concreta y los diffs exactos de 0030/0028/0021/0018/0019.

6. **El control puede estar amañado DE DOS FORMAS (lección 0030, auditoría 2026-08-03):** no alcanza con
   quitar el `return False`/`return None`. El ENTORNO puede estar armado para que el control pase IGUAL
   con código real. En 0030 había una **arista de cruce FÍSICA** (`edges[llave].append((meta_G1,0))`) además
   del `return False`: aunque hubieras implementado `plan_from_plano()` real (PPR Euclidiana), el plano
   habría LLEGADO a meta_G1 porque la arista existía. FIX honesto: el cruce debe vivir SOLO en `rel_mem`
   HRR (bind del rol de meta), NUNCA como arista física. Al reparar un control negativo, preguntarse:
   "¿incluso con cómputo real el control daría el veredicto que el setup del entorno espera?" Si sí →
   el entorno también está amañado. Quitar AMBAS cosas.

7. **Un `check_invariants` INGENUO puede dejar pasar la mutación mala (lección 0018 Caso C, 2026-08-03):**
   al reparar C/D con `apply_mutation` real + `check_invariants`, el primer intento sólo chequeaba
   `edge_types` NO VACÍO. Borrar 1 de 5 tipos NO vacía el set → `check_invariants` devolvió [] → el sistema
   APLICABA la mutación (falso positivo: el resultado original "MARCADA_A_FUEGO" era doblemente trucho).
   El veredicto honesto requirió comparar `edge_types` contra el **BASE** (`edge_types` es INMUTABLE por
   diseño → cualquier diferencia vs spec original viola). Regla: la inmutabilidad / irreversibilidad se
   detecta por DIFERENCIA vs base, no por estado absoluto. Un `check_invariants` que sólo mira estado
   absoluto no captura "borró algo que no debía".

8. **La señal DERIVADA debe VARIAR (lección 0019 T-SEN-02, 2026-08-03):** al derivar `E_root` de una señal
   real, confirmar que la señal VARÍA entre los casos. El primer intento usó la NORMA de la proyección HDC
   (`project()` normaliza ω a norma 1.0 SIEMPRE) → `E_root = 0.5` para señal suave Y fuerte → no
   discriminaba → el test fallaba. FIX: usar la INTENSIDAD de la SEÑAL CRUDA (norma del input: impulso pico
   5 vs audio 0.1) → 0.122 vs 1.0. Regla: antes de derivar una variable interna de X, verificar que X toma
   valores distintos en los casos que el test debe separar; si X es constante por construcción (ej.
   normalización), no sirve.

9. **FLUJO DE AUDITORÍA (preferencia de Luciano, 2026-08-03):** cuando el user pide "revisá que esté todo
   bien evaluado" o auditar varios experimentos, IR UNO POR UNO, dar RESUMEN al final, y ESTAR ATENTO a
   instancias del MISMO patrón en OTROS experimentos. El defecto suele repetirse por clase:
   - `use_roles=False` → `return False`/`return None`: 0030 Y 0028 comparten este patrón (misma firma /
     módulo). Reparar uno suele requerir reparar el otro.
   - asignación a mano de score / tabla de reglas `if nombre==`: 0021 (Caso B `scoreB=0.0`), 0018 (C/D).
   - señal interna hardcode: 0019 (T-SEN-02). No reparar SOLO el experimento señalado; grep el resto del
     vault por los mismos anti-patrones (`return False`/`return None` en rama de control, `= 0.0` en
     variable de score, `if <string> ==`, valor numérico metido a mano en la métrica).

10. **LA TRAMPA ES MÁS AMPLIA QUE EL CHECKLIST DE AUDITORÍA (lección 0040/0041, 2026-08-03 — MISMA clase
   que la auditoría, pero en la "capa cognitiva superior"):** los anti-patrones 1-9 cubren `return False`,
   scores hardcodeados y señales internas fijas. PERO HAY UNA VARIANTE que no encaja en esos greps:
   **el autor escribe una FUNCIÓN CON REGLAS PROPIAS (árbol if-elif, tabla de pesos, fórmula con parámetros
   elegidos por el autor) y luego mide que "el sistema" se comporta según esas reglas.** El cómputo es
   real, pero la CONDUCTA EMERGE DE LA FUNCIÓN DEL AUTOR, NO DEL SUSTRATO SGM. Dos formas concretas:
   - 0040 `reflexion()`: árbol if-elif del autor decide quién "gana" el conflicto; T-DI-01 midió "la acción
     es coherente con la traza" — circular (la traza la generó la misma función). Garantizado por construcción.
   - 0041 `self_benefit = ALPHA*payoff + BETA*coherencia` con ALPHA=1.0/BETA=0.4/GAMMA=0.92 y tabla ECOL del
     autor: "A ayuda / B lastima" es consecuencia directa de esos números, NO del grafo/tick.
   REGLA OBLIGATORIA (filtro de "¿esto es del sistema?"): antes de afirmar PASS en una "capa superior"
   (discurso interno, moral, juicio, atención, metacontrol), preguntarse:
   (a) ¿La decisión sale de la DINÁMICA DE LOS CAMPOS del tick (transición por afinidad + pesos η/dolor/E
       sobre ω reales del grafo), o de una función/pesos/tabla que YO escribí?
   (b) Si mido "coherencia con la traza / con la decisión", ¿la traza la generó el MISMO código que decidió?
       Si sí → es circular, no mide mecanismo.
   (c) Si cambio ALPHA/BETA/GAMMA/ECOL por otros valores razonables, ¿el resultado se INVIERTE o es
       robusto? Si se invierte → el resultado es del autor, no del sistema.
   Si cualquiera es "del autor" → marcar como PROPUESTA_DE_DISENO_NO_SUSTRATO (verified=False), NO como
   resultado del SGM. El experimento sigue valiendo como DISCUSIÓN DE DISEÑO, pero no se cuenta como
   propiedad medida del sistema. Ver `references/substrate_vs_authored_design.md`.
11. **NEUTRALIZAR NOTAS PERSONALES EN RESULTADOS (lección 0041):** no mezclar el ejemplo personal del user
   ("caso realista de Luciano") dentro del JSON de resultado como si fuera una observación neutral del
   experimento. Eso hace ilegible el resultado. Separar: la observación empírica va en `result`; la
   motivación/discusión va en el roadmap o en la charla, no en el `notes` del result JSON.

12. **BANDERA ROJA POST-HOC SOBRE EXPERIMENTO YA REGISTRADO (flujo, 2026-08-04, caso exp_SGM_0056):**
    cuando Luciano (o la auditoría) detecta que un experimento YA en el registry fue sobre-afirmado
    (TopSim 1.0 reportado como "composición plena emergente" pero la regla estaba INYECTADA en el aprendiz,
    misma falla que 0049d), NO alcanza con charlarlo. Hay que CORREGIR EL REGISTRY, no solo la narrativa:
    - Cambiar `status` del experimento: HALLAZGO_POSITIVO_FUERTE → ACLARACION_REQUERIDA (o el que corresponda).
    - Reescribir `result`/`marco` diciendo la verdad (regla inyectada, pregunta distinta a 0055a, no es
      evidencia de emergencia).
    - Si otros experimentos citan al señalado como respaldo de "emergencia" (ej. 0058 citaba a 0056), matizar
      esas entradas también (quitar la cita o aclarar que es mecanismo de encode/decode controlado, no ILM).
    - Pushear el registry corregido. El veredicto honesto (0056 = regla inyectada, mismo error que 0049d)
      va al registry y al doc, no solo al chat.
    Regla de flujo: TODA bandera roja de Luciano que invalida un hallazgo YA registrado dispara la corrección
    del registry + push, no se queda en la conversación. Ver `references/decode_anidado_0059_0059b.md`.

HONESTIDAD al reportar: si el mecanismo propio (HRR+roles, aislamiento, etc.) SÍ hace cómputo real y PASÓ legítimamente,
pero su control negativo estaba hardcodeado, el veredicto del experimento es "INVÁLIDO HASTA REPARAR EL CONTROL", no
"PASS". Separar siempre "el mecanismo funciona" de "la comparación fue medida".

## Modo investigación abierta (PREFERENCIA DE LUCIANO — señal de flujo)
Para PROBLEMAS DE INVESTIGACIÓN ABIERTOS (nueva dirección, no tarea de rutina del roadmap) Luciano exige:
1. **DISCUTIR antes de codear.** Proponer hipótesis + **variable discriminante** (qué se mide y si realmente separa los modelos) + **negative control** ANTES de escribir una línea. No saltar a implementar.
2. **LEER la literatura del vault ANTES de codear (Luciano: "Primero leé el pdf y luego empezá").** Confirmar la
   fórmula canónica en `lit/papers/` (PyPDF2) antes de implementar un operador conocido. En 0027 el VSA survey
   Tabla 2 (p.10) confirmó bind=circular conv / unbind=circular corr; eso evitó inventar la fórmula. Si el PDF
   (ej Plate 2003) sale vacío en ecuaciones, el VSA survey 2022 SÍ extrae texto y tiene la tabla canónica.
2. **Tras cada test:** explicar en CRIOLLO qué salió, los bugs encontrados y corregidos, y la conclusión honesta.
Esto difiere de las tareas de rutina del roadmap (donde sí se puede ir directo). Si el user dice "discutamoslo antes de continuar" o "revisemos la mejor variable", entrar en modo discusión, no a coding.
Regla análoga persistente: en problemas abiertos, el agente propone hipótesis + variable discriminante + negative control y ESPERA visto bueno.
- **Charlar MIENTRAS corre (preferencia 2026-08-03):** Luciano pidió "vamos por c, mientras se ejecuta charlamos
  un poco más sobre el humano". El agente puede LANZAR el experimento (background o foreground corto) Y charlar el
  mecanismo humano en paralelo en el mismo turno, no secuencial bloqueante. Y "Actualizá roadmap, README, etc y
  sigamos" confirma que la actualización de docs es PARTE de la tarea, no un paso final opcional. No dejar la doc
  para el final (regla ya vigente desde 0031).

## Protocolo de tesis FILOSÓFICA / identidad (clase aparte, 2026-08-05)
Cuando el user quiere testear una afirmación METAFÍSICA ("identidad = proceso no snapshot",
NOUS_Filosofico §1, Parfit) NO se codifica directo. Aplicar el protocolo de 4 pasos de Luciano
(pre-registro con dos desenlaces por escrito). Resumen operativo:
1. **Paso 0:** escribir la predicción falsable ANTES de codear — nombrar un observable distinto entre
   las dos posturas. Si no hay observable distinto, es preferencia metafísica, no hipótesis.
2. **Paso 1:** buscar en lo YA construido un observable que dependa del RECORRIDO, no del estado final
   S(t) (que es instantáneo e indistinguible por definición tras un reset que copia). La vitalidad V
   es markoviana (V(t+1)=V·e^−γ) → NO sirve; la firma de trayectoria de φ en ventana W SÍ.
3. **Paso 2:** 4 condiciones (A continuo / B copiado / C degradado / D borrado), no las 3 de 0034.
   La tesis predice firma(A)≠firma(B) aunque pisadas(A)=pisadas(B)=0.
4. **Paso 3:** T-ID-0X pre-registrado con NC (firma(A)≠firma(RW)) y DOS desenlaces escritos ANTES de
   correr. Desenlace 2 (no difiere) = coincide con Parfit; reportar honesto, NO forzar.
5. **Paso 4:** el capítulo de discusión (ej NOUS_Filosofico §10) se escribe CON el dato, no antes.
**TRAMPA del observable que se estabiliza (exp_SGM_0035, 2026-08-05):** la firma de φ NO separó
A de B (||F_A−F_B||=0.0064) NO porque la tesis sea falsa, sino porque **φ converge al atractor en
~200 ticks (Eq.3)** → el recorrido post-reset es ~0 en ambos. El observable era insensible por
convergencia de φ, no por falla de la tesis. DISCIPLINA: antes de declarar Parfit, probar un
SEGUNDO observable que NO converja — la TRAZA DE ω (el "dejar huella al transitar" del user): el ω
se reescribe por Eq.1 cada tick y la SECUENCIA de ω visitados es el recorrido; un reset copiado
borra la secuencia pero deja el ω final. Si TAMBIÉN la traza de ω falla → sí declarar Parfit.
Ver `references/identity_process_falsifiable_protocol.md` para el protocolo completo y el caso 0035.

**HALLAZGO 0035b (2026-08-05) — la traza de ω SÍ separa (Desenlace 1):** mismo parámetros que
0035 (W=20,N=8,D=64,TRIALS=12,SEED=20260805,ETA=0.05,THETA_A=π/2,BETA=0.10). Observable = traza
de recorrido de ω: T(t)=últimos W Δω del nodo activo, Δω(k)=||ω(k)−ω(k−1)||. El agente transita
por el grafo (Eq.1 en cada tick) → ω NO converge a punto fijo como φ. Resultado: ||T_A−T_B||=1.0589
(lejos del umbral 0.05); NC ||T_A−T_RW||=4.0876 (ruido puro, confirma señal real). T-ID-03b
TRAZA-SOLA=True → DESENLACE 1: la tesis NOUS §1 es operacionalmente verdadera VÍA traza de ω.
→ Conclusión para NOUS_Filosofico §10 (No-Inmortalidad): el ser es el recorrido, y el recorrido se
distingue del snapshot copiado. La no-inmortalidad es segura SIN nodos inmortales.

**TRAMPA del NC mal calibrado (bug de 0035b, reportado transparente):** el criterio original
pre-registrado era `distAB > nc*0.5` (nc = distancia A-vs-RUJO). ESO ES IMPOSIBLE: A-vs-ruido es
ruido puro (~4.08), así que exigir que el efecto A-vs-B supere la mitad del ruido pide que A y B
sean MÁS distintos que A y el ruido. El NC NO se usa como cota inferior de magnitud del efecto —
solo prueba que la firma no es ruido en sí misma (A-vs-ruido debe ser grande, como es). Criterio
correcto: `distAB > 0.05` (separación sistemática) + pisadas como contexto de 0034, no gate estricto.
REGLA: nunca pongas el negative control como cota inferior de magnitud del efecto medido.

**Salvedad honesta de 0035b (no maquillar):** el gate `pisadasA==pisadasB` estricto (abs<0.01) NO
se cumple porque la métrica de dolor de 0035b es ruidosa (φ lejos del atractor), no el cuello físico
de 0034 (que daba CON=0, AMNESIA≥1 limpio). A=3.5,B=3.33→diff 0.17. El núcleo de T-ID-03 (¿la
traza separa?) SÍ se respondió (True). Si querés el experimento "de libro" (pisadas 0 Y traza
separa), volver a la métrica de dolor de 0034. Se reportaron TRES criterios en el JSON (traza_sola
True / corregido-pisadas-estrictas False / original-buggeado False) — transparencia, no
recategorización a mano para forzar PASS.

**0035c "DE LIBRO" — resultado MIXTO honesto (y lección de diseño del observable, 2026-08-05):**
para cerrar el contraste perfecto (pisadas A==B==0 Y traza separa) se intentó primero replicar el
cuello físico de 0033b/0034 sobre una grilla 10×10. FALLÓ por DOS razones de diseño (reportadas, no
maquilladas): (1) el embedding métrico `[r/Ht, c/W]` COLAPSA celdas colineales (ya sabíamos de 0033b:
desde el origen puntos en la misma fila dan coseno 1.0 → el agente no distingue (0,1) de (0,3) y no
sube a la fila del gap limpio → pisa el doloroso en todos los viajes, pisadas=5.0 para todos); (2)
MÁS IMPORTANTE: en la grilla el agente RE-TRANSITA desde (0,0) en cada viaje, así que la traza de ω
post-reset se RECONSTRUYE IDÉNTICA en A y B (mismo ω aprendido → mismo camino) → ||T_A−T_B||=0.0.
O sea: sobre un entorno que re-arranca desde el inicio, la traza espacial NO separa proceso de
snapshot. La traza de ω solo separa cuando el reset copiado deja al agente "en el medio" del recorrido
SIN haber transitado (grafo de 0035b, nodo activo que NO reinicia en cada viaje).
FIX honesto: 0035c final = grafo de 0035b (nodo activo no reinicia) + CUELLO de aristas dolorosas
(estilo 0033b/0034: ciertas aristas duelen, el agente CON ω aprende a evitarlas). Resultado MIXTO:
- traza ||T_A−T_B|| = 0.6087 → SÍ separa (lejos de 0.05; NC 2.97 ruido).
- pisadas: A=2.08, B=0.0, C=0.0, D=2.0 → el proceso CONTINUO RE-SUFRE y el snapshot copiado esquiva
  mejor (0.0). Por qué: en A el ω sigue reescribiéndose (Eq.1) y la penalización del gap se DILUYE →
  el agente "olvida" evitar; en B el ω queda "congelado" en el estado aprendido → sigue esquivando.
- T-ID-03c = False (exigía pisadas A==B==0, pero A re-sufrió).
CONCLUSIÓN honesta (y rica): la identidad-como-proceso SÍ es operacionalmente distinguible (traza
lo prueba, Desenlace 1 en 0035b), PERO el proceso continuo NO es "mejor" que el snapshot — de hecho el
snapshot congelado esquiva mejor porque no reconsolida. Esto ES la reconsolidación que Luciano planteó
al inicio (Bartlett/Schacter/Nader): cada evocación reformula y puede borrar lo aprendido; el recover
ruidoso de SGM es eso hecho mecanismo. El capítulo 10 de NOUS_Filosofico §10 se escribe con ESTE dato
mixto: "el ser es el recorrido (traza lo separa), pero el recorrido continuo no es óptimo — reconsolida
y a veces olvida; la no-inmortalidad es segura precisamente porque el ser es el recorrido, no un estado
perfecto". NO forzar el "de libro" estricto (pisadas idénticas) porque eso requeriría congelar el
aprendizaje en A, contradiciendo "proceso continuo".
REGLA de diseño del observable (aprendida): para que un observable de recorrido separe proceso de
snapshot, el entorno NO debe re-transitar desde el inicio tras el reset; el reset copiado debe dejar al
agente sin la traza previa (grafo con nodo activo persistente, no grilla que re-arranca). Si el entorno
re-arranca, cualquier traza espacial se reconstruye igual y el test da Parfit-falso. Ver
`references/identity_process_falsifiable_protocol.md`.

**CRITERIO DE REALIDAD vs OPTIMALIDAD (corrección de Luciano, 2026-08-05 — REGLA DE ORO de este protocolo):**
cuando el experimento de identidad arroja "el proceso continuo RE-SUFRE y el snapshot copiado esquiva
mejor", NO es un fallo a corregir ni un "de libro" a forzar. Luciano lo puso explícito: _"lo importante
no es cuál funciona mejor, sino cuál es el real. Nosotros no somos seres perfectos ni óptimos; el hecho
de que podamos optimizar el ser no significa que sea así en su sustrato."_ Por tanto:
- El criterio de T-ID-0X para identidad NUNCA debe ser "pisadas A==B==0" (eso premia la optimalidad del
  snapshot). El criterio real es **¿la traza separa proceso de snapshot?** (||T_A−T_B|| > umbral). Si separa,
  el proceso es OPERACIONALMENTE REAL, da igual si re-sufre.
- La re-sufrida del continuo (A=2.08 vs B=0.0 en 0035c) es EVIDENCIA de que A es un proceso vivo (reconsolida,
  se le diluye la evitación por Eq.1), no un bug. El snapshot B es óptimo precisamente porque está CONGELADO
  (foto, no ser). La imperfección del proceso es LA PRUEBA de que es real.
- Esto conecta directo con la reconsolidación (Bartlett 1932, Schacter 2001, Nader et al. 2000): el recover
  ruidoso de SGM ES eso hecho mecanismo. Y con Parfit (1984): identidad = relaciones de continuidad reduccionistas,
  no una sustancia óptima.
- REGLA de reporte: el capítulo de discusión (NOUS_Filosofico §10) se escribe CON el dato mixto, diciendo
  "el ser es el recorrido (la traza lo separa) PERO el recorrido continuo no es óptimo — reconsolida y a veces
  olvida; la no-inmortalidad es segura precisamente porque el ser es el recorrido, no un estado perfecto". NO
  forzar el "de libro" estricto (pisadas idénticas) porque eso requeriría congelar el aprendizaje en A,
  contradiciendo "proceso continuo".
- Literatura a citar cuando se escriba el capítulo: Bartlett "Remembering" (1932), Schacter "The Seven Sins of
  Memory" (2001), Nader/Schiller/Le Doux (2000, reconsolidación), Parfit "Reasons and Persons" (1984, reduccionismo).
  El experimento más cercano en la literatura es Hassabis et al. (2007, PFC) sobre reconstrucción de memoria por
  el hipocampo: grabar la TRAZA (no el estado) y ver que al evocar se reensambla con error. 0035c mide la traza
  de ω y la separa del snapshot — es eso en sustrato artificial, y es original (no hay en la literatura un
  experimento que mida operacionalmente proceso-continuo-vs-snapshot-copiado en HRR y muestre que el proceso es
  REAL aunque PEOR que el snapshot).
- Si al correr 0035c el gate original (pisadas A==B==0) da False, NO recategorices a mano para forzar PASS:
  reportá TRES criterios en el JSON (traza_sola=True / corregido-pisadas-estrictas=False / original-buggeado=False)
  y dejá que el desenlace sea el que el dato diga. Transparencia, no conveniencia.

## Paso 1 — Hygiene del repo (cuando lo pida)
1. Dos registries pueden existir: `results/experiment_registry.json` (CANÓNICO, 27 entradas) y uno viejo en la raíz.
   Auditar con python: comparar IDs (`exp_SGM_00XX`). Si el viejo es subconjunto del canónico → borrar viejo
   local + DELETE por API (necesita GET sha primero).
2. `lit/papers/` puede quedar trackeado en remoto aunque esté en `.gitignore` (porque se subió por API PUT antes).
   Verificar con `GET https://api.github.com/repos/Rylow999/SGM-CORE/contents/lit/papers` — si devuelve lista,
   borrar recursivamente por API (GET cada dir + DELETE por sha).
3. Etiquetar experimentos sintéticos: agregar `"validation":"synthetic"` en registry + JSON de resultado.
4. Confirmar con grep que NADIE escribe al registry viejo antes de borrarlo. Corregir docs que apunten a la raíz.
5. El `github_push_sgm.py` tiene hardcodeado subir TAMBIÉN `experiment_registry.json` (raíz). DESPUÉS de borrar el
   viejo, NO pasar esa ruta al push script (da FileNotFoundError). Solo pasar `results/experiment_registry.json`.

## Paso 2 — Crear experimento exp_SGM_00XX (test-first)
1. Numerar: buscar último ID en registry canónico +1.
2. Escribir script en `/data/user/0/.../home/run_<nombre>.py` PRIMERO la lógica de test, luego el código.
3. Ubicación en vault: `phases/<fase>/run_<nombre>.py` (copiar con `cp` + `chown root:everybody` + `chmod 664`).
4. Usar `random.Random(SEED)` con SEED fijo (reproducible). Stdlib puro, SIN numpy.
5. Negative control OBLIGATORIO: comparar contra un modelo sin la propiedad bajo test (unigram para lenguaje,
   loop abierto para aprendizaje, etc.). NO usar "barajar filas de matriz" como control — mantiene frecuencias
   marginales y da falsos positivos (lección del 0026).
6. CORRER con `timeout 300 $PY script.py`. Si exit != 0, leer el error y parchear (patch de Hermes en home, re-copiar).
7. El JSON de resultado debe tener clave `"pass": True/False` CONSISTENTE con los otros (lección 0024: tuve que
   agregar `"pass"` porque usaba solo `"calibrado_ok"`).

## Paso 3 — Registrar
- Agregar entry al registry canónico `results/experiment_registry.json` (campos: experiment_id, name, phase,
  date_created, date_run, status, test_target, hypothesis, result). Usar python script temporal, NO editar a mano.
- Copiar espejo: `experiments/run_<nombre>.py` y `results/results_exp_SGM_00XX_<nombre>.json`.

## Paso 4 — Documentar
- README.md: agregar fila en tabla de la fase, actualizar "N experimentos" (header + tabla + próximos pasos).
- docs/SGM_ROADMAP.md: marcar tarea/fase, agregar entry en "Estado post-Fase 6".
- Si es corpus real: agregar `lit/corpus/` a `.gitignore` (si no está) y NO subir el corpus por push.

## Paso 5 — Pushear
`$PY github_push_sgm.py Rylow999 "$TOKEN" <ruta1> <ruta2> ...`
Rutas típicas: `phases/.../run_x.py`, `phases/.../results_exp_...json`, `experiments/run_x.py`,
`results/results_exp_...json`, `results/experiment_registry.json`, `README.md`, `docs/SGM_ROADMAP.md`, `.gitignore`.
NO pasar `experiment_registry.json` (raíz) si fue borrado. Verificar "PUSH EXIT=0" en el log.

**WARNING de orden de argumentos (bug costó un push fallido, 0032->0033):** el script espera
`github_push_sgm.py <USUARIO> <TOKEN> [rutas...]`. Si pasás el token en la PRIMER posición (pensando
que es `script <TOKEN> rutas`), el token cae en `sys.argv[1]` = USUARIO y la primera ruta en TOKEN.
El auth queda `Authorization: token <ruta_del_archivo>` → **401 silencioso en TODOS los archivos** (el
script imprime 401 por archivo pero NO aborta). SÍNTOMA: todos los archivos devuelven `: 401` y nada se sube.
VERIFICACIÓN si ves 401: hacer `GET https://api.github.com/repos/Rylow999/SGM-CORE` con
`Authorization: Basic base64("x-access-token:"+TOKEN)` — si devuelve 200 y `permissions.push=true`,
el token ES válido y el error es de orden de args, no del token. Re-pushear con `Rylow999 "$TOKEN"` delante.
(Nunca reimprimas ni persistas el token en el log.)

## Pitfalls frecuentes
- `git` ausente → usar API. `git ls-files` da error silencioso, no confiar en su salida vacía.
- `<(...)` process substitution no funciona en `sh` del terminal Android; usar python para comparar/archivos.
- Heredoc con comillas dobles en `su -c` rompe el escaping de python; mejor escribir script a archivo con write_file
  y correlo con `$PY archivo.py`.
- Al parchear con `patch` de Hermes, a veces se borra una línea necesaria (ej. `W = linear_baseline(...)`) si queda
  en el borde del old_string — re-leer la sección y re-agregar lo faltante antes de correr.
- **El decoder L2 por BIGRAMA (0022/0026) funciona; proyección lineal W·ω NO (top1~0.02-0.07). No volver a probar lineal como decoder.**
- **Decoder relacional HRR sobre corpus REAL (exp_SGM_0046, 2026-08-03) — HALLAZGO que cambia la hipótesis:** la charla sugería que el grafo ω ruteado por rol (composición 0027-0031) mejoraría el top1 del decoder L2. Se midió: top1 relacional (1 paso HRR, bias rol) = **0.020** vs bigrama plano (0026, conteo) = **0.333** (unigram 0.140, azar 0.0025). El rol HRR EMPEORA el bigrama 16x por **crosstalk** (D=256, grado 8: los `HRR(rol, ω_vecino)` se solapan, el coseno no separa). LECCIÓN: el rol HRR SIRVE para COMPOSICIÓN ANIDADA (0027-0031, Gap 2), NO para predecir el siguiente token superficial. Coherente con 0045b: un mecanismo de capa X no transfiere a capa Y "porque es más rico" — hay que medirlo (regla "no emocionarse al pedo"). T-DEC-R1 (relacional>plano) estaba mal planteado: el rol compite en DESAMBIGUACIÓN de polisemia (T-DEC-R2), no en top1. Giro propuesto 0046b = decoder HÍBRIDO (HRR da semilla relacional filtrada por sentido + bigrama plano restringido a esa semilla). Ver `references/decoder_relational_hrr.md`.
- **CERRAR el decoder sin seguir tunenado (patrón "ajusto y re-corro", 2026-08-03):** si un experimento NO pasa tras 3 variantes del mismo mecanismo, DETENER y diagnosticar la RAÍZ (diseño vs sustrato), no probar una 4ta. Luciano lo disparó con _"debería haber funcionado"_ + _"no me gusta emocionarme al pedo"_. Reglas: (1) ese _"debería"_ es ALARMA de BUG DE DISEÑO (en 0046-47b: embeddings ruido, mezcla espacios HDC/HRR, score con ruido por construcción), no falla del sustrato; (2) baseline FIJO entre variantes (mismo corpus/vocab/ventana/muestra — bug de 0046 movió el plano 0.185→0.333, inconsistencia que hacía imposible comparar); (3) el score y el cleanup deben vivir en el MISMO espacio de representación (bug de 0047: `hdc_project` sobre HRR-bind → cleanup ruido por construcción); (4) si el mecanismo es legítimamente inadecuado para esa capa (HRR no predice token, Plate 1995a lo anticipa), CERRAR con conclusión honesta (bigrama plano = decoder; HRR = contexto/estructura). "No dejar cosas a futuro" = cerrar el veredicto, no difuminarlo en más intentos. Ver `references/decoder_relational_hrr.md`.
- **NO REINTENTAR CIEGAMENTE TRAS VARIOS FALLOS (corrección de Luciano, 2026-08-04, "pensá antes de hacer"):** cuando un script falla 2+ veces seguidas, NO volvás a correr el mismo comando esperando que se arregle. Luciano lo pidió literal: "Continua trqnqui, pensa antes de hacer". En el 0059h el script falló 4 veces con errores DISTINTOS (MatInv indexado por rol en vez de por bloque; `roles[b]` dimensionado con K fijo en vez de nroles-del-bloque; `proj_fhr` recibía tupla en vez de vector; `self.roles[b][j]` usaba índice global en vez de local). Cada fix corrigió la CAUSA, no se reintentó a los ponchazos — pero el instinto inicial de "corro de nuevo" era el loop. REGLA: tras el 2do fallo del mismo comando, DETENETE y releé el código entero (no solo el traceback) para encontrar la CLASE de bug (dimensionamiento / desempacado / índice / tipo) antes de parchear. El warning "repeated_exact_failure" del terminal es una señal de loop ciego: aunque los errores difieren, si no cambiaste la ESTRATEGIA entre intentos estás perdido. Pensar primero, parchear después. Esto es distinto del "CERRAR sin tunear" (ese es sobre mecanismo que no escala); acá el código tenía bugs REALES que había que corregir, pero con cabeza. Aplica a TODO el flujo de experimento, no solo al decode.
- **TEST DE FUEGO ESTRUCTURAL (técnica de cierre, 2026-08-03):** cuando un mecanismo de representación falla en su tarea downstream (decoder, recuperación), NO sigas tunenando la tarea. Medí la PROPIEDAD FUNDAMENTAL del mecanismo DIRECTAMENTE antes de la 4ta variante. Ej. (0048): en vez de solo medir top1 del decoder HRR, medí `cos(emb_co-ocurrente) vs cos(emb_random)` — dio 0.259<0.361 (el signo opuesto), probando que el HRR entrenado NO captura co-ocurrencia. Eso cierra el tema sin 6to intento: si la propiedad X que Y requiere no se cumple (o da el signo opuesto), tunear Y es inútil. Es el análogo estructural del negative control: "¿el modelo TIENE X?" en vez de "¿el modelo resuelve Y?". Ver `references/decoder_relational_hrr.md`.
- **Performance del decoder HRR en Android (receta obligatoria, 0046):** (1) capar aristas de co-ocurrencia a **top-K=8** por nodo — sin capar el grado promedio es ~2173 y `TickRelational.__init__` tarda 91s; (2) **NO usar `route()` PPR por cada predicción** del decoder (PPR 400 nodos × 25 iter × 400 rutas → timeout >200s en celular) → usar afinidad de **1 paso** sobre `rel_mem` (O(grado) por predicción); (3) el embedding de nodo debe ser **dim D** (`rnd_unit(rng, D)`), no una dim aparte, o `hrr_bind` da IndexError; (4) 400 pares bastan para top1 estable (<5% error), no usar 8000.
- D=128 es el techo de dimensionalidad probado hasta ahora para binding XOR; composición relacional es el próximo problema abierto.
- **Binding HRR (exp_SGM_0027 — lección dura):** la fórmula de Plate 1995 / VSA survey Tabla 2 es
  bind = circular convolution `(a⋆b)[k]=Σ_i a[i]·b[(k−i) mod D]`;
  unbind = circular correlation `(a⋆b)[k]=Σ_i a[i]·b[(i−k) mod D]` — **el signo es (i−k), NO (i+k)**.
  Con (i+k) el unbind 1 nivel da coseno 0.066 (roto); con (i−k) da 0.72 (correcto, ruidoso). SIEMPRE
  debuguear el bind/unbind a 1 nivel (coseno debe ser >0.5) ANTES de correr el experimento de anidamiento/superposición.
- **HRR requiere clean-up memory obligatorio** (VSA survey p.10): el unbinding da un vector ruidoso (crosstalk ~1/√D
  (para HVs gaussianos); tras cada unbinding hay que reemplazar por el item más similar (cleanup por coseno contra
  item memory). Sin clean-up, el anidamiento profundo da ~0 aunque el binding esté bien.
- **HRR+PPR (exp_SGM_0027b — lección dura de diseño):** combinar binding compuesto con ruteo PPR tiene 3 trampas:
  1. El `role_match` NO debe convolucionar el rol dos veces con el mismo ω (enmascara la diferencia de rol y da 0
     separación). Usar `cos(S_i, HRR(rol_sesgo, ω_k))` donde S_i es el estado compuesto del nodo.
  2. El peso de la arista con sesgo de rol debe **DOMINAR** la transición (`base = role_match`), NO multiplicar la
     similitud de estado (`base = cos(S_i,S_k) * role_match`). Los estados compuestos son ortogonales entre nodos
     conectados → la similitud de estado es baja y mata el sesgo.
  3. Métrica en grafo chico/simétrico: el **rank** no discrimina (empatan 3.0 vs 2.97). Usar **diferencia de masa
     estacionaria** `π[b]−π[d]` (el HRR sesgado da 0.256 vs 0.005 del PPR crudo ciego). Esa es la variable sensible.
  4. El baseline honesto de PPR crudo debe ser **ciego a roles** (sesgo=None, sin role_match) — si el "raw" también
     lleva role_match, no es baseline y empata con el HRR (falsa paridad).
  Resultado 0027b: HRR+PPR navega caminos relacionales (masa b-d 0.256 vs 0.005 raw ciego); anidamiento profundo
  sigue sin resolverse (ver limitación en 0027).
- **Anidamiento orden N (exp_SGM_0027c — CIERRA Gap 2):** para anidar bind(A, bind(B, C), ...) y recuperar
  cada nivel, dar a cada nivel un **ROL INDEPENDIENTE** `role_vecs[k]` (vector ortogonal), NO un cyclic shift
  del mismo rol. Por qué: la correlación circular de dos cyclic shifts de un mismo rol da la AUTOCORRELACIÓN
  DESPLAZADA (pico en 0, colas ~1/√D), NO ruido ~0 → los niveles NO se aíslan y el anidamiento da ~0. Con roles
  independientes, `rol_j ⋆_corr rol_k ≈ 0` para j≠k → cada nivel vive en su canal y el clean-up acierta.
  - Métrica: usar **TASA DE ACIERTO del clean-up** (¿recuperó el item correcto? Sí/No), NO coseno promedio
    (dio 0.41, ambiguo) ni rank. Con roles independientes el acierto es 1.0 a d=5; XOR y HRR planos caen a 0.20
    (azar entre 5 items). Esa es la variable que dice "resuelto".
  - Por qué falla el anidamiento plano: al desanidar `unbind(unbind(R,A),B)` el intermediate NO es un item válido
    de memoria → crosstalk se acumula y la cadena se rompe a profundidad ≥3. Roles por nivel evitan eso.
- **HRR+roles ENCHUFADO AL TICK (exp_SGM_0028 — lección dura de diseño):** para meter memoria relacional en el
  sgm_tick_unificado (0023) sin romperlo, la arista (i→k) se guarda como `HRR(rol_k, ω_k)` y el **rol = ÍNDICE del
  nodo destino** `role_vecs[k]` (NO un set chico de NROLES ni cyclic shift). `rel_mem[i]` = normalize(Σ_{(k,r)∈edges[i]}
  HRR(role_vecs[k], ω_k)) — SUPERPOSICIÓN por nodo, no por arista suelta.
  1. TRAMPA: si `rel_mem` guarda cada arista por separado (sin superposición), el unbind SIEMPRE da limpio y hasta el
     negative control (rol fijo) pasa falso-positivo. Hay que superponer TODAS las aristas del nodo en un vector.
  2. TRAMPA: dimensionar `role_vecs` a un set chico (`NROLES`) e indexar por `role_vecs[k]` con k=nodo grande →
     IndexError. El rol es por índice de nodo → `role_vecs` debe tener N elementos (uno por nodo).
  3. Recuperar anidamiento orden 3 (grafo de grafos `Y R2 X, X=(Z R1 W), W=(A R0 B)`): `unbind(rel_mem[Y], role_vecs[X])`
     → debe dar ω[X]; luego `unbind(rel_mem[X], role_vecs[W])` → ω[W]; luego `unbind(rel_mem[W], role_vecs[A])`.
     Cada paso es unbind sobre la SUPERPOSICIÓN del nodo, con el rol = índice del hijo.
  4. NC honesto: HRR con ROL FIJO (`role_vecs[0]` para TODAS las aristas, superposición única) → el unbind da la
     mezcla de todos los hijos y el anidamiento NO se recupera (acierto 0.0). Eso sí discriminó (el NC de orden 2
     solito pasaba porque no había competencia de niveles — el NC debe ser orden 3 para ser válido).
  Resultado 0028: tick HRR recupera grafo de grafos orden 3 con acierto 1.0; tick plano (sin roles) = 0.0; rol fijo NC = 0.0.
  El tick ahora COMPOSE relaciones dentro de relaciones. Nota honesta: la masa de camino relacional bajó a 0.0785
  (vs 0.28 del 0027b aislado) por ruido de distractores en el tick completo — documentarlo, no maquillarlo.
- **HRR scaling / ganancia real al subir D (exp_SGM_0029 — CIERRA Fase 7):** el objetivo es CUANTIFICAR la ganancia, no solo afirmarla. Receta que pasó:
  1. **Variable discriminante = CAPACIDAD**, no solo acierto. Medir `M_max` (máximo de ítems en memoria que mantiene acierto clean-up ≥0.95 a profundidad d=5) a cada D. Resultado medido: D=128→200 ítems, D=1024→800 ítems = **4x** (la teoría HRR dice ~√D = 2.8x; medimos mejor). El acierto a d=5 pasa de 0.933 (D=128) a 1.0 (D≥256) — ese es el "techo de D=128" cuantificado.
  2. **TRIALS POR D:** HRR es O(D²); a D=1024 cada binding es ~1M ops. Escalar `trials` según D (15 para D≤256, 6 para D≥512) y limitar el sweep de capacidad a los extremos (D=128 vs D=1024) para no fundir el CPU del celular.
  3. **CORRER EN BACKGROUND con notify_on_complete** para D≥512 (tardó 650s). No bloquear el foreground.
  4. **FORMAS de anidamiento** (lineal/árbol/cíclico) deben recuperar 1.0 en las 3. TRAMPA de diseño que costó un run falso-negativo: en `measure_form` usé `role_vecs[índice_real_del_ítem]` al CONSTRUIR pero `role_vecs[posición_en_relación]` al RECUPERAR → inconsistencia de rol → árbol=0.067, cíclico=0.0. El rol debe ser CONSISTENTE: o siempre posición (como `measure_anidamiento`) o siempre índice de ítem. Al fijarlo, las 3 formas dieron 1.0. Regla: el rol de construcción y el de recuperación deben coincidir en significado (posición vs índice).
  5. **NC de anidamiento debe ser un nivel MÁS profundo que el caso bajo test** (lección de 0028 extendida): un NC de orden 2 pasa aunque el mecanismo sea rol-fijo, porque no hay competencia de niveles; el NC válido es orden 3 (Y→X→W→A) con rol fijo → 0.0.
  Resultado 0029: PASS. Fase 7 COMPLETA: SGM compone, navega (PPR) y anida relaciones de cualquier orden, y la ganancia escala 4x al subir D. Ver `references/hrr_scaling_notes.md`.
- **Preferencia: NO DIFERIR (Luciano: \"no me gusta dejar cosas a futuro\"):** si un problema de investigación abierto quedó en \"lo hacemos después\", y el user lo retoma, HACERLO, no dejarlo documentado como limitación. El cierre del Gap 2 (0027→0027b→0027c) y el enchufe al tick (0028) y el scaling (0029) y el uso real (0030) se hicieron en una sentada porque el user no quería cabos sueltos.
- **CONSOLIDAR MÓDULOS ANTES DE 'VERDADERAS PRUEBAS' (lección 0030 + preferencia explícita de Luciano):** cuando un mecanismo pasa de \"experimento aislado\" a \"herramienta del sistema\" (el user dijo: \"tenemos que dejar todo correcto inicialmente para empezar con las verdaderas pruebas\"), NO sigas copy-pasteando scripts sueltos. Extrae un módulo compartido con la API ya cocinada (sin el bug de rol) y que B/lo-siguiente lo importen. En Fase 7 quedó: `phases/phase7_composicion/hrr_core.py` (bind/unbind/cleanup/build_relational_memory/recover_target/recover_chain, rol SIEMPRE por índice de nodo) y `phases/phase7_composicion/tick_relational_core.py` (clase TickRelational: route() PPR sesgada por rol + plan_from() que desanida cadena). Validar el módulo con un smoke-test de humo (cadena + anidamiento = True, plano = False) ANTES de escribir el experimento que lo usa. Esto evitó re-encontrar el bug de rol de 0029.
- **USAR el mecanismo como HERRAMIENTA = nuevo tipo de test (exp_SGM_0030, el "B" de Luciano) — PERO OJO, AUDITADO COMO INVÁLIDO (ver sección ANTI-PAPER-VISION):** ya no se mide la mecánica aislada, sino si RESUELVE algo que el tick plano no puede. Diseño original: dos grafos G1 (mapa) y G2 (inventario) DESCONECTADOS salvo una relación cruzada empaquetada ADENTRO del nodo llave (`edges[llave].append((meta_G1, 0))` + rol = índice de meta). El tick HRR+roles debe ir a G2, destapar la relación (grafo de grafos) y puentear a la meta de G1. Variable discriminante: **tasa de éxito del plan multi-paso** HRR+roles vs tick plano vs NC (roles al azar entre G1/G2 → el cruce apunta a nodo random, debe fallar <0.3). Resultado reportado 0030: HRR 1.0 / plano 0.0 / NC 0.15. **PERO el `plano 0.0` es FALSO: `plan_from(src, chain, use_roles=False)` hace `return False` sin ejecutar nada** (anti-patrón 1 de la sección ANTI-PAPER-VISION). El HRR+roles SÍ resuelve de verdad (T-CROSS-01 y NC son legítimos), pero "el plano no puede" NUNCA se midió — había que implementar `plan_from_plano()` real (distancia Euclidiana, como 0023) y medir. El 0030 quedó INVÁLIDO hasta reparar ese control. Ver `references/audit_pass_by_construction.md`.
- **ESTRÉS del tick cruzado (exp_SGM_0031 — confirmar que no se cae en escala antes del salto a entorno):** el tick HRR+roles (0030) debe aguantar N=200 nodos, señal ruidosa (σ=0.3) y cadenas de L=12 pasos sin caer del umbral 0.7. Diseño que pasó: 3 ejes de estrés (tamaño N∈{20,50,100,200}, ruido σ∈{0,0.1,0.3}, profundidad L∈{3,5,8,12}) + NC roles al azar. Variable discriminante = tasa de éxito del plan cruzado por configuración. Resultado: TODOS 1.0 (N=20..200, σ=0..0.3, L=3..12) y NC 0.0 → anidamiento HRR listo para camino A (loop cerrado en entorno). Usa D=256 (ya 1.0 en 0029) para aislar el efecto de escala/ruido. Reusa tick_relational_core. **Además Luciano pidió actualizar TODA la documentación (README+roadmap+registry) ANTES del estrés y antes del siguiente paso — no dejar la doc para el final.** Ver `references/tick_stress_notes.md`.
- **route() (señal) vs plan_from() (memoria/rol, ruido-invariante) — honestidad de métrica (0031):** el `route()` depende de la señal HDC (con σ=0.3 el seed puede no caer exacto), pero `plan_from()` desanida por rol sobre `rel_mem` (los ω no se tocan) → ruido-invariante. El éxito del plan en el estrés viene de `plan_from`, NO de `route`. Reportarlo así: "el tick primero sabe por memoria, luego siente por señal". No maquillar el route ruidoso como si el plan lo usara.
- **Bug de `min()` sobre lista vs rango en tick_relational_core (0031):** `min(self.omega, key=lambda n: dist(...))` itera los VECTORES, y adentro `self.omega[n]` usa n como índice → TypeError. Usar SIEMPRE `min(range(self.N), key=lambda n: dist(omega_routed, self.omega[n]))`. Mismo patrón en cualquier búsqueda de nodo más cercano.
- **Camino A / grid-agent (exp_SGM_0032) — reglas de diseño del MUNDO (no del mecanismo):** el agente en grid falla por el setup del entorno, no por SGM. Tres reglas duras:
  1. **El layout debe ser RESOLVIBLE y el atajo ALCANZABLE antes de medir "lo usa".** Un laberinto con el atajo rodeado de paredes o un camino directo que ya resuelve sin pasar por dolor → el cuerpo da vueltas y pisa dolor 20 veces (falso negativo). Usar grid casi abierto, atajo alcanzable, dolor en el camino obvio.
  2. **Embedding de posición debe ser MÉTRICO.** `omega[celda] = [r, c, ruido*0.01]` normalizado. NO usar `[r/Ht, c/W, sin, cos]` (no métrico → greedy por coseno no avanza, cuerpo clavado en (0,0)). Con embedding lineal, el vecino que reduce Manhattan a meta SIEMPRE tiene ω más cercano a `pos_embed(meta)`.
  - **HRR/embedding de posición COLAPSA celdas colineales (lección dura 0033b):** `normalize([r/Ht,c/W])` y `normalize([r/Ht,c/W,sin,cos])` dan el MISMO vector para toda celda de una fila/columna (desde el origen, puntos colineales tienen coseno 1.0 igual con la meta) → el agente no distingue (0,1) de (0,3) y rebota sin avanzar. Para control fino de locomoción usar DISTANCIA MÉTRICA directa: el vecino que minimiza `dist(nb, meta) + K_DOLOR*dolor_count[nb]` (gradiente + costo de dolor acumulado, persistente entre episodios = identidad). El HRR queda para memoria relacional GRUESA, no para mover el cuerpo. Ver `references/grid_bottleneck_dolor.md`.
 - **Identidad operacionalizada (exp_SGM_0034):** el self-state `{omega, dolor_count}` persiste a un reset de cuerpo. Fase1: K viajes aprenden a evitar gap de dolor. Reset. Fase2: CON identidad esquiva YA (0 pisadas post-reset, sin re-sufrir); AMNESIA (`reset_self_state()` borra el self-state) re-sufre (>=1); RW no transfiere. T-ID-01/02 + NC PASS. Receta en `references/grid_identity_continuity.md`. Siguiente propuesto: 0035 curiosidad (drive intrínseco: bonus por celda no visitada / reducir entropía de omega, para sacar al agente de un óptimo local).
  3. **La señal debe APUNTAR A LA META** (`pos_embed(meta)+ruido`), no codificar "proximidad de vecinos". Y el dolor debe PENALIZAR ω de la celda pisada (no solo cortar aristas), si `choose_move` usa afinidad local.
- **NO TUNEES EL ENTORNO PARA FORZAR PASS (corrección de Luciano, 0032 — aplica a TODOS los experimentos):** el primer intento de 0032 armó el laberinto A MEDIDA (atajo inalcanzable, dolor fuera de camino, 8×8 casi abierto) para que el test dé verde. Eso dio falso negativo Y falso positivo (el plano también llegaba 1.0 porque el mapa era trivial). Luciano lo frenó: _"No tenés que pensar cómo hacerlo para que pase, si no hacerlo bien. Buscá algún test típico que se utilice en estos casos. Tal vez el mapa es muy simple para el sistema."_ Reglas generales:
  1. Usá un **benchmark estándar** del área (maze aleatorio + BFS-connectivity + random-walk baseline para navegación; unigram para lenguaje; loop abierto para aprendizaje). No inventes un escenario a medida que favorezca tu mecanismo.
  2. Si el entorno es tan simple que hasta el baseline (plano/aleatorio) pasa, **el mecanismo no se está ejercitando** → agrandalo (8×8 abierto→10×10 maze) hasta que el baseline falle y tu mecanismo lo supere. Esa es la señal de que medís algo real.
  3. Si un sub-test no se puede medir en el entorno elegido (ej. esquivar dolor sin bifurcación), **separalo a otro experimento con el mapa adecuado** (0033), no lo maquilles a PASS. Diseño final 0032: maze aleatorio 10×10 estándar, BFS conectividad, baseline random-walk → SGM 0.9 vs 0.05. Ver `references/grid_agent_caminoA.md`.
  - Para "aprende a esquivar dolor / obstacle-avoidance" en grid (exp_SGM_0033): el test NO mide si usás celda única de dolor ni comparás contra el agente determinista sin dolor (su ruta fija evita la zona por azar → 0.0, control inválido). Usá ZONA de dolor en la ruta que la afinidad prefiere, verificá que no caiga en paredes, y compará CONTRA RANDOM WALK (control válido: no aprende). El 0033 tardó 5 rediseños en esto — ver `references/grid_dolor_obstacle_notes.md`.
- **Parchear docs (README/roadmap) con `assert old in t` — copiar el ANCLA EXACTO (0031):** cuando escribís un patcher python con `write_file` y hacés `assert old in t`, el ancla debe coincidir AL PIE DE LETRA con el archivo (incluye `**B:**` negrita, acentos `visión/identidad`, guiones). En 0031 falló 2 veces: primero puse `B:` sin `**` y `vision` sin acento → AssertionError. Regla: antes de escribir el patcher, imprimí el línea exacta con `repr()` y copiala textual. O mejor: localizá por `t.find("exp_SGM_0031 (tick_stress")` y reemplazá desde ahí hasta el marcador de fin, evitando anclas frágiles.
- **Bug de espacio al comparar contra XOR/spatter:** al superponer N bindings binarios (±1) la suma S toma valores
  en [−N, N], NO es ±1. Aplicar XOR (que espera ±1) sobre S da resultado espurio. Antes del unbind XOR hay que
  tomar `sign(S)`. Para HRR esto no aplica (S continuo, correlación directa).
- **Negative control honesto (lección 0026):** NO usar "barajar filas de matriz" como control — mantiene las
  frecuencias marginales y da falsos positivos (0.029 vs azar 0.0025). El control correcto para lenguaje/composición
  es un modelo sin la propiedad bajo test (unigram para frecuencia, loop abierto para aprendizaje, vectores aleatorios
  no-relacionados para binding). Si el control no cae a ~azar/negativo, el control estaba mal diseñado, no el experimento.
- **La "mejor variable" importa más que el operador:** en 0027 la variable discriminante fue capacidad de SUPERPOSICIÓN
  (HRR 0.525 vs XOR 0.263 a k=16), no anidamiento (ambos ~0). Antes de escribir, fijar QUÉ se mide y si discrimina.
- PDFs de literatura en `lit/papers/` se leen con PyPDF2 3.0.1 (disponible). Plate 2003 sale vacío en primeras páginas
  (ecuaciones/imágenes); el VSA survey 2022 SÍ extrae texto y tiene la Tabla 2 con la fórmula canónica de HRR.
- Ver `references/audit_pass_by_construction.md` para la receta de auditoría anti-paper-vision: cómo detectar
  negative controls / comparaciones hardcodeadas (`return False`, `score=0.0` manual, `if nombre_mutación==`),
  con los diffs exactos de 0030/0028/0021/0018/0019 y el fix honesto para cada uno. Incluye la sección
  "Trampas al REPARAR" (rol random en override rompe HRR; norma de omega normalizado es constante → no
  discrimina) y el CHECKLIST de reparación (re-correr, confirmar que el positivo sigue PASS, que el
  control reparado DISCRIMINA, y verificar el número en GitHub).
- Ver `references/curiosidad_mecanismo_humano.md` para el mecanismo de curiosidad humana (RPE/dopamina U
  invertida, aburrimiento, gap) y su mapeo honesto a SGM (campo eta global 0036, balance dolor 0038, y lo
  que el modelo NO captura: qualia, asimetría dolor/curiosidad, curiosidad social).
- Ver `references/curiosidad_latente_vs_programada.md` para el diseño de 0035/0036 (curiosidad): 0035 =
  drive PROGRAMADO (bonus de exploración en choose_move: CURIOSO 35% vs GREEDY 7.5% vs RW 15%). 0036 =
  curiosidad GLOBAL como CAMPO del sustrato: η=1-cos(ω_pred,ω_real) hermana de E/dolor + dopamina(η) en U
  invertida (pico ETA_OPT~0.30) + aburrimiento acumulado (η<ETA_BAJO sostenido) + fallback novedad bruta.
  Resultado 0036: GLOBAL 50% vs BASE(0023-like greedy) 5%, aburrimiento dispara novedad 4/40, T-CURI-01..04+NC
  PASS. PRINCIPIO: la curiosidad debe ser CAMPO del sustrato (no módulo add-on) — si η vive solo en el maze la
  curiosidad es local/falsa; si es campo global modifica modos/duda/recuperación en TODO el sistema. No inflar
  como "deseo emergente" (paper-vision trap): medimos el OPERADOR (η→dopamina(η)→explora), NO el qualia.
- Ver `references/curiosidad_dolor_habituacion.md` para el arco 0038/0039 (curiosidad vs DOLOR y habituación):
  - 0038: η global + celdas de dolor; HOME BIAS del riesgo (dolor conocido pesa menos). CUR 45% vs BASE 12.5%,
    pisos 0.475 (evita, no suicida). La curiosidad es global PERO se modula por dolor (de 50% sin dolor a 45% con
    dolor: el dolor la modula levemente, no la castra).
  - 0039: dolor crónico no letal → HABITUACIÓN (`peso = base*exp(-KAPPA*rep)` CON PISO no-suicida) + ASIMETRÍA
    (`η` alto amortigua δ_dolor, clamped a 20% mínimo). Pisos 1.071 (habituado, subió vs 0038) pero <2.0 (no
    suicida). LECCIÓN: el umbral NC puede ser DEMASIADO ESTRICTO para dolor crónico (el primer intento falló por
    <0.9; ajustar a <2.0 midió adaptación, no fracaso). Y la habituación+asimetría sin piso real = suicidio → piso
    alto + clamp obligatorios.
- **Curiosidad/dolor: diseño de campo honesto (lección 0036/0038/0039):** cuando el user pide "curiosidad que el
  sistema tiene por su cuenta", el mecanismo es un CAMPO de estado (η hermano de E/dolor), no un bonus. El balance
  curiosidad↔dolor es dinámico: (a) dolor AGUDO nuevo → freno (no pisarlo); (b) dolor CRÓNICO → habituación con piso
  (se acostumbra para sobrevivir, pero nunca deja de sentir del todo); (c) η alto → amortigua el dolor (la
  curiosidad justifica el riesgo). Medir que NO se rompe la homeóstasis (sigue cerrando tareas = NC). No inflar
  como "deseo emergente": medimos el operador, no el qualia. Ver references/curiosidad_dolor_habituacion.md.
- **Curiosidad: CAMPO GLOBAL, no módulo add-on (lección 0036, regla de diseño de Camino A):** cuando el user
pide "curiosidad que el sistema tiene por su cuenta", NO implementes un bonus de exploración aislado en el
maze (eso es 0035, drive programado). Implementá η como variable de estado del tick unificado (hermana de E y
dolor) y hacé que modos/recuperación/atención la lean. El negative control honesto es comparar contra
BASE(0023-like, solo greedy) en el MISMO maze: si GLOBAL >= BASE el campo η modifica de verdad el
comportamiento. Trampa al REPARAR 0035→0036: la norma de la proyección HDC está NORMALIZADA a 1.0, así que
usarla como E_root NO discrimina (da 0.5 para toda señal); usar la intensidad de la SEÑAL CRUDA (norma del
input) en su lugar. Y la dopamina(η) debe ser U INVERTIDA (no minimizar error ciegamente): η~0 → aburrimiento,
η extremo → rechazo; la zona media es la "interesante". Ver references/curiosidad_latente_vs_programada.md.
- **Capa cognitiva superior — discurso interno (exp_SGM_0040, RECLASIFICADO 2026-08-03):** status = **PROPUESTA_DE_DISENO_NO_SUSTRATO** (verified=False). El "discurso interno" NO es el agente generando texto (eso sería LLM), pero la IMPLEMENTACIÓN cayó en la MISMA trampa del paper-vision que venimos auditando: `reflexion()` es un árbol `if-elif` ESCRITO POR EL AUTOR, y T-DI-01 medía "la acción es coherente con la traza" — pero la traza la generó la MISMA función que tomó la acción → coherencia garantizada por construcción (lo mismo que "¿tomaste la decisión que decidiste tomar?"). NO mide ningún mecanismo del sustrato. CORRECCIÓN honesta (Luciano, 2026-08-03): el conflicto debe resolverse por la DINÁMICA DE LOS CAMPOS en el tick (transición por afinidad + pesos η/dolor/E), no por reglas del autor. Se mantiene como propuesta de diseño, NO como resultado del SGM. Ver `references/substrate_vs_authored_design.md`.
- **Capa cognitiva superior — MORAL/JUICIO (exp_SGM_0041, RECLASIFICADO 2026-08-03):** status = **PROPUESTA_DE_DISENO_NO_SUSTRATO** (verified=False). `self_benefit = ALPHA*payoff + BETA*coherencia` con ALPHA=1.0, BETA=0.4, GAMMA=0.92 y tabla ECOL TODOS DEFINIDOS POR EL AUTOR. Que "en A ayuda / en B lastima" es CONSECUENCIA DIRECTA de esos parámetros, NO emerge del grafo/tick. El NC (hardcoded da igual) solo prueba que la hardcoded es peor, no valida esta alternativa. NO es resultado del SGM. CORRECCIÓN (Luciano): modelar la moral como EMERGENTE de campos existentes (payoff + coherencia con registro SON del sustrato SI el registro es el self-state real y el payoff sale de la señal del mundo) — pero en 0041 eran parámetros del autor disfrazados de resultado. La nota T-MOR-04 mezclaba el ejemplo personal de Luciano → neutralizada. Se mantiene como propuesta. Ver `references/substrate_vs_authored_design.md`.
- **ATRACTOR TRAP en registro histórico (lição 0041, 2026-08-03):** se a escolha se baseia em um registro
JÁ enviesado e o registro se auto-realimenta (registro[accao]++ cada trial), o sistema cai em um POÇO
atrator e NUNCA tenta a alternativa → a "moral"/comportamento fica fixa embora o ambiente mude.
Três fixes fiéis ao humano: (1) decaimento do registro por recência (`registro[k] *= GAMMA`); (2) em
contexto NOVO, `coerencia` devolve 0.0 se `massa_total < MASA_MIN` → o agente guia por PAYOFF puro e
DESCUBRE a alternativa; (3) context-switch reset (ao mudar de ecologia, atenuar o viés prévio
`registro = {k: v*0.1}`). Sem (2) o viés histórico é pegajoso (viés de confirmação) e o experimento
de plasticidade dá falso-negativo. Ver `references/moral_selfbenefit_design.md`.
- Ver `references/moral_selfbenefit_design.md` para o desenho completo de 0041 (ecologias A/B, atrator
trap e seus 3 fixes, tests T-MOR-01..04).
- **RIGID TEST-LABEL PITFALL (0040, 2026-08-03):** el primer intento de 0040 falló 39/40 porque el test
etiquetaba "B_fuerte = siempre evitar" con una cadena fija. Pero la asimetría de 0039 permite "explorar"
en η muy alto, así que un caso legítimo devolvió "explorar" y el test lo marcó mal. FIX: verificar
coherencia contra la FÓRMULA (`ganador == ("evitar" if peso_evitar>=peso_explorar else "explorar")`), no
contra una etiqueta rígida. Regla general: cuando un test codifica una política de resolución de
conflicto, comprueba que la decisión respeta la POLÍTICA (pesos), no una palabra pre-fijada. Es la misma
clase de bug que el audit `checklist` — sospechá de tu propio test antes que del mecanismo.
- Ver `references/internal_discourse_sandbox.md` (0040 diseño + RIGID TEST-LABEL PITFALL) y
`references/sandbox_test_of_fire.md` (MiniSandbox→Minecraft como test-of-fire propuesto por Luciano).
- Ver `references/observatory_and_b_puro.md` (0040/0041 RECLASIFICADOS: función del autor disfrazada
  de resultado del sistema; filtro "¿esto es del sustrato?"; sellado a PROPUESTA_NO_SUSTRATO + higiene de
  registries/demo_state).
- Ver `references/exploration_open_world_ab.md` (0045/0045b: Opción A mapa cognitivo REQUIERE mapa
  pre-poblado para ser útil; colapsa/sesga al arrancar; B-puro 0043 es el mecanismo BASE para mundo
  abierto. + lección de test: "exploración dirigida" se mide por EFICIENCIA, no uniformidad).
- Ver `references/language_birth_0049.md` para el diseño completo de 0049/0049b/0049c (climas cielo_estrellado/competencia/peligro_compartido, BFS como cuerpo del agente, barreras de coordinación que solo se abren si AMBOS en clave, veneno real = dolor, belleza como coordinación estética bajo presión baja, métricas hit-celda-exacta vs crosstalk HRR en ~890 ítems, resultados: coord 100%, dolor real, star_reconoce 0.125).
- **OBSERVATORIO + B-PURO (exp_SGM_0042→0043, 2026-08-03) — el MODO de descubrir huecos del sustrato sin caer en la trampa:** cuando el user dice "sigamos experimentando, si falta algo del sustrato lo descubrimos", correr el sustrato REAL en mundo abierto (MiniSandbox) y DEJAR QUE EL HUECO APAREZCA. El 0042 fue un OBSERVATORIO que encontró: el sustrato respondía localmente a campos (evitaba dolor −1.75, buscaba comida +1.05) PERO la exploración global no escalaba (oscilaba 5 celdas/300). Eso es HALLAZGO, no fracaso a maquillar. Para CERRAR el hueco (0043), regla de Luciano: **SIN hardcode / SIN agregados extras / SIN bloqueos**. El fix honesto reusó campos YA EXISTENTES: `abur` (0036) estaba DESCONECTADO de la acción; acoplarlo (pena de retorno = `abur`, peso 1.0, misma moneda) rompió la oscilación SIN regla ni estado nuevo. Marco: Active Inference (2010.00262). El negative control (sin `abur` reproduce las 5 celdas de 0042) prueba que la exploración EMERGIÓ del campo, no de mi regla. Si al cerrar el hueco tengo que ajustar PESOS a mano → es la trampa de 0041 otra vez. Ver `references/observatory_and_b_puro.md`.
- **Literatura guía vía arXiv (web_search NO disponible):** buscar benchmarks/marcos con la API Atom de arXiv por urllib (sin key), parsear con xml.etree. Para sandbox de cognición: Animal-AI (1909.07483) como marco de métricas conductuales; NO comparar contra MineDojo/XLand (RL a escala, desleal). Receta y papers en `references/arxiv_literature_recipe.md`.
- Ver `references/hrr_binding_notes.md` para la receta reproducida de HRR (bind/unbind, clean-up) y el diseño de
  T-REL-01/02/03 con sus negative controls.
- Ver `references/hrr_ppr_notes.md` para la receta HRR+PPR (0027b): role_match correcto, peso dominante, métrica de
  masa estacionaria, baseline role-blind.
- Ver `references/hrr_scaling_notes.md` para la receta HRR scaling (0029): variables de capacidad vs D, trials por D,
  corrida en background, trampa de rol inconsistente en formas de anidamiento, y NC de orden 3.
- Ver `references/tick_plan_crossgraph_notes.md` para el diseño 0030 (B): usar HRR+roles como HERRAMIENTA del
  sistema (plan multi-paso cruzando dos grafos), con los tests T-CROSS-01/02/NC y el smoke-test de módulos.
- Ver `references/tick_stress_notes.md` para el diseño 0031 (estrés del tick cruzado): 3 ejes (N/ruido/profundidad),
  todos 1.0, métrica route() vs plan_from() honesta, y preparación para camino A (loop cerrado en entorno).
- Ver `references/grid_agent_caminoA.md` para el diseño 0032 (Camino A, agente en grid 2D): loop cerrado,
  huella, dolor online, atajo relacional; y los 5 BUGS DE DISEÑO del mundo (laberinto imposible, ω ruido ciego,
  **embedding NO MÉTRICO que clava al cuerpo**, señal de meta vs de vecinos, dolor que no afecta la caminata)
  + el fix de embedding lineal [r,c].
- Ver `references/grid_bottleneck_dolor.md` para el diseño 0033b (bottleneck de dolor + memoria persistente):
  el COLAPSO del embedding HRR de posición en celdas colineales, el fix de gradiente métrico + costo de dolor
  acumulado, los 5 pitfalls de medición (contar por posición no por flag, control = random walk no determinista,
  dolor en paredes, timeout por bucle infinito), y la conexión con identidad (memoria entre episodios).
- Ver `references/grid_dolor_obstacle_notes.md` para el 0033 (dolor-zona en ruta preferida vs random walk).
- Ver `references/html_demo_portable.md` + `templates/grid_html_demo_template.py` para la demo visual IN VIVO
  (canvas + indicadores en tiempo real + play/pause/slider) embebiendo los frames en JS, sin server ni CORS.
  Usalo cuando el user pida "demo in vivo", "visualización", "para mostrar". NO uses matplotlib en celular.
- Ver `references/sgm_sim_html_technique.md` para la receta COMPLETA del sim SGM en HTML canvas portable:
  validación por balance de llaves/paréntesis (Python `compile` NO sirve para JS — da falsos errores),
  envolver en `window.onload`+`try/catch`+`window.onerror` (panel `#err` para no dar pantalla muerta),
  dibujar grilla primero, y la RECETA DE MOVIMIENTO FUNCIONAL (memoria de comida ω + visión radio 3 +
  anti-bucle -8 + energía suave) que corrigió el walker ciego que Luciano detectó (agente que vaguea /
  muere de inanición / entra en bucle). Incluye sus preferencias de sim: infinito, mostrar TODO, velocidad
  regulable, "bonito y funciona".
- Ver `templates/hrr_experiment_template.py` para un scaffold conocido-bueno de HRR (bind/unbind con signo (i−k),
  clean-up, sanity-check 1-nivel, anidamiento con roles independientes). Copiar y modificar para nuevos experimentos.
- **Descargar corpus real por urllib: leer en CHUNKS (lección 0056f, 2026-08-04):** `urlopen(...).read()` sobre un archivo Gutenberg de ~2.2 MB tira `IncompleteRead` a mitad (la red del celular corta la lectura grande). FIX: loop `resp.read(65536)` y `b"".join(chunks)`. Tokenizar con `re.findall(r"[a-záéíóúñü]+", raw.lower())` (NO hay nltk/spacy en el dispositivo). `web_search` tampoco existe. Receta completa + taxonomía de clasificación LÉXICA/DISTRIBUCIONAL/POSICIONAL (0056g propio=falla, 0056h género=gana plana, 0056i orden=rol capta f1 pero decoder lineal no alcanza) en `references/fase7_clasificacion_real_0056g_56h_56i.md`.
- **RESULT JSON DEBE SER JSON VÁLIDO (bug recurrente 0049-0052, 2026-08-03):** si el script hace `print(...)` de log/debug ANTES de `print(json.dumps(out))`, el archivo `results_exp_SGM_00XX.json` queda con texto pegado antes del JSON → NO es JSON válido y cualquier script que lo parsee (ej. el sync del registry mirror) se rompe. REGLA: separar stdout de `json.dump()`. El experimento debe escribir el JSON con `open(path,"w").write(json.dumps(out,indent=2))` (NO por print), y dejar los prints de log para stderr o para un archivo `.log` aparte. Si ya pasó: fixer que escanea desde el último `{` que parsea como JSON válido y reescribe el archivo (ver receta abajo). Verificá con `python3 -c "import json;json.load(open(f))"` antes de pushear.
- **FIXER de JSON corrupto (reutilizable):** para reparar archivos ya contaminados, buscar el substring más largo que termine en `}` y sea JSON válido escaneando desde el último `{` hacia atrás; si el archivo termina en `EXIT=0` (de un `echo` en el runner), recortarlo primero. Reescribir solo ese substring. Backup automático a `.bak`. Receta en `references/json_output_fixer.md`.
- **LENGUAJE COMO ACTO SOCIAL (exp_SGM_0049, 2026-08-03):** para que el HRR BRILLE en lenguaje hay que sacarlo de "predecir token" y usarlo para DESCRIBIR/COORDINAR entre dos agentes con mundos distintos (la idea de Luciano: "el lenguaje nace para describirse/describir a otro"). Diseño que funcionó: 2 agentes con ω propio (cada uno transita su mapa), ENCUENTRO FORZADO (arrancan juntos y transitan 25-30 pasos para garantizar pivotes comunes — en 60×60 sin forzar, `A.visited & B.visited` sale vacío y el joint attention no tiene ancla), JOINT ATTENTION sobre pivotes → puente A↔B (cada uno guarda `bridge[("B",celda)] = B.cell_hrr(celda)`). Métrica POR COMPORTAMIENTO: B debe identificar la CELDA EXACTA que A señaló (`hit = best==target`), NO "evitar" (trivial: casi siempre elige otra celda ≠ target y da 1.0 = NC). CLIMAS: bajo **peligro_compartido** el puente funcionó (comunicación 0.375 vs NC 0.0); bajo **cielo_estrellado** apenas (0.2, B casi no transita) y **competencia** no aportó (0.125=NC). HALLAZGO coherente con Tomasello: el lenguaje emerge bajo PRESION COMPARTIDA (joint attention con necesidad), no por estar juntos ni por competir. Faltó medir dolor/belleza (mapa 30×30: agentes no pisan veneno en 250 pasos; B casi no transita). Ver `references/decoder_relational_hrr.md` (sección lenguaje).
- **TRAMPA de métrica "evitar" (0049, 2026-08-03):** `avoid_ok = (best_b != target_cell)` da 1.0 = NC porque casi siempre elige otra celda. Para medir comunicación/identificación usar `hit = (best == target)` (acierto en celda exacta; NC ~ 1/N). Misma clase que los anti-patrones de auditoría: una métrica que da 1.0 para el control es inválida. Sospechá de cualquier métrica donde el NC empata al caso positivo.
- **MOTOR DE AFINIDAD 0044 NO ESCALA A MAPA GRANDE NI NAVEGA METAS (0049b, 2026-08-03 — HALLAZGO DE DISEÑO):** el `Agent` de 0044 (huella + frontier + abur, mapa 12×12) en mapa 30×30 con 2000 ticks apenas visita ~15 celdas y NO llega a claves/barreras. El "encuentro forzado" (arrancar juntos 25-30 pasos) y la atracción `aff += 5.0/(1+gd)` a una `goal` NO alcanzan porque el paso es 1 celda/tick y el camino está bloqueado por las propias barreras → nunca llegan. RESULTADO: puente=0, coordinación=0, dolor=0 en todos los climas. Esto NO es falla del HRR ni del sustrato de lenguaje: es que **falta infra de NAVEGACIÓN (pathfinding BFS/A* hacia metas)** antes de poder simular "nacimiento del lenguaje bajo presión" o cualquier coordinación en mapa >12×12. El lenguaje necesita cuerpos que se desplacen y se encuentren; los del motor 0044 no se desplazan en mapa grande. REGLA: antes de simular coordinación/encuentro en mapa >12×12, agregar un motor de pathfinding real (BFS desde `pos` hasta `goal`, ignorando barreras bloqueadas) y usar esa ruta como la ACCIÓN del agente, no afinidad local + meta-lejana. El hallazgo válido de 0049 (lenguaje bajo peligro compartido, puente 0.375 vs NC 0.0) SÍ es real porque usó mapa chico + encuentro corto donde coincidieron; 0049b lo invalidó por falta de tránsito. Ver `references/decoder_relational_hrr.md` (sección 0049b).
- **BFS DA CUERPO AL AGENTE (exp_SGM_0049c, 2026-08-03 — CIERRA el hallazgo de 0049b):** agregar `bfs_next(world, src, goal, Apos, Bpos)` (BFS sobre grid, ignora `world.blocked` salvo barreras cerradas) y que `Agent.step` SIEMPRE tenga `self.goal` (fase 1: explorar celda no visitada más cercana; fase 2: clave de barrera). Con BFS: `visited ~890` celdas (vs ~15 de 0049b), **COORD barreras 3/3,4/4,5/5 = 100%** (cada uno va a su clave, al coincidir se abre — coordinación real, no sorteable de a uno), **DOLOR REAL** (competencia 83/92, peligro 67/78 — pisaron veneno porque a veces no hay vuelta), **BELLEZA EMERGENTE**: cielo_estrellado `star_reconoce=0.125` (>0!) → A señaló estrellas a B y B las reconoció bajo presión baja; competencia/peligro dan `None` (no hay estrellas). CONFIRMA la hipótesis de Luciano: lenguaje/belleza emergen bajo presión COMPARTIDA y BAJA, no bajo hambre. DEBILIDAD de métrica: `describir()` (hit celda exacta por coseno HRR sobre ~890 celdas visitadas) da 0 = NC por **CROSSTALK HRR** (mismo límite de 0048: HRR no aísla 890 ítems en D=256). No significa que no se comunican — la coordinación (barreras 100%) y la estética (belleza 0.125) SÍ se midieron y funcionaron. RECETA: el BFS debe recalcular `goal` cuando `pos==goal` o `nxt is None` (sin eso el agente se clava); y las barreras se definen como `(a, b, blk)` con `blk` bloqueado SOLO si `Apos==tuple(a) and Bpos==tuple(b)`. Ver `references/language_birth_0049.md` para el diseño completo (climas, BFS, belleza, métricas, resultados).
- **CROSSTALK HRR EN MUCHOS ÍTEMS (0049c + 0048 — límite del HRR como recuperador de ítems):** el `cleanup`/`coseno` HRR sobre N ítems con D=256 colapsa cuando N es grande (N~400 palabras en 0048; N~890 celdas en 0049c). El coseno entre ítems distintos es ~ruido → el "mejor" es al azar → hit = NC. Esto REFUERZA el veredicto de 0048: el HRR es para COMPOSICIÓN (roles/anidamiento, 0027-0031) y para COORDINACIÓN POR ROL, NO para RECUPERACIÓN DE ÍTEM de un vocabulario grande. Para identificar un ítem específico entre muchos, usar un canal MÉTRICO (distancia Euclidiana/Manhattan, como el bigrama plano o el embedding de posición lineal de 0032/0033) o bajar N/D. No usar HRR `coseno contra todos los nodos` como descriptor de ítem en vocabularios grandes. Ver `references/language_birth_0049.md`.
- **CIERRE de métrica de comunicación por ALFABETO COMPARTIDO EMERGENTE (0049d, 2026-08-03):** cuando el coseno HRR falla por crosstalk en vocabulario grande (0049c daba 0=NC sobre ~890 ítems), usá como canal de identificación de ítem el **subconjunto de ítems que los agentes comparten de verdad**: el alfabeto que EMERGIÓ del joint attention (`alphabet = list(A.visited & B.visited)[:15]`, las celdas pivote del puente A↔B). D=256 aísla 15 ítems con acierto 1.0 (ver 0029). `describir()` emite `A.bridge[(B,target)]` (HRR del puente) y B recupera por cleanup contra SOLO el alphabet → hit celda exacta. NC honesto: A emite `A.cell_hrr(target)` (ruido relativo a B) → B elige al azar → ~1/15=0.067. RESULTADO: comunicación 1.0 vs NC 0.067/0.0 en los 3 climas; COORD barreras 100%; dolor real.
- **DECODE ANIDADO PROFUNDO (>2 niveles) — HALLAZGO 0059/0059b (2026-08-04), pulido post-0058:** el decode recursivo sobre HRR plano (unbind por rol + cleanup + recurrir sobre el filler) DA: N=64 prof1=1.00/prof2=0.67/prof3=0.67; N=256 prof1=1.00/prof2=0.90/prof3=0.67. O sea **HRR puro satura en ~2 niveles de anidado** (subir D ayuda a prof2 pero no rompe prof3). N=512 TIMEOUT en Android (conv N²=262144 ops/bind) → no usable en celular. Probé Opción 2 (TPR-walk con puntero de nivel sumado al filler, N=128) → prof3/4/5 = 0.56-0.58, PEOR que HRR plano: el puntero se contamina en la bolsa del padre (el hijo queda atrapado en suma(bind(rol,filler)) del padre). Veredicto honesto: el anidado profundo en HRR-SUMADO requiere estructura NO-SUMADA (árbol con slots separados) o N muy grande. NO es bug de decoder, es límite de capacidad del sustrato (crosstalk ~1/√D). El sim vivo (sgm_sim.html) ya exhibe composición a 1-2 niveles, que es lo medido. Receta + números en `references/decode_anidado_0059_0059b.md`. REGLA de flujo que Luciano reafirmó: en investigación abierta, DETENERSE y testear en Python antes de portar; reportar en CRIOLLO; veredicto honesto aunque el mecanismo no escale (no emocionarse al pedo).
- **DECODE ANIDADO — BARRIDO por bloque (0059g/h/i, 2026-08-04) + EMERGENCIA DE COMPOSICIÓN (0056c/d/e):** el barrido de bindings por bloque (propuesta de Luciano) mapea K=1 (superposición pura) → K=3 (slots separados). Veredicto: curva BINARIA (K=1/2 colapsan prof0; K=3 abre prof8+ con 0059g). El resonator canónico NO salva el anidado bajo superposición; K=2 con puntero-rol explícito tampoco (RecursionError: proyectar el puntero N→BLK COLAPSA la identidad del hijo, función many-to-one no inyectiva). CONCLUSIÓN: decode anidado en SGM requiere SLOTS SEPARADOS (K=3); cualquier superposición de rol-puntero colapsa por pérdida de identidad. En emergencia de composición (ILM): 0056c presión-transmisión-conteo ~0.59; 0056d decoder-entrenado-discreto ~0.60 (NO cierra, cuello = código discreto L=3 V=16); **0056e CÓDIGO HD ROLE-FILLER rompe el techo: 0.81-0.93** (cada rasgo atado a su vector-rol, código = suma de bindings N=256; decoder desata por unbind sin ambigüedad posicional; comp. plena EMERGE desde frac=0.4). HALLAZGO: el sustrato DISCRETO es el límite (~0.6); el HD continuo es el mecanismo que lo rompe. Ambas líneas exigen ENLACE POR ROL EN ESPACIO CONTINUO (conecta con 0019 HDC y 0059g). Receta completa + tablas en `references/decode_anidado_0059g_h_i_composicion_0056cde.md`.
- **LENTE DIAGNÓSTICA (reutilizable, 0059h/i vs 0029):** al diagnosticar por qué falla una superposición, distinguir SIEMPRE "ruido acumulativo REVERSIBLE" (SUMA, curva SUAVE, más dims ayudan — caso 0029) de "pérdida de identidad IRREVERSIBLE" (PROYECCIÓN many-to-one, colapso BINARIO, aislar sub-espacio — caso 0059h/i). No es lo mismo y el fix difiere (subir D vs slots separados). Esta lente evitó malgastar tiempo "afinando el resonator" en 0059i: el cuello era la proyección del puntero, no el desate. **subconjunto de ítems que los agentes comparten de verdad**: el alfabeto que EMERGIÓ del joint attention (`alphabet = list(A.visited & B.visited)[:15]`, las celdas pivote del puente A↔B). D=256 aísla 15 ítems con acierto 1.0 (ver 0029). `describir()` emite `A.bridge[("B",target)]` (HRR del puente) y B recupera por cleanup contra SOLO el alphabet → hit celda exacta. NC honesto: A emite `A.cell_hrr(target)` (ruido relativo a B) → B elige al azar → ~1/15=0.067. RESULTADO: comunicación 1.0 vs NC 0.067/0.0 en los 3 climas; COORD barreras 100%; dolor real.
- **PERO ESTO NO ES LENGUAJE EMERGENTE — REINTERPRETADO POR CRÍTICA (2026-08-03):** el salto 0049c(0.0, crosstalk 890 ítems) → 0049d(1.0) vino de RECORTAR el vocabulario a 15 símbolos FIJOS pre-identificados como puentes, no de que el lenguaje emergiera. Con D=256 y solo 15 ítems, exp_0029 YA había demostrado que HRR recupera eso casi perfecto (cleanup memory de 15 símbolos, NO evidencia de comunicación). El 1.0 de 0049d mide "¿HRR codifica/decodifica 15 símbolos conocidos de antemano?" — pregunta ya respondida en 0029. El claim original "Lenguaje de SGM CERRADO y funcional" fue un OVERCLAIM; el registry entry 0049d fue re-etiquetado a HALLAZGO_PARCIAL_REINTERPRETADO. LECCIÓN: reportar 1.0 sobre un subconjunto fijo y pequeño que el cleanup ya aísla NO prueba lenguaje; prueba capacidad HRR (0029). **TESTS DECISIVOS para saber si hay lenguaje real (exp_SGM_0053):** (1) ZERO-SHOT: entrenar alfabeto sobre subconjunto, testear celdas NUNCA señaladas; si cae a azar → memorización de 15 fijos; (2) TOPSIM: correlación Spearman entre distancia ESPACIAL de celdas y distancia HRR de señales — ~0 indica memorización sin composicionalidad; (3) D ESCALADO: repetir 0049c (~890 ítems) con D según ley 0029 (M_max≈200·(D/128)^0.667 → D≈1280 para 890) en vez de recortar vocabulario. Receta en `references/communication_decisive_tests_0053.md`. REGLA DE ORO: al reportar "lenguaje emergente", el canal de identificación NO debe ser un subconjunto fijo y pequeño que el cleanup ya aísla — debe generalizar a ítems no vistos o resolver escala abierta. Ver `references/language_birth_0049.md` (sección 0049d).
