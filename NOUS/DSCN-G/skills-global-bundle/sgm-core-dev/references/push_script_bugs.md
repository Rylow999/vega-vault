# github_push_sgm.py — bugs found and fixed

## Bug 1: skipped hidden files (`.gitignore`, `LICENSE` never uploaded)
Original line inside `os.walk`:
```python
for f in files:
    if f.startswith("."): continue   # BUG: also skips .gitignore, .gitattributes
```
Fix: only skip `__pycache__` / `*.pyc`:
```python
if f == "__pycache__" or f.endswith(".pyc"): continue
```

## Bug 2: .gitignore parsed as absolute path -> never matched
`.gitignore` had `lit/papers/`. Old code:
```python
ignore.add(os.path.normpath(os.path.join(BASE, line)))   # -> /sdcard/.../SGM/lit/papers/
...
if any(rel.startswith(ig) or ("/"+ig in "/"+rel) for ig in ignore if ig.endswith("/")):
```
`rel` is RELATIVE (`lit/papers/x.pdf`), `ig` is ABSOLUTE -> never matches, so PDFs kept
re-uploading even after being deleted from GitHub.

Fix: parse `.gitignore` as relative, and check `rel.startswith(ig + "/")` (don't require the
trailing slash, since `os.path.normpath` strips it):

**WHY this bit 3 times:** `os.path.normpath("lit/papers/")` returns `"lit/papers"` (no trailing
slash). The OLD check was `if ig.endswith("/")` — that was always FALSE for the normpath'd value,
so the `rel.startswith(ig)` branch never ran and PDFs re-uploaded on every push even after being
API-deleted from GitHub. The fix drops the `endswith("/")` gate and uses `ig + "/"` at comparison
time. The dry-run snippet below is the ONLY reliable way to confirm the fix before pushing — USE IT.
```python
ignore.add(os.path.normpath(line).replace(os.sep,"/"))   # -> lit/papers
...
skip=False
for ig in ignore:
    if rel == ig or rel.startswith(ig + "/") or rel == ig.rstrip("/"):
        skip=True; break
if skip or rel in ignore or f in ignore: continue
```

## Gotcha: PUT doesn't DELETE
The script only upserts. After deleting a file locally, DELETE it on GitHub via the API
(`DELETE /repos/{user}/{repo}/contents/{path}` with the file's `sha`), or it lingers.

## Gotcha: re-upload loop
If you delete a file locally AND it's in `.gitignore`, the next push won't re-add it (good).
But if it's NOT in `.gitignore`, every push re-creates it on GitHub. So: exclude `lit/papers/` in
`.gitignore` AND delete the PDFs from GitHub once; the repo stays binary-free.
**After fixing the ignore filter, VERIFY, don't assume:** re-run the dry-run snippet (must show 0
PDFs in `would_push`), then push, then GET `https://api.github.com/repos/{user}/{repo}/contents/lit/papers`
and confirm the listing is empty / only the dir is gone. This session pushed 3 times (sgm10/11/12)
before the normpath fix actually stuck — the log line `lit/papers/x.pdf: 201` is the tell.

## Verification snippet (dry-run, no upload)
```python
import os
BASE="/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM"
ignore=set()
for line in open(os.path.join(BASE,".gitignore")):
    line=line.strip()
    if line and not line.startswith("#"): ignore.add(os.path.normpath(line).replace(os.sep,"/"))
would_push=[]
for root,_,files in os.walk(BASE):
    for f in files:
        if f=="__pycache__" or f.endswith(".pyc"): continue
        rel=os.path.relpath(os.path.join(root,f),BASE).replace(os.sep,"/")
        skip=any(rel==ig or rel.startswith(ig+"/") or rel==ig.rstrip("/") for ig in ignore)
        if not skip and rel not in ignore and f not in ignore: would_push.append(rel)
pdfs=[p for p in would_push if p.endswith(".pdf")]
assert not pdfs, pdfs   # must be empty
```

## Bug 3: `IncompleteRead` on flaky connection (GET for "does file exist?")
The script does a `GET` per file before PUT. On a weak/mobile connection the GET response can be
truncated → `http.client.IncompleteRead: IncompleteRead(... bytes read, ... more expected)` and the
whole push dies mid-way (exit 1), uploading only the first few files. This is TRANSITORY — re-running
usually succeeds, but the full-tree push re-sends ~70 files each attempt, so it's fragile.

Workarounds (in order of preference):
1. **Honor Luciano's "no push now, low connection"** — if he says `no hagas push, poca conexión`,
   do NOT push. Local files are safe; nothing is lost. Resume when signal is better.
2. **Push narrow explicit paths** instead of the whole tree:
   `python3 github_push_sgm.py Rylow999 "$TOKEN" path1 path2 path3 ...`
   This skips the `paths`-empty branch (no walk) and only uploads the named files — far fewer bytes,
   far less chance of a mid-GET truncation. Used to recover sgm14 → sgm15 after the network drop.
3. If a full-tree push still truncates, retry; the script upserts (idempotent) so re-pushing the
   whole tree just overwrites what's there.

Note: this is a network/transport issue, not a logic bug in the script — don't "fix" it by changing
the script's GET logic unless Luciano asks. The robust move is explicit-path pushes on bad signal.

## Bug 4: ARGUMENT ORDER — token in the wrong position yields silent 401 on EVERY file
`github_push_sgm.py` parses `sys.argv` as `user=argv[1], token=argv[2], paths=argv[3:]`.
If you call it as `github_push_sgm.py "$TOKEN" path1 path2 ...` (token FIRST), then:
- `user` = the token, `token` = `path1` (a filename), `paths` = the rest.
- Every `PUT` then sends `Authorization: token <filename>` → GitHub returns **401** for all files
  (no "fatal" error, just `201`→`401` flipped in the printed status). It looks like "uploaded nothing".
- The token itself may be perfectly valid (verified separately via API returns 200 + push:true),
  so this is purely the wrong arg position — NOT a revoked/invalid token.

CORRECT call (user first, then token):
```bash
python3 github_push_sgm.py Rylow999 "$TOKEN" path1 path2 path3 ...
```
Quick sanity check BEFORE a big push: confirm the token works with a direct API call, and that
you passed it as `argv[2]` (second positional), not first:
```python
import urllib.request, base64
auth=base64.b64encode(("x-access-token:"+TOKEN).encode()).decode()
# direct GET https://api.github.com/repos/Rylow999/SGM-CORE -> STATUS 200, permissions.push: True
# means token OK; then check your argv order in the push call.
```
Lesson: never assume a 401 means "token dead". First check the call signature. A wrong-order call
fails identically for a perfectly good token. Always be explicit: `Rylow999` is the literal user.
