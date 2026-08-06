#!/usr/bin/env python3
"""
verify_phi_proxy.py — Claim 7: Φ_proxy scaling O(log N) (Ronda 4).

AVISO IMPORTANTE, léase antes de citar nada de este archivo: Φ_proxy no
tiene una definición formal en ningún documento del paquete (paper.md,
paper_structure.md, claims_falsifiable.md) — se menciona únicamente como
"pendiente", con la predicción de que debería escalar como O(log N), pero
sin fórmula. La definición de abajo es una PROPUESTA mía, no algo que ya
estuviera decidido. Es una operacionalización razonable y estándar
(información mutua gaussiana entre dos mitades del sistema, en el espíritu
de Barrett & Seth 2011 para "practical measures of integrated
information"), pero es una decisión de diseño que corresponde revisar y
aprobar (o reemplazar) antes de que esto entre al paper como Claim 7
verificado.

Definición propuesta:
  1. Se toman las trayectorias de fase φ_i(t) de los nodos activos en una
     ventana estacionaria (post-convergencia, últimos `window` pasos).
  2. Cada φ_i se embebe en (cos φ_i, sin φ_i) para respetar su naturaleza
     circular (usar φ directamente en una covarianza gaussiana ignora el
     wraparound en 2π).
  3. Se parte el sistema en dos mitades contiguas A/B (no búsqueda
     exhaustiva de la partición mínima de información — eso es O(2^n),
     intratable para n>~15 — así que esto es explícitamente una partición
     fija, de ahí el nombre "proxy").
  4. Φ_proxy = I(A;B) bajo aproximación gaussiana:
       I(A;B) = ½ · (log|Σ_A| + log|Σ_B| − log|Σ_full|)
     usando la covarianza muestral de la ventana embebida.

Segundo punto importante, no menor: T1 (homeostasis) hace que la
población activa converja a N_ss* casi sin importar N_init (ya
demostrado: N_init=4/50/200 dan N_ss*≈4.0/4.8/4.2). Por lo tanto barrer
N_init, como sugiere ingenuamente el criterio de falsificación original
("Medir Φ_proxy para N=[10,50,100,200,500]"), no mueve la población activa
real en absoluto — mediría Φ_proxy sobre el mismo N*≈4-5 una y otra vez.
Para que el experimento tenga sentido hay que mover N* de verdad, y la
única perilla que lo hace (T1: N_ss* ≤ 1/θ_death) es θ_death. Este script
barre θ_death, no N_init.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3  # noqa: E402


def phi_proxy_gaussian_mi(phi_traj: np.ndarray) -> float:
    """phi_traj: (T, n) trayectorias de fase de n nodos activos en una
    ventana de T pasos. Devuelve I(A;B) gaussiana entre dos mitades
    contiguas del sistema, en nats."""
    T, n = phi_traj.shape
    if n < 2 or T < 4 * n:
        return float("nan")

    cos_p = np.cos(phi_traj)
    sin_p = np.sin(phi_traj)
    # columnas intercaladas [cos0,sin0,cos1,sin1,...] para que cada nodo
    # quede junto a sí mismo en cualquier partición contigua
    emb = np.empty((T, 2 * n))
    emb[:, 0::2] = cos_p
    emb[:, 1::2] = sin_p

    half = n // 2
    if half < 1 or (n - half) < 1:
        return float("nan")
    idxA = list(range(0, 2 * half))
    idxB = list(range(2 * half, 2 * n))

    cov_full = np.cov(emb, rowvar=False) + 1e-6 * np.eye(2 * n)
    cov_A = cov_full[np.ix_(idxA, idxA)]
    cov_B = cov_full[np.ix_(idxB, idxB)]

    _, logdet_full = np.linalg.slogdet(cov_full)
    _, logdet_A = np.linalg.slogdet(cov_A)
    _, logdet_B = np.linalg.slogdet(cov_B)

    return float(0.5 * (logdet_A + logdet_B - logdet_full))


def run_scaling(theta_deaths, alpha=5.0, seeds=10, steps=2000, window=300,
                 N_init_headroom=1.5) -> list:
    results = []
    for td in theta_deaths:
        N_init = max(20, int(N_init_headroom * (1.0 / td)))
        Ns, phis = [], []
        for s in range(seeds):
            sim = DSCN_G_v3(N=N_init, alpha=alpha, theta_death=td, seed=s)
            phi_hist = []
            for t in range(steps):
                sim.step()
                if t >= steps - window and sim.nodes_active:
                    phi_hist.append(sim.phi[sim.nodes_active].copy())
            if not sim.nodes_active:
                continue
            n_active = len(sim.nodes_active)
            phi_hist = [h for h in phi_hist if len(h) == n_active]
            if len(phi_hist) < max(20, 4 * n_active):
                continue
            phi_arr = np.array(phi_hist)
            val = phi_proxy_gaussian_mi(phi_arr)
            if not np.isnan(val):
                Ns.append(n_active)
                phis.append(val)

        if not Ns:
            print(f"  θ_death={td}: sin corridas válidas (ventana insuficiente)")
            continue
        Ns = np.array(Ns); phis = np.array(phis)
        print(f"  θ_death={td:.3f}  N*={Ns.mean():5.2f}±{Ns.std():4.2f}  "
              f"Φ_proxy={phis.mean():7.4f}±{phis.std():6.4f}  "
              f"(n_valid={len(Ns)}/{seeds})")
        results.append(dict(theta_death=td, N_init=N_init,
                             N_mean=float(Ns.mean()), N_std=float(Ns.std()),
                             phi_proxy_mean=float(phis.mean()),
                             phi_proxy_std=float(phis.std()),
                             n_valid_seeds=int(len(Ns))))
    return results


def fit_scaling(results):
    """Ajusta Φ_proxy vs log(N) y vs N por separado (regresión lineal
    simple) y compara R² para decidir cuál ajusta mejor — eso es lo que
    realmente responde el criterio de falsificación de Claim 7, no una
    inspección visual."""
    Ns = np.array([r["N_mean"] for r in results])
    phis = np.array([r["phi_proxy_mean"] for r in results])

    def r_squared(x, y):
        if len(x) < 3 or np.std(x) == 0:
            return float("nan"), (float("nan"), float("nan"))
        A = np.vstack([x, np.ones_like(x)]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        pred = slope * x + intercept
        ss_res = np.sum((y - pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        return float(r2), (float(slope), float(intercept))

    r2_log, (slope_log, intercept_log) = r_squared(np.log(Ns), phis)
    r2_lin, (slope_lin, intercept_lin) = r_squared(Ns, phis)

    return dict(r2_vs_logN=r2_log, slope_vs_logN=slope_log, intercept_vs_logN=intercept_log,
                r2_vs_N=r2_lin, slope_vs_N=slope_lin, intercept_vs_N=intercept_lin,
                better_fit="log(N)" if (not np.isnan(r2_log) and r2_log > r2_lin) else "N")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--window", type=int, default=300)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    seeds = 3 if args.quick else args.seeds
    steps = 500 if args.quick else args.steps
    window = 100 if args.quick else args.window

    theta_deaths = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01]

    print("\n" + "=" * 70)
    print("Φ_proxy SCALING (Claim 7) — Ronda 4, definición propuesta")
    print("=" * 70)
    print(f"seeds={seeds}  steps={steps}  window={window}")
    print("(θ_death barrido, no N_init — ver docstring del módulo)")

    results = run_scaling(theta_deaths, seeds=seeds, steps=steps, window=window)
    fit = fit_scaling(results) if len(results) >= 3 else None

    if fit:
        print(f"\n  R² vs log(N)  = {fit['r2_vs_logN']:.4f}  (slope={fit['slope_vs_logN']:.4f})")
        print(f"  R² vs N       = {fit['r2_vs_N']:.4f}  (slope={fit['slope_vs_N']:.6f})")
        print(f"  Mejor ajuste: {fit['better_fit']}")

    out = dict(theta_deaths=theta_deaths, seeds=seeds, steps=steps, window=window,
               method="gaussian_MI_bipartition_proxy_PROPOSED_NOT_PREVIOUSLY_DEFINED",
               results=results, fit=fit)
    with open("phi_proxy_scaling_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n→ phi_proxy_scaling_results.json")
