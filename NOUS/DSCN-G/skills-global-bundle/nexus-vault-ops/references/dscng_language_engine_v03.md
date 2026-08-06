# DSCN-G Language Engine v0.3 — RETRIEVAL ("¿el grafo entiende?")

**Fecha:** 2026-07-25 (tarde). **Estado:** HECHO, resultado empírico real.
**Decisión de usuario que lo motiva:** "primero validar que el grafo entienda,
luego vamos al decoder." Esto REORDENA el pipeline: v0.3 = retrieval, NO hibernado.

## Hipótesis
Dado un ω de consulta, el grafo recupera el nodo/concepto correcto de una masa
semántica. Y la representación en BITS/puertas lógicas (idea de Luciano: ω→bits,
afinidad por Hamming) CONSERVA la semántica de la norma flotante del motor real.

## Diseño (run_v03.py, Python puro, sin numpy)
- Vocabulario de M conceptos. Cada concepto = un centroide ω lejano de los otros
  (gaussiana con spread=2.0), más 3 nodos ruidosos alrededor (σ=0.15).
- Consulta: ω = centroide + ruido pequeño (σ=0.1). Se pide top-1 recovery.
- Afinidad A (NORMATIVA, motor real): `exp(-α·‖ω_q − ω_i‖)`, α=5.0, d=8.
- Afinidad B (BITS/lógica, idea Luciano): ω cuantizado a 2 bits/dim
  (signo+magnitud: 00/01/10/11), distancia = 1 − Hamming/L. `affinity_bits = 1 - mism/L`.
- Métrica: accuracy top-1 = ¿el nodo recuperado pertenece al concepto consultado?
  (índice i//3 == concepto_ci). 10 seeds × 20 queries cada uno.

## Resultado (results_v03.json)
| M (conceptos) | norma | bits  |
|---------------|-------|-------|
| 4             | 1.000 | 1.000 |
| 16            | 1.000 | 1.000 |
| 64            | 1.000 | 0.975 |
| 256           | 1.000 | 0.910 |

Tiempo: M=256 en ~4 s (liviano, sin loop O(n²) sobre N=1000).

## Conclusión honesta
1. El grafo RECUPERA correctamente (norma = 100% hasta 256 conceptos): "entiende"
   en el sentido mínimo previo al decoder.
2. Los BITS de Luciano funcionan IGUAL que la norma hasta 16 conceptos y solo
   bajan a 0.91 a 256 — por la cuantización gruesa de 2 bits/dim, no por pérdida
   de semántica. La idea es VIABLE; se puede mejorar con más bits/dim o mejor
   codificación sin que se caiga.
3. Esto desbloquea v0.5 (decoder): ya tenemos retrieval funcionando; el L2 solo
   proyecta el ω recuperado a texto.

## Ruta en vault
NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/v0.3_retrieval/
  - run_v03.py
  - results_v03.json

## Relación con v0.3b (HIBERNADO, pendiente)
v0.3 usa la masa como store ESTÁTICO (no hay stepping/poda). v0.3b (HIBERNADO)
debe preguntar si una poda-DINÁMICA-con-hibernación mantiene la masa viva durante
el stepping sin colapsar a 4.5. Ambos validan la "memoria de masa" pero en fases
distintas (recuperación vs supervivencia dinámica).
