# Backprop diagnostic probe (v0.14b/v0.14c lessons)

When a hand-rolled pure-Python transformer lowers loss but scores ~0 accuracy,
you must distinguish a BROKEN GRADIENT from a CONVERGENCE/HEAD bug before writing
another variant. This probe settled it in one short run (no need to scale D).

## The probe (run on a small corpus slice, ~5k tokens)
1. Print `mean pairwise distance` between omega_base vectors (sample 200 pairs).
   - If ~0.0 -> embeddings COLLAPSED (graph flattened them); transformer input
     has no signal. (Did NOT happen here: 0.715.)
   - If >0.5 -> embeddings have identity; bug is downstream of the input.
2. Print cross-entropy loss BEFORE and AFTER N training steps (e.g. step 10 vs
   step 3010).
   - If loss falls smoothly toward `ln(V)` (here ln(150)~5.01) -> gradient is
     CORRECT, model is converging to the UNIFORM floor. That means: convergence /
     output-head bug, NOT a broken backward pass.
   - If loss stays flat or rises -> sign/shape error in the backward pass; rewrite it.

## What this proved (2026-07-25)
- Embedding dispersion 0.715 -> graph input was fine.
- Loss 5.575 -> 5.01 (= ln150) -> backprop gradient was correct; model stalled at
  the uniform floor. So acc=0.001 was a CONVERGENCE bug, not a broken gradient.
- Raising D (8->16, v0.14c) did NOT move acc (0.0012->0.0013) -> not a capacity issue.

## The actual fix (for the NEXT variant, v0.14d+)
- Learn a SEPARATE output projection `Wo*h -> logits`; do NOT reuse omega_base as
  the classifier weights (it couples embedding and head and is "dirty").
- Drop lr from 0.05 to ~0.005 (large lr bounces around the floor).
- Loop the corpus 2-3 epochs (single pass over 20-30k tokens is too few).
- Keep the causal self-attention + softmax + cross-entropy backward pass as-is
  (it is correct -- only the head/schedule need changing).

## Pure-Python backprop building blocks (no numpy)
- `dot(a,b)`, `mat_vec(M,v)`, `vec_add(a,b,a2=1.0)`, `scale(v,s)`,
  `softmax_logits(logits)`.
- Causal attention: for each t, scores=dot(Q[t],K[s])/sqrt(D) for s in 0..t;
  att=softmax(scores); h[t]=sum_s att[s]*V[s].
- Loss: cross-entropy over `logits = [dot(h_last, omega[j]) for j]`.
- Backward: d_logits = probs; d_logits[target]-=1; d_hlast = sum_j d_logits[j]*omega[j];
  propagate att->scores (softmax jacobian: a[s]*(d_att[s]-sum a[k]*d_att[k]));
  scores->Q/K via /sqrt(D); Q/K->Wq/Wk/Wv via outer product with ctx. SGD update.
