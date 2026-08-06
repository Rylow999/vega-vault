#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSCN-G Language Engine v0.1 — Concept Proof (runner eficiente).
Barrido N_init con presupuesto adaptado: pocas semillas en escalas masivas
porque la saturación de N* es robusta y lo que importa es la TENDENCIA."""
import json, math, random, sys, time

ALPHA=5.0; BETA=0.20; GAMMA=0.01; THETA_DEATH=0.10; D=8; N_CHAINS=3

def make_omega(rng,d,scale=0.1):
    return [rng.gauss(0.0,scale) for _ in range(d)]
def norm(v): return math.sqrt(sum(x*x for x in v))
def dot(a,b): return sum(x*y for x,y in zip(a,b))

class Node:
    __slots__=("omega","vitality","alive")
    def __init__(self,omega):
        self.omega=omega; self.vitality=1.0; self.alive=True

class Engine:
    def __init__(self,N_init,seed):
        self.rng=random.Random(seed)
        self.omega_ideal=[1.0/math.sqrt(D) for _ in range(D)]
        self.nodes=[Node(make_omega(self.rng,D)) for _ in range(N_init)]
        idx=list(range(N_init)); self.rng.shuffle(idx)
        self.chains=idx[:N_CHAINS]; self.t=0
    def _active(self): return [i for i,n in enumerate(self.nodes) if n.alive]
    def _chain_step(self,src):
        act=self._active()
        if not act: return src
        src_n=self.nodes[src]
        diffs=[math.sqrt(sum((a-b)**2 for a,b in zip(self.nodes[m].omega,src_n.omega))) for m in act]
        mx=max(diffs); ws=[math.exp(-ALPHA*(diffs[i]-mx)) for i in range(len(act))]
        s=sum(ws); r=self.rng.random()*s; acc=0.0
        for i,w in enumerate(act):
            acc+=ws[i]
            if acc>=r: return w
        return act[-1]
    def _interf(self,i): return norm(self.nodes[i].omega)
    def step(self):
        self.t+=1; act=self._active()
        if not act: return
        activity={i:0.0 for i in act}
        for k in range(N_CHAINS):
            old=self.chains[k]
            if not self.nodes[old].alive: old=self.rng.choice(act); self.chains[k]=old
            new=self._chain_step(old); self.chains[k]=new; activity[new]=activity.get(new,0.0)+1.0
        root=act[0]; activity[root]=activity.get(root,0.0)+1.0
        denom=N_CHAINS+1
        for i in activity: activity[i]/=denom
        decay=math.exp(-GAMMA)
        for i in act:
            a=activity.get(i,0.0); n=self.nodes[i]
            n.vitality=n.vitality*decay+a*(1.0-decay)
            if n.vitality<THETA_DEATH: n.alive=False
        act=self._active()
        if not act: return
        sel=max(act,key=lambda i:self._interf(i))
        w=self.nodes[sel].omega; nrm=norm(w)+1e-8; reward=(dot(w,self.omega_ideal)/nrm+1.0)/2.0
        for i in act:
            I=self._interf(i)
            if I>0:
                beta_eff=min(BETA,BETA*(I/(norm(self.nodes[i].omega)+1e-8)))
                o=self.nodes[i].omega
                self.nodes[i].omega=[(1-beta_eff)*o[k]+beta_eff*reward*self.omega_ideal[k] for k in range(D)]
    def herfindahl(self):
        act=self._active()
        if not act: return 0.0
        counts={}
        for c in self.chains:
            if self.nodes[c].alive: counts[c]=counts.get(c,0.0)+1.0
        s=sum(counts.values())
        return sum((v/s)**2 for v in counts.values()) if s>0 else 0.0

def run_N(N_init,seeds,steps):
    Ns=[];rhos=[]
    for s in range(seeds):
        eng=Engine(N_init,seed=s)
        for _ in range(steps): eng.step()
        Ns.append(sum(1 for n in eng.nodes if n.alive)); rhos.append(eng.herfindahl())
    return Ns,rhos

def main():
    # (N_init, seeds, steps) — presupuesto adaptado
    plan=[(4,20,2000),(10,20,2000),(50,20,2000),(200,20,2000),
          (1000,10,1500),(5000,5,1000),(10000,3,800)]
    ub=1.0/THETA_DEATH; rows=[]
    print(f"{'N_init':>8} | {'N* mean':>9} | {'N* std':>7} | {'rho':>6} | fp? | bound?")
    for Ni,se,st in plan:
        t0=time.time(); Ns,rhos=run_N(Ni,se,st)
        Nm=sum(Ns)/len(Ns); Nsd=math.sqrt(sum((x-Nm)**2 for x in Ns)/len(Ns)); rm=sum(rhos)/len(rhos)
        fp=rm>=Nm*THETA_DEATH**2; ubok=Nm<=ub
        rows.append(dict(N_init=Ni,seeds=se,steps=st,N_star_mean=round(Nm,3),N_star_std=round(Nsd,3),
                         rho_mean=round(rm,4),fixed_point_ok=fp,universal_bound_ok=ubok,bound=ub))
        print(f"{Ni:>8} | {Nm:>9.2f} | {Nsd:>7.2f} | {rm:>6.3f} | {'✓' if fp else '✗'}   | {'✓' if ubok else '✗'}   ({time.time()-t0:.0f}s)")
        sys.stdout.flush()
    out=dict(experiment="v0.1_concept_proof",
             hypothesis="N* escala sublinealmente con N_init (memoria escasa)",
             params=dict(alpha=ALPHA,beta=BETA,gamma=GAMMA,theta_death=THETA_DEATH,d=D,chains=N_CHAINS),
             universal_bound=ub,
             note="Replica Eq.2 (afinidad cadena)+Eq.5 (poda). Kuramoto omitido (no afecta punto fijo).",
             results=rows)
    with open("results_v01.json","w") as f: json.dump(out,f,indent=2)
    print("\n-> results_v01.json")

if __name__=="__main__": main()
