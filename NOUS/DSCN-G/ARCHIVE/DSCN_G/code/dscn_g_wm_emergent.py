#!/usr/bin/env python3
"""DSCN-G Working Memory — modelo de capacidad EMERGENTE (v2, corregido)

Diferencias respecto de la version anterior (dscn_g_simulator_wm.py):

1. SIN tope explicito de items. No existe ninguna linea del tipo
   `if len(items) > k: items = items[:k]`. La capacidad no es un parametro
   declarado; es una consecuencia medible de la competencia por recursos.

2. SIN rama condicionada a n_back. La version anterior tenia:
       if n_back > len(self.working_memory): return random()
   lo cual garantizaba nivel de azar para todo n_back > capacidad POR
   CONSTRUCCION, sin importar la dinamica. Aca la MISMA regla de decision
   (comparacion de fase contra un criterio fijo) se aplica identica para
   cualquier n_back; si la traza fue sobrescrita, se compara igual contra
   lo que efectivamente hay en ese nodo (ruido u otro item), y el
   desempeno a nivel de azar (si aparece) emerge solo.

3. Mecanismo: cada nodo tiene una vitalidad V_i que decae exponencialmente
   (misma Eq. 5 del modelo base: V_i(t+1) = V_i(t)*e^-gamma + A_i(t)*(1-e^-gamma)).
   Un item nuevo se escribe preferentemente sobre los nodos de MENOR
   vitalidad actual (softmax inverso, no un argmin determinista), es decir,
   compite por el mismo sustrato finito que los items anteriores. Nodos por
   debajo de theta_death pierden la identidad que representaban (olvido real).

4. Metrica: como P(match) = 1/n_stimuli en una secuencia iid, "responder
   siempre no-match" ya da ~90% de accuracy cruda sin memoria real. Para
   evitar ese artefacto, generamos ~50% de trials de match (diseno estandar
   de N-back) y reportamos accuracy balanceada y d' (sensibilidad de teoria
   de deteccion de senales), que no estan inflados por el desbalance de clases.

Resultado honesto (ver bloque __main__): la degradacion con n_back es GRADUAL,
no un colapso abrupto a nivel de azar en un punto preciso. Esto es consistente
con modelos de "recurso continuo" de memoria de trabajo (p.ej. Bays & Husain,
2008) mas que con un modelo de "slots discretos" con limite duro tipo Cowan
(2001) 4±1. Esto es una diferencia real e importante respecto de lo que
afirmaba la version anterior del paper, y se documenta como tal.
"""
import numpy as np
from scipy.stats import norm
from typing import Tuple


def _generate_balanced_sequence(seq_len: int, n_back: int, n_stimuli: int,
                                 p_match: float, rng: np.random.Generator):
    """Secuencia con ~p_match de trials de match, para evitar el confound
    de clase desbalanceada (ver punto 4 arriba)."""
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


