#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Push incremental para repo SGM-CORE.
# USO: python3 github_push_sgm.py <usuario> <token> [ruta_rel...]
#   Si no se pasan rutas, sube TODO EXPERIMENTOS/SGM/ (excepto lo ignorado).
# KNOWN-GOOD VERSION (bugs fixed):
#   - no saltea archivos ocultos (sube .gitignore, LICENSE)
#   - .gitignore parseado como RUTA RELATIVA (no absoluta) -> si .gitignore tiene
#     "lit/papers/", se excluye correctamente (normpath le quita la barra final,
#     por eso el check usa ig + "/" en vez de exigir que termine en "/")
#   - excluye __pycache__ y *.pyc
# NOTA: este script hace PUT (upsert) pero NO borra en GitHub. Si borras algo del
# vault, hacelo DELETE por API en GitHub aparte.
import sys, os, json, base64, urllib.request, urllib.error
API="https://api.github.com"
BASE="/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM"
REPO="SGM-CORE"
def req(method,url,token,data=None):
    h={"Authorization":f"token {token}","Accept":"application/vnd.github+json","User-Agent":"x"}
    b=json.dumps(data).encode() if data is not None else None
    r=urllib.request.Request(url,data=b,headers=h,method=method)
    try:
        with urllib.request.urlopen(r) as resp: return resp.read().decode(),resp.status
    except urllib.error.HTTPError as e: return e.read().decode(),e.code
def _get(url,token):
    h={"Authorization":f"token {token}","User-Agent":"x"}
    return urllib.request.urlopen(urllib.request.Request(url,headers=h)).read().decode()
def _put(user,token,rel,fp):
    with open(fp,"rb") as fh: content=base64.b64encode(fh.read()).decode()
    url=f"{API}/repos/{user}/{REPO}/contents/{rel}"
    _,st=req("GET",url,token)
    data={"message":f"add/update {rel}","content":content}
    if st==200:
        try: data["sha"]=json.loads(_get(url,token))["sha"]
        except: pass
    _,s=req("PUT",url,token,data)
    print(f"  {rel}: {s}")
def main():
    user,token=sys.argv[1],sys.argv[2]
    paths=sys.argv[3:]
    if not paths:
        ignore=set()
        gi=os.path.join(BASE,".gitignore")
        if os.path.isfile(gi):
            for line in open(gi):
                line=line.strip()
                if line and not line.startswith("#"): ignore.add(os.path.normpath(line).replace(os.sep,"/"))
        for root,dirs,files in os.walk(BASE):
            for f in files:
                if f == "__pycache__" or f.endswith(".pyc"): continue
                rel=os.path.relpath(os.path.join(root,f),BASE).replace(os.sep,"/")
                skip=False
                for ig in ignore:
                    if rel == ig or rel.startswith(ig + "/") or rel == ig.rstrip("/"):
                        skip=True; break
                if skip or rel in ignore or f in ignore: continue
                _put(user,token,rel,os.path.join(root,f))
        print("PUSH SGM-CORE TERMINADO (arbol completo)")
        return
    for p in paths:
        full=os.path.join(BASE,p)
        if os.path.isdir(full):
            for root,_,files in os.walk(full):
                for f in files:
                    if f == "__pycache__" or f.endswith(".pyc"): continue
                    fp=os.path.join(root,f)
                    rel=os.path.relpath(fp,BASE).replace(os.sep,"/")
                    _put(user,token,rel,fp)
        else:
            rel=p.replace(os.sep,"/")
            _put(user,token,rel,full)
    print("PUSH SGM-CORE TERMINADO")
if __name__=="__main__":
    if len(sys.argv)<3: print("USO: github_push_sgm.py <user> <token> [ruta...]"); sys.exit(1)
    main()
