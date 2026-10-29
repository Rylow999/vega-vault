"""
VERIFICACION INDEPENDIENTE DEL TEOREMA 4.2 (weak coupling).

El paper predice (Teorema 4.2):
    <W(C)> ~ exp(-C_F * P / beta),  con C_F = 3/4 (caso fundamental SU(2))
Para una plaqueta triangular, P = 3:
    <tr(U_p)/2> ~ 1 - (C_F * P) / (2 * beta)      [el 1/2 es por el factor tr/2]
  => coeficiente de 1/beta = C_F * P / 2 = 3 * 0.75 / 2 = 1.125

O con la convencion de la accion exp((beta/2) tr U_p):
    el coeficiente de la accion es beta/2, asi que el termino de orden 1/beta
    es C_F * P / (2 * beta) * (beta/2) = C_F * P / 4 ... etc.

Este script mide el coeficiente de 1/beta de la plaquette DIRECTAMENTE, sin
asumir la forma funcional, y lo compara con los candidatos:
    C_F * P / 2      (P=3, C_F=3/4)  = 1.125
    C_F * P          (P=3, C_F=3/4)  = 2.25
    3/2             (caso abeliano SU(2)->U(1), C_F=1/2)
    1.287           (valor medido previamente)

Metodo: para beta grande, calcular c(beta) = (1 - <plaq>) * beta.
Si <plaq> = 1 - k/beta + O(1/beta^2), entonces c(beta) -> k.
Se mide en beta = 10, 20, 40, 80, 160.

Ademas: se verifica el orden 1/beta con un fit de <plaq> vs 1/beta
(lineal) y se reporta el residuo para confirmar que el orden siguiente es
1/beta^2 y no 1/beta^(3/2) (que seria indicio de logaritmo).
"""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauge_instrument import build_circulant, build_graph
from gauge_sim import random_su2, su2_near_identity, plaquette_trace, block_error


def sweep(U, edges, triangles, beta, epsilon, rng):
    for i, j in edges:
        old = U[(i, j)]
        rel = [t for t in triangles if i in t and j in t]
        os_ = sum(plaquette_trace(t, U) for t in rel)
        R = su2_near_identity(epsilon, rng)
        new = R @ old
        U[(i, j)] = new
        U[(j, i)] = new.conj().T
        ns = sum(plaquette_trace(t, U) for t in rel)
        d = (beta / 2) * (ns - os_)
        if d > 0 or rng.random() < np.exp(d):
            pass
        else:
            U[(i, j)] = old
            U[(j, i)] = old.conj().T


def measure_plaq(N, beta, n_therm, n_meas, seed):
    rng = np.random.default_rng(seed)
    _, S_sym = build_circulant(N)
    edges, adj, triangles = build_graph(N, S_sym)
    U = {(i, j): random_su2(rng) for i, j in edges}
    for i, j in edges:
        U[(j, i)] = U[(i, j)].conj().T
    for _ in range(n_therm):
        sweep(U, edges, triangles, beta, 0.3, rng)
    vals = []
    for _ in range(n_meas):
        sweep(U, edges, triangles, beta, 0.3, rng)
        vals.append(np.mean([plaquette_trace(t, U) for t in triangles]) / 2)
    return np.array(vals)


if __name__ == "__main__":
    N = 16
    print("=" * 78)
    print("TEOREMA 4.2 — coeficiente de 1/beta en la plaquette (medicion directa)")
    print("=" * 78)
    print()
    rows = []
    for beta in [10, 20, 40, 80, 160]:
        # mas termalizacion en beta alto (la configuracion se ordena)
        vals = measure_plaq(N, beta, 400, 3000, seed=1000 + beta)
        m = vals.mean()
        e, nb, tau, neff = block_error(vals, 16)
        c = (1.0 - m) * beta
        ce = e * beta
        rows.append((beta, m, e, c, ce))
        print(f"  beta={beta:5}  plaq={m:.8f} +- {e:.8f}   "
              f"c=(1-plaq)*beta = {c:.5f} +- {ce:.5f}   (tau={tau:.1f}, N_eff={neff:.0f})")
    print()
    cs = np.array([r[3] for r in rows])
    ces = np.array([r[4] for r in rows])
    w = 1.0 / ces ** 2
    c_mean = float(np.sum(w * cs) / np.sum(w))
    c_err = float(1.0 / np.sqrt(np.sum(w)))
    print(f"  c inversamente ponderado = {c_mean:.5f} +- {c_err:.5f}")
    print()
    print("  Candidatos:")
    P = 3
    for label, val in [
        ("C_F*P/2 con C_F=3/4 (prediccion si <plaq> ~ 1 - C_F P/(2 beta))", 0.75 * P / 2),
        ("C_F*P   con C_F=3/4 (prediccion del paper)", 0.75 * P),
        ("C_F*P/2 con C_F=1/2 (abeliano)", 0.5 * P / 2),
        ("C_F*P   con C_F=1/2 (abeliano)", 0.5 * P),
        ("1.5 (C_F=1, P/2)", 1.5),
    ]:
        z = (c_mean - val) / c_err
        mark = "  <<< COINCIDE" if abs(z) < 3 else ""
        print(f"    {label:<62} = {val:.4f}   z={z:+8.2f}{mark}")
    print()
    print("  Verificacion del orden 1/beta: fit de <plaq> vs 1/beta")
    inv = np.array([1.0 / r[0] for r in rows])
    vals = np.array([r[1] for r in rows])
    A = np.vstack([np.ones_like(inv), inv]).T
    coef, *_ = np.linalg.lstsq(A, vals, rcond=None)
    pred = A @ coef
    resid = vals - pred
    print(f"    fit: <plaq> = {coef[0]:.8f} + ({coef[1]:.5f}) / beta")
    print(f"    coeficiente de 1/beta del fit = {-coef[1]:.5f}")
    print(f"    residuo max = {np.max(np.abs(resid)):.2e}")
    # si el orden fuera 1/beta^(3/2) (log), el residuo del fit 1/beta seria ~1/beta
    print(f"    residuo relativo max = {np.max(np.abs(resid)) / np.max(np.abs(vals)):.2e}")
    # test explicito de 1/beta^2: comparar residuos
    inv2 = inv ** 2
    A2 = np.vstack([np.ones_like(inv), inv, inv2]).T
    coef2, *_ = np.linalg.lstsq(A2, vals, rcond=None)
    r2 = vals - A2 @ coef2
    print(f"    con termino 1/beta^2: residuo max = {np.max(np.abs(r2)):.2e}")
    print(f"    coeficiente de 1/beta^2 = {coef2[2]:.5f}")
