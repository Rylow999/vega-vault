#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DSCN-G Language Engine v0.1 — Concept Proof
============================================
Hipótesis (de la propuesta "reemplazar Transformer por DSCN-G"):
  "El sistema converge a pocos nodos activos mediante homeostasis
   -> arquitectura de memoria escasa escalable O(nodos_activos)."

Este experimento mide si eso es cierto. Pregunta científica:
  ¿N* (número de nodos activos en estado estacionario) crece con N_init,
   o satura en un pequeño punto fijo independiente de N_init?

Dinámica implementada (fiel al motor real, sin numpy):
  - Ec.2  Afinidad de cadena: P(m|n) ∝ exp(-α·‖ω_m − ω_n‖)
  - Ec.5  Vitalidad: V ← V·e^{-γ} + A·(1−e^{-γ}); poda si V < θ_death
  - Ec.1  ω aprende hacia ω_ideal (broadcast, gating por interferencia)
  NOTA: acoplamiento Kuramoto (O(n^2), requiere numpy) se omite; no afecta
        el punto fijo de poda (solo recalcula φ, no V ni la visita de cadenas).

Salida: JSON con curva N* vs N_init + verificación de la cota universal
        N* ≤ 1/θ_death y de la condición de punto fijo ρ ≥ N*·θ_death^2.
"""
import json, math, random, sys, time

# ── defaults (del motor real, verify_dscng_v3.py) ──
ALPHA = 5.0
BETA = 0.20
GAMMA = 0.01
THETA_DEATH = 0.10
D = 8                      # dim embedding
N_CHAINS = 3
STEPS = 2000
SEEDS = 20

def make_omega(rng, d, scale=0.1):
    return [rng.gauss(0.0, scale) for _ in range(d)]

def norm(v):
    return math.sqrt(sum(x*x for x in v))

def dot(a, b):
    return sum(x*y for x,y in zip(a,b))

class Node:
    __slots__ = ("omega", "vitality", "alive")
    def __init__(self, omega):
        self.omega = omega
        self.vitality = 1.0
        self.alive = True

class Engine:
    def __init__(self, N_init, seed):
        self.rng = random.Random(seed)
        self.omega_ideal = [1.0/math.sqrt(D) for _ in range(D)]
        self.nodes = [Node(make_omega(self.rng, D)) for _ in range(N_init)]
        # cadenas: posiciones iniciales únicas
        idx = list(range(N_init))
        self.rng.shuffle(idx)
        self.chains = idx[:N_CHAINS]
        self.t = 0

    def _active(self):
        return [i for i,n in enumerate(self.nodes) if n.alive]

    def _chain_step(self, src):
        act = self._active()
        if not act:
            return src
        src_n = self.nodes[src]
        diffs = []
        for m in act:
            wm = self.nodes[m].omega
            d = math.sqrt(sum((a-b)**2 for a,b in zip(wm, src_n.omega)))
            diffs.append(d)
        mx = max(diffs)
        # estabilizar para evitar underflow
        ws = [math.exp(-ALPHA*(diffs[i]-mx)) for i in range(len(act))]
        s = sum(ws)
        r = self.rng.random()*s
        acc = 0.0
        for i,w in enumerate(act):
            acc += ws[i]
            if acc >= r:
                return w
        return act[-1]

    def _interf(self, i):
        # I_i = ‖ω_i‖·cos(φ_i − φ_root) — sin Kuramoto, φ=0 ⇒ cos=1
        return norm(self.nodes[i].omega)

    def step(self):
        self.t += 1
        act = self._active()
        if not act:
            return
        activity = {i:0.0 for i in act}
        for k in range(N_CHAINS):
            old = self.chains[k]
            if not self.nodes[old].alive:
                old = self.rng.choice(act)
                self.chains[k] = old
            new = self._chain_step(old)
            self.chains[k] = new
            activity[new] = activity.get(new, 0.0) + 1.0
        root = act[0]
        activity[root] = activity.get(root, 0.0) + 1.0
        denom = N_CHAINS + 1
        for i in activity:
            activity[i] /= denom
        # vitalidad + poda (Ec.5)
        decay = math.exp(-GAMMA)
        for i in act:
            a = activity.get(i, 0.0)
            n = self.nodes[i]
            n.vitality = n.vitality*decay + a*(1.0-decay)
            if n.vitality < THETA_DEATH:
                n.alive = False
        act = self._active()
        if not act:
            return
        # ω update (Ec.1) — nodo de mayor interferencia
        sel = max(act, key=lambda i: self._interf(i))
        w = self.nodes[sel].omega
        nrm = norm(w) + 1e-8
        align = dot(w, self.omega_ideal)/nrm
        reward = (align+1.0)/2.0
        for i in act:
            I = self._interf(i)
            if I > 0:
                beta_eff = min(BETA, BETA*(I/(norm(self.nodes[i].omega)+1e-8)))
                o = self.nodes[i].omega
                self.nodes[i].omega = [(1-beta_eff)*o[k] + beta_eff*reward*self.omega_ideal[k]
                                       for k in range(D)]

    def herfindahl(self):
        act = self._active()
        if not act:
            return 0.0
        counts = {}
        for c in self.chains:
            if self.nodes[c].alive:
                counts[c] = counts.get(c,0.0)+1.0
        s = sum(counts.values())
        if s <= 0:
            return 0.0
        return sum((v/s)**2 for v in counts.values())

def run_N(N_init, seeds=SEEDS, steps=STEPS):
    Ns, rhos = [], []
    for s in range(seeds):
        eng = Engine(N_init, seed=s)
        for _ in range(steps):
            eng.step()
        Ns.append(sum(1 for n in eng.nodes if n.alive))
        rhos.append(eng.herfindahl())
    return Ns, rhos

def main():
    N_inits = [4, 10, 50, 200, 1000, 5000, 10000]
    ub = 1.0/THETA_DEATH
    rows = []
    print(f"{'N_init':>8} | {'N* mean':>9} | {'N* std':>7} | {'rho':>6} | {'N*·θ²':>8} | fp? | bound?")
    for Ni in N_inits:
        t0 = time.time()
        Ns, rhos = run_N(Ni)
        Nm = sum(Ns)/len(Ns); Ns_ = math.sqrt(sum((x-Nm)**2 for x in Ns)/len(Ns))
        rm = sum(rhos)/len(rhos)
        fp_ok = rm >= Nm*THETA_DEATH**2
        ub_ok = Nm <= ub
        rows.append(dict(N_init=Ni, N_star_mean=round(Nm,3), N_star_std=round(Ns_,3),
                         rho_mean=round(rm,4), fixed_point_ok=fp_ok,
                         universal_bound_ok=ub_ok, bound=ub))
        print(f"{Ni:>8} | {Nm:>9.2f} | {Ns_:>7.2f} | {rm:>6.3f} | {Nm*THETA_DEATH**2:>8.3f} | {'✓' if fp_ok else '✗'}   | {'✓' if ub_ok else '✗'}")
        sys.stdout.flush()
    out = dict(experiment="v0.1_concept_proof",
               hypothesis="N* escala sublinealmente con N_init (memoria escasa)",
               params=dict(alpha=ALPHA, beta=BETA, gamma=GAMMA, theta_death=THETA_DEATH,
                           d=D, chains=N_CHAINS, steps=STEPS, seeds=SEEDS),
               universal_bound=ub,
               note="Replica Eq.2 (afinidad cadena) + Eq.5 (poda). Kuramoto omitido (no afecta punto fijo).",
               results=rows)
    with open("results_v01.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n-> results_v01.json")

if __name__ == "__main__":
    main()
