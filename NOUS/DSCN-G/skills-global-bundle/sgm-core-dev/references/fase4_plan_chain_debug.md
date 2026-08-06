# Fase 4 — Plan chain test traps (exp_SGM_0020, learned 2026-08-02)

## Symptom
`run_plan` returns INCONCLUSA with `len(visited)` hitting the horizon (~59 for rho=0.05)
instead of DETERMINADO at the terminal. T-PLAN-01 fails even though the graph "has" a plan chain.

## Root cause 1 — affinity-only graph wanders
A graph where every node is connected to every other by Eq.2 affinity has no directed path.
The walk drifts and cuts at `ticks >= H_plan + 5` without arriving. Build a STRUCTURED chain:
nodes 0..L-1 placed close in omega sequence, terminal = last of the chain, query = first.

## Root cause 2 — rotational steps create equidistant loops
With `step = [0.3 if j==(k % D) else 0.0 ...]` the chain nodes sit at equal pairwise distance
(0.3) in rotating dims, so non-consecutive nodes (2,3,4) form a triangle. All carry equal boost
-> the walk oscillates forever: `0->1->2->3->2->3...` then `2->3->4->2->3->4...`.

### FIX (apply BOTH)
1. Gradient in ONE dimension: `step = [0.3 if j==0 else 0.0 for j in range(D)]`.
   Then `dist(k,m) = |k-m|*0.3` — a true gradient, next node always wins.
2. Working memory: in `affinity_move`, exclude the immediately-previous node
   (`if b == cur or b == prev: continue`). Pass `prev` through `run_plan`
   (`prev = cur` BEFORE moving).

## Debug recipe (catch oscillation early)
Copy `build_graph` + `precompute` + `affinity_move` (with `prev`) into a tiny script and print
the first ~15 visited nodes:
```python
cur=0; prev=None; visited=[0]
for t in range(15):
    nxt=affinity_move(cur,nodes,M,"PLAN",prev)
    visited.append(nxt); prev=cur; cur=nxt
    if cur==terminal: print("LLEGO en",t+1); break
print("traza:",visited)
```
If you see a repeating subsequence (2,3 / 2,3,4), the chain is not a gradient — fix step dim.

## Related
- Spec SGM v1.4 §4 (MODO_PLAN boost Temporal/Functional=2.0, kappa_trauma=0.50, H_base=50, H_plan=H_base*(1+rho)).
- Roadmap Fase 4 tests T-PLAN-01 (reach terminal, Q>0.5), T-PLAN-03 (rho low vs high -> horizon length).
- Trazabilidad: in a bifurcation at equal distance, PLAN must pick Temporal/Functional node and
  RAZONAMIENTO the Causal node (reuse the 0016 competition pattern).
