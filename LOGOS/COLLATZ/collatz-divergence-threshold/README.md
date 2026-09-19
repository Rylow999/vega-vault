# The Divergence Threshold of the Collatz Map

**A Conditional Closed-Form Necessary Condition**

> **Author:** Luciano Benjamín Nieto  
> **Date:** July 25, 2026  
> **Status:** Research paper — rigorous results and open conjectures

---

## Abstract

We derive an exact closed-form candidate threshold for divergence in the accelerated
Collatz map $R_3(n) = (3n+1)/2^{\nu_2(3n+1)}$, and prove it as a necessary condition
*conditional on* an explicit Local Equidistribution Hypothesis (LEH — see the paper).
Defining $f_P$ as the empirical frequency of visits to the class $P = \{n \equiv 3 \pmod{4}\}$,
we show that, under LEH, any orbit diverging sub-exponentially must satisfy
$f_P \geq f_P^* = \log_4(8/3) = (3 - \log_2 3)/2 \approx 0.7075$.
The threshold value itself rests on the exact, unconditional identity $\mu_P + \mu_N = -2$;
LEH is the unproven ingredient needed to promote that ensemble-level identity to a
per-orbit necessary condition.

## Repository Structure

```
.
├── README.md                          # This file
├── paper/
│   └── collatz_divergence_threshold.tex   # Main LaTeX source
├── code/
│   └── collatz_simulation.py          # Python simulation script
├── data/
│   ├── collatz_orbits_50000.csv       # Raw simulation data (25,000 orbits)
│   └── collatz_simulation_summary.txt # Statistical summary
└── .gitignore
```

## Key Results

| Result | Status |
|--------|--------|
| $\Phi(a) = \log_2 a - 2$ (exact 2-adic drift) | **Proven** |
| $\mathbb{E}[\Delta V_{4/3}] = -1$ (natural metric drift) | **Proven** |
| $a=3$ unique contractive odd parameter (among $R_a$, odd $a>1$) | **Proven** |
| Fibonacci convergents of $\log_2 3$ | **Proven** |
| $f_P^* = \log_4(8/3)$ exact divergence threshold | **Proven, conditional on LEH** |
| $\mu_P + \mu_N = -2$ (unifying identity) | **Proven** |
| $f_P \to 0.5$ for every orbit (Universal Map Balance) | **Conjecture** |
| $\Sigma_{\text{div}} = \emptyset$ via Baire | **Conjecture** |

## Simulation Results

- **25,000 orbits** analyzed (odd $n \leq 50{,}000$), **0 truncated** by the $100{,}000$-step cap — every $f_P$ value is a true, full-orbit value
- **Maximum $f_P$ observed:** $0.\overline{6}$ (at $n = 151$ and $n = 1431$)
- **Empirical separation from the conditional divergence threshold:** $5.8\%$
- **Orbits exceeding $f_P^*$:** $0$ ($0\%$)
- **Lag-1 autocorrelation of P/N steps:** $\approx -0.005$ (near-zero)

## Limitations

This repository does not prove the Collatz conjecture. The main theorem
($f_P \geq f_P^*$ as a necessary condition for divergence) is proven
*conditional on* the Local Equidistribution Hypothesis (LEH), which is stated
explicitly in the paper and remains open. Closing that gap is at least as hard
as the Collatz conjecture itself. The empirical results (25,000 orbits, none
approaching the threshold) are corroborating evidence, not a proof, and do not
bear on LEH.

## Compilation

```bash
cd paper
pdflatex collatz_divergence_threshold.tex
bibtex collatz_divergence_threshold  # if using BibTeX
pdflatex collatz_divergence_threshold.tex
pdflatex collatz_divergence_threshold.tex
```

## Running the Simulation

```bash
cd code
python collatz_simulation.py
```

Requires: Python 3.8+, NumPy

## License

MIT License — See LICENSE file for details.

## Citation

```bibtex
@article{nieto2026collatz,
  title={The Divergence Threshold of the Collatz Map: A Conditional Closed-Form Necessary Condition},
  author={Nieto, Luciano Benjam\'{i}n},
  year={2026},
  note={Preprint}
}
```

---

*Per Aspera, Ad Astra.*

---

## 2026-09-18 — La convergencia como invariante entre observadores (RHO_LAW)

Experimento en `NOUS/RHO_LAW/experiments/exp_collatz_multi_observer.py`
(161 órbitas: impares hasta 100k + campeones):

| Observador | Umbral | Resultado |
|---|---|---|
| O1: f_P | 0.7075 | **0 cruces** (máx 0.369) |
| O2: drift 2-adico | 0 | **0 positivos** (máx -5.02) |
| O3: ratio N/P | 3.0 | **redundante con O1** — las 3 órbitas con ratio≥3 convergen (f_P≈0.23, drift -14 a -17) |
| S4: resonator HRR sobre la secuencia | — | **nivel azar** (0.15-0.28) |

**Hallazgos:**

1. **Los observadores independientes (O1, O2) coinciden 161/161**: la
   convergencia es invariante entre espacios (enteros, log₂, 2-adico) y
   observadores. Es propiedad del **sustrato** (drift<0), no de cómo se mira.

2. **El ratio N/P ≥ 3 NO implica divergencia**: las órbitas con pocas
   visitas a P convergen más rápido. El umbral del ratio solo funciona en
   una dirección.

3. **El resonator HRR ve solo azar en la secuencia de pasos** — consistente
   con DDSD (medida invariante plana en log): la secuencia es pseudorandom
   **por diseño**. La información está en el drift (el promedio), no en los
   pasos individuales.

4. **El forzado de observador no rompe la equidistribución** (experimento
   `exp_collatz_forzado.py`): forzar la medición (ε≥0.10 cruza f_P* en la
   medición) NO genera divergencia real — termination rate 1.00 en todos
   los ε. La divergencia de sustrato (a≥4, drift≥0) es la única real.

**Conexión con la ley ρ** ([`Rylow999/fhrr-rho-collapse`](https://github.com/Rylow999/fhrr-rho-collapse)):
en VSA el observador tiene una banda crítica (κ∈[10³,10⁴]) donde colapsa.
En Collatz, NINGÚN observador encuentra divergencia — el sustrato la impide.
La tesis filosófica del programa: el colapso es relativo al observador;
cuando ni el observador ni el instrumento lo producen, queda la estructura
irreducible del sustrato.
