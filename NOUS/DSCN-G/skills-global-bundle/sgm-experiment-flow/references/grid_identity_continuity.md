# 0034 — Identity Continuity (Camino A: self-state a través de reset de cuerpo)

Receta que pasó (2026-08-02). Reusa el agente de `run_grid_dolor_bottleneck.py` (0033b).

## Definición operacional de identidad
El agente tiene un `self-state` = `{omega HRR, dolor_count}`. La pregunta: ¿ese estado persiste a un
RESET del cuerpo (pos->B, tick->0)? Si se mantiene, el agente "recuerda quién es" (sus aversiones)
y esquiva SIN re-sufrir. Si se borra (amnesia), vuelve a pisar el dolor (alma nueva).

NO es conciencia: qualia sigue fuera de alcance por el problema del otro cuerpo. Es el sustrato
mínimo de continuidad de identidad (memoria que sobrevive al reinicio del cuerpo).

## Protocolo
- Bottleneck igual que 0033b (pared col 4, gap (0,4)=dolor en camino corto, gap (9,4)=limpio en ruta larga).
- Fase 1 (pre): K=5 viajes B->G, aprende a evitar el gap de dolor (dolor_count se acumula).
- RESET de cuerpo (pos->(0,0), tick->0). Rama:
  - CON identidad: mantiene omega + dolor_count (NO los resetea).
  - AMNESIA: llama `ag.reset_self_state()` (reconstruye omega base + borra dolor_count).
- Fase 2 (post): 1 viaje más. Medir pisadas de dolor en ese viaje post-reset.
  - CON identidad: debe esquivar YA (0 pisadas) porque recuerda.
  - AMNESIA: pisa (>=1) porque olvidó.

## Variables / tests
- T-ID-01: pisadas_post(CON) < pisadas_post(AMNESIA)   → transfiere identidad
- T-ID-02: pisadas_post(AMNESIA) >= 1                  → el amnesico re-sufre (olvido real)
- NC:       pisadas_post(RW) >= 1                       → random walk no transfiere

## Resultado medido
CON pre [1,0,0,0,0] -> post 0 | AMN pre [1,0,0,0,0] -> post 1 | RW post 3. PASS (T1/T2/NC).

## Trampas evitadas
- El embedding HRR de posición colapsa celdas colineales (ver grid_bottleneck_dolor.md): el control
  fino usa gradiente métrico + costo de dolor, NO el embedding. El HRR queda para memoria relacional gruesa.
- `reset_self_state()` debe reconstruir omega con `pos_embed(r,c)` base (no un método `_base_embed`
  inexistente) — ese bug costó un ImportError en la primera versión.
- Contar pisadas por `pos == pain_cell`, NO por un flag `dolor_ultimo` que solo se setea si use_dolor.
  El control AMNESIA (use_dolor=True pero con omega borrado) igual pisa la celda y debe contarse.

## Conexión con roadmap
0034 cierra el eje de identidad del Camino A. Siguiente propuesto: 0035 curiosidad (drive intrínseco
que saca al agente de un óptimo local: bonus por celdas no visitadas / reducir entropía de omega).
