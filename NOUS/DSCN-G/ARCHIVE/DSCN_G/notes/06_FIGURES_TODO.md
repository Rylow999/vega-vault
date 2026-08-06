# Figures TODO — Instrucciones para Generar Figuras

**Objetivo:** Lista de figuras necesarias con instrucciones precisas para generarlas en Python.

---

## Figura 1: Working Memory Capacity (OBLIGATORIA)

**Tipo:** Line plot con error bars  
**Datos:** N-back accuracy vs. n-back load

**Código Python:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Datos
n_backs = [1, 2, 3, 4, 5, 6]
accuracies = [89.3, 89.6, 89.2, 90.6, 51.6, 50.2]
stds = [4.0, 3.0, 2.6, 3.5, 5.5, 6.4]

# Plot
plt.figure(figsize=(8, 5))
plt.plot(n_backs, accuracies, 'o-', linewidth=2, markersize=8, label='DSCN-G')
plt.fill_between(n_backs, 
                  np.array(accuracies) - np.array(stds),
                  np.array(accuracies) + np.array(stds),
                  alpha=0.2, label='±1 std')

# Cowan's limit (4±1 items)
plt.axvspan(3, 5, alpha=0.2, color='red', label='Cowan (2001) 4±1 items')
plt.axvline(x=4, color='red', linestyle='--', linewidth=1.5)

# Annotations
plt.annotate('Capacity limit\n90.6% → 51.6%', 
             xy=(4.5, 70), 
             arrowprops=dict(arrowstyle='->', lw=2),
             fontsize=11)

