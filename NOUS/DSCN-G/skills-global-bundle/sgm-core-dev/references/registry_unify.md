# Repo hygiene — registry unification, API deletes, synthetic labelling

Concrete procedure used 2026-08-02 when Luciano asked to "unify the two registries,
`git rm -r --cached lit/papers/`, and label 0022 as synthetic".

## 0. CRITICAL ENVIRONMENT FACT
`git` is NOT installed on this Android (`system/bin/sh: git: inaccessible or not found`).
So `git rm`, `git status`, `git ls-files` DO NOT WORK. Equivalent ops go through the
GitHub API (token per-message). The repo is managed by `github_push_sgm.py` (PUT only).

## 1. Find duplicate registries
```
find $SGM -iname "*registry*"
```
Found: `results/experiment_registry.json` (canonical, 26 entries) AND
`experiment_registry.json` at the vault ROOT (stale, 12 entries).

## 2. Audit before deleting the stale one
a) **Diff ID sets** (python): confirm stale ⊆ canonical so nothing is lost.
   `viejo NO en nuevo: []` ⇒ safe to delete.
   Here root had 0001-0012; canonical had 0001-0025. Safe.
b) **Grep for writers**: `grep -rsn "experiment_registry.json" $SGM --include=*.py`
   must show NO reference to the ROOT path (only `results/...`). None found ⇒ safe.
c) If any `.py` writes the root path, fix it first.

## 3. Delete the stale registry
- Local: `rm -f $SGM/experiment_registry.json`
- Remote (API, because git absent):
  GET `https://api.github.com/repos/Rylow999/SGM-CORE/contents/experiment_registry.json`
  → take `sha`; DELETE same URL with body `{"message":..., "sha":<sha>}`. Expect 200.
- Confirm 404 via GET afterward.

## 4. `git rm --cached lit/papers/` equivalent
Since git is absent, do it via API:
- List `contents/lit/papers/` via GET (recurse into subdirs like `wrong_id/`).
- For EACH file: GET sha → DELETE with sha. (Dirs auto-vanish when empty; a 404 on
  the dir DELETE just means it's already gone.)
- This session removed 13 files (9 PDFs + 4 in wrong_id/). Locals stay (covered by
  `.gitignore` for future pushes).
- **TRAP:** `.gitignore` does NOT retroactively remove files already PUT to GitHub.
  The ignore only stops FUTURE uploads. Verify actual tracked state via API GET, NOT
  `git ls-files` (which lies when git is absent — returned empty here though 13 files
  WERE tracked).

## 5. Honest synthetic labelling (0022 case)
In BOTH `results/experiment_registry.json` entry AND its result JSON, set:
```
"validation": "synthetic",
"corpus": "sintetico (lenguaje de juguete, bigrama oculto determinante) — NO corpus natural",
"test_target_real": "T-DEC-01 REAL sobre corpus natural (Don Quijote) PENDIENTE"
```
Do NOT let a synthetic PASS read as a natural-corpus result (Luciano requires this).

## 6. Fix docs that pointed at the deleted root path
`docs/SGM_experiment_protocol.md` and `README_SGM.md` mentioned
`experiment_registry.json` (root) — rewrite to `results/experiment_registry.json`
and fix stale counts (was "15 experimentos" → 26).

## 7. Push
Push ONLY the canonical `results/experiment_registry.json` + the relabelled result JSON
+ the doc fixes. Do NOT re-push the deleted root registry (the push script will try to
upload it and fail with FileNotFoundError — just omit it from the path list).
