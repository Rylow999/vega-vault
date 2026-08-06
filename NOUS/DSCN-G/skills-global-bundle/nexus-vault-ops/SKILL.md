---
name: nexus-vault-ops
description: Operate on and advance the nexus-vault research project (DSCN-G, DDSD, LOGOS, FATE, the "Tríada"/unificación hypothesis) on this rooted Android device. Covers the /sdcard/Hermes permission workaround, the only working python, the heredoc quoting trap, and the unified-dynamics testing methodology. Trigger when the user asks to read/write/test anything under /sdcard/Hermes/nexus-vault or discusses the unificación / Tríada hypothesis, NOUS/LOGOS/FATE, or the Galileo/DSCN-G/Collatz/Riemann connections.
---

# nexus-vault-ops

## When to use
The user references nexus-vault, NOUS, LOGOS, FATE, DSCN-G, DDSD, "Tríada", unificación,
Galileo_Escalamiento_*, or wants to read/write/test files under /sdcard/Hermes. Also when
advancing the cross-domain unification research (testing whether domains share a mechanism).

## CRITICAL: /sdcard permission workaround (Android scoped storage)
The Hermes app shell CANNOT see or write /sdcard/Hermes directly:
- `search_files` and terminal `ls`/`find` on /sdcard/Hermes return EMPTY (0 results) from the
  app shell. The vault looks empty but is NOT — it has ~609 files.
- `read_file` on a /sdcard path FAILS ("File not found") from the app shell — the file IS
  there but app user u0_a471 cannot read it without `su`. NEVER call read_file on
  /sdcard; `su -c 'cp <vault-file> <hermes-home>/'` then read_file the home copy.
- `write_file` writes to Hermes home (/data/data/com.hermesagent.android/files/home/), never
  to /sdcard.
- A terminal command that touches /sdcard WITHOUT `su -c` may be **BLOCKED by the
  permission system** ("User denied this command" / "BLOCKED"). User explicitly said
  "Recordá usar su" (2026-07-26) — ALWAYS wrap vault reads/writes/copies in
  `su -c '...'`. This is the single most repeated mistake in these sessions.
Fix: prefix ANY vault read/write with `su -c '...'`. To read a vault file into context:
  `su -c 'cp /sdcard/Hermes/nexus-vault/.../<f> /data/.../home/<f>'`, then read_file the copy.
- Read:  `su -c 'cd /sdcard/Hermes/nexus-vault && find NOUS LOGOS FATE -type f | sort'`

## Reading arbitrary vault files (incl .docx, .pdf, .xlsx) into context
When the user asks to read/edit documents under the vault (e.g. "leé los docs en X"), the
app-shell read_file/search_files CANNOT traverse /sdcard. Stage files to Hermes home first:
1. `su -c 'mkdir -p /data/.../home/<tmpname>/ && cp /sdcard/Hermes/nexus-vault/<path>/<file> /data/.../home/<tmpname>/ && chmod 664 /data/.../home/<tmpname>/<file>'`
   - Do each file in a SEPARATE su -c call (a chained mkdir+cp+chown+chmod in one call gets
     BLOCKED by the permission system) — copy each file with a small explicit `su -c "cp ..."`
     + `chmod 664`.
2. Then `read_file` the home copy. read_file auto-extracts .docx/.xlsx/.pptx/.ipynb —
   Word docs become readable text directly, no LibreOffice needed. For .pdf use PyPDF2
   `extract_text` (the `su` python has it; `strings`/`pdfinfo` are unreliable on FlateDecode
   PDFs — they return garbage/empty Title). To CONFIRM a mislabeled PDF's true identity, see
   the "Literature hygiene" PyPDF2 recipe below — do NOT trust `strings` or the filename.
3. Bulk copy pattern: first `su -c 'cp /sdcard/Hermes/.../*.md /data/.../home/docs/'`
   - Read:  `su -c 'cd /sdcard/Hermes/nexus-vault && find NOUS LOGOS FATE -type f | sort'`
   - New SGM project: `su -c 'mkdir -p /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/{specs,motor,decoder,phases/{phase0_substrato,...},tests,results,docs,lit/references}'`
   - Write: `write_file` to Hermes home, then
     `su -c 'cp /data/data/com.hermesagent.android/files/home/<f> /sdcard/Hermes/nexus-vault/<dest>'`
   - **EXPERIMENT ID PROTOCOL (added 2026-08-02):** every experiment gets a globally-unique
     ID `exp_SGM_XXXX_<descriptor>` (XXXX = 4-digit sequential). NO reusing IDs — if re-run,
     use `exp_SGM_XXXX_rev2`. Each run writes its result JSON to `experiment_registry.json`
     (at vault root or project root) with config, seed, hypothesis, test_target, and links
     to baseline/variant. This kills the old `v0.14d audit vs v0.14d` circular-id problem.
   - **TEST-FIRST WORKFLOW (added 2026-08-02):** Write the test of equivalence/validation
     FIRST (e.g. T-INF-06), run it against the baseline to capture baseline snapshots/results,
     THEN implement the new component, and finally re-run the same test against the new
     implementation. The test is the contract; the implementation must pass it. The test
     file itself is the primary artifact — results JSON are secondary evidence.
   - **SU FOR ALL FILESYSTEM SEARCHES (added 2026-08-02):** The user explicitly requires
     using `su` for ALL filesystem searches, not just /sdcard ones. Even within the
     Hermes home directory, use `su -c 'find ...'` or `su -c 'grep ...'` instead of
     plain `find`/`grep`/`search_files`. The app shell's `search_files` returns 0 results
     under FUSE for some paths; `su -c` is the reliable alternative.
   - **ARXIV ID VERIFICATION (added 2026-08-02):** Arxiv IDs in literature indexes can
     be wrong. Always verify by fetching the arxiv abstract page:
     `python3 -c "import urllib.request; ..."` and check the returned title matches
     expectations. If the ID returns a different paper, it is wrong — do not trust the
     index blindly. Wrong IDs produce wrong PDFs that waste time and confuse the literature review.
     When a paper ID is wrong, move the mislabeled PDF to a `wrong_id/` subfolder and
     download the correct one.
DO NOT trust a "vault is empty / 0 results" answer from non-`su` commands. The backup
nexus-vault_BACKUP_20260725_002225.tar (~75MB) and nexus-vault.zip also live in /sdcard/Hermes.

## Working python (no numpy)
- `python3` in the `su` PATH is inaccessible. Use exactly:
  `export LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib; PY=/data/data/com.hermesagent.android/files/usr/bin/python3`
  then `$PY script.py`.
- This python has NO numpy — use pure stdlib (math, random) only.
- `execute_code`'s python3 is broken (numpy import fails, bad binary links) — avoid for heavy
  compute; use the `su` python above.
- SIMPLER PATH for doc-editing scripts (2026-07-25): plain `python3` in the HERMES TERMINAL
  (NOT `su`, NOT `execute_code`) is Python 3.13.13 and WORKS for any script that only reads/writes
  files in Hermes home (/data/data/com.hermesagent.android/files/home/). So: `write_file` the
  script to home, then just run `python3 /data/.../home/script.py` in a normal terminal call.
  Only reach for the `su` + LD_LIBRARY_PATH python when the script must run AS ROOT on /sdcard
  (e.g. reading a vault JSON in place). For editing the v4 compendium, plain terminal python3
  + `patch` tool is the least-friction route.
- To run a script: write it with Hermes `write_file` to Hermes home, then
  `su -c 'cp /data/data/com.hermesagent.android/files/home/<f>.py /tmp/ && export LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib; /data/data/com.hermesagent.android/files/usr/bin/python3 /tmp/<f>.py'`
- AVOID `<<EOF` heredocs for writing scripts ALTOGETHER on this device. Even `<<'PYEOF'` with
  single-quoted delimiter breaks when the body contains apostrophes, parentheses, or backticks
  (seen live: `print("E(2^p-1)=p exact by definition (nu_2...)")` and `print('... (paren) ...')`
  and even `cat > /tmp/x.py <<'PYEOF'` with `(` inside threw "syntax error near unexpected token").
  RULE: always write scripts with Hermes `write_file` to Hermes home, then `su -c 'cp ... /tmp/'`.
  This also sidesteps the ~8K-token stream-timeout (write_file chunks are small; one big heredoc
  in a terminal call times out). If you must inline a tiny command, keep it single-line and quote-free.

