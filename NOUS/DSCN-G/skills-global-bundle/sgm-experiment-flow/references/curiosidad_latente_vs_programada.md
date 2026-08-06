# Curiosidad / drive intrínseco: latente vs programado (exp_SGM_0035 / 0036)

Luciano pidió un agente que "decide explorar por su cuenta, de forma más latente" y señaló que
eso requiere estratos superiores a los que venimos trabajando. Distinción operacional HONESTA
(2026-08-03) antes de codear.

## Lo que ya tenemos (estrato bajo/intermedio)
- Homeóstasis (valencia E, dolor Eq.6), memoria persistente (ω, dolor_count), modos tipados
  (RAZONAL/SENSORIAL/PLAN, 0016/0020), identidad (self-state a través de reset, 0034).
- Una "curiosidad" implementada como bonus de exploración en `choose_move` (premiar celdas no
  visitadas / baja entropía de ω) es un DRIVE PROGRAMADO: el sistema empuja al agente por un
  término en la función de costo. El agente NO "quiere" explorar — es empujado. Como hambre
  artificial, no inquietud.

## Lo que Luciano quiere (estrato superior — "querer explorar por su cuenta")
Requiere que la curiosidad EMERJA de la dinámica interna, no de un término impuesto. Mecanismos
honestos (no humo):
1. **Predicción de error como drive:** modelo interno del mundo (ω de transiciones); cuando la
   predicción falla (surprise alta), eso genera valencia positiva (dopamina-predicción-error,
   tipo Schmidhuber/Free Energy). La curiosidad nace porque reducir la sorpresa es homeostático.
2. **Aburrimiento / homeostasis de estimulación:** si E (valencia) lleva mucho tiempo en equilibrio
   sin novedad, un término de "aburrimiento" sube y empuja a buscar novedad. Es LATENTE.
3. **Metacontrol de modo:** un estrato que, según el historial, elige entrar en modo exploratorio.

## 0035 (curiosidad PROGRAMADA — sustrato bajo) — RECETA QUE PASÓ
- Agente con `visitas[celda]`; `choose_move` suma bonus: `costo(nb) = manhattan(nb,meta) - ALPHA*novedad(nb)`,
  novedad = 1/(1+visitas[nb]).
- Maze 10x10 aleatorio (reusa gen_maze/bfs_path de 0032). Comparar GREEDY (sin visitas) vs
  CURIOSO vs RW (NC).
- Resultado: CURIOSO 35% vs GREEDY 7.5% (se traba rebotando en callejones) vs RW 15% (no focaliza).
  T-CUR-01/02 + NC PASS. Documentado como estrato bajo (el agente no "elige").

## 0036 (curiosidad GLOBAL como CAMPO del sustrato) — RECETA QUE PASÓ (el que quería Luciano)
PRINCIPIO CLAVE: la curiosidad debe ser un CAMPO del sustrato (hermano de E y dolor en el tick
unificado), NO un módulo add-on tipo 0035. Si η vive solo en el maze, la curiosidad es local y
falsa; si es campo global, modifica modos / duda / recuperación / atención en TODO el sistema.

DISEÑO (test-first, con NC):
- `eta = 1 - cos(omega_pred, omega_real)` tras cada tick (forward model = reusa transición por
  afinidad del 0023; predice el ω del vecino elegido, compara contra el ω real). Es variable de estado.
- `dopamina(eta) = exp(-((eta - ETA_OPT)/SIGMA)**2)` — U INVERTIDA (pico en ETA_OPT~0.30).
  Captura la zona "interesante": eta~0 → aburrimiento (no curiosidad); eta extremo → rechazo.
- `aburrimiento += 1` si eta < ETA_BAJO (~0.05) sostenido; se vacía si eta alto. Disparador
  acumulativo (no instantáneo como el RPE). Si `aburrimiento >= THETA_ABURR` → elige la acción de
  MAYOR novedad (1/(1+visitas)) SIN término externo.
- `choose()`: lee eta global: eta alto → explora (penaliza visitado para salir de callejón);
  eta~0 + aburrido → busca novedad; zona óptima → explota (greedy a meta).
- NOVEDAD BRUTA (fallback cuando no hay modelo): reusa memoria de visitas de 0035. El humano
  también es curioso sin modelo (el bebé frente a luz nueva) — necesita las DOS fuentes.

TESTS (todos honestos, con NC):
- T-CURI-01/03 (nace del sustrato + homeostasia): tasa GLOBAL(eta) >= 0.35 (no peor que 0035) y
  el sistema SIGUE CERRANDO la tarea (no loop de exploración infinita).
- T-CURI-02 (U invertida / aburrimiento): con modelo perfecto (eta~0 sostenido), el acumulador
  dispara búsqueda de novedad por su cuenta (sin forzar desde afuera) — medir >=1 caso.
- T-CURI-04 (modifica valores previos): GLOBAL >= BASE(0023-like, solo greedy) en el mismo maze.

RESULTADO 0036 (medido, 40 trials, maze 10x10):
- GLOBAL(eta): 50% de llegada.
- BASE (0023-like greedy sin curiosidad): 5% (se traba igual que greedy de 0035).
- Aburrimiento disparó novedad: 4/40 casos (T-CURI-02 REAL, no programado).
- Pasos: 25.8 global vs 18 base (margen OK).
- T-CURI-01/02/03/04 + NC: PASS. Supera 0035 (35%) y aplasta base (5%).

HONESTIDAD: medimos el OPERADOR (eta -> dopamina(eta) -> explora), NO el qualia de "interesarse"
(igual que con dolor/valencia — problema del otro cuerpo). El 0036 NO rompe homeóstasis (NC ✅):
el η no dispara loop infinito porque el aburrimiento tiene tope y la dopamina(eta) cae cuando eta
es extremo.

## MAPEO HUMANO → SGM (charla previa a 0036, para no medir humo)
- Curiosidad humana = ERROR DE PREDICCIÓN (dopamina RPE, Schultz), NO "deseo noble de conocer".
  El cerebro minimiza sorpresa (Friston Free Energy); el error de predicción ES la fuerza, intrínseca.
- CURVA DE U INVERTIDA (Berlyne 1954): novedad óptima en el medio; muy conocido = aburrido,
  muy extraño = rechazo. La dopamina(eta) del 0036 la captura.
- GAP DE INFORMACIÓN (Loewenstein 1994): la curiosidad es tensión desagradable de saber que falta.
- ABURRIMIENTO = homeostato que dispara cuando el modelo predice todo (eta~0 sostenido). El
  aburrimiento acumulado del 0036 lo implementa.
- SOPORTE NEURO (Kang 2009): dopamina + mejor consolidación hippocampal en estado curioso.
- LO QUE NO SE PUEDE CAPTURAR: el qualia de "interesarse" (mismo límite que dolor/valencia).

RIESGO HONESTO al pasar η a todos los modos: podría desestabilizar el 0023 (ya delicado). El NC
(T-CURI-03) debe verificar que el sistema sigue cerrando tareas. Próximo propuesto: 0037 =
enchufar η global en el sgm_tick_unificado canónico (no módulo aparte) y medir modos/duda en
tarea cognitiva; 0038 = balance dolor vs curiosidad (usar 0033b: ¿el η frena ante dolor o el
aburrimiento lo vence?).

## Conecta con identidad (0034)
La curiosidad latente depende de que el self_state persista (el "aburrimiento" es un estado del
self, no del entorno). 0034 ya probó que ω+dolor_count sobreviven al reset; eso es el andamiaje
para que un drive intrínseco sea estable entre episodios.
