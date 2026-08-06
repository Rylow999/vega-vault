#!/usr/bin/env python3
import math, random, re, time
D=8; V=150; W=4; LR=0.05; SEED=0; CORPUS_N=5000; BETA=0.10
def tok(t): return re.findall(r"[a-záéíóúñü]+", t.lower())
def build_vocab(words, V):
    from collections import Counter
    return [w for w,_ in Counter(words).most_common(V)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def mat_vec(M,v): return [dot(M[i],v) for i in range(len(M))]
def vec_add(a,b,a2=1.0): return [a[i]+a2*b[i] for i in range(len(a))]
def scale(v,s): return [x*s for x in v]
def softmax_logits(logits):
    mx=max(logits); ex=[math.exp(l-mx) for l in logits]; s=sum(ex); return [e/s for e in ex]
def norm(v): return math.sqrt(sum(x*x for x in v))

text=open("/data/user/0/com.hermesagent.android/files/home/donquijote.txt",encoding="utf-8",errors="ignore").read()
words=tok(text)[:CORPUS_N*2]; vocab=build_vocab(words,V)
rng=random.Random(SEED)
omega=[[rng.gauss(0,1) for _ in range(D)] for _ in range(V)]
seq=[w for w in words if w in set(vocab)][:CORPUS_N]
idx={w:i for i,w in enumerate(vocab)}
for i in range(1,len(seq)):
    a,b=seq[i-1],seq[i]; ia,ib=idx[a],idx[b]
    omega[ia]=[(1-BETA)*omega[ia][k]+BETA*omega[ib][k] for k in range(D)]
# dispersion de omega_base: distancia media entre pares distintos
import itertools
ds=[norm([omega[i][d]-omega[j][d] for d in range(D)]) for i,j in itertools.islice(itertools.combinations(range(V),2),200)]
print("dispersion media omega_base (deberia ser >0.5 si hay identidad):",round(sum(ds)/len(ds),3))
# transformer
def rnd_mat(): return [[rng.gauss(0,0.3) for _ in range(D)] for _ in range(D)]
Wq=rnd_mat(); Wk=rnd_mat(); Wv=rnd_mat()
def loss_at(step):
    ctx=[omega[idx[seq[step-W+j]]] for j in range(W)]
    Q=[mat_vec(Wq,ctx[t]) for t in range(W)]
    K=[mat_vec(Wk,ctx[t]) for t in range(W)]
    VV=[mat_vec(Wv,ctx[t]) for t in range(W)]
    H=[None]*W; atts=[None]*W
    for t in range(W):
        scores=[dot(Q[t],K[s])/math.sqrt(D) for s in range(t+1)]
        a=softmax_logits(scores); atts[t]=a
        h=[0.0]*D
        for s in range(t+1): h=vec_add(h,VV[s],a[s])
        H[t]=h
    hlast=H[-1]; logits=[dot(hlast,omega[j]) for j in range(V)]
    target=idx[seq[step]]; probs=softmax_logits(logits)
    return -math.log(probs[target]+1e-12)
print("loss inicial (paso 10):", round(loss_at(10),3))
# entrenar 3000 pasos, medir loss
for step in range(W, W+3000):
    ctx=[omega[idx[seq[step-W+j]]] for j in range(W)]
    Q=[mat_vec(Wq,ctx[t]) for t in range(W)]
    K=[mat_vec(Wk,ctx[t]) for t in range(W)]
    VV=[mat_vec(Wv,ctx[t]) for t in range(W)]
    H=[None]*W; atts=[None]*W
    for t in range(W):
        scores=[dot(Q[t],K[s])/math.sqrt(D) for s in range(t+1)]
        a=softmax_logits(scores); atts[t]=a
        h=[0.0]*D
        for s in range(t+1): h=vec_add(h,VV[s],a[s])
        H[t]=h
    hlast=H[-1]; logits=[dot(hlast,omega[j]) for j in range(V)]
    target=idx[seq[step]]; probs=softmax_logits(logits)
    d_logits=[p for p in probs]; d_logits[target]-=1.0
    d_hlast=[0.0]*D
    for j in range(V): d_hlast=vec_add(d_hlast,omega[j],d_logits[j])
    d_Wv=[[0.0]*D for _ in range(D)]; d_VV=[[0.0]*D for _ in range(W)]
    a_last=atts[W-1]
    for s in range(W): d_VV[s]=scale(d_hlast,a_last[s])
    d_att=[dot(d_hlast,VV[s]) for s in range(W)]
    sum_ad=sum(a_last[k]*d_att[k] for k in range(W))
    d_scores=[a_last[s]*(d_att[s]-sum_ad) for s in range(W)]
    d_Q=[[0.0]*D for _ in range(W)]; d_K=[[0.0]*D for _ in range(W)]
    for s in range(W):
        d_Q[W-1]=vec_add(d_Q[W-1],K[s],d_scores[s]/math.sqrt(D))
        d_K[s]=vec_add(d_K[s],Q[W-1],d_scores[s]/math.sqrt(D))
    for t in range(W):
        for i in range(D):
            for jj in range(D): Wq[i][jj]-=LR*d_Q[t][i]*ctx[t][jj]
    for s in range(W):
        for i in range(D):
            for jj in range(D):
                Wk[i][jj]-=LR*d_K[s][i]*ctx[s][jj]; Wv[i][jj]-=LR*d_VV[s][i]*ctx[s][jj]
print("loss tras 3000 pasos (paso 3010):", round(loss_at(3010),3))
