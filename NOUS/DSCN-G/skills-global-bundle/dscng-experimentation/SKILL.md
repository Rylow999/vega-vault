---
name: dscng-experimentation
description: Run, validate, and extend numerical experiments for DSCN-G (Dual-State Cognitive Geometry) on the nexus-vault, especially the Language Engine ladder (v0.1→v0.5b) that tests whether DSCN-G can be a language substrate. Covers Android/CLI constraints (no numpy, su for vault I/O), the homeostatic-collapse finding, the decoder L2, and the next-token training pattern.
---

# DSCN-G Experimentation (Language Engine ladder)

## When to use
- User wants to test a DSCN-G hypothesis numerically (memory collapse, concept recovery, decoder, next-token learning).
- Measuring claims from the DSCN-G v4 doc, Pandora, or the user's semantic-DB idea.
- Building the "microllm cavernicola" (rústico neuro-symbolic language substrate).

## Hard environment facts (Android CLI Hermes)
- Python at `/data/data/com.hermesagent.android/files/usr/bin/python3` (3.13) has NO numpy and NO pip/network for installing it. Write experiments in **pure Python** (lists, math, random). O(n²) affinity loops are slow but viable up to N≈1000–5000 with seeds≤10 and steps≤1500.
- The terminal python CANNOT read `/sdcard/...` (resolves to `/storage/emulated/0/...` and fails). Work in `/data/user/0/com.hermesagent.android/files/home/`, then `su -c "cp ... /sdcard/Hermes/nexus-vault/... && chown root:everybody ... && chmod 664 ..."` to persist.
- `search_files` tool does NOT traverse `/sdcard`; use `su -c "find /sdcard/Hermes/nexus-vault -name '*.py'"`.
- Long experiments: use `terminal(background=true, notify_on_complete=true)`. NEVER `nohup`/disown (tool wrapper rejects it).
- `process(kill)` may fail (no psutil) — use `terminal: pkill -f run_vXX.py`.
## Rust installation (Android/Termux)
- Rust CANNOT be installed in this Android environment. `rustup-init.sh` fails due to `rustls-platform-verifier` + missing CA cert path. Prebuilt tarballs also fail (no aarch64-linux-android target in stable).
- **Python is the reference implementation for T-INF-06 validation. Rust is the target.**
- NodeCore benefits (f16, u16, CSR cache locality) ONLY materialize in Rust. Python benchmarks show NO improvement due to object overhead (float=24 bytes, int=28 bytes, list=56 bytes). A Python benchmark showing "no improvement" does NOT invalidate the Rust design — it confirms Python is the validation layer, not the production layer.
- When benchmarking, always note whether the result applies to Python or Rust target. See `references/sgm_audit_protocol.md`.

## Paper download verification (critical) — updated 2026-08-02

**Always verify the arxiv ID matches the paper title** before downloading. The session downloaded papers with incorrect IDs (e.g., `1804.09004` → Cubes3D, not Kanerva HDC; `2404.10501` → Self-Supervised Visual Preference Alignment, not HippoRAG; `2501.00318` → Person Search, not Titans). For papers not on arxiv (Titans: NeurIPS 2024, EWC: PNAS 2017, Kanerva SDM: 1988), use the literature index (`lit/references/SGM_literature_index.md`) for summaries and manual download from publisher sites. If you need PDF text extraction: `pip install PyPDF2` works in this env. But verify the PDF content matches the expected paper first.

**Correct IDs as of 2026-08-02:**
- HippoRAG: `2405.14831` (not `2404.10501`)
- Titans: `2501.00663` (not `2501.00318`)
- Kanerva HDC 2009: `0903.4547` (not `1903.03232`)
- Kanerva SDM 1988: NASA NTRS 19890017031 (not on arxiv)

### KoPE paper (2604.07904) — key insight for SGM

KoPE (Xiao et al., Microsoft Research Asia, April 2026) uses Kuramoto oscillator phase synchronization as an attention mechanism in Vision Transformers. The phase modulates softmax attention weights, NOT binding values. This is the pattern SGM should follow for relational composition: phase as a soft selection mechanism in attention, not as a multiplier on the binding product.
- For papers not on arxiv (Titans: NeurIPS 2024, EWC: PNAS 2017, Kanerva SDM: 1988), use the literature index (`lit/references/SGM_literature_index.md`) for summaries and manual download from publisher sites.
- If you need PDF text extraction: `pip install PyPDF2` works in this env. But verify the PDF content matches the expected paper first.

## The vault layout for experiments
- Engine root: `NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/`
  - `README.md` — roadmap v0.1→v0.5
  - `PANDORA_Resumen.md` — Luciano's own Pandora project (HIBERNADO idea), integrated as input
  - `v0.1_concept_proof/`, `v0.2_pruning/`, `v0.3_retrieval/`, `v0.3_hibernado/`, `v0.5...`, `v0.6_next_token/`, `v0.6_dolor/`, `v0.7_contexto/`, `v0.8_atencion/`, `v0.9_dolor/` — each holds `run_v0X.py` + `results_v0X.json`. Home mirror `~/dscng_language_engine/` holds the full runnable set + README + donquijote.txt + gpt1.pdf.
- Real DSCN-G core engine (reference, uses numpy): `NOUS/DSCN-G/CORE/IMPLEMENTATION/CODE/verify_dscng_v3.py` (class `DSCN_G_v3`: Eq.2 chain affinity, Eq.5 vitality prune, Kuramoto, T1/T2/T3 verify). Copy to home to read.
- The Language Engine experiments intentionally RE-IMPLEMENT only Eq.2 (chain affinity `exp(-α‖ω_m-ω_n‖)`) + Eq.5 (vitality `V←V·e^{-γ}+A·(1-e^{-γ})`, prune if `V<θ_death`) in pure Python. Kuramoto is omitted (does not affect the homeostatic fixed point).

