---
name: dscn-g-language-engine
description: Iterative minimal-cognition NLP experiments on DSCN-G (pure Python, no numpy/PyTorch). Covers sense disambiguation, skip-gram, k-means, bigram transition models, competitive memory, pain/error signals, closed-loop integration, corpus selection, and GitHub push workflow.
---

# DSCN-G Language Engine — experimental minimal cognition

Class-level skill for running iterative NLP experiments on the DSCN-G minimal-language-engine codebase (Python, no numpy/PyTorch). Captures durable workflow rules, failure modes, and user preferences from live sessions.

## When to use this skill

Any task involving:
- running or extending DSCN-G experiments (v0.21–v0.25)
- sense disambiguation / polysemy detection on small corpora
- closed-loop integration of memory, attention, pain/error, and generation
- skip-gram / k-means / bigram / linear classifier experiments in pure Python
- corpus selection (Don Quijote, synthetic labeled, restricted-context subcorpora)
- push workflow to `engine_export` + GitHub incremental API

## Core workflow rules

1. **Offline before online.** Always run k-means on real word contexts first. If k=2 does not beat k=1 on silhouette/inertia, stop — no local signal means no online mechanism can detect it.

2. **Strong-supervised baseline first.** Measure a strong supervised baseline before declaring any loop/integration successful. Weak baselines are not proof of harm; strong baselines are proof of failure to integrate.

3. **Synthetic labeled corpus is a valid fallback.** When real corpora (Wikipedia/Tatoeba) are unavailable, a realistic synthetic labeled corpus with explicit sense labels is acceptable. Control monosemity when possible.

