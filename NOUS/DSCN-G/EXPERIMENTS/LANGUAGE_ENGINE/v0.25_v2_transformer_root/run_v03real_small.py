#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSCN-G v0.3 REAL — HIBERNADO (memoria de masa, no borrar omega).
Toma motor de v0.2 (afinidad Ec.2 + poda Ec.5) y cambia poda por HIBERNAR:
V<theta_death => alive=False (no entra a cadenas) PERO omega/phi se preservan.
Mide: N_active (working set) + N_hibernated = N_total. ¿N_total ~ N_init?
Esto valida la idea de Luciano (DB semantica: no borrar, guardar en masa).
"""
import json, math, random, sys, time
ALPHA=5.0; BETA=0.20; GAMMA=0.05; K=10; THETA_DEATH=0.02; STEPS=1200
N_INIT=200

class Node:
    __slots__=['w','phi','V','alive','hibernated']
    def __init__(s,w,phi):
        s.w=w; s.phi=phi; s.V=1.0; s.alive=True; s.hibernated=False

class Engine:
    def __init__(s,N,seed=0,theta_death=THETA_DEATH):
        r=random.Random(seed)
        s.N=N; s.theta_death=theta_death
        s.nodes=[Node([r.gauss(0,1) for _ in range(8)], r.uniform(0,2*math.pi)) for _ in range(N)]
        s.ideal=[n.w[:] for n in s.nodes]
        s.active=s.nodes[:]
        s.hibernated=[]
    def step(s):
        act=s.active; na=len(act)
        # afinidad Ec.2
        for n in act:
            rho=sum(math.exp(-ALPHA*math.sqrt(sum((a-b)**2 for a,b in zip(n.w,m.w))))
                    for m in act if m is not n)
            n.V+=-GAMMA*n.V+BETA*(1-rho/max(1,na-1))
            n.V=max(0.0,min(1.0,n.V))
        # poda => HIBERNAR (no borrar)
        for n in act[:]:
            if n.V < s.theta_death:
                n.alive=False; n.hibernated=True
                act.remove(n); s.hibernated.append(n)
        # aprendizaje omega hacia ideal (solo vivos)
        for n in act:
            idx=s.nodes.index(n)
            for k in range(8):
                n.w[k]+=BETA*(s.ideal[idx][k]-n.w[k])
    def counts(s):
        return len(s.active), len(s.hibernated), s.N

def main():
    print("=== v0.3 REAL — HIBERNADO (memoria de masa) N_init=%d ===" % N_INIT)
    t0=time.time()
    e=Engine(N_INIT, seed=0)
    for _ in range(STEPS): e.step()
    na,nh,tot=e.counts()
    print(f"corrido en {time.time()-t0:.0f}s")
    print(f"N_active (working set): {na}")
    print(f"N_hibernated (masa):    {nh}")
    print(f"N_total (masa viva):    {na+nh}  (N_init={tot})")
    print(f"colapso v0.1 (sin hibernar) daba ~4.5. Aca masa={na+nh}")
    out=dict(experiment="v0.3_real_hibernado",
             hypothesis="Hibernar (no borrar omega) mantiene la masa total ~N_init; el grafo no colapsa.",
             params=dict(alpha=ALPHA,beta=BETA,gamma=GAMMA,K=K,theta_death=THETA_DEATH,steps=STEPS,N_init=N_INIT),
             N_active=na, N_hibernated=nh, N_total=na+nh, N_init=tot,
             retencion_masa=round((na+nh)/tot,4),
             comparar_v01_sin_hibernar=4.5)
    with open("results_v03real.json","w") as f: json.dump(out,f,indent=2)
    print("\n-> results_v03real.json")

if __name__=="__main__": main()
