---
name: sgm-core-dev
description: Running SGM-CORE (Synaptic Graph Model) experiments on Android — vault layout, the sequential experiment workflow Luciano expects, the github_push_sgm.py script and its known bugs, repo hygiene, and the hard rule of SGM/LE separation. Use whenever Luciano asks to define, run, verify, push, reconstruct, or clean up SGM experiments (exp_SGM_00XX).
---

# SGM-CORE Dev Workflow

SGM (Synaptic Graph Model) lives in a vault at
`/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM` and is mirrored to GitHub
`Rylow999/SGM-CORE`. SGM is **STRICTLY SEPARATE** from the DSCN-G Language Engine (LE) —
see Pitfalls. Treat them as two repos that only cross-reference.

## When to use
- Define / run / verify a new `exp_SGM_00XX`.
- Push vault → GitHub via `github_push_sgm.py`.
- Clean or reorganize the SGM repo (registry, READMEs, lit/papers, .gitignore, LICENSE).
- Reconstruct or audit `results/experiment_registry.json`.

## User workflow — EMBED THESE (Luciano is explicit, corrects when missed)
- **One experiment at a time, sequential.** He prefers chatting between each. Do NOT silently
  batch many experiments. After each run, explain results in **criollo** (plain, warm, informal ES).
- **Deep-read the whole project before the next experiment.** Before starting `exp_SGM_00XX`,
  read every result JSON + the spec/roadmap so the project is "clavado en la cabeza" from real
  data, not memory. Reconstruct the registry by reading the actual JSONs, not from memory.
- **Verify, don't claim.** Confirm push exit codes, GitHub file presence, and registry JSON
  validity with real tool output before reporting success. Never say "done" without the proof.
- **Never assume when deleting/moving files.** Open the file and confirm what it actually is.
  Example: a PDF named `hipporag_v2_2025.pdf` was really SNAP (McGill 2024) — confirmed by
  extracting text with PyPDF2, not by its name. Verify md5 before declaring two files duplicates.

## Vault layout (real, not aspirational)
- `docs/` — spec v1.4, roadmap, protocol, `SGM_literature_index.md`, `Arquitectura_Pure_L2_Pandora.md`, `RIZOMA_Vision_Futuro_SGM.md`.
- `phases/phase0_substrato/`, `phases/phase2_inferencia/` — `run_*.py` + `results_*.json`.
- `experiments/` — mirror of `run_*.py`. `results/` — mirror of `results_*.json` + `experiment_registry.json`.
- `lit/papers/` — PDFs (kept LOCAL in vault; EXCLUDED from GitHub via .gitignore). `lit/papers/wrong_id/` — PDFs with wrong IDs.
- `README.md` (raíz) = canonical. `README_SGM.md` = navigation index only. (`docs/SGM_README.md` was deleted — it was a duplicate with LE mix.)

## Experiment convention
- Name: `exp_SGM_00XX_<short_name>`. Script: `phases/phase2_inferencia/run_<short_name>.py`.
  Result: `results_exp_SGM_00XX_<short_name>.json`. Mirror script→`experiments/`, JSON→`results/`.
- Each result JSON carries: `experiment_id`, `name`, `phase`, `date`, `hypothesis`,
  `config`, `result` (dict with `pass`), `script`, `results_file`, `test_target`
  (e.g. `T-INF-02`), `lit_refs`, `notes`, `notes_criollo`.
- After a run: append entry to `results/experiment_registry.json` (dedup by `experiment_id`;
  sort by number). Registry entry keys: `experiment_id, name, phase, date_created, date_run,
  status, test_target, hypothesis, result`.
- Smoke-test every script first: `py_compile` then run. Stdlib-only (no pip installs on device).
- **Test-design discipline (learned hard on 0016):** when proving a mechanism *changes behavior*,
  do NOT use "the walk path differs on a trivial graph" — a global-nearest node dominates and the
  mode's boost won't reverse the ranking, so the test falsely FAILS (PASS:False) even though the
  mechanism is correct. Instead build a **competition scenario**: two candidate nodes at EQUAL
  distance from the root, connected by DIFFERENT edge types (e.g. Terminal vs Causal). With the
  spec's `β_mode` table, Sensorial (Terminal boost 2.0) must pick the Terminal node and Razonamiento
  (Causal boost 2.0) must pick the Causal node. That proves the mode changes the decision. Also add
  independent checks: affinity-with-boost differs between modes, W(t)=W_base/(1+κ_W·E) differs, and
  mode transition leaves ω uncontaminated. If a test fails, suspect the TEST design before the mechanism.
