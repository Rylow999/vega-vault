# sgm_core.py — Template de módulo único consolidado (exp_SGM_0053, 2026-08-04)

Cuando Luciano pide pasar de ~60 experimentos sueltos a un test real (Crafter), consolidar SOLO los
mecanismos GANADORES en UN módulo stdlib puro portable. Forma validada en `sgm_core.py` (raíz SGM):

## Capas / API pública
- `HDC(rng, D)` -> `.project(signal)` : SensorBridge (0019), estado semantico -> omega. NO pixeles.
- `HRR(D, rng, n_roles)` -> `.bind/.unbind/.cos/.cleanup/.role(i)/.relational_memory/.recover` :
  composicion relacional con rol POR INDICE DE NODO (0027c / hrr_core). Bind = conv circular (i-k).
- `ppr_route(adj, seed, aff_fn, alpha=0.15, iters=100)` -> dict nodo->prob : ruteo multi-hop (0004).
- `BigramDecoder(counts)` -> `.top1/.top5` : decoder validado en corpus real (0026).
- `SGMAgent(...)` -> `.step(state_semantic, valid_actions)` + `.reward(r, pain)` : loop percepcion->tick->accion.
- `build_nested_K3(hrr, parent_vec, child_fact, role_parent, role_child)` : anidado profundo slots separados (0059g).

Smoke test obligatorio: `python sgm_core.py` debe imprimir "sgm_core SMOKETEST OK" y el `HRR.recover`
debe dar 1.0 (composicion real). Todo stdlib puro (sin numpy).

## Que ENTRA (ganadores validados)
- HRR rol-por-nivel (0027c) — composicion.
- PPR (0004) — ruteo.
- Decoder bigrama corpus real (0026) — top1 >> azar.
- Slots separados K=3 (0059g) — anidado profundo (prof 12+).

## Que queda AFUERA EXPLICITAMENTE (y por que)
- NodeCore en Python (0002): no aporto rendimiento -> usamos `omega` como lista de floats.
- Fase dinamica para XOR: fallo documentado -> no se reimplementa.
- 0056 con regla inyectada: TRAMPA (gramatica hardcodeada) -> excluida por honestidad.
- Resonator puro (0059f): techo confirmado, no rompe -> usamos slots K=3 (0059g).

## Reglas de diseno dictadas (Luciano, 2026-08-04)
1. Un modulo, no scripts sueltos.
2. SensorBridge con estado semantico (inventario/logros/salud), NO pixeles crudos.
3. Loop SOLO primero (percepcion->tick->accion con un agente, logros simples) ANTES de sumar
   multi-agente + capa de lenguaje (0055/0056). Si se meten ambas capas juntas y falla, no se
   sabe cual rompio.
4. Documentar la lista "afuera" en un doc de consolidacion (ej `docs/SGM_CORE_CONSOLIDACION.md`).

## Que NO incluye este modulo (a proposito)
- Multi-agente y capa de lenguaje (0055/0056): se suman DESPUES de cerrar el loop solo.
- Cualquier mecanismo no validado: integracion = wiring, no fisica nueva (leccion de 0023).
