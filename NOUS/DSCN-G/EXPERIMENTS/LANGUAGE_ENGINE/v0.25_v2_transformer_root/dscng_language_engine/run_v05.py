#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSCN-G v0.5 — L2 RUSTICO (decoder omega->texto).
Nivel 1: retrieval -> palabra (dado omega, elige la palabra de centroide mas cercano).
Nivel 2: generacion rustica -> encadena palabras por afinidad del grafo (Ec.2),
         el decoder proyecta cada omega siguiente a texto. Esto es la "microllm cavernicola".
Corpus chico y Python puro (sin numpy): cada palabra = un omega centroide fijo.
"""
import json, math, random, sys, time
ALPHA=5.0; D=8

# Corpus mini: frases simples. Cada palabra tiene un omega (vector fijo pseudo-semantico).
CORPUS = ["el","gato","come","pez","la","casa","es","roja","el perro","corre"]

def omega_of(word, rng):
    # hash determinista de la palabra -> omega estable
    r=random.Random(hash(word)%100000)
    return [r.gauss(0,1) for _ in range(D)]

def norm(v): return math.sqrt(sum(x*x for x in v))
def affinity(q,w):
    d=math.sqrt(sum((a-b)**2 for a,b in zip(q,w)))
    return math.exp(-ALPHA*d)

def build_vocab():
    rng=random.Random(1)
    return {w:omega_of(w,rng) for w in CORPUS}

def decode(vocab, q):
    # Nivel 1: palabra de centroide mas cercano
    best,bests=-1,None
    for w,o in vocab.items():
        s=affinity(q,o)
        if s>best: best=s; bestw=w
    return bestw, best

def generate(vocab, seed_word, steps=6):
    # Nivel 2: parte de omega de seed, elige siguiente por afinidad maxima
    # (el grafo "salta" al nodo mas afin al actual), decodifica a palabra.
    rng=random.Random(2)
    cur=vocab[seed_word][:]
    out=[seed_word]
    for _ in range(steps):
        # siguiente = palabra con mayor afinidad al omega actual (excluye la misma)
        bestw,bests=None,-1
        for w,o in vocab.items():
            if w==out[-1]: continue
            s=affinity(cur,o)
            if s>bests: bests=s; bestw=w
        out.append(bestw)
        # el omega "avanza" mezclandose con el de la palabra elegida (aprendizaje L2 trivial)
        cur=[0.7*cur[k]+0.3*vocab[bestw][k] for k in range(D)]
    return out

def main():
    print("=== v0.5 L2 RUSTICO (microllm cavernicola) ===")
    vocab=build_vocab()
    # Nivel 1: dado el omega de "gato", ¿decodifica "gato"?
    w1,s1=decode(vocab, vocab["gato"])
    print(f"Nivel1 retrieve 'gato' -> '{w1}' (score {s1:.3f})  {'OK' if w1=='gato' else 'FALLÓ'}")
    # Nivel 2: genera una frase desde "el"
    frase=generate(vocab,"el",steps=6)
    print(f"Nivel2 genera desde 'el': {' '.join(frase)}")
    out=dict(experiment="v0.5_L2_rustico",
             hypothesis="El decoder omega->texto (retrieval + encadenamiento por afinidad) produce secuencias.",
             params=dict(alpha=ALPHA,d=D,corpus_size=len(CORPUS)),
             note="L2 mas rustico: nearest-centroid + salto por afinidad (microllm cavernicola).",
             nivel1=dict(query="gato",decoded=w1,ok=(w1=="gato")),
             nivel2=dict(seed="el",frase=" ".join(frase)))
    with open("results_v05.json","w") as f: json.dump(out,f,indent=2)
    print("\n-> results_v05.json")

if __name__=="__main__": main()
