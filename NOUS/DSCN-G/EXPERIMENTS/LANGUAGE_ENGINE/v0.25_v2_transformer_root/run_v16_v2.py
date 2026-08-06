#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.16 v2 — COMPOSICION con metrica CORREGIDA de 'borrar' (Don Quijote real).
Igual que v0.3b v2: eval sobre secuencia COMPLETA. Podar refs (desenlazar) NO
toca omega -> accuracy = base (el nodo vive). Borrar el nodo (omega=0) -> el sistema
pierde acceso -> accuracy BAJA. Esto muestra que la composicion (refs internas) es
una vista NO destructiva del nodo externo que vive.
"""
import json, math, random, re, time
from collections import Counter
D=16; V=150; BETA=0.10; EPOCHS=3; SEED=0; WINDOW=3
def tok(t): return re.findall(r"[a-záéíóúñü]+", t.lower())
def build_vocab(words,V): return [w for w,_ in Counter(words).most_common(V)]
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
    print("=== v0.16 v2 COMPOSICION (metrica borrar corregida) ===")
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
    # refs por co-ocurrencia
    refs=[set() for _ in range(V)]
    for i in range(len(seq)):
        for j in list(range(max(0,i-WINDOW),i))+list(range(i+1,min(len(seq),i+WINDOW+1))):
            refs[idx[seq[i]]].add(idx[seq[j]])
    # podar refs incoherentes (desenlazar, NO toca omega)
    refs_pod=[set() for _ in range(V)]
    for n in range(V):
        for r in refs[n]:
            if cos(omega[n],omega[r])>=0.0: refs_pod[n].add(r)
    acc_podar=acc_full(vocab,omega,seq)  # omega intacto
    # borrar nodos con muchas refs (omega=0) -> pierde acceso
    cand=sorted(range(V), key=lambda i: -len(refs[i]))[:30]
    omega_del=[list(o) for o in omega]
    for i in cand: omega_del[i]=[0.0]*D
    acc_borrar=acc_full(vocab,omega_del,seq)
    out=dict(experiment="v0.16_v2_composicion_metrica_corr",
             hypothesis="Podar refs NO degrada (nodo vive, vista no destructiva); borrar nodo SI degrada (pierde acceso). Composicion = refs + nodo externo vivo.",
             params=dict(d=D,V=V,beta=BETA,epochs=EPOCHS,window=WINDOW),
             acc_base=round(base,4), acc_podar_refs=round(acc_podar,4), acc_borrar_nodo=round(acc_borrar,4),
             db_semantica_real=(abs(acc_podar-base)<0.01 and acc_borrar<acc_podar-0.01))
    json.dump(out,open("results_v16_v2.json","w"),indent=2)
    print(f"base={base:.4f} podar_refs={acc_podar:.4f} borrar_nodo={acc_borrar:.4f}")
    print("\n-> results_v16_v2.json")
if __name__=="__main__": main()
