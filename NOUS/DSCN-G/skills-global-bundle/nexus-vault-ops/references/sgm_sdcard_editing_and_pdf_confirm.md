# SGM vault: editing /sdcard in-place + confirming PDF identity

Two techniques confirmed working 2026-08-02 on this Android host (Hermes app shell
cannot `read_file`/`write_file`/`patch` paths under `/sdcard/Hermes/...`; only `su -c`
sees them).

## 1. Confirm a mislabeled PDF's TRUE identity with PyPDF2

`strings` and `pdfinfo` are unreliable on FlateDecode-compressed PDFs: they return
garbage or an EMPTY `/Title`. The filename and the literature index can BOTH be wrong.
The only sure check is to extract the actual text.

PyPDF2 is present in the `su` python (no pip install needed). Recipe:

```sh
su -c 'export LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib; /data/data/com.hermesagent.android/files/usr/bin/python3 -c "
import PyPDF2
F=\"/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/lit/papers/wrong_id/hipporag_v2_2025.pdf\"
r=PyPDF2.PdfReader(F)
print(\"PAGINAS:\", len(r.pages))
if r.metadata:
    for k,v in r.metadata.items(): print(\"META\",k,\":\",v)
txt=\"\"
for i,pg in enumerate(r.pages[:3]):
    try: txt += pg.extract_text() or \"\"
    except Exception as e: txt += \"[err %d: %s]\"%(i,e)
print(txt[:2500])
"'
```

REAL EXAMPLE (2026-08-02): `wrong_id/hipporag_v2_2025.pdf` had empty Title and `strings`
showed nothing useful. PyPDF2 extracted the title **"SNAP: Stopping Catastrophic Forgetting
in Hebbian Learning with Sigmoidal Neuronal Adaptive Plasticity"** (McGill University,
Tianyi Xu et al., 2024-10-22). So it was NOT HippoRAG2 — it was SNAP. Action taken:
renamed to `snap_2024.pdf`, moved OUT of `wrong_id/` (it is a real, relevant paper on
Hebbian catastrophic forgetting — directly relevant to SGM Fase 4 Planificacion /
hibernacion), and updated `SGM_literature_index.md`.

Rule: if you cannot confirm what a PDF IS from its extracted text, DO NOT delete it.
Leave it in place (or in wrong_id/) pending user confirmation.

## 2. Edit a /sdcard vault file IN-PLACE with sed inside su -c

`patch` and `read_file` cannot target `/sdcard/...`. `write_file` writes only to Hermes
home. So to edit a vault file in place, use `sed -i` inside `su -c`.

- Android's `sed` is toybox and ACCEPTS `-i` (no GNU `--in-place` quirks).
- Use `|` as the s/// delimiter so file paths containing `/` need no escaping.
- Verify immediately after with `sed -n` / `grep` inside `su -c`.

Single-line replace:
```sh
su -c 'sed -i "s|OLD TEXT|NEW TEXT|" /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/docs/SGM_literature_index.md'
su -c 'grep -n "NEW TEXT" /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/docs/SGM_literature_index.md'
```

Multi-line / structural edit (safer with assert):
```python
# write_file this to Hermes home, then su -c 'cp ... /tmp/ && <su-python> /tmp/x.py'
old = "..."   # exact bytes, assert old in s before replace
new = "..."
p = "/sdcard/Hermes/nexus-vault/.../file.md"
s = open(p).read()
assert old in s, "old string not found — check exact bytes with su -c 'sed -n L,Mp'"
open(p,"w").write(s.replace(old, new, 1))
```
Run with: `su -c 'export LD_LIBRARY_PATH=/data/.../usr/lib; /data/.../usr/bin/python3 /tmp/x.py'`

## 3. GitHub push: .gitignore handling

`github_push_sgm.py` had `if f.startswith("."): continue` which SKIPPED `.gitignore`
and any dotfile. Fixed 2026-08-02 to skip only `__pycache__` / `*.pyc`. After fixing,
`.gitignore` and `LICENSE` upload correctly. Also: the script IGNORES `.gitignore` for
the actual upload (it uses its own `ignore` set built from `.gitignore` lines that end
in `/`). So to exclude `lit/papers/` from the repo while KEEPING the PDFs on disk in the
vault, add the line `lit/papers/` to `.gitignore` (the trailing slash makes the script's
`ig.endswith("/")` check exclude it). Then DELETE each PDF from GitHub via the API.