- **Separate orthogonal concerns into separate experiments (trazability rule, learned on B/0016-0017):**
  when one next step bundles two independent validations (e.g. "type the modes" AND "scale the loop
  to a large graph"), SPLIT them (0016 = modos tipados, 0017 = escalado honesto). If a combined
  experiment fails you cannot tell which half broke. This also satisfies the DSCN-G LOOP RULE
  ("require >=2-word generalization before declaring a loop successful") — scale only AFTER the
  building block is proven alone.
- **Scaled-loop / contradiction test-design (learned hard on 0017):** to prove CONTRADICTORIA fires
  under load, pain must be ON the active path, not on isolated nodes. Two failure modes bit us:
  (a) marking 15% of nodes `painful` and letting affinity pick the walk — the walk never VISITS a
  painful node, so accumulated pain stays 0 and contradiction never triggers; (b) even with per-tick
  pain injected at `cur` (`painful_path=True`), if the QUERY sits in its OWN cluster the walk resolves
  (DETERMINADO) in 1-2 ticks before pain > θ_refut=2.0. Honest fix: set a REMOTE target cluster
  (`tc = (nc[q] + 5) % CLUSTERS`) AND inject per-tick pain. Only then does the long painful walk
  accumulate >2.0 and fire CONTRADICTORIA. General rule: for any "mechanism X should fire under
  condition Y" test, make Y actually occur ON the execution path.
- **Autonomy / self-mod experiments (0018 pattern, learned 2026-08-02):** when the next step is a
  system that mutates its OWN spec, design it as LIBERTY + DAMAGE-MEASUREMENT + CONSEQUENCE, not as a
  locked-down sandbox. Concrete design that passed:
  * The system mutates a FORK of its spec (a deep copy), never the live original.
  * Damage is measured with the system's OWN signals (dolor Eq.6, novelty/duda, tasa de resolución) —
    NOT a hardcoded "good/bad" flag.
  * Three consequences: (a) mutation improves metrics → PROMOTE (becomes new valid config);
    (b) mutation damages AND is reversible → REVERT to the pre-mutation snapshot (baseline_snapshots
    pattern from 0003); (c) mutation damages AND is irreversible (e.g. tries to delete an IMMUTABLE
    structure like `edge_types`) → create a "prohibido" node A FUEGO in the graph.
  * The "marca a fuego" is CREATED by the system but CANNOT BE DELETED by it (only the operator can) —
    so the system has liberty to err and learn, but cannot wipe its own error memory. This is the
    self-protection Luciano's philosophy requires ("a well-made system won't self-destruct because
    that would be stupid"): the brakes are its own reason to exist, not a cage we bolt on.
  * Pre-application brake = INVARIANT CHECK, not a metric. A mutation that deletes the brakes
    (THETA_REFUT→∞, W_BASE→0, ALPHA→0) must be blocked BEFORE applying by asserting the invariants
    `THETA_REFUT<999 and W_BASE>0 and ALPHA>0` — NOT by re-running the task and seeing lower accuracy
    (a walkable toy graph resolves 1.0 either way, so a metric check never fires). This is a real test
    trap: "delete brakes" looks harmless on a small walkable graph.
  * TEST TRAP (caso D, 0018): do NOT measure "does the mutation hurt accuracy" to block suicidal
    mutations — on a walkable graph it won't. Block on INVARIANT VIOLATION instead.
  * TEST TRAP (caso B, 0018): to make pain actually accumulate, inject per-tick pain on the ACTIVE
    NODE (`painful_path=True`), and use a REMOTE target cluster so the walk is long enough to exceed
    θ_refut. Without both, the "damage" never registers and the revert/reject branch is dead code.
  * Document the philosophy→experiment chain: write a `docs/NOTA_FILOSOFICA_*.md` capturing the
    hypothesis (e.g. conciencia alienígena, sentido de existir como efecto secundario, trauma/singularidad
    nodal) and reference it from the experiment's `philosophical_note_ref` field. This keeps the
    reasoning auditable when you return months later.
  * SensorBridge / HDC projection (0019 pattern, learned 2026-08-02): when projecting signals to a
    NORMALIZED omega (unit vector) of dimension D, the max pairwise distance is 2.0 — a threshold like
    5.0 can NEVER fire. Set a realistic threshold (~0.3 for D=128). Also: HDC of LOW granularity
    (CHUNK=16 → 8 chunks) COLLAPSES signals of equal smoothness (audio sine vs thermal ramp land at
    distance ~0.2). Increase granularity (CHUNK=8 → 16 chunks) to separate structurally-different
    signals. Round-trip recovery needs the INVERSE permutation per chunk (store `inv` beside the bind
    perm) — without it unproject is garbage. Test INJECTIVITY only between STRUCTURALLY DISTINCT signals
    (audio vs visual-edge vs impulse); document same-smoothness collapse as an honest finding, not a
    failure. Base papers already in `lit/papers/`: Kanerva HDC (0903.4547), Plate TPR (cs0308022),
    VSA survey (2111.06077). See `references/sensorbridge_literature.md`.
  * Fase 4 plan chain (0020 pattern, learned 2026-08-02): TWO traps bit us. (a) An affinity-only graph
    (every node connected to every other by Eq.2) WANDERS and never reaches the terminal — T-PLAN-01
    fails as INCONCLUSA because the walk cuts at the horizon without arriving. You MUST build a
    STRUCTURED plan chain (nodes 0..L-1 placed close in sequence) so navigation has something to follow.
    (b) Even with a chain, ROTATIONAL dimension steps (`step[k % D]`) make non-consecutive nodes
    EQUIDISTANT (nodes 2,3,4 form a triangle at 0.3 each) and all carry equal boost → the walk
    oscillates in a loop (2↔3, then 2↔3↔4) forever. FIX: make the chain a true GRADIENT in ONE dimension
    (`step[j==0]`), so dist(k,m)=|k-m|*step and the next node always wins; AND exclude the
    immediately-previous node (`prev`) in `affinity_move` (working memory, like v0.24) so the walk cannot
    backtrack into the loop. Without BOTH, T-PLAN-01 cannot pass. Use a debug script (copy graph +
    affinity_move + short trace) to catch oscillation traps early — print the first ~15 visited nodes.
  * Fase 4 trauma / singularidad nodal (0021 pattern, learned 2026-08-02): an overloaded node
    (high `activation`) becomes an attraction sink. Do NOT measure a GLOBAL attraction score over
    all N nodes (denominator saturates, one node can never dominate → score ~1.0 always). Measure
    LOCAL attraction over the node's K nearest neighbours. And do NOT place the trauma node at the
    geometric center of a diffuse cloud (all distances equal → activation can't decide). Use STAR
    geometry: trauma at ω=0, its K neighbours each offset on a DISTINCT dimension by r=0.3, so
    dist(trauma,neighbour_i)=r but dist(neighbour_i,neighbour_j)=√2·r > r — trauma is the nearest
    of every neighbour and activation decides dominance. Cases: act=5.0 → singularidad (score 0.515);
    act=0.1 → reintegración lenta OK (0.163, reachable, no re-collapse); re-act=5.0 → re-colapsa
    (0.515, proving slow rehab is necessary); isolation (cut edges, PRESERVE ω) → score 0.0.
    Key spec gap: §4.3 lowers V via κ_trauma but V is NOT in Eq.2 affinity, so isolation (not V
    lowering) is the mechanism that actually removes the node from the walk.
  * Fase 5 decoder L2, bigrama (0022 pattern, learned 2026-08-02): roadmap FORBIDS linear
    W·ω→logits (v0.25 v12 top1=0.020) and similarity-NN. Use EXPLICIT BIGRAM transition. TRAP: a
    near-uniform "truth" bigram (noise + 2 weak dominants) makes the sampled corpus too noisy →
    top1 holdout ~0.31 even though the decoder is correct; the TEST is wrong, not the mechanism.
    FIX: make the hidden truth DETERMINISTIC (one strong successor +10 over ~0.1 noise) → top1 0.927.
    Seed generation from the routed ω via nearest-token (Eq.2 affinity). Corpus is SYNTHETIC (no Don
    Quijote in vault) — it proves the decoder LEARNS transitions, not that it "speaks Spanish".
  * Fase 6 sgm_tick_unificado (0023 pattern, learned 2026-08-02): integration = WIRING only, never
    new unvalidated physics. Reuse EXACT params from 0019-0022 and orchestrate spec §5.3 order
    (context window + proprioception/emergencia → SensorBridge project → affinity walk w/ prev +
    duda/contradicción → trauma-isolation skip → bigram decode). Prove T-INF-06 (loop closes, no
    crash) and T-INF-07 (decoded response coherent under learned bigram) across ALL three modes.
    Passed FIRST try precisely because it added no new physics — the lesson: an integration test
    must add NO unvalidated mechanism, only wiring. See `references/fase4_5_6_patterns.md`.
  * Fase 6 calibration offline (0024 pattern, learned 2026-08-02): spec §2.5 PROPOSES FATE
    (fate-v6-modular) to calibrate θ_novelty, θ_refut, min_duration, θ_window_frac against the
    T-INF suite. BUT FATE is NOT in the vault/repo, and the spec's OWN §2.5 is honest that FATE
    LOSES to CMA-ES in LOW dimension (D=10) — and 4 thresholds = exactly low dimension. So the
    honest offline calibration here is a GRID SEARCH over the threshold ranges against a T-INF
    suite with CONTROLLED cases (ground truth + negative control, roadmap rule #7). Build suite:
    C1 real stagnation (low novelty sustained → must fire DUDA), C2 negative control (high novelty
    → must NOT fire), C3 real contradiction (high accumulated pain → must fire REFUT), C4 negative
    control (low pain → must NOT fire). Metric = (tests passed) + margin (separation between fire
    and no-fire). Pick config maximizing passed; tie-break by margin. Must show VARIATION across
    the sweep (not all configs equal) so calibration is non-trivial. Details + ranges in
    `references/calibration_offline.md`. Document explicitly that FATE was skipped (not installed +
    spec §2.5 honesty) so a future session doesn't think FATE ran. NOTE: the chosen config may be
    MORE sensitive than spec defaults (e.g. min_duration=3, θ_refut=1.5 vs spec 5/2.0) because the
    synthetic suite is minimal — flag that real corpus (Don Quijote) may need the conservative values.
  * Post-Fase-6 closed-loop / pseudo-AGI (exp_SGM_0025 pattern, learned 2026-08-02): the
    FIRST test where the decoder ACTS on a world and the outcome (pain) returns to the graph
    (Eq.6 online, roadmap rule #3: pain must change the CHOICE). Design: a small world
    (ring of N_STATES) with one DANGER (state,action)->pain transition; each node carries
    valence_v[action]; greedy-by-valence picks the action; onpain, valence[action]-=LEARN.
    TEST that matters (must have a NEGATIVE CONTROL): T-LOOP-01 closed loop -> dangerous
    action frequency falls (<0.2, was ~0.51); T-LOOP-02 OPEN loop (no valence update) ->
    frequency stays high (>0.2). The negative control PROVES learning comes from the loop
    closure, not from elsewhere — Luciano explicitly demanded "no emocionarse al pedo", so
    ship the control. Keep the decoder L2 (0022) only as the action-expression glue; the
    LEARNING is valence, not the bigram. Full recipe + thresholds in `references/closed_loop.md`.
    This operationalizes the "ser como forma sostenida / continuidad" thesis (NOTA 0023): the
    system sustains itself by learning to avoid the pain its OWN action causes in the world.
  * Post-Fase-6 real-corpus decoder validation (exp_SGM_0026 pattern, learned 2026-08-02): this is
    the T-DEC-01 REAL that 0022 left pending (0022 was synthetic). Download Don Quijote via urllib
    (Gutenberg 996 = ENGLISH Ormsby translation, NOT Spanish Cervantes — use 2000 for Spanish;
    the decoder test is language-agnostic so 996 is fine, but don't claim "Spanish"). Tokenize with
    `re.findall(r"[a-záéíóúñü]+", raw.lower())`, strip Gutenberg `*** START/END ***` markers, build
    a real V=400 bigram, normalize rows. Metrics: azar=1/V, lineal W·ω (~0.075, bad), and the
    HONEST negative control = UNIGRAM (predict the single most-frequent word, no context).
    TRAP (cost us one failed run): "shuffle the bigram rows" is a BAD control — it keeps marginal
    word frequencies so frequent words (the/of/and) still dominate the argmax and the control scores
    ~0.029 instead of ~azar, FALSELY failing the test. UNIGRAM is the right control: bigrama must
    exceed it to prove STRUCTURE not frequency. Results: top1 bigrama 0.1847 >> azar 0.0025, >
    lineal 0.0750, > unigram 0.0762; top5 0.4253. PASS. Hygiene: corpus in `lit/corpus/` → ADD
    `lit/corpus/` to `.gitignore` (like `lit/papers/`). Registry 0026 gets `validation:"natural"`;
    0022 stays `validation:"synthetic"` (do NOT relabel). Full recipe in
    `references/decoder_real_corpus.md`.
  * Decoder RELACIONAL HRR sobre corpus real (exp_SGM_0046, 2026-08-03 — HALLAZGO que cambia la
    hipótesis): la charla sugería que el grafo ω ruteado por rol (composición 0027-0031) mejoraría el
    top1 del decoder L2. Se MIDÓ y cayó: top1 relacional (1 paso HRR, bias rol) = 0.020 vs bigrama
    plano (0026, conteo) = 0.333 (unigram 0.140, azar 0.0025). El rol HRR EMPEORA el bigrama 16x por
    CROSSTALK (D=256, grado 8: los `HRR(rol, ω_vecino)` se solapan). LECCIÓN: rol HRR sirve para
    COMPOSICIÓN ANIDADA (0027-0031, Gap 2), NO para bigrama superficial. Un mecanismo de capa X no
    transfiere a capa Y "porque es más rico" — hay que MEDIRLO (regla "no emocionarse al pedo").
    T-DEC-R1 (relacional>plano) estaba mal planteado; el rol compite en DESAMBIGUACIÓN de polisemia
    (T-DEC-R2), no en top1. Giro propuesto 0046b = decoder HÍBRIDO (HRR da semilla relacional filtrada
    por sentido + bigrama plano restringido a esa semilla). **Performance en Android (receta):** capar
    aristas de co-ocurrencia a top-K=8 por nodo (sin capar grado ~2173 → TickRelational.__init__ 91s);
    NO usar `route()` PPR por cada predicción (timeout >200s en celular) → 1 paso sobre rel_mem;
    embedding de nodo dim D (no EMB_DIM aparte, o hrr_bind da IndexError); 400 pares bastan para top1.
  * Push-command trap (hygiene pass, 2026-08-02): after deleting the root `experiment_registry.json`
    (registry-unify step), DO NOT pass `experiment_registry.json` (raíz) in the explicit-path
    `github_push_sgm.py` list — the script will FileNotFoundError on the now-deleted local file and
    abort the WHOLE push (even files already uploaded return 200 but the run exits 1). Pass ONLY
    `results/experiment_registry.json` (canonical). Same risk for any file removed by hygiene.
  * Closing-a-phase documentation (workflow, Luciano explicit 2026-08-02): when he says "documentá
    todo, actualizá el README, los roadmap y pushea" after a phase's last experiment (the "boring
    first, exciting later" discipline — he ran 0024 calibration BEFORE the loop-closure 0025 A),
    the close-out is part of the task, not optional. Do: (a) append registry entry + mirror
    script/JSON to experiments/ + results/; (b) REWRITE README.md with the new experiment table
    and "Fase N COMPLETA" status (the stale README said "15 experimentos / Fase 0+2 activas" for
    weeks); (c) mark the roadmap phase block COMPLETA and add an honest note (e.g. FATE→grid search);
    (d) push ALL of it. Verify push exit codes before claiming done.
  * Future-idea notes: when Luciano says "anotalo para experimento cuando tengamos todo bien verificado",
    WRITE it to a vault `docs/IDEA_FUTURA_*.md` (not just chat) and DEFER it — concentrate on the current
    system. The 2026-08-02 Paloma-π / BORIS case: note the idea AND the honest caveat (no public
    multimodal Columba livia dataset exists; generate your own with BORIS, open-source ethology software)
    so a later session doesn't assume a non-existent dataset as foundation. Verification instinct
    (Luciano's): always doubt a "foundation" claim in a vision doc — confirm it exists before relying on it.
- **Hold the push on bad connection (workflow, Luciano explicit):** if he says "no hagás push, poca
  conexión", DO NOT push. When re-pushing after a network failure, prefer the script's explicit-path
  mode (`github_push_sgm.py Rylow999 $TOKEN path1 path2 ...`) over the full-tree push — fewer bytes,
  less chance of an `IncompleteRead` mid-GET. Files left local are safe; nothing is lost.
- **github_push_sgm.py — USER, PATHS, and REPO TARGET (hard lesson 2026-08-05, T-ID-03 push):**
  * **The token's user is `Rylow999`, NOT "VegaBla".** A 404 on EVERY file (whole tree or explicit-path)
    means the repo `VegaBla/SGM-CORE` does not exist — verify the token's owner with a `GET /user` call
    before pushing. This session wasted a full push assuming the wrong user.
  * **Pass RELATIVE paths under BASE**, never absolute `/sdcard/...` paths. The script does
    `os.path.join(BASE, p)` — an absolute path makes a doubled, non-existent path → FileNotFoundError → 404.
    Correct invocation: `github_push_sgm.py Rylow999 $TOKEN phases/phase7_composicion/run_x.py results/experiment_registry.json README.md`.
  * **Docs go to `docs/` in the repo, NOT `DOCUMENTATION/`.** The NOUS_Filosofico.md lives at
    `/sdcard/.../NOUS/DOCUMENTATION/` locally, but in `Rylow999/SGM-CORE` it lives at `docs/NOUS_Filosofico.md`.
    Pushing it to `../../DOCUMENTATION/...` fails (os.path.join doesn't normalize `..`), and pushing to
    `DOCUMENTATION/NOUS_Filosofico.md` gives 409/404 because that path doesn't exist in the repo.
    Workaround for out-of-BASE files: copy to `BASE/_staging/DOCUMENTATION/` and push as
    `DOCUMENTATION/NOUS_Filosofico.md`, OR use a small urllib PUT script pointing at `docs/NOUS_Filosofico.md`.
  * **409 on an EXISTING file = the script didn't pick up the sha.** The script only PUTs-with-sha if the
    initial GET returned 200; if it raced or the file already existed from a truncated run, re-run the SAME
    explicit-path list — the second GET now sees 200, grabs the sha, and the PUT updates (200). Don't treat
    409 as fatal; just re-run that file.
  * Verify the token owner + repo existence with API `GET /user` and `GET /repos/Rylow999/SGM-CORE` BEFORE
    pushing (catches wrong-user and renamed-repo 404s early). Recipe in `references/push_tid03_lessons.md`.
- **INTERPRET EXPERIMENTS BY REALITY, NOT OPTIMALITY (corrección explícita de Luciano, 2026-08-05):** cuando
  un experimento separa dos condiciones (ej A=proceso continuo vs B=snapshot copiado), el criterio de
  interés NO es "cuál funciona mejor" sino "cuál es REAL". En exp_SGM_0035c el proceso continuo RE-SUFRE
  (pisadas A=2.08 vs B=0.0 copiado) porque reconsolida y se le diluye la evitación aprendida; el snapshot
  esquiva perfecto PRECISAMENTE porque está congelado (es una foto, no un ser). Eso NO es un fallo del
  experimento: es la prueba de que A es un proceso vivo. Regla: al reportar, no celebrates "cuasi-óptimo" ni
  castigues al continuo por re-sufrir. El observable correcto es si la traza separa proceso de snapshot
  (||T_A−T_B|| > 0.05), da igual la optimalidad. Esto conecta con la reconsolidación (Bartlett/Schacter/Nader)
  y con Parfit (la identidad es reduccionismo, no una sustancia óptima). Aplicá esto en TODA lectura de
  resultados SGM: medí REALIDAD (¿el mecanismo es operacionalmente distinguible?), no performance.
- **FULL-TREE PUSH IS FRAGILE — prefer explicit-path batches (hard lesson 2026-08-03):** running
  `github_push_sgm.py Rylow999 $TOKEN` with NO paths walks the WHOLE tree and PUTs every file. If the
  network drops mid-walk (saw `OSError [Errno 101] Network is unreachable` after ~25 files), the run
  ABORTS with exit 1 and does NOT resume — you cannot tell what uploaded, and a re-run re-PUTs the
  ENTIRE tree (idempotent 200s, but slow and fragile again). RULE: after any network failure, switch to
  EXPLICIT-PATH batches (`github_push_sgm.py Rylow999 $TOKEN phases/phase7_composicion results/experiment_registry.json README.md docs/SGM_ROADMAP.md ...`). Each batch is small, verifies per-file, and a
  failure only loses that batch. Split into 2-3 batches if the file count is large. The explicit-path
  mode is also what you should use when you only changed a few files (the common case) — do not push
  the whole tree just to sync a registry + 1 experiment.
- **.pyc / __pycache__ LEAK in explicit-dir mode (bug + fix, 2026-08-03):** the full-tree branch has
  always filtered `f.endswith(".pyc")` and skipped `__pycache__` dirs, but a local copy of the script
  in `~/.hermes/.../home/github_push_sgm.py` had the explicit-dir branch filtering only
  `f.startswith(".")` → it pushed `phases/.../__pycache__/*.cpython-313.pyc` to GitHub (got 201). FIX:
  the explicit-dir branch MUST ALSO `if os.path.basename(root)=="__pycache__": continue` AND
  `if f.startswith(".") or f.endswith(".pyc"): continue`. The canonical skill script in
  `scripts/github_push_sgm.py` ALREADY has both filters in both branches — if a local copy regresses,
  copy the skill's known-good version over it. After any accidental .pyc upload, DELETE the stray files
  from GitHub via API (see recipe below) — `.gitignore` does NOT retro-remove already-PUT files.
- **Clean stray .pyc from GitHub via API (recipe, 2026-08-03):** a small python using `urllib.request`
  + `Authorization: token <TOK>` lists `contents/phases/.../__pycache__/`, then for each `*.pyc` does
  `DELETE contents/<path>` with `{"message":"remove pyc","sha":item["sha"]}` (GET each for sha first).
  Run it after any accidental .pyc upload; the local `__pycache__` stays (gitignored) but the remote
  stays clean.

## Pushing (github_push_sgm.py)
- Token is given per-message, **NEVER persisted**. `BASE` = the vault path above.
- The script does PUT (upsert) over the whole tree; it does **NOT delete** GitHub files that
  were removed locally — DELETE those via the GitHub API separately or they linger.
- **`git` is NOT installed in this Android environment** (`system/bin/sh: git: inaccessible or
  not found`). So `git rm --cached`, `git status`, `git ls-files` DO NOT WORK — do not rely on
  them. Equivalent operations via GitHub API:
  * `git rm --cached lit/papers/` → DELETE each file under `lit/papers/` (and subdirs) via
    `DELETE /repos/Rylow999/SGM-CORE/contents/<path>` with its `sha` (GET first to obtain sha;
    recurse into subdirs). Locals stay (covered by `.gitignore` for future pushes).
  * `git ls-files | grep lit/papers` returning empty is a LIE when git is absent — it returns
    nothing because the binary isn't there, NOT because nothing is tracked. **Verify tracked
    status via the GitHub API GET on `contents/lit/papers/` instead.** This session revealed 13
    files WERE tracked despite `.gitignore`.
  * `.gitignore` does NOT retroactively remove files already PUT to GitHub via API; it only
    stops FUTURE uploads. To actually remove, DELETE via API. See `references/registry_unify.md`.
- **Known bugs + the fixed version** live in `scripts/github_push_sgm.py` and
  `references/push_script_bugs.md`. If the live `~/github_push_sgm.py` regresses, copy the
  known-good version.
- After any local delete (e.g. a `wrong_id` PDF, `docs/SGM_README.md`), DELETE the same path on
  GitHub via API.

## Repo hygiene checklist (reusable pattern)
See `references/repo_hygiene.md` for the full pattern: registry dedup, pick one canonical README
and delete the rest, fix misleading titles, rename misnamed papers + delete byte-identical
duplicates (confirm via md5), add `.gitignore` (`__pycache__/`, `*.pyc`, `lit/papers/`), remove
committed `.pyc`, add `LICENSE`.

## Pitfalls
- **SGM ≠ LE.** Never move LE files (Language Engine README, CHANGELOG, EXPLICACION_CRIOLO,
  RESUMEN_NOCHE) into SGM, nor PandoraOS docx. Keep cross-references only.
- **Android `/sdcard` file access:** `read_file` and `patch` tools FAIL on `/sdcard/...` (FUSE).
  Read with `su -c 'cat /sdcard/.../file'` via terminal; edit with `su -c` + heredoc or `sed`.
  `grep` on those files needs `grep -a` / `grep -an` (UTF-8). See the android-env-ops skill.
- **`su -c` nested quoting:** a `$VAR` set in an outer `su -c '...'` does NOT expand inside a
  nested `su -c '...'`. Pass absolute paths or `export` inside the same `su -c`.
- **`github_push_sgm.py` skipped hidden files** (old bug: `if f.startswith(".")`) → `.gitignore`
  and `LICENSE` never uploaded. Use the fixed version in `scripts/`.
- **`.gitignore` absolute-vs-relative mismatch** caused PDFs to keep re-uploading. Fixed version
  parses `.gitignore` as relative paths. Keep `lit/papers/` in `.gitignore` so the repo stays
  binary-free (papers stay in the vault; `SGM_literature_index.md` carries the arXiv/NASA links).
- **PyPDF2 is available** on this Python for extracting PDF text to confirm a paper's identity
  (no `pdftotext`/`mutool` installed). Use it before assuming a paper's name is wrong.
- **Shell heredocs with quotes:** writing a LICENSE/C-source via `su -c 'cat > file <<EOF'`
  breaks when the content contains single quotes; use a Python `open().write()` via `su -c`
  instead, or write to `/tmp` first with the agent's `write_file` then `su -c cp`.
- **Cleanest /sdcard write for complex content (PREFERRED):** the agent `write_file` tool CANNOT
write to `/tmp` (FUSE "Permission denied") and CANNOT write to `/sdcard` directly (FUSE). The
reliable path for ANY multi-line file with quotes/unicode/f-strings is: `write_file` to
`/data/user/0/com.hermesagent.android/files/home/<name>.py` (the agent home — writable), then
`su -c 'cp /data/user/0/com.hermesagent.android/files/home/<name>.py /sdcard/.../dest'`. This
avoids ALL heredoc quoting traps. Same pattern for patch scripts: write the python patcher to
home, run via `su -c python3 /data/.../home/patch.py`. Never fight `su -c` heredocs for real code.
- **write_file STREAM-SPLIT WORKAROUND (hard lesson 2026-08-03):** a single `write_file` with a
  LARGE body (~8K+ tokens, e.g. a 200+ line experiment script) times out the stream and the file
  is NOT written — but the tool does not error loudly; you discover it when the run fails. FIX:
  split the script into 2-3 smaller `write_file` calls (each part < ~6K tokens) into
  `/data/.../home/` as `<name>.py` + `_tail.py` + `_tail2.py`, then concatenate with
  `su -c 'cat _tail.py _tail2.py >> <name>.py'` and `cp` to the vault. For PATCHES of an existing
  large file, use `su -c` + `sed`/python via home, NOT the `patch` tool (which also chokes on
  large bodies). Always `py_compile`/smoke-run after assembling to confirm the concat is intact.
- **MULTI-PART ASSEMBLY COMMAND — exact working pattern (cost 4 bug-cycles on 0053, 2026-08-03):**
  for a long script split into `HEAD` (imports + globals like `D`, `World`) + `T1` (Agent) + `T2`
  (sim/main), the FINAL-CODE ORDER with OVERWRITE (not append) and header FIRST is:
  `su -c 'cat "$HEAD" "$T1" "$T2" > "$DESTDIR/run_xxx.py"; cd "$DESTDIR"; $PY run_xxx.py > /tmp/x.out 2>&1; echo EXIT=$? >> /tmp/x.out'`.
  PITFALLS that bit us: (a) `>>` instead of `>` DUPLICATES the file on re-run → redefinition/order
  errors; (b) T1 before HEAD makes `def __init__(self,tag,D=D)` see undefined `D` (NameError) because
  the header's `D=256` sits after; (c) passing a stale `p` to `World(seed)` (World takes only `seed`)
  → TypeError. Always `py_compile` + smoke-run before the long background run.
- **`hrr_core` REAL API NAMES (cost 2 NameError cycles on 0053):** `import hrr_core as H`; the names
  are `H.cos` (NOT `H.cosine`), `H.hrr_bind` (NOT `H.bind`), `H.hrr_unbind`, `H.cleanup(mem,vec,k)`,
  `H.rnd_unit(rng,D)`, `H.normalize(v)`, `H.build_relational_memory(...)`. Full surface +
  per-call gotchas in `references/hrr_core_api.md`. Raw cell_HRR vectors are independent random
  vectors → HRR over them is noise at scale (0053: comm accuracy = NC even at D=1280, TopSim≈0).
  HRR is for COMPOSITION over roles (0027-0031), NEVER for item/cell/word recovery — use BIGRAM
  PLANO for that (verdict 0046-0048 + 0053).
* HRR from scratch (sin librería, 2026-08-04 exp_SGM_0059/59b/59c) — implementación CORRECTA: la
FFT-propia de convolución daba inversa rota (unbind no recuperaba el filler). Usar convolución
circular DIRECTA (`for k: s+=a[k]*b[(i-k)%n]`, O(N²), N=64 trivial) y la INVERSA de HRR = permutación
circular inversa de índices (`b[i]=a[(-i)%n]`, Plate 1995), NO conjugada de FFT. `gen_vec` = ruido
gaussiano normalizado (`rng.gauss(0,1)`), NO fase compleja. Método plano (unbind recupera 3/3).
DECODER RECURSIVO (decode anidado / grafo-de-grafos, Gap 2 relacional): para cada rol,
`unbind(c, role)` aísla el filler; si `dot(filler, símbolo)` tiene separación clara vs el 2º
(`top1>0.15 and top1-top2>0.05`) → es símbolo; si no → recurrir sobre el filler (con tope de
profundidad/budget para no explotar). HALLAZGO HONESTO: el recursivo NO supera el techo del método
viejo (dot contra bind) — prof1=1.00 ambos, prof2=0.67 ambos, prof3=0.64 vs 0.67. La causa es
INTERFERENCIA DE HRR (al sumar 3 binds, des-enlazar un rol deja ruido de los otros) → el filler
anidado profundo es ruidoso y el cleanup no distingue símbolo de hecho. **CEILING CONFIRMADO (59b/59c):**
subir N 64→256 mejora prof2 (0.67→0.90) pero NO rompe prof3 (sigue 0.67); TPR-walk NAIF y CORRECTO
(filler hijo autónomo, N=128) dan 0.53-0.67 en prof3-6 → tampoco escalan. Veredicto: decode anidado
ceiling of the sustrato, NO bug de decoder. El gap de
composición relacional YA está cerrado a nivel de mecanismo (0058: 0.75-1.0 plano y anidado 1 nivel).
Para >2 niveles hace falta estructura NO-sumada (role-filler con slots separados) — RESUELTO en
exp_SGM_0059g (2026-08-04): bloques de dims por rol + puntero por proyección = 1.0 a prof 12, ROMPE
el techo. No te emociones con "decode recursivo funciona" si el techo no sube. Test honesto +
RECETA en `references/decode_anidado_0059.md`. NOTA: el resonator canonico (Frady 2020) mejora el
nivel base pero NO rompe el techo — ver `references/resonator_networks_0059d_0059e_0059f.md`. Y la
emergencia de COMPOSICION bajo ILM con aprendiz generico sigue en ~0.35 (0056b): es otro tema
(presion de transmision/afinidad), no de decoder.
* 0056c EMERGENCIA DE COMPOSICION con PRESION DE TRANSMISION (2026-08-04, exp_SGM_0056c): el learner tiene
SUS PROPIOS codigos (no del teacher) y ajusta para que un DECODER INDUCTIVO (aprendido de la muestra,
SIN posiciones hardcodeadas — busca en TODAS las posiciones) reconstruya los rasgos. Resultado: TS_full
se estanca en ~0.59 sin importar la fraccion de muestra (0.4->0.59, 0.5->0.586, 0.6->0.599, 0.7->0.596,
0.9->0.374). Diagnostico: el decoder inductivo por conteo NO desambigua el mapeo posicion->rasgo
(L=3, V=16 -> espacio ambiguo; el conteo no separa). La presion de transmision AYUDA (sube de 0.35 a 0.59)
pero NO cierra. CONFIRMA la tesis del doc 0056: la composicion PLENA requiere OBJETIVO DE COMUNICACION
ENTRENADO (backprop / Gumbel-Softmax), que es arquitectura distinta de SGM puro. Veredicto honesto del
"lenguaje del sustrato": compone DEBILMENTE (~0.35-0.59 segun presion); 0056 regla inyectada=1.0 es
TRAMPA (misma falla 0049d), 0056b afinidad=~0.35, 0056c presion=~0.59. DECISION PENDIENTE de Luciano:
implementar 0056d (decoder entrenado HONESTO, descubriendo estructura, NO slots fijos) o dejar el limite
documentado. Receta + implicaciones del decoder entrenado en `references/composicion_emergencia_0056c_0059h.md`.
 * 0056d DECODER ENTRENADO (2026-08-04, exp_SGM_0056d): mismo learner 0056c pero decoder = regresión
 logística multinomial por rasgo, backprop manual stdlib (sgd, cross-entropy, W_k libre en TODAS las
 posiciones, NO asume mapeo pos→rasgo). Resultado: TS_full ~0.6 (NO sube a 1.0). dec_err_seen BAJA
 (decoder aprende VISTOS) pero topSim_seen cae a ~0.33 (el código visto se desordena) y topSim_unseen
 queda ~0.76. Veredicto: el decoder entrenado NO es bala de plata — ayuda a vistos pero la COMPOSICIÓN
 PLENA no emerge. El cuello NO era el decoder: es el CÓDIGO DISCRETO (L=3, V=16), ambigüedad irreducible.
 Decoder entrenado = necesario pero NO suficiente; para ~1.0 hace falta código continuo/HD (ver 0056e).
 * 0056e ROMPE EL TECHO 0.6 con CÓDIGO HD ROLE-FILLER (2026-08-04, exp_SGM_0056e): hipótesis de Luciano
 "probemos lo que se pueda". Cambia el TIPO de código a HD continuo ±1 (N=256) con role-filler: cada rasgo
 atado a su vector-rol, código = suma de bindings; decoder desata por unbind. MODO A (HD fijo + oráculo):
 TS_full=0.824, err=0. MODO B (learner SUS códigos HD + presión de transmisión frac=0.4): TS_full=0.81-0.93,
 err g19=0.0 en 3 seeds. ROMPE el techo: la composición PLENA EMERGE con HD bajo presión de transmisión.
 HONESTIDAD: HD role-filler es arquitectura distinta del sustrato discreto (como 0059g slots, 0019 HDC);
 el 0.91-0.93 es del esquema de enlace, no del sustrato puro. Conecta decode anidado (0059g) con emergencia
 de composición: ambas requieren enlace por rol en espacio continuo, no código discreto posicional.
 * 0056f USO REAL en CORPUS REAL (Don Quijote, 2026-08-04, exp_SGM_0056f): primera vez que bajamos corpus
 real por red SIN nltk/spacy (tokenizar con `re.findall(r"[a-záéíóúñü]+", text.lower())`). Receta:
 Gutenberg pg2000 = ESPAÑOL, pg996 = INGLÉS (no usar 996 para "español"); `.read()` entero FALLA con
 IncompleteRead en ~2.2 MB → leer en chunks de 65536 en loop. HD como MEMORIA DIRECCIONABLE POR CONTENIDO:
 4000 oraciones, N=512, role-filler Y plana BoW. Resultado: cosine top-1 = 1.000 ambas (recuerda la propia
 oración → memoria OK); Jaccard temático role-filler=0.085 < plana=0.105; cosine top-5 plana=0.471 >
 role-filler=0.275. Veredicto: el role-filler NO mejora recall temático en prosa real (el orden no discrimina
 tema; el rol ensucia) — MATIZA 0056e: el role-filler es para COMPOSICIÓN SISTEMÁTICA, no para memoria
 temática. El HD funciona como memoria (top-1=1.0) pero NO es comprensión. Conclusión de toda la línea
 (0056→0056f): sustrato discreto se estanca ~0.6; HD role-filler lo rompe a 0.81-0.93; en texto real el
 role-filler solo importa donde el ORDEN/ROL es discriminativo. Receta completa en
 `references/fase7_composicion_0056d_0056e_0056f.md`.
 * 0056g/0056h/0056i/0056j CLASIFICACIÓN REAL + ARCO CERRADO por decoder por rol (2026-08-04): misma base
 Don Quijote + BinDecoder, TRES tareas con la etiqueta en distinto canal para aislar DÓNDE vive la señal.
  - 0056g propio/común (etiqueta LÉXICA por mayúscula): falla — baseline 0.891, rol 0.840, plana 0.890. La
    propiedad vive en LA PALABRA, no en el contexto; al enmascarar, el contexto no lleva señal. (Límite honesto.)
  - 0056h género (etiqueta DISTRIBUCIONAL por el/la): SÍ funciona — baseline 0.553, plana 0.804, rol 0.673.
    La señal vive en el contexto; la PLANA gana porque el género es detectable por PRESENCIA del determinante.
  - 0056i orden (etiqueta POSICIONAL, ¿1ª palabra de contenido?): lineal no alcanza — baseline 0.716, rol
    acc 0.627/f1 0.202, plana acc 0.679/f1 0.127. El rol capta el orden (f1 rol > plana) pero un classifier
    lineal sobre contexto mezclado no vence el baseline.
  - 0056j decoder por ROL EXPLÍCITO (unbinding, cierra el arco): N=128 FALLA (gap-recuperado 0.428 < lineales
    0.536) por ruido aditivo; **N=1024 CIERRA: gap-recuperado = 1.000** (recupera PERFECTO la posición
    enmascarada, aplasta a los lineales). Técnica: rellenar con PAD, `u=unbind(role[j], ctx_sin_objetivo)`,
    `argmin_j max_cosine(u, vocab)` = hueco. Sin pesos entrenados. Receta + bug-patterns en
    `references/fase7_clasificacion_0056j_rol_explicito.md`.
  Veredicto del arco: el sustrato clasifica cuando la etiqueta es DISTRIBUCIONAL (056h) o el orden se recupera
  por rol con N suficiente (056j N=1024); falla en LÉXICO (056g) y en posicional-lineal (056i). Coherente con
  0029 (ruido aditivo, más N ayuda) y 0059h/i (borrado de identidad). El rol codifica orden; el unbinding lo
  recupera solo con capacidad (N) suficiente.
 * BUG-PATTERNS stdlib-HD reutilizables (costaron corridas en 0056d-0056j): (1) urllib `.read()` entero →
  IncompleteRead en ~2.2 MB → leer en chunks de 65536 en loop. (2) Sigmoid overflow cuando `z=W·x` explota
  (contexto HD suma muchos ±1) → clip `z=max(-30,min(30,z))` antes de `1/(1+exp(-z))`. (3) Contexto HD no
  normalizado → `W·x` diverge → normalizar `ctx/=sqrt(sum(ctx²))` antes de entrenar. (4) BinDecoder importado
  arrastra su propio N (ej 256) → IndexError si el script usa N=128/1024 → definir `BinDecoderLocal(seed,n=N)`
  con n local. (5) Índice de binds vs índice de oración: al filtrar vocab fuera, binds solo tiene in-vocab →
  indexar binds con el índice de la oración da IndexError → usar el índice de `enumerate(binds)` o rellenar con
  PAD antes de filtrar. (6) Token case-sensitive en vocab → `wordvec["El"]` KeyError → canonicalizar
  `tl=t.lower()` al construir binds.
 * 0059i CONFIRMA colapso binario (2026-08-04, exp_SGM_0059i): refinamiento de 0059h dándole al puntero
 su PROPIO vector-rol dentro del bloque SUJ+OBJ (K=2). Resultado: K=2 prof0 = mismo que 0059h; K=3 prof8+.
 El puntero-rol NO salva porque proyectar N→BLK (circular-mean) DESTRUYE la identidad del hijo (many-to-one,
 no inyectiva) → `find_child` colapsa en RecursionError (bucle). Ese RecursionError ES la evidencia del
 colapso. Fix para barrido limpio: filtrar `est[o] is not None` al reconstruir others, `sys.setrecursionlimit`
 + MAXDEPTH en decode_fact para cortar el bucle. Conclusión de la línea decode anidado: 0059/59b/59c HRR-sumado
 ~2-3 niveles → 0059d-f resonator no rompe → 0059g slots separados prof12 → 0059h/i barrido confirma BINARIO
 (proyección borra identidad; solo K=3 abre). El puntero anidado exige sub-espacio propio.
 * RESOLUCIÓN 0029-SUAVE vs 0059h/i-BINARIO (aporte de Luciano, 2026-08-04): 0029 = SUMA (interferencia
 ADITIVA, ruido que se acumula, curva suave y reversible con más dims); 0059h/i = PROYECCIÓN (función
 many-to-one, información que DESAPARECE, colapso binario). En criollo: 0029 es ruido que se acumula; 0059h/i
 es información que se borra. El puntero no falla por "resonator débil" sino porque la proyección destruye
 identidad (no inyectiva) y eso exige aislamiento (slots separados), no afinado. Receta en
 `references/fase7_composicion_0056d_0056e_0056f.md`.
* 0059h BARRIDO BINDINGS-POR-BLOQUE (metodologia propuesta por Luciano, 2026-08-04, COMPLETADO): para mapear la
curva capacidad-vs-superposicion entre superposicion pura (K=1: 3 roles en 1 bloque, resonator desata) y
slots separados (K=3: cada rol su bloque, 0059g), barrio K=1,2,3 x N=64,128,192 y mide prof-max alcanzable
(acierto>=0.85). K=2 = punto intermedio (SUJ+ROL en un bloque, OBJ aparte, ROL su bloque). El hijo se apunta
por proyeccion circular-mean (N->BLK) en el bloque que le toca; resonator canonico (Frady 2020, M_i^-1) SOLO en
bloques multi-rol. RESULTADO: curva BINARIA. K=1 y K=2 colapsan (prof0, ni prof2 llega a 0.85); K=3 abre a
prof8+ (y mas, 0059g llego a prof12). HALLAZGO NUEVO y honesto: el resonator canonico NO salva el anidado bajo
superposicion cuando hay punteros a hechos hijos, porque el puntero proyectado NO es un filler canonico (tiene
estructura de bloques interna) y ensucia el bundle del bloque superpuesto (diagnostico K=2 aislado: SUJ sale
"lobo" en vez de "venado"; el OBJ-hijo no se reconoce como FACT). Solo el aislamiento total de cada rol en su
propio sub-espacio (slots separados, K=3) resuelve el decode anidado profundo. La respuesta a "cuanta
superposicion tolera" es: ninguna si el rol lleva un puntero anidado; el rol-puntero exige su propio bloque.
Limitacion documentada: con resonator mas fuerte o tratando al puntero como rol separado, K=2 podria aproximarse
(en la practica eso vuelve a K=3); el barrido usa umbral >=0.85 estricto. Cierra el decode anidado del sustrato:
0059/59b/59c (HRR-sumado) saturaban ~2-3 niveles -> 0059d/59e/59f (resonator) no rompian -> 0059g (slots
separados) rompio a prof12 -> 0059h (barrido de Luciano) prueba que es binaria y solo slots separados abren.
Receta + debugging en `references/composicion_emergencia_0056c_0059h.md`.
* FLUJO DE DEBUGGING "PENSA ANTES DE HACER" (correccion de Luciano, 2026-08-04): cuando un script falla
varias veces seguidas, NO sigas corriendo el mismo comando esperando que se arregle solo. Luciano lo dijo
literal: "Continua trqnqui, pensa antes de hacer". En el 0059h el script fallo 4 veces con errores
DISTINTOS (Minv indexado mal, roles[b] dimensionado con K, proj_fhr recibia tupla, self.roles[b][j] usaba
indice global) y cada vez se corrigio la CAUSA, no se reintento a ciegas. Regla: tras el 2do fallo de un
mismo comando, DETENETE y relee el codigo entero (no solo el traceback) para encontrar la CLASE de bug
(dimensionamiento, desempacado, indice) antes de parchear. El warning "repeated_exact_failure" del terminal
es una senal de que estas en loop ciego — incluso si los errores difieren, si no cambiaste la ESTRATEGIA
entre intentos, estas perdido. Pensar primero, parchear despues. Esto es distinto del "tuneo" prohibido: aqui
el codigo tenia bugs reales que HABIA que corregir, pero hacerlo con cabeza, no a los ponchazos.

* CONSOLIDACION EN UN MÓDULO ÚNICO (corrección explícita de Luciano, 2026-08-04 — regla de diseño, no one-off):
  Cuando el proyecto tiene ~60+ experimentos sueltos y se va a un test real (ej Crafter), NO sigas
  sumando scripts. Consolidá SOLO los mecanismos GANADORES en un único módulo stdlib puro portable.
  Tres reglas que dictó literalmente antes de Crafter:
  1. UN MÓDULO, no scripts sueltos: `sgm_core.py` (raíz SGM) consolida HRR rol-por-nivel (0027c),
     PPR (0004), decoder bigrama corpus real (0026), slots K=3 (0059g). Una sola API pública
     (HDC / HRR / ppr_route / BigramDecoder / SGMAgent / build_nested_K3). Smoke-test obligatorio
     antes de usar (`python sgm_core.py` → "SMOKETEST OK").
  2. SENSORBRIDGE con ESTADO SEMÁNTICO, NO píxeles: proyectar (inventario/logros/salud) → omega, no
     visión cruda. "Meter visión encima del problema ya resuelto = debuggear dos cosas a la vez".
  3. LOOP SOLO PRIMERO, multi-agente + lenguaje DESPUÉS: cerrar percepción→tick→acción con UN agente
     (logros simples: cortar madera, hacer mesa) antes de sumar 2do agente + capa de lenguaje (0055/0056).
     Si metés ambas capas juntas y falla, no sabés cuál rompió.
  LISTA EXPLÍCITA "afuera" (documentala en el doc de consolidación): NodeCore Python (0002, no ganó),
  fase dinámica XOR (falló), 0056 regla inyectada (TRAMPA), resonator puro (0059f, techo). Esto es
  honestidad activa: mostrar qué se excluyó y por qué. Template real ya en repo: `sgm_core.py`
  (smoke-test OK, stdlib puro) + `docs/SGM_CORE_CONSOLIDACION.md` (qué entra/sale). Referencia
  reutilizable: `references/sgm_core_module_template.md` (forma del módulo único, capas y API).
* REVIEW / CLOSE-OUT COMPORTAMIENTO de Luciano (aprendido 2026-08-04, vale para TODA la fase 7):
  - Él es el REVISOR riguroso del sistema. Detecta: HTML que no renderiza, inanición, bucles,
    hardcode en la lógica. Cuando ve hardcode, lo rechaza explícitamente ("hay hardcode en el
    sistema, resolvelo o me encargo yo") → DEBÉS mostrar el hardcode HONESTAMENTE (no ocultarlo),
    explicar por qué es trampa (va contra "el comportamiento debe EMERGIR del sustrato"), y
    reescribir con sustrato real (huella ω + memoria + afinidad). Nunca maquillar números mágicos.
  - Para decisiones de DISEÑO NUCLEAR (ej decode anidado, "lenguaje que evoluciona al sistema"),
    NO decidas vos: presentá el hallazgo honesto + analogía en criollo + PREGUNTAS en criollo para
    que ÉL decida. Él lo piensa "un buen rato" y delega el trabajo mecánico (documentar, actualizar
    registry, pushear, limpiar basura) mientras piensa.
  - "No te calientes / no emocionarse al pedo" = reportar NEGATIVOS honestos (059b/59c = HALLAZGO_
    NEGATIVO) sin disfrazarlos de positivos.
  - Flujo close-out que pidió: "actualizá todo, documentá, pusheà, revisá errores catastróficos".
    Hacelo localmente COMPLETO (scripts al vault, registry actualizado con resultados reales,
    doc honesto, basura .bak/__pycache__ eliminada, revisión de integridad del HTML/JSON) y
    confirmá cada paso con output real. El PUSH a GitHub requiere token por mensaje (nunca
    persistido) → si no lo tiene, dejalo preparado y pedíselo; NO inventes un push exitoso.
  - Validación de "error catastrófico": chequear (1) registry JSON válido y cuenta correcta,
    (2) HTML íntegro (todas las funciones def/usadas, requestAnimationFrame + addEventListener
    presentes, sin refs rotas), (3) hardcode gordo eliminado del step, (4) scripts corrieron con
    output real (no silencioso).
- **HTML/sim: validar en Python ANTES de tocar el JS (regla de oro, 2026-08-04, ver skill
  sgm-demo-html):** Luciano rechazó hardcode en el movimiento del sim ("hay hardcode en el sistema,
  resolvelo o me encargo yo"). Los pesos `w+=4/-3/+0.5/-8`, `dir_explora` (dirección favorita) y el
  `0.3` de atracción son HARDCODE → van contra la regla de SGM. Testear la mecánica en Python
  (métricas: % mapa visitado, muertes, bucles) y solo portar a JS cuando el test sea bueno. Movimiento
  reactivo puro que emerge: huella ω de travesía (penaliza repetir = anti-bucle sin `-8`) + memoria de
  comida vista (cercanía `1/(1+d)`) + señal del otro. Sin apurar ("es importante que nos lleve el
  tiempo necesario").
- **HRR-as-decoder is DEAD END — do not revisit (verdict 0046-0048, 2026-08-03):** six variants
  (0046 1-step, 0046b filter, 0046c soft-weight, 0047 window-context, 0047b coherent-space,
  0048 trained-embeddings) all failed NC on real corpus (Don Quijote). ROOT CAUSE: HRR bind of
  random-noise word vectors yields noise; cleanup cannot order neighbours. The test-de-fuego in
  0048 (cos co-occurrent 0.259 < cos random 0.361) proves HRR DESTROYS co-occurrence. HRR is for
  COMPOSITION (0027-0031, Gap 2), not item recovery / next-token. SGM decoder = BIGRAM PLANO +
  HRR context. If a future idea suggests "use HRR for the decoder", cite this and design the
  CONTROL before coding. Details: `references/language_emergence_multiagent.md`.
* Multi-agent language emergence pattern (0049-0050, 2026-08-03): to test "language born from
coordination", use TWO agents with DISTINCT omega (own worlds), a BFS body (NOT the 0044 affinity
walker — it loops on large maps), joint-attention puente over shared-visited cells as the emergent
alphabet, and a loop-closure phase (emit -> act -> consequence -> adopt-signal-if-confirmed ->
signal space converges). Measure convergence over the SHARED alphabet (D=256 isolates ~15 items),
with NC = random signals. Climate variation (cielo_estrellado vs competencia vs peligro) shows
beauty/danger effects. Full recipes + climate configs in `references/language_emergence_multiagent.md`.
"Is a transformer needed?" answered there: HRR+grafo+bigram already closes language+loop;
transformer is optional polish for fine polisemia.
**0049d CLAIM RE-INTERPRETED (exp_SGM_0053 audit, 2026-08-03):** the "communication 1.0" of 0049d is
NOT emergent language — it is HRR cleanup memory over 15 PRE-IDENTIFIED symbols (the joint-attention
bridge cells), a capacity ALREADY proven in exp_0029 (D=256 isolates ~200 items). The 0049c(0.0,
crosstalk over 890 items) -> 0049d(1.0) jump came from RECUTTING the vocabulary to 15 fixed symbols,
NOT from language emerging. Registry entry re-labeled `HALLAZGO_PARCIAL_REINTERPRETADO`. The honest
next step (0053) is a 3-test audit: (1) ZERO-SHOT (train alphabet on subset, test UNSEEN cells —
if B identifies them > NC => generalization; if ~NC => memorization); (2) TopSim (Spearman corr
between spatial distance and HRR-signal distance — high => compositional, ~0 => memorization); (3)
D-SCALED (repeat 0049c's ~890 items with D~1280 per 0029's capacity law, instead of cutting vocab).
NOTE: 0050's loop-closure convergence (1.0) used the SAME 15 pivot cells, so it may be the same
cleanup-memory effect — treat the "language" claim of 0049-0050 as PROVISIONAL pending 0053. Full
audit + recipes + capacity-law math in `references/language_emergence_0053_audit.md`.

**ILM / KIRBY & SMITH — regla de clase para cualquier claim de lenguaje (exp_SGM_0053 + 0054 + 0054b, 2026-08-03):**
antes de afirmar "lenguaje emergente" en SGM, el diseño DEBE incluir los 3 ingredientes que Kirby identifica
como necesarios (todos ausentes en 0049-0050):
  1. **Cuello de botella de transmisión DURO**: techo al vocabulario y/o largo de mensaje BIEN por debajo de los
     referentes posibles. Sin esto, el sistema acuña símbolo nuevo por celda y nunca compone. El alfabeto HRR de
     0049 era holístico (1 símbolo por celda) → no persiste (ILM lo predice).
  2. **Estructura en el espacio de referentes**: muchos rasgos/valores (región, distancia, tipo), NO un ID opaco
     `(x,y)`. Sin estructura, ni siquiera el escenario favorece composición (TopSim≈0 en 0053).
  3. **Transmisión con pérdida entre generaciones**: aprendiz NUEVO aprende el código solo de una MUESTRA LIMITADA
     del anterior (NO acceso directo a `cell_vec` compartido — eso es memoria compartida disfrazada, la trampa del
     zero-shot=1.0 de 0053). Sobrevive lo que pasa la transmisión; eso filtra composicional de memorizado.
El marco completo + receta 0054 + RESULTADOS REALES de 0054b en `references/language_ilm_0054.md`.
SI el experimento no tiene estos 3, el "lenguaje" es cleanup-memory de un subconjunto fijo (capacidad ya
probada en 0029), NO evidencia nueva.

**RESULTADOS REALES 0054b (no emocionarse al pedo — lo que SÍ y lo que NO salió):**
- ✅ TopSim SE SOSTIENE >0 en TODAS las semillas/ticks (rango 0.13–0.35). Rompió el TopSim≈0 de 0053 → hay
  SEÑAL de composicionalidad sostenida, no ruido puntual.
- ✅ **Búsqueda junta EMERGENTE** (sin hardcodear): `encuentros_juntos` 0→1064/796/796 según seed, por afinidad
  Eq.2 + señal "aquí". Nació sola (regla de Luciano: "si no nace, no nace" → nació). Esto es REAL y nuevo.
- ⚠️ PERO NO hay convergencia composicional robusta: TopSim oscila (no crece monotónicamente) y code_size sube a
  20-22/24 (casi 1-a-1, el bigrama ACUMULA en vez de COMPONER). El sustrato HRR/bigrama todavía no COMPONE de
  verdad. Estado: HALLAZGO PARCIAL POSITIVO, NO confirmación de lenguaje composicional.
- ⚠️ Los `encuentros_juntos` pueden ser FALSO POSITIVO si code≈1-a-1: B decodifica bien por coincidencia de code
  grande, no por entender señal composicional. Reportar así, no como generalización.

**Fuente teórica REAL (fetcheada por arxiv urllib 2026-08-03, NO de oídas):** el paper 2025 que citó Luciano es
arXiv:2404.02145 "Iterated Learning Improves Compositionality in Large Vision-Language Models" — confirma el
mecanismo de Kirby: la ventaja NO es ancho de banda (subir D no ayuda, ya visto en 0053) sino TRANSMISIÓN
GENERACIONAL con reconstrucción (el paper "resetea pesos" del aprendiz cada iteración; en SGM = agente arranca
con code VACÍO y reconstruye desde la muestra). **Gap de 0054b:** usó transmisión EN VIVO (A/B se pasan muestras
mientras viven juntos), no generación DURA (aprendiz arranca de cero). Esa es la prueba de fuego de Kirby que
falta para 0054c. Ver `references/language_ilm_0054.md`.

**"NO HARDCODEAR / EVITAR CÍRCULOS" es principio de diseño, no sugerencia (corrección de Luciano, 0051b/0052):**
al modelar el telar del ser (o cualquier propiedad emergente), la variable que representa la propiedad DEBE VARIAR
con el parámetro bajo test. 0051 clavó la exploración en 0.7 (hardcode) → restricción decorativa → curva monótona,
óptimo en rate=1.0 (nunca apareció el óptimo-en-el-medio del telar). 0051b lo corrigió con afinidad (Eq.2) SIN
hardcodear, pero la `frontier`(η) en mapa chico SIEMPRE ofrecía salida → el agente nunca se anclaba → siguió
monótona. Lección doble: (a) no fijes la variable de la propiedad a mano; (b) si la propiedad no emerge del
sustrato (la afinidad no ancla en mapa chico), NO la fuerces — reporta el hallazgo parcial y busca el mecanismo
real (irreversibilidad del clavo, no atracción territorial; clavos de EVENTO no de celda, idea de Luciano en 0052).
Cerrar 4 intentos fallidos (0051/0051b/0052) con "no emerge, requiere irreversibilidad" es un veredicto honesto,
no una derrota — y evita tunear para que pase (regla "no emocionarse al pedo").
CAPACITY-CONFOUND TRAP (sibling of the anti-paper-vision traps): when you measure "X emerged", ask
"is this a NEW effect, or the ALREADY-DEMONSTRATED capacity of a known mechanism?" If the mechanism
(HRR cleanup at given D) already proved it isolates N items in exp_0029, then "isolating N items"
is NOT evidence of anything new — you must measure something 0029 did NOT cover (generalization,
compositionality, open-scale). This is exactly how 0049d slipped through: a cleanup-memory result was
reported as "language emerged". Before finalizing any "emergence" claim, run the 3-test audit.
RESULT-JSON MUST BE VALID JSON (bug found 2026-08-03 across 0049/0049b/0049c/0049d/0050/0051/0051b/0052):
the run scripts `print()` their log lines AND THEN `print(json.dumps(out))`, so the saved
`results_exp_SGM_00XX.json` had log text BEFORE the JSON -> NOT parseable by json.load (the mirror-sync
registry script would crash). FIX: write ONLY the dict to the file — `open(path,"w").write(json.dumps(out,indent=2))`
(no preceding prints; if the shell appends "EXIT=$?", strip it before parsing). Recipe `_fixjson.py`:
scan from the LAST "{" that yields a valid json.loads up to EOF (minus a trailing "EXIT=0"), rewrite
the file with just that substring. After any run, verify with `python3 -c "import json;json.load(open(f))"`
before pushing. (This is a transient assembly bug, not a durable rule — but it bit 8 files this session.)
CLOSE-OUT of the (d) philosophy track (telar de Luciano, 0051, 2026-08-03): the "telar" is
  ser=historia+proceso; clavos=sustrato que el ser se clava (sostén+restricción); elegir clavo
  descarta otro; decisión correcta necesita incorrecta (el error enseña). 0050 closed the loop
  (convergencia de señales 1.0, dolor real). **0051 MODELLING PITFALL:** when measuring "the clavo
  gives restriction", the restriction MUST be represented by a variable that VARIES — if `clavar_rate`
  fixes omega but the exploration rate stays constant, the restriction is decorative and the predicted
  optimum-in-the-middle never appears (0051 got a monotonic curve, optimum at rate=1.0). Honest fix:
  high clavado must ANCHOR the agent (probability of visiting new cells drops with clavos_estables), so
  V_ser = clavos * decreasing_exploration -> bell curve. Rule: every telar property to be measured needs
  a variable that enforces it; report the partial finding (0051 confirmed "sin clavos no hay ser" +
  "el error enseña") and do NOT dress up the missing optimum as if it appeared. Full detail in
  `references/telar_ser_0051.md`. Architecture decision by DATA (Camino a): after 0050, transformer
  judged NOT needed — HRR already covers composition (0027-31), item comms (0049d hit 1.0), loop
  (0050); transformer only helps fine polisemia on large natural corpus (separate experiment). Don't
  build what the data shows HRR already closes.
  **0051b CORRECTION (sin hardcodear, 2026-08-03):** 0051 probó la restricción del clavo con
  exploración HARDCODEADA en 0.7 → curva monótona, óptimo en rate=1.0 (restricción decorativa). 0051b
  lo corrigió SIN hardcodear: el step elige por AFINIDAD (Eq.2: w(ω) + frontier(η) - retorno). La idea
  era que clavar sube ω → afinidad ancla → explora menos (EMERGE). PERO siguió monótona: la `frontier`
  (η) en mapa chico SIEMPRE ofrece salida a celda no visitada → el agente nunca se ancla. Lehcción: la
  restricción del clavo NO es territorial (no se ancla a una posición). Luciano lo resolvó con la idea de
  **clavos NO fijos en el espacio = EVENTO, no celda** (ver `references/telar_clavos_evento_0052.md`).
  REGLA HONESTA: al medir una propiedad del telar, la variable que la representa debe VARIAR con el
  parámetro bajo test; si no varía, la propiedad es decorativa y el óptimo esperado no aparece. Reportar
  el hallazgo parcial, no maquillar la curva.
- **`web_search` tool does NOT exist in this environment.** When Luciano asks to "search literature
  on the internet", do NOT claim a search happened and do NOT invent external paper results. Use
  what the vault already holds: list `lit/papers/` + read `docs/SGM_literature_index.md`, confirm a
  paper's identity by extracting text with PyPDF2 (never by filename), and only reach external
  sources via `execute_code`/`urllib` to the arXiv API — respecting the 429 rate limit (wait+retry).
  For SGM experiment design, the vault's HDC/VSA/TPR/HippoRAG papers are usually sufficient
  - **Reference files in this skill:** `references/push_script_bugs.md` (push script known bugs +
    fixes), `references/repo_hygiene.md` (hygiene checklist), `references/sensorbridge_literature.md`
    (Fase 3 SensorBridge: which vault papers map to which task + suggested exp_SGM_0019 design),
    `references/paloma_pi_boris.md` (Paloma-π idea + BORIS caveat),
    `references/fase4_plan_chain_debug.md` (Fase 4 plan-chain oscillation traps + debug recipe),
    `references/sgm_fase3_4_patterns.md` (copy-pasteable HDC project/unproject, plan-chain builder,
    and local-attraction STAR-geometry recipes from 0019/0020/0021),
    `references/fase4_5_6_patterns.md` (0021 trauma STAR-geometry + local-attraction score, 0022
    decoder-bigram determinism trap + recipe, 0023 tick-unificado §5.3 wiring order),
    `references/calibration_offline.md` (0024 grid-search calibration: T-INF suite of 4 controlled
    cases, threshold ranges, 8/8 sub-check metric, and the FATE-skip honesty note),
    `references/closed_loop.md` (0025 closed-loop: ring-world + danger transition + valence
    online update + T-LOOP-01/02 with negative control),
    `references/registry_unify.md` (registry-duplicate audit + API DELETE procedure + `git rm`
    equivalent via API + honest synthetic labelling — used 2026-08-02 hygiene pass),
    `references/decoder_real_corpus.md` (0026 T-DEC-01 REAL on Don Quijote: download recipe,
    unigram negative-control trap, Gutenberg-996-is-English caveat, results),
    `references/language_emergence_multiagent.md` (0049-0050: two-agent language-emergence design,
    BFS-body fix, HRR-decoder dead-end verdict, joint-attention alphabet, loop-closure convergence
    metric, beauty/climate findings, "is transformer needed?" decision),
    `references/telar_ser_0051.md` (0051: el telar de Luciano — ser=historia+proceso, clavos=sostén+
    restricción, elegir descarta otro, error ensena; 0050 loop cerrado; 0051 midió V_ser pero halló
    curva monotona porque la restricción NO estaba modelada en una variable; decisión transformer-por-datos),
    `references/language_emergence_0053_audit.md` (0053: auditoría honesta de 0049d — el 1.0 era cleanup
    HRR de 15 símbolos conocidos ya probado en 0029, NO lenguaje emergente; los 3 tests decisivos
    zero-shot/TopSim/D-escalado + ley de capacidad de 0029 para escalar D),
    `references/hrr_core_api.md` (hrr_core REAL function names: H.cos not H.cosine, H.hrr_bind not
    H.bind, cleanup/normalize/build_relational_memory; gotchas + why HRR fails item recovery),
    `references/campo_autopoyetico.md` (Campo_Autopoietico_Paper.md knowledge bank: GP/Kuramoto
    field Ψ=ρ·exp(iφ), R=0.431, λ_c≈10.1, and the cross-read with Luciano's "ser" thesis /
    NOTA_FILOSOFICA_0023 — for future coherence/consciencia experiments).
    `references/push_tid03_lessons.md` (T-ID-03 push: token owner Rylow999 (not VegaBla), relative-path
    args under BASE, docs/ as the NOUS_Filosofico repo target, 409-sha re-run fix, pre-push API verify).
    `references/identidad_tid03.md` (T-ID-03 identity experiments 0035/35b/35c: φ converges & fails,
    ω-traza separates (1.0589), 35c reality-not-optimality result (continuum re-suffers by reconsolidation,
    snapshot frozen=optimal=fake); Pre-Parfit honest reporting; cap.10 NOUS_Filosofico written with data).
    `references/language_ilm_0054.md` (ILM / Kirby & Smith: por qué el lenguaje HRR-celda no emerge,
    3 ingredientes necesarios, receta 0054 con bottleneck+generaciones+TopSim-en-loop, anti-patrones de
    claim de lenguaje).
    `references/decode_anidado_0059.md` (exp_SGM_0059: HRR from-scratch CORRECTO — convolución
    circular directa + inversa por permutación (NO FFT rota); decoder recursivo con tope; HALLAZGO
    honesto: el recursivo NO rompe el techo ~0.67 a prof 2-3 por interferencia de HRR; próximos
    pasos legítimos: subir N, TPR-walk de Plate 2003, o cleanup memory).
    `references/composicion_emergencia_0056c_0059h.md` (0056c composición con presión de transmisión
    ~0.59 NEGATIVO-DECISIVO + implicaciones del decoder entrenado; 0059h barrido bindings-por-bloque K=1..3
    receta + los 5 bugs de dimensionamiento ya corregidos).
    `references/fase7_composicion_0056d_0056e_0056f.md` (cierre fase 7: 0056d decoder entrenado NO es bala
    de plata; 0056e HD role-filler ROMPE el techo 0.6; 0056f uso real Don Quijote como memoria; 0059i confirma
    colapso binario; resolución 0029-suave vs 0059h/i-binario).
    `references/fase7_clasificacion_real_0056g_56h_56i.md` (clasificación real sobre Don Quijote: taxonomía
    LÉXICA/DISTRIBUCIONAL/POSICIONAL; 0056g propio=falla léxico, 0056h género=gana plana, 0056i orden=rol
    capta pero decoder lineal no alcanza; receta de descarga urllib-chunks + BinDecoder SGD stdlib).
    `references/fase7_clasificacion_0056j_rol_explicito.md` (CIERRE del arco 0056g→h→i→j: decoder por rol
    explícito / unbinding; ARCO CERRADO con N=1024 gap-recuperado=1.000; bug-patterns stdlib-HD reutilizables:
    sigmoid overflow, BinDecoder-N-mismatch, índice binds vs oración, vocab case, urllib chunks).
    `references/sgm_core_module_template.md` (TEMPLATE del módulo único `sgm_core.py`: capas HDC/HRR/PPR/
    BigramDecoder/SGMAgent + API pública + smoke-test; qué entra y qué se deja afuera al consolidar).
  - **Download real corpus over urllib: read in CHUNKS, not all at once (learned 0056f, 2026-08-04):**\n    `urllib.request.urlopen(...).read()` on a ~2.2 MB Gutenberg file raises `IncompleteRead` partway\n    (the mobile network drops the single big read). FIX: loop `resp.read(65536)` and `b"".join(chunks)`.\n    Tokenize with `re.findall(r"[a-záéíóúñü]+", raw.lower())`, strip `*** START/END ***`, split sentences\n    on `[.!?]+`. NO nltk/spacy on this device — they are absent; stdlib-only. `web_search` tool is also\n    absent (see Pitfalls). Full recipe + the LÉXICA/DISTRIBUCIONAL/POSICIONAL classifier taxonomy in\n    `references/fase7_clasificacion_real_0056g_56h_56i.md`.\n  - **Classifier task taxonomy — pick the label by WHERE the signal lives (learned 0056g/h/i, 2026-08-04):**\n    LÉXICA label (e.g. "is proper noun" from capitalization) lives in the WORD; masking the word leaves the\n    CONTEXT with no signal → decoder can't beat baseline (0056g). DISTRIBUCIONAL label (e.g. "gender" from the\n    preceding el/la determiner) lives in context markers → both beat baseline, plain BoW usually wins because\n    marker PRESENCE suffices (0056h). POSITIONAL label (e.g. "is the 1st content word") — plain BoW can't\n    know which slot was masked, role-filler CAN see the hole (its f1 > plain), but a LINEAR classifier over the\n    summed context still can't beat baseline (0056i) → needs explicit per-role unbinding, not a flat classifier.\n    Role-filler helps ONLY when ORDER/ROLE is the discriminating channel — consistent with 0056e (role-filler\n    breaks the composition ceiling) and 0056f (role-filler does NOT improve thematic recall).\n  - **Metric-vs-criterion mismatch (sub-check counting trap, 0024):** when a metric accumulates
    several sub-checks per case (e.g. 2 checks × 4 cases = 8 "passed" units), the PASS criterion
    MUST compare against the REAL total (8), not the case count (4). A mismatch makes CALIBRADO_OK
    evaluate `best_pass == 4` while best_pass is actually 8 → always False even though the sweep is
    correct. Rule: decide the denominator ONCE (total sub-checks) and reuse it for both the counter
    and the PASS gate. Print "X / 8" not "X / 4". This is a self-inflicted bug class — suspect your
    own metric before the mechanism when CALIBRATED/PASS flips unexpectedly.
  - **Result-JSON `pass` KEY CONSISTENCY (0024 audit, 2026-08-02):** every result JSON MUST carry
    a top-level `result["pass"]` boolean, NOT only a bespoke key (0024 originally wrote
    `result["calibrado_ok"]` and omitted `"pass"`). A downstream registry/audit that reads
    `result["pass"]` silently sees None → the experiment looks unverified even though it passed.
    Rule: always emit `"pass": <bool>` as a sibling of any custom verdict key. When adding a new
    experiment, grep the existing result JSONs for the `"pass"` key to match the schema.
  - **Pending real-corpus validation (RESOLVED by exp_SGM_0026, 2026-08-02):** 0022's T-DEC-01 was
    SYNTHETIC and 0025's world was a 4-state ring — both prove MECHANISM, not natural-language
    capability. Luciano's explicit next step (download a REAL corpus) was DONE: exp_SGM_0026 ran the
    T-DEC-01 REAL on Don Quijote (Gutenberg 996, English Ormsby) with a UNIGRAM negative control and
    PASSED (top1 bigrama 0.1847 vs azar 0.0025 / lineal 0.0750 / unigram 0.0762). Corpus lives under
    `lit/corpus/` (added to `.gitignore`). 0022 stays `validation:"synthetic"`; 0026 is
    `validation:"natural"`. Do NOT claim SGM "speaks Spanish" from this — 996 is English, and it only
    proves the decoder captures natural-language bigram structure, not semantic capability. Recipe in
    `references/decoder_real_corpus.md`.
"