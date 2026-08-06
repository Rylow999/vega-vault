# Substrate vs Author-Authored Design (lección 0040/0041, 2026-08-03)

Luciano detectó que los experimentos de la "capa cognitiva superior" (discurso interno 0040,
moral 0041) NO miden propiedades del sustrato SGM: miden propiedades del código que el agente escribió.
Es la MISMA trampa del paper-vision que venimos auditando en 0030/0028/0021/0018/0019, pero en una
forma que no cae en los greps del checklist de auditoría (no hay `return False`, no hay `score=0.0` a
mano). Por eso merece su propia sección.

## La trampa: "función del autor disfrazada de resultado del sistema"

El agente escribe una función con reglas/pesos/tablas propias y luego mide que "el sistema" se comporta
según esas reglas. El cómputo es real, pero la CONDUCTA EMERGE DE LA FUNCIÓN DEL AUTOR, no del grafo/tick.

### 0040 — discurso interno (INVÁLIDO como resultado del SGM)
- `reflexion(state)` = árbol `if/elif` escrito por el autor que decide quién "gana" el conflicto.
- T-DI-01 medía "la acción es coherente con la decisión de la traza". PERO la traza la generó la MISMA
  función que tomó la acción → coherencia garantizada por construcción.
- Como decirle a alguien "¿tomaste la decisión que decidiste tomar?" → siempre sí. No mide mecanismo.
- El "discurso interno" DEBERÍA ser un loop donde los CAMPOS del tick (η, dolor, E, modo, duda) resuelven
  el conflicto por su dinámica (transición por afinidad + pesos), no por reglas del autor.

### 0041 — moral (INVÁLIDO como resultado del SGM)
- `self_benefit = ALPHA*payoff + BETA*coherencia` con ALPHA=1.0, BETA=0.4, GAMMA=0.92 y tabla ECOL del autor.
- Que "en A ayuda / en B lastima" es CONSECUENCIA DIRECTA de esos parámetros y de ECOL, NO emerge del grafo.
- El NC (hardcoded da igual en A y B) solo prueba que la hardcoded es peor, NO valida esta alternativa.
- La nota T-MOR-04 mezclaba el ejemplo personal de Luciano ("caso realista de Luciano") → ilegible como
  resultado neutral; se neutralizó.
- La MORAL SÍ puede ser emergente de campos reales (payoff = señal del mundo; registro = self-state real
  del 0034; coherencia = peso del registro). Pero en 0041 eran parámetros del autor, no del sustrato.

## Filtro de "¿esto es del sistema?" (aplicar SIEMPRE en capa superior)

Antes de afirmar PASS en discurso interno / moral / juicio / atención / metacontrol:
1. ¿La decisión sale de la DINÁMICA DE LOS CAMPOS del tick (transición por afinidad + pesos η/dolor/E sobre
   ω reales del grafo), o de una función/pesos/tabla que el autor escribió?
2. Si mido "coherencia con la traza / con la decisión", ¿la traza la generó el MISMO código que decidió?
   Si sí → circular, no mide mecanismo.
3. Si cambio ALPHA/BETA/GAMMA/ECOL por otros valores razonables, ¿el resultado se INVIERTE? Si sí → es del
   autor, no del sistema.

Si cualquiera es "del autor" → marcar `status=PROPUESTA_DE_DISENO_NO_SUSTRATO`, `verified=False`. El
experimento sigue valiendo como DISCUSIÓN DE DISEÑO, pero NO se cuenta como propiedad medida del SGM.
(Así se hizo: registry + result JSON de 0040/0041 sellados; README/roadmap actualizados a PROPUESTA.)

## REGLA DE ORO DE LA CAPA SUPERIOR (corrección filosófica de Luciano, 2026-08-03)
La distinción anterior (¿esto es del sistema?) es necesaria PERO INSUFICIENTE. Hay un paso previo que
Luciano planteó y que cambia el enfoque de toda la capa cognitiva superior:

**La moral, el discurso interno, el juicio, la atención, etc. son CONCEPTOS — etiquetas que NOSOTROS
pegamos a un patrón de conducta. NO son cosas que viven dentro del sistema. Si son emergentes, intentar
"integrarlos" es una CONTRADICCIÓN: la emergencia no se integra, se deja pasar.**

Por eso, incluso cuando un mecanismo es 100% del sustrato (ej. la homeostasis + afecto + coherencia de
identidad que SÍ producen una conducta que catalogaríamos como "moral"), la regla es:

- **NO se agrega un módulo/función de "moral" ni de "discurso interno".** Eso sería fabricar una función
  que simula moral = disfrazar código del autor de resultado del sistema (la MISMA trampa de 0041, pero
  esta vez vista antes de codear).
- **SÍ se observa y CATALOGA (afuera, por nosotros) si de la dinámica del sustrato sale conducta que
  etiquetaríamos como cautelosa/coherente/pro-social.** La etiqueta vive AFUERA, no adentro.
- Los MECANISMOS que dan lugar a esa conducta SÍ están y son legítimos del sustrato (dolor/evasión 0033/39,
  rel_mem + cross-graph HRR 0030 donde degradar al otro rompe mi propia memoria relacional, coherencia de
  identidad 0034). Esos no son "moral": son homeóstasis y afecto. La moral (el concepto) EMERGE de ellos.

Consecuencia práctica aplicada en esta sesión: el plan original de "reimplementar 4040/41 sobre el sustrato"
se CANCELÓ por ser conceptualmente incorrecto. 4040/4041 se retiraron como experimentos de integración y
quedaron como NOTA CONCEPTUAL: "intentamos integrar conceptos emergentes; es un error de framing; se
descarta. Se miden descriptivamente, no se agregan." Y el MiniSandbox (0042+) se reencuadró como OBSERVATORIO
de emergencia (catalogar si aparece conducta etiquetable), no como "hacer que el sistema tenga moral".

Regla de oro: **en la capa superior, el trabajo honesto es DISEÑAR EL SUSTRATO PARA QUE LA CONDUCTA EMERJA y
LUEGO OBSERVARLA, no diseñar la conducta y luego simularla.** Si alguien propone "integrar X (moral/discurso/
juicio)" como módulo → frenar: eso es el paper-vision trap disfrazado de feature.

## Higiene aplicada junto con esta corrección (dos pedidos de Luciano)
- `demo_grid_state.json` (estado de runtime de la demo HTML) → al `.gitignore`, borrado de repo/local.
- `experiment_registry_mirror.json` → BORRADO (unificar en el registry central `results/experiment_registry.json`,
  como Luciano propuso al arranque y nunca se ejecutó). Cero riesgo de desincronía.
- Regla: nunca mantener dos registries; si en algún momento hubiera dos, el proceso de update debe pisar
  AMBOS juntos o se vuelve imposible saber cuál tiene la verdad.
