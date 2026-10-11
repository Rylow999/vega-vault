"""
DSCN-G-Gauge: Monte Carlo verification
SU(2) lattice gauge theory on fractal circulant C_N(S)
Author: Luciano Benjamín Nieto, 2026
License: MIT
"""
import numpy as np
from collections import defaultdict

def build_circulant(N):
    """Build fractal circulant S = {1, 2, 4, ..., N/2}."""
    m = int(np.log2(N))
    S = [2**k for k in range(m)]
    S_sym = set(S) | {(N - d) % N for d in S}
    S_sym.discard(0)
    return S, sorted(S_sym)

def build_graph(N, S_sym):
    """Build edges, adjacency, and triangular plaquettes."""
    edges = set()
    adj = defaultdict(set)
    for i in range(N):
        for d in S_sym:
            j = (i + d) % N
            adj[i].add(j)
            if i < j: edges.add((i, j))
            elif i > j: edges.add((j, i))
    
    triangles = set()
    for i in range(N):
        for j in adj[i]:
            if j <= i: continue
            for k in adj[j]:
                if k <= j: continue
                if k in adj[i]:
                    triangles.add(tuple(sorted([i, j, k])))
    
    return list(edges), adj, list(triangles)

def random_su2():
    """Haar-random SU(2) matrix via quaternion parametrization."""
    x = np.random.normal(size=4)
    x /= np.linalg.norm(x)
    u0, u1, u2, u3 = x
    return np.array([[u0+1j*u3, u2+1j*u1],
                     [-u2+1j*u1, u0-1j*u3]])

def su2_near_identity(epsilon):
    """SU(2) matrix close to identity for Metropolis proposals."""
    x = np.random.normal(size=3)
    x /= np.linalg.norm(x)
    angle = epsilon * np.random.uniform(-1, 1)
    u0 = np.cos(angle)
    u1, u2, u3 = np.sin(angle) * x
    return np.array([[u0+1j*u3, u2+1j*u1],
                     [-u2+1j*u1, u0-1j*u3]])

def get_oriented(U, a, b):
    """Get U_{ab} from dictionary storing only one orientation."""
    if (a, b) in U: return U[(a, b)]
    return U[(b, a)].conj().T

def plaquette_trace(tri, U):
    """Compute tr(U_p) for oriented triangle i->j->k->i."""
    i, j, k = tri
    return np.real(np.trace(
        get_oriented(U, i, j) @ get_oriented(U, j, k) @ get_oriented(U, k, i)
    ))

def wilson_loop(U, N, start, R, T, d1, d2):
    """Rectangular Wilson loop: R steps of d1, T of d2, R of -d1, T of -d2."""
    cur = start
    H = np.eye(2, dtype=complex)
    for d, n_steps in [(d1, R), (d2, T), (-d1, R), (-d2, T)]:
        for _ in range(n_steps):
            nxt = (cur + d) % N
            H = H @ get_oriented(U, cur, nxt)
            cur = nxt
    assert cur == start, "Loop did not close"
    return np.real(np.trace(H)) / 2

def metropolis_sweep(U, edges, triangles, beta, epsilon):
    """One full Metropolis sweep over all links."""
    accepted = 0
    for i, j in edges:
        old = U[(i, j)]
        relevant = [t for t in triangles if i in t and j in t]
        old_sum = sum(plaquette_trace(t, U) for t in relevant)
        
        R = su2_near_identity(epsilon)
        new = R @ old
        U[(i, j)] = new
        U[(j, i)] = new.conj().T
        new_sum = sum(plaquette_trace(t, U) for t in relevant)
        
        delta = (beta / 2) * (new_sum - old_sum)
        if delta > 0 or np.random.random() < np.exp(delta):
            accepted += 1
        else:
            U[(i, j)] = old
            U[(j, i)] = old.conj().T
    return accepted / len(edges)

def run_simulation(N, beta_values, n_therm=300, n_meas=300, epsilon=0.3):
    """Full simulation pipeline."""
    S, S_sym = build_circulant(N)
    edges, adj, triangles = build_graph(N, S_sym)
    print(f"N={N}, |S|={len(S)}, edges={len(edges)}, triangles={len(triangles)}")
    
    d1, d2 = 1, 2  # generators for Wilson loops
    
    for beta in beta_values:
        U = {(i, j): random_su2() for i, j in edges}
        for i, j in edges: U[(j, i)] = U[(i, j)].conj().T
        
        for _ in range(n_therm):
            metropolis_sweep(U, edges, triangles, beta, epsilon)
        
        plaqs, wl_data = [], defaultdict(list)
        for _ in range(n_meas):
            metropolis_sweep(U, edges, triangles, beta, epsilon)
            plaqs.append(np.mean([plaquette_trace(t, U) for t in triangles]) / 2)
            for R, T in [(1,1), (1,2), (2,2), (2,3), (3,3)]:
                vals = [wilson_loop(U, N, i, R, T, d1, d2) for i in range(0, N, 2)]
                wl_data[(R, T)].append(np.mean(vals))
        
        print(f"beta={beta:5.1f}  plaq={np.mean(plaqs):.4f}  "
              f"W(1,1)={np.mean(wl_data[(1,1)]):.4f}  "
              f"W(2,2)={np.mean(wl_data[(2,2)]):.4f}")

if __name__ == "__main__":
    run_simulation(N=16, beta_values=[0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0])
    # Para resultados cuantitativos: run_simulation(N=64, ...)
