# Fase 4/5/6 experiment recipes (exp_SGM_0021 / 0022 / 0023)

Condensed, copy-with-modification recipes for the later SGM phases. Each is a TEST-FIRST
synthetic experiment; parameters are the values that passed on the device (seed 42).

## 0021 — Trauma nodal + aislamiento (hipótesis Luciano: singularidad nodal)
Mechanism: an overloaded node (high `activation`) becomes an attraction sink ("singularidad
nodal"). Fix = ISOLATE (cut edges, PRESERVE ω) then REINTEGRATE SLOWLY (weak→strong activation).

Traps that bit us:
- GLOBAL attraction score over all N nodes is insensitive: denominator ~ sum over N terms, one
  node can never dominate → score saturates. Measure LOCAL attraction over the node's K nearest
  neighbours instead.
- If the trauma node sits at the geometric CENTER of a diffuse cloud, all pairwise distances are
  ~equal → activation doesn't decide → score ~1.0 regardless. FIX = STAR geometry.

STAR geometry (the key fix):
```
r = 0.3
trauma.omega = [0]*D
for i in range(K):                 # K=8 neighbours
    vec = [0]*D; vec[i] = r        # each neighbour offset on a distinct dim
    nodes[i].omega = vec
# dist(trauma, neighbour_i) = r ; dist(neighbour_i, neighbour_j) = sqrt(2)*r > r
# => trauma is the NEAREST of every neighbour; activation decides dominance.
```
Attraction-local score: for each of the K neighbours s, P(trauma|s) =
  exp(-ALPHA*dist(s,trauma))*(1+act_trauma) / sum_b exp(-ALPHA*dist(s,b))*(1+act_b)
average over the K neighbours. THETA_SING = 0.30.
Results (deterministic, seed 42): act=5.0 → 0.515 (singularidad formada); act=0.1 → 0.163
(reachable, no re-collapse = reintegración lenta OK); re-act=5.0 → 0.515 (re-colapsa, proving
slow rehab is necessary); isolation → score 0.0 with ω preserved.
Note: spec §4.3 only lowers V via κ_trauma=0.50, but V does NOT enter Eq.2 affinity — so lowering
V alone never removes the node from the walk. Isolation (cut edges) is the actual mechanism.

## 0022 — Decoder L2, bigrama (camino A del roadmap Fase 5)
Roadmap says: NO linear projection W·ω→logits (v0.25 v12 top1=0.020), NO similarity-NN. Use
explicit bigram transition (v0.25 reported top1=0.630) or transformer. Use BIGRAM.

Trap: if the hidden "truth" bigram matrix is near-uniform (weights ~1 each + 2 dominant at +5/+3),
the sampled corpus is too noisy → top1 on holdout ~0.31 (<0.5) even though the decoder is correct.
The TEST is wrong, not the mechanism. FIX = make truth DETERMINISTIC (one strong successor +10 over
~0.1 noise): top1 jumps to ~0.927.

```
def true_bigram(rng, V):
    M={}
    for a in range(V):
        w=[rng.random()*0.1 for _ in range(V)]
        w[rng.randrange(V)] += 10.0          # ONE strong successor
        s=sum(w); M[a]=[x/s for x in w]
    return M
train: count token->token over corpus (N_SENT=400, L=8) -> model[a][b]=count/total
predict: greedy argmax_b model[prev][b]
seed: routed_omega -> nearest token node via Eq.2 (affinity) -> generation starts there
T-DEC-01: top1_holdout > 0.5 ; T-DEC-02: mean transition prob under TRUTH > 0.20 (coherence)
```
Corpus is SYNTHETIC (no Don Quijote in vault) — it proves the decoder LEARNS transitions, not that
it "understands Spanish". Honest scope.

## 0023 — sgm_tick_unificado (Fase 6, glue)
Integration experiment = WIRING, not new physics. Reuse EXACT params from 0019-0022 and orchestrate
§5.3 order:
```
update context window (W(t)=W_base/(1+κ_W·pain)) + E_root/emergencia (0019)
omega_routed = SensorBridge.project(signal)            # HDC, 0019
seed_node = argmin_n dist(omega_routed, nodes[n].omega)
walk: affinity_move with prev-exclusion + duda/contradicción (0014/15/17)
      if nodes[cur].activation > 3.0: mark trauma, skip (isolation, 0021)
tokens = decode(bigram, seed_by_affinity, L)            # 0022
```
Prove T-INF-06 (loop closes, non-empty response, no crash) and T-INF-07 (decoded response coherent
under learned bigram, prob>0.20) across ALL three modes (RAZONAMIENTO/PLAN/SENSORIAL) without
explosion. Passed FIRST try because it only orchestrates already-proven pieces — the lesson: an
integration test must add NO new unvalidated physics, only wiring.
