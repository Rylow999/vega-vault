#!/usr/bin/env python3
"""
verify_c3_redesign.py — Ronda 4: rediseño de C3 (phase hijacking).

Diagnóstico de por qué C3 no se sostenía (claims_falsifiable.md, hipótesis
no verificada por separado hasta ahora): con θ_death=0.10 default, T1
converge a N*≈4-5 nodos activos. `plv_intra_group()` mide el orden de
Kuramoto R sobre `nodes_active[1:]` — el grupo de seguidores, SIN la raíz
(ver verify_dscng_v3.py línea 168-174: `others = self.nodes_active[1:]`,
excluye explícitamente `nodes_active[0]` que es la raíz). Con N*≈4-5 eso
dejaba 3-4 nodos en el grupo — muy poca población para que 15 pasos de
pull (η=0.15) produzcan una sincronización medible y estable frente al
ruido del acoplamiento Kuramoto basal.

Rediseño (opción elegida: más nodos activos, vía θ_death más bajo —
la misma perilla que usa verify_phi_proxy.py, y por la misma razón: es la
única que realmente mueve N* sin tocar N_init inútilmente, ver T1). Se
barre θ_death y, cruzado con eso, `hijack_steps` y `eta_hijack`, para ver
si con más población el mecanismo empieza a producir el efecto que la
claim describe, y no solo confirmar que "más nodos" alcanza por sí solo.
"""
import sys, os, json, itertools
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3, DEFAULTS  # noqa: E402


def verify_c3_config(theta_death, hijack_steps, eta_hijack, seeds=10, steps=2000,
                      N_init_headroom=1.5, alpha=5.0) -> dict:
    N_init = max(50, int(N_init_headroom * (1.0 / theta_death)))
    all_deltas = []
    hijack_events = 0
    n_active_at_trigger = []

    for s in range(seeds):
        sim = DSCN_G_v3(seed=s, N=N_init, alpha=alpha, theta_death=theta_death,
                         hijack_steps=hijack_steps, eta_hijack=eta_hijack)
        for _ in range(steps):
            sim.step()

        evts = sim.c3_root_plv_deltas
        hijack_events += len(evts)
        for t_start, plv_before, plv_after, delta in evts:
            all_deltas.append(delta)
        # population size at end, as a proxy for "how big was the follower
        # group during these hijack events" (population is ~stable by the
        # time hijacks start triggering, post burn-in)
        if sim.nodes_active:
            n_active_at_trigger.append(len(sim.nodes_active) - 1)  # minus root

    rise_events = sum(1 for d in all_deltas if d < -0.3)
    rise_rate = rise_events / max(1, len(all_deltas))
    mean_delta = float(np.mean(all_deltas)) if all_deltas else None
    std_delta = float(np.std(all_deltas)) if all_deltas else None

    return dict(theta_death=theta_death, hijack_steps=hijack_steps, eta_hijack=eta_hijack,
                N_init=N_init, seeds=seeds, steps=steps,
                follower_group_size_mean=float(np.mean(n_active_at_trigger)) if n_active_at_trigger else None,
                hijack_triggers=hijack_events,
                rise_rate=float(rise_rate),
                mean_delta_plv=mean_delta, std_delta_plv=std_delta,
                n_deltas=len(all_deltas))


def sweep(seeds=10, steps=2000):
    print("\n" + "=" * 78)
    print("C3 REDISEÑADO (Ronda 4) — barrido θ_death × hijack_steps × η_hijack")
    print("=" * 78)

    theta_deaths = [0.10, 0.05, 0.02]        # baseline, then more active nodes
    hijack_steps_opts = [15, 40]             # baseline, then longer hijack window
    eta_hijack_opts = [0.15, 0.30]           # baseline, then stronger pull

    rows = []
    for td, hs, eh in itertools.product(theta_deaths, hijack_steps_opts, eta_hijack_opts):
        r = verify_c3_config(td, hs, eh, seeds=seeds, steps=steps)
        rows.append(r)
        grp = r["follower_group_size_mean"]
        grp_s = f"{grp:.1f}" if grp is not None else "n/a"
        dplv_s = f"{r['mean_delta_plv']:+.3f}±{(r['std_delta_plv'] or 0):.3f}" if r["mean_delta_plv"] is not None else "n/a (0 triggers)"
        print(f"  θ_death={td:.2f} hijack_steps={hs:3d} η_hijack={eh:.2f}  "
              f"grupo_seguidores≈{grp_s}  triggers={r['hijack_triggers']:4d}  "
              f"ΔPLV={dplv_s}  "
              f"rise_rate={r['rise_rate']*100:5.1f}%")
    return rows


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    seeds = 5 if args.quick else args.seeds
    steps = 500 if args.quick else args.steps

    rows = sweep(seeds=seeds, steps=steps)
    with open("c3_redesign_results.json", "w") as f:
        json.dump(rows, f, indent=2)
    print("\n→ c3_redesign_results.json")

    best = max([r for r in rows if r["mean_delta_plv"] is not None],
               key=lambda r: -r["mean_delta_plv"], default=None)
    if best:
        print(f"\nMejor config (ΔPLV más negativo = más hijacking real): "
              f"θ_death={best['theta_death']} hijack_steps={best['hijack_steps']} "
              f"η_hijack={best['eta_hijack']}  ΔPLV={best['mean_delta_plv']:+.3f}  "
              f"rise_rate={best['rise_rate']*100:.1f}%")
