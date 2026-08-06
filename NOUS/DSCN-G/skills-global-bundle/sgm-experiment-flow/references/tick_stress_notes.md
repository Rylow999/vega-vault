# exp_SGM_0031 — tick_stress_crossgraph (estrés del tick cruzado, 2026-08-02)

## Por qué existe
Luciano pidió, ANTES del salto a entorno (camino A), "confirmar que no se cae" en escala. El 0030
probó el tick HRR+roles resolviendo un plan cruzado en grafo chico (N~12). El 0031 estresa eso en 3 ejes.

## Diseño (test-first, con NC)
Reusa `tick_relational_core.TickRelational` (infra consolidada en 0030).
Grafo cruzado: G1 = cadena de L nodos (meta en L-1), G2 = llave→puerta→caja, DESCONECTADOS salvo
`edges[llave].append((meta_G1, 0))` (relación "llave destraba meta" empaquetada en nodo llave, rol=índice de meta).
Relleno: distractores hasta N nodos totales.

Ejes:
- TAMAÑO N ∈ {20, 50, 100, 200}
- RUIDO DE SEÑAL σ ∈ {0.0, 0.1, 0.3} (gauss sobre la señal senoidal de entrada al tick)
- PROFUNDIDAD DEL PLAN L ∈ {3, 5, 8, 12}
- NC: roles al azar en el cruce (el cruce apunta a nodo random, no a meta) → debe fallar <0.3

Variable discriminante: tasa de éxito del plan cruzado (HRR+roles) por configuración.
Umbral honesto: si cae <0.7 en alguna, reportar DÓNDE se rompe (no maquillar).
D=256 (ya 1.0 en 0029) para aislar efecto de escala/ruido del de dimensionalidad.

## Resultado (medido, PASS)
- tamano N:   {20:1.0, 50:1.0, 100:1.0, 200:1.0}
- ruido σ:    {0.0:1.0, 0.1:1.0, 0.3:1.0}
- profundidad L: {3:1.0, 5:1.0, 8:1.0, 12:1.0}
- NC roles azar: 0.0
→ anidamiento HRR aguanta estrés completo sin colapsar. Listo para camino A.

## Nota honesta de métrica
El éxito del plan usa `plan_from()` (desanidado por rol sobre `rel_mem`; los ω no se tocan → ruido-invariante),
NO `route()` (que sí depende de la señal HDC y con σ=0.3 puede no caer en el seed exacto). Reportarlo así:
"el tick primero sabe por memoria, luego siente por señal". No maquillar el route ruidoso como si el plan lo usara.

## Bugs encontrados y corregidos (esta sesión)
1. `min(self.omega, key=lambda n: dist(...))` itera VECTORES; adentro `self.omega[n]` usa n como índice →
   TypeError. Fix: `min(range(self.N), key=lambda n: dist(omega_routed, self.omega[n]))`.
2. Patcher de docs con `assert old in t` falló 2 veces por ancla inexacta (`B:` sin `**`, `vision` sin acento).
   Fix: imprimir la línea con `repr()` y copiar textual, o usar `t.find(...)` + reemplazo por rango.

## Siguiente (camino A)
Cuerpo virtual (grid 2D) que recibe señal HDC; el tick decide acción; el cuerpo ejecuta; la señal vuelve; ω
se actualiza. Une composición (Fase 7) + loop cerrado (0025). Ver closed_loop.md de sgm-core-dev.
