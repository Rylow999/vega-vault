#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.3b v2 — MEMORIA con metrica CORREGIDA de 'borrar'.
El v0.3b original usaba eval que ignoraba vectores nulos -> 'borrar' subia (artefacto).
Aca: eval sobre la SECUENCIA COMPLETA (todos los targets, incluso los borrados).
Si un nodo se borra (omega=0), el sistema YA NO PUEDE predecirlo -> error en esos
targets -> accuracy BAJA. Si se hiberna (omega vive), se puede predecir -> = base.
Esto captura 'perder acceso' de verdad.
"""
import json, math, random, re, time
D=16; V=150; BETA=0.10; EPOCHS=3; SEED=0
def tok(t): return re.findall(r"[a-záéíóúñü]+", t.lower())
def build_vocab(words,V):
    from collections import Counter
    return [w for w,_ in Counter(words).most_common(V)]
def cos(a,b):
    na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(x*x for x in b))
    return 0.0 if na<1e-9 or nb<1e-9 else sum(x*y for x,y in zip(a,b))/(na*nb)
def acc_full(vocab,omega,seq):
    idx={w:i for i,w in enumerate(vocab)}
    ok=tot=0
    for i in range(1,len(seq)):
        if seq[i-1] not in idx or seq[i] not in idx: continue
        q=omega[idx[seq[i-1]]]; excl={seq[i-1]}; best,bv=-1,-1.0
        for j,o in enumerate(omega):
            if vocab[j] in excl: continue
            s=cos(q,o)
            if s>bv: bv=s; best=j
        if vocab[best]==seq[i]: ok+=1
        tot+=1
    return ok/tot if tot else 0
def main():
    print("=== v0.3b v2 MEMORIA (metrica borrar corregida) ===")
    rng=random.Random(SEED)
    text=open("/data/user/0/com.hermesagent.android/files/home/donquijote.txt",encoding="utf-8",errors="ignore").read()
    words=tok(text); vocab=build_vocab(words,V)
    omega=[[rng.gauss(0,1) for _ in range(D)] for _ in range(V)]
    seq=[w for w in words if w in set(vocab)]
    idx={w:i for i,w in enumerate(vocab)}
    t0=time.time()
    for ep in range(EPOCHS):
        for i in range(1,len(seq)):
            a,b=idx[seq[i-1]],idx[seq[i]]
            omega[a]=[(1-BETA)*omega[a][k]+BETA*omega[b][k] for k in range(D)]
    print(f"train {time.time()-t0:.0f}s")
    base=acc_full(vocab,omega,seq)
    nodes=list(range(V)); rng.shuffle(nodes); half=nodes[:V//2]
    omega_h=[list(o) for o in omega]
    omega_d=[list(o) for o in omega]
    for i in half: omega_d[i]=[0.0]*D
    acc_h=acc_full(vocab,omega_h,seq)
    acc_d=acc_full(vocab,omega_d,seq)
    out=dict(experiment="v0.3b_v2_memoria_metrica_corr",
             hypothesis="Hibernar (omega vive) mantiene accuracy; borrar (omega=0) la DESTRUYE porque el sistema pierde acceso al concepto.",
             params=dict(d=D,V=V,beta=BETA,epochs=EPOCHS),
             acc_base=round(base,4), acc_hibernado=round(acc_h,4), acc_borrado=round(acc_d,4),
             memoria_real=(abs(acc_h-base)<0.01 and acc_d<acc_h-0.01))
    json.dump(out,open("results_v03b_v2.json","w"),indent=2)
    print(f"base={base:.4f} hibernado={acc_h:.4f} borrado={acc_d:.4f}")
    print("\n-> results_v03b_v2.json")
if __name__=="__main__": main()
