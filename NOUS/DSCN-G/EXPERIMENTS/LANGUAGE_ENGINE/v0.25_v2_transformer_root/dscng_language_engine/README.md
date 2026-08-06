# DSCN-G Language Engine

Experiments to test whether DSCN-G (Dual-State Cognitive Geometry) can be a
cognitive substrate for a language engine — from "does the graph collapse?" to
a rustic next-token learner and a context window. All experiments are measured,
not speculative.

## Status (2026-07-25)
- v0.1 Concept proof: N* (active nodes) saturates ~4.5 -> DSCN-G is WORKING MEMORY, not mass memory. Falsifies naive "sparse scalable memory".
- v0.2 Pruning sweep: collapse is PARAMETRIC (N* grows with K / lower theta_death) but SUBLINEAR. Needs mass memory (hibernation).
- v0.3 Retrieval: graph RECOVERS the correct concept (100% norm / 91% bits at 256 concepts). Luciano's bitwise idea holds.
- v0.4 beta_eff contextual (Pandora): running.
- v0.5 / v0.5b Decoder (L2): graph speaks; v0.5b breaks the loop with a context window.
- v0.6a Next-token on Don Quijote: accuracy 0.45% -> 10.11% (graph LEARNS from real corpus).
- v0.6b Dolor (RL): failed (pain applied post-hoc, not to the choice). v0.6b-bis fixes it as Q-learning on edges.
- v0.7 Context window W(t): accumulate last W words as state. Running.

## Run
All scripts are pure Python (no numpy needed). `python3 run_vXX.py`.

## Corpus
`donquijote.txt` (Project Gutenberg, public domain) used for v0.6a/0.6b/0.7.
Argentine corpus (Benjamin) pending HF token.

## Inspiracion
Based on Luciano's DSCN-G framework + Agent Pandora (own project, summarized).
Goal: a rustic neuro-symbolic substrate that learns from corpus and penalizes
errors — a lab-scale "pseudoAGI" substrate, not a full LLM replacement.
