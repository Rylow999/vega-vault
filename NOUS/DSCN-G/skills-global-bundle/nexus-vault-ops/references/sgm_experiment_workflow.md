# SGM Experiment Workflow — concrete recipe (reference)

Reusable pattern for authoring a SGM experiment on this Android host (FUSE + pure-stdlib
python). Derived from exp_SGM_0014 (verify_contradiction) and exp_SGM_0015 (unified_loop),
both DONE 2026-08-02.

## 0. Read the project first (MANDATORY before coding)
```sh
su -c 'sed -n "102,206p" /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/docs/SGM_v1_4_Especificacion_Corregida.md'   # §2.3.1 / §2.3.2
su -c 'grep -an "Fase 2" /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/docs/SGM_ROADMAP.md'
su -c 'cat /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/results/experiment_registry.json'
```
Explain the plan + prior results in criollo to the user BEFORE writing code.

## 1. Write the script (heredoc inside su, absolute paths, no outer-shell vars)
```sh
su -c 'cat > /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/phases/phase2_inferencia/run_X.py <<"PYEOF"
# -*- coding: utf-8 -*-
import math, random, json
D=16; SEED=42; THETA_REFUT=2.0
def pain(A,V): return max(0.0, A-V)*1.0
# ... mechanism under test ...
def main():
    rA=...; rB=...; rC=...
    overall = pass_A and pass_B and pass_C
    result={"experiment_id":"exp_SGM_00NN","experiment_name":"...",
            "phase":"Fase 2 - Inferencia simbolica + duda","date":"2026-08-02",
            "hypothesis":"...","config":{...},"result":{...},
            "script":"phases/phase2_inferencia/run_X.py",
            "results_file":"phases/phase2_inferencia/results_exp_SGM_00NN_X.json",
            "test_target":"T-INF-0X (...)",
            "notes":"...","notes_criollo":"..."}
    with open("/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/phases/phase2_inferencia/results_exp_SGM_00NN_X.json","w") as f:
        json.dump(result,f,indent=2,ensure_ascii=False)
    print("PASS:",overall)
    return result
if __name__=="__main__": main()
PYEOF
chown root:everybody /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/phases/phase2_inferencia/run_X.py
chmod 664 /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/phases/phase2_inferencia/run_X.py'
```

## 2. Smoke test + run (with the LD_LIBRARY_PATH fix)
```sh
su -c 'export LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib; PY=/data/data/com.hermesagent.android/files/usr/bin/python3; S=/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/phases/phase2_inferencia/run_X.py; $PY -c "import py_compile; py_compile.compile(\"$S\", doraise=True)" && $PY "$S"'
```

## 3. Honest PASS gate (critical)
- A scenario that ends in its target state via TIMEOUT, not via the intended mechanism, is
  NOT a valid test. Check the mechanism's counter (e.g. doubt_count) — if it is 0 but the
  end-state is "INCONCLUSA", the test did not actually exercise doubt; rewrite the scenario
  so the mechanism truly fires (trap the chain in few nodes + contract the window).
- Negative control MUST stay in its "no fire" state (low pain -> not CONTRADICTORIA; free
  exploration -> not INCONCLUSA).

## 4. Register + mirror + push
```sh
su -c 'export LD_LIBRARY_PATH=...; PY=...; $PY - <<PYEOF
import json, re
p="/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/results/experiment_registry.json"
d=json.load(open(p)); d.append(entry); d.sort(key=lambda e:int(re.search(r"(\d+)",e["experiment_id"].split("_")[-1]).group(1)))
json.dump(d,open(p,"w"),indent=2,ensure_ascii=False)
PYEOF'
su -c 'SGM=.../SGM; cp phases/phase2_inferencia/run_X.py experiments/; cp phases/phase2_inferencia/results_exp_SGM_00NN_X.json results/; rm -rf phases/phase2_inferencia/__pycache__'
su -c 'export LD_LIBRARY_PATH=...; PY=...; cd /data/user/0/com.hermesagent.android/files/home; $PY github_push_sgm.py Rylow999 "<TOKEN>"'
```

## 5. If you deleted/renamed a vault file, sync GitHub
The push script only PUTs. For a removed file: DELETE via GitHub API (recipe in
android-env-ops "Deleting a file from GitHub"). For a renamed PDF: mv in vault + update the
literature index line + DELETE the old name from GitHub.

## Key equations referenced
- Eq.6  E_i = max(0, A_i - V_i) * kappa        (pain / valence)
- Eq.8  W(t) = W_base / (1 + kappa_W * E_root) (context window contracts with root pain)
- §2.3.1 contradiction: sum(E over trajectory) > theta_refut(2.0) -> CONTRADICTORIA, relaunch
         with phi_root -> phi* + pi, cooldown 5 ticks. Fires DURING traversal (not post-hoc).
- §2.3.2 doubt: novelty = unique_nodes_in_window / W(t) (COUNT, never averaged omega). If
         novelty < theta_novelty(0.30) while window contracted -> handle_doubt escalates
         relax -> relaunch -> abandon = INCONCLUSA.
- Three end-states must stay distinct: DETERMINADO (success), CONTRADICTORIA (pain, evidence
  against), INCONCLUSA (stuck, no evidence against).
