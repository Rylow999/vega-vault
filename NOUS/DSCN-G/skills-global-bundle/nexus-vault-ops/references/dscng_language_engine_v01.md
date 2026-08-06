# DSCN-G Language Engine — v0.1 Concept Proof (2026-07-25)

## Why this experiment exists
User proposed (after a GPT discussion) replacing/hybridising the Transformer
paradigm with a DSCN-G cognitive substrate: semantic nodes ω/φ/V + dynamic
memory with homeostatic pruning. The load-bearing claim: "the system converges
to few active nodes via homeostasis → sparse-memory architecture scalable as
O(active nodes), vs O(n²) Transformer attention."

## Falsification question
Does N* (active nodes at steady state) grow with N_init, or saturate in a small
fixed point independent of N_init? If it saturates, "scalable sparse memory" is
FALSE with the current pruning dynamics and the architecture cannot hold a
language-scale vocabulary.

## Design (faithful, minimal)
- Replicate ONLY the mechanisms that govern N*:
  - Eq.2 chain affinity: P(m|n) ∝ exp(-α·‖ω_m−ω_n‖)
  - Eq.5 vitality + prune: V ← V·e^{-γ} + A·(1−e^{-γ}); prune if V < θ_death
  - Eq.1 ω broadcast toward ω_ideal (gating by interference)
- Kuramoto coupling OMITTED: it only recomputes φ, not V or chain visits, so it
  does not affect the pruning fixed point. Document this honestly.
- Params copied from CORE/IMPLEMENTATION/CODE/verify_dscng_v3.py defaults:
  α=5.0, β=0.20, γ=0.01, θ_death=0.10, d=8, K=3 chains.
- Pure stdlib Python (no numpy on this device). run_v01.py lives in
  NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/v0.1_concept_proof/.

## Result (real run, 2026-07-25)
N_init | N* mean | N* std
4      | 4.00    | 0.00
50     | 4.40    | 0.49
200    | 4.40    | 0.49
1000   | 4.33    | (3 seeds × 600 steps)
Universal bound N* ≤ 1/θ_death = 10 respected; fixed-point condition
ρ ≥ N*·θ_death² ✓.

## Conclusion
N* SATURATES at ~4.3–4.4 nodes for N_init from 4 to 1000. Falsifies the
"scalable sparse memory" scaling claim: the homeostat collapses any vocabulary
to ~4 live nodes — that is amnesia, not efficiency.

## Paths to make DSCN-G a real language engine (v0.2 candidates)
1. Predictive-coding survival: a node survives iff it carries unique prediction,
   not merely if visited by a chain (this is the local/Hebbian learning GPT proposed).
2. Raise K (more chains) + lower θ_death → more "light" traversing the graph keeps
   more nodes alive.
3. Separate MASS memory (all concepts, latent V) from WORKING set (active sub-graph
   ~N*). N*≈4–5 becomes the working memory, not the vocabulary — consistent with
   the v4 Ring-0/1/2/3 design (DSCN-G = cognitive layer, LLM = I/O adapter).

## Criterion to carry forward
Any "DSCN-G as LLM" claim must first answer: at what N_init does N* stop
growing? If it never grows, the pruning dynamics must change before the claim
is meaningful. The v0.1 run_v01.py is reusable: extend N_inits / adjust K,
θ_death, γ to test the v0.2 redesigns above.
