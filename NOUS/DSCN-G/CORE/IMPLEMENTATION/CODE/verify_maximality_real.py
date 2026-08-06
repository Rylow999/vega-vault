#!/usr/bin/env python3
"""
verify_maximality_real.py — Ronda 4: prueba REAL de la sub-claim de
maximalidad de T1 (iii), pedido explícito de R en esta ronda.

Qué reemplaza: verify_theorem_1() en verify_dscng_v3.py aproxima el
comportamiento a N_ss*+1 con una fórmula (`rho_approx = K/n_test`), que
según claims_falsifiable.md reporta "suspicious" siempre, en toda corrida.
Eso no es evidencia de que la maximalidad sea falsa — es que la fórmula no
simula nada real. verify_dscng_v3.py NO se tocó (sigue igual, sigue siendo
la fuente de T1/T2/T3/C3 "aproximados"); este archivo es un experimento
nuevo y separado, igual que nback_v6 no tocó nback_v5.

Diseño del experimento real:
  1. Correr la simulación exactamente como T1 (mismo N_init, alpha,
     theta_death, seeds, steps) hasta que converge a N* (igual que antes).
  2. Sobre esa población ya convergida, forzar la población a N*+1 —
     agregando un nodo genuinamente nuevo (vitalidad plena, ω y φ
     inicializados igual que al arranque). Se agrega un nodo nuevo en vez
     de "revivir" uno podado porque algunos N_init (p.ej. N_init=4) nunca
     podan a nadie — no hay de dónde revivir, así que la operacionalización
     correcta y uniforme en los 3 casos es agregar un nodo nuevo.
  3. Medir el ρ_eff REAL (Herfindahl real de la distribución de las K
     cadenas, no la fórmula) en el instante en que la población es N*+1,
     ANTES de que la dinámica tenga chance de podar — esto es el chequeo
     directo de la condición (ii) al tamaño N*+1 con un ρ_eff medido, no
     inventado.
  4. Dejar correr la dinámica normal (poda incluida) por otros `steps`
     pasos más, y medir a dónde converge realmente la población. Si vuelve
     a N* (se poda el nodo agregado), eso es evidencia empírica directa de
     maximalidad: el sistema no sostiene N*+1 como punto fijo estable.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3, DEFAULTS  # noqa: E402


def herfindahl(sim) -> float:
    """Mismo cálculo que usa verify_theorem_1 (línea ~388 de
    verify_dscng_v3.py), extraído acá para no duplicarlo mal."""
    if not sim.nodes_active:
        return 0.0
    act = np.zeros(len(sim.nodes_active))
    for pos in sim.chain_positions:
        if pos in sim.nodes_active:
            act[sim.nodes_active.index(pos)] += 1
    if act.sum() > 0:
        act /= act.sum()
        return float(np.sum(act ** 2))
    return 0.0


def force_add_node(sim, init_vitality=1.0) -> int:
    """Agrega un nodo genuinamente nuevo al sistema ya convergido, con
    ω/φ inicializados igual que en __init__. Extiende los arrays fijos
    (omega, phi, vitality) en vez de reusar un índice podado, para que
    funcione igual sin importar si hubo poda o no.

    init_vitality es un parámetro deliberado (no fijo en 1.0): arrancar
    con vitalidad plena le da al nodo nuevo margen para sobrevivir varios
    cientos de pasos sin actividad antes de decaer bajo θ_death (con
    γ=0.01, decaimiento lento). Si eso resulta ser la causa de que el
    nodo sobreviva en el experimento principal (init_vitality=1.0), un
    nodo inyectado justo en el umbral (init_vitality=θ_death) es el
    control que lo aísla."""
    new_idx = sim.N
    sim.omega = np.vstack([sim.omega, sim.rng.normal(0, 0.1, (1, sim.d))])
    sim.phi = np.append(sim.phi, sim.rng.uniform(0, 2 * np.pi))
    sim.vitality = np.append(sim.vitality, init_vitality)
    sim.N += 1
    sim.nodes_active.append(new_idx)
    return new_idx


def verify_maximality_real(alpha=5.0, theta_death=0.10, N_inits=(4, 50, 200),
                            seeds=DEFAULTS["seeds"], steps=DEFAULTS["steps"],
                            post_perturb_steps=None, init_vitality=1.0,
                            label="full_vitality") -> dict:
    if post_perturb_steps is None:
        post_perturb_steps = steps  # same duration as the original convergence phase

    t2 = theta_death ** 2
    print("\n" + "=" * 70)
    print(f"MAXIMALIDAD DE T1 — simulación real de N* + 1 (Ronda 4) [{label}]")
    print("=" * 70)
    print(f"alpha={alpha}  theta_death={theta_death}  seeds={seeds}  "
          f"steps={steps}  post_perturb_steps={post_perturb_steps}  "
          f"init_vitality={init_vitality}")

    results = []
    for N_init in N_inits:
        Nstar_vals = []
        rho_at_np1_vals = []           # ρ_eff medido EN EL INSTANTE de N*+1
        fp_violated_immediately = []   # condición (ii) falla apenas se fuerza N*+1?
        N_final_vals = []              # población tras post_perturb_steps más
        pruned_back = []               # ¿volvió a N* (o menos)?

        for s in range(seeds):
            sim = DSCN_G_v3(N=N_init, alpha=alpha, theta_death=theta_death, seed=s)
            for _ in range(steps):
                sim.step()
            if not sim.nodes_active:
                continue  # extinción total, caso degenerado, se excluye
            Nstar = len(sim.nodes_active)
            Nstar_vals.append(Nstar)

            force_add_node(sim, init_vitality=init_vitality)
            n_np1 = len(sim.nodes_active)
            rho_immediate = herfindahl(sim)
            rho_at_np1_vals.append(rho_immediate)
            fp_violated_immediately.append(bool(rho_immediate < n_np1 * t2))

            for _ in range(post_perturb_steps):
                sim.step()
                if not sim.nodes_active:
                    break

            N_final = len(sim.nodes_active)
            N_final_vals.append(N_final)
            pruned_back.append(bool(N_final <= Nstar))

        Nstar_vals = np.array(Nstar_vals)
        N_final_vals = np.array(N_final_vals)
        rho_at_np1_vals = np.array(rho_at_np1_vals)

        frac_violated_immediately = float(np.mean(fp_violated_immediately))
        frac_pruned_back = float(np.mean(pruned_back))

        print(f"\n  N_init={N_init:3d}: N*={Nstar_vals.mean():.2f}±{Nstar_vals.std():.2f}  "
              f"(n={len(Nstar_vals)} valid seeds)")
        print(f"    Forzado a N*+1: ρ_eff real={rho_at_np1_vals.mean():.4f}±{rho_at_np1_vals.std():.4f}  "
              f"→ condición (ii) VIOLADA inmediatamente en "
              f"{frac_violated_immediately*100:.0f}% de los seeds")
        print(f"    Tras {post_perturb_steps} pasos más con poda activa: "
              f"N_final={N_final_vals.mean():.2f}±{N_final_vals.std():.2f}  "
              f"→ podado de vuelta a ≤N* en {frac_pruned_back*100:.0f}% de los seeds")
        maximal_real = bool(frac_pruned_back >= 0.9 and frac_violated_immediately >= 0.9)
        print(f"    Maximalidad real: {'✓ SOSTENIDA' if maximal_real else '✗ NO sostenida'} "
              f"(criterio: ≥90% de los seeds violan (ii) Y se podan de vuelta)")

        results.append(dict(
            N_init=N_init,
            N_star_mean=float(Nstar_vals.mean()), N_star_std=float(Nstar_vals.std()),
            n_valid_seeds=int(len(Nstar_vals)),
            rho_at_Nplus1_mean=float(rho_at_np1_vals.mean()),
            rho_at_Nplus1_std=float(rho_at_np1_vals.std()),
            frac_fixed_point_violated_immediately=frac_violated_immediately,
            N_final_after_post_perturb_mean=float(N_final_vals.mean()),
            N_final_after_post_perturb_std=float(N_final_vals.std()),
            frac_pruned_back_to_star=frac_pruned_back,
            maximal_real=maximal_real,
        ))

    return dict(alpha=alpha, theta_death=theta_death, seeds=seeds, steps=steps,
                post_perturb_steps=post_perturb_steps, init_vitality=init_vitality,
                label=label, results=results)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=DEFAULTS["seeds"])
    ap.add_argument("--steps", type=int, default=DEFAULTS["steps"])
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    seeds = 5 if args.quick else args.seeds
    steps = 500 if args.quick else args.steps

    report_full_vitality = verify_maximality_real(
        seeds=seeds, steps=steps, init_vitality=1.0, label="full_vitality")

    # Control: inject the extra node right at the death threshold instead of
    # full vitality, to check whether "full vitality" was giving it an
    # unrealistic head start that explains why it survives.
    report_boundary = verify_maximality_real(
        seeds=seeds, steps=steps, init_vitality=0.10, label="boundary_vitality")

    out = dict(full_vitality=report_full_vitality, boundary_vitality=report_boundary)
    with open("maximality_real_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n→ maximality_real_results.json")
