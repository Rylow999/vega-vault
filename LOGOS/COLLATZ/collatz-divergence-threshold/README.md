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
