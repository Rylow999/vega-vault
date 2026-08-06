# Relational composition — Hebb 3-body (v0.23, Gap 2)

The fractal graph (v0.21 v8) encodes CO-OCCURRENCE ("banco aparece con dinero"),
NOT structured relation ("banco TIENE dinero" / "banco ESTÁ_EN río"). For a
pseudoAGI substrate we need knowledge, not just association. This recipe learns
TRIPLES (subject, RELATION, object) with NO backprop.

## Design
- Embeddings `emb[w]` (D-dim) for every word, anchor `o0` (copy) like v0.21 v8.
- Per-relation matrix `R[r]` (D×D) for each relation label r (e.g. TIENE, LUGAR).
- Corpus carries explicit relation tags on the (S, R, O) triple, e.g. the token
  sequence `el banco TIENE dinero` marks `rel[i]="TIENE"` on the object position
  and `rel[i-2]="el"/"X"` on the subject. (In real text the relation is latent —
  see "Scaling" below; v0.23 uses a controlled corpus so the signal is clean.)
- Training (per occurrence of `S R O`):
    ps = emb[S]; po = emb[O]
    psr = R[r] · ps
    R[r] += lr · normalize(psr) ⊗ normalize(po)      # Hebb outer-product
    emb[S] pulls toward po; emb[O] pulls toward ps    # basic association
  (normalize = x / (norm(x) or 1e-9) — protect the norm, see PITFALL #25.)

## Prediction
Given a pair (S, O), score each relation by `cos(R[r]·emb[S], emb[O])`; the argmax
is the predicted relation. Baseline chance = 1 / (#relations) (0.5 for 2).

## v0.23 v1 result + THE CONTAMINATION BUG (2026-07-28)
- **v0.23 v1 result: 4/12 = 0.333 (WORSE than chance 0.5).** Honest failure, not a
  measurement artifact. The 4 "correct" were noise.
- **ROOT CAUSE = BASIC-ASSOCIATION CONTAMINATION.** The v0.23 v1 training step did
  TWO things: (a) reinforce `R[r]` via Hebb outer-product (correct), AND (b) pull
  `emb[S]` toward `emb[O]` directly (basic co-occurrence). Because BOTH `banco-dinero`
  AND `banco-río` occur in the corpus, (b) makes `emb[banco]` sit between `emb[dinero]`
  and `emb[río]` — so `R[TIENE]·emb[banco]` and `R[LUGAR]·emb[banco]` both end up near
  BOTH objects, and the relation matrices cannot specialize. Scores land ~0 or
  NEGATIVE (noise). RULE: to learn RELATIONS, do NOT also pull the base embeddings of
  subject/object together — that is plain co-occurrence and it drowns the relation
  signal. Let ONLY `R[r]` encode the relation; keep `emb` for identity only.
- **v0.23 v2 (the fix, launched 2026-07-28, result PENDING):** remove step (b)
  entirely (only `R[r] += lr·normalize(R[r]·emb[S])⊗normalize(emb[O])`); richer corpus
  (8 subjects × 4 relations TIENE/LUGAR/CAUSA/PARTE_DE, low-overlap objects, ~64 pairs);
  20 epochs; test BOTH D=16 and D=32 (larger D = more room for relation subspaces).
  Baseline chance drops to 0.25 (4 relations) — stricter. Hypothesis: without the
  contaminant, `R[r]` specializes and acc beats 0.25. If D=32 still fails, relational
  composition is a HARD GAP needing a tensor / dedicated relational embedding, not
  Hebb 3-body on flat `emb`.

## Honest test (don't leak)
- Controlled corpus: each subject paired with relation-specific objects
  (banco→{dinero,cuenta,oro} under TIENE; banco→{río,plaza,ciudad} under LUGAR).
  Same pattern as the v0.21 contrastive corpus (strong, asymmetric signal).
- Report acc vs 0.5; also dump the per-pair prediction table (did "banco-dinero"
  predict TIENE? "banco-río" predict LUGAR?).
- Do NOT claim success if acc≈0.5 — that means R[r] didn't specialize.

## Why this is the right next gap
v0.22 closed the root director (routing perfect with projection, but word-sense
doubt is trivially resolvable by the graph — see root_director.md). The real
cognitive leap is STRUCTURED knowledge: "what relates to what", transitive
inference, contradiction detection. Hebb 3-body is the DSCN-G-native way (no
backprop, no GPU) to grow that layer on top of the fractal substrate.

## Scaling to real text (future)
- Latent relations: cluster co-occurrence patterns into relation-types, or use the
  transformer context (v0.14d) to propose candidate relations, then bind R[r] by
  co-occurrence of (S-context, O-context). Not yet implemented.
- Compose: chain R[r1]·R[r2] for transitive queries ("A TIENE B, B PARTE_DE C →
  A TIENE_TRANSITIVO C"). This is the reasoning layer (Gap 2 → Gap 3).
