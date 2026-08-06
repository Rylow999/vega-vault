#!/usr/bin/env python3
"""
DSCN-G — N-back v6: occurrence-aware (fix del hallazgo de AUDIT_NOTES_ROUND2.md Sec.2)

QUE CAMBIA RESPECTO DE v5 (nback_v5_grounded.py) Y POR QUE
============================================================

v5 evaluaba si la identidad `target` (el estimulo de hace n_back pasos)
estaba "viva" DESPUES de escribir el estimulo actual `s` en el sustrato.
En un trial *match*, por definicion `s == target`. Como la escritura del
paso actual ocurre ANTES del chequeo, un trial match se "auto-satisface":
el chequeo encuentra la traza recien escrita EN ESTE MISMO PASO, no una
traza que sobrevivio desde hace n_back pasos. Esto no es un efecto
probabilistico -- es una garantia estructural. Confirmado empiricamente:
con el orden de v5, `match_alive_frac = 1.0000 exacto` para CUALQUIER
n_back probado (1 a 80) y CUALQUIER n_stimuli probado (10, 30, 100) --
aumentar el alfabeto de estimulos (opcion 3) no lo cambia en absoluto,
porque el problema no es de colision estadistica entre identidades, es de
orden de las operaciones.

FIX (v6, este archivo):
  1. [Necesario] Se invierte el orden: el chequeo de match/no-match para
     el paso t se evalua usando el estado del sustrato tal como quedo
     DESPUES del paso t-1 (es decir, antes de escribir el estimulo
     presentado en t). Recien despues de evaluar, se escribe `s=seq[t]`
     para que quede disponible para pasos futuros. Esto elimina la
     auto-satisfaccion: en un trial match, la pregunta pasa a ser
     genuinamente "¿sigue viva la traza de una presentacion ANTERIOR de
     este estimulo?", no "¿acabo de escribir yo mismo esta identidad?".
  2. [Complementario, opcion 3] `n_stimuli` sube de 10 a 50 (configurable).
     Con un alfabeto de solo 10 identidades reciclandose en 300 pasos, aun
     con el fix (1), una identidad puede seguir "viva" por PURA
     COINCIDENCIA de que otra presentacion no relacionada del mismo
     estimulo ocurrio recientemente en otro punto de la secuencia (no
     necesariamente en t-n_back). Un alfabeto mas grande reduce la tasa de
     estas coincidencias y acerca el chequeo por-identidad a un chequeo
     por-ocurrencia genuino. Verificado empiricamente: con el fix (1)
     solo, n_stimuli=10 todavia deja un piso de FA notable en n_back
     grande; n_stimuli=50-100 lo reduce sustancialmente. n_stimuli=50 se
     eligio como punto medio razonable (ver AUDIT_NOTES_ROUND3.md para la
     tabla comparativa 10/30/100).

Lo que NO cambia respecto de v5: la formula de vitalidad (Eq. 5), la
regla de decision (similitud coseno, mismo criterio para todo n_back), el
sustrato reutilizable sin pruning permanente, measure_N_ss() (no depende
de esto -- ver nota en el codigo).
"""

import numpy as np
from scipy.stats import norm
from typing import Tuple


def _generate_balanced_sequence(seq_len, n_back, n_stimuli, p_match, rng):
    seq = list(rng.integers(0, n_stimuli, n_back))
    is_match_trial = [None] * n_back
    for t in range(n_back, seq_len):
        if rng.random() < p_match:
            seq.append(seq[t - n_back])
            is_match_trial.append(True)
        else:
            choices = [x for x in range(n_stimuli) if x != seq[t - n_back]]
            seq.append(rng.choice(choices))
            is_match_trial.append(False)
    return np.array(seq), is_match_trial


def measure_N_ss(seed, gamma, theta_death, N, k_write, n_stimuli=10, warmup=500):
    """Sin cambios respecto de v5: esta funcion mide el tamaño de
    poblacion en regimen estacionario bajo escritura competitiva continua
    (Eq. 5), y no depende de que el estimulo escrito sea `s` o cualquier
    otro valor -- la variable `s` que dibuja aqui nunca se usa para nada
    mas que consumir el rng de forma determinista. No tiene el problema de
    Sec.2 porque no compara identidades entre si; solo cuenta nodos vivos."""
    rng = np.random.default_rng(seed)
    vitality = np.zeros(N)
    for _ in range(warmup):
        s = rng.integers(0, n_stimuli)
        p = np.exp(-vitality * 5.0)
        p /= p.sum()
        write_idx = rng.choice(N, size=k_write, replace=False, p=p)
        activity = np.zeros(N)
        activity[write_idx] = 1.0
        decay = np.exp(-gamma)
        vitality = vitality * decay + activity * (1 - decay)
    return int(np.sum(vitality >= theta_death))


