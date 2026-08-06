#!/usr/bin/env python3
"""
verify_hub_boost_fix.py — Ronda 5: ¿el hub_boost reubicado (en
_apply_hijack_pull, no en la matriz de Kuramoto) mueve el rise_rate de
C3 esta vez? El primer intento (Kuramoto) dio 0.7%→0.7% (sin efecto,
ver AUDIT_NOTES_ROUND4.md tabla "Thalamic"). Este script repite esa
misma comparación con el fix aplicado.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3  # noqa: E402
from thalamic_model import ThalamicDSCN_G_v3  # noqa: E402


def c3_stats(model_cls, theta_death, hijack_steps, eta_hijack, seeds=15,
             steps=2000, N_init_headroom=1.5, alpha=5.0, hub_boost=None):
    N_init = max(50, int(N_init_headroom * (1.0 / theta_death)))
    all_deltas = []
    for s in range(seeds):
        kw = dict(seed=s, N=N_init, alpha=alpha, theta_death=theta_death,
                   hijack_steps=hijack_steps, eta_hijack=eta_hijack)
        if hub_boost is not None:
            kw["hub_boost"] = hub_boost
        sim = model_cls(**kw)
        for _ in range(steps):
            sim.step()
        for _t, _b, _a, delta in sim.c3_root_plv_deltas:
            all_deltas.append(delta)
    rise = sum(1 for d in all_deltas if d < -0.3)
    rate = rise / max(1, len(all_deltas))
    mean_d = float(np.mean(all_deltas)) if all_deltas else None
    return dict(n_events=len(all_deltas), rise_rate=rate, mean_delta_plv=mean_d)


if __name__ == "__main__":
    seeds, steps = 15, 2000
    configs = [
        ("DSCN_G_v3 (sin boost)",            DSCN_G_v3,        None),
        ("Thalamic hub_boost=1.0 (control)", ThalamicDSCN_G_v3, 1.0),
        ("Thalamic hub_boost=2.0",           ThalamicDSCN_G_v3, 2.0),
        ("Thalamic hub_boost=5.0",           ThalamicDSCN_G_v3, 5.0),
    ]
    param_sets = [
        ("baseline R4", 0.10, 15, 0.15),
        ("rediseño R4", 0.01, 150, 0.80),
    ]

    rows = []
    print("=" * 78)
    print("Fix del hub_boost (Ronda 5): reubicado a _apply_hijack_pull")
    print("=" * 78)
    for pname, td, hs, eh in param_sets:
        print(f"\n--- {pname}: θ_death={td} hijack_steps={hs} η_hijack={eh} ---")
        for label, cls, hb in configs:
            r = c3_stats(cls, td, hs, eh, seeds=seeds, steps=steps, hub_boost=hb)
            r.update(param_set=pname, label=label, hub_boost=hb)
            rows.append(r)
            md = f"{r['mean_delta_plv']:+.3f}" if r["mean_delta_plv"] is not None else "n/a"
            print(f"  {label:36s} events={r['n_events']:4d}  "
                  f"ΔPLV_mean={md}  rise_rate={r['rise_rate']*100:5.1f}%")

    with open("hub_boost_fix_results.json", "w") as f:
        json.dump(rows, f, indent=2)
    print("\n→ hub_boost_fix_results.json")
