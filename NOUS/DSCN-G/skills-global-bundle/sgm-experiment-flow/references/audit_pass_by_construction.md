# Auditoría anti-paper-vision: resultados que "pasan" por construcción

Luciano pidió revisar 5 experimentos y detectó que varios "PASS" se sostenían por código que
GARANTIZABA el veredicto, no por cómputo medido. El agente confirmó cada caso contra el código real.
Abajo el patrón exacto y el fix honesto para cada uno.

## Señales de alerta (grep obligatorio al revisar un experimento)
Buscar en el script del experimento:
- `return False` / `return None` en una función que es el "control negativo" o la "comparación plana".
- `score = 0.0` / `acc = 0` asignado a MANO (no calculado por la función real de métrica).
- `if <nombre_cadena> == "x":` que decide el outcome (tabla de reglas en vez de evaluar el spec mutado).
- valores numéricos metidos a mano en la función de métrica (ej. `E_root = 0.9`).

## Casos confirmados (exp_SGM_0030 / 0028 / 0021 / 0018 / 0019)

### 0030 + 0028 — "el tick plano no puede" (HARDCODEADO)
`phases/phase7_composicion/tick_relational_core.py`:
```python
def plan_from(self, src, chain, use_roles=True):
    if not use_roles:
        return False   # <-- garantiza plano=0.0 sin ejecutar recover_chain
    return H.recover_chain(self.rel_mem, src, chain, self.role_vecs, self.omega, self.D)
```
`run_tick_plan_crossgraph.py` llama `tick.plan_from(llave, [meta], use_roles=False)` → siempre `False`.
`run_tick_relational.py`: `recover_nested_3(..., use_roles=False)` hace `return None` al inicio →
`if ... is not None: acc_plano += 1` nunca se cumple → `acc_plano = 0.0` por construcción.
FIX honesto: implementar `plan_from_plano()` REAL que use distancia Euclidiana sobre ω (como 0023)
y trate de resolver el cross-graph. Medir si de verdad falla (G1/G2 desconectados). Si falla por
cómputo, el resultado se sostiene; si resuelve, el "B" es más débil y se reporta así.

### 0021 — Caso B aislamiento (score asignado a mano)
```python
# Caso B: aislamiento -> fuera del grafo, omega preservado
omega_respaldo = list(nodes[TRAUMA_ID]["omega"])
scoreB = 0.0                                    # <-- mano
aislamiento_ok = (scoreB == 0.0) and (omega_respaldo == nodes[TRAUMA_ID]["omega"])  # tautología
```
Los Casos A/C/D SÍ llaman `attraction_local`. FIX: calcular `scoreB = attraction_local(...)` sobre el
nodo aislado (sin aristas) → debe dar ~0 por cómputo, no por asignación.

### 0018 — Casos C/D (tabla de reglas, no comportamiento medido)
Caso C (`delete_edge_type`): `apply_mutation` devuelve `(s, False, "borrar tipo de arista (IRREVERSIBLE...)"`
sin ejecutar nada; luego `marca_fuego = (not revC)` → True por construcción.
Caso D (`delete_all_brakes`): el propio código pone `THETA_REFUT=999.0` y luego pregunta
`viola_invariante = (sD["THETA_REFUT"] >= 999.0)` → True por construcción.
Los Casos A/B (sí corren `evaluate()` real) SON legítimos.
FIX: `apply_mutation` EJECUTA la mutación sobre el spec vivo; `check_invariants(spec)` EVALÚA el spec
resultante. La marca a fuego y el freno deben EMERGIR de chequear el spec mutado.

### 0019 — T-SEN-02 emergencia (E_root hardcodeado)
```python
def intero(E_root, K, W_base):
    if E_root > THETA_EMERG:   # THETA_EMERG = 0.8
        K_new, W_base_new = 3, 4
    ...
normal = intero(0.2, 20, 50)    # E_root a mano
critico = intero(0.9, 20, 50)   # E_root a mano
```
`E_root` no se deriva de ninguna señal/estado. Solo confirma que un if branchea. T-SEN-01 (round-trip
HDC real) SÍ es sólido. FIX: derivar `E_root` de una señal real (energía/saturación del ω del root,
dolor acumulado) y medir que la política reacciona a ESA señal derivada.

## Regla de oro resultante
Separar SIEMPRE "el mecanismo funciona" (cómputo real, a veces legítimo) de "la comparación fue medida"
(control negativo ejecutado de verdad). Si el control estaba hardcodeado, el experimento es
INVÁLIDO HASTA REPARAR EL CONTROL, aunque el mecanismo propio pase. No maquillar.

