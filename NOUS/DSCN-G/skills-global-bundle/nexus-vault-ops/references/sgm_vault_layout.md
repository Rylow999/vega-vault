# SGM Vault Layout & Governance (updated 2026-08-02)

## Where SGM lives
- Real vault (user-visible): `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/`
- GitHub mirror: `Rylow999/SGM-CORE` (main), pushed via `~/github_push_sgm.py` (BASE = absolute vault path above; never `~` under `su`).
- Agent HOME `/data/user/0/com.hermesagent.android/files/home/` is a SANDBOX the user CANNOT open. Old `rizoma_docs/` and `~/EXPERIMENTOS/SGM/` are STALE MIRRORS — ignore them.

## Separation rule (hard, Luciano)
SGM and DSCN-G Language Engine are SEPARATE projects. Cross-references only, never mixed files.
- LE: `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/`
- PandoraOS docs: `/sdcard/Hermes/nexus-vault/SHARED/PandoraOS/`
- If LE / PandoraOS / CHANGELOG / EXPLICACION_CRIOLO / RESUMEN_NOCHE appear inside SGM -> `mv` them out (never `rm`).
- SGM README must state separation explicitly and list only SGM experiments.

## Structure (real)
- `docs/` (7, SGM-only): spec v1.4, roadmap, protocol, literature_index, SGM_README, Arquitectura_Pure_L2_Pandora, RIZOMA_Vision
- `experiments/` + `phases/phase0_substrato/` + `phases/phase2_inferencia/` — scripts (dup'd across both, ok)
- `results/` + `phases/*/` — JSON results
- `lit/papers/` (wrong_id/ for mislabeled)
- `experiment_registry.json` — 15 entries (0001–0014 + 0003_stress)

## ID protocol
`exp_SGM_XXXX_<descriptor>`, unique, no reuse. Registry entry: config/seed/hypothesis/test_target/links.

## Rebuild / fix the registry (drifts!)
Duplicates (0008/0009) and missing (0005) happen. Honest rebuild:
1. List `results_exp_SGM_*.json` under `phases/`.
2. Read each, extract id/name/result.pass/metrics.
3. Dedup by `experiment_id`; SORT by regex `\d+` on last segment (naive `int(split("_")[-1])` breaks on `exp_SGM_0003_stress`).
4. Write via `su -c` python (FUSE: write_file/patch fail on /sdcard).

## Push flow (SGM-CORE)
`python3 github_push_sgm.py Rylow999 <token>` from agent home. Token per-message, never persist. GET repo tree before/after (409 = nothing uploaded). `.gitignore` excludes `__pycache__/`, `wrong_id/`, `.hermes` — add `__pycache__/` if missing (smoke tests leave .pyc the push will upload).

## Before a new SGM experiment (Luciano)
Read ALL prior JSON results + the relevant spec section (§2.3.1 contradiction, §2.3.2 doubt). Reconstruct registry from JSONs to know true state. Explain results in criollo after.
