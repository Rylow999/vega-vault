"""
Parte 2 del instrumento: simulacion, estadistica y observables.

Continuacion de gauge_instrument.py (se importa, no se duplica).
"""
import numpy as np
from collections import defaultdict

from gauge_instrument import (CONFIG, build_circulant, build_graph, loop_path,
                              classify_loop, area_min_bfs)


# --------------------------------------------------------------------------
# SU(2) y Metropolis
# --------------------------------------------------------------------------
def random_su2(rng):
    """SU(2) Haar-random via parametrizacion por quaternion."""
    x = rng.normal(size=4)
    x /= np.linalg.norm(x)
    u0, u1, u2, u3 = x
    return np.array([[u0 + 1j * u3, u2 + 1j * u1],
                     [-u2 + 1j * u1, u0 - 1j * u3]])


def su2_near_identity(epsilon, rng):
    """SU(2) cercana a la identidad, para la propuesta Metropolis."""
    x = rng.normal(size=3)
    x /= np.linalg.norm(x)
    angle = epsilon * rng.uniform(-1, 1)
    u0 = np.cos(angle)
    u1, u2, u3 = np.sin(angle) * x
    return np.array([[u0 + 1j * u3, u2 + 1j * u1],
                     [-u2 + 1j * u1, u0 - 1j * u3]])


def get_oriented(U, a, b):
    """U_ab a partir del diccionario que guarda una sola orientacion."""
    if (a, b) in U:
        return U[(a, b)]
    return U[(b, a)].conj().T


def plaquette_trace(tri, U):
    """tr(U_p) para el triangulo orientado i->j->k->i."""
    i, j, k = tri
    return np.real(np.trace(
        get_oriented(U, i, j) @ get_oriented(U, j, k) @ get_oriented(U, k, i)))


def wilson_loop(U, N, start, R, T, d1, d2):
    """Holonomia del loop, normalizada: tr(H)/2.

    El path se recorre DESDE `start` (no desde 0): los offsets del loop son
    relativos al punto de partida.
    """
    cur = start
    H = np.eye(2, dtype=complex)
    for d, n in [(d1, R), (d2, T), (-d1, R), (-d2, T)]:
        for _ in range(n):
            nxt = (cur + d) % N
            H = H @ get_oriented(U, cur, nxt)
            cur = nxt
    assert cur == start, "loop no cierra"
    return np.real(np.trace(H)) / 2


def metropolis_sweep(U, edges, triangles, beta, epsilon, rng):
    """Un sweep Metropolis sobre todos los links.

    La accion es S = (beta/2) * sum_p tr(U_p). El delta de la accion al
    cambiar un link es (beta/2) * (cambio en la suma de plaquetas que lo
    contienen).
    """
    accepted = 0
    for i, j in edges:
        old = U[(i, j)]
        relevant = [t for t in triangles if i in t and j in t]
        old_sum = sum(plaquette_trace(t, U) for t in relevant)

        R = su2_near_identity(epsilon, rng)
        new = R @ old
        U[(i, j)] = new
        U[(j, i)] = new.conj().T
        new_sum = sum(plaquette_trace(t, U) for t in relevant)

        delta = (beta / 2) * (new_sum - old_sum)
        if delta > 0 or rng.random() < np.exp(delta):
            accepted += 1
        else:
            U[(i, j)] = old
            U[(j, i)] = old.conj().T
    return accepted / len(edges)