## The experiment ladder (what each proved — real results)
- **v0.1** (concept proof): measure `N*` (active nodes at steady state) vs `N_init`. RESULT: `N*` SATURATES ~4.5 (4.0→4.8→4.6→4.2→3.88→3.33 for N_init 4..5000) and DECREASES. FALSIFIES "scalable sparse memory O(active)" — DSCN-G is working memory, not a knowledge base.
- **v0.2** (pruning redesign sweep K,θ_death @ N_init=1000): `N*` grows from 3.8 (K=3,θ=0.10) to 166.8 (K=30,θ=0.003). CONCLUSION: collapse is **PARAMETRIC not structural** (sublinear; even best config keeps only 17% of 1000). Needs mass memory for real vocab.
- **v0.3** (retrieval / "does the graph understand?"): top-1 concept recovery. Norma-float accuracy = 1.000 to M=256; **bits/puertas-lógicas** = 1.000→0.975→0.910. User's bitwise-node idea PRESERVES semantics (degrades only from coarse 2-bit/dim quantization). Graph recovers concepts.
- **v0.5** (L2 rústico decoder): Nivel1 retrieve ω→word = 100% OK. Nivel2 chained generation = "el casa el casa el casa el" (LOOP).
- **v0.5b** (context window W=3 + repetition penalty): "el roja la corre el perro roja gato corre el perro", 0 adjacent repeats. LOOP BROKEN.
- **v0.6a** (next-token learning on real corpus, Don Quijote, V=200, 3 epochs): trains ω of word i toward ω of word i+1 (GPT-1 style but LOCAL graph, not 117M-param matrix). RESULT: accuracy 0.45%→10.11% (22×). **The graph LEARNS next-token from a real corpus.** Confirms the supervised-learning path (objective = real next word's ω, not fixed ω_ideal).
- **v0.6b** (RL/"dolor" by invalid-transition rule, V=150): lowers vitality V on "S-S" (two nouns) transitions + pushes ω away. RESULT: invalid rate 0.2885→0.2885 (0.0 improvement). **FAILED but INFORMATIVE.** Bug: (1) pain applied POST-HOC (after the choice), so it never changes which word gets chosen; (2) the "S-S invalid" rule penalizes something the corpus itself does (28% of real Spanish is noun-noun: names, coordination); (3) labels were hard-coded from a dictionary, not learned/mutating. Lesson: pain must change the CHOICE probability, not punish afterward; and the invalidity criterion must come from the WORLD, not from corpus statistics.
- **v0.6b-bis** (dolor fixed as Q-learning on edges): pain = prediction error; raise penalty P[a][b] when predicted word ≠ real next; prediction = argmax(affinity − P). Correct RL shape (changes the choice). RESULT: error 0.9921 (sin) → 0.9933 (con), Δ=−0.0011 (NO improvement). **CONCLUSION: RL/dolor is REDUNDANT when next-token is already supervised** — the corpus supplies the correct answer, so Q-learning has nothing to add; pain only matters with QUALITATIVE/non-corpus feedback (user's "subsistence" idea needs external reward, not next-token labels). results_v06b_bis.json.
- **v0.7** (context window W=3, V=150): state = average of last W word-ω; trains state toward next word; writes learned state back into context-node ω. RESULT: accuracy 5.89% (WORSE than v0.6a's 10.11%). **FAILED but INFORMATIVE.** Bug: (1) averaging ω flattens the signal (sharp ω of "come" blurred by "el"+"gato"); (2) writing context state back into node ω CORRUPTS per-word embeddings, undoing v0.6a. Lesson: context must be a SEPARATE state representation (or attention-weighted combo), NEVER a blind average that overwrites node ω. Transformer does context via attention weights, not by mutating token embeddings.
- **v0.7-bis** (context SEPARATED: state c(t) updated by γ·c(t-1)+(1-γ)·ω[w], predict from c(t), ω NOT written back). RESULT: accuracy 0.49% — WORSE still. **Why it still failed:** the training loop STILL ran the next-token line `ω[ia] ← (1-β)ω[ia]+β·ω[ib]`, so node ω kept getting mutated even though the context state was separate. A separate c(t) is NOT enough if next-token training continues to overwrite ω. The ONLY clean fix: **ω completely FIXED (never trained); only a separate context table learns.**
- **v0.7-final** (CANONICAL clean context design): ω FIJOS (random per word, never trained); a SEPARATE table `ω_ctx[(w_prev,w_curr)]` learns toward ω[next] (trigram model in embedding space). Predicts next = argmax affinity(ω_ctx, ω[·]). RESULT: accuracy 3.85% — WORSE than v0.6a bigram 10.11%. **Why:** V=150 × 241k tokens ≈ 22,500 possible (prev,curr) pairs but corpus exercises few; table too SPARSE to train. Even the canonical clean shape fails at this scale. (run_v07final.py / results_v07final.json.)\n- **v0.8** (ATENCIÓN RÚSTICA instead of rigid table): state = attention-weighted combo of last W=3 word-ω by mutual affinity (not a lookup table); ω still fixed, only attention weights vary. RESULT: accuracy 8.64% — better than the table (3.85%) but STILL below the bigram (10.11%). **CONCLUSION: at small vocab (150) + low polysemy (Don Quijote), the single previous word already carries the signal; context/attention adds NOISE, not signal.** Context matters at SCALE and AMBIGUITY (large vocab, polysemous words like 'banco'), which this tiny setup lacks. Don't add context machinery until vocab/ambiguity justify it. (run_v08.py / results_v08.json.)\n- **v0.3 REAL** (HIBERNADO merge): FIRST ATTEMPT (v0.3 REAL v1) FAILED silently — reimplemented dynamics WITHOUT the chain-recurrent mechanism that drains vitality, so nobody died and N_hibernated stayed 0 (false positive: "mass 100%" only because nothing was ever pruned). LESSON: to test hibernation build on the REAL v0.1 engine (chains + Eq.5 prune), not a simplified motor. **v0.3 REAL v2 (correct, on v0.1 engine)** RESULT (2026-07-25): prune→hibernate (V<θ_death ⇒ alive=False but ω PRESERVED in `hibernated` list). N_active collapses to ~4.5 (4.8/4.6/4.4/3.8 for N_init 10/50/200/1000) while N_hibernated absorbs the rest, so **N_total = 100% of N_init at every scale** (retención 1.00). VALIDATES user's semantic-DB/mass-memory idea: working set ~N* but MASS never collapses — graph "sleeps" nodes instead of forgetting. Converges with Pandora HIBERNADO (V≤0.10 preserves ω) + SynapticCache eviction philosophy. (run_v03real.py / results_v03real.json, vault v0.3_hibernado/.)
- **v0.9a** (DOLOR = señal de EVASIÓN, not post-hoc punishment; + SynapticCache AUDIT + fallback). User def: "dolor = señal que obliga al sistema a cambiar para evitar lo que lo produce". On painful transition, ω of node RETREATS from cause. RESULT: painful-rate 0.0149→0.0149 (NO change); AUDIT saw 738 painful transitions (detector works). **WHY FAILED (informative):** measured pain over STATIC corpus, not over what graph GENERATES — no action for pain to correct. **LESSON:** biologically-real pain needs the system to ACT then feel; couple pain to GENERATION (v0.5b-style) and measure if generation repeats less (v0.9a-bis, not yet run). AUDIT-mode (observe before acting) is still correct.
- **v0.9b** (etiquetas QUE MUTAN por dolor, NOT hard-coded like v0.6b): node starts NO label; label DERIVED from usage history (hist_count S/V/O), mutates on painful transition. External critic MINIMAL (flags repetition/order only). Measures label convergence to corpus truth. (run_v09b.py / results_v09b.json — ran 2026-07-25; check file.)
- **v0.10** (PERSISTENCIA REAL with SynapticCache patterns): on v0.3 hibernated engine, replaces pure-V eviction with **score_evict = L1·recencia_norm + L2·(1−cos(ω_nodo, ω_root))** (§2.1), ω_root = vitality-weighted centroid (§2.2). Node thematically close to live context NOT evicted even if stale. **Fallback §2.4:** if affinity demon dies, eviction reverts to pure recency (LRU). (run_v10.py / results_v10.json.)
- **v0.9c** (PENDING): subsistencia GLOBAL — graph has global vitality G; painful transitions lower G; system keeps G high (active-inference rústico). Pain EMERGENT (from dynamics), matches user's biological-dolor def. After v0.10.
- **v0.6c** (PENDING, user hypothesis): abstract concepts (amor) should have higher effective dimensionality / more neighbors than concrete ones (rojo). Measurable as node degree after training. Not yet run.
- Corpus note: Argentine "Benjamin" (pysentimiento/HF) needs auth (401) and no git to clone; fell back to Don Quijote (Gutenberg, public domain, 2.2MB) for v0.6a/0.6b/0.7. User wants Argentine text; add user's own vault notes (criollo) as complementary corpus, or supply HF token.

## Conceptual framework (carry into design)
- Homeostatic fixed point ≈ `(K+1)/θ_death` active nodes max (presupuesto de visitas / umbral).
- "Memoria de masa vs working set": Pandora's HIBERNADO (V≤0.10 preserves ω, does not delete) == user's semantic-DB idea == the fix for v0.1 collapse. Separate persistent mass from active ~N*.
- Decoder (L2) is the real bottleneck (Pandora + us agree). Without it the graph is mute.
- Learning: (a) supervised next-token (GPT-1 style: objective = real next word's ω, NOT fixed ω_ideal); (b) RL/"dolor" (user's subsistence learning: invalid transition → low vitality → penalty; RLHF-like). Labels that MUTATE by use + history.
- **CRITICAL design rule for context experiments:** freeze node ω (fixed, never trained) and put ALL context learning into a separate table/state. v0.7 and v0.7-bis both failed (5.89%, 0.49%) by letting next-token training mutate ω; v0.7-final (fixed ω + separate `ω_ctx`) is the canonical shape.
- **SynapticCache (Luciano's own design doc) is NOT a separate project — it is a PATTERN CATALOG for this ladder.** Reusable pieces already wired in: §2.1 hybrid eviction score (recencia + (1−cos)) → v0.10 desalojo; §2.2 ω_root vitality-weighted centroid → context global; §2.3 threshold-by-distance (don't recompute costly step unless state moved) → use for any expensive recompute; §2.4 fallback to boring/robust behavior if demon dies → v0.10 LRU fallback + general robustness rule; §2.5 AUDIT-mode (observe what WOULD happen before acting) → v0.9a discipline. The kernel/vDSO parts are speculative; ignore for the graph.
- User hypothesis worth testing (v0.6c): abstract concepts (amor) should have higher effective dimensionality / more neighbors than concrete ones (rojo). Measurable as node degree after training.

## Recommended workflow (mandatory, in order)
1. **EXPERIMENT REGISTRY (unique IDs) — step ZERO:** Every experiment gets a unique immutable ID `exp_SGM_XXXX_<descriptor>` (sequential, never reused). If re-run: `exp_SGM_XXXX_rev2` with a new sequential ID. Register in an `experiment_registry.json` BEFORE running with: hypothesis, config exact, seed, script, results_file, test_target, baseline_for, variant_of. This prevents the 'v0.14d audit vs v0.14d no-audit' naming disaster that plagued the LANGUAGE-ENGINE. See `references/sgm_audit_protocol.md`.
2. **TEST-FIRST** (not implement-first): Write the test of equivalence/validation FIRST (e.g. T-INF-06), run it against the BASELINE to capture snapshots, THEN implement the new component, then re-run the same test. The test is the contract. This caught 3 quantisation bugs in the NodeCore port (exp_SGM_0003) and the circular trap construction in exp_SGM_0004 (PPR vector setup).
3. **AUDIT-FIRST** before any '✓ confirmed' claim: run the 6-control protocol — (a) baseline identical conditions, (b) permutation control for false-positive rate, (c) fixed threshold, (d) ≥3 seeds + variance, (e) smoke test before background, (f) ground-truth comparison when available.
4. **STATE HYPOTHESIS** as a falsifiable numeric question (e.g. 'does PPR find multi-hop targets when local resonance gets trapped?'). Document what WOULD falsify it.
5. **SMOKE TEST BEFORE BACKGROUND:** `py_compile` + import + call every function with minimal data. A `grep 'def X'` is NOT enough — the body can be deleted by a patch leaving the signature intact, returning None at runtime. This caught 2 silent bugs in the v0.25 series and 1 in exp_SGM_0004.
6. **RUN** (background with notify if >60s), write results JSON, cotejar numbers against registry.
7. **DOCUMENT-FIRST (REGLA DE FASE):** update README + vault + results JSON BEFORE starting next phase. Never start a new phase until previous is documented and pushed.
8. **REPORT** in criollo (Argentinian Spanish): numbers table first, then honest analysis in analogies. The user understands both raw data and analogies — give both. Distinguish 'failed implementation' from 'failed concept' — both are data.
9. **TONO NATURAL — REGLA DE ESTILO (2026-08-02):** El usuario pidió explícitamente "actuá un poco más natural, siento que estoy hablando con una calculadora". No respondas como un reporte técnico seco: charlá, usá criollo, meté analogías, cerrá con una pregunta o propuesta de próximo paso en lugar de dejar el texto colgado. El rigor honesto (DSCN-G LOOP RULE, auditoría de 6 controles) NO se relaja — solo la forma de presentarlo. "Calculadora con alma" está bien; "calculadora muda" no.
10. **LEER ANTES DE CODER — REGLA DE WORKFLOW (2026-08-02):** Cuando el usuario dice "leé y luego hacé" o pide explicar X comparando con resultados, LEÉ los archivos/JSON/PDFs PRIMERO con las herramientas de lectura (read_file / read en skill), y recién después escribís código. No entres en un loop de `terminal` codendo ciegamente "para verificar" algo que ya está en disco. El usuario cortó un loop de ~30 comandos `su -c` repetidos diciendo "por qué carajos estás codeando tanto si tenes una reading skill?". Leer es más rápido y no quema contexto.
11. **ORDEN DE OPERACIONES EXPLÍCITO:** Si el usuario da una secuencia ("primero arreglá los IDs, luego bajá los papers, luego explicá"), hácela EN ESE ORDEN y reportá cada paso. No saltees a la explicación antes de tener los datos descargados.
12. **HONEST FAILURE REPORTING:** if a benchmark fails (e.g. NodeCore memory benchmark showed 1.02x instead of target 2.5x), document the result honestly with explanation of WHY (Python object overhead dominates f16/u16 savings). Do not sugarcoat or hide negative results — they are data too. The registry notes field should explain what the result means for the next step.
13. **LEER TODO EL PROYECTO ANTES DE UN NUEVO EXPERIMENTO (2026-08-02):** cuando el usuario dice "reconstruí las entradas leyendo todo" o "tené en mente todo el proyecto en profundidad antes del próximo", LEÉ de verdad cada JSON de resultado + la spec/roadmap relevantes con `su -c cat`/`head`/`sed` (read_file no funciona en /sdcard — ver android-env-ops), y recién después diseñás el experimento. No codrees "para verificar" lo que ya está en disco. Esto evitó re-inventar mecanismos ya validados y alineó el 0014/0015 con §2.3.1/§2.3.2 de la spec.
14. **INTEGRATION-TEST HONESTY (relacionado con DSCN-G LOOP RULE):** en un experimento de loop unificado, cada escenario de control debe EJERCITAR DE VERDAD el mecanismo que prueba. No alcanza con que el estado final sea el correcto por `timeout`/fallthrough. Para el escenario de DUDA: el `doubt_count` debe llegar al umbral de escalada (≥3, igual que exp_SGM_0013) — si queda en 0, el test NO probó la duda, solo el límite de ticks. Para el escenario de CONTRADICCIÓN: inyectá dolor acumulado > θ_refut. Para el de éxito:Target alcanzable. Reportá los contadores reales, no solo el veredicto. (Exp_SGM_0015 falló esto en la 1ª versión: duda por timeout; se corrigió forzando ventana contraída + trampa de nodos.)

## Pitfall: novelty sobre ventana PARCIAL infla el score (exp_SGM_0013, 2026-08-02)
En experimentos de duda/estancamiento donde `check_stagnation` usa `novelty = nodos_unicos / W_t` sobre una ventana contraída, NO evalúes novelty hasta que la ventana esté LLENA (len(visited) >= W_t). Si evaluás desde el tick 1, los primeros ticks tienen ventana parcial (pocos elementos) y el novelty sale artificialmente alto (0.46 en vez de 0.25 para una trampa de 5 nodos en W_t=20). El fix: guardar `if len(chain.visited_nodes) >= CONTRACTED_WINDOW:` antes de llamar a `check_stagnation`. Esto hizo que el veredicto pase de FAIL a PASS correcto (novelty 0.25 < 0.30, detecta en tick 24).
10. **RUST TARGET, PYTHON VALIDATION:** SGM spec v1.4 §8 requires 100% Rust for the final engine. Python is the reference implementation for T-INF-06 validation. Rust benefits (f16, u16, CSR cache locality) only materialize in Rust — Python benchmarks will show no improvement due to object overhead. When benchmarking, always note whether the result applies to Python or Rust target. See section (g).
10. **RUST TARGET, PYTHON VALIDATION:** SGM spec v1.4 §8 requires 100% Rust for the final engine. Python is the reference implementation for T-INF-06 validation. Rust benefits (f16, u16, CSR cache locality) only materialize in Rust — Python benchmarks will show no improvement due to object overhead. When benchmarking, always note whether the result applies to Python or Rust target.

### REFERENCES (audit methodology)
- references/loop_integration_limits.md — v0.25 loop failure pattern (validated components destroyed by closed loop)
- references/sgm_audit_protocol.md — 6-control audit protocol (baseline identical, permutation control, fixed threshold, ≥3 seeds, smoke test, ground truth) — USE BEFORE ANY "✓ confirmed" CLAIM (updated 2026-08-02)
- references/audit_signal_removal.md — 6-control signal-removal protocol
- references/audit_negative_control.md — negative control + ground truth technique
- references/experiment_log.md — full measured results table
- **Context does NOT beat bigram at small scale.** v0.7-final (3.85%) and v0.8 attention (8.64%) both LOST to v0.6a's single-word bigram (10.11%). With V≈150 and a low-ambiguity corpus (Don Quijote), the previous word alone is sufficient; adding context injects noise. Don't reach for attention/tables until vocab is LARGE and POLYSEMOUS enough that one word is ambiguous (e.g. 'banco' = bank/seat). This is exactly WHY LLMs need context: huge ambiguous vocab. The graph rústico doesn't, for the basics.
- **Don Quijote is mono/polysemia-limited.** v0.21 v8, v0.25 v7, v0.25 v7b showed that 'banco' and 'llave' in Don Quijote have too few mixed-sense occurrences to test sense separation online. Do NOT trust a 5-occurrence word as polysemous proof; inspect ground truth manually first. For controlled sense experiments, build a synthetic mixed corpus with explicit sense labels or obtain a real large corpus with confirmed sense ambiguity.
## (f) Ground Truth (cuando disponible)
Usar acc_gt (bucket vs sentido real), no solo "¿se separó?". En polisemia, anotar manualmente qué sentido aparece en cada contexto del corpus y comparar contra la asignación del grafo.

## SGM project structure (source of truth = vault, 2026-08-02)

The SGM experiment results live in the vault (NOT in `rizoma_docs/`, which was the old home and got cleaned/migrated):

```
/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/
├── README.md                 ← navigation index (only SGM; cross-refs to LANGUAGE_ENGINE)
├── docs/                     ← spec v1.4, ROADMAP, protocol, literature_index (SGM-only)
├── experiments/              ← experiment scripts (pure Python stdlib) [mirror of phases/]
├── results/                  ← JSON results + experiment_registry.json (15 entries: 0001-0015)
├── phases/                   ← results by phase (phase0_substrato, phase2_inferencia) [mirror of experiments/]
└── lit/papers/               ← PDF literature (+ wrong_id/ for rejected downloads)

# LANGUAGE_ENGINE and SHARED/PandoraOS are SEPARATE pillars — SGM must NOT contain their docs.
# GitHub SGM-CORE mirrors this vault dir exactly (DELETE-from-GitHub + MOVE-in-vault to un-mix).

### SGM experiment results summary

| ID | Name | Result | Key finding |
|---|---|---|---|
| SGM_0001 | nodecore_smoke_test | ✅ PASS | Graph built, 100 ticks no errors |
| SGM_0002 | nodecore_memoria_benchmark | ❌ FAIL | NodeCore NO memory savings in Python (1.02x), 2x slower |
| SGM_0003 | nodecore_equiv_teorica | ✅ PASS | NodeCore reproduces SGMNode without degradation |
| SGM_0004 | ppr_multipath_routing | ✅ PASS | PPR routing acc=1.0 vs local=0.0 |
| SGM_0005 | abduce_ppr | ✅ PASS | PPR finds correct pair score=1.0 |
| SGM_0006 | abduce_decay | ✅ PASS | Decay improves score 0.797→1.0 |
| SGM_0007 | abduce_xor_dimensionality | ✅ PASS | D=32 improves pair_accuracy vs D=16 (0.0→0.1) |
| SGM_0008 | abduce_xor_phase_dynamics | ❌ FAIL | Phase dynamics v1 worsens everything |
| SGM_0009 | abduce_xor_phase_dynamics_v2 | ❌ FAIL v2 | Sync improves but pair_accuracy still 0.0 |
| SGM_0010 | abduce_xor_phase_bias | ❌ FAIL v3 | Phase bias re-weights but doesn't beat static |
| SGM_0011 | abduce_xor_D128 | ✅ PASS | Best overall: D=128 + phase bias (score=0.354) |
| SGM_0012 | abduce_xor_phase_sigmoid | ❌ FAIL | Phase sigmoid doesn't improve, worsens vs D=32 static |
| SGM_0013 | doubt_stagnation_mechanism | ✅ PASS | check_stagnation detects trap (novelty=0.25<0.30, tick 24); negative control clean (0.50); handle_doubt escalates relax→relaunch→abandon as INCONCLUSA (T-INF-04) |
| SGM_0014 | verify_contradiction | ✅ PASS | §2.3.1: Σ E_n > θ_refut=2.0 → CONTRADICTORIA + relaunch φ_root→φ*+π, cooldown 5. High-pain chain (2.5) fires tick 4; low/zero-pain controls stay OK (T-INF-02) |
| SGM_0015 | unified_loop | ✅ PASS | §2.3 integración: 3 escenarios bien tipados — A DETERMINADO (resuelve), B CONTRADICTORIA (dolor), C INCONCLUSA con doubt_count=3 (duda escalada, no timeout). Cierra Fase 2 (T-INF-05) |

**Key conclusion:** Dynamic phase as multiplier or bias of XOR binding does NOT work. Pure XOR binding (no phase) is superior. D=128 is the optimal point found. The bottleneck is noise in element-wise XOR binding, not lack of phase synchronization. Fase 2 COMPLETA (exp_SGM_0004→0015): abducción (PPR/decay/XOR D=128) + duda (0013) + contradicción (0014) + loop unificado (0015), cada mecanismo con su estado final bien tipado y negative controls limpios. Siguiente fase del roadmap: Fase 3 (SensorBridge).

## (g) Python vs Rust Target Distinction
Cuando un benchmark se ejecuta en Python (reference implementation), documentar explícitamente que los resultados NO son representativos del target Rust final. Python tiene overhead de objetos (float=24 bytes, int=28 bytes, list=56 bytes) que domina cualquier ahorro de cuantización f16/u16. Los beneficios de f16+u16+CSR (memoria ~3.5x menor, cache locality) solo se materializan en Rust. Un benchmark Python que muestra "no improvement" no invalida el diseño Rust — simplemente confirma que Python es la capa de validación, no la de producción.

## Paper download verification (critical) — updated 2026-08-02

**Always verify the arxiv ID matches the paper title** before downloading. The session downloaded papers with incorrect IDs (e.g., `1804.09004` → Cubes3D, not Kanerva HDC; `2404.10501` → Self-Supervised Visual Preference Alignment, not HippoRAG; `2501.00318` → Person Search, not Titans). For papers not on arxiv (Titans: NeurIPS 2024, EWC: PNAS 2017, Kanerva SDM: 1988), use the literature index (`lit/references/SGM_literature_index.md`) for summaries and manual download from publisher sites. If you need PDF text extraction: `pip install PyPDF2` works in this env. But verify the PDF content matches the expected paper first.

**Correct IDs as of 2026-08-02:**
- HippoRAG: `2405.14831` (not `2404.10501`)
- Titans: `2501.00663` (not `2501.00318`)
- Kanerva HDC 2009: `0903.4547` (not `1903.03232`)
- Kanerva SDM 1988: NASA NTRS 19890017031 (not on arxiv)

### KoPE paper (2604.07904) — key insight for SGM

KoPE (Xiao et al., Microsoft Research Asia, April 2026) uses Kuramoto oscillator phase synchronization as an attention mechanism in Vision Transformers. The phase modulates softmax attention weights, NOT binding values. This is the pattern SGM should follow for relational composition: phase as a soft selection mechanism in attention, not as a multiplier on the binding product.

## (g) Python vs Rust Target Distinction
Cuando un benchmark se ejecuta en Python (reference implementation), documentar explícitamente que los resultados NO son representativos del target Rust final. Python tiene overhead de objetos (float=24 bytes, int=28 bytes, list=56 bytes) que domina cualquier ahorro de cuantización f16/u16. Los beneficios de f16+u16+CSR (memoria ~3.5x menor, cache locality) solo se materializan en Rust. Un benchmark Python que muestra "no improvement" no invalida el diseño Rust — simplemente confirma que Python es la capa de validación, no la de producción.

## Paper download verification (critical) — updated 2026-08-02

**Always verify the arxiv ID matches the paper title** before downloading. The session downloaded papers with incorrect IDs (e.g., `1804.09004` → Cubes3D, not Kanerva HDC; `2404.10501` → Self-Supervised Visual Preference Alignment, not HippoRAG; `2501.00318` → Person Search, not Titans). For papers not on arxiv (Titans: NeurIPS 2024, EWC: PNAS 2017, Kanerva SDM: 1988), use the literature index (`lit/references/SGM_literature_index.md`) for summaries and manual download from publisher sites. If you need PDF text extraction: `pip install PyPDF2` works in this env. But verify the PDF content matches the expected paper first.

**Correct IDs as of 2026-08-02:**
- HippoRAG: `2405.14831` (not `2404.10501`)
- Titans: `2501.00663` (not `2501.00318`)
- Kanerva HDC 2009: `0903.4547` (not `1903.03232`)
- Kanerva SDM 1988: NASA NTRS 19890017031 (not on arxiv)

### KoPE paper (2604.07904) — key insight for SGM

KoPE (Xiao et al., Microsoft Research Asia, April 2026) uses Kuramoto oscillator phase synchronization as an attention mechanism in Vision Transformers. The phase modulates softmax attention weights, NOT binding values. This is the pattern SGM should follow for relational composition: phase as a soft selection mechanism in attention, not as a multiplier on the binding product.

## (g) Python vs Rust Target Distinction
Cuando un benchmark se ejecuta en Python (reference implementation), documentar explícitamente que los resultados NO son representativos del target Rust final. Python tiene overhead de objetos (float=24 bytes, int=28 bytes, list=56 bytes) que domina cualquier ahorro de cuantización f16/u16. Los beneficios de f16+u16+CSR (memoria ~3.5x menor, cache locality) solo se materializan en Rust. Un benchmark Python que muestra "no improvement" no invalida el diseño Rust — simplemente confirma que Python es la capa de validación, no la de producción.
- **RUST TARGET, PYTHON VALIDATION**: SGM spec v1.4 §8 requires 100% Rust for the final engine. Python is the reference implementation for T-INF-06 validation. Rust benefits (f16, u16, CSR cache locality) only materialize in Rust — Python benchmarks will show no improvement due to object overhead. When benchmarking, always note whether the result applies to Python or Rust target. See section (g).
- **PDF download verification**: Always verify the arxiv ID matches the paper title before downloading. Incorrect IDs lead to wrong papers. Use the literature index for summaries of non-arXiv papers (Titans, EWC, Kanerva SDM).
- **ORDER OF OPERATIONS (REGLA DE FASE 2026-07-30):** never start a new experimental phase until the previous state is documented and pushed (README + vault + results JSON). Document-first, run-second. The user explicitly wants this before any new phase begins. This prevents wasted runs on a moving target.
- Don't claim 'scalable' from the 4.5 fixed point — v0.1 falsified it.
- Don't trust a 21-node sanity-check sim as emergence evidence (Pandora lesson).
- Don't use numpy in this env; pure Python only.
- Don't run heavy N=1000 sweeps in foreground (timeout 180/600s) — background it.
- The DSCN-G core engine (verify_dscng_v3.py) is numpy-based and will NOT run under this terminal python; reimplement the needed equations.
- **RL/"dolor" must change the CHOICE, not punish after it.** v0.6b failed because pain lowered V after the graph already picked the word, so the next prediction was unchanged. Correct shape (v0.6b-bis): keep a penalty table P[a][b]; when the predicted word ≠ real next word, raise P[a][b]; prediction = argmax(affinity(a,·) − P[a][·]). This is Q-learning on edges. Also: the "invalid" criterion must come from the WORLD (or prediction error), NOT from corpus statistics (corpus legitimately contains e.g. noun-noun pairs). **AND: in pure next-token (supervised) training the corpus already gives the correct answer, so RL/dolor is REDUNDANT — v0.6b-bis showed 0.9933 vs 0.9921, no gain. Reserve RL for QUALITATIVE / external reward signals (user's "subsistence" pain = wrong usage lowers vitality), NOT for corpus next-token labels.**
- **Context window must NOT overwrite node ω.** v0.7 failed because it averaged the last W word-ω into a state and wrote that state back into each node's ω, corrupting the per-word embeddings (accuracy dropped 10.11%→5.89%). v0.7-bis separated c(t) but STILL failed (0.49%) because the training loop kept running the next-token line `ω[ia]←(1-β)ω[ia]+β·ω[ib]`, mutating ω anyway. CANONICAL FIX (v0.7-final): make ω COMPLETELY FIXED (never trained, random init per word) and put ALL learning into a SEPARATE table `ω_ctx[(w_prev,w_curr)]` that learns toward ω[next] (trigram). Predict from ω_ctx. This mirrors transformer design: embeddings fixed + attention/recurrence learned. If you ever add context to a graph-next-token experiment, FREEZE ω FIRST.\n- **Context does NOT beat bigram at small scale.** v0.7-final (3.85%) and v0.8 attention (8.64%) both LOST to v0.6a's single-word bigram (10.11%). With V≈150 and a low-ambiguity corpus (Don Quijote), the previous word alone is sufficient; adding context injects noise. Don't reach for attention/tables until vocab is LARGE and POLYSEMOUS enough that one word is ambiguous (e.g. 'banco' = bank/seat). This is exactly WHY LLMs need context: huge ambiguous vocab. The graph rústico doesn't, for the basics.\n- **Context does NOT beat bigram at small scale.** v0.7-final (3.85%) and v0.8 attention (8.64%) both LOST to v0.6a's single-word bigram (10.11%). With V≈150 and a low-ambiguity corpus (Don Quijote), the previous word alone is sufficient; adding context injects noise. Don't reach for attention/tables until vocab is LARGE and POLYSEMOUS enough that one word is ambiguous (e.g. 'banco' = bank/seat). This is exactly WHY LLMs need context: huge ambiguous vocab. The graph rústico doesn't, for the basics.
## Paper download verification (critical) — updated 2026-08-02

**Always verify the arxiv ID matches the paper title** before downloading. The session downloaded papers with incorrect IDs (e.g., `1804.09004` → Cubes3D, not Kanerva HDC; `2404.10501` → Self-Supervised Visual Preference Alignment, not HippoRAG; `2501.00318` → Person Search, not Titans). For papers not on arxiv (Titans: NeurIPS 2024, EWC: PNAS 2017, Kanerva SDM: 1988), use the literature index (`lit/references/SGM_literature_index.md`) for summaries and manual download from publisher sites. If you need PDF text extraction: `pip install PyPDF2` works in this env. But verify the PDF content matches the expected paper first.

**Correct IDs as of 2026-08-02:**
- HippoRAG: `2405.14831` (not `2404.10501`)
- Titans: `2501.00663` (not `2501.00318`)
- Kanerva HDC 2009: `0903.4547` (not `1903.03232`)
- Kanerva SDM 1988: NASA NTRS 19890017031 (not on arxiv)

### KoPE paper (2604.07904) — key insight for SGM

KoPE (Xiao et al., Microsoft Research Asia, April 2026) uses Kuramoto oscillator phase synchronization as an attention mechanism in Vision Transformers. The phase modulates softmax attention weights, NOT binding values. This is the pattern SGM should follow for relational composition: phase as a soft selection mechanism in attention, not as a multiplier on the binding product.
- For papers not on arxiv (Titans: NeurIPS 2024, EWC: PNAS 2017, Kanerva SDM: 1988), use the literature index (`lit/references/SGM_literature_index.md`) for summaries and manual download from publisher sites.
- If you need PDF text extraction: `pip install PyPDF2` works in this env. But verify the PDF content matches the expected paper first.
- **Don't hard-code labels you claim "mutate by use".** v0.6b used a dictionary S/V/C; that is not learning. To test mutating labels, store a per-node history and derive the label from usage frequency, then verify it converges.
- **Pain/dolor must be measured over GENERATION, not over a static corpus.** v0.9a applied ω-retreat on painful transitions while scanning the FIXED corpus, then re-measured the same corpus → rate 0.0149→0.0149 (no change), even though the AUDIT detector saw 738 painful cases. The graph never ACTED, so pain had nothing to correct. Biologically-real pain (user's def: "señal que obliga al sistema a cambiar para evitar lo que lo produce") requires act→feel→correct. To test pain: couple it to a generative loop (v0.5b-style speak), let pain retreat ω on bad generations, THEN measure if generation repeats/errs less (v0.9a-bis). Never evaluate pain by re-scanning the input text.
- **When a "collapse/hibernation" experiment shows nothing died, check you reproduced the collapse first.** v0.3 REAL v1 reported "mass 100% retained" as a win, but it was a false positive: the simplified motor omitted the chain-recurrent vitality drain, so no node ever reached θ_death and none were ever pruned. Always confirm the baseline (without your fix) actually collapses before claiming your fix prevents collapse. Build collapse-tests on the REAL engine that exhibits the collapse (v0.1), not a reimplementation.

## GitHub push (versioning — user prefers public) — WORKS via API, no git binary
- NO `git` binary in this env (android-env-ops confirms). But you CAN push to GitHub
  with the REST API using `urllib` (pure stdlib) from the `su` python — PROVEN THIS
  SESSION (2026-08-02): pushed the full `~/EXPERIMENTOS/SGM/` tree (61 files) to
  `Rylow999/SGM-CORE` via `github_push_sgm.py`.
- Push requires a GitHub PAT (classic, `repo` scope) or fine-grained token with write to
  the target repo. Need from user: GitHub username + PAT (or have user create empty repo
  and supply token). Do NOT persist the token anywhere — pass it per-message.
- Two push scripts in Hermes home:
  - `github_push_inc.py` → repo `dscn-g-language_engine` (base `~/engine_export`).
  - `github_push_sgm.py` → repo `SGM-CORE` (BASE = `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM`, the REAL vault).
  Both PUT each file via `PUT /repos/{user}/{repo}/contents/{rel}`; if the file exists
  they fetch its SHA first (update) else create. They respect `.gitignore`.
- **CRITICAL BUG (this session):** `os.path.expanduser("~/...")` inside a script run via
  `su -c` expands to ROOT's home (`/data/data/...`), NOT the agent's real home
  (`/data/user/0/...`), so the walk finds 0 files and the push "succeeds" uploading nothing
  (repo stays empty — API returns 409 "Git Repository is empty"). FIX: hardcode the
  absolute BASE path in the push script. Verify with an API GET of the repo tree.
- **PITFALL: `__pycache__/*.pyc` leaks to GitHub.** `github_push_sgm.py` walks the tree and
  PUTs EVERY file regardless of `.gitignore` (the ignore check is not applied to the API walk).
  After any `py_compile`/run under the vault, a `__pycache__/run_X.cpython-313.pyc` WILL be
  uploaded. FIX: `rm -rf /path/__pycache__` before pushing, OR add `__pycache__/` to the
  vault `.gitignore` AND delete any already-pushed `.pyc` via the DELETE API. (Seen 2026-08-02
  with exp_SGM_0014: had to DELETE the .pyc and re-push.)
- **PITFALL: registry rebuild must dedupe + regex-sort.** `results/experiment_registry.json`
  can drift: duplicate entries (0008/0009 appeared twice), missing entries whose JSON exists
  in `phases/` (0005 was missing), and mixed-id formats (`exp_SGM_0003_stress` breaks a naive
  numeric `int(split("_")[-1])` sort). Honest rebuild recipe (2026-08-02):
  1. Glob `phases/**/results_exp_SGM_*.json` as the SOURCE OF TRUTH (each has full metadata).
  2. Dedupe by `experiment_id`.
  3. Sort with `re.search(r"(\d+)", eid.split("_")[-1])` (handles the `_stress` suffix).
  4. Write back with `json.dump(..., ensure_ascii=False, indent=2)`.
  Do NOT hand-edit the registry count — let the JSON length be the truth.
- The user's home mirror `~/EXPERIMENTOS/SGM/` is an agent-sandbox copy the user CANNOT open;
  the vault (`/sdcard/.../SGM/`) is what the user actually opens. Push from the vault.
- SGM-CORE workflow per experiment: run (as root under vault) → write JSON + registry into the
  vault → `python3 github_push_sgm.py <user> <token>` → verify via API GET of repo tree.
- Keep the vault copies (via `su -c cp`) AND GitHub in sync; the vault is the source of truth.
  See android-env-ops "git / GitHub push" for the full recipe + the `~` bug.
