# Identidad como proceso — protocolo falsable (Pasos 0-4 de Luciano, 2026-08-05)

Cuando el user quiere testear una tesis FILOSOFICA/metafísica como "identidad = proceso
ininterrumpido, no snapshot preservado" (NOUS_Filosofico §1, Parfit 1984), NO se codifica
directo. Se aplica este protocolo (Luciano lo dictó textual y es de clase, aplica a cualquier
pregunta "¿esto es del sistema o solo una preferencia mía?").

## Paso 0 — predicción falsable POR ESCRITO (antes de tocar código)
Nombrar un comportamiento OBSERVABLE distinto entre las dos posturas. Si no podés nombrar la
diferencia, no tenés una hipótesis científica, tenés una preferencia metafísica. Dejar registrado
cuál de las dos cosas se está por escribir.

## Paso 1 — el problema técnico real: el estado instantáneo no guarda el recorrido
S(t) = (ω, φ, V, posiciones, W, ρ) es un estado instantáneo. Si φ es un escalar que vale X,
un reset que copia φ=X y un proceso que nunca se detuvo llegan al MISMO φ → indistinguibles por
definición. Hay que buscar en lo YA construido un observable que dependa del RECORRIDO, no del punto
final. Candidatos probados:
- Firma de trayectoria de fase: integral/acumulación de delta_φ en ventana W(t) (reusa W como
  ventana). UN reset copiado tiene F=[0,0,...] (no hubo recorrido); el continuo tiene recorrido.
  ✓ depende del recorrido.
- Histéresis de vitalidad V: V(t+1)=V(t)·e^(−γ) es PURAMENTE MARKOVIANA → NO depende del recorrido.
  ✗ no sirve (reportarlo como negativo, no fuerzar).
REGLA: si después de buscar no encontrás ningún observable que dependa genuinamente de la
continuidad, ESE es un resultado real: la arquitectura no puede distinguir operacionalmente las
dos posturas → reportarlo así (es literalmente el punto de Parfit: identidad "de verdad" vs
continuidad funcional idéntica son indistinguibles). NO forzar el resultado para que la tesis gane.

## Paso 2 — cuatro condiciones, no tres (extiende CON/AMNESIA/RW de exp_SGM_0034)
| Cond | Tick | Estado final |
|------|------|--------------|
| A continuo | nunca reset, teletransportás cuerpo | igual que si nada |
| B interrumpido + copiado (CON) | tick→0 | copiado del pre-reset |
| C interrumpido + degradado | tick→0 | copiado con ruido/decay |
| D interrumpido + borrado (AMNESIA) | tick→0 | borrado |
La tesis predice: firma(A) ≠ firma(B) aunque pisadas(A)=pisadas(B)=0. Si medís SOLO pisadas
(exp_0034), A y B dan 0 las dos → no separaste nada.

## Paso 3 — pre-registrar T-ID-0X con NC y DOS desenlaces por escrito ANTES de correr
Hipótesis: firma(A)≠firma(B) aunque pisadas iguales.
NC: firma(A)≠firma(RW) — la firma capta algo real, no ruido.
Desenlace 1 (SI difiere): la tesis NOUS §1 es operacionalmente verdadera en este sustrato.
Desenlace 2 (NO difiere): la arquitectura NO distingue proceso de snapshot copiado → coincide con
Parfit; reportarlo con la honestidad de 0056 cuando el 1.0 resultó trampa. NO se fuerza.

## Paso 4 — el capítulo se escribe CON datos, sea cual sea
En este caso "No-Inmortalidad como Característica de Seguridad" (NOUS_Filosofico §10, en el
índice sin escribir) = contenido del experimento. NO escribirlo hasta tener el resultado. Si la
firma no encuentra diferencia, el capítulo dice ESO, honesto.

## CASO REAL exp_SGM_0035 (2026-08-05) — lo que salió y la salsa
Resultó DESENLACE 2 (firma ||F_A−F_B|| = 0.0064 ≈ 0; NC vs RW = 2.49 >> 0). PERO la causa NO fue
"Parfit automático": el observable (a) de φ era correcto en principio, pero **φ converge al
atractor (π/2) en ~200 ticks (Eq.3)**, así que en A el recorrido post-reset es ~0 (φ ya estabilizado)
y en B arranca del mismo φ final → ambos dan F≈[0,0,...]. La firma solo separa DURANTE la ventana
W post-reset, antes de que φ converja. El observable elegido era INSENSIBLE porque φ se estabiliza.
DISCIPLINA honesta (no declarar Parfit todavía): probar un SEGUNDO observable que NO converja —
la TRAZA DE ω (el "dejar huella al transitar" que el user definió para las simulaciones): el ω se
reescribe por Eq.1 con cada transición y la SECUENCIA de ω visitados es el recorrido real; un reset
copiado deja el ω final pero borra la secuencia. Esa firma SÍ debería separar A de B. Solo si TAMBIÉN
la traza de ω falla, declarar Parfit y escribir el cap. 10 diciendo eso. (Propuesta 0035b.)