4. **Failure framing.** Must state the structural reason for failure before discarding (e.g., “loop destroys signal because omega update dominates context noise”, not just “doesn't work”).

5. **Explanation frame for non-technical audiences.** When asked to explain the system to a psychologist or outsider, use this frame: minimal artificial brain with memory (long-term + working), pain/error signal that redirects learning, attention/focus competition, context/prediction substrate, and generation. Current strengths: selective forgetting, error-driven learning, sense disambiguation in controlled corpora, coherent generation with stable context. Current gap: robust closed-loop operation over long dialogues and real-complex corpora.

6. **Literature awareness.** User asks whether component methods exist in literature. Core answer: most cognitive/neural mechanisms exist separately (word2vec, WSD, conditional NLG, relational composition, meta-learning). The likely novel contribution is a specific combination: closed-loop integration of natural pain/error signals, competitive memory, sense-aware routing, conditional generation, and relational composition into one minimal system.

7. **Continuance rule.** After documenting results, continue the next concrete step unless blocked. Do not ping the user after every finished step; only stop when blocked or when asked.

5. **User's explanation frame.** For non-technical audiences (e.g., psychologists), use this frame: minimal artificial brain with memory (long-term + working), pain/error signal that redirects learning, attention/focus competition, context/prediction substrate, and generation. Current strengths: selective forgetting, error-driven learning, sense disambiguation in controlled corpora, coherent generation with stable context. Current gap: robust closed-loop operation over long dialogues and real-complex corpora.

## Android vault access

`/sdcard/Hermes/nexus-vault/` and similar paths require `su -c "..."` to list/read files; normal access often returns empty/length 0. Always verify with root when vault listings fail.

## Logging and batch validation

On this Android Hermes host, `/tmp` redirection is unreliable. Write batch validation logs into the home workspace and inspect from there. Use background batches only when necessary; prefer sequential runs if the user wants result-by-result control.

## SGM vault location (added 2026-08-01, updated 2026-08-02)

When the user asks about SGM (Synaptic Graph Model) content in the vault, look in
`rizoma_docs/` — NOT in `engine_export/` (which is DSCN-G v0.1→v0.25) and NOT in
the home directory root.

### Organized structure (as of 2026-08-02)

```
rizoma_docs/
├── README_SGM.md              ← navigation index
├── docs/                      ← all technical documentation
├── experiments/               ← all experiment scripts (pure Python stdlib)
├── results/                   ← all experiment result JSONs + experiment_registry.json
├── phases/                    ← results organized by phase (phase0_substrato, phase2_inferencia)
└── lit/papers/                ← PDF literature (KoPE, HippoRAG, Kanerva SDM, etc.)
```

### Key files by category

**Specs & docs** (in `docs/`):
- `SGM_v1_4_Especificacion_Corregida.md` — full spec
- `SGM_ROADMAP.md` — 6-phase roadmap
- `SGM_README.md` — master index with validation status
- `Arquitectura_Pure_L2_Pandora.md` — unified SGM+NOUS+DSCN-BIO architecture
- `RIZOMA_Vision_Futuro_SGM.md` — long-term vision (speculative)
- `SGM_experiment_protocol.md` — experiment protocol
- `SGM_literature_index.md` — literature index

**Experiment results** (in `results/`):
- `experiment_registry.json` — central registry (12 experiments, SGM_0001–SGM_0012)
- `results_exp_SGM_0002..0012.json` — individual results
- `baseline_snapshots_exp_SGM_0003_nodecore_equiv_teorica.json` — NodeCore baseline

**Scripts** (in `experiments/`):
- `run_abduce_*.py` (7 scripts: D dimensionalidad, phase dynamics v1/v2/v3, PPR, decay, XOR)
- `run_nodecore_*.py` (2 scripts: smoke test, memory benchmark)
- `run_ppr_routing.py`
- `t_inf_06_*.py` (3 scripts: equivalence, NodeCore port, stress test)

**Literature** (in `lit/papers/`):
- `kope_arxiv_2604.07904.pdf` — KoPE (Xiao et al., Microsoft Research Asia, April 2026)
- `hipporag_arxiv_2404.10501.pdf` — HippoRAG (NeurIPS 2024)
- `1804.09004.pdf` — Kanerva SDM (verify arxiv ID)
- `2105.13495.pdf` — (verify arxiv ID)

The SGM README's target structure (`motor/`, `decoder/`, `phases/phase1_modos/`, etc.)
is aspirational — those directories do NOT exist yet.

After modularization into `dscng_core.py`, rerun real results:
- v2c OK: acc_pred≈0.33, acc_gt≈0.33, foco≈0.60.
- v2b/v2d: root over transformer does not route sense; transformer predictions do not separate A/B.
- v4/v5: pain/doubt does not distinguish ambiguity or context change.
- v6: selective attention functional (acc_decision≈0.89).
- v8/v8b: closed loop harms baseline.
- v9: weak baseline improvement in fallback synthetic.
- v10: classifier=0.766, loop=0.490.
- v11: conservative loop improves one word, does not generalize.
- v12: embedding-similarity decoder non-functional.
- v13: explicit transition bigrams/trigrams functional (top1≈0.85).
- v14: per-sense A/B model perfect purity.
- v15: sense-loop acc≈0.938.
- v16: competitive memory coherence≈0.750.
- v17/v18/v20: Don Quijote real k-means does not yield usable sense separation for tested words.

## Batch rerun log discipline

After a batch rerun, inspect representative logs and update `_README_ENGINE.md` with the consolidated veredicto list before any new architectural change. Do not introduce new claims while still validating previous changes.

## Repo hygiene before push

Before push: compile all experiment scripts with `py_compile`, run the canonical core script, and confirm local and vault paths are synchronized. Only then run `github_push_inc.py`. If push fails with `URLError` / hostname resolution, retry once; if it fails again, report partial upload and stop.

## Literature audit

The user asked whether similar solutions exist in literature. Core answer retained: most components exist separately; likely novelty is the specific combination: closed-loop natural pain/error, competitive memory, sense-aware routing, conditional generation, relational composition.

## New stable artifacts from this session

- `dscng_core.py` is now the canonical shared core.
- `test_dscng_core.py` is the unit-test contract.
- `run_v25_v2_core.py` is the canonical import-from-core experiment.
- `MetricLogger` must be used for any new experiment to keep metrics comparable.
- `build_polysemy_corpus(..., n_per_sense=350)` has been expanded toward 1000+ examples per sense with controlled augmentation; keep ground truth integrity.

## Active gaps (keep current)

- stable closed loop in real corpora
- generalization beyond one-word/two-sense setup
- groundedness in real prose, not only synthetic or bigram stats
- strong 3-body relational composition
- meta/self-observation / decision pain

## Script inventory

After modularization into `dscng_core.py`, rerun real results:
- v2c OK: acc_pred≈0.33, acc_gt≈0.33, foco≈0.60.
- v2b/v2d: root over transformer does not route sense; transformer predictions do not separate A/B.
- v4/v5: pain/doubt does not distinguish ambiguity or context change.
- v6: selective attention functional (acc_decision≈0.89).
- v8/v8b: closed loop harms baseline.
- v9: weak baseline improvement in fallback synthetic.
- v10: classifier=0.766, loop=0.490.
- v11: conservative loop improves one word, does not generalize.
- v12: embedding-similarity decoder non-functional.
- v13: explicit transition bigrams/trigrams functional (top1≈0.85).
- v14: per-sense A/B model perfect purity.
- v15: sense-loop acc≈0.938.
- v16: competitive memory coherence≈0.750.
- v17/v18/v20: Don Quijote real k-means does not yield usable sense separation for tested words.

## Script inventory

- **Embeddings:** Skip-gram over restricted-context subcorpora works. Full-corpus skip-gram in pure Python is often too slow; prefer epoch reduction or window reduction over abandoning the approach.
- **Generation:** Explicit transition models (bigrams/trigrams conditioned by sense) outperform embedding-similarity decoders. Documented: bigram top1 ≈ 0.63, top5 ≈ 0.94; embedding-similarity top1 ≈ 0.02.
- **Loop design:** Direct focal-omega update destroys signal. Conservative updates (context-only, moving average, threshold gating) do not generalize across words. Loop generation with competitive memory can reach sense coherence ≈ 0.75 on synthetic data, but generalizes poorly. `SenseMemory` should use letter-based keys (`A/B/C...`) when K can exceed 2; derive key as `chr(65+int(pred_class))`.
- **Corpus selection:** Don Quijote is mostly monosemic for candidate words. Use restricted-context fragments around target words (e.g., 60-token windows) for subcorpora instead of trying to parse full sentences.
- **Vault access on Android:** `/sdcard/Hermes/nexus-vault/` and similar paths require `su -c "..."` to list/read files; normal access often returns empty/length 0. Always verify with root when vault listings fail.

## Known failure modes and fixes

- `defaultdict(Counter)` inside another `defaultdict(...)` can surface as `AttributeError: 'int' object has no attribute 'items'` during `+=1` accumulation. Use `defaultdict(lambda: defaultdict(int))` when building nested count tables, not `defaultdict(lambda: defaultdict(Counter))`.
- GitHub push script requires positional args `user token path...`. Do not rely on persisted tokens; confirm with user when token is missing.
- `Counter` has no `.index()`. Build a separate `vocab = sorted(counter.keys())` list for index operations.
- Don Quijote sentence split on `.!?` creates one giant sentence in this text. Use fixed-size token windows around target occurrences instead.
- Restricted-subcorpus skip-gram timeout: if full-book skip-gram times out, switch to fixed-size windows around the target word (e.g., 60 tokens) and reduce epochs/window/neg_samples before abandoning the approach.
- Hidden-layer stream validation: expect a clean stream to have low variance across the 4 semantic channels; noisy or corrupted streams raise variance. Reduced degrees of freedom should be detectable as significantly lower average variance in clean vs noisy runs.
- Log redirection to `/tmp` is unreliable on this Android Hermes host; if validation batches need logs, write them into the home workspace and inspect from there.

## User preferences

- Language: informal Spanish `tú`, direct, "en criollo".
- Continuance: do not pause after every executed step. Continue to the next concrete step and only stop when blocked or when the user asks for a result.
- Batch vs single runs: default to one experiment at a time, but if the user explicitly asks for a full batch or says "sin pausas / en bloque", run the complete batch continuously.
- Documentation: update README after every meaningful result, good or bad.
- Honesty: report failures with structural reasons; do not inflate weak improvements.
- Token handling: do not persist GitHub tokens; user provides them on demand.
- Metric shift: the user's working thesis is that **coherence of domain behavior is a better metric than A/B sense accuracy**. When validating over real corpora, prefer a coherence/overlap score over `acc_gt`; if it fails where `acc_gt` looked fine, surface that explicitly.

## Modularization standard

Use `dscng_core.py` as the single shared core. Canonical class set:
- `SimpleTransformer(vocab, D, lr)` with `contexto(seq)` returning averaged-window vector and storing `current`.
- `RootMemory(D, lr, beta_anchor, beta_repulse, theta, beta_mem)` with `enraizar(A, B)` returning `A|B` and exposing `dolor`, `W_actual`, `last_veredicto`, `last_diver`, `foco`.
- `LinearSenseClassifier(D, lr)` with `fit(X, Y, epochs)` and `predict(x)` returning `0|1`.
- `SkipGram(vocab, D, lr, window, neg_samples)` with `fit(tokens, epochs)`.
- `MetricLogger()` logging canonical metrics `acc_pred`, `acc_gt`, `dolor`, `foco_acc`, `W_actual`; use `summary()` and `to_json(path)`.
- `build_polysemy_corpus(word, n_per_sense, augmentation=True)` for controlled synthetic corpora with ground truth.

Each experiment script should import from `dscng_core` and stay small; do not duplicate these classes. New experiments should be named `run_v25_v{N}_core.py` and write `results_v25_v{N}_core.json`.

## Unit-test contract

Run tests with the available system Python via `terminal`, not `execute_code`, because `execute_code` may fail to link Python on this Android build. Known-good coverage:
- `dot`, `norm`, `cos`, `softmax` against deterministic values.
- `MetricLogger` summary aggregation.
- `SimpleTransformer.contexto` length and `current`.
- `RootMemory.enraizar` returns `A|B`, `dolor>=0`, and stable `W_actual`.
- `LinearSenseClassifier` fit/predict on a linearly separable tiny set.
- `SkipGram.fit` over a tiny synthetic corpus; assert `word in sg.emb`.

## Corpus expansion rule

When expanding synthetic corpora, keep ground truth by mutating only non-target tokens and preserving the target token per sense. Do not change the target token itself.

## Omega0 seeding from k-means offline

Use k-means centers as `RootMemory.omega` initialization when offline silhouette shows `k=2 > k=1` for a target word's contexts. Seeding helps start online, but does not guarantee refinement in current online settings. At minimum, it distinguishes "no bimodal signal in corpus" from "online mechanism fails to refine".

## Dynamic window contraction W(t)

Implemented in `RootMemory.contraer_ventana(W_base, kappa)`; formula: `W_actual = max(2, W_base / (1 + κ·dolor))`. Keep it off by default for early probes; enable it when measuring whether pain/error sharpens focus after a doubt episode. Measure recovery post-doubt, not just the value of `W_actual`.

## Script inventory (canonical, v0.25)

| Script | Purpose |
|--------|---------|
| `run_v25_v2_core.py` | Canonical minimal experiment importing `dscng_core` |
| `run_v25_v3_core.py` | BERT-style transformer (NO FUNCIONAL: acc_clf≈azar) |
| `run_v25_v4_core.py` | Root como sistema de duda (NO FUNCIONAL: acc_decision≈azar) |
| `run_v25_v5_core.py` | Duda como indicador de cambio (NO FUNCIONAL: dolor_en_cambio < dolor_en_estable) |
| `run_v25_v6_core.py` | Atención selectiva sobre bloques largos (NO FUNCIONAL sobre mezcla) |
| `run_v25_v12_core.py` | Decoder por similitud embeddings (NO FUNCIONAL: top1≈0.01) |
| `run_v25_v13_transicion.py` | Modelo transición explícito bigramas/trigramas (FUNCIONAL: top1≈0.85) |
| `run_v25_v14_sense_transition.py` | Transición por sentido A/B (FUNCIONAL: pureza 1.0) |
| `run_v25_v15_loop_sentido.py` | Loop generativo por sentido (FUNCIONAL: acc_sense≈0.938) |
| `run_v25_v16_loop_generativo_memoria.py` | Loop con memoria competitiva (FUNCIONAL: coherencia 0.75) |
| `run_v25_v18_dq_cabo.py` | K-means + bigramas sobre Don Quijote "cabo" (FUNCIONAL PARCIAL) |
| `run_v25_v19_tiempo_dq.py` | K-means sobre contextos bag-of-words de "tiempo" |
| `run_v25_v20_tiempo_sustrato.py` | Skip-gram sobre contextos restringidos de "tiempo" |
| `run_v25_v21_classifier_loop.py` | Clasificador lineal + loop (FUNCIONAL: 1.0 sobre sintético) |
| `run_v25_v22_coherencia.py` | Coherencia de dominio sobre corpus sintético (FUNCIONAL) |
| `run_v25_v22b_coherencia_dq.py` | Coherencia sobre Don Quijote "tiempo" (NO FUNCIONAL: score 0.0) |
| `run_kmeans_seed_online_v7c.py` | K-means seed online (técnico, no semántico) |
| `run_v23_v4.py` | Hebb 3-body sobre Don Quijote (NO FUNCIONAL: 0.036 vs 0.026) |
| `github_push_inc.py` | Push incremental a GitHub |

## Android operational pitfalls (current)

- `/tmp` redirection is unreliable on this Android Hermes host; write batch logs into the home workspace.
- `execute_code` may fail to link Python on this Android build; prefer `terminal` for running scripts.
- `/sdcard/Hermes/nexus-vault/` requires `su -c` to list/read; normal access returns empty.
- `defaultdict(Counter)` inside another `defaultdict(...)` causes `AttributeError` on `+=1`; use `defaultdict(lambda: defaultdict(int))`.
- `Counter` has no `.index()`; build a `vocab = sorted(counter.keys())` list first.
- Don Quijote splits as one giant sentence on `.!?`; use fixed-size token windows around target occurrences.
- Full-book skip-gram in pure Python times out; use restricted-context windows (≈60 tokens) and reduced epochs/window/neg_samples.
- v7/v7b/v7c scripts are lost (only JSON results preserved); do not attempt to reconstruct them blindly.
- GitHub push requires positional args `user token path...`; do not persist tokens. Retry once on `URLError`; if it fails again, report partial upload and stop.
