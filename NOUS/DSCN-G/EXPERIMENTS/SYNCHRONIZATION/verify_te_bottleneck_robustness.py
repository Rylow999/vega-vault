#!/usr/bin/env python3
"""
verify_te_bottleneck_robustness.py — Ronda 6: robustez de la métrica
TE-bottleneck (Φ_proxy_TE) propuesta en Ronda 5 / verify_phi_proxy_v3.py.

Pregunta: ¿el hallazgo "ΔMI sube, ΔTE-bottleneck baja durante el hijack"
depende de la partición root/periferia particular que se eligió, o de
usar VAR(1) en el estimador de Geweke? Se prueban:

PARTICIONES
  P0  root_vs_periphery   — la de Ronda 5 (baseline, sin cambios)
  P1  periphery_split     — CONTROL NEGATIVO: la periferia partida en dos
                             mitades arbitrarias (excluyendo la raíz).
                             Si el patrón (MI sube / TE baja) aparece
                             IGUAL acá, no sería específico del rol de la
                             raíz como "titiritero" — sería un artefacto
                             de cualquier partición durante sincronía alta.
                             Se espera que este control NO muestre el
                             mismo patrón tan marcado.
  P2  root_vs_1follower   — raíz contra un solo seguidor (el más cercano
                             en índice), en vez de la periferia agregada.
                             Prueba si el resultado depende de resumir la
                             periferia con el parámetro de orden de
                             Kuramoto (que ya de por sí impone estructura)
                             o se sostiene con la señal cruda de un nodo.

LAGS DEL VAR
  lag=1 (Ronda 5, sin cambios) y lag=2, para ver si el resultado depende
  de la memoria asumida en el estimador de Geweke.

Condiciones de simulación: mismas 2 de Ronda 5 relevantes (thalamic
queda retirado por decisión de esta ronda) — baseline R4 y rediseño R4,
ambas sobre DSCN_G_v3 puro.

Esto sigue sin estar aprobado como Claim 7 citable — es evidencia de
robustez metodológica, no un resultado nuevo de teoría.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3  # noqa: E402


# ── embeddings por partición ────────────────────────────────────────

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


def pt_periphery_split(sim):
    """Control negativo: periferia partida en dos mitades arbitrarias,
    SIN la raíz en ninguna de las dos."""
    if not sim.nodes_active or len(sim.nodes_active) < 5:
        return None
    others = sim.nodes_active[1:]
    half = len(others) // 2
    if half < 2:
        return None
    g1, g2 = others[:half], others[half:]
    z1 = np.mean(np.exp(1j * sim.phi[g1]))
    z2 = np.mean(np.exp(1j * sim.phi[g2]))
    return (float(z1.real), float(z1.imag), float(z2.real), float(z2.imag))


def pt_root_single_follower(sim):
    """Raíz contra un único seguidor (el primero de la lista de activos
    tras la raíz), sin agregación de periferia."""
    if not sim.nodes_active or len(sim.nodes_active) < 2:
        return None
    root = sim.nodes_active[0]
    follower = sim.nodes_active[1]
    root_pt = (np.cos(sim.phi[root]), np.sin(sim.phi[root]))
    f_pt = (np.cos(sim.phi[follower]), np.sin(sim.phi[follower]))
    return root_pt + f_pt


PARTITIONS = {
    "P0_root_vs_periphery": pt_root_periphery,
    "P1_periphery_split_CONTROL": pt_periphery_split,
    "P2_root_vs_single_follower": pt_root_single_follower,
}


# ── métricas (mismo estimador de Geweke que Ronda 5, ahora con lag variable) ──

def gaussian_mi_bipartition(pts: np.ndarray) -> float:
    T = pts.shape[0]
    if T < 20:
        return float("nan")
    cov_full = np.cov(pts, rowvar=False) + 1e-8 * np.eye(4)
    cov_A = cov_full[0:2, 0:2]
    cov_B = cov_full[2:4, 2:4]
    _, ldA = np.linalg.slogdet(cov_A)
    _, ldB = np.linalg.slogdet(cov_B)
    _, ldF = np.linalg.slogdet(cov_full)
    return float(0.5 * (ldA + ldB - ldF))


def _resid_cov(Y, P):
    beta, *_ = np.linalg.lstsq(P, Y, rcond=None)
    resid = Y - P @ beta
    return np.cov(resid, rowvar=False)


def _lagmat(A, lags):
    """Apila [A_{t-1},...,A_{t-lags}] en columnas, recortando el frente."""
    T = A.shape[0]
    cols = [A[lags - k: T - k] for k in range(1, lags + 1)]
    return np.hstack(cols)


def geweke_te(X: np.ndarray, Y: np.ndarray, lags: int = 1) -> float:
    """F_{Y->X} = 1/2 * ln(|Sr|/|Su|), VAR(lags) gaussiano."""
    T = X.shape[0]
    if T < 30 + lags:
        return float("nan")
    Xt = X[lags:]
    Xlag = _lagmat(X, lags)
    Ylag = _lagmat(Y, lags)
    n = Xt.shape[0]
    ones = np.ones((n, 1))
    P_restricted = np.hstack([ones, Xlag])
    P_full = np.hstack([ones, Xlag, Ylag])
    Sr = _resid_cov(Xt, P_restricted)
    Su = _resid_cov(Xt, P_full)
    dr, du = np.linalg.det(Sr), np.linalg.det(Su)
    if dr <= 0 or du <= 0 or du > dr:
        du = min(du, dr * (1 - 1e-9)) if dr > 0 else du
    if dr <= 0 or du <= 0:
        return float("nan")
    return float(0.5 * np.log(dr / du))


def te_bottleneck(pts: np.ndarray, lags: int = 1) -> float:
    A = pts[:, 0:2]
    B = pts[:, 2:4]
    f_a2b = geweke_te(B, A, lags=lags)
    f_b2a = geweke_te(A, B, lags=lags)
    if np.isnan(f_a2b) or np.isnan(f_b2a):
        return float("nan")
    return float(min(f_a2b, f_b2a))


# ── driver de simulación ────────────────────────────────────────────

def collect_all_partitions(theta_death, hijack_steps, eta_hijack,
                            seeds, steps, window):
    """Corre la simulación UNA vez por seed y extrae los puntos de las 3
    particiones en paralelo dentro del mismo loop (evita resimular)."""
    N_init = max(50, int(1.5 * (1.0 / theta_death)))
    per_seed = {pname: [] for pname in PARTITIONS}
    for s in range(seeds):
        sim = DSCN_G_v3(seed=s, N=N_init, alpha=5.0, theta_death=theta_death,
                         hijack_steps=hijack_steps, eta_hijack=eta_hijack)
        buf = {pname: dict(baseline=[], hijack=[]) for pname in PARTITIONS}
        for t in range(steps):
            sim.step()
            if not sim.nodes_active:
                break
            for pname, efn in PARTITIONS.items():
                pt = efn(sim)
                if pt is None or any(np.isnan(pt)):
                    continue
                if sim.in_hijack:
                    buf[pname]["hijack"].append(pt)
                elif t >= steps - window:
                    buf[pname]["baseline"].append(pt)
        for pname in PARTITIONS:
            b, h = buf[pname]["baseline"], buf[pname]["hijack"]
            per_seed[pname].append(dict(
                baseline=np.array(b) if b else None,
                hijack=np.array(h) if h else None,
            ))
    return per_seed


def summarize(label, partition_name, per_seed, theta_death, hijack_steps,
              eta_hijack, lags, seeds, steps, window):

    def agg(key, metric_fn):
        vals = []
        for d in per_seed:
            pts = d[key]
            if pts is None or len(pts) < 30 + lags:
                continue
            v = metric_fn(pts)
            if not (isinstance(v, float) and np.isnan(v)):
                vals.append(v)
        return vals

    mi_b = agg("baseline", gaussian_mi_bipartition)
    mi_h = agg("hijack", gaussian_mi_bipartition)
    te_b = agg("baseline", lambda p: te_bottleneck(p, lags=lags))
    te_h = agg("hijack", lambda p: te_bottleneck(p, lags=lags))

    n_valid_hijack = sum(1 for d in per_seed if d["hijack"] is not None
                          and len(d["hijack"]) >= 30 + lags)

    def m(v):
        return (float(np.mean(v)), float(np.std(v)), len(v)) if v else (float("nan"), float("nan"), 0)

    mi_bm, mi_bs, mi_bn = m(mi_b)
    mi_hm, mi_hs, mi_hn = m(mi_h)
    te_bm, te_bs, te_bn = m(te_b)
    te_hm, te_hs, te_hn = m(te_h)

    return dict(
        label=label, partition=partition_name, lags=lags,
        theta_death=theta_death, hijack_steps=hijack_steps, eta_hijack=eta_hijack,
        seeds=seeds, n_seeds_valid_hijack=n_valid_hijack,
        MI_baseline=(mi_bm, mi_bs, mi_bn), MI_hijack=(mi_hm, mi_hs, mi_hn),
        MI_delta=(mi_hm - mi_bm) if mi_bn and mi_hn else float("nan"),
        TE_baseline=(te_bm, te_bs, te_bn), TE_hijack=(te_hm, te_hs, te_hn),
        TE_delta=(te_hm - te_bm) if te_bn and te_hn else float("nan"),
    )


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--window", type=int, default=300)
    args = ap.parse_args()

    conditions = [
        dict(label="baseline_R4", theta_death=0.10, hijack_steps=15, eta_hijack=0.15),
        dict(label="rediseno_R4", theta_death=0.01, hijack_steps=150, eta_hijack=0.80),
    ]

    rows = []
    print("=" * 90)
    print("TE-bottleneck — robustez de partición y de orden del VAR (Ronda 6)")
    print(f"seeds={args.seeds}  steps={args.steps}  window={args.window}")
    print("=" * 90)

    for cond in conditions:
        print(f"\n>>> simulando condición {cond['label']} "
              f"(seeds={args.seeds}, steps={args.steps})...")
        per_seed_all = collect_all_partitions(
            cond["theta_death"], cond["hijack_steps"], cond["eta_hijack"],
            args.seeds, args.steps, args.window)
        for pname in PARTITIONS:
            for lags in (1, 2):
                r = summarize(cond["label"], pname, per_seed_all[pname],
                               cond["theta_death"], cond["hijack_steps"], cond["eta_hijack"],
                               lags, args.seeds, args.steps, args.window)
                rows.append(r)
                mi_dir = "SUBE" if r["MI_delta"] > 0 else ("BAJA" if r["MI_delta"] < 0 else "n/a")
                te_dir = "SUBE" if (not np.isnan(r["TE_delta"]) and r["TE_delta"] > 0) else \
                         ("BAJA" if (not np.isnan(r["TE_delta"]) and r["TE_delta"] < 0) else "n/a")
                print(f"\n{pname:28s} {cond['label']:14s} lag={lags}  "
                      f"hijack_windows_validas={r['n_seeds_valid_hijack']}/{args.seeds}")
                print(f"  MI:  base={r['MI_baseline'][0]:+.4f}±{r['MI_baseline'][1]:.4f} (n={r['MI_baseline'][2]})  "
                      f"hijack={r['MI_hijack'][0]:+.4f}±{r['MI_hijack'][1]:.4f} (n={r['MI_hijack'][2]})  "
                      f"Δ={r['MI_delta']:+.4f} {mi_dir}")
                print(f"  TE:  base={r['TE_baseline'][0]:+.4f}±{r['TE_baseline'][1]:.4f} (n={r['TE_baseline'][2]})  "
                      f"hijack={r['TE_hijack'][0]:+.4f}±{r['TE_hijack'][1]:.4f} (n={r['TE_hijack'][2]})  "
                      f"Δ={r['TE_delta']:+.4f} {te_dir}")

    out = os.path.join(os.path.dirname(__file__), "te_bottleneck_robustness_results.json")
    with open(out, "w") as f:
        json.dump(rows, f, indent=2, default=str)
    print(f"\n→ {out}")
