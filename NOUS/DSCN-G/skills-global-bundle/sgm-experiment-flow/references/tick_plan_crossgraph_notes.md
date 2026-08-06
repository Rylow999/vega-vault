# exp_SGM_0030 — tick_plan_crossgraph (B: mecanismo como HERRAMIENTA)

## Cuándo usar este patrón
Cuando Luciano pasa de "medir la mecánica" a "verdaderas pruebas" (usar el mecanismo para
resolver algo). Es un tipo de test DISTINTO a 0027/0027b/0027c/0029: ya no se mide el operador,
sino si el sistema RESUELVE un problema que el tick plano no puede.

## Diseño que pasó (variable discriminante = éxito del plan multi-paso)
- G1 = "mapa": cadena `0->1->...->(n_g1-1)` [meta en n_g1-1].
- G2 = "inventario": `llave -> puerta -> caja`.
- RELACIÓN CRUZADA empaquetada ADENTRO del nodo llave:
  `edges[llave].append((n_g1-1, 0))`  # "la llave destraba la meta de G1"
  (rol = índice del nodo meta; viene de build_relational_memory en hrr_core).
- G1 y G2 ESTÁN DESCONECTADOS salvo por esa arista cruzada. Sin ella, el tick plano no llega a
  la meta (G1 y G2 sueltos).

## Tests
- T-CROSS-01: `tick.plan_from(llave, [meta])` AND `tick.plan_from(0, list(range(1,meta+1)))` -> exito > 0.8.
  Resultado: 1.0.
- T-CROSS-02: tick PLANO (`use_roles=False` -> plan_from devuelve False siempre) -> exito < 0.3.
  Resultado: 0.0.
- T-CROSS-NC: roles al azar entre G1/G2. Truco: sobreescribir `tick.rel_mem[llave]` para que apunte
  a un nodo random distinto de meta (`fake_tgt`), luego `plan_from(llave,[meta])` debe FALLAR (<0.3).
  Resultado: 0.15. (Si con ruido igual llegara, el test no mediria nada.)

## Codigo (usa modulos consolidados, NO copy-paste)
```python
import hrr_core as H
import tick_relational_core as T
tick = T.TickRelational(omega, edges, D, seed=SEED)
ok = tick.plan_from(llave, [meta])   # desanida cadena por rol = indice de nodo
```
- `hrr_core.py`: bind/unbind/cleanup/build_relational_memory/recover_target/recover_chain.
  Rol SIEMPRE `role_vecs[indice_nodo]`.
- `tick_relational_core.py`: clase TickRelational con `route()` (PPR sesgada por rol, HDC previa)
  y `plan_from()` (recover_chain sobre rel_mem).

## Resultado
HRR+roles 1.0 / plano 0.0 / NC 0.15 -> PASS. Primera vez que el anidamiento (0027c/28) deja de ser
experimento y pasa a HERRAMIENTA del sistema (resuelve planes cruzando grafos).

## Smoke-test del modulo (correr antes de escribir el exp)
```python
# cadena y anidamiento deben dar True; plano False; NC cos a random ~0.1
print(H.recover_chain(rel, 0, [1,2], role, omega, D))            # True
print(H.recover_chain(rel, 20, [21,22,23], role, omega, D))      # True
```
