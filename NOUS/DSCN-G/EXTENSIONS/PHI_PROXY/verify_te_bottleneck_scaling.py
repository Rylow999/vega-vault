#!/usr/bin/env python3
"""
verify_te_bottleneck_scaling.py — Ronda 6: repite el barrido de escalado
de Claim 7 (verify_phi_proxy.py, Ronda 4) pero con Φ_proxy_TE
(TE-bottleneck, partición root/periferia, lag=1) en vez de MI gaussiana
cruda entre dos mitades arbitrarias.

Motivo: Φ_proxy_TE (Ronda 5) pasó la prueba de robustez de Ronda 6
(control negativo P1 muestra un patrón distinto/opuesto al de P0/P2 —
ver AUDIT_NOTES_ROUND6.md) y fue aprobado por Delorien para reemplazar la
MI cruda de Ronda 4 como la definición operativa de Φ_proxy. La pregunta
original de Claim 7 (¿Φ_proxy escala como O(log N)?) nunca se re-testeó
con esta métrica — Ronda 5 solo comparó pre/durante-hijack a θ_death
fijo. Este script cierra ese pendiente.

Diseño: idéntico al barrido de Ronda 4 en escala (mismos θ_death, seeds,
steps, window) para que los resultados sean directamente comparables.
Se mide Φ_proxy_TE sobre la ventana ESTACIONARIA (post-convergencia, sin
hijack — los últimos `window` pasos no-hijack de la corrida), con
partición root/periferia (P0, la misma que Ronda 5) y VAR(1) (lag=1,
el que se probó y validó en Ronda 6). Se usan los parámetros de hijack
por defecto (baseline R4: hijack_steps=15, η=0.15) — el rediseño C3
(θ_death=0.01, hijack_steps=150, η=0.80) es una configuración aparte que
no aplica acá; lo único que este script necesita del hijack es que NO
contamine la ventana estacionaria, y la recolección ya filtra por
sim.in_hijack==False.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3  # noqa: E402


def pt_root_periphery(sim):
    if not sim.nodes_active:
        return None
    root = sim.nodes_active[0]
    others = sim.nodes_active[1:]
    root_pt = (np.cos(sim.phi[root]), np.sin(sim.phi[root]))
    if len(others) >= 2:
        z = np.mean(np.exp(1j * sim.phi[others]))
        b_pt = (float(z.real), float(z.imag))
    else:
        b_pt = (float("nan"), float("nan"))
    return root_pt + b_pt


def _resid_cov(Y, P):
    beta, *_ = np.linalg.lstsq(P, Y, rcond=None)
    resid = Y - P @ beta
    return np.cov(resid, rowvar=False)


def geweke_te(X: np.ndarray, Y: np.ndarray) -> float:
    """lag=1, la formulación aprobada en Ronda 6."""
    T = X.shape[0]
    if T < 31:
        return float("nan")
    Xt, Xlag, Ylag = X[1:], X[:-1], Y[:-1]
    n = Xt.shape[0]
    ones = np.ones((n, 1))
    Sr = _resid_cov(Xt, np.hstack([ones, Xlag]))
    Su = _resid_cov(Xt, np.hstack([ones, Xlag, Ylag]))
    dr, du = np.linalg.det(Sr), np.linalg.det(Su)
    if dr <= 0 or du <= 0 or du > dr:
        du = min(du, dr * (1 - 1e-9)) if dr > 0 else du
    if dr <= 0 or du <= 0:
        return float("nan")
    return float(0.5 * np.log(dr / du))


def te_bottleneck(pts: np.ndarray) -> float:
    root, periph = pts[:, 0:2], pts[:, 2:4]
    f_r2p = geweke_te(periph, root)
    f_p2r = geweke_te(root, periph)
    if np.isnan(f_r2p) or np.isnan(f_p2r):
        return float("nan")
    return float(min(f_r2p, f_p2r))


def run_condition(theta_death, N_init, seeds, steps, window,
                   hijack_steps=15, eta_hijack=0.15, alpha=5.0):
    n_active, phis = [], []
    for s in range(seeds):
        sim = DSCN_G_v3(seed=s, N=N_init, alpha=alpha, theta_death=theta_death,
                         hijack_steps=hijack_steps, eta_hijack=eta_hijack)
        baseline_pts = []
        for t in range(steps):
            sim.step()
            if not sim.nodes_active:
                break
            if not sim.in_hijack and t >= steps - window:
                pt = pt_root_periphery(sim)
                if pt is not None and not any(np.isnan(pt)):
                    baseline_pts.append(pt)
        if sim.nodes_active:
            n_active.append(len(sim.nodes_active))
        if len(baseline_pts) >= 31:
            phi = te_bottleneck(np.array(baseline_pts))
            if not np.isnan(phi):
                phis.append(phi)
    return n_active, phis


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--window", type=int, default=300)
    args = ap.parse_args()

    theta_deaths = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    N_inits = {0.5: 20, 0.2: 20, 0.1: 20, 0.05: 30, 0.02: 75, 0.01: 150}

    print("=" * 78)
    print("Φ_proxy_TE (TE-bottleneck, P0 root/periferia, lag=1) vs θ_death")
    print(f"seeds={args.seeds}  steps={args.steps}  window={args.window}")
    print("=" * 78)

    results = []
    for td in theta_deaths:
        n_active, phis = run_condition(td, N_inits[td], args.seeds, args.steps, args.window)
        if len(n_active) == 0:
            print(f"θ_death={td}: sin corridas válidas (N* colapsó a <2, no hay periferia)")
            continue
        n_mean, n_std = float(np.mean(n_active)), float(np.std(n_active))
        if phis:
            phi_mean, phi_std = float(np.mean(phis)), float(np.std(phis))
        else:
            phi_mean, phi_std = float("nan"), float("nan")
        results.append(dict(theta_death=td, N_init=N_inits[td], N_mean=n_mean, N_std=n_std,
                             phi_proxy_TE_mean=phi_mean, phi_proxy_TE_std=phi_std,
                             n_valid_seeds=len(phis), n_seeds_total=args.seeds))
        print(f"θ_death={td:5.2f}  N*={n_mean:5.2f}±{n_std:4.2f}  "
              f"Φ_proxy_TE={phi_mean:+.4f}±{phi_std:.4f}  (válidas {len(phis)}/{args.seeds})")

    # fit vs log(N) and vs N, sólo con puntos válidos (>=2 seeds válidas)
    fit_rows = [r for r in results if r["n_valid_seeds"] >= 2]
    fit = {}
    if len(fit_rows) >= 3:
        Ns = np.array([r["N_mean"] for r in fit_rows])
        Phis = np.array([r["phi_proxy_TE_mean"] for r in fit_rows])
        logN = np.log(Ns)
        for name, xvar in [("logN", logN), ("N", Ns)]:
            A = np.vstack([xvar, np.ones_like(xvar)]).T
            slope, intercept = np.linalg.lstsq(A, Phis, rcond=None)[0]
            pred = slope * xvar + intercept
            ss_res = np.sum((Phis - pred) ** 2)
            ss_tot = np.sum((Phis - np.mean(Phis)) ** 2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
            fit[f"r2_vs_{name}"] = float(r2)
            fit[f"slope_vs_{name}"] = float(slope)
            fit[f"intercept_vs_{name}"] = float(intercept)
        fit["better_fit"] = "log(N)" if fit["r2_vs_logN"] > fit["r2_vs_N"] else "N"
        print("\nAjuste:")
        print(f"  R² vs log(N) = {fit['r2_vs_logN']:.3f}")
        print(f"  R² vs N      = {fit['r2_vs_N']:.3f}")
        print(f"  mejor ajuste: {fit['better_fit']}")
    else:
        print("\nMenos de 3 puntos válidos — no se intenta ajuste.")

    out = dict(theta_deaths=theta_deaths, seeds=args.seeds, steps=args.steps,
               window=args.window, method="TE_bottleneck_P0_lag1_APPROVED_ROUND6",
               results=results, fit=fit)
    outpath = os.path.join(os.path.dirname(__file__), "te_bottleneck_scaling_results.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n→ {outpath}")
