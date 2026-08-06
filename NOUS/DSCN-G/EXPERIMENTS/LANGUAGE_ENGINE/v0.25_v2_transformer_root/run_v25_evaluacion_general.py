#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.25 EVALUACION GENERAL — Don Quijote real, palabra 'tiempo'.
Consolidación final:
- Sustrato real: skip-gram acotado
- Sentido: k-means como pseudo-ground-truth
- Clasificador lineal sobre embeddings reales
- Generación condicionada al sentido (bigrama por cluster)
- Loop generativo con memoria competitiva
Métricas: acc_sentido, pureza_vocabulario, coherencia_loop,Top-10 embeddings.
"""
import json, math, random, re
from collections import defaultdict, Counter

random.seed(0)

WORD="tiempo"
W_CTX=8; W_EMB=3; D=32; EPOCHS_SG=5; NEG=5; K=3

# ---------- carga ----------
with open("donquijote.txt", encoding="utf-8") as f:
    text=f.read().lower(); text=re.sub(r"[^\w\sáéíóúüñ]"," ",text)
seq=text.split()
print(f"tokens totales={len(seq)}")

indices=[i for i,w in enumerate(seq) if w==WORD]
print(f"ocurrencias '{WORD}'={len(indices)}")

# subcorpus acotado: fragmentos únicos de ~60 tokens alrededor de cada ocurrencia
L=60; used=set(); sub=[]
for idx in indices:
    start=max(0, idx-L//2); end=min(len(seq), idx+L//2)
    key=(start,end)
    if key in used: continue
    used.add(key); sub.extend(seq[start:end])
print(f"subcorpus tokens={len(sub)} fragmentos={len(used)}")

acotado_vocab=sorted(set(sub))
print(f"vocab acotado={len(acotado_vocab)}")

# ---------- A) skip-gram acotado ----------
print("\n[A] Entrenando skip-gram acotado...")
emb={w:[random.gauss(0,0.1) for _ in range(D)] for w in acotado_vocab}
ctx={w:[random.gauss(0,0.1) for _ in range(D)] for w in acotado_vocab}
rng=random.Random(1)

sub_idx=[acotado_vocab.index(w) for w in sub]

for ep in range(EPOCHS_SG):
    for i in range(len(sub)):
        target=sub[i]
        start=max(0,i-W_EMB); end=min(len(sub),i+W_EMB+1)
        for j in range(start,end):
            if j==i: continue
            context=sub[j]
            if context not in ctx or context==target: continue
            for d in range(D): emb[target][d]+=0.01*(ctx[context][d]-emb[target][d])
            neg=rng.sample(acotado_vocab, min(NEG, len(acotado_vocab)))
            for ns in neg:
                for d in range(D): emb[target][d]-=0.01*ctx[ns][d]

# top-10 más cercanos a WORD
vt=emb.get(WORD, [0.0]*D)
sims=[]
for w in acotado_vocab:
    if w==WORD: continue
    na=math.sqrt(sum(x*x for x in vt)); nb=math.sqrt(sum(x*x for x in emb[w]))
    sim=sum(a*b for a,b in zip(vt,emb[w]))/((na*nb)+1e-9)
    sims.append((sim,w))
top10=[(float(s),str(w)) for s,w in sorted(sims, reverse=True)[:10]]
print("Top-10 cercanos a '"+WORD+"':", [w for _,w in top10])

# ---------- B) k-means sobre contextos BoW ----------
print("\n[B] K-means sobre contextos bag-of-words...")
bow=[]; positions=[]
for idx in indices:
    ctx=seq[max(0,idx-W_CTX):idx]
    vec=[0.0]*len(acotado_vocab)
    for w in ctx:
        if w in acotado_vocab:
            vec[acotado_vocab.index(w)]=1.0
    bow.append(vec); positions.append(idx)

def norm(v): return math.sqrt(sum(x*x for x in v))
def cos(a,b):
    na=norm(a); nb=norm(b)
    return 0.0 if na<1e-9 or nb<1e-9 else sum(x*y for x,y in zip(a,b))/(na*nb)

centroids=random.sample(bow, min(K, len(bow)))
labels=[0]*len(bow)
for it in range(25):
    clusters=[[] for _ in range(K)]
    for idx,x in enumerate(bow):
        sims_c=[cos(x,c) for c in centroids]
        labels[idx]=max(range(K), key=lambda i: sims_c[i])
        clusters[labels[idx]].append(x)
    centroids=[]
    for k_ in range(K):
        if clusters[k_]:
            centroids.append([sum(x[j] for x in clusters[k_])/len(clusters[k_]) for j in range(len(bow[0]))])
        else:
            centroids.append([0.0]*len(bow[0]))
counts=Counter(labels)
coh={}
for k_ in range(K):
    pts=[x for x,l in zip(bow,labels) if l==k_]
    coh[k_]=sum(cos(p,centroids[k_]) for p in pts)/len(pts) if pts else 0.0
print(f"cluster sizes={dict(counts)} cohesion={ {k:round(v,3) for k,v in coh.items()} }")

# ---------- C) Clasificador de sentido sobre embeddings reales ----------
print("\n[C] Clasificador lineal sobre embeddings skip-gram...")
X=[]; Y=[]; pos_list=[]
for idx,label in zip(positions, labels):
    ctx=seq[max(0,idx-W_CTX):idx]
    vec=[0.0]*D; valid=0
    for w in ctx:
        if w in emb:
            for d in range(D): vec[d]+=emb[w][d]
            valid+=1
    if valid>0: vec=[x/valid for x in vec]
    X.append(vec); Y.append(label); pos_list.append(idx)

split=max(1, int(0.7*len(X)))
Xtr,Xte=X[:split],X[split:]; ytr,yte=Y[:split],Y[split:]
class Linear:
    def __init__(self, D, lr=0.05):
        self.D=D; self.lr=lr; self.w=[random.gauss(0,0.1) for _ in range(D)]; self.b=0.0
    def predict(self, x):
        return 1 if sum(wi*xi for wi,xi in zip(self.w,x))+self.b>0 else 0
    def fit(self, X, Y, epochs=20):
        rng=random.Random(2)
        for ep in range(epochs):
            idx=list(range(len(X))); rng.shuffle(idx)
            for i in idx:
                yhat=self.predict(X[i]); err=Y[i]-yhat
                for d in range(self.D): self.w[d]+=self.lr*err*X[i][d]
                self.b+=self.lr*err

clf=Linear(D=D, lr=0.05)
clf.fit(Xtr, ytr, epochs=20)
acc=sum(1 for x,y in zip(Xte,yte) if clf.predict(x)==y)/len(Xte) if Xte else 0
print(f"acc_sentido (embeddings reales)={acc:.3f}")

# baseline: embeddings aleatorios (misma arquitectura)
clf_rand=Linear(D=D, lr=0.05)
Xtr_rand=[[random.gauss(0,0.1) for _ in range(D)] for _ in Xtr]
Xte_rand=[[random.gauss(0,0.1) for _ in range(D)] for _ in Xte]
clf_rand.fit(Xtr_rand, ytr, epochs=20)
acc_rand=sum(1 for x,y in zip(Xte_rand,yte) if clf_rand.predict(x)==y)/len(Xte_rand) if Xte_rand else 0
print(f"acc_sentido (baseline aleatorio)={acc_rand:.3f}")

# ---------- D) Generación bigrama por cluster ----------
print("\n[D] Generación condicionada al sentido...")
cluster_tokens={k_:[] for k_ in range(K)}
cluster_texts={k_:[] for k_ in range(K)}
for pos,lbl in zip(positions, labels):
    cluster_tokens[lbl].append(seq[pos])
    cluster_texts[lbl].append(" ".join(seq[max(0,pos-W_CTX):pos]))

models={}
for lbl,tokens in cluster_tokens.items():
    if not tokens: continue
    t=defaultdict(Counter)
    for w,wn in zip(tokens, tokens[1:]): t[w][wn]+=1
    models[lbl]={w:{k:v/sum(c.values()) for k,v in c.items()} for w,c in t.items()}

pureza={}
sets={lbl:set([w for w,_ in Counter(tokens).most_common(25)]) for lbl,tokens in cluster_tokens.items()}
for a in range(K):
    for b in range(a+1,K):
        overlap=len(sets[a] & sets[b])
        diff=len(sets[a] ^ sets[b])
        pureza[(a,b)]={"overlap":overlap, "diff":diff, "parecidos":overlap<diff}
print("diferenciación clusters (top-25):", pureza)

generaciones={}
for lbl in range(K):
    if not cluster_texts[lbl]: continue
    seed=random.choice(cluster_texts[lbl]).split()[-3:]
    ctx=list(seed); out=[]
    for _ in range(12):
        probs=models[lbl].get(ctx[-1], {})
        preds=sorted(probs, key=probs.get, reverse=True)[:8]
        if not preds: break
        out.append(preds[0]); ctx.append(preds[0]); ctx=ctx[-10:]
    generaciones[lbl]={"seed":seed, "generado":out}

for lbl,g in generaciones.items():
    print(f" cluster {lbl}: {' '.join(g['seed'])} -> {' '.join(g['generado'])}")

# ---------- E) Loop generativo con memoria competitiva ----------
print("\n[E] Loop generativo con memoria competitiva...")
class SenseMemory:
    def __init__(self, n=2, alpha=0.8, beta=0.05):
        self.alpha=alpha; self.beta=beta
        keys=[chr(65+i) for i in range(n)]
        self.foco={k:0.5 for k in keys}
        self.hist=[]
    def update(self, pred_class):
        key=chr(65+int(pred_class))
        self.foco[key]+=self.beta
        total=sum(self.foco.values())
        for k in self.foco: self.foco[k]/=total
        self.hist.append(key)
    def current(self):
        return max(self.foco, key=self.foco.get)

mem=SenseMemory(n=K, alpha=0.8, beta=0.05)
ctx=sub[10:10+W_CTX]
history=[]
for step in range(20):
    vec=[0.0]*D; valid=0
    for w in ctx:
        if w in emb:
            for d in range(D): vec[d]+=emb[w][d]
            valid+=1
    if valid>0: vec=[x/valid for x in vec]
    pred_class=clf.predict(vec)
    mem.update(pred_class)
    active=mem.current()
    # generación por cluster del sentido activo
    lbl=int(active) if active.isdigit() else 0
    probs=models[lbl].get(ctx[-1], {})
    preds=sorted(probs, key=probs.get, reverse=True)[:5]
    nxt=preds[0] if preds else ""
    history.append(active)
    ctx.append(nxt); ctx=ctx[-10:]

counts_hist=Counter(history)
total=sum(counts_hist.values())
dominant=max(counts_hist, key=counts_hist.get)
coherence=counts_hist[dominant]/total if total>0 else 0
print(f"coherencia sentido activo={coherence:.3f} ({dominant}) distrib={dict(counts_hist)}")

# ---------- F) Guardar consolidación ----------
results={
    "word": WORD,
    "skipgram_top10": top10,
    "kmeans": {"K":K, "sizes":dict(counts), "cohesion":coh},
    "clasificador": {"acc_real":acc, "acc_aleatorio":acc_rand, "delta":acc-acc_rand},
    "pureza_clusters": {f"{a}_{b}":v for (a,b),v in pureza.items()},
    "generaciones": generaciones,
    "loop_memoria": {"coherence":coherence, "dominant":dominant, "distrib":dict(counts_hist)},
    "veredicto_general":""
}
# veredicto automático
veredicto_parts=[]
if acc > acc_rand + 0.1:
    veredicto_parts.append("clasificador con embeddings reales supera baseline")
if any(v["diff"]>v["overlap"] for v in pureza.values()):
    veredicto_parts.append("clusters tienen vocabulario diferenciado")
if coherence > 0.6:
    veredicto_parts.append("loop con memoria competitiva mantiene coherencia")
else:
    veredicto_parts.append("loop con memoria competitiva NO mantiene coherencia")
if veredicto_parts:
    results["veredicto_general"]="; ".join(veredicto_parts)
else:
    results["veredicto_general"]="sin señal clara en corpus real"

print("\n=== VEREDICTO GENERAL ===")
print(results["veredicto_general"])
json.dump(results, open("results_v25_evaluacion_general.json","w"), indent=2)
print("-> results_v25_evaluacion_general.json")
