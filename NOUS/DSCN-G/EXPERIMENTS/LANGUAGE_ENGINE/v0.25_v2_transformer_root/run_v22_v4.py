#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.22 v4 — ROOT DIRECTOR con MARGIN ADAPTATIVO (percentil de top1-top2).
v0.22 v3: proyeccion Hebb rutea perfecto (1.0) pero MATA la duda (Fase B duda=0).
FIX: MARGIN no fijo, sino PERCENTIL p de la distribucion de (top1-top2) en el corpus.
La duda emerge donde la ambiguedad es REAL (cola alta), no por numero a ojo.
Usa W Hebb de v3 (ruteo bueno) + MARGIN adaptativo (recupera duda honesta).
"""
import json, math, random, re, time
from collections import Counter
D=16; WIN=4; K=2; BETA=0.10; BETA_REP=0.20; ALPHA=0.10; LR_W=0.01; EPOCHS_W=3
PCTILES=[70,80,90]; SEED=0
def norm(v): return math.sqrt(sum(x*x for x in v))
def cos(a,b):
    na=norm(a); nb=norm(b)
    return 0.0 if na<1e-9 or nb<1e-9 else sum(x*y for x,y in zip(a,b))/(na*nb)
def mat_vec(M,v): return [sum(M[i][j]*v[j] for j in range(D)) for i in range(D)]
def build_contrast(seed=SEED, n=50):
    rng=random.Random(seed)
    poly={"banco":(["dinero","pagar","cuenta","oro","plata"],["rio","agua","pez","orilla","puente"]),
          "llave":(["puerta","cerradura","abrir","candado"],["musica","nota","tono","cancion"]),
          "mouse":(["computadora","click","pantalla","cable"],["animal","cola","raton","hueco"])}
    filler=["el","la","de","y","en","con","por","un","una","que","los","las"]
    seq=[]; tags=[]
    for w,(sa,sb) in poly.items():
        for _ in range(n):
            c=[rng.choice(filler) for _ in range(3)]+list(sa[:3])+[w]+list(sa[1:3]); seq+=c; tags+=[0]+[0]*(len(c)-1)
        for _ in range(n):
            c=[rng.choice(filler) for _ in range(3)]+list(sb[:3])+[w]+list(sb[1:3]); seq+=c; tags+=[1]+[0]*(len(c)-1)
    pr=list(zip(seq,tags)); rng.shuffle(pr); seq=[p[0] for p in pr]; tags=[p[1] for p in pr]
    return seq,tags,list(dict.fromkeys(seq)),list(poly.keys()),poly
def train_fractal(seq,vocab,epochs):
    Vn=len(vocab); idx={w:i for i,w in enumerate(vocab)}; rng=random.Random(SEED)
    frac=[[[rng.gauss(0,1) for _ in range(D)] for _ in range(K)] for _ in range(Vn)]
    o0=[[list(o) for o in frac[wi]] for wi in range(Vn)]
    for ep in range(epochs):
        for i in range(1,len(seq)):
            a=idx[seq[i-1]]; b=idx[seq[i]]; tb=frac[b][0]
            for k in range(K):
                new=[(1-BETA)*frac[a][k][d]+BETA*tb[d] for d in range(D)]
                new=[ALPHA*o0[a][k][d]+(1-ALPHA)*new[d] for d in range(D)]
                j=1-k; nj=norm(frac[a][j])
                if nj>1e-9: new=[new[d]-BETA_REP*(frac[a][j][d]/nj) for d in range(D)]
                frac[a][k]=new
    return frac,idx
def ctx_vec(frac,idx,seq,i):
    cw=list(range(max(0,i-WIN),i))
    if not cw: return None
    c=[0.0]*D; n=0
    for x in cw:
        for k in range(K):
            for d in range(D): c[d]+=frac[idx[seq[x]]][k][d]
        n+=K
    return [v/n for v in c] if n else None
def train_W(frac,idx,seq,poly_words,use_tags=False,tags=None):
    rng=random.Random(SEED)
    W=[[1.0 if i==j else 0.01*rng.gauss(0,1) for j in range(D)] for i in range(D)]
    for ep in range(EPOCHS_W):
        for i,w in enumerate(seq):
            if w not in idx: continue
            c=ctx_vec(frac,idx,seq,i)
            if c is None: continue
            if use_tags and w in set(poly_words): sense=tags[i]
            else:
                cw=list(range(max(0,i-WIN),i))
                if not cw: continue
                lc=[0.0]*D; n=0
                for x in cw:
                    for k in range(K):
                        for d in range(D): lc[d]+=frac[idx[seq[x]]][k][d]
                    n+=K
                if not n: continue
                lc=[v/n for v in lc]
                sc=[cos(frac[idx[w]][k],lc) for k in range(K)]; sense=max(range(K),key=lambda k:sc[k])
            pc=[v/(norm(c) or 1) for v in c]; ps=frac[idx[w]][sense]; np_=norm(ps)
            if np_>1e-9: ps=[v/np_ for v in ps]
            pc=mat_vec(W,pc); ps=mat_vec(W,ps)
            W=[[W[i][j]+LR_W*pc[i]*ps[j] for j in range(D)] for i in range(D)]
    return W
def route(frac,idx,W,w,c,margin):
    pc=mat_vec(W,c); sc=[cos(mat_vec(W,frac[idx[w]][k]),pc) for k in range(K)]
    o=sorted(range(K),key=lambda k:-sc[k]); return o[0],(sc[o[0]]-sc[o[1]])<margin,round(sc[o[0]],3),round(sc[o[1]],3)
def pct(vals,p):
    s=sorted(v for v in vals if v==v and v is not None)
    if not s: return 0.0
    k=(len(s)-1)*p/100; f=int(k)
    return s[min(f+1,len(s)-1)] if f+1<len(s) else s[0]
def norm(v): return math.sqrt(sum(x*x for x in v)) or 1e-9
def main():
    print("=== v0.22 v4 ROOT DIRECTOR (MARGIN adaptativo, W Hebb) ===")
    t0=time.time()
    seq,tags,vocab,pw,poly=build_contrast()
    frac,idx=train_fractal(seq,vocab,15)
    W=train_W(frac,idx,seq,pw,use_tags=True,tags=tags)
    # FASE A: routing_acc + duda con margin por percentil
    diffs=[]; resA={}
    for i,w in enumerate(seq):
        if w not in set(pw): continue
        c=ctx_vec(frac,idx,seq,i)
        if c is None: continue
        _,_,s1,s2=route(frac,idx,W,w,c,1.0); diffs.append(s1-s2)
    for p in PCTILES:
        m=pct(diffs,p); ok=tot=dud=0
        for i,w in enumerate(seq):
            if w not in set(pw): continue
            c=ctx_vec(frac,idx,seq,i)
            if c is None: continue
            r,d,_,_=route(frac,idx,W,w,c,m); tot+=1; dud+=1 if d else 0
            if not d and r==tags[i]: ok+=1
        resA[str(p)]=dict(margin=round(m,3),routing_acc=round(ok/tot,3) if tot else 0,tasa_duda=round(dud/tot,3) if tot else 0)
    # FASE B Don Quijote
    txt=open("/data/user/0/com.hermesagent.android/files/home/donquijote.txt",encoding="utf-8",errors="ignore").read()
    wr=re.findall(r"[a-záéíóúñü]+",txt.lower()); vocab=[w for w,_ in Counter(wr).most_common(150)]
    ia=[i for i,w in enumerate(wr) if w in set(vocab)]; st=ia[::max(1,len(ia)//20000)][:20000]; seqB=[wr[i] for i in st]
    fB,iB=train_fractal(seqB,vocab,4); WB=train_W(fB,iB,seqB,vocab)
    cnt=Counter(seqB); cand=[w for w in vocab if cnt[w]>=20][:40]
    dB=[]; resB={}
    for i,w in enumerate(seqB):
        if w not in set(cand): continue
        c=ctx_vec(fB,iB,seqB,i)
        if c is None: continue
        _,_,s1,s2=route(fB,iB,WB,w,c,1.0); dB.append(s1-s2)
    for p in PCTILES:
        m=pct(dB,p); dud=tot=0
        for i,w in enumerate(seqB):
            if w not in set(cand): continue
            c=ctx_vec(fB,iB,seqB,i)
            if c is None: continue
            _,d,_,_=route(fB,iB,WB,w,c,m); tot+=1; dud+=1 if d else 0
        resB[str(p)]=dict(margin=round(m,3),tasa_duda=round(dud/tot,3) if tot else 0)
    print(f"train+eval {time.time()-t0:.0f}s")
    print("FASE A (contrastivo) por percentil:",resA)
    print("FASE B (Don Quijote) por percentil:",resB)
    out=dict(experiment="v0.22_v4_margin_adaptativo",
             hypothesis="MARGIN = percentil de top1-top2 recupera la duda SIN perder ruteo (W Hebb). La duda cae en ambiguedad real, no por umbral fijo.",
             params=dict(d=D,window=WIN,k=K,beta=BETA,beta_rep=BETA_REP,alpha=ALPHA,lr_w=LR_W,epochs_w=EPOCHS_W,pctiles=PCTILES),
             fase_A=resA, fase_B=resB,
             duda_emerge=any(resB[str(p)]["tasa_duda"]>0 for p in PCTILES),
             ruteo_mantiene=all(resA[str(p)]["routing_acc"]>0.9 for p in PCTILES))
    json.dump(out,open("results_v22_v4.json","w"),indent=2)
    print("\n-> results_v22_v4.json")
if __name__=="__main__": main()
