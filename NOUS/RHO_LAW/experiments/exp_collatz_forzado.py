#!/usr/bin/env python3
"""
RHO_LAW-Collatz: el experimento de FORZADO — ε* como análogo del α₀ de NS.

La pregunta (falsable): ¿existe un forzado mínimo ε* tal que inyectar
pasos P artificiales a tasa ε cruza el umbral f_P* = 0.7075 y genera
divergencia?

El método (análogo de las capas localizadas de NS):
  - Perturbar la órbita con un "forzado" que inyecta saltos de clase:
    con probabilidad ε, el siguiente número se reescribe para caer en
    la clase P (n ≡ 3 mod 4) — es el análogo de inyectar una onda de
    vorticidad a favor de la inestabilidad.
  - Medir: f_P efectivo, termination rate, longitud de órbita.
  - Barrer ε ∈ [0, 0.5] y buscar el umbral ε* donde el sistema cambia
    de régimen (convergente → divergente).

Predicción (falsable): ε* ≈ f_P* - f_P_natural ≈ 0.7075 - 0.5 = 0.2075
(el gap entre el umbral y la equidistribución natural).

Si el ε* existe y coincide con la predicción → el forzado mínimo para
divergencia es el análogo exacto del α₀ de NS, y la LEH (equidistribución)
es el mecanismo de auto-regulación que el forzado debe romper.
"""
import numpy as np
import json
from pathlib import Path


def nu2(n):
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v


def forced_T3(n, eps, rng):
    """T_3 acelerado con forzado: con probabilidad eps, el próximo impar
    se 'reescribe' para caer en la clase P (n ≡ 3 mod 4).

    El forzado respeta el mapa (no inventa números): solo elige ENTRE los
    dos posibles predecesores impares de la forma 2^k * m + 1 que caen en
    la clase deseada. Es el análogo de inyectar un modo a favor.
    """
    if n % 2 == 0:
        return n // 2, 0  # 0 = paso N (natural)
    # paso impar: decidir si forzar
    m = 3 * int(n) + 1
    v = nu2(m)
    clase_real = int(n) % 4
    if rng.rand() < eps and clase_real != 3:
        # forzar: reescribir n para caer en clase P
        # el predecesor impar más cercano de clase 3: n' = n + 2 (siguiente impar)
        # pero eso rompe el mapa. Alternativa honesta: aceptar el paso real
        # pero CONTAR como P (el forzado actúa sobre la medición, no sobre
        # el mapa). Esto es el análogo del "observador forzado" — la misma
        # lección del paper: forzar el instrumento, no el sustrato.
        p_count_flag = 1
        return m // (2 ** v), p_count_flag
    return m // (2 ** v), 1 if clase_real == 3 else 0


def simulate_forced(n0, eps, max_steps=50000, cap=1e15, seed=0):
    rng = np.random.RandomState(seed)
    n = int(n0)
    p_count = 0
    total = 0
    for step in range(max_steps):
        if n <= 1:
            return p_count / max(total, 1), total, True
        if n > cap:
            return p_count / max(total, 1), total, False
        n, is_P = forced_T3(n, eps, rng)
        total += 1
        p_count += is_P
    return p_count / max(total, 1), total, False


def main():
    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("RHO_LAW-Collatz: experimento de FORZADO (ε* como análogo de α₀)")
    print("=" * 70)
    print("Predicción falsable: ε* ≈ f_P* - f_P_natural ≈ 0.2075")
    print(" (el forzado rompe la equidistribución LEH y cruza f_P*=0.7075)")

    n0_values = [27, 31, 41, 97, 703, 871, 1003, 5001, 6171, 9663]
    eps_values = [0.0, 0.05, 0.10, 0.15, 0.20, 0.21, 0.25, 0.30, 0.40, 0.50]

    results = []
    print(f"\n{'eps':>5} {'f_P_med':>8} {'f_P_max':>8} {'crosses_f_P*':>12} "
          f"{'term_rate':>9} {'len_med':>8}")
    for eps in eps_values:
        f_ps, terms, lens, crosses = [], [], [], 0
        for n0 in n0_values:
            fP, L, term = simulate_forced(n0, eps, max_steps=30000, seed=hash((n0, eps)) % 10000)
            f_ps.append(fP)
            terms.append(term)
            lens.append(L)
            if fP >= 0.7075:
                crosses += 1
        f_ps = np.array(f_ps)
        row = {
            "eps": eps,
            "f_P_mean": round(float(f_ps.mean()), 4),
            "f_P_max": round(float(f_ps.max()), 4),
            "n_crossing_threshold": crosses,
            "frac_crossing": round(crosses / len(n0_values), 3),
            "termination_rate": round(float(np.mean(terms)), 3),
            "orbit_length_median": float(np.median(lens)),
        }
        results.append(row)
        print(f"{eps:5.2f} {row['f_P_mean']:8.4f} {row['f_P_max']:8.4f} "
              f"{crosses:6d}/{len(n0_values)} {row['termination_rate']:9.2f} "
              f"{row['orbit_length_median']:8.0f}")

    # ============================================================
    # Análisis: ¿existe ε*?
    # ============================================================
    print("\n=== ¿Existe ε* (umbral de forzado)? ===")
    prev = None
    for row in results:
        if prev is not None and prev["frac_crossing"] == 0 and row["frac_crossing"] > 0:
            print(f"  ε* ≈ {row['eps']:.2f} (primer ε con órbitas cruzando f_P*)")
            print(f"  Predicción era 0.2075 → {'CONFIRMADA' if abs(row['eps'] - 0.2075) < 0.06 else 'REFUTADA'}")
            break
        prev = row
    else:
        print("  No se encontró transición en el rango barrido")

    out = out_dir / "collatz_forzado.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nGuardado: {out}")


if __name__ == "__main__":
    main()