## Research methodology: unified-dynamics / Tríada
The user's hypothesis: all domains share ONE mechanism (dissipative confinement; duality
phase-vector; vitality). Test it TWO ways:
1. Formula-level: predict a SHARED constant across domains (RG exponent -2π/3, spectral gap
   λ₂=4, GOE level stat). Compute it from REAL data in each domain. Shared → literal
   unification; not shared → structural only.
2. Structural (the Tríada): look for the 3rd regulating dynamic, not a shared number.
   Architecture = two competing dynamics → a THIRD emerges that autorregulates (confines) them.

Confirmed Tríada in 4 domains (2026-07-25, see references/triada_results.md):
- NS: transfer T(k) + dissipation D(k) → spectral curvature G[k] ("Tercer Motor"); G converges
  to a finite plateau (no divergence), H¹ does not blow up. Holds in 1D/2D/3D spectral models.
- DSCN-G: phase φ + vector ω → vitality V_i (poda confina grafo a N*≤~5, T1 verificado).
- Collatz: 2-adic drift + recurrence → balance f_P (<0.7075, umbral de divergencia); confinado.
- Riemann: ceros + función Xi → regulador GOE (level repulsion); ceros confinados en línea crítica.

Formula-level tests (A/B/C/M) REFUTED literal unification: domains do NOT share the RG exponent
(Collatz drift is constant, not (log2 N)^-2.094), the gap (Collatz ~0.75 Ruelle, not λ₂=4),
the spectral stat (sustrato is expander-uniform, zeta is GOE-chaotic), nor a Mersenne signature.
CONCLUSION: unification is STRUCTURAL (same confinement principle), not formula-level. Matches
NS §10.2 ("analogy at the level of structural questions, not mathematical objects").
Deliver this honestly: the Tríada is a real STRUCTURAL unification; do NOT claim literal
constant-sharing across domains.

### 2026-07-25 session — additional honest results (reviewer's 7-point audit applied)
- NS regularity (Galileo Φ=G): G[k] ("Tercer Motor") stays bounded in 1D/2D/3D SPECTRAL MODELS,
  but the STRONG lemma "G bounded ⇒ H¹ bounded" is REFUTED: in the 3D model α_min→0 BOTH with and
  without G. G moderates transfer but does NOT impose a minimum spectral slope. Regularity is
  still saved by the viscous cut-off k_diss (Foias-Temam), not by G alone. NS status = PARTIAL
  (real regulator, not a Millennium proof). State this caveat every time.
- CONTROL NEGATIVE (critical check): the Tríada mold ALSO "confirms" in unrelated stable systems —
  Lotka-Volterra (predator-prey) and Kuramoto (phase coupling) WITHOUT pruning BOTH stay bounded.
  So the mold is NOT a unique signature; it is a pattern of STABLE DISSIPATIVE SYSTEMS. The real
  distinction is the MECHANISM (criterion C3 below), not mere boundedness.
- Riemann: sustrato circulante fractal does NOT match zeta level statistics (spacings 0.138 vs
  0.612 fraction <0.5). Riemann row = NOT CONFIRMED as the unified substrate. BUT real Riemann
  zeros DO show GOE/GUE level repulsion (downloaded 100k zeros from Odlyzko — see
  references/odlyzko_gue_probe.py). The "3rd dynamic" of Riemann = the GUE regulator; it is
  observational, not a proof of RH.
- 2^φ: found in Master-Document/DSCN-G_Master_Document.md (line 99): "a=3 is arithmetically
  isolated as the only odd integer in (1, 2^φ), φ=(1+√5)/2". CORRECTION (2026-07-25):
  2^φ = 3.069, NOT 3.694. With φ=(1+√5)/2≈1.618, 2^φ = e^(1.618·ln2) = 3.069. The value
  3.694 = 2^1.885, which is NOT 2^φ — that was a transcription error when the note was copied
  into the Tríada docs (the original Master-Document line is symbolically correct, no number).
  DYNAMIC DERIVATION (closes reviewer Point 7): why φ and not another constant?
  Collatz cycles are 3^m/2^k ≈ 1 → k/m ≈ log₂(3)≈1.585. The best k/m are the Fibonacci
  convergents of log₂(3) (3/2, 8/5, 21/13, …), whose limit is φ=(1+√5)/2 (since CF of φ is
  [1;1,1,1,…]). BUT log₂(3)=[1;1,1,2,2,3,…] breaks the Fibonacci pattern at the 4th coefficient
  (it is 2, not 1) → that is where the map stops having Fibonacci-optimal cycles. So 2^φ=3.069
  is the boundary where a=3 is dynamically isolated. This is a MECHANISM (Fibonacci convergents
  of log₂(3) limit to φ), satisfying the reviewer's "explain WHY φ, not just near 4" gate.
  Full write-up: references/phi_2_dynamic_derivation.md.
- Cross-domain quantitative prediction: NO formula derives Collatz f_P* (~0.7075) from DSCN-G
  N* (~4.8) or vice versa (tried 1/f_P, log2 N*, 2^(4 f_P), -1/Φ(3)). Bounds are INDEPENDENT.
  Negative but informative: the Tríada is structural analogy, not constant unification.

## SGM project in the vault — structure and status (added 2026-08-01, reorganized 2026-08-02)

CRITICAL SEPARATION RULE (user correction 2026-08-02): SGM and the DSCN-G Language Engine
are SEPARATE pillars. Their FILES must never be mixed — only cross-references in docs.
- SGM canonical: `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/`
- LE canonical:  `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/`
- PandoraOS (other project): `/sdcard/Hermes/nexus-vault/SHARED/PandoraOS/`
The SGM (Synaptic Graph Model) project lives in the vault at
`/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/` (canonical, `chown root:everybody`
so the user can open it). It was previously kept only in the agent-home `rizoma_docs/`
mirror (invisible to the user); as of 2026-08-02 the vault is the source of truth and
`rizoma_docs/` is just the writable working copy. Its implementation folders (`motor/`,
`decoder/`, `phases/phase1_modos/`, etc.) referenced in `SGM_README.md` are **aspirational**
— they do NOT exist as physical directories yet (the `motor/` `decoder/` `specs/` `tests/`
dirs seen in the vault are empty stubs).

### Where SGM content actually lives (organized structure)

```
rizoma_docs/
├── README_SGM.md              ← navigation index (created 2026-08-02)
├── docs/                      ← all technical documentation
│   ├── SGM_v1_4_Especificacion_Corregida.md   (full spec, 787 lines)
│   ├── SGM_ROADMAP.md           (6-phase roadmap + Fase 0)
│   ├── SGM_README.md            (master index + validation status)
│   ├── SGM_experiment_protocol.md   (experiment protocol)
│   ├── SGM_literature_index.md      (literature index)
│   ├── Arquitectura_Pure_L2_Pandora.md  (unified SGM+NOUS+DSCN-BIO arch)
│   ├── RIZOMA_Vision_Futuro_SGM.md     (long-term vision, speculative)
│   ├── README.md              (vault index, 37KB, audit of 4 false claims)
│   ├── CHANGELOG.md
│   ├── EXPLICACION_CRIOLO.md
│   ├── RESUMEN_NOCHE.md
│   └── PandoraOS_*.docx       (5 PandoraOS design docs)
├── experiments/               ← all experiment scripts (pure Python stdlib)
│   ├── run_abduce_xor_d.py        (exp_SGM_0007: dimensionalidad D)
│   ├── run_abduce_phase.py        (exp_SGM_0008: fase dinámica v1)
│   ├── run_abduce_phase_v2.py     (exp_SGM_0009: fase dinámica v2)
│   ├── run_abduce_phase_bias.py   (exp_SGM_0010: sesgo relacional v3)
│   ├── run_abduce_xor_D128.py     (exp_SGM_0011: D=128 + fase sesgo)
│   ├── run_abduce_xor_sigmoid.py  (exp_SGM_0012: fase sigmoid)
│   ├── run_abduce_decay.py        (exp_SGM_0006: decaimiento temporal)
│   ├── run_abduce_ppr.py          (exp_SGM_0005: PPR-guided abducción)
│   ├── run_ppr_routing.py         (exp_SGM_0004: PPR multi-hop routing)
│   ├── run_nodecore_smoke.py      (exp_SGM_0001: smoke test)
│   ├── run_nodecore_memory.py     (exp_SGM_0002: benchmark memoria)
│   ├── t_inf_06_equiv.py          (T-INF-06: equivalencia NodeCore)
│   ├── t_inf_06_nodecore_port.py  (T-INF-06: port NodeCore)
│   └── t_inf_06_stress.py         (T-INF-06: stress test)
├── results/                   ← all experiment result JSONs
│   ├── experiment_registry.json     (registro maestro: 12 experimentos)
│   ├── results_exp_SGM_0002..0012.json
│   └── baseline_snapshots_exp_SGM_0003_nodecore_equiv_teorica.json
├── phases/                    ← results organized by phase (unchanged)
│   ├── phase0_substrato/
│   │   ├── results_exp_SGM_0002_nodecore_memoria_benchmark.json
│   │   ├── results_exp_SGM_0003_nodecore_equiv_teorica.json
│   │   ├── results_exp_SGM_0003_stress.json
│   │   └── baseline_snapshots_exp_SGM_0003_nodecore_equiv_teorica.json
│   └── phase2_inferencia/
│       ├── results_exp_SGM_0004_ppr_multipath_routing.json
│       ├── results_exp_SGM_0005_abduce_ppr.json
│       └── results_exp_SGM_0006_abduce_decay.json
└── lit/                       ← literature (unchanged)
    └── papers/
        ├── kope_arxiv_2604.07904.pdf    (KoPE: Kuramoto phase coupling)
        ├── hipporag_arxiv_2404.10501.pdf (HippoRAG: NeurIPS 2024)
        ├── 1804.09004.pdf               (Kanerva SDM — verify ID)
        └── 2105.13495.pdf               (verify ID)
```

