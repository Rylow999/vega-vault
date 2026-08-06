# Offline polysemy signal check + online seeded graph (v0.25 v7 pattern)

Use when the user asks to validate whether real sense ambiguity exists in a corpus
_before_ running an online mechanism, or when proposing a "seed the graph from
data" step for polisemia.

## Protocol
1. Pick ONE candidate ambiguous word from real text.
2. Extract real contexts: window W around each occurrence, bag-of-words normalized.
3. Run pure offline k-means k=2 vs k=1.
   - Metrics: inertia, silhouette (cosine), majority-cluster fraction.
   - If k=2 does not clearly beat k=1 → stop; no local sense signal in this corpus
     for this word. Do not spin up online mechanisms.
4. If k=2 wins → project the two centroids to the online D and use them as omega0
   for the two sub-nodes of that word (instead of `gauss(0,1)`).
5. Run the online graph (anchor/repulsion/competition) and track cos(A,B) over
   epochs. Divergence from the seeded hypothesis = mechanism can track real signal.
6. Compare against a random-init baseline in the same conditions.

## Key finding (Don Quijote, 2026-07-28)
- Word: `banco`, 5 occurrences, W=10 window, bow normalized.
- k=1 inertia=1.307, silhouette=0.000.
- k=2 inertia=0.559, silhouette=0.552, improvement=57%.
- Seeded online graph: cos(A,B) went from 0.640 (init) to -0.375 after 20 epochs
  (clear divergence). Random init did not show this separation.

## Rule
Never start an online polisemy mechanism from random omega0 when the corpus
already contains a hypothesis you can extract. Use the data's own structure as
the prior; let the online dynamics refine, not discover from zero.
