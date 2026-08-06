# FATE ← DSCN-G v3: capa cognitiva reemplazada por dinámicas reales

Parche sobre `fate-v6-modular` (commit del 2026-07-19, bajado por codeload).
Reemplaza la capa "cognitiva" de `core/fate_engine.c` — `omega_root` (EWMA de
campeones) + `resonance` (similitud coseno) + `state_weight` (3 buckets
ACTIVE/DORMANT/HIBERNATE por densidad de visitas) — que tenía el nombre de
DSCN-G pero ninguna relación real con sus ecuaciones, por las dinámicas
**auditadas** de `DSCN_G_v3` (`verify_dscng_v3.py`, 6 rondas, 2026-07-22/24):
acoplamiento de fase Kuramoto real + homeostasis por vitalidad real.

**Cómo aplicar:** los archivos completos están en `core/`; o `patch -p1 <
fate_engine.h.diff` / `fate_engine.c.diff` desde la raíz de
`fate-v6-modular`. El resto del repo (CLI, oráculos, chembl) no se tocó.

## Qué cambió, ecuación por ecuación

Cada candidato de la población de FATE pasa a ser un nodo DSCN-G:

| DSCN-G v3 (`verify_dscng_v3.py`) | Campo/función en FATE |
|---|---|
| ω_i (vector semántico) | `Candidate.state` (ya existía — es el vector que FATE busca) |
| φ_i (fase Kuramoto) | `Candidate.phase` — **nuevo campo**, real, no derivado |
| V_i (vitalidad) | `Candidate.vitality` — **nuevo campo** |
| `_apply_kuramoto_coupling` (Ecs. acoplamiento, con el fix de Ronda 6 de snapshot pre-escritura) | `dscng_kuramoto_step()` — corre cada era sobre los primeros `min(pop_n, 64)` candidatos (población ya ordenada por valencia; el propio DSCN-G auditado usa N=50) |
| `_update_vitality_and_prune` (Ec.5) | `dscng_vitality_step()` — corre cada era; poda = **respawn** del slot (FATE tiene población de tamaño fijo, DSCN-G no) |
| `phase_coherence()` (R de Kuramoto) | `dscng_phase_coherence()` — expuesto en `FateState.dscng_phase_coherence` |

Constantes: `alpha=5.0, eta_kura=0.005 (basal), gamma=0.01, theta_death=0.10`
— las `DEFAULTS` de `DSCN_G_v3`, **no** las de `bench/oracle_dscng.py`
(N_ss\*=7, ω\*=0.649747, con dormancy talámica), que no pasaron auditoría.

**Lo que NO se portó:** el mecanismo de hijacking (C3) — la auditoría de
Ronda 6 lo encontró no sostenido a los parámetros originales (0.9% de los
triggers muestra el efecto, ΔPLV medio≈−0.007). Solo se porta lo verificado
(T1 homeostasis, T2/T3 dinámica de fase).

## Dos adaptaciones necesarias (no están en el paper, son decisión mía)

DSCN-G no recibe un objetivo externo — converge hacia su propio ω_ideal.
FATE sí necesita optimizar lo que sea que le pasen. Dos piezas no tienen
equivalente directo en el paper y tuve que decidir cómo resolverlas:

1. **Actividad para la vitalidad.** DSCN-G la saca de K cadenas de paseo
   aleatorio. FATE no tiene eso — reutilicé la densidad de visitas del
   `topo_map` que FATE ya calculaba (mismo rol: "¿esta región se visita
   seguido?"), en vez de inventar una señal nueva.
2. **Fase derivada para candidatos de escape.** Los candidatos que genera
   CTEG en un escape son vectores nuevos sin `phase` propia todavía. Uso la
   media circular de las componentes del propio vector de estado como fase
   "derivada" — es el mismo truco que el `topo_map` ya usaba para mapear un
   vector a una celda.

Ninguna de las dos es una ecuación del paper — son puentes de ingeniería
para que las ecuaciones auditadas tengan sentido dentro de la arquitectura
de FATE. Las marco explícitamente en los comentarios del código.

## Verificación hecha (no solo compilado)

- `gcc -O3 -Wall -Wextra` → **0 warnings**.
- `gcc -fsanitize=address,undefined` sobre el binario completo (`main_v5` +
  `fate_engine.c` + `chembl_oracle.c`), corrido contra rastrigin D=10,
  budget=300 → **sin hallazgos**.
- Smoke test dedicado (`dscng_smoke_test.c`, incluido acá) que llama
  `fate_step` directo 100 eras, imprime R de Kuramoto y vitalidad media cada
  20 eras, chequea NaN explícitamente → limpio bajo ASan/UBSan también.
  R sube gradualmente (0.13→0.16 en 100 eras) y vitalidad decae gradualmente
  (1.0→0.65), sin poda todavía a esa escala — consistente con que
  `eta_kura`/`gamma` son los valores *basales* del paper, pensados para
  correr miles de pasos, no cientos.
- Repliqué el smoke test que ya usa `FINALIZACION.md` del repo
  (`--dim 10 --oracle rastrigin -n -C -b 100 -s 42`), con y sin la capa
  cognitiva (`-n`) → ambos corren limpio, mismo formato de salida JSONL.

**Lo que NO verifiqué:** no corrí los benchmarks completos (ChEMBL/EGFR/
aspirina) para ver si el cambio mejora o empeora el `best_fit` reportado en
el README del repo — eso requiere `rdkit` y los datasets, que no están en
este entorno. Antes de reemplazar la capa cognitiva vieja en el repo real,
correr `bench/run_v6_benchmark.py` con ambas versiones y comparar.

## Compatibilidad con la CLI

`-n` (`use_cog=0`) y `-C` (`cog_fix=1`) de `main_v5.c` siguen andando igual
que antes — `cog_fix` ahora amplifica los pesos de coherencia/vitalidad
(0.45/0.35) en vez de resonancia/estado, mismo rol. No toqué `cli/main_v5.c`
ni `oracles/pipe/main_v5_pipe.c`.

## Nota aparte, no relacionada con este cambio

Al tocar la función que reemplacé noté que usaba un buffer de stack
`double or_norm[MAX_DIM]` con `MAX_DIM=1024`, pero el README de este repo
reporta benchmarks a D=2048 — eso desborda la pila para cualquier dim>1024.
Mi código nuevo no usa ese patrón (asigno dinámico, del tamaño de la
población, no de `dim`), así que no lo heredé, pero el bug original seguía
ahí en el archivo que reemplacé — si corrieron D=2048 con `use_cog=1`
alguna vez, vale la pena revisar si eso ya causó algo raro.
