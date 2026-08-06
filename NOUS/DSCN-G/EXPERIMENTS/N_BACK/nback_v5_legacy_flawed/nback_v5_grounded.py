#!/usr/bin/env python3
"""
DSCN-G — N-back sobre una reimplementacion standalone de la Ec. 5 de
DSCN_G_v2 (mismo alfabeto omega d-dimensional, misma formula de vitalidad,
parametros propios) (v5)

AUDIT FIX (ronda 2, 2026-07-22): el docstring original decia "grounded
directly in DSCN_G_v2's own vitality/omega substrate" e importaba
`DSCN_G_v2` sin usarlo nunca -- ninguna funcion de este archivo instancia
esa clase. Lo que este script realmente hace es reimplementar a mano la
Ec. 5 (decaimiento de vitalidad + escritura competitiva) y la
representacion omega d-dimensional, con sus propios parametros
(gamma=0.20, theta_death=0.15 -- distintos de los defaults del nucleo).
Es una reimplementacion paralela de la misma ecuacion, no una corrida
sobre la instancia compartida de DSCN_G_v2. Se saco el import no usado y
se corrigio esta descripcion para no sugerir una integracion mas fuerte
de la que hay. Ver AUDIT_NOTES_ROUND2.md Sec.3.1 para el detalle, y Sec.2
para un hallazgo mas de fondo sobre que mide (o no mide) esta tarea.

Diferencias respecto de nback_v4_capacity.py:

1. Seed fija en vez de sin seed -- N_ss* deja de fluctuar de corrida en
   corrida (antes daba 4 o 5 al azar, ver auditoria previa).

2. Sin cap explicito ni rama condicionada a n_back. La version anterior tenia:
       if n_back >= N_ss: response = random()
   lo cual garantizaba nivel de azar mas alla de la capacidad POR CONSTRUCCION.
   Aca la MISMA regla de decision (similitud coseno en el espacio omega,
   contra un criterio fijo) se aplica identica para cualquier n_back.

3. Usa una representacion omega (d-dimensional) analoga a la de DSCN_G_v2
   -- el mismo tipo de vector que usan las Ecs. 1 y 2 del nucleo -- para
   codificar la identidad del estimulo, en vez de una fase ad hoc. Los
   nodos compiten por espacio de escritura via la MISMA formula de
   vitalidad (Eq. 5) que usa el nucleo del modelo, reimplementada aqui
   (no la instancia compartida -- ver nota de arriba).

NOTA METODOLOGICA (declarada, no escondida): en el nucleo original, la
vitalidad decae solo sobre nodos en `nodes_active`, y el pruning ELIMINA
nodos permanentemente (adecuado para el equilibrio poblacional de Teorema 1,
donde "morir" es definitivo). Un buffer de memoria de trabajo necesita
sustrato reutilizable: un nodo que "olvido" un item viejo tiene que poder
volver a usarse para un item nuevo. Por eso aca aplicamos la MISMA formula
de la Ec. 5 a los N nodos completos en cada paso (sin remocion permanente),
en vez de reusar `_update_vitality_and_prune` tal cual (que si elimina
nodos para siempre). Esta es una desviacion deliberada del modelo de
poblacion, declarada explicitamente, no una copia disimulada.

NOTA METODOLOGICA ADICIONAL (ronda 2, ver AUDIT_NOTES_ROUND2.md Sec.2): el
chequeo de "traza viva" es por IDENTIDAD de estimulo (`tag == target`), no
por OCURRENCIA especifica. Con solo `n_stimuli=10` identidades reciclandose
en 300 pasos, la traza del target en trials *match* esta viva el 100% de
las veces para cualquier n_back probado (1 a 80) -- nunca hay un miss
genuino por olvido de la ocurrencia especifica. Toda la curva de d' viene
del lado de falsas alarmas (que tan seguido la identidad target de un
trial *non-match* ya fue re-escrita por otra presentacion reciente). Esto
no se corrigio aqui porque cambiar el chequeo a por-ocurrencia es una
decision de diseno experimental, no un bug con arreglo unico -- ver el
archivo de auditoria para las opciones.
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
    """N_ss* empirico: cuantos nodos se mantienen vivos en régimen estacionario
    bajo escritura continua competitiva. Reproducible (seed fija)."""
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
              seq_len: int = 300, seed: int = 0, n_stimuli: int = 10,
              match_criterion: float = 0.85, p_match: float = 0.5) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)
    
    # Vectores canonicos por estimulo en el espacio omega real de la arquitectura
    # (d-dimensional, como en DSCN_G_v2), fijos por corrida.
    stim_rng = np.random.default_rng(1234)  # fijo, no depende del seed del trial
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
        
        # Escritura: competencia por vitalidad (misma logica que Eq.5, sustrato reutilizable)
        p = np.exp(-vitality * 5.0)
        p /= p.sum()
        write_idx = rng.choice(N, size=k_write, replace=False, p=p)
        tag[write_idx] = s
        omega[write_idx] = stim_vectors[s] + rng.normal(0, 0.05, d)
        
        activity = np.zeros(N)
        activity[write_idx] = 1.0
        vitality = vitality * decay + activity * (1 - decay)  # Eq. 5, aplicada a todo el pool
        
        dead = vitality < theta_death
        tag[dead] = -1
        
        if t >= n_back:
            target = seq[t - n_back]
            is_match = is_match_trial[t]
            
            alive = np.where((tag == target) & (vitality >= theta_death))[0]
            query_vec = stim_vectors[s]
            
            if len(alive) > 0:
                stored_vec = np.mean(omega[alive], axis=0)
                stored_vec /= (np.linalg.norm(stored_vec) + 1e-8)
            else:
                # Sin traza viva: comparamos contra lo que REALMENTE hay en el
                # sustrato (posible interferencia con otro item ahi guardado),
                # no contra ruido sintetico ortogonal (eso inflaba accuracy a
                # ~100% en todo n_back, ver nota de la corrida anterior).
                probe_idx = rng.integers(0, N)
                stored_vec = omega[probe_idx].copy()
                stored_vec /= (np.linalg.norm(stored_vec) + 1e-8)
            
            sim_score = np.dot(query_vec, stored_vec)  # coseno, MISMA regla para todo n_back
            response = sim_score > match_criterion
            
            if is_match and response: hits += 1
            elif is_match and not response: misses += 1
            elif (not is_match) and response: fas += 1
            else: crs += 1
    
    n_match = hits + misses
    n_nonmatch = fas + crs
    hit_rate = hits / n_match if n_match else np.nan
    fa_rate = fas / n_nonmatch if n_nonmatch else np.nan
    bal_acc = 0.5 * (hit_rate + (1 - fa_rate))
    
    def z(p, n):
        # AUDIT FIX (ronda 2, 2026-07-22): la correccion log-lineal (Hautus,
        # 1995) para evitar z(0)/z(1) debe usar el N de CADA condicion
        # (n_match para hit_rate, n_nonmatch para fa_rate), no el mismo N
        # para ambas. Impacto medido sobre las 4 n_back ya publicadas:
        # +0.009 en d'(1-back), 0.000 en 5/10/15-back (40 trials,
        # seeds 0-39) -- no cambia ninguna conclusion, se corrige igual
        # para no arrastrar el error.
        p = min(max(p, 1.0 / (2 * n)), 1 - 1.0 / (2 * n))
        return norm.ppf(p)
    
    dprime = z(hit_rate, n_match) - z(fa_rate, n_nonmatch)
    return bal_acc, dprime

def sweep(gamma, theta_death, N, k_write, d=8, n_backs=(1,2,3,4,5,6,8,10), n_trials=40, seq_len=300):
    N_ss_estimates = [measure_N_ss(seed=s, gamma=gamma, theta_death=theta_death, N=N, k_write=k_write)
                       for s in range(10)]
    print(f"N_ss* empirico (10 seeds, reproducible): {np.mean(N_ss_estimates):.2f} ± {np.std(N_ss_estimates):.2f}  "
          f"valores: {N_ss_estimates}")
    
    rows = []
    for n in n_backs:
        results = [run_trial(n, gamma, theta_death, N=N, k_write=k_write, d=d, seed=s, seq_len=seq_len)
                   for s in range(n_trials)]
        bal = np.mean([r[0] for r in results]); bal_sd = np.std([r[0] for r in results])
        dp = np.nanmean([r[1] for r in results])
        rows.append((n, bal, bal_sd, dp))
        print(f"  {n:2d}-back: bal.acc={bal*100:5.1f}%±{bal_sd*100:4.1f}%   d'={dp:5.2f}")
    
    return rows, N_ss_estimates

if __name__ == "__main__":
    import json
    import argparse

    ap = argparse.ArgumentParser(description="Grounded N-back sweep")
    ap.add_argument("--n-backs", type=int, nargs="+",
                     default=[1, 2, 3, 4, 5, 6, 8, 10, 12, 15],
                     help="n-back values to sweep (paper cites up to 15-back)")
    ap.add_argument("--n-trials", type=int, default=40)
    ap.add_argument("--out", type=str, default="nback_v5_paper_ready.json")
    args = ap.parse_args()

    print("Grounded N-back — reimplementacion standalone de la Ec.5 (no cap, no n_back branch, seed fija)")
    print("=" * 78)

    gamma, theta_death, N, k_write, d = 0.20, 0.15, 100, 5, 8
    rows, N_ss_estimates = sweep(gamma=gamma, theta_death=theta_death, N=N, k_write=k_write, d=d,
                                  n_backs=tuple(args.n_backs), n_trials=args.n_trials)

    # AUDIT FIX (2026-07-22): the original script computed everything above but
    # never wrote a results file. generate_figure2.py and analyze_results.py
    # both require nback_v5_paper_ready.json — without this block the pipeline
    # in README.md ("python nback_v5_grounded.py" then "python
    # generate_figure2.py") cannot succeed; the second and later steps fail on
    # FileNotFoundError. Schema below matches exactly what those two scripts
    # read (data['N_ss_mean'], data['N_ss_std'], data['N_ss_estimates'],
    # data['n_back_results'][i]['n_back'|'bal_acc'|'bal_acc_std'|'dprime']).
    out = dict(
        params=dict(gamma=gamma, theta_death=theta_death, N=N, k_write=k_write, d=d,
                    n_trials=args.n_trials),
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