def run_trial(n_back: int, gamma: float, theta_death: float, N: int, k_write: int,
              seq_len: int = 300, seed: int = 0, n_stimuli: int = 10,
              match_criterion: float = 0.85, p_match: float = 0.5) -> Tuple[float, float, int]:
    """Corre un trial de N-back con el modelo de capacidad emergente.

    match_criterion es un criterio de decision FIJO (no se ajusta por n_back;
    es el mismo umbral de similitud de fase para todas las condiciones).

    Returns: (balanced_accuracy, d_prime, mean_live_nodes)
    """
    rng = np.random.default_rng(seed)
    vitality = np.zeros(N)
    tag = np.full(N, -1)
    phase = rng.uniform(0, 2 * np.pi, N)

    seq, is_match_trial = _generate_balanced_sequence(seq_len, n_back, n_stimuli, p_match, rng)

    hits = fas = misses = crs = 0
    live_counts = []

    for t in range(seq_len):
        s = seq[t]

        # Escritura: competencia por vitalidad, no un buffer de tamano fijo.
        p = np.exp(-vitality * 5.0)
        p /= p.sum()
        write_idx = rng.choice(N, size=k_write, replace=False, p=p)
        tag[write_idx] = s
        phase[write_idx] = s * (2 * np.pi / n_stimuli) + rng.normal(0, 0.05, k_write)

        # Decay + refuerzo (Eq. 5 del modelo base)
        activity = np.zeros(N)
        activity[write_idx] = 1.0
        decay = np.exp(-gamma)
        vitality = vitality * decay + activity * (1 - decay)

        # Pruning real: se pierde la identidad, no solo se "olvida" nominalmente
        dead = vitality < theta_death
        tag[dead] = -1

        live_counts.append(int(np.sum(vitality >= theta_death)))

        if t >= n_back:
            target = seq[t - n_back]
            is_match = is_match_trial[t]

            alive = np.where((tag == target) & (vitality >= theta_death))[0]
            query_phase = s * (2 * np.pi / n_stimuli)
            if len(alive) > 0:
                stored_phase = np.mean(phase[alive])
            else:
                # No hay traza viva: se compara igual, contra fase no informativa.
                stored_phase = rng.uniform(0, 2 * np.pi)

            sim = np.cos(query_phase - stored_phase)
            response = sim > match_criterion  # MISMA regla para todo n_back

            if is_match and response:
                hits += 1
            elif is_match and not response:
                misses += 1
            elif (not is_match) and response:
                fas += 1
            else:
                crs += 1

    n_match = hits + misses
    n_nonmatch = fas + crs
    hit_rate = hits / n_match if n_match else np.nan
    fa_rate = fas / n_nonmatch if n_nonmatch else np.nan
    bal_acc = 0.5 * (hit_rate + (1 - fa_rate))

    def z(p):
        p = min(max(p, 1.0 / (2 * n_match)), 1 - 1.0 / (2 * n_match))  # correccion log-linear
        return norm.ppf(p)

    dprime = z(hit_rate) - z(fa_rate)
    return bal_acc, dprime, int(np.mean(live_counts))


def sweep(gamma: float, theta_death: float, N: int, k_write: int,
          n_backs=(1, 2, 3, 4, 5, 6, 8, 10), n_trials: int = 40, seq_len: int = 300):
    rows = []
    for n in n_backs:
        results = [run_trial(n, gamma, theta_death, N=N, k_write=k_write,
                              seed=s, seq_len=seq_len) for s in range(n_trials)]
        bal = np.mean([r[0] for r in results])
        bal_sd = np.std([r[0] for r in results])
        dp = np.nanmean([r[1] for r in results])
        live = np.mean([r[2] for r in results])
        rows.append((n, bal, bal_sd, dp, live))
    return rows


if __name__ == "__main__":
    GAMMA, THETA_DEATH, N, K_WRITE = 0.20, 0.15, 100, 5

    print("=" * 68)
    print("DSCN-G Working Memory — capacidad emergente (sin cap, sin fallback)")
    print(f"N={N}  k_write={K_WRITE}  gamma={GAMMA}  theta_death={THETA_DEATH}")
    print("=" * 68)
    print(f"{'n-back':<8}{'bal.acc':<12}{'d-prime':<10}{'nodos vivos (avg)':<20}")
    print("-" * 68)

    rows = sweep(GAMMA, THETA_DEATH, N, K_WRITE)
    for n, bal, bal_sd, dp, live in rows:
        print(f"{n:<8}{bal*100:5.1f}% ± {bal_sd*100:3.1f}%   {dp:<10.2f}{live:<20}")

    print("\nNota: la degradacion es gradual (no colapsa a d'~0 / azar en un\n"
          "punto preciso dentro del rango medido). Esto NO reproduce un limite\n"
          "discreto tipo Cowan 4±1; es mas consistente con un modelo de recurso\n"
          "continuo. Se documenta como tal en el paper — no se fuerza la forma\n"
          "del resultado.")