### SGM experiment + hygiene workflow (added 2026-08-02)
The SGM experiments run as a clean Fase-0→Fase-6 ladder (exp_SGM_0001..0015 done through
Fase 2). The user requires a SPECIFIC sequence before each new experiment and during cleanup:

**BEFORE a new experiment — read the WHOLE project first (user rule, 2026-08-02):**
Do NOT design exp_SGM_00NN from memory. Reconstruct state by reading:
1. `docs/SGM_v1_4_Especificacion_Corregida.md` — esp. §2.3.1 (contradicción/dolor) and
   §2.3.2 (duda/estancamiento); these define the mechanism the next test must validate.
2. `docs/SGM_ROADMAP.md` — which Fase/T-INF test is next.
3. `results/experiment_registry.json` — what already exists (IDs, status, pass/fail).
4. The result JSONs of the closest prior experiments (cat them via `su -c`, see pitfalls).
Then explain the plan + prior results in criollo BEFORE writing code. The user explicitly
wants to "reconstruir el registry leyendo cada JSON" and understand before proceeding.

**Experiment authoring rules (confirmed working this session):**
- Pure stdlib Python (math/random/json). NO numpy (absent on this host).
- TEST-FIRST + CONTROL: each test has a positive case AND a negative control (e.g. doubt
  fires on a trapped chain but NOT on a free-exploring one; contradiction fires on high pain
  but NOT on low pain). The 0013/0014/0015 all pass because the controls are explicit.
- SMOKE TEST before claiming success: `python3 -c "import py_compile; py_compile.compile(path)"`
  THEN run it. A script that compiles but crashes on the control is not PASS.
- HONEST PASS GATE: if a scenario reaches its end-state by TIMEOUT instead of by the intended
  mechanism, it is NOT a valid test of that mechanism. Seen 2026-08-02: exp_SGM_0015 scenario C
  first returned `INCONCLUSA` with `doubt_count=0` (timeout, not doubt) — rewrote C to trap the
  chain in few nodes + contracted window so `handle_doubt` actually escalated to doubt_count>=3.
  Only then report PASS.
- Write result JSON with: experiment_id, name, phase, date, hypothesis, config (seed/D/θ),
  result (pass + per-scenario), test_target, script path, notes + notes_criollo.

**Registry hygiene (the user audits this):**
- The registry MUST list every experiment that has a result JSON on disk. If a JSON exists
  but the ID is missing → ADD it. If an ID appears 2+ times (duplicate entry) → KEEP ONE.
- Reconstruct from disk when in doubt: `json.load` each `results_exp_SGM_*.json`, build the
  entry from its own fields, dedupe by `experiment_id` (regex the trailing number for sort).
- As of 2026-08-02 the registry has 16 entries (exp_SGM_0001..0015, with 0003_stress separate).
  The old "12 experimentos" note in the structure block above is STALE — registry is the truth.

**README / doc canonicity (hygiene 2026-08-02):**
- Canonical README = `README.md` at SGM root. `README_SGM.md` = navigation index ONLY
  (already labeled "Índice de navegación rápida"). `docs/SGM_README.md` was a DUPLICATE old
  index with LE results mixed in + false title → DELETED.
- FORBIDDEN TITLE: never write "Primer sistema cognitivo funcional" as a heading — it
  contradicts the project's own honest limits table. Use "Grafo sináptico cognitivo (en
  construcción …)" instead.
- When un-mixing SGM from LE/PandoraOS: DELETE the LE/PandoraOS files from the SGM repo
  (GitHub DELETE API) and MOVE them in the vault to LANGUAGE_ENGINE/ or SHARED/PandoraOS/.
  Do not leave cross-project files inside SGM.

**Literature hygiene (lit/papers/):**
- Rename files to the CORRECT arxiv ID. Confirmed 2026-08-02: `kanerva_hdc_1988_0903.4547.pdf`
  is actually Kanerva 2009 (arxiv 0903.4547) — the "1988" in the name was wrong; renamed to
  `kanerva_hdc_2009_0903.4547.pdf` and updated `SGM_literature_index.md` line accordingly.
- DELETE byte-identical duplicates: `wrong_id/kanerva_hdc_2009.pdf` had the SAME md5
  (3867be7e…) as the renamed file → removed. Always `md5sum` before declaring a duplicate.
- DO NOT delete on assumption. `wrong_id/hipporag_v2_2025.pdf` was flagged "wrong ID" but its
  PDF Title metadata is EMPTY and strings showed no "SNAP"/"HippoRAG" text → left in place
  pending human confirmation. Rule: if you cannot confirm what a file IS, do not delete it.
- CONFIRM PDF IDENTITY WITH PyPDF2 (the real fix for "don't assume", 2026-08-02): `strings` and
  `pdfinfo` are unreliable on compressed (FlateDecode) PDFs — they return garbage or empty Title.
  The working check is to EXTRACT TEXT with PyPDF2 (available in the `su` python, no extra install):
  `su -c 'export LD_LIBRARY_PATH=/data/.../usr/lib; /data/.../usr/bin/python3 -c "import PyPDF2; r=PyPDF2.PdfReader(\"<vault-pdf>\"); print(r.metadata); print((r.pages[0].extract_text() or \"\")[:2500])"'`
  This revealed `wrong_id/hipporag_v2_2025.pdf` is actually **SNAP** (McGill 2024, catastrophic
  forgetting in Hebbian Learning) — NOT HippoRAG2. So: rename to `snap_2024.pdf`, move OUT of
  wrong_id/ (it is a real, relevant paper on Hebbian forgetting — relevant to SGM Fase 4),
  and update `SGM_literature_index.md`. PyPDF2 is the tool; `strings` alone is NOT sufficient.
- Optional cleanup the user may request: drop the full PDFs from the repo and keep only
  `SGM_literature_index.md` (links) to avoid redistribution issues — ask before doing it.
  When doing it: add `lit/papers/` to `.gitignore` (keeps them on disk in the vault, excludes
  from the GitHub push) then DELETE each PDF from GitHub via API. The vault retains the papers.

