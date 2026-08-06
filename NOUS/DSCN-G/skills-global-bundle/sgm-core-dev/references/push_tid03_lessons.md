# Push lessons from T-ID-03 (exp_SGM_0035 / 0035b / 0035c) — 2026-08-05

## Symptom → cause map (all hit during this push)

| Symptom | Real cause | Fix |
|---|---|---|
| EVERY file 404 (whole tree AND explicit-path) | Wrong repo user — assumed `VegaBla/SGM-CORE`; token actually belongs to `Rylow999` | Before pushing, `GET https://api.github.com/user` to read `login`; push to `Rylow999/SGM-CORE` |
| 404 on a specific file passed as absolute `/sdcard/...` path | Script does `os.path.join(BASE, p)`; absolute path → doubled non-existent path | Pass RELATIVE paths only (`phases/...`, `results/...`, `README.md`) |
| 409 on an EXISTING file (registry, README, tid03c) | Script PUT without sha (GET didn't return 200 in that run, or file already existed from a truncated run) | Re-run the SAME explicit-path list; second GET now sees 200, grabs sha, PUT updates → 200 |
| `DOCUMENTATION/NOUS_Filosofico.md` 404/409 from repo root | Repo has no `DOCUMENTATION/` dir at root; local vault path ≠ repo path | NOUS_Filosofico lives at `docs/NOUS_Filosofico.md` in `Rylow999/SGM-CORE` |
| `../../DOCUMENTATION/NOUS_Filosofico.md` FileNotFoundError | `os.path.join(BASE, "../../DOCUMENTATION/...")` does not normalize `..` | Copy to `BASE/_staging/DOCUMENTATION/NOUS_Filosofico.md`, push as `DOCUMENTATION/NOUS_Filosofico.md`, then `rm -rf BASE/_staging`; OR use a standalone urllib PUT to `docs/NOUS_Filosofico.md` |

## Pre-push verification recipe (run BEFORE the big push)
```python
import urllib.request, json
API="https://api.github.com"; TOK="<token>"
def get(u):
    r=urllib.request.Request(u,headers={"Authorization":f"token {TOK}","User-Agent":"x","Accept":"application/vnd.github+json"})
    try: return json.loads(urllib.request.urlopen(r).read()),200
    except Exception as e: return None,getattr(e,"code",None)
print("USER:", get(f"{API}/user")[0]["login"])                       # must be Rylow999
print("REPO:", get(f"{API}/repos/Rylow999/SGM-CORE")[1])             # must be 200
```

## Correct invocations
- Explicit-path batch (preferred): `github_push_sgm.py Rylow999 $TOKEN phases/phase7_composicion/run_identity_tid03c.py results/experiment_registry.json README.md`
- Full tree (fragile, avoid on bad network): `github_push_sgm.py Rylow999 $TOK` with NO paths.
- Out-of-BASE doc (NOUS_Filosofico): standalone PUT to `docs/NOUS_Filosofico.md`:
```python
import base64,json,urllib.request,urllib.error,sys
API="https://api.github.com";USER="Rylow999";TOK=sys.argv[1];REPO="SGM-CORE";REL="docs/NOUS_Filosofico.md"
FP="/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/_staging/DOCUMENTATION/NOUS_Filosofico.md"
def req(m,u,d=None):
    h={"Authorization":f"token {TOK}","Accept":"application/vnd.github+json","User-Agent":"x"}
    b=json.dumps(d).encode() if d is not None else None
    r=urllib.request.Request(u,data=b,headers=h,method=m)
    try:
        with urllib.request.urlopen(r) as resp: return resp.read().decode(),resp.status
    except urllib.error.HTTPError as e: return e.read().decode(),e.code
with open(FP,"rb") as fh: content=base64.b64encode(fh.read()).decode()
url=f"{API}/repos/{USER}/{REPO}/contents/{REL}"
body,st=req("GET",url); data={"message":"add NOUS_Filosofico cap10","content":content}
if st==200:
    try: data["sha"]=json.loads(body)["sha"]
    except Exception: pass
print(REL, req("PUT",url,data)[1])
```

## Token hygiene
Token is given per-message, NEVER persisted (Luciano deletes it after the docs pass). Do not store it in
memory or files. Use it only for that session's push.
