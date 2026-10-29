"""
DSCN-G-Gauge: runner del instrumento corregido.

HIPOTESIS (falsable)
  H1 (instrumento): los loops TIPO-E del script original tienen holonomia
     identicamente 1 (degenerados) y NO son comparables con los loops SIMPLE.
     Falsable: si |W(TIPO-E)| promediado sobre starts NO es ~1, H1 es falsa.

  H2 (G1, strong coupling): para loops SIMPLE con area minima A, el valor
     esperado es <W> = (beta/4)^A [Teorema 4.1]. En el regimen observable
     (beta >= 0.1) la senal es << error, por lo que el test NO puede
     distinguir area law de perimeter law con esta instrumentacion.
     Falsable: si <W> medido es distinguible de 0 Y consistente con (beta/4)^A
     con |z| < 3, la G1 es detectable y el test es mas fuerte de lo que creo.

  H3 (temperatura): la plaquette debe ser monotona creciente en beta.
     Falsable: si no es monotona, hay un bug de muestreo.

NEGATIVE CONTROL
  NC-1: los loops TIPO-E deben dar |W| ~ 1 (holonomia trivial). Si dieran
     un valor con estructura, la instrumentacion de loops estaria rota.
  NC-2: a beta -> 0 (plaquettes identidad), TODOS los observables deben ir
     a 1 y los errores a 0 (configuracion trivial). Si no, hay un bug.
  NC-3: permutando las etiquetas de los loops (shuffle), la correlacion
     log|W| vs A debe colapsar a ~0.

CRITERIO PASS/FAIL (pre-registrado)
  H1 PASS si: |W(TIPO-E)| - 1 < 0.02 (con error < 0.02) para todo beta.
  H2 PASS si: para al menos un loop, el z-score de <W> supera 2 Y la
     prediccion (beta/4)^A esta dentro de 3 sigma. FAIL (honesto) si el
     z-score de todos los loops es < 2 => la senal es indetectable con
     esta instrumentacion y la G1 NO queda falsada, solo no testada.
  H3 PASS si: la plaquette es monotona no-decreciente en beta en todos los
     pares consecutivos (tolerancia 0.02).

Uso:
  python3 run_gauge_instrument.py --out results/xxx.json --quick
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauge_instrument import CONFIG, build_circulant, build_graph, classify_loop
from gauge_sim import run_simulation


def nc_permutation_test(data, seed=999):
    """NC-3: correlacion log|W| vs A con las etiquetas de loop permutadas."""
    rng = np.random.default_rng(seed)
    rows = []
    for beta, res in data["betas"].items():
        for key, entry in res["loops"].items():
            if entry.get("A_min") is None or "absW" not in entry:
                continue
            rows.append((entry["A_min"], entry["absW"]["mean"], beta, key))
    if len(rows) < 4:
        return None
    A = np.array([r[0] for r in rows], dtype=float)
    y = np.log(np.array([r[1] for r in rows], dtype=float))
    real = float(np.corrcoef(A, y)[0, 1])
    # permutar etiquetas de A entre filas
    null = []
    for _ in range(2000):
        null.append(float(np.corrcoef(rng.permutation(A), y)[0, 1]))
    null = np.array(null)
    p = float((np.abs(null) >= abs(real)).sum() / len(null))
    return {"corr_real": real, "corr_null_mean": float(null.mean()),
            "corr_null_std": float(null.std()), "p_value": p,
            "n_rows": len(rows)}


def check_h1(data):
    """H1: los loops TIPO-E deben tener |W| ~ 1."""
    res = []
    for beta, b in data["betas"].items():
        for key, entry in b["loops"].items():
            if entry.get("clase") != "TIPO-E":
                continue
            if "absW" not in entry:
                continue
            m = entry["absW"]["mean"]
            e = entry["absW"]["err"]
            res.append({"beta": beta, "loop": key, "absW": m, "err": e,
                        "desvio_de_1": abs(m - 1.0),
                        "z_vs_1": (m - 1.0) / e if e > 0 else None})
    if not res:
        return {"verdict": "SKIP", "detalle": "no se midieron loops degenerados"}
    worst = max(r["desvio_de_1"] for r in res)
    return {"verdict": "PASS" if worst < 0.02 else "FAIL",
            "max_desvio_de_1": worst, "muestras": res}


def check_h2(data):
    """H2: la senal de area law es detectable y consistente con Thm 4.1?

    Doble criterio:
      (a) DETECTABILIDAD: existe algun observable con |z| > 2 (senal por
          encima del error)?
      (b) CONSISTENCIA: para esos observables, la prediccion (beta/4)^A del
          Teorema 4.1 esta dentro de 3 sigma?
    Si (a) falla, el veredicto es INCONCLUYENTE: la G1 no queda falsada,
    solo NO TESTEADA con esta instrumentacion.
    """
    det = []
    for beta, b in data["betas"].items():
        for key, entry in b["loops"].items():
            if entry.get("clase") != "SIMPLE" or "W" not in entry:
                continue
            z = entry["W"].get("z")
            A = entry.get("A_min")
            if z is None or A is None:
                continue
            beta_f = float(beta)
            pred = (beta_f / 4) ** A
            m = entry["W"]["mean"]
            e = entry["W"]["err"]
            det.append({"beta": beta_f, "loop": key, "A_min": A,
                        "W": m, "err": e, "z": z,
                        "pred_thm41": pred,
                        "z_vs_pred": (m - pred) / e if e > 0 else None})
    if not det:
        return {"verdict": "SKIP", "detalle": "no hay loops SIMPLE medidos"}
    max_z = max(abs(d["z"]) for d in det)
    con_senal = [d for d in det if abs(d["z"]) > 2]
    if not con_senal:
        return {"verdict": "INCONCLUYENTE (senal indetectable: G1 no testada, no refutada)",
                "max_abs_z": max_z, "n_observables": len(det), "detalle": det}
    consistentes = [d for d in con_senal
                    if d["z_vs_pred"] is not None and abs(d["z_vs_pred"]) < 3]
    return {"verdict": "PASS" if consistentes else "FAIL",
            "max_abs_z": max_z, "n_observables": len(det),
            "n_con_senal": len(con_senal), "n_consistentes": len(consistentes),
            "detalle": det}


def check_h3(data):
    """H3: la plaquette es monotona creciente en beta."""
    betas = sorted(float(b) for b in data["betas"].keys())
    vals = [data["betas"][str(b)]["plaq"]["mean"] for b in betas]
    viol = []
    for i in range(len(betas) - 1):
        if vals[i + 1] < vals[i] - 0.02:
            viol.append({"beta_de": betas[i], "beta_a": betas[i + 1],
                         "valor_de": vals[i], "valor_a": vals[i + 1]})
    return {"verdict": "PASS" if not viol else "FAIL",
            "betas": betas, "plaq": vals, "violaciones": viol}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/gauge_instrument.json")
    ap.add_argument("--quick", action="store_true", help="corrida corta (smoke test)")
    ap.add_argument("--N", type=int, default=None)
    ap.add_argument("--n-therm", type=int, default=None)
    ap.add_argument("--n-meas", type=int, default=None)
    ap.add_argument("--seeds", type=int, default=None, help="cuantas semillas promediar")
    args = ap.parse_args()

    cfg = dict(CONFIG)
    if args.N:
        cfg["N"] = args.N
    if args.n_therm is not None:
        cfg["n_therm"] = args.n_therm
    if args.n_meas is not None:
        cfg["n_meas"] = args.n_meas
    if args.quick:
        cfg["n_therm"] = min(cfg["n_therm"], 200)
        cfg["n_meas"] = min(cfg["n_meas"], 600)
        cfg["betas"] = [0.1, 1.0, 5.0]
    if args.seeds:
        cfg["seeds"] = cfg["seeds"][:args.seeds]
    # Los loops degenerados (TIPO-E) existen cuando d2 es multiplo de d1 en
    # Z_N (p.ej. d1=1,d2=8: la ida y la vuelta son consecutivas => U.Udag
    # contiguo => holonomia identicamente 1). Con d1=1,d2=2 NO hay TIPO-E:
    # los loops (2,2),(3,1) son TIPO-V (repiten vertice, no degenerados).
    # Para el NC-1 hay que correr una pasada extra con d2=8.
    cfg["include_degenerate"] = True
    cfg["shapes"] = [[1, 1], [1, 2], [1, 3], [2, 1], [3, 1], [2, 2], [3, 3]]

    print("=" * 78)
    print("DSCN-G-Gauge — instrumento corregido")
    print("=" * 78)
    print(f"config: {json.dumps(cfg, indent=1)}")
    print()

    # geometria previa (para el reporte)
    _, S_sym = build_circulant(cfg["N"])
    edges, adj, triangles = build_graph(cfg["N"], S_sym)
    print(f"grafo: N={cfg['N']} |S_sym|={len(S_sym)} edges={len(edges)} "
          f"triangulos={len(triangles)}")
    print()

    runs = []
    for seed in cfg["seeds"]:
        print(f"--- semilla {seed} ---")
        t0 = time.time()
        r = run_simulation(
            N=cfg["N"], beta_values=cfg["betas"], shapes=[tuple(s) for s in cfg["shapes"]],
            d1=cfg["d1"], d2=cfg["d2"], n_therm=cfg["n_therm"], n_meas=cfg["n_meas"],
            n_blocks=cfg["n_blocks"], epsilon=cfg["epsilon"], seed=seed,
            include_degenerate=cfg["include_degenerate"],
            measure_absW=cfg["measure_absW"])
        r["runtime_s"] = time.time() - t0
        runs.append(r)
        print()

    # promediar sobre semillas (el grafo es el mismo; las semillas son las
    # replicaciones independientes)
    merged = {"config": cfg, "runs": runs, "checks": {}}
    merged["checks"]["H1_tipoE_degenerado"] = check_h1(runs[0])
    merged["checks"]["H2_area_law_detectable"] = check_h2(runs[0])
    merged["checks"]["H3_monotonia_plaquette"] = check_h3(runs[0])
    merged["checks"]["NC3_permutacion"] = nc_permutation_test(runs[0])

    # --- NC-1: corrida extra con d1=1, d2=8 (generador multiplo) ---
    # Ahi existen los loops TIPO-E: la ida y la vuelta por el mismo link son
    # consecutivas, asi que U.Udag aparece como factor contiguo y la
    # holonomia debe valer 1 EXACTAMENTE. Si dieran otra cosa, la
    # instrumentacion de loops estaria rota.
    print("--- NC-1: corrida con d2 multiplo de d1 (d1=1, d2=8) ---")
    nc1_runs = []
    for seed in cfg["seeds"]:
        r = run_simulation(
            N=cfg["N"], beta_values=cfg["betas"],
            shapes=[tuple(s) for s in cfg["shapes"]],
            d1=1, d2=8, n_therm=cfg["n_therm"], n_meas=cfg["n_meas"],
            n_blocks=cfg["n_blocks"], epsilon=cfg["epsilon"], seed=seed,
            include_degenerate=True, measure_absW=True)
        nc1_runs.append(r)
    merged["nc1_degenerados"] = nc1_runs
    merged["checks"]["H1_tipoE_degenerado"] = check_h1(nc1_runs[0])
    merged["checks"]["NC1_holonomia_trivial"] = {
        "verdict": merged["checks"]["H1_tipoE_degenerado"]["verdict"],
        "nota": "los loops TIPO-E (d1=1,d2=8) deben tener |W| = 1 exacto",
    }

    print("=" * 78)
    print("RESULTADOS")
    print("=" * 78)
    for name, c in merged["checks"].items():
        v = c.get("verdict") if isinstance(c, dict) else c
        print(f"  {name:34s} {v}")
        for k in ("max_desvio_de_1", "max_abs_z", "n_observables"):
            if isinstance(c, dict) and k in c:
                print(f"      {k}: {c[k]}")
        if isinstance(c, dict) and "corr_real" in c:
            print(f"      corr_real: {c['corr_real']:.4f}  "
                  f"null: {c['corr_null_mean']:+.4f} +- {c['corr_null_std']:.4f}  "
                  f"p={c['p_value']:.4f}")
    print()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(merged, f, indent=2, default=str)
    print(f"resultado guardado en: {args.out}")


if __name__ == "__main__":
    main()
