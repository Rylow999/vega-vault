# SGM Vault Sync & Push — exact recipes (2026-08-02)

## Problem this fixes
Files written to the agent home (`/data/user/0/com.hermesagent.android/files/home/...`)
are invisible to the user's file manager — that path is the Hermes app sandbox. The user
only sees `/sdcard/Hermes/nexus-vault/`. A 2026-08-02 session wasted turns because SGM
was mirrored to `~/EXPERIMENTOS/SGM/` (also invisible). The canonical deliverable is the
vault path below.

## Canonical paths
- Working copy (agent-writable): `/data/user/0/com.hermesagent.android/files/home/rizoma_docs/`
- Vault deliverable (user-visible):   `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/`
- GitHub mirror:                      `Rylow999/SGM-CORE` (branch `main`)

## Sync home -> vault (run after every experiment/doc edit)
```sh
su -c 'SRC=/data/user/0/com.hermesagent.android/files/home/rizoma_docs; \
  DST=/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM; \
  cp -r "$SRC/docs/."        "$DST/docs/"; \
  cp -r "$SRC/experiments/." "$DST/experiments/"; \
  cp -r "$SRC/results/."     "$DST/results/"; \
  cp -r "$SRC/phases/."      "$DST/phases/"; \
  cp -r "$SRC/lit/."         "$DST/lit/"; \
  cp    "$SRC/README_SGM.md"  "$DST/"; \
  chown -R root:everybody "$DST"; \
  chmod -R u+rwX,g+rwX,o+rX "$DST"; \
  echo "vault SGM sync done: $(find "$DST" -type f | wc -l) files"'
```
`~/sync_vault.sh` wraps exactly this. It must run via `su` (FUSE).

## Push vault -> GitHub SGM-CORE
`github_push_sgm.py` reads BASE from the vault path above (hardcoded absolute — NEVER
use `os.path.expanduser("~/...")` inside `su -c`, it resolves to root's home and uploads
nothing). Token is passed per-message, never persisted.
```sh
su -c 'export LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib; \
  PY=/data/data/com.hermesagent.android/files/usr/bin/python3; \
  TOKEN="<PAT>"; cd /data/user/0/com.hermesagent.android/files/home; \
  $PY github_push_sgm.py Rylow999 "$TOKEN"'
```
Verify after push (catches the empty-repo / expanduser bug):
```sh
GET https://api.github.com/repos/Rylow999/SGM-CORE/git/trees/main?recursive=1
# 409 "Git Repository is empty" => push uploaded nothing, fix BASE and re-run
```

## Permission recipe so the user can open vault files
After any `cp`/`mkdir` into `/sdcard/Hermes/...` as root:
`chown -R root:everybody <path>` then `chmod -R u+rwX,g+rwX,o+rX <path>`.
Note FUSE may still block the unprivileged app user on some paths; if the user reports
"can't open", re-apply chown/chmod and confirm via `su -c 'ls -la <path>'`.
