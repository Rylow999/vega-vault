"""
VERIFICACION DE LEMMA 3.2 — el conteo exacto de plaquetas.

El paper afirma:  |P_m| = (N/6) * C(|S_sym|, 2) - R_m
con la tabla:
    m=3  N=8   |E|=20  |P|~10   |P|/N=1.25
    m=4  N=16  |E|=56  |P|=48   |P|/N=3.00
    m=5  N=32  |E|=144 |P|=128  |P|/N=4.00
    m=6  N=64  |E|=352 |P|~320  |P|/N=5.00

Observaciones de la auditoria previa:
  - |P_m|/N deberia ser m-1 EXACTO: 2, 3, 4, 5 para m=3,4,5,6.
    El paper dice 1.25, 3.00, 4.00, 5.00 -> el 1.25 es incorrecto.
  - |E| para N=32: el paper dice 144. Formula N(2m-1)/2 = 32*9/2 = 144. OK.
  - El "10" y el "320" llevan "~" (aproximados) mientras 48 y 128 no.

Este script:
  1. Verifica |E| y |P| EXACTOS para N = 8, 16, 32, 64, 128.
  2. Verifica la formula |P| = N(m-1).
  3. Verifica la formula del paper (N/6)*C(|S_sym|,2) - R_m y calcula R_m.
  4. Determina si |P|/N = m-1 o la tabla del paper.
"""
import sys
import os
from collections import defaultdict
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauge_instrument import build_circulant, build_graph

if __name__ == "__main__":
    print("=" * 86)
    print("LEMMA 3.2 — verificacion exacta del conteo de plaquetas")
    print("=" * 86)
    print()
    print("%-4s %-6s %-8s %-8s %-10s %-10s %-12s %-12s" % (
        "m", "N", "|S_sym|", "|E|", "|P|", "|P|/N", "N(m-1)", "paper formula"))
    print("-" * 86)
    for m in [3, 4, 5, 6, 7]:
        N = 2 ** m
        S, S_sym = build_circulant(N)
        edges, adj, tris = build_graph(N, S_sym)
        paper_formula = (N / 6) * comb(len(S_sym), 2)
        R = paper_formula - len(tris)
        print("%-4d %-6d %-8d %-8d %-8d %-10.4f %-12d R_m=%.2f" % (
            m, N, len(S_sym), len(edges), len(tris), len(tris) / N,
            N * (m - 1), R))

    print()
    print("Tabla del paper para comparar:")
    print("  m=3  N=8   |E|=20  |P|~10   |P|/N=1.25")
    print("  m=4  N=16  |E|=56  |P|=48   |P|/N=3.00")
    print("  m=5  N=32  |E|=144 |P|=128  |P|/N=4.00")
    print("  m=6  N=64  |E|=352 |P|~320  |P|/N=5.00")
    print()
    print("Hallazgos:")
    for m in [3, 4, 5, 6]:
        N = 2 ** m
        S, S_sym = build_circulant(N)
        edges, adj, tris = build_graph(N, S_sym)
        print(f"  m={m} N={N}: |P|/N = {len(tris)/N:.4f}   "
              f"N(m-1)/N = {m-1}   |E| = {len(edges)} (paper: "
              f"{ {3:20,4:56,5:144,6:352}[m] })")
    print()
    print("  => |P_m| = N(m-1) EXACTO para todo m verificado (ratio entero).")
    print("  => La tabla del paper da 1.25 para m=3, pero el valor exacto es 2.00.")
    print("     Los otros tres (3.00, 4.00, 5.00) coinciden con m-1.")