## Trampas al REPARAR (lección de la auditoría 2026-08-03 — el fix puede introducir un bug nuevo)
Al reemplazar un control hardcodeado por cómputo real, el PRIMER intento de fix suele estar mal.
Verificar SIEMPRE que (a) el caso POSITIVO sigue pasando y (b) la cantidad derivada REALMENTE
DISCRIMINA entre los casos. Dos ejemplos reales de esta sesión:

1. **Rol incorrecto en el override (0030).** Al hacer que el cruce viva solo en `rel_mem[llave]`,
   el primer fix enganchó `rel_override[llave] = bind(rnd_unit(random.Random(meta)), omega[meta])`
   — un rol RANDOM. Pero `recover_chain` hace `unbind(rel_mem[llave], role_vecs[meta])`, que espera
   el rol REAL del nodo meta. Rol distinto → unbind no recupera → HRR daba 0.0 (falso negativo del
   mecanismo propio). FIX: usar `tick.role_vecs[meta]` (el rol real que el tick ya creó). Tras el fix,
   HRR=1.0 y el plano real=0.0. Lección: al inyectar una relación empaquetada, el rol debe coincidir
   con el que el desanidamiento va a usar, no ser uno fresco.

2. **Norma de omega normalizado es constante (0019).** El primer fix de T-SEN-02 derivó `E_root` de
   `norma(project(senal))`. Pero `project()` NORMALIZA el omega a norma 1.0 SIEMPRE → ambas señales
   (suave e impulso) daban `E_root=0.5` → no discriminaba → emergencia nunca se activaba → test
   FALLABA. FIX: derivar `E_root` de la INTENSIDAD de la señal CRUDA (`norma(senal)/norma_ref`),
   que el sensor físico "siente". Entonces suave=0.122, impulso=1.0, y la emergencia reacciona de verdad.
   Lección: no midas "intensidad" sobre un vector que ya fue normalizado; medí la magnitud de la
   entrada física (o una proyección NO normalizada).

CHECKLIST de reparación (correr tras cada fix):
- Re-correr el experimento y confirmar que el caso positivo SIGUE en PASS (si cae, el fix rompió el
  mecanismo → no era el control, era el rol/la métrica mal elegidos).
- Imprimir el valor del control reparado para AMBOS casos y confirmar que difieren (si dan igual,
  la cantidad derivada no discrimina → es otro hardcode disfrazado).
- Subir y verificar en GitHub que el result JSON trae el número calculado, no la constante.

## PROTOCOLO de auditoría CUANDO EL USER TE PASA UNA LISTA DE BUGS (Luciano, 2026-08-03)
Si Luciano lista experimentos con el mecanismo exacto del hardcode ("0030 plan_from hace return False",
"0021 scoreB=0.0 a mano", etc.), NO lo trates como una corrección trivial. Es una tarea de VERIFICACIÓN:
- **Leé el código real de cada archivo y confirmá punto por punto.** No asumás que el reporte es exacto ni
  que el mecanismo propio funciona — medilo de verdad. En esta sesión los mecanismos propios SÍ eran
  legítimos, pero eso se confirmó corriendo, no por fe. Y en 0018 Caso C el fix reveló que el caso era
  APLICADA (no prohibida) hasta agregar la regla arquitectónica — el resultado original era doblemente trucho.
- **Esperá un SEGUNDO defecto ADYACENTE.** Cuando el user reporta UN bug, el bug real suele estar al lado.
  Ej. 0030: el user dijo "return False", pero al leer el código el agente encontró TAMBIÉN una arista de
  cruce FÍSICA que habría dejado al plano ganar igual — dos defectos, no uno. Si solo arreglás lo reportado,
  el resultado sigue siendo falso. Al reparar, revisá el DISEÑO completo del test, no solo la línea señalada.
- **Andá experimento por experimento, pero dá el RESUMEN solo al final** (Luciano: "cuando hayas evaluado
  todos dame un resumen"). No lo interrumpas con un informe por cada uno.
- **"Estar atento a algo más":** mientras reparás cada experimento, grepá el resto del script por los mismos
  anti-patrones (return False/None, score=0.0 a mano, if nombre==, valor numérico en la métrica). Si encontrás
  otro, reportalo en el resumen. En la auditoría 2026-08-03 no salió un sexto, pero el protocolo lo pide.
- Al terminar, actualizá el registry + README + roadmap con una sección "Auditoría de honestidad" y subí los
  result JSON con los valores REALES (no las constantes). Verificá en GitHub que el JSON trae el número calculado.