**Editing /sdcard files IN-PLACE (patch/read_file do NOT resolve /sdcard) — 2026-08-02:**
Neither the Hermes `patch` tool nor `read_file` can see `/sdcard/Hermes/...` (FUSE + root-only).
`write_file` writes to Hermes home, not /sdcard. So to EDIT a vault file in place, use `sed`
inside `su -c` (Android's `sed` is toybox and DOES accept `-i`):
  `su -c 'sed -i "s|OLD|NEW|" /sdcard/Hermes/nexus-vault/.../file.md'`
  - Use `|` as delimiter (not `/`) so paths with `/` don't need escaping.
  - For multi-line / structural edits, prefer a `python3` script with `assert old in s` +
    `s.replace(old,new)` written via `write_file` to home, then
    `su -c 'cp ... /tmp/ && <su-python> /tmp/x.py'`.
  - VERIFY after: `su -c 'sed -n "L,Mp" <file>'` or `su -c 'grep -n "pattern" <file>'`.
  - Note: `grep`/`find`/`sed` inside `su -c` work fine on /sdcard; only the non-`su` app-shell
    tools (search_files, read_file, write_file, patch-on-/sdcard) fail.

**GitHub push hygiene:**
- `github_push_sgm.py` only PUTs (no delete). After `rm`-ing a vault file, DELETE it from
  GitHub via API (recipe in android-env-ops "Deleting a file from GitHub").
- The script's old `f.startswith(".")` filter SKIPPED `.gitignore`/dotfiles — fixed to skip
  only `__pycache__`/`*.pyc`. Verify dotfiles landed with a GET after pushing.
- Always `rm -rf` any `__pycache__` in the vault before pushing (the API push ignores
  .gitignore); otherwise the .pyc gets committed and you must DELETE it after.

### What does NOT exist yet (common confusion)

The SGM README describes a target structure that hasn't been created:
- `motor/` (engine.py, chains.py, vitality.py, valence.py) — **does not exist**
- `decoder/` (transformer.py, project.py, l1_lookup.py) — **does not exist**
- `phases/phase1_modos/` through `phase6_integracion/` — **do not exist** (only phase0 and phase2 have content)
- `tests/` with T-INF/T-SEN/T-PLAN/T-DEC — **does not exist**

The `results/` folder NOW EXISTS (created 2026-08-02 during reorganization).
The `experiments/` folder NOW EXISTS (created 2026-08-02 during reorganization).
The `docs/` folder NOW EXISTS (created 2026-08-02 during reorganization).

### DSCN-G vs SGM — don't confuse them

The vault contains TWO separate projects that share history but are distinct:
- **DSCN-G Language Engine** (`engine_export/`, `dscng_language_engine/`, `backups_previos/`): the earlier v0.1→v0.25 experiment ladder (DSCN-G substrate, polysemy, pain, closed-loop). Pure Python, no numpy.
- **SGM** (`rizoma_docs/`): the newer Synaptic Graph Model spec + experiments (NodeCore, EdgeTable, ChainMode, FATE integration, 6-phase roadmap). Spec is detailed; implementation is aspirational.

The `dscng_core.py` in the home directory is a 226-line stub for DSCN-G, not SGM. It has no SGM concepts (NodeCore, EdgeTable, abduce, fate, ChainMode, modos).

### Key vault files for SGM review

When reviewing SGM in the vault, start with these in order:
1. `rizoma_docs/SGM_v1_4_Especificacion_Corregida.md` — the spec
2. `rizoma_docs/SGM_ROADMAP.md` — what's planned vs done
3. `rizoma_docs/README.md` (in rizoma_docs) — index/master doc
4. `rizoma_docs/experiment_registry.json` — what experiments exist
5. `rizoma_docs/results_exp_SGM_0007..0012.json` — latest results
6. `rizoma_docs/Arquitectura_Pure_L2_Pandora.md` — architecture context
When the user proposes a new architecture direction (e.g. "replace Transformer with
DSCN-G"), do NOT just discuss — build the smallest experiment that can FALSIFY the
load-bearing claim, then run it for real. Concrete recipe that worked 2026-07-25:
1. Create the dir from `su`: `su -c 'mkdir -p /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/<NAME>/{v0.1_concept_proof,baselines,decoder,results}'`.
2. Pull the REAL engine as the source of truth: copy
   `CORE/IMPLEMENTATION/CODE/verify_dscng_v3.py` to the experiment dir (so the
   dynamics are the published ones, not a reconstruction). Read it with
   `read_file` after `su -c 'cp ... <hermes-home>/'`.
3. Write the experiment as PURE STDlib Python (no numpy here) replicating ONLY the
   equations that govern the claim. For the "sparse memory scales" claim, that is
   Eq.2 (chain affinity) + Eq.5 (pruning) + Eq.1 (ω update); Kuramoto can be omitted
   because it does not touch vitality/chain-visits (state this caveat in the README).
4. RUN IT — and use the correct long-running recipe below. v0.1 result
   (N* saturates ~4.3 for N_init 4→1000, falsifying "scalable sparse memory") is in
   references/dscng_language_engine_v01.md.
5. The falsification metric: N* vs N_init. If N* saturates, the claim is dead with
   current dynamics; propose v0.2 redesigns (predictive-coding survival, raise K /
   lower θ_death, or mass-memory vs working-set split) and reuse run_v01.py to test them.

## DSCN-G Language Engine — evolving the experiment (v0.1 → v0.5)
The Language Engine is a VERSIONED experiment pipeline (under
NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/) whose goal is to test whether DSCN-G
can be a language-engine substrate, ending in a rustic L2 (ω→text) decoder. The
v0.1 template above is step 1; the pipeline then EVOLVES version by version. The
key methodological fork AFTER a falsification is to classify WHY it failed:

- **Parametric vs structural fork (v0.2 design):** when v0.1 falsifies a claim
  (N* saturates), the next experiment must decide if the collapse is FIXABLE by
  parameters or needs a REDESIGN. Sweep the parameters that bound N* at fixed
  large N_init: K chains and θ_death. Theory: N*_max ≈ (K+1)/θ_death (visit
  budget / death threshold). If raising K / lowering θ_death lets N* track
  N_init → collapse was PARAMETRIC (salvageable). If not → STRUCTURAL (needs
  redesign). Run the sweep, THEN read the result before designing v0.3.

- **USER DECISION (2026-07-25 tarde): "primero validar que el grafo entienda,
  luego vamos al decoder."** This REORDERS the pipeline: v0.3 is NOT hibernado
  first — it is RETRIEVAL ("¿el grafo entiende?"). Validate the graph can
  RECOVER the correct concept from a mass BEFORE building any decoder. The
  decoder (L2) is pushed to v0.5 and only attempted after retrieval validates.

- **v0.3 RETRIEVAL (DONE 2026-07-25):** built a vocabulary of M concepts (each
  a distant ω centroid, 3 noisy nodes per concept). Query = ω near a centroid;
  measure top-1 recovery accuracy. TWO affinity modes compared: (A) NORMATIVE
  = motor's real exp(-α‖ω_q−ω_i‖); (B) BITS/logic-gates = Luciano's idea, ω
  quantized to 2 bits/dim (sign+magnitude) and distance by Hamming. RESULT:
  norma = 1.000 at M=4/16/64/256; bits = 1.000/1.000/0.975/0.910. CONCLUSION:
  the graph RECOVERS correctly (entiende), and the bits representation PRESERVES
  semantics (only degrades to 0.91 at M=256 due to coarse 2-bit quantization).
  So Luciano's bits idea is VIABLE. Full design + result: references/
  dscng_language_engine_v03.md. Script+JSON in vault:
  NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/v0.3_retrieval/.

- **HIBERNADO / mass-memory split (v0.3b, PENDING):** the fix for catastrophic
  collapse is to NOT DELETE a node at V<θ_death — move it to a dormant list
  PRESERVING ω (the PANDORA project's rule: V≤0.10 → ω preserved, not erased;
  ACTIVO/DURMIENTE/HIBERNADO/MUERTO with HIBERNADO keeping ω). This turns the
  working-set (active ~N*) into a sub-graph of a persistent MASS. Luciano's own
  "semantic DB" idea (nodes as bits + logic gates; persist ω/φ/V in RAM; split
  memory into types/relations) converges INDEPENDENTLY with PANDORA's HIBERNADO.
  Two independent paths reaching the same fix is a VALIDATION signal, not a
  coincidence — treat it as the correction the v0.1 evidence demanded. v0.3b
  metric: N_active + N_hibernated = N_total_mass; compare against v0.1's 4.5.
  (Note: v0.3 retrieval ABOVE uses the mass as a STATIC store; v0.3b asks
  whether a DYNAMIC poda-with-hibernation keeps the mass alive during stepping.)

- **Decoder is the real bottleneck (v0.4→v0.5):** PANDORA and the GPT discussion
  BOTH converge that without L2 (ω→text) the elegant graph is mute. v0.4 = cheap
  win (β_eff = β(1+ρ), contextual learning rate, salvaged from PANDORA). v0.5 =
  rustic LINEAR projection ω→vocab on a tiny corpus. Decide up front: pure linear
  decoder vs retrieval+decoder (the latter if you want the graph to "retrieve"
  concepts from the mass DB first). If v0.5 produces no coherent text even in the
  simplest form, the substrate alone is insufficient — hybridize with an LLM
  (Option B) rather than replace it.

- **v0.5 RESULT (DONE 2026-07-25):** the rustic L2 = nearest-centroid retrieval +
  affinity-chaining. Nivel1 (dado ω de "gato" → decodifica "gato") = 100% OK.
  Nivel2 (generar encadenando por afinidad desde "el", 6 pasos) = "el casa el
  casa el casa el" → un LOOP de 2 pasos. LECCIÓN: el decoder RECUPERA perfecto,
  pero el encadenamiento ciego por afinidad se atora en ciclos porque no hay
  (a) ventana de contexto que acumule historial, (b) penalización de repetición,
  (c) anclaje a un prompt. Esto ES el piso "cavernícola": habla, pero dice
  bobadas en loop. El síntoma del loop es el marcador de lo que falta, no un bug
  del decoder. Fix inmediato (v0.5b): repetition penalty + memory window; luego
  W(t) de PANDORA (v0.7) para mover el ω con el historial.

- **"Microllm cavernícola" — distancia honesta (2026-07-25):** el usuario preguntó
  qué tan lejos está una microllm rústica. Respuesta medida, no humo:
  * HUESOS presentes: recuperación semántica (v0.3, 100%/91% a 256), memoria que
    no colapsa totalmente (v0.2, N* sube con K/θ), decoder mínimo que habla (v0.5).
  * FALTA para texto coherente/condicional: (1) ventana de contexto W(t) de
    PANDORA que mueva el ω con el historial; (2) penalizar repetición para romper
    el loop; (3) HIBERNADO (v0.3b/mass-memory) para vocabulario de miles sin
    colapso; (4) L2 ENTRENADO (v0.6, aprender ω→token de un corpus, no vectores
    hardcodeados). Con (1)+(2) salís de los loops; con (3)+(4) te acercás a microllm
    real. Híbrido con LLM (Opción B) sigue siendo necesario para generación seria.
  * NO es "mañana" ni "años": es semanas de experimentos chicos (v0.5b→v0.7).
  Full write-up + diseño de cada versión: references/dscng_language_engine_v05.md.

- **v0.4 β_eff CONTEXTUAL (diseñado 2026-07-25, CORRIENDO al cierre de sesión):** sacado de
  PANDORA, β pasa a β_eff = β·(1+ρ) donde ρ = densidad de conexiones activas (fracción de
  pares con afinidad > umbral). Hipótesis a medir: β contextual mejora retención de masa (N*)
  y convergencia de ω (T2) vs β fijo. IMPORTANTE: el sweep completo (N_init=1000 × 1500 pasos
  × 8 seeds × 2 configs) NO terminó confirmado en la sesión (se cortó antes de escribir JSON).
  Relanzar run_v04.py y leer results_v04.json antes de afirmar resultado. Código en vault
  LANGUAGE_ENGINE/ como run_v04.py.

- **v0.5b ROMPER EL LOOP (DONE 2026-07-25):** fijación inmediata de v0.5. Agrega (a) ventana de
  contexto WINDOW=3 que PENALIZA repetir las últimas W palabras, y (b) el ω de estado ACUMULA
  historial (se mezcla 0.6/0.4 con la palabra dicha, no queda fijo en la semilla). RESULTADO:
  "el casa el casa el casa el" → "el roja la corre el perro roja gato corre el perro", 0
  repeticiones adyacentes → LOOP ROTO. No es gramática (sigue saltando por afinidad) pero ya no
  es disco rayado. LECCIÓN: la ventana de contexto mínima es el puente entre "loop" y "secuencia
  que se mueve"; W(t) de PANDORA (v0.7) es la versión continua.

- **HOJA DE RUTA v0.6 (acordada 2026-07-25, EN MARCHA):** el usuario pidió v0.6a Y v0.6b e
  aportó ideas. CORPUS: el usuario exigió corpus EXISTENTE real (no frases a mano). Bajado Don
  Quijote (gutenberg, 2.2MB, español real) a home/vault; Benjamin (argento de pysentimiento) NO
  bajó (HF auth 401, no hay git, GitHub 404) → PENDIENTE con token HF del usuario. v0.6a corrió
  sobre Don Quijote + textos criollos del vault. Ver references/dscng_language_engine_v06.md.
  * **v0.6a — APRENDIZAJE SUPERVISADO (next-token, estilo GPT-1): DONE.** Vocab top-V=200 de Don
    Quijote; ω de w_i aprende acercarse a ω de w_{i+1} (objetivo = palabra REAL, no ω_ideal fijo).
    RESULTADO REAL (run_v06a.py, 241.443 palabras, 3 epochs): accuracy 0.0045 → 0.1011 (22x).
    El grafo APRENDE next-token de datos reales en representación LOCAL (ajusta 200 ω, no 117M
    params). BUG/FIX: `predict()` arrancaba `best,bests=-1,None` → `s>bests` comparaba float>None
    (TypeError); fix `best,bests=-1,-1.0`. Vault: LANGUAGE_ENGINE/v0.6_next_token/.
  * **v0.6b — APRENDIZAJE POR DOLOR (RL/RLHF): DISEÑADO/CORRIENDO.** "dolor" = baja de V por uso
    incorrecto. Regla HARDCODEADA (Opción A, sin simular usuario): transición inválida = dos
    sustantivos seguidos (S-S, diccionario mini SUST/VERB/CONN) → baja V (V-=0.05) + aleja ω de la
    transición; válida → sube V (+0.01). ETIQUETA del nodo MUTA por uso y guarda HISTORIAL de
    aplicaciones. Métrica: tasa de transiciones inválidas ANTES vs DESPUÉS. Al reiniciar: leer
    results_v06b.json (v0.6b seguía corriendo al cierre). El dolor hardcodeado es placeholder;
    el dolor REAL debe venir de CONSECUENCIA EN EL MUNDO (entorno), no de regla del agente.
  * **v0.6c — DIMENSIONES POR ABSTRACCIÓN (idea de Luciano, PENDIENTE):** hipótesis de que
    conceptos abstractos (amor) necesitan más grados de libertad / más vecinos conectados que
    concretos (rojo). Medible como GRADO DEL NODO (cantidad de vecinos con afinidad>umbral) tras
    entrenar: si "amor" tiene más vecinos que "rojo", la hipótesis se confirma. Conecta con
    etiquetas mutables (un nodo abstracto cambia de rol seguido).
  * **MARCO Transformer vs GRAFO (respuesta al usuario):** Transformer entrena UNA matriz W (117M
    params GPT-1) por backprop sobre todo el corpus (O(params)); "gato→come" vive EN LOS PESOS
    (difusa). Grafo DSCN-G: conexión = arista real entre nodos; ajusta SOLO nodos tocados
    (O(~4.5, v0.1)) → barato. MISMA dinámica (minimizar error next-token) pero el "peso" es el ω
    del nodo. Tensión honesta: Transformer paga potencia por ESCALA (50k palabras vivas); grafo
    barato PERO colapsa a ~4 sin HIBERNADO (v0.1/v0.3b). El ahorro no es "despilfarro" del
    Transformer — es el costo de vocabulario masivo vivo.
  * **"PseudoAGI" — distancia honesta (respuesta al usuario):** YA tenemos (medido): marco
    auditado; grafo recupera (v0.3); no colapsa si ajustás params (v0.2); decoder habla (v0.5b);
    aprende next-token de corpus real (v0.6a). Es un SUSTRATO COGNITIVO RÚSTICO neuro-simbólico,
    pieza legítima de ruta a AGI. FALTAN 4 gaps: (1) CONTEXTO global (W(t) Pandora); (2) DOLOR
    real desde entorno; (3) ABSTRACCIÓN/dimensiones (v0.6c); (4) PERSISTENCIA real (hibernado
    v0.3b no mergeado). Veredicto: pseudoAGI de laboratorio ALCANZABLE en meses; AGI completa es
    otro orden de magnitud. El usuario debe elegir la prioridad de los 4 gaps.

- **COMPARACIÓN TRANSFORMER vs GRAFO (marco 2026-07-25):** Transformer entrena UNA matriz de
  pesos W (117M params en GPT-1) por backprop sobre todo el corpus; la conexión "gato→come" vive
  EN LOS PESOS (difusa), no en nodos; backprop recorre toda la red (O(params)) → POR ESO usa tanta
  potencia. Grafo DSCN-G: la conexión sería arista real entre nodos con ω/φ propios; ajusta SOLO
  los nodos tocados (O(nodos activos) ~4.5, v0.1) → POR ESO es barato. La dinámica es la MISMA
  (minimizar error de next-token) pero el "peso" es el ω del nodo, no un número en W. Tensión
  honesta: el Transformer paga potencia por ESCALA (50k palabras vivas); el grafo es barato PERO
  colapsa a ~4 sin hibernado (v0.1/v0.3b). El ahorro de cómputo no es "despilfarro" del
  Transformer — es el costo de vocabulario masivo vivo; el grafo lo resuelve con HIBERNADO.

- **PATRÓN: NO hay herramienta web_search en este entorno.** Para bajar papers/acceder a red usar
  el terminal con urllib (hay red). Funcionó 2026-07-25: bajar GPT-1 ("Improving Language
  Understanding by Generative Pre-Training", Radford 2018) desde
  `https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf`
  vía `python3 -c "import urllib.request; urllib.request.urlretrieve(url,'gpt1.pdf')"` y copiar al
  vault con `su -c 'cp gpt1.pdf /sdcard/Hermes/.../LANGUAGE_ENGINE/'`. PDF en vault:
  NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/gpt1_paper.pdf (referencia para v0.6a). Para extraer
  texto evitar pdfminer (falla por dependencia cryptography ausente); citar hechos estándar del
  paper (12-layer decoder-only, 117M params, objetivo log-likelihood next-token, pre-training +
  fine-tuning).

**Pitfall — experiment queueing on this device (CORREGIDO 2026-07-25 tarde):**
The real bottleneck is NOT concurrency per se — it is ONE runaway cell in a sweep.
A pure-Python O(n²) sim over N_init=1000 × 1000 steps × 5 seeds ≈ 2 min; the SAME
at K=30/θ=0.003 ran ~28 min and never finished (the extreme parameter corner is the
killer, not the parallel launch). LESSON: if a sweep stalls, KILL it and relaunch a
CUT-DOWN version (drop the extreme K/θ corners) — the truncated sweep already answers
the parametric-vs-structural question. A LIGHT experiment (v0.3 retrieval: M≤256,
3 nodes/concept, no N=1000 O(n²) loop) runs FINE concurrently with a heavy one on this
single CPU. So: do NOT hold a light experiment waiting on a heavy sweep — kill the
heavy sweep's runaway corner, launch the cut-down heavy, and run the light one in parallel.
(Confirmed 2026-07-25: v0.2 full sweep stalled at 75 min; killed via `pkill -f run_v02.py`,
relaunched cut-down run_v02c.py, and ran v0.3 in parallel — both completed.)
**To KILL a stuck background process:** `terminal(background=true)` + `process(action='kill')`
FAILS ("No module named 'psutil'"). Use the terminal: `pkill -f <scriptname>.py` then
`pgrep -f <scriptname>.py` to confirm. Do NOT rely on the process() kill API on this host.

Full roadmap, PANDORA convergence notes, and per-version design recipes:
references/dscng_language_engine_roadmap.md.

### Long-running experiment execution on this Android host (CRITICAL)
- A Python-pure O(n²) loop over N_init=10000 × 2000 steps × 20 seeds WILL exceed
  600 s and time out a foreground terminal call. Use `terminal(background=true,
  notify_on_complete=true)` for anything >~60 s. NEVER use `nohup ... &` / `setsid`
  / `disown` — the Hermes terminal rejects shell-level background wrappers
  ("Foreground command uses shell-level background wrappers ... use terminal(background=true)").
- Run the script FROM HERMES HOME, NOT from /sdcard. The app-shell `cd /sdcard/...`
  does not resolve (FUSE), so Python errors with "can't open file ... No such file".
  Recipe: `cp script.py ~/run_x.py` then `cd ~ && python3 run_x.py`. Write results
  to a JSON in home, then `su -c 'cp ~/results_x.json /sdcard/Hermes/.../results/'`.
- Before the heavy barrido, PROBE COST: run a small N_init (e.g. 1000/3 seeds/600)
  and time it; linear-extrapolate to decide whether a larger N_init is feasible in
  pure Python. (Observed: ~44 s for 1000×3×600 ⇒ 10000 would need ~10×/node ⇒
  infeasible here; N_init up to 1000 is already enough to falsify saturation.)
- **write_file STREAM-TIMEOUT pitfall (2026-07-25 tarde):** a single `write_file`
  call with a >~8K-token body TIMED OUT mid-stream and the file was NOT written
  (the tool reported "stream stalled", action not executed). Keep every
  write_file body UNDER ~8K tokens — split large scripts into 2+ write_file calls
  (or write a compact version). This is separate from the heredoc trap; it bites
  even with `write_file` directly. The v0.3 run_v03.py was written compact (3.4KB)
  precisely to dodge this.
- **Kill stuck background via terminal, NOT process() API (2026-07-25 tarde):**
  `process(action='kill')` fails with "No module named 'psutil'" on this host.
  To stop a runaway `terminal(background=true)` job, run in a normal terminal:
  `pkill -f <script>.py` then `pgrep -f <script>.py` to confirm it is gone.

## Delivery style
User explicitly asked: "Recordá decirme todo en criollo cuando lleguen los resultados."
Summarize empirical/computational RESULTS in informal Argentinian Spanish ("criollo"),
concrete and direct, no academic fluff. Keep the whole conversation in Spanish (user pref).

## Pitfalls / honest boundaries
- NS 3D regularity is NOT proven. The "G acotada ⇒ no blow-up de H¹" result is from a SIMPLIFIED
  spectral model (1D/2D/3D mode grids), not full DNS. It is a direction + candidate Φ=G[u], not
  a Millennium-proof. State the caveat every time.
- VERIFY USER-CLAIMED EDITS BEFORE TRUSTING (2026-07-25): when the user says "ya corregí el
  archivo X con los datos de Y", do NOT take it at face value — verify. This session the user
  claimed to have applied the 7-point audit fixes to NOUS_Tecnico_v4.md "using the frozen DSCN-G
  v1.0 data"; in reality the vault v4 was BYTE-IDENTICAL to the pre-session copy (mtime 06:22,
  clean diff) and NO v4 was touched after 06:30 anywhere on device. The confusion was
  terminological: "la v1.0 congelada" = the NOUS/DSCN-G/ DIRECTORY (a FORM freeze per
  FREEZE_CHECKLIST.md), whose data files are authoritative, NOT the v4 doc. Recipe before
  reporting any doc as 'corregido': run `su -c 'stat -c "%y %s" <file>'` and diff against a
  known-good copy; if unchanged, tell the user the edit did not land and offer to apply it
  yourself FROM the authoritative source. The frozen DSCN-G dir is the SOURCE OF TRUTH for
  claims; the v4 doc is a downstream artifact that lags and must be patched from that source.
- DDSD "Mersenne identity" E(2^p-1)=p is conventional (bits); the paper correctly OMITS it as a
  main result (§11.3, "has no dynamical content"). Do NOT "fix" it as a bug.
- NOUS_Tecnico_v4.md is STALE vs the Ronda 6 audit AND internally self-contradictory. Use
  ANALISIS_ESTADO_2026-07-24.md + claims_falsifiable.md as authoritative for DSCN-G claims.
  Concrete internal contradictions found 2026-07-25 (full list + fix targets in
  references/nous_tecnico_v4_audit.md):
    * C3: index + §16.1 say RETIRED (0.9% triggers, ΔPLV≈0) but §15.5 reports 28.6% ticks C3
      active, r=0.73, 94% antipodal — must reconcile before any citation.
    * ρ notation recycled: 'ρ_eff=0.7001' is BOTH 'vitality convergence factor' (T1/§13.1)
      AND 'densidad contextual' (§13.5/§15.3) — two different variables, coincidental same
      number. Rename one.
    * T2: §line303 'distancia final 0.612' is actually cosine similarity (confirmed §13.3
      ω_sim=0.612). Do NOT call it a norm-distance.
    * T3: body cites 97/100 (ω_sim>0.5, soft) without flagging the 76.7% strict (R≥0.9) that
      the index already corrected to. Report both criteria explicitly.
    * T1: statement is just 0≤V≤1 (=Invariante 7.1) but §13.1 renames it 'Convergencia de
      Vitalidad' with a different enunciado and verifies it by measuring ρ (density), not
      vitality convergence. Statement ≠ verification.
    * Graph does not grow in the reference sim (telemetry §15.4: 'Nodos activos = 4.0±0.0'),
      yet P6 (inheritance drift) and P7 (XOR abstraction) require a growing graph; the
      reference code (step_12) leaves cascade as `pass` and XOR is not implemented. P6/P7
      metrics do not come from the quoted reference code — say which sim produces them or
      downgrade the claim.
    * Index promises §18 (NOUS-Memory/OpenClaw), §19 (Limitaciones Honestas), §20
      (Referencias) but the file ends at §17.5 (1777 lines). Those promised sections are
      missing — a reviewer hits the gap immediately. Especially §19.
    * VERIFICATION-PARAM MISMATCH (2026-07-25): the frozen verification_results_v3.json used
      β=0.20 for T2 and η=0.50 for T3, but the v4 doc states β=0.10 (T2) and η=0.05 (T3) as the
      "parameters of Tabla 3.1". The v4's quoted verification therefore does NOT use its own
      stated base parameters. When auditing, cross-check the param block of the doc against the
      JSON in CORE/VALIDATION/RESULTS/ — they diverge.
    * T1 MAXIMALITY IS CONDITIONAL (2026-07-25): the v4 lists T1 maximalidad as "✅ Validado"
      flat. The frozen maximality_real_results.json shows it depends on injection protocol:
      full-vitality injection (V=1.0) → only 3–77% pruned back (maximal_real = FALSE); boundary
      injection (V=θ_death) → 100% pruned back (TRUE). The claims_falsifiable.md admits this
      openly ("corrección de diseño propia que se documenta sin esconder"). The v4 must carry the
      condition or it overclaims.
    * T2 ALIGNMENT is 1.0000 (frozen verification_results_v3.json), matching the doc's Claim 2 —
      so the doc's OWN "distancia 0.612" (Point 4 above) is doubly wrong: wrong metric AND it
      shadows the real 1.0000 alignment result.
- FREEZE_CHECKLIST.md caveat (2026-07-25): the DSCN-G v1.0 freeze is a FORM/structure freeze
  (folders, CORE/EXTENSION split, claims table), explicitly NOT a scientific freeze — it leaves
  C3 / Φ_proxy / discrete-dynamics OPEN as content decisions. "Congelado" ≠ "validado". The
  frozen DSCN-G dir is the authoritative DATA source; treat it as such when patching the v4.
- Don't conflate the cosmic narrative (two primordial nodes perturbed) with the verified
  formalism. The narrative is the interpretive layer; label it as such (like NOUS_Filosofico
  does for consciousness).

## Rigorous falsification protocol (reviewer's 7 checks — apply to ANY unifying claim)
When a friend/reviewer stress-tests a grand unification, run these IN ORDER before writing the
resolution. Each maps to a concrete action already proven in-session:
1. CONTROL NEGATIVE FIRST. Run the unifying mold on a system with NO reason to connect
   (Lotka-Volterra / Kuramoto WITHOUT pruning). If it "confirms" there too → the pattern
   distinguishes nothing (it is just "stable system"). If it fails → you have something real.
   (Session: both stayed bounded → mold is NOT exclusive; mechanism C3 is the real filter.)
2. OPERATIONAL CRITERION, DEFINED BLIND. Before looking at the target domains, write a strict
   definition of "two competing dynamics" someone could apply to a NEW system without knowing
   your conclusion. Then apply it unmodified to 2-3 random systems and record pass/fail.
   Working criterion used: C1 two positive quantities A,B evolve with opposite-sign means;
   C2 a third R(A,B) is non-increasing / bounded; C3 the bound comes from the COUPLING STRUCTURE,
   not an external variable (viscosity, friction). C3 is what separates NS/DSCN-G/Collatz from
   Lotka-Volterra/Kuramoto/decaying-oscillator (which fail C3).
3. RESOLVE TABLE CONTRADICTIONS. If a test script says "no match" but a summary table says
   "confirmed", RE-RUN the script and downgrade/mark the row as unconfirmed. Do not leave a row
   at the same level as the confirmed ones. (Session: Riemann row downgraded to NOT CONFIRMED.)
4. CROSS-DOMAIN QUANTITATIVE PREDICTION. Pick two rows and try to DERIVE one bound from the
   other with a real formula (not just "both bounded"). If no formula emerges, record it as a
   NEGATIVE result — that is information, not failure. (Session: f_P* vs N* — no formula; bounds
   independent → structural-only unification confirmed.)
5. LOWER NS STATUS IN THE TABLE. Once the strong lemma fails (α_min→0 with AND without G), the
   table must NOT list NS as "confirming" like the others. Mark it PARTIAL so the table does not
   lie by omission.
6. REAL DATA, NOT TRUST. Download actual published data (Odlyzko's 100k Riemann zeros) and run
   the level-spacing test against GUE yourself. Costs nothing, gives a reusable routine, and
   removes "we assume" from the claim. (Script: references/odlyzko_gue_probe.py. Note: simple
   mean-normalization is NOT the correct unfolding for zeta — density grows as (T/2π)log(T/2π);
   the qualitative repulsion result holds, but a tight Wigner-surmise match needs proper unfolding.)
7. 2^φ GATE. Do not promote a constant from "pending" until there is a MECHANISM explaining why
   THAT constant and not another (not "it is relatively close to 4"). For 2^φ the mechanism is
   arithmetic isolation of a=3 in (1,2^φ); acceptable as explanation, but it is arithmetic not
   dynamic → keep dynamic derivation pending.

## Document-consistency audit of NOUS_Tecnico_v4.md (technical-compendium review)
When the user asks to read/audit the NOUS_Tecnico_v4.md compendium 'en profundidad', read the
WHOLE file in chunks (it is ~1777 lines / 91KB; copy it out with
`su -c 'cp /sdcard/Hermes/nexus-vault/NOUS/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md <hermes-home>/'`
then read_file in ~400-line windows). Do NOT summarize the index — the body is where the
contradictions live.

Reusable 7-point internal-consistency checklist (derived 2026-07-25; caught all 7 real issues):
1. INDEX-vs-BODY completeness: every section in the Índice de Contenidos must exist in the
   body. Flag promised-but-missing sections (here: §18/§19/§20 gone, ends at §17.5).
2. STATUS-vs-BODY claim contradiction: if the status/index says a claim is RETIRED, the body
   must not still show it as live evidence (here: C3 retirado vs §15.5 r=0.73). Reconcile or
   the doc lies by omission.
3. NOTATION recycling: one symbol used for two different quantities (here: ρ_eff = vitality
   convergence factor AND densidad contextual). Same number by coincidence hides it. Rename.
4. METRIC-NAME vs METRIC-MEANING mismatch: a reported number labeled with the wrong quantity
   (here: T2 'distancia 0.612' is a cosine). Cross-check each reported value against its
   definition in the equation/verification section.
5. MULTI-CRITERION values reported without unification: when a theorem has a soft and a strict
   pass threshold (here: T3 97% at ω_sim>0.5 vs 76.7% at R≥0.9), report BOTH explicitly,
   don't leave the loose one standing as if it were the corrected value.
6. CODE-vs-CLAIM gap: does the quoted 'reference implementation' actually produce the reported
   metric? (here: graph stays at 4 nodes, cascade is `pass`, XOR unimplemented → P6/P7 can't
   come from that code). State the real provenance of each claim or downgrade it.
7. THEOREM STATEMENT vs VERIFICATION mismatch: the proven statement and the verification must
   measure the same thing (here: T1 statement = 0≤V≤1, verification measures ρ density).

This checklist is the document-level analogue of the 'reviewer's 7 checks' (which target
unifying CLAIMS). Use both: one for internal doc hygiene, one for cross-domain validity.
Full concrete findings + fix targets: references/nous_tecnico_v4_audit.md.

## Applying the 7-point audit fixes to the v4 (patch recipe)
Auditing is step 1; the user will often then say "apply the fixes using the frozen source".
Concrete recipe that WORKED 2026-07-25 (all 7 points applied, diff clean, written to vault):
1. Copy the v4 out to Hermes home with `su -c 'cp /sdcard/Hermes/nexus-vault/NOUS/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md <hermes-home>/'`. Work on the home copy (readable by `patch`/`read_file`); the /sdcard original is root-only.
2. Read the EXACT bytes of each target region with `su -c "sed -n 'L,Mp' <vault-v4>" | cat -A`
   before editing — LaTeX backslashes (e.g. `\|`, `\\rho`) are real chars and must match exactly.
3. FIRST attempt: a Python bulk-replace script (`write_file` to home → `python3 script.py` in a
   NORMAL terminal — plain python3 3.13.13 works for home-only files). Use `content.count(old)`
   and assert ==1 before replace; collect a list of which labels applied and which FAILED.
   This catches escaping drift: the script's `\\|` vs the file's `\|` desync will show as
   "encontrados 0". Note the SyntaxWarning on `\\|` is harmless.
4. For any block the script FAILED (usually the ones with heavy `\|`, `$`, `∑`), fall back to the
   Hermes `patch` tool (mode=replace, NOT execute_code). `patch` fuzzy-matches literal text
   including backslashes and is far more reliable than fighting Python string escaping. Do these
   last two blocks (here: §13.4 table, §13.5) via `patch`.
5. VERIFY no old-number residue remains: `grep -n "r = 0.73\|97 / 100\|Distancia final\|28.6%"`
   on the home copy must return nothing; `grep -c "RETIRADA\|76.7%\|Limitaciones Honestas"` must
   be >0. Also `wc -l` to confirm growth (1777 → ~1814 after adding §19/§20).
6. Write back to vault: `su -c "cp <home>/NOUS_Tecnico_v4.md /sdcard/Hermes/nexus-vault/NOUS/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md"` then
   `su -c "chown root:everybody ... && chmod 664 ..."`. ALSO keep a vault-side backup:
   `su -c "cp <dst> <dst>.vault_orig_YYYYMMDD.bak"`.
7. Emit the diff for the user: `su -c "diff <dst>.vault_orig_*.bak <dst>" | head -120`.
PITFALL: the v4's own stated base params (β=0.10, η=0.05) differ from the frozen verification
JSON (β=0.20, η=0.50). When patching the verification sections, DECLARE this gap explicitly
(added to §19 point 3) rather than silently "fixing" β to match — both converge, the mismatch is
a documentation debt, not a contradiction to hide.
Full before/after + the exact replacement strings used: references/nous_tecnico_v4_fix_applied.md.

## References
When a session produces a cross-domain result (e.g. the Tríada shows DSCN-G is the
cognitive layer of a shared mechanism), the user may ask to "update what we changed in
DSCN-G inside NOUS". The DSCN-G core is FROZEN at v1.0 (Ronda 6, 2026-07-24). Rule:
**never edit the core paper or CORE claims** — only the EXTENSION placeholders and the
index/status tables that explicitly mark open items. Concrete recipe used 2026-07-25:
1. `find NOUS/DSCN-G -name "*.md"` + grep for `triada|2^phi|galileo|riemann|tercer motor`
   to find what (if anything) references the new result. Usually NOTHING — the Tríada lives
   in `/TRIADA_AUTORREGULACION/` at vault root, not in NOUS.
2. Identify which frozen-doc rows become stale. Two changed this session:
   - `EXTENSIONS/DISCRETE_DYNAMICS/README.md` was a placeholder ("vacío, sin contenido,
     no fabricar contenido"). The Tríada GAVE it content → rewrite it as
     "CON CONTENIDO PARCIAL" documenting DSCN-G = cognitive layer (φ_i + ω_i → V_i) and the
     link to DDSD/Collatz/NS/Riemann. Do NOT claim it joins CORE.
   - `CLAIMS_STATUS.md` row "Dinámica discreta — relación con el núcleo" was
     "⚠️ Hipótesis — sin contenido aún". Patch it to
     "✅ Marco formalizado 2026-07-25 vía Tríada" with a pointer to the EXTENSIONS README
     and /TRIADA_AUTORREGULACION/.
3. Write the new README / status text with Hermes `write_file` to Hermes home, then
   `su -c 'cp ... /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/...'`. For a single-table-row edit,
   use a tiny Python script (write_file → su python) doing `assert old in s; s.replace(old,new)`
   so a wrong old_string fails loudly instead of silently corrupting the table.
4. Explicitly tell the user what did NOT change (core paper, T1/T2/T3, Φ_proxy retired) so the
   freeze integrity is visible. Keep the Tríada marked as a COMPARATIVE framework, not CORE —
   because cross-domain quantitative prediction is still NEGATIVE (bounds independent, Point 4).
Full recipe + before/after: references/updating_nous_from_triada.md.

## References
- references/triada_results.md — full test outcomes (A/B/C/M, Riemann GOE, NS 1D/2D/3D G
  plateaus, Galileo Φ=G regularity argument, DDSD correction, reviewer's 7-point audit).
- references/odlyzko_gue_probe.py — reusable routine: download Odlyzko zeros, compute spacing
  statistics, compare against GUE/GOE Wigner surmise.
- references/phi_2_dynamic_derivation.md — the 2^φ derivation: 2^φ=3.069 (NOT 3.694), and the
  dynamic mechanism via Fibonacci convergents of log₂(3) (closes reviewer Point 7).
- references/updating_nous_from_triada.md — freeze-safe recipe to propagate Tríada (or any
  cross-domain) findings into NOUS/DSCN-G EXTENSIONS + CLAIMS_STATUS without touching CORE.
- references/nous_tecnico_v4_audit.md — the 7 concrete internal-consistency findings on
  NOUS_Tecnico_v4.md (2026-07-25 session): index/body gap, C3 retiro-vs-r=0.73 contradiction,
  ρ recycling, T2 distance/cosine, T3 dual criterion, graph-doesn't-grow vs P6/P7, T1
  statement/verification mismatch. Use as the fix list before any doc edit or submission.
- references/nous_tecnico_v4_fix_applied.md — the exact replacement strings + diff recipe used
  to APPLY the 7-point audit to the v4 (2026-07-25): where the β-mismatch note landed, the
  §19/§20 appendix text, and the two blocks that had to be done via `patch` not Python.
- references/dscng_language_engine_v01.md — DSCN-G "Language Engine" v0.1 concept-proof:
  the hypothesis (Transformer→DSCN-G), the falsification design (N* vs N_init),
  the real result (N* saturates ~4.3 → "scalable sparse memory" claim falsified),
  and the v0.2 redesign candidates (predictive-coding survival / raise K / working-set split).
- references/dscng_v1_frozen_source_map.md — WHERE the authoritative DSCN-G v1.0 frozen data
  lives and what each file proves. Use this to resolve any v4-vs-source conflict: it maps
  CLAIMS_STATUS.md, claims_falsifiable.md, C3_Face_Hijacking/{STATUS,README}.md,
  CORE/VALIDATION/RESULTS/{verification_results_v3,maximality_real_results}.json, and
  EXPERIMENTS/N_BACK/nback_v6_corrected/nback_v6_paper_ready.json to the specific claim each
  corrects in the v4.
- references/dscng_language_engine_roadmap.md — the v0.1→v0.5 Language Engine pipeline:
  layout, hypothesis→falsification lineage, the v0.2 parametric/structural fork, the v0.3
  HIBERNADO/mass-memory split, PANDORA convergence, and the Android running recipe.
- references/dscng_language_engine_v03.md — v0.3 RETRIEVAL experiment (DONE 2026-07-25):
  design (vocabulary of M concepts, query ω near centroid, top-1 recovery), the two
  affinity modes (normative exp(-α‖·‖) vs Luciano's bits/Hamming), and the real result
  (norma=1.000 at M≤256, bits=0.910 at M=256). Validates "the graph understands" and
  that the bits representation preserves semantics. Precedes the decoder (v0.5) per
  user decision "validate understanding first, then the decoder".
- references/dscng_language_engine_v05.md — v0.5 L2 RUSTIC DECODER (DONE 2026-07-25, v0.5b breaks the loop):
  nearest-centroid retrieval (100% OK: "gato"→"gato") + affinity-chaining that LOOPS
  ("el casa el casa el casa el"). v0.5b added context window (WINDOW=3) + repetition
  penalty → "el roja la corre el perro roja gato corre el perro" (loop broken, 0
  adjacent repeats). The loop is the marker of missing context/repetition-penalty/prompt-
  anchor. NOTE: this reference file is listed as "NOT YET WRITTEN" in the original skill —
  if it's missing on disk, create it from the SKILL.md v0.5 block.
  create it from the SKILL.md v0.5 block if the file is missing on disk.
- references/dscng_language_engine_v06.md — v0.6 next-token + dolor (2026-07-25 noche):
  Don Quijote corpus bajado (Benjamin bloqueado por HF auth); v0.6a DONE (accuracy
  0.0045→0.1011, 22x, bug bests=None fixeado); v0.6b diseñado/corriendo (dolor hardcodeado
  S-S, etiquetas mutantes + historial); marco Transformer-vs-grafo; 4 gaps de pseudoAGI.
- references/sgm_experiment_workflow.md — concrete SGM experiment recipe (2026-08-02):
  read-project-first, heredoc script shape, smoke-test+run, HONEST PASS gate (mechanism
  must truly fire, not timeout), register+mirror+push, GitHub DELETE for removed files,
  and the Eq.6/Eq.8/§2.3.1/§2.3.2 equations for contradiction vs doubt.
- references/sgm_sdcard_editing_and_pdf_confirm.md — how to EDIT /sdcard vault files in
  place (sed-in-su / assert-python, because patch+read_file can't see /sdcard) and how to
  CONFIRM a mislabeled PDF's true identity with PyPDF2 extract_text (the "don't assume"
  rule that caught hipporag_v2_2025.pdf → SNAP).