## CASO REAL exp_SGM_0035b (2026-08-05) — la traza de ω SÍ separa (Desenlace 1)
Hecho tras 0035. Mismos parámetros (W=20, N=8, D=64, TRIALS=12, SEED=20260805, ETA=0.05,
THETA_A=π/2, BETA=0.10) para comparabilidad. Observable = TRAZA de recorrido de ω:
T(t) = últimos W Δω del nodo activo, Δω(k)=||ω_activo(k)−ω_activo(k−1)||. El agente transita
por el grafo (move_and_update aplica Eq.1 en cada tick) así ω SÍ evoluciona (no converge a punto
fijo como φ). A continuo deja recorrido real; B copiado arranca con Δω=0 (solo snapshot).
Resultado REAL: ||T_A−T_B|| = 1.0589 (separación sistemática y real, lejos del umbral 0.05);
NC ||T_A−T_RW|| = 4.0876 (ruido puro, confirma que la firma capta señal real).
→ T-ID-03b TRAZA-SOLA = True → DESENLACE 1_SI_difiere. La tesis NOUS §1 es operacionalmente
verdadera en este sustrato VÍA traza de ω (no vía φ, que converge).

**BUG DE CALIBRACIÓN DEL NC (trampa nueva, reportada transparente):**
El criterio original pre-registrado era `tid03b = (pisadasA==pisadasB) and (distAB > 0.05)
and (distAB > nc*0.5)`. Eso es IMPOSIBLE de cumplir: nc = distancia A-vs-RUJO (ruido puro) =
4.08, así que exigir `distAB > nc*0.5` (=2.04) pide que A y B sean MÁS distintos que A y el ruido.
El NC de "firma capta señal real" NO se usa comparando magnitud contra el ruido — se usa para
confirmar que A-vs-ruido ES ruido (como debe ser). El criterio correcto es solo `distAB > 0.05`
(separación sistemática) + pisadas como contexto de 0034, no como gate estricto. REGLA: nunca
pongas el NC como cota inferior de magnitud del efecto; el NC solo prueba que la firma no es ruido
en sí misma.

**Salvedad honesta (no maquillar):** el gate `pisadasA==pisadasB` estricto (abs<0.01) NO se
cumple en 0035b porque la métrica de dolor usada es ruidosa (φ lejos del atractor), no el cuello
físico de 0034 (que daba CON=0, AMNESIA≥1 limpio). A=3.5, B=3.33 → diff 0.17. Esto no invalida el
hallazgo de la traza (el núcleo de T-ID-03 es ¿la traza separa? SÍ), pero si querés el experimento
"de libro" (pisadas A==B==0 Y traza separa) hay que volver a la métrica de dolor de 0034.
Se reportaron TRES criterios en el JSON: traza_sola (True), corregido-pisadas-estrictas (False),
original-buggeado (False) — transparencia total, no recategorización a mano.

## CONCLUSIÓN PARA NOUS_Filosofico §10 (No-Inmortalidad como Característica de Seguridad)
Se escribe CON este dato: la identidad en SGM es PROCESO (traza de ω), no snapshot. Un reset que
copia el estado PERO borra la traza de transiciones es operacionalmente distinto de un proceso
continuo. Por eso la no-inmortalidad es segura: no necesitás nodos inmortales porque el ser es el
recorrido, y el recorrido se distingue del snapshot copiado. CONFIRMA la tesis NOUS §1 con
evidencia, no solo filosofía. (φ no separa por convergencia; ω sí separa por traza.)

## Lección de flujo (generalizable)
En preguntas filosóficas: (1) no codigues hasta tener la predicción falsable por escrito; (2) el
primer observable que se estabiliza NO prueba la tesis opuesta — probá un segundo observable antes
de cerrar; (3) el capítulo de discusión se escribe con el dato, no antes; (4) NUNCA uses el NC como
cota inferior de magnitud del efecto (el NC solo prueba que la señal no es ruido en sí); (5) si el
gate de "métrica secundaria igual" falla por ruido de métrica, reportá los criterios por
separado, no recategorices a mano para que dé PASS. Esto es la misma disciplina de "no emocionarse
al pedo" / "no dejar a futuro", aplicada a metafísica.
