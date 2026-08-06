#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.25 v7c — CAMBIO DE CONFIG ONLINE (build sencilla).
Comparacion directa baseline v7b vs config nueva sana: misma semilla k-means,
mismo corpus, distintas reglas de update. Medimos divergencia final.
"""
import json, math, random, re
from collections import defaultdict, Counter

random.seed(0)

# ---------- basics ----------
def norm(v): return math.sqrt(sum(x*x for x in v))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cos(a,b):
    na=norm(a); nb=norm(b)
    return 0.0 if na<1e-9 or nb<1e-9 else dot(a,b)/(na*nb)

# ---------- corpus (mism v7b) ----------
POLYSEMY = {
    "banco": {
        "A": ["dinero","pagar","cuenta","ahorro","plata","banquero","interes","cheque","tarjeta","retiro"],
        "B": ["rio","agua","pez","orilla","puente","corriente","boga","remo","proa","popa"],
        "templates_A": [
            "fue al banco para {A1} y {A2} con {A3} en mano",
            "el banco aprobo el {A2} sin {A3} ni {A4} de por medio",
            "si tienes {A1} en el banco podras usar el {A2} sin {A3}",
            "cerro su {A1} en el banco despues de {A2} el {A3}",
        ],
        "templates_B": [
            "se tiro al banco del {B1} para {B2} con su {B3}",
            "el {B3} choco contra el banco de la {B1} al {B2}",
            "amarraron la barca en el banco mientras el {B1} {B2}",
            "cerca del banco se {B2} una {B3} sobre la {B1}",
        ],
    },
}

def fill_template(tpl, sense, word):
    def rep(m):
        key=m.group(0).strip("{}")
        idx=int(key[1:])-1
        words=POLYSEMY[word][sense]
        return words[idx % len(words)]
    return re.sub(r'\{[AB]\d+\}', rep, tpl)

def build_corpus(n_per_sense=60):
    word="banco"
    seq=[]; meta=[]; word_ids=[]
    word_set={word:0}
    for sense_label in ["A","B"]:
        tpls=POLYSEMY[word][f"templates_{sense_label}"]
        for _ in range(n_per_sense):
            sentence=fill_template(random.choice(tpls), sense_label, word)
            if word not in sentence.split():
                sentence = sentence + " y " + word
            toks=sentence.split()
            for t in toks:
                seq.append(t); meta.append(sense_label if t==word else "O"); word_ids.append(word_set.get(t,-1))
    return seq, list(dict.fromkeys(seq)), word_set, meta, word_ids

# ---------- kmeans offline ----------
def extract_contexts(tokens, meta, word, W=10):
    contexts=[]; labels=[]
    for i,t in enumerate(tokens):
        if t==word:
            start=max(0,i-W); end=min(len(tokens),i+W+1)
            ctx=tokens[start:i]+tokens[i+1:end]
            contexts.append(ctx); labels.append(meta[i])
    return contexts, labels

def build_bow(contexts):
    vocab=sorted(set(w for ctx in contexts for w in ctx))
    idx={w:i for i,w in enumerate(vocab)}
    mat=[]
    for ctx in contexts:
        c=Counter(ctx)
        total=len(ctx) if len(ctx)>0 else 1
        mat.append({idx[w]:c[w]/total for w in c if w in idx})
    return mat, vocab, idx

def kmeans(mat, k, seed=0, max_iter=80, tol=1e-4):
    rng=random.Random(seed)
    n=len(mat)
    if n<k: raise ValueError("menos puntos que clusters")
    centroids=[dict(mat[i]) for i in rng.sample(range(n), k)]
    labels=[0]*n
    for it in range(max_iter):
        new_labels=[]
        for v in mat:
            best_j=0; best_cos=-1.0
            for j,ce in enumerate(centroids):
                c=cos_sparse(v,ce)
                if c>best_cos: best_cos=c; best_j=j
            new_labels.append(best_j)
        new_cent=[defaultdict(float) for _ in range(k)]
        cnts=[0]*k
        for lab,v in zip(new_labels,mat):
            cnts[lab]+=1
            for pos,val in v.items():
                new_cent[lab][pos]+=val
        for j in range(k):
            if cnts[j]>0:
                for pos in new_cent[j]:
                    new_cent[j][pos]/=cnts[j]
        shift=0.0
        for j in range(k):
            shift=max(shift, norm_sparse({p:abs(new_cent[j][p]-centroids[j].get(p,0.0)) for p in new_cent[j] if centroids[j].get(p,0.0)!=new_cent[j][p]}))
        centroids=[dict(c) for c in new_cent]; labels=new_labels
        if shift<tol: break
    inertia=sum(1.0-cos_sparse(v,centroids[lab]) for v,lab in zip(mat,labels))
    return labels, centroids, inertia

def cos_sparse(a,b):
    na=norm_sparse(a); nb=norm_sparse(b)
    return 0.0 if na<1e-9 or nb<1e-9 else dot_sparse(a,b)/(na*nb)
def dot_sparse(a,b): return sum(a[k]*b[k] for k in a if k in b)
def norm_sparse(v): return math.sqrt(sum(x*x for x in v.values())) if v else 0.0

# ---------- grafo online ----------
class PolysemyGraph:
    def __init__(self, D, beta_anchor, beta_repulse, theta, repulsion_mode="cond"):
        self.D=D; self.beta_anchor=beta_anchor; self.beta_repulse=beta_repulse; self.theta=theta; self.repulsion_mode=repulsion_mode
        self.emb={}; self.sub={}
    def seed_word(self, word, seed_vecs):
        self.sub[word]=[list(seed_vecs[0]), list(seed_vecs[1])]
        self.emb[word]=[0.0]*self.D
    def update(self, word, context_words):
        A=self.sub[word][0]; B=self.sub[word][1]
        ctx=[0.0]*self.D; valid=0
        for w in context_words:
            if w in self.emb:
                for d in range(self.D): ctx[d]+=self.emb[w][d]
                valid+=1
        if valid>0: ctx=[x/valid for x in ctx]
        ca=cos(ctx,A); cb=cos(ctx,B)
        if ca>=cb:
            for d in range(self.D): A[d]+=self.beta_anchor*(ctx[d]-A[d])
            if self.repulsion_mode=="cond":
                if ca<self.beta_repulse or ca<self.theta:
                    for d in range(self.D): B[d]-=self.beta_repulse*A[d]
            else:
                for d in range(self.D): B[d]-=self.beta_repulse*A[d]
        else:
            for d in range(self.D): B[d]+=self.beta_anchor*(ctx[d]-B[d])
            if self.repulsion_mode=="cond":
                if cb<self.beta_repulse or cb<self.theta:
                    for d in range(self.D): A[d]-=self.beta_repulse*B[d]
            else:
                for d in range(self.D): A[d]-=self.beta_repulse*B[d]
        for d in range(self.D):
            A[d]=max(-1.0,min(1.0,A[d])); B[d]=max(-1.0,min(1.0,B[d]))
        self.sub[word]=[A,B]

def run_online(tokens, meta, word, seed_vecs, D, epochs, W, beta_anchor, beta_repulse, theta, repulsion_mode):
    g=PolysemyGraph(D=D, beta_anchor=beta_anchor, beta_repulse=beta_repulse, theta=theta, repulsion_mode=repulsion_mode)
    g.seed_word(word, seed_vecs)
    vocab=sorted(set(tokens))
    for w in vocab:
        if w not in g.emb: g.emb[w]=[random.gauss(0,0.1) for _ in range(D)]
    dists=[]
    for ep in range(epochs):
        for i in range(W, len(tokens)):
            w=tokens[i]
            if w not in g.sub or g.sub[w] is None: continue
            ctx=tokens[max(0,i-W):i]
            g.update(w, ctx)
        A,B=g.sub[word]; dists.append(cos(A,B))
    return dists

# ---------- main ----------
def main():
    print("=== v0.25 v7c CAMBIO DE CONFIG ONLINE ===")
    seq,vocab,word_set,meta,word_ids=build_corpus(n_per_sense=60)
    word="banco"
    contexts,gt=extract_contexts(seq,meta,word,W=12)
    mat,bow_vocab,bow_idx=build_bow(contexts)
    labs,centers,iner=kmeans(mat,k=2,seed=0)
    def project(c,D):
        v=[0.0]*D
        for pos,val in c.items():
            d=pos % D
            v[d]+=val
        n=norm(v)
        if n>1e-9: v=[x/n for x in v]
        return v

    configs=[
        dict(name="baseline_v7b", D=16, epochs=30, W=8, beta_anchor=0.2, beta_repulse=0.05, theta=0.8, repulsion_mode="cond"),
        dict(name="repulsion_fuerte", D=16, epochs=40, W=8, beta_anchor=0.2, beta_repulse=0.4, theta=0.0, repulsion_mode="uncond"),
        dict(name="anchor_mas_fuerte", D=16, epochs=30, W=8, beta_anchor=0.5, beta_repulse=0.1, theta=0.6, repulsion_mode="cond"),
    ]
    results={}
    for cfg in configs:
        name=cfg.pop("name")
        # semilla en D correcto
        seed0=project(centers[0], cfg["D"])
        seed1=project(centers[1], cfg["D"])
        dists=run_online(seq,meta,word,[seed0,seed1], **cfg)
        init=dists[0]; final=dists[-1]; divergence=final-init
        if divergence < -0.05:
            verdict="SEPARA ONLINE"
        elif divergence > 0.05:
            verdict="COLAPSA ONLINE"
        else:
            verdict="ESTABLE ONLINE"
        print(f"{name}: init={init:.3f} final={final:.3f} div={divergence:.3f} -> {verdict}")
        results[name]=dict(cfg=cfg, dists=dists, init=init, final=final, divergence=divergence, veredicto=verdict)
    best=max((r for r in results.values() if r["divergence"]<0), key=lambda r: r["divergence"], default=None)
    mejor=best["veredicto"] if best else "NINGUNA SEPARA"
    print("\nMEJOR CONFIG:", mejor)
    # ---------- evaluacion real acc_gt ----------
    eval_word="banco"
    eval_cfg_name="repulsion_fuerte"
    eval_cfg=results[eval_cfg_name]["cfg"]
    best_dists=results[eval_cfg_name]["dists"]
    # reentrenar con esa config hasta convergencia
    seed0=project(centers[0], eval_cfg["D"])
    seed1=project(centers[1], eval_cfg["D"])
    g=PolysemyGraph(D=eval_cfg["D"], beta_anchor=eval_cfg["beta_anchor"], beta_repulse=eval_cfg["beta_repulse"], theta=eval_cfg["theta"], repulsion_mode=eval_cfg["repulsion_mode"])
    g.seed_word(eval_word,[seed0,seed1])
    vocab=sorted(set(seq))
    for w in vocab:
        if w not in g.emb: g.emb[w]=[random.gauss(0,0.1) for _ in range(eval_cfg["D"])]
    for ep in range(eval_cfg["epochs"]):
        for i in range(eval_cfg["W"], len(seq)):
            w=seq[i]
            if w not in g.sub or g.sub[w] is None: continue
            ctx=seq[max(0,i-eval_cfg["W"]):i]
            g.update(w, ctx)
    # medir acc_gt en cada ocurrencia
    correct=0; total=0
    for i,t in enumerate(seq):
        if t==eval_word:
            total+=1
            ctx=seq[max(0,i-eval_cfg["W"]):i]
            ctx_vec=[0.0]*eval_cfg["D"]; valid=0
            for w in ctx:
                if w in g.emb:
                    for d in range(eval_cfg["D"]): ctx_vec[d]+=g.emb[w][d]
                    valid+=1
            if valid>0: ctx_vec=[x/valid for x in ctx_vec]
            ca=cos(ctx_vec,g.sub[eval_word][0]); cb=cos(ctx_vec,g.sub[eval_word][1])
            pred="A" if ca>=cb else "B"
            if pred==meta[i]: correct+=1
    acc_gt=correct/total if total>0 else 0.0
    print(f"acc_gt real ('{eval_word}', config={eval_cfg_name}): {acc_gt:.3f} ({correct}/{total})")
    out=dict(experiment="v0.25_v7c_cambio_config_online", word=eval_word,
             offline=dict(k2_inertia=iner, silhouette=0.0, mejora_inertia=(37.290-iner)/37.290),
             best=mejor, results=results, evaluation=dict(config=eval_cfg_name, acc_gt=acc_gt, correct=correct, total=total))
    json.dump(out,open("results_v25_v7c.json","w"),indent=2)
    print("-> results_v25_v7c.json")
if __name__=="__main__":
    main()
