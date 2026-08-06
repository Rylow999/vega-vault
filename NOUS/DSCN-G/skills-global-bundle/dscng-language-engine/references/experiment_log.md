# DSCN-G Language Engine — Measured Experiment Log

Live state also in vault: `NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/README.md`
Corpus: Don Quijote (Project Gutenberg, public domain) for v0.6+.

## Result table (2026-07-25)
| Exp | Question | Result | Verdict |
|-----|----------|--------|---------|
| v0.1 | Does graph collapse? | N* saturates ~4.5 (sublinear) | PASS — working memory, not mass |
| v0.2 | Collapse parametric? | N* grows w/ K/θ (3.8→166) but sublinear | PASS — parametric, not structural |
| v0.3 retrieval | Graph understands? | recover 100% (norm)/91% (bits) @256 | PASS — understands |
| v0.3 REAL v2 | Hibernation preserves mass? | retention 100% (N_total=N_init, ws~4.5) | PASS — VALIDATES DB semántica |
| v0.4 | β contextual (Pandora) | β_eff N*=5.2 vs β_fixed N*=5.0 (noise) | FAIL — doesn't fire (ρ≈0) |
| v0.5 | L2 decoder retrieve | "gato"→"gato" OK | PASS |
| v0.5b | L2 breaks loop | "el casa el casa"→"el roja la corre..." (0 adj rep) | PASS — loop broken |
| v0.6a | next-token (real corpus) | acc 0.45%→10.11% | PASS — LEARNS |
| v0.6b | dolor post-hoc (RL) | improvement 0.0 | FAIL — punishment too late |
| v0.6b-bis | dolor Q-learning on edge | improvement -0.0012 (noise) | FAIL — redundant on supervised |
| v0.7 | context average | 5.89% (worse than 10.11%) | FAIL — overwrites nodes |
| v0.7-bis | separate context state | 0.49% | FAIL — contaminates omega |
| v0.7-final | clean trigram (table) | 3.85% | FAIL — sparse, no scale |
| v0.8 | rustic attention | 8.64% (worse than 10.11%) | FAIL — no beat bigrama (small vocab) |
| v0.9a | dolor = evasion signal + AUDIT | 0.0149→0.0149 (measured wrong: on corpus not generation) | FAIL — design, not concept |
| v0.9b | labels that MUTATE by use | 92.67% acc vs corpus truth | PASS — label emerges from dynamics |
| v0.9a-bis v1 | dolor on top-k generation | 0.0→0.0 | FAIL — design (never repeated, nowhere to act) |
| v0.9a-bis v2 | dolor ONLINE on v0.5b generator (repeats) | correct design (evasion + re-pick 2nd) | DONE — proper pain test (but see v0.9c) |
| v0.9c | subsistence global (internal pain) | G 0.0 (no learn) → 1.0 (learn) | PASS — CLOSES pain arc (internal pain) |
| v0.11 | abstraction (gamma per concept) | D=16, abstract γ=0.3 / concrete γ=0.1 | see spread+acc in references |
| v0.12 | attention, synthetic ambiguity | W1=0.0967 vs W2=0.0558 | FAIL — context can't disambiguate (limit) |
| v0.10 | persistence hybrid score (SynapticCache 2.1+2.4) | N_active=N_total (no collapse) | ~ LIVE-by-relevance, not asleep |

## Lessons that recurred
- "Failed" experiments (v0.6b, v0.7*, v0.9a) mapped real limits; report as data.
- v0.3 REAL v1 was a bad design (didn't reproduce collapse) — re-derived from
  run_v01.py (the real collapse dynamic) before adding hibernation. Lesson: a
  long run with no JSON often means the script didn't reproduce the effect.
- Dolor/RL only helps where there's NO correct answer given (qualitative
  feedback), not on supervised next-token. Pain needs ACTIVE generation, not a
  static corpus (v0.9a measured on corpus → saw nothing).
- Context helps only with large/ambiguous vocab + attention (not tabla rígida).
- **A 0.0 / flat result means the TEST was wrong, not the concept.** v0.9a
  (corpus), v0.9a-bis-v1 (top-k never repeats), v0.12-v1 (predicted "banco"
  which always follows context) all returned zero because the measurement had
  nothing to act on. Rule: inspect the test before re-launching. v0.12-v2 fixed it
  by predicting the word AFTER "banco" (the real disambiguation target).
- **Context/disambiguation needs LEARNED attention, not averaged ω or a table.**
  v0.7/0.7-final/0.8 and v0.12 all failed to beat bigrama: cosine + averaged ω
  can't split an ambiguous node into its senses. HONEST LIMIT of the rústico graph.

## SynapticCache patterns integrated (from Luciano's own summary doc)
- 2.1 hybrid evict score → v0.10 desalojo criterion
- 2.2 omega_root (centroid by V) → v0.10
- 2.3 distance-based threshold → pending
- 2.4 LRU fallback if daemon dies → v0.10
- 2.5 AUDIT mode (observe before act) → v0.9a
