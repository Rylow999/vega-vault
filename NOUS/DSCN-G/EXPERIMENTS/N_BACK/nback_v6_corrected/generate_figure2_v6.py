#!/usr/bin/env python3
"""
Genera Figura 2 (v6) del paper: degradacion de d' vs n-back, con el N-back
occurrence-aware (nback_v6_occurrence_aware.py) — ver AUDIT_NOTES_ROUND3.md.
"""

import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open('nback_v6_paper_ready.json', 'r') as f:
    data = json.load(f)

n_backs = [r['n_back'] for r in data['n_back_results']]
bal_accs = [r['bal_acc'] * 100 for r in data['n_back_results']]
bal_acc_stds = [r['bal_acc_std'] * 100 for r in data['n_back_results']]
dprimes = [r['dprime'] for r in data['n_back_results']]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.errorbar(n_backs, bal_accs, yerr=bal_acc_stds, fmt='o-', linewidth=2,
             markersize=8, capsize=5, color='#2E86AB', label='DSCN-G v3 (v6, occurrence-aware)')
ax1.axhline(y=50, color='gray', linestyle='--', linewidth=1, label='Chance (50%)')
ax1.set_xlabel('n-back (carga de memoria)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Balanced Accuracy (%)', fontsize=12, fontweight='bold')
ax1.set_title('Degradación de la Precisión con la Carga', fontsize=13, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 21)
ax1.set_ylim(40, 105)

ax2.plot(n_backs, dprimes, 'o-', linewidth=2, markersize=8,
         color='#A23B72', label='DSCN-G v3 (v6, occurrence-aware)')
ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, label='d\' = 0 (sin sensibilidad)')
ax2.set_xlabel('n-back (carga de memoria)', fontsize=12, fontweight='bold')
ax2.set_ylabel('d\' (sensibilidad)', fontsize=12, fontweight='bold')
ax2.set_title('Degradación de la Sensibilidad (d\')', fontsize=13, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 21)
ax2.set_ylim(0, 7)

# Anotación: la caída real ahora ocurre entre 2 y 5-back, con piso desde ~6-back
ax2.annotate('Caída pronunciada 2→5-back,\nluego piso (~0.8–1.0)\nno cae a 0',
             xy=(6, dprimes[5]), xytext=(11, 4.5),
             fontsize=10, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('figure2_nback_v6_paper.png', dpi=300, bbox_inches='tight')
print('✓ Figura 2 (v6) generada: figure2_nback_v6_paper.png')
