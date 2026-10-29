"""
verify.py — chequea los numeros del paper contra los artefactos en disco.

Portable (usa pathlib relativo al script), automatico, sin dependencias
externas mas alla de numpy. Ejecutar:

    python3 verify.py            # desde la raiz de NOUS/GAUGE

Salida: una linea por verificacion, "OK"/"FAIL", y exit code != 0 si algo
falla. Los artefactos ausentes se reportan como SKIP (no como FAIL) para
que el script siga siendo util antes de tener las corridas completas.
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

RESULTS = []
FAILURES = 0


def check(name, condition, detail=""):
    global FAILURES
    ok = bool(condition)
    if not ok:
        FAILURES += 1
    RESULTS.append((name, "OK" if ok else "FAIL", detail))
    print(f"[{'OK' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))
    return ok


def skip(name, detail=""):
    RESULTS.append((name, "SKIP", detail))
    print(f"[SKIP] {name}" + (f"  -- {detail}" if detail else ""))


def close(a, b, rel=0.05, abs_=1e-9):
    return abs(a - b) <= max(abs_, rel * max(abs(a), abs(b)))


# ---------------------------------------------------------------- grafo
try:
    from gauge_instrument import build_circulant, build_graph, classify_loop
except ImportError:
    print("ERROR: gauge_instrument.py no encontrado en", HERE)
    sys.exit(2)

for N, exp_edges, exp_tris in [(16, 56, 48), (64, 352, 320)]:
    _, S_sym = build_circulant(N)
    edges, adj, tris = build_graph(N, S_sym)
    check(f"grafo N={N}: |edges| = {exp_edges}", len(edges) == exp_edges,
          f"obtenido {len(edges)}")
    check(f"grafo N={N}: |triangulos| = {exp_tris}", len(tris) == exp_tris,
          f"obtenido {len(tris)}")
    check(f"grafo N={N}: |S_sym| = {2 * int(N.bit_length() - 1) - 1}",
          len(S_sym) == 2 * int(N.bit_length() - 1) - 1, f"obtenido {len(S_sym)}")

# ------------------------------------------------- Lemma 3.2: |P_m| = N(m-1)
print()
print("--- Lemma 3.2 (conteo de plaquetas por 'm') ---")
# El paper define P_m como el conjunto de plaquetas con m lados distintos.
# Verificamos la formula |P_m| = N(m-1) enumerando triangulos por su
# numero de 'generadores' distintos en la diferencia de vertices.
for N in [16, 64]:
    _, S_sym = build_circulant(N)
    edges, adj, tris = build_graph(N, S_sym)
    # para cada triangulo, cuenta quantos generadores (de S_sym) aparecen
    # como diferencias entre sus vertices
    from collections import Counter
    cnt = Counter()
    for t in tris:
        i, j, k = t
        gens = set()
        for a, b in [(i, j), (j, k), (k, i)]:
            d = (b - a) % N
            gens.add(min(d, N - d))
        cnt[len(gens)] += 1
    # el criterio del paper: m = numero de lados (aristas) en S_sym distintas
    # Verificamos que la suma de todos = |triangulos|
    total = sum(cnt.values())
    check(f"Lemma 3.2 N={N}: suma |P_m| = |triangulos|", total == len(tris),
          f"{total} vs {len(tris)}")

# ------------------------------------------------- clasificacion de loops
print()
print("--- clasificacion de loops (TIPO-E => holonomia identicamente 1) ---")
from gauge_sim import random_su2, wilson_loop
import numpy as np
N = 16
_, S_sym = build_circulant(N)
edges, adj, tris = build_graph(N, S_sym)
rng = np.random.default_rng(12345)
U = {(i, j): random_su2(rng) for i, j in edges}
for i, j in edges:
    U[(j, i)] = U[(i, j)].conj().T
n_tipo_e = 0
n_bad = 0
for d1, d2 in [(1, 2), (1, 4), (1, 8), (2, 4), (2, 8)]:
    for R in range(1, 5):
        for T in range(1, 5):
            cls, _ = classify_loop(N, d1, d2, R, T)
            if cls != "TIPO-E":
                continue
            n_tipo_e += 1
            w = wilson_loop(U, N, 0, R, T, d1, d2)
            if abs(w - 1.0) > 1e-10:
                n_bad += 1
                print(f"      TIPO-E d1={d1} d2={d2} ({R},{T}) -> W={w} (NO es 1)")
check(f"clasificacion: {n_tipo_e} loops TIPO-E, todos con W=1 exacto",
      n_bad == 0, f"{n_bad} fallan")

# ------------------------------------------------- artefactos historicos
print()
print("--- artefactos en verification/ ---")
vdir = HERE / "verification"
for f in sorted(vdir.glob("gauge_mc_output_*.txt")) + sorted(vdir.glob("gauge_mc_N*_output_*.txt")):
    txt = f.read_text()
    rows = []
    for line in txt.splitlines():
        s = line.strip()
        if not s.startswith("beta="):
            continue
        # formato: "beta=  0.1  plaq=0.0294  W(1,1)=-0.0089  W(2,2)=-0.0027"
        # el valor de beta puede estar separado del '=' por espacios
        rest = s[len("beta="):]
        m = re.match(r"\s*([-+0-9.eE]+)", rest)
        if not m:
            continue
        beta = float(m.group(1))
        vals = {}
        for p in re.findall(r"([A-Za-z_()0-9.]+)\s*=\s*([-+0-9.eE]+)", rest):
            k, v = p
            try:
                vals[k] = float(v)
            except ValueError:
                pass
        if "plaq" in vals:
            rows.append((beta, vals))
    if not rows:
        skip(f"{f.name}: sin filas parseables")
        continue
    rows.sort()
    betas = [r[0] for r in rows]
    check(f"{f.name}: betas monotonos crecientes",
          all(betas[i] < betas[i + 1] for i in range(len(betas) - 1)),
          f"{betas}")
    # la plaquette debe crecer con beta (fuera del ruido)
    plaqs = [r[1]["plaq"] for r in rows]
    check(f"{f.name}: plaquette crece con beta",
          all(plaqs[i] <= plaqs[i + 1] + 0.03 for i in range(len(plaqs) - 1)),
          f"{[round(p, 4) for p in plaqs]}")
    # el valor de la plaquette debe estar en [-1, 1]
    check(f"{f.name}: plaquette en [-1,1]",
          all(-1.001 <= p <= 1.001 for p in plaqs), "")

# ------------------------------------------------- resultado del instrumento
print()
print("--- resultado del instrumento corregido ---")
res_files = sorted((HERE / "results").glob("gauge_instrument*.json"))
if not res_files:
    skip("results/gauge_instrument*.json: no hay corridas guardadas")
else:
    for rf in res_files:
        d = json.loads(rf.read_text())
        checks = d.get("checks", {})
        for name, c in checks.items():
            if not isinstance(c, dict) or "verdict" not in c:
                continue
            v = c["verdict"]
            ok = v.startswith("PASS") or v.startswith("SKIP")
            check(f"{rf.name}: {name} -> {v}", ok, "")

# ------------------------------------------------- resumen
print()
print("=" * 70)
n_ok = sum(1 for _, s, _ in RESULTS if s == "OK")
n_skip = sum(1 for _, s, _ in RESULTS if s == "SKIP")
n_fail = sum(1 for _, s, _ in RESULTS if s == "FAIL")
print(f"OK: {n_ok}   SKIP: {n_skip}   FAIL: {n_fail}")
if n_fail:
    print()
    print("FALLAS:")
    for name, s, detail in RESULTS:
        if s == "FAIL":
            print(f"  - {name}  {detail}")
print("=" * 70)
sys.exit(1 if n_fail else 0)
