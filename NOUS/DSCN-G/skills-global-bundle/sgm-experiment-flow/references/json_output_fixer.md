# JSON Output Discipline — SGM results_exp files (bug recurrente 0049-0052, 2026-08-03)

## The bug
Several `run_*.py` experiments did `print("CLIMA ... | comunicacion ...")` debug lines
and THEN `print(json.dumps(out, indent=2))` at the end. The redirect `> /tmp/00XX.out`
captures everything, so the saved `results_exp_SGM_00XX.json` looks like:

```
CLIMA cielo_estrellado | puente 15 | comunicacion 0.0 NC 0.0 | ...
CLIMA competencia | ...
{ "experiment_id": "exp_SGM_00XX", ... }
EXIT=0
```

That file is NOT valid JSON. `json.load()` raises; any downstream tool that syncs the
registry / mirrors the file breaks silently.

## Prevention (do this in new experiments)
Write the JSON with `open(path,"w").write(json.dumps(out,indent=2))`, never via print.
Keep debug `print()` for stderr or a separate `.log` file. This is the only robust fix.

## Fixer (when already contaminated)
Scan from the LAST `{` backwards; for each candidate start, take the substring to EOF
(stripping a trailing `EXIT=0`) and try `json.loads`. The first that parses is the real
result JSON. Rewrite the file with only that substring; keep a `.bak`.

Reusable script (run under `su` because /sdcard is FUSE):

```python
import os, json
files = [ "results_exp_SGM_0049_lenguaje.json", "results_exp_SGM_0049c_lenguaje_bfs.json",
          "results_exp_SGM_0049d_cierre.json", "results_exp_SGM_0050_loop.json",
          "results_exp_SGM_0051_telar.json", "results_exp_SGM_0051b_telar.json",
          "results_exp_SGM_0052_eventos_telar.json" ]
def extract(text):
    text = text.strip()
    if text.endswith("EXIT=0"): text = text[:-6].rstrip()
    last = text.rfind("{")
    while last != -1:
        cand = text[last:]
        if cand.rstrip().endswith("}"):
            try: return cand, json.loads(cand)
            except Exception: pass
        last = text.rfind("{", 0, last)
    return None, None
for f in files:
    raw = open(f, encoding="utf-8").read()
    cand, obj = extract(raw)
    if cand is None:
        print("NO JSON", f); continue
    open(f+".bak","w",encoding="utf-8").write(raw)
    open(f,"w",encoding="utf-8").write(cand)
    print("FIXED", f, "->", len(cand), "bytes")
```

Note: 0049b had NO JSON file (only a log), so it is correctly skipped.
Verify after: `python3 -c "import json;json.load(open(f))"` for each.