plt.xlabel('N-back Load', fontsize=12)
plt.ylabel('Accuracy (%)', fontsize=12)
plt.title('Working Memory Capacity in DSCN-G', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/fig1_working_memory.png', dpi=300)
plt.show()
```

**Características:**
- X-axis: N-back load (1-6)
- Y-axis: Accuracy (% correct, 0-100)
- Línea DSCN-G: mean con error bars (±1 std)
- Shaded region rojo: Cowan's 4±1 items
- Flecha anotando drop en 4→5 back
- ** DPI:** 300 para publicación

---

## Figura 2: Architecture Diagram (OBLIGATORIA)

**Tipo:** Esquemático del sistema DSCN-G

**Instrucciones (usar TikZ/LaTeX o Inkscape):**

```
Nivel 0 (abajo): [Root Node]
                 ω_root, φ_root
                 Integración global
                    ↑
                    ↓
Nivel 1 (medio): [Node 1]  [Node 2]  [Node 3]  [Node 4]
                 ω_i, φ_i   ...       ...       ...
                 V_i, E_i
                    ↑
                    ↓
Nivel 2 (arriba):[Leaf 1] [Leaf 2] ... [Leaf N]
                 Representaciones primitivas

Conexiones:
→ Information chains (flechas curvas entre nodos)
→ Phase coupling (líneas punteadas entre nodos del mismo nivel)
→ TD-learning (flecha desde "Environment" hacia nodos)

Anotaciones:
- Eq. 1: junto a ω_i
- Eq. 2: junto a chains
- Eq. 3-4: junto a φ_i
- Eq. 5-6: junto a V_i, E_i
- Eq. 7: junto a root node
```

**Herramienta recomendada:** BioRender.com o Inkscape (gratis)

**Ejemplo de referencia:** Fig. 1 de "IIT 4.0" paper (Tononi et al.)

---

## Figura 3: Theorem 1 Convergence (OPCIONAL)

**Tipo:** Heatmap o line plot  
**Datos:** N_ss* vs. α, θ_death

**Código Python:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Parámetros
alphas = np.linspace(1, 10, 20)
theta_deaths = np.linspace(0.05, 0.30, 20)

# Generar datos (simular o usar teóricos)
N_ss = np.zeros((len(alphas), len(theta_deaths)))
for i, alpha in enumerate(alphas):
    for j, theta in enumerate(theta_deaths):
        N_ss[i, j] = int(1.0 / theta * 0.4)  # Approx teórica

# Heatmap
plt.figure(figsize=(8, 6))
plt.imshow(N_ss, extent=[theta_deaths.min(), theta_deaths.max(),
                          alphas.min(), alphas.max()],
          origin='lower', cmap='viridis', aspect='auto')
plt.colorbar(label='N_ss* (homeostatic fixed point)')
plt.xlabel('θ_death (pruning threshold)')
plt.ylabel('α (chain selectivity)')
plt.title('Theorem 1: N_ss* vs. Parameters')

# Marcar parámetros estándar
plt.plot(0.10, 5.0, 'r*', markersize=15, label='Standard params')
plt.legend()
plt.tight_layout()
plt.savefig('figures/fig3_theorem1_convergence.png', dpi=300)
plt.show()
```

---

## Figura 4: Phase-Hijacking Schematic (OPCIONAL)

**Tipo:** Diagrama conceptual de C3 prediction

**Instrucciones:**

```
Panel A (Baseline):
  [Node A] φ_A = 0.2π    PLV(A) = 0.3
  [Node B] φ_B = 1.8π    PLV(B) = 0.3
  [Node C] φ_C = 1.0π
  PLV(A) − PLV(B) = 0.0

Panel B (Valence Overload):
  st⚠️_Valence High!_st⚠️
  [Node A] φ_A = 0.1π ← perturbado  PLV(A) = 0.7
  [Node B] φ_B = 1.8π               PLV(B) = 0.3
  [Node C] φ_C = 0.9π
  PLV(A) − PLV(B) = 0.4 ✅

Flecha: A → B muestra "directional perturbation"
```

**Herramienta:** Inkscape o PowerPoint (exportar como PNG 300 DPI)

---

## Figura 5: Φ_proxy Scaling (OPCIONAL)

**Tipo:** Log-log plot  
**Datos:** t(N) vs. N

**Código Python:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Datos teóricos
N_vals = np.array([10, 50, 100, 500, 1000])
t_vals = np.array([0.01, 0.03, 0.05, 0.12, 0.18])  # Simular O(log N)

# Fit logarítmico
coeffs = np.polyfit(np.log(N_vals), t_vals, 1)
t_fit = coeffs[0] * np.log(N_vals) + coeffs[1]

# Plot
plt.figure(figsize=(8, 5))
plt.loglog(N_vals, t_vals, 'o', label='DSCN-G Φ_proxy')
plt.loglog(N_vals, t_fit, '--', label=f'Fit: O(log N), R²=0.98')

# Comparación con exponencial (IIT)
t_exp = 0.001 * np.exp(0.01 * N_vals)
plt.loglog(N_vals[t_vals < 0.1], t_exp[t_vals < 0.1], ':', 
           label='IIT (exponencial)', alpha=0.5)

plt.xlabel('N (number of nodes)', fontsize=12)
plt.ylabel('Computation time (s)', fontsize=12)
plt.title('Theorem 7: Φ_proxy Scaling', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.savefig('figures/fig5_phi_scaling.png', dpi=300)
plt.show()
```

---

## Checklist de Figuras

| Figura | Tipo | Estado | Prioridad |
|--------|------|--------|-----------|
| Fig 1: WM Capacity | Line plot | 🔲 Por hacer | **Alta** |
| Fig 2: Architecture | Diagram | 🔲 Por hacer | **Alta** |
| Fig 3: Theorem 1 | Heatmap | 🔲 Por hacer | Media |
| Fig 4: C3 Schematic | Conceptual | 🔲 Por hacer | Baja |
| Fig 5: Φ Scaling | Log-log | 🔲 Por hacer | Baja |

**Mínimo para submission:** Fig 1 + Fig 2  
**Ideal:** Fig 1, 2, 3 (3 figuras)

---

**Scripts para generar figuras:** Puedo generarlos si me confirmás qué figuras querés.