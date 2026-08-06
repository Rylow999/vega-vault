#!/usr/bin/env python3
"""
verify_phi_proxy_v3.py — Ronda 5: fix del Φ_proxy de Ronda 4.

Por qué se reemplaza `phi_proxy_gaussian_mi` (ver `verify_phi_proxy.py`,
Ronda 4): esa métrica usaba (a) una partición arbitraria del sistema en
dos mitades contiguas por índice, sin relación con la estructura del
modelo, y (b) información mutua cruda entre las dos mitades. Al correrla
comparando ventana pre-hijack vs. ventana durante-hijack (experimento que
Ronda 4 no había hecho — barría θ_death, no el hijack), dio el resultado
opuesto al esperado: la MI cruda SUBE durante el hijack en vez de caer.
Diagnóstico (ver AUDIT_NOTES_ROUND5.md): la MI cruda no distingue
"integración genuina" de "arrastre" (entrainment) — un titiritero y su
marioneta comparten muchísima información mutua (la marioneta es
predecible a partir del titiritero) sin que eso sea integración en el
sentido de IIT, que exige que la información sea sinérgica/bidireccional,
no que dos señales estén correlacionadas porque una dicta a la otra.

Dos cambios en este módulo:

1. Partición: root vs. periferia (no dos mitades arbitrarias) — es la
   partición que tiene sentido dado el rol estructural del root
   (`nodes_active[0]`, el driver durante el hijack). El root se embebe
   como (cos φ_root, sin φ_root); la periferia se resume con el parámetro
   de orden de Kuramoto del grupo excluyendo la raíz,
   z = mean(exp(i·φ_others)) → (Re z, Im z). Esto mantiene la
   dimensionalidad fija en 2D de cada lado incluso si N* cambia entre
   configuraciones o se pierden nodos por poda, y es la misma cantidad
   que ya usa `plv_intra_group()` en el núcleo (consistencia con el resto
   del paquete).

2. Métrica: en vez de I(root;periferia) por MI gaussiana cruda, se usa
   una medida de retroalimentación lineal de Geweke (1982) —
   transfer entropy gaussiana vía log-det de covarianzas residuales de
   VAR(1) — calculada en LAS DOS direcciones (root→periferia y
   periferia→root), y se reporta el MÍNIMO de las dos como "integración
   genuina" (Φ_proxy_TE). Razonamiento: un sistema solo integra
   información en el sentido fuerte si el flujo es significativo en
   ambas direcciones (análogo a la partición de información mínima de
   IIT: la integración la limita el enlace más débil, no el más fuerte).
   Arrastre puro (root→periferia fuerte, periferia→root ≈0) hace que el
   mínimo caiga a ~0 aunque la MI cruda entre ambos sea alta — esa es
   exactamente la distinción que la métrica de Ronda 4 no podía hacer.

   F_{Y→X} = ½·ln( |Σ_R| / |Σ_U| )
     Σ_R = covarianza residual de  X_t ~ 1 + X_{t−1}         (restringido)
     Σ_U = covarianza residual de  X_t ~ 1 + X_{t−1} + Y_{t−1} (completo)
   (misma convención de normalización de ½·log-det que ya usaba
   `phi_proxy_gaussian_mi` en Ronda 4, para que los números sean
   comparables en unidades — nats.)

Se reportan AMBAS métricas (MI cruda de Ronda 4 y TE-bottleneck nueva)
sobre la MISMA partición root/periferia, en ventana pre-hijack
("baseline", últimos `window` pasos no-hijack de la corrida) y ventana
durante-hijack (todos los pasos con `sim.in_hijack == True`,
concatenados dentro de cada seed). El núcleo (`verify_dscng_v3.py`) NO se
toca — se orquesta desde afuera llamando `sim.step()` e inspeccionando
atributos públicos, igual que Ronda 4.

AVISO: igual que en Ronda 4, esto es una propuesta de definición, no algo
previamente acordado — requiere aprobación antes de citarse como Claim 7
verificado en el paper.
"""
import sys, os, json, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3  # noqa: E402
from thalamic_model import ThalamicDSCN_G_v3  # noqa: E402


# ── embeddings ─────────────────────────────────────────────────────

def _root_periph_point(sim):
    """(root_x, root_y, periph_x, periph_y) para el paso actual."""
    if not sim.nodes_active:
        return None
    root = sim.nodes_active[0]
    others = sim.nodes_active[1:]
    root_pt = (np.cos(sim.phi[root]), np.sin(sim.phi[root]))
    if len(others) >= 2:
        z = np.mean(np.exp(1j * sim.phi[others]))
        periph_pt = (float(z.real), float(z.imag))
    else:
        periph_pt = (float("nan"), float("nan"))
    return root_pt + periph_pt


# ── metrics on a (T,4) array [root_x,root_y,periph_x,periph_y] ─────

def gaussian_mi_bipartition(pts: np.ndarray) -> float:
    """MI gaussiana cruda I(root;periferia) — métrica de Ronda 4,
    reportada acá solo para comparación directa sobre la misma
    partición root/periferia."""
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
    """Covarianza residual de la regresión OLS multivariada Y ~ P."""
    beta, *_ = np.linalg.lstsq(P, Y, rcond=None)
    resid = Y - P @ beta
    return np.cov(resid, rowvar=False)


def geweke_te(X: np.ndarray, Y: np.ndarray) -> float:
    """F_{Y->X} = ½·ln(|Σ_R|/|Σ_U|), VAR(1) gaussiano. X,Y: (T,2)."""
    T = X.shape[0]
    if T < 30:
        return float("nan")
    Xt, Xlag, Ylag = X[1:], X[:-1], Y[:-1]
    n = Xt.shape[0]
    ones = np.ones((n, 1))
    P_restricted = np.hstack([ones, Xlag])
    P_full = np.hstack([ones, Xlag, Ylag])
    Sr = _resid_cov(Xt, P_restricted)
    Su = _resid_cov(Xt, P_full)
    dr, du = np.linalg.det(Sr), np.linalg.det(Su)
    if dr <= 0 or du <= 0 or du > dr:  # du>dr shouldn't happen (nested models); guard numerics
        du = min(du, dr * (1 - 1e-9)) if dr > 0 else du
    if dr <= 0 or du <= 0:
        return float("nan")
    return float(0.5 * np.log(dr / du))


def te_bottleneck(pts: np.ndarray) -> dict:
    """Devuelve F_root->periph, F_periph->root, y su mínimo (Φ_proxy_TE)."""
    root = pts[:, 0:2]
    periph = pts[:, 2:4]
    f_r2p = geweke_te(periph, root)   # root predice periferia -> flujo root->periph
    f_p2r = geweke_te(root, periph)   # periferia predice root -> flujo periph->root
    if np.isnan(f_r2p) or np.isnan(f_p2r):
        bottleneck = float("nan")
    else:
        bottleneck = min(f_r2p, f_p2r)
    return dict(F_root_to_periph=f_r2p, F_periph_to_root=f_p2r,
                phi_proxy_TE=bottleneck)


# ── simulation driver ────────────────────────────────────────────

def collect_windows(model_cls, theta_death, hijack_steps, eta_hijack,
                     seeds=15, steps=2000, window=300, alpha=5.0,
                     N_init_headroom=1.5, hub_boost=None):
    N_init = max(50, int(N_init_headroom * (1.0 / theta_death)))
    per_seed = []  # list of dicts: baseline_pts, hijack_pts (each (T,4) or None)

    for s in range(seeds):
        kw = dict(seed=s, N=N_init, alpha=alpha, theta_death=theta_death,
                   hijack_steps=hijack_steps, eta_hijack=eta_hijack)
        if hub_boost is not None:
            kw["hub_boost"] = hub_boost
        sim = model_cls(**kw)

        baseline_pts, hijack_pts = [], []
        for t in range(steps):
            sim.step()
            if not sim.nodes_active:
                break
            pt = _root_periph_point(sim)
            if pt is None or any(np.isnan(pt)):
                continue
            if sim.in_hijack:
                hijack_pts.append(pt)
            elif t >= steps - window:
                baseline_pts.append(pt)

        per_seed.append(dict(
            baseline=np.array(baseline_pts) if baseline_pts else None,
            hijack=np.array(hijack_pts) if hijack_pts else None,
        ))
    return per_seed


def summarize_condition(label, model_cls, theta_death, hijack_steps,
                         eta_hijack, seeds=15, steps=2000, window=300,
                         hub_boost=None):
    per_seed = collect_windows(model_cls, theta_death, hijack_steps,
                                eta_hijack, seeds=seeds, steps=steps,
                                window=window, hub_boost=hub_boost)

    def agg(key, metric_fn):
        vals = []
        for d in per_seed:
            pts = d[key]
            if pts is None or len(pts) < 30:
                continue
            v = metric_fn(pts)
            if isinstance(v, dict):
                v = v["phi_proxy_TE"]
            if not (isinstance(v, float) and np.isnan(v)):
                vals.append(v)
        return vals

    mi_baseline = agg("baseline", gaussian_mi_bipartition)
    mi_hijack = agg("hijack", gaussian_mi_bipartition)
    te_baseline = agg("baseline", lambda p: te_bottleneck(p)["phi_proxy_TE"])
    te_hijack = agg("hijack", lambda p: te_bottleneck(p)["phi_proxy_TE"])

    n_seeds_with_hijack = sum(1 for d in per_seed if d["hijack"] is not None
                               and len(d["hijack"]) >= 30)
    hijack_sample_sizes = [len(d["hijack"]) for d in per_seed if d["hijack"] is not None]

    def m(v):
        return (float(np.mean(v)), float(np.std(v))) if v else (float("nan"), float("nan"))

    mi_b_m, mi_b_s = m(mi_baseline)
    mi_h_m, mi_h_s = m(mi_hijack)
    te_b_m, te_b_s = m(te_baseline)
    te_h_m, te_h_s = m(te_hijack)

    row = dict(
        label=label, theta_death=theta_death, hijack_steps=hijack_steps,
        eta_hijack=eta_hijack, hub_boost=hub_boost, seeds=seeds, steps=steps,
        n_seeds_with_valid_hijack_window=n_seeds_with_hijack,
        hijack_sample_sizes=hijack_sample_sizes,
        MI_baseline_mean=mi_b_m, MI_baseline_std=mi_b_s,
        MI_hijack_mean=mi_h_m, MI_hijack_std=mi_h_s,
        MI_delta=(mi_h_m - mi_b_m) if not np.isnan(mi_h_m) and not np.isnan(mi_b_m) else float("nan"),
        TE_baseline_mean=te_b_m, TE_baseline_std=te_b_s,
        TE_hijack_mean=te_h_m, TE_hijack_std=te_h_s,
        TE_delta=(te_h_m - te_b_m) if not np.isnan(te_h_m) and not np.isnan(te_b_m) else float("nan"),
    )
    return row


def print_row(r):
    hb = f"{r['hub_boost']:.1f}" if r["hub_boost"] is not None else "—"
    print(f"\n{r['label']}  (θ_death={r['theta_death']}, hijack_steps={r['hijack_steps']}, "
          f"η_hijack={r['eta_hijack']}, hub_boost={hb})")
    print(f"  ventanas de hijack válidas (≥30 muestras): "
          f"{r['n_seeds_with_valid_hijack_window']}/{r['seeds']} seeds  "
          f"tamaños={r['hijack_sample_sizes']}")
    print(f"  MI cruda (Ronda 4):  baseline={r['MI_baseline_mean']:.3f}±{r['MI_baseline_std']:.3f}  "
          f"hijack={r['MI_hijack_mean']:.3f}±{r['MI_hijack_std']:.3f}  "
          f"Δ={r['MI_delta']:+.3f}  {'SUBE' if r['MI_delta']>0 else 'BAJA' if r['MI_delta']<0 else 'n/a'}")
    print(f"  TE-bottleneck (v3):  baseline={r['TE_baseline_mean']:.3f}±{r['TE_baseline_std']:.3f}  "
          f"hijack={r['TE_hijack_mean']:.3f}±{r['TE_hijack_std']:.3f}  "
          f"Δ={r['TE_delta']:+.3f}  {'SUBE' if r['TE_delta']>0 else 'BAJA' if r['TE_delta']<0 else 'n/a'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=15)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--window", type=int, default=300)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    seeds = 5 if args.quick else args.seeds
    steps = 500 if args.quick else args.steps
    window = 100 if args.quick else args.window

    print("=" * 78)
    print("Φ_proxy v3 (Ronda 5) — partición root/periferia, TE-bottleneck vs MI cruda")
    print("=" * 78)
    print(f"seeds={seeds}  steps={steps}  window={window}")

    conditions = [
        dict(label="DSCN_G_v3  (baseline R4)", model_cls=DSCN_G_v3,
             theta_death=0.10, hijack_steps=15, eta_hijack=0.15, hub_boost=None),
        dict(label="DSCN_G_v3  (rediseño R4)", model_cls=DSCN_G_v3,
             theta_death=0.01, hijack_steps=150, eta_hijack=0.80, hub_boost=None),
        dict(label="Thalamic   (baseline R4, hub_boost=5.0)", model_cls=ThalamicDSCN_G_v3,
             theta_death=0.10, hijack_steps=15, eta_hijack=0.15, hub_boost=5.0),
        dict(label="Thalamic   (rediseño R4, hub_boost=5.0)", model_cls=ThalamicDSCN_G_v3,
             theta_death=0.01, hijack_steps=150, eta_hijack=0.80, hub_boost=5.0),
    ]

    rows = []
    for c in conditions:
        r = summarize_condition(c["label"], c["model_cls"], c["theta_death"],
                                 c["hijack_steps"], c["eta_hijack"],
                                 seeds=seeds, steps=steps, window=window,
                                 hub_boost=c["hub_boost"])
        rows.append(r)
        print_row(r)

    print("\n" + "=" * 78)
    print("RESUMEN")
    print("=" * 78)
    print(f"{'condición':42s} {'ΔMI':>8s} {'ΔTE':>8s}")
    for r in rows:
        print(f"{r['label']:42s} {r['MI_delta']:+8.3f} {r['TE_delta']:+8.3f}")

    with open("phi_proxy_v3_results.json", "w") as f:
        json.dump(rows, f, indent=2, default=str)
    print("\n→ phi_proxy_v3_results.json")
