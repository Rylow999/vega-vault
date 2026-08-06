#!/usr/bin/env python3
"""
Analiza resultados de verificación y N-back
"""

import json
import numpy as np

def analyze_verification():
    """Analiza resultados de verificación de teoremas"""
    print("=" * 78)
    print("ANÁLISIS DE VERIFICACIÓN DE TEOREMAS")
    print("=" * 78)
    
    with open('verification_results_v3.json', 'r') as f:
        data = json.load(f)
    
    # Theorem 1
    t1 = data['theorem1']['results']
    print("\n📊 Theorem 1: Homeostatic Fixed Point")
    for r in t1:
        print(f"  N_init={r['N_init']:3d}: N_ss*={r['N_mean']:.1f}±{r['N_std']:.1f}  "
              f"ρ={r['rho_mean']:.4f}±{r['rho_std']:.4f}")
        print(f"    Universal bound: {'✓' if r['ub_ok'] else '✗'}")
        print(f"    Fixed point: {'✓' if r['fp_ok'] else '✗'}")
        print(f"    Maximality: {'✓' if r['max_ok'] else '✗'}")
    
    # Theorem 2
    t2 = data['theorem2']
    print(f"\n📊 Theorem 2: ω Alignment Convergence")
    print(f"  Final alignment = {t2['mean_alignment']:.4f} ± {t2['std_alignment']:.4f}")
    print(f"  Threshold (1−2β) = {t2['threshold']:.4f}")
    print(f"  Converged: {'✓' if t2['converged'] else '✗'}")
    
    # Theorem 3
    t3 = data['theorem3']
    print(f"\n📊 Theorem 3: Phase Consensus")
    print(f"  Consensus rate = {t3['fraction']:.3f} ({t3['consensus_count']}/{t3['seeds']})")
    
    # C3
    c3 = data['c3']
    print(f"\n📊 C3: Phase Hijacking")
    print(f"  Hijack triggers: {c3['hijack_triggers']} ({100*c3['hijack_rate']:.2f}% of steps)")
    print(f"  PLV-rises >0.3: {c3['plv_rises']} ({100*c3['rise_rate']:.1f}% of triggers)")
    if c3['mean_delta_plv'] is not None:
        # AUDIT FIX (2026-07-22): original line computed np.std() on
        # c3['min_delta_plv'], a single scalar (always 0 — not a real std).
        # verify_dscng_v3.py now emits std_delta_plv directly; use it, with a
        # safe fallback for older result files that predate the fix.
        std_plv = c3.get('std_delta_plv')
        if std_plv is None and c3.get('all_delta_plv'):
            std_plv = float(np.std(c3['all_delta_plv']))
        std_str = f"{std_plv:.3f}" if std_plv is not None else "N/A"
        print(f"  Mean ΔPLV: {c3['mean_delta_plv']:.3f} ± {std_str}")

def analyze_nback():
    """Analiza resultados de N-back"""
    print("\n" + "=" * 78)
    print("ANÁLISIS DE N-BACK (RECURSO CONTINUO)")
    print("=" * 78)
    
    with open('nback_v5_paper_ready.json', 'r') as f:
        data = json.load(f)
    
    print(f"\n📊 N_ss* empírico")
    print(f"  Mean: {data['N_ss_mean']:.2f} ± {data['N_ss_std']:.2f}")
    print(f"  Valores: {data['N_ss_estimates']}")
    
    print(f"\n📊 Curva de degradación")
    for r in data['n_back_results']:
        print(f"  {r['n_back']:2d}-back: bal.acc={r['bal_acc']*100:5.1f}%±{r['bal_acc_std']*100:4.1f}%   "
              f"d'={r['dprime']:5.2f}")
    
    # Análisis de degradación
    dprimes = [r['dprime'] for r in data['n_back_results']]
    n_backs = [r['n_back'] for r in data['n_back_results']]
    
    if len(dprimes) >= 2:
        decay_1_to_10 = dprimes[0] - dprimes[-1] if n_backs[-1] >= 10 else None
        print(f"\n📊 Patrón de degradación")
        print(f"  d'(1-back) = {dprimes[0]:.2f}")
        print(f"  d'({n_backs[-1]}-back) = {dprimes[-1]:.2f}")
        print(f"  Decaimiento total = {decay_1_to_10:.2f}" if decay_1_to_10 else "  Decaimiento: N/A")
        
        # Verificar si es suave (no escalón)
        max_drop = max([abs(dprimes[i] - dprimes[i+1]) for i in range(len(dprimes)-1)])
        avg_drop = np.mean([abs(dprimes[i] - dprimes[i+1]) for i in range(len(dprimes)-1)])
        
        print(f"  Max drop por step: {max_drop:.2f}")
        print(f"  Avg drop por step: {avg_drop:.2f}")
        if max_drop < 2.0:
            print(f"  ✓ Degradación SUAVE (no escalón abrupto)")
        else:
            print(f"  ⚠ Posible escalón detectado")

if __name__ == "__main__":
    analyze_verification()
    analyze_nback()
    print("\n" + "=" * 78)
    print("✓ Análisis completo")
    print("=" * 78)