def run_trial(n_back: int, gamma: float, theta_death: float, N: int, k_write: int, d: int,
              seq_len: int = 300, seed: int = 0, n_stimuli: int = 50,
              match_criterion: float = 0.85, p_match: float = 0.5) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)

    stim_rng = np.random.default_rng(1234)
    stim_vectors = stim_rng.normal(0, 1, (n_stimuli, d))
    stim_vectors /= np.linalg.norm(stim_vectors, axis=1, keepdims=True)

    omega = rng.normal(0, 0.1, (N, d))
    vitality = np.zeros(N)
    tag = np.full(N, -1)

    seq, is_match_trial = _generate_balanced_sequence(seq_len, n_back, n_stimuli, p_match, rng)

    hits = fas = misses = crs = 0
    decay = np.exp(-gamma)

    for t in range(seq_len):
        s = seq[t]

        # ── 1. EVALUAR PRIMERO, usando el estado heredado de t-1 ──────
        # (fix v6: antes de escribir el estimulo actual, para que un
        # trial match no pueda auto-satisfacerse con su propia escritura)
        if t >= n_back:
            target = seq[t - n_back]
            is_match = is_match_trial[t]

            alive = np.where((tag == target) & (vitality >= theta_death))[0]
            query_vec = stim_vectors[s]

            if len(alive) > 0:
                stored_vec = np.mean(omega[alive], axis=0)
                stored_vec /= (np.linalg.norm(stored_vec) + 1e-8)
            else:
                probe_idx = rng.integers(0, N)
                stored_vec = omega[probe_idx].copy()
                stored_vec /= (np.linalg.norm(stored_vec) + 1e-8)

            sim_score = np.dot(query_vec, stored_vec)
            response = sim_score > match_criterion

            if is_match and response: hits += 1
            elif is_match and not response: misses += 1
            elif (not is_match) and response: fas += 1
            else: crs += 1

        # ── 2. ESCRIBIR el estimulo actual (queda disponible para el futuro) ──
        p = np.exp(-vitality * 5.0)
        p /= p.sum()
        write_idx = rng.choice(N, size=k_write, replace=False, p=p)
        tag[write_idx] = s
        omega[write_idx] = stim_vectors[s] + rng.normal(0, 0.05, d)

        activity = np.zeros(N)
        activity[write_idx] = 1.0
        vitality = vitality * decay + activity * (1.0 - decay)  # Eq. 5

        dead = vitality < theta_death
        tag[dead] = -1

    n_match = hits + misses
    n_nonmatch = fas + crs
    hit_rate = hits / n_match if n_match else np.nan
    fa_rate = fas / n_nonmatch if n_nonmatch else np.nan
    bal_acc = 0.5 * (hit_rate + (1 - fa_rate))

    def z(p, n):
        p = min(max(p, 1.0 / (2 * n)), 1 - 1.0 / (2 * n))
        return norm.ppf(p)

    dprime = z(hit_rate, n_match) - z(fa_rate, n_nonmatch)
    return bal_acc, dprime


def sweep(gamma, theta_death, N, k_write, d=8, n_stimuli=50,
          n_backs=(1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20), n_trials=40, seq_len=300):
    N_ss_estimates = [measure_N_ss(seed=s, gamma=gamma, theta_death=theta_death, N=N, k_write=k_write)
                       for s in range(10)]
    print(f"N_ss* empirico (10 seeds, reproducible): {np.mean(N_ss_estimates):.2f} ± {np.std(N_ss_estimates):.2f}  "
          f"valores: {N_ss_estimates}")

    rows = []
    for n in n_backs:
        results = [run_trial(n, gamma, theta_death, N=N, k_write=k_write, d=d, n_stimuli=n_stimuli,
                             seed=s, seq_len=seq_len)
                   for s in range(n_trials)]
        bal = np.mean([r[0] for r in results]); bal_sd = np.std([r[0] for r in results])
        dp = np.nanmean([r[1] for r in results])
        rows.append((n, bal, bal_sd, dp))
        print(f"  {n:2d}-back: bal.acc={bal*100:5.1f}%±{bal_sd*100:4.1f}%   d'={dp:5.2f}")

    return rows, N_ss_estimates


if __name__ == "__main__":
    import json
    import argparse

    ap = argparse.ArgumentParser(description="Occurrence-aware N-back sweep (v6)")
    ap.add_argument("--n-backs", type=int, nargs="+",
                     default=[1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20],
                     help="n-back values to sweep")
    ap.add_argument("--n-trials", type=int, default=40)
    ap.add_argument("--n-stimuli", type=int, default=50,
                     help="tamaño del alfabeto de estimulos (v5 usaba 10; ver docstring)")
    ap.add_argument("--out", type=str, default="nback_v6_paper_ready.json")
    args = ap.parse_args()

    print("Occurrence-aware N-back (v6) — fix de orden + alfabeto ampliado")
    print(f"n_stimuli={args.n_stimuli}")
    print("=" * 78)

    gamma, theta_death, N, k_write, d = 0.20, 0.15, 100, 5, 8
    rows, N_ss_estimates = sweep(gamma=gamma, theta_death=theta_death, N=N, k_write=k_write, d=d,
                                  n_stimuli=args.n_stimuli,
                                  n_backs=tuple(args.n_backs), n_trials=args.n_trials)

    out = dict(
        params=dict(gamma=gamma, theta_death=theta_death, N=N, k_write=k_write, d=d,
                    n_stimuli=args.n_stimuli, n_trials=args.n_trials),
        N_ss_mean=float(np.mean(N_ss_estimates)),
        N_ss_std=float(np.std(N_ss_estimates)),
        N_ss_estimates=[int(x) for x in N_ss_estimates],
        n_back_results=[
            dict(n_back=int(n), bal_acc=float(bal), bal_acc_std=float(bal_sd), dprime=float(dp))
            for (n, bal, bal_sd, dp) in rows
        ],
    )
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n→  {args.out}")
