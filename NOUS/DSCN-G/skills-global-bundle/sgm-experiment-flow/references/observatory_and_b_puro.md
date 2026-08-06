# Observatorio (MiniSandbox) + B-puro: cerrar huecos del sustrato sin hardcode/agregados/bloqueos

Lecciones de la secuencia 0042 (observatorio) → 0043 (B-puro, frustración), 2026-08-03.
Complementa `substrate_vs_authored_design.md` (filtro "¿esto es del sistema?") y la regla
"NO TUNEES EL ENTORNO PARA FORZAR PASS" del SKILL.md.

## Cuándo usar este modo
Cuando el user dice "sigamos experimentando, si falta algo del sustrato lo descubrimos" o propone un
mundo abierto / sandbox para ver qué hace el sistema. Es el MODO INVESTIGACIÓN ABIERTA del Camino A:
correr el sustrato REAL en un entorno abierto y DEJAR QUE EL HUECO APAREZCA, no pre-ensamblar módulos.

## Metodología Observatorio (0042)
1. El agente NO recibe objetivos. Su loop es el tick unificado (0023) / campos (η, dolor, E) + HRR, tal cual.
2. Mapear el entorno a TAREAS DE BENCHMARK CONOCIDO (sin lenguaje, conductuales) para tener métrica comparable
   honesta. Referencia: **Animal-AI (arXiv 1909.07483)** = test battery de cognición animal-like
   (evitación de daño, espacial, herramientas, causalidad). NO comparar contra MineDojo/XLand (RL a escala
   internet + billones de params) — sería desleal. El marco de comparación honesta es: "¿SGM resuelve la
   tarea usando SU mecanismo, contra un baseline ciego en el MISMO entorno?".
3. Reportar un NO-PASS como HALLAZGO, no como fracaso a maquillar. El hallazgo de 0042 fue: el sustrato
   respondía LOCALMENTE a campos (evitaba celda de dolor −1.75, buscaba comida adyacente +1.05; el NC sin
   dolor no penalizaba) PERO la EXPLORACIÓN GLOBAL no escalaba (oscilaba 5 celdas/300 steps). Ese es un HUECO
   DEL SUSTRATO, no un bug de un test.
4. VERIFICAR que el mecanismo responde localmente ANTES de decir "no funciona" (debug de afinidades desde
   una celda con estímulo adyacente). En 0042 eso confirmó que campos OK, falla solo la exploración.

## Cómo cerrar el hueco: regla B-puro (0043), exigencia de Luciano
"no me gustaría que hayan bloqueos, hardcode o agregados extras". Tres prohibiciones y su traducción honesta:

- **Sin hardcode**: NO escribir `if abur > UMBRAL: explora` ni `if nombre == "x"`. El campo debe modular la
  afinidad POR SÍ MISMO.
- **Sin agregados extras**: NO agregar estado nuevo (ej. un mapa de familiaridad, o un set de "celdas
  visitadas" que se usa como memoria de mundo). Usar SOLO lo que el sustrato YA TIENE.
- **Sin bloqueos**: NO prohibir "volver a la celda previa" como regla. El agente debe romper la oscilación
  SOLO porque repetir se vuelve menos atractivo.

### Aplicación concreta que pasó (0043)
- El campo `abur` (0036) YA EXISTÍA pero en 0042 estaba DESCONEctADO de la acción (variable muerta).
- El `last_pos` (memoria de trabajo, 0020) YA EXISTÍA.
- Acoplamiento honesto: la afinidad de volver a `last_pos` lleva PENA = `abur` (misma moneda del campo,
  peso 1.0 — NO un número mágico elegido por el autor). A medida que `abur` sube (novedad hundida),
  repetir pesa menos → el agente se va. ROMPE la oscilación sin regla ni estado nuevo.
- Marco teórico que respaldó esto: **Active Inference (arXiv 2010.00262)** — la exploración EMERGE de
  minimizar sorpresa (error de predicción = η = dopamina), no de un módulo de mapa. Respaldó B-puro sobre
  la Opción A (mapa cognitivo generativo, arXiv 2504.20628) que habría requerido agregar estado.

### Tests con negative control (lo que probó que emergió del sustrato, no de mi regla)
- T-FR-01: celdas visitadas CON `abur` dinámico = 107 vs SIN `abur` (NC) = 5.
- T-FR-02: retornos a `last_pos` dinámico = 60 vs NC = 296 (el NC rebota casi 1/step).
- T-FR-03 (NC): SIN `abur` reproduce exactamente el hallazgo de 0042 (5 celdas) → confirma que la exploración
  emergió del campo `abur`, no de una regla mía.

### Riesgo de la trampa al reparar
Si al cerrar el hueco tengo que ajustar PESOS a mano para que "explore", caí en la MISMA trampa de 0041
(parámetros del autor disfrazados de resultado). El peso de pena de retorno debe ser 1.0 = la misma moneda
que `abur`. Si el comportamiento solo sale con un peso arbitrario → es del autor, no del sistema.

## Literatura que guió (buscar vía arXiv — ver references/arxiv_literature_recipe.md)
- Animal-AI 1909.07483 — benchmark de cognición animal-like (tareas conductuales, sin lenguaje).
- Active Inference 2010.00262 — exploración por minimizar sorpresa; marco de 0043.
- Cognitive maps are generative programs 2504.20628 — mapa cognitivo como programa generativo (Opción A, no usada).
- Scheduled Intrinsic Drive 1903.07400 — exploración intrínseca jerárquica.

## Checklist antes de afirmar PASS en modo observatorio/B-puro
1. ¿El mecanismo que "cerró el hueco" usa SOLO campos/estado que el sustrato ya tenía?
2. ¿El peso de acoplamiento es la misma moneda del campo (1.0), no un número mío?
3. ¿El NC reproduce el hueco original (sin el mecanismo) → confirma emergencia del sustrato?
4. ¿El agente ROMPE la oscilación SOLO (sin `if`/bloqueo mío)?