# --------------------------------------------------------------------------
# Estadistica honesta
# --------------------------------------------------------------------------
def autocorr_tau(x, cmax=80):
    """tau_int estimado por autocorrelacion truncada (Geyer)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 10:
        return 0.5
    x = x - x.mean()
    var = np.dot(x, x) / n
    if var <= 0:
        return 0.5
    tau = 0.5
    for c in range(1, min(cmax, n // 2)):
        rho = np.dot(x[:-c], x[c:]) / (n * var)
        if rho <= 0.05:
            break
        tau += rho
    return max(tau, 0.5)


def block_error(x, n_blocks=16):
    """Error por bloques: std de las medias de bloque / sqrt(n_blocks).

    Devuelve (error, n_blocks_usados, tau_int, n_eff).
    """
    x = np.asarray(x, dtype=float)
    nb = min(n_blocks, len(x) // 10)
    if nb < 2:
        return float(np.std(x) / max(np.sqrt(len(x)), 1)), 1, 1.0, len(x)
    bs = len(x) // nb
    means = np.array([x[i * bs:(i + 1) * bs].mean() for i in range(nb)])
    err = float(np.std(means, ddof=1) / np.sqrt(nb))
    tau = autocorr_tau(x)
    n_eff = len(x) / tau
    return err, nb, tau, n_eff


# --------------------------------------------------------------------------
# Corrida
# --------------------------------------------------------------------------
def run_simulation(N, beta_values, shapes, d1, d2, n_therm, n_meas,
                   n_blocks, epsilon, seed, include_degenerate=False,
                   measure_absW=True, starts_step=2):
    """Simula y devuelve un dict con observables por beta y por loop.

    Cada loop se mide sobre `range(0, N, starts_step)` puntos de partida y se
    promedia (el grafo es circulante, los puntos son equivalentes).
    """
    rng = np.random.default_rng(seed)
    _, S_sym = build_circulant(N)
    edges, adj, triangles = build_graph(N, S_sym)

    # geometria de cada shape (precalculada)
    geo = {}
    for (R, T) in shapes:
        cls, path = classify_loop(N, d1, d2, R, T)
        A, status = area_min_bfs(N, d1, d2, R, T, triangles)
        geo[(R, T)] = {"clase": cls, "A_min": A, "area_status": status,
                       "perimetro": len({(min(a, b), max(a, b))
                                         for a, b in path}),
                       "n_aristas_path": len(path)}

    out = {"N": N, "d1": d1, "d2": d2, "seed": seed,
           "grafo": {"edges": len(edges), "triangulos": len(triangles),
                     "S_sym": len(S_sym)},
           "geometria": {f"{R},{T}": v for (R, T), v in geo.items()},
           "betas": {}}

    for beta in beta_values:
        U = {(i, j): random_su2(rng) for i, j in edges}
        for i, j in edges:
            U[(j, i)] = U[(i, j)].conj().T

        for _ in range(n_therm):
            metropolis_sweep(U, edges, triangles, beta, epsilon, rng)

        plaqs = []
        series = defaultdict(list)
        for _ in range(n_meas):
            metropolis_sweep(U, edges, triangles, beta, epsilon, rng)
            plaqs.append(np.mean([plaquette_trace(t, U) for t in triangles]) / 2)
            for (R, T) in shapes:
                g = geo[(R, T)]
                if g["clase"] != "SIMPLE" and not include_degenerate:
                    continue
                vals = [wilson_loop(U, N, i, R, T, d1, d2)
                        for i in range(0, N, starts_step)]
                series[(R, T)].append(float(np.mean(vals)))

        pe, pnb, ptau, pneff = block_error(plaqs, n_blocks)
        beta_res = {
            "plaq": {"mean": float(np.mean(plaqs)), "err": pe,
                     "tau": ptau, "n_eff": pneff, "n_blocks": pnb},
            "loops": {},
        }
        for (R, T), x in series.items():
            x = np.array(x)
            e, nb, tau, neff = block_error(x, n_blocks)
            g = geo[(R, T)]
            entry = {
                "clase": g["clase"],
                "A_min": g["A_min"],
                "perimetro": g["perimetro"],
                "W": {"mean": float(x.mean()), "err": e, "tau": tau,
                      "n_eff": neff, "n_blocks": nb},
            }
            if measure_absW:
                ab = np.abs(x)
                ae, _, atau, aneff = block_error(ab, n_blocks)
                entry["absW"] = {"mean": float(ab.mean()), "err": ae,
                                 "tau": atau, "n_eff": aneff}
                # z-score: el valor es distinguible de 0?
                entry["W"]["z"] = (float(x.mean()) / e) if e > 0 else None
            beta_res["loops"][f"{R},{T}"] = entry

        out["betas"][str(beta)] = beta_res
        print(f"  beta={beta:5.1f}  plaq={beta_res['plaq']['mean']:+.4f}"
              f" +- {pe:.4f}   (tau={ptau:.1f}, N_eff={pneff:.0f})")

    return out
