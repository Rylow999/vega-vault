---
ontology_id: pape_4f227a39
type: Paper
title: thermodynamic_confinement_v4
tags: []
---
# thermodynamic_confinement_v4

**Ontology ID**: `pape_4f227a39`
**Type**: Paper

**authors**: ['Luciano Benjamín Nieto']
**year**: 2026
**venue**: Technical Report
**doi**: 
**url**: 
**summary**: # Thermodynamic Confinement in Discrete Dynamical Systems
## Spectral Phase Transition in the Family of Accelerated Collatz Maps: From Point Localization to Continuous Spectrum

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Research  
**Contact:** lucianobenjaminnieto@gmail.com  
**Date:** 2026  
**License:** CC-BY 4.0 (Share, adapt, build upon freely)

---

## Abstract

We present computational evidence for a spectral phase transition in the family of accelerated maps $R_a(n) = (an+1)/2^{\nu_2(an+1)} \bmod 2^K$, parameterized by the odd coefficient $a$. For $a=3$ (Collatz), we verify a clean spectral gap with a unique dominant cycle ($\lambda = 3/4$, drift $= -0.415$) up to $K=30$, with a single isolated resonance at $K=20$ (cycle length 22, drift $+0.221$) exhibiting internal block structure. For $a=5$, we discover neutral cycles ($\lambda = 1.0$, drift $= 0$) dominating 94.9% of the dynamics at $K=28$. For $a=7$ (Ultra-Champion), we find multiple unstable cycles 
**tags**: []

---

# Thermodynamic Confinement in Discrete Dynamical Systems
## Spectral Phase Transition in the Family of Accelerated Collatz Maps: From Point Localization to Continuous Spectrum

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Research  
**Contact:** lucianobenjaminnieto@gmail.com  
**Date:** 2026  
**License:** CC-BY 4.0 (Share, adapt, build upon freely)

---

## Abstract

We present computational evidence for a spectral phase transition in the family of accelerated maps $R_a(n) = (an+1)/2^{\nu_2(an+1)} \bmod 2^K$, parameterized by the odd coefficient $a$. For $a=3$ (Collatz), we verify a clean spectral gap with a unique dominant cycle ($\lambda = 3/4$, drift $= -0.415$) up to $K=30$, with a single isolated resonance at $K=20$ (cycle length 22, drift $+0.221$) exhibiting internal block structure. For $a=5$, we discover neutral cycles ($\lambda = 1.0$, drift $= 0$) dominating 94.9% of the dynamics at $K=28$. For $a=7$ (Ultra-Champion), we find multiple unstable cycles with eigenvalues up to 3.5, dominating 99.997% of the dynamics at $K=30$. We propose a phase diagram in the parameter $a$ with three distinct types: Type I (spectral gap, $a=3$), Type II (marginal spectrum, $a=5$), and Type III (continuous spectrum, $a \geq 7$). The Inverse Participation Ratio (IPR) jumps from low values (extended states) to IPR = 1.0 (perfect point localization) for Type I systems. We independently verify Chang's (2026) Map Balance Theorem for pure Collatz (bit-4 structure confirmed) and discover that the Ultra-Champion map breaks this structure, providing a computational bridge between Chang's formal reduction and the spectral phase diagram. We explicitly document what we proved and what we did not, including honest negative results and the failure of our initial hypotheses regarding universality.

**Keywords:** Collatz conjecture, Ruelle operator, 2-adic dynamics, spectral phase transition, Anderson localization, discrete dynamical systems, computational number theory, one-bit mixing structure

---

## 1. Introduction

### 1.1 The Problem

The Collatz conjecture asks whether every positive integer $n$ eventually reaches the cycle $(1,4,2)$ under iteration of $T(n) = n/2$ (even) or $3n+1$ (odd). Tao (2019) proved that almost all orbits attain almost bounded values. We ask a different question: what structural properties of the map make boundedness thermodynamically plausible, and how do these properties vary across the family of maps $R_a(n) = (an+1)/2^{\nu_2(an+1)}$?

### 1.2 Our Approach

Rather than attacking Collatz directly with number-theoretic tools, we embed it in a framework borrowed from condensed matter physics and quantum information theory. The central thesis:

> **Collatz is a marginally dissipative discrete system operating below the Hagedorn criticality, where Anderson localization in 2-adic space confines orbits to the cycle $(1,4,2)$.**

This is a framework proposal, not a proof. We provide computational evidence and establish formal connections to existing results (Lagarias 1985, Wirsching 1998, Chang 2026), but the central claim remains a research program.

### 1.3 Main Results

1. **Phase transition at $K=13$ for $a=3$:** Truncation cycles disappear abruptly, leaving only the trivial cycle $n=1$ with $\lambda = 0.75$.
2. **Isolated resonance at $K=20$:** A single exotic cycle (length 22, drift $+0.221$) appears, affecting only 0.05% of nodes, with internal block structure (three blocks with constant $\sum \nu_2 = 10$).
3. **Robustness up to $K=30$:** For $a=3$, the transition persists for all verified $K \in \{13, 14, \ldots, 30\}$ except $K=20$.
4. **Phase diagram in $a$:** Three distinct types emerge — Type I ($a=3$, spectral gap), Type II ($a=5$, marginal), Type III ($a \geq 7$, continuous spectrum).
5. **Failure of universality:** The Ultra-Champion map ($a=7$) never exhibits a clean spectral gap, invalidating our initial hypothesis of universal 1-cycle behavior.
6. **Verification and extension of Chang (2026):** Pure Collatz satisfies Chang's Map Balance Theorem (bit-4 structure confirmed); Ultra-Champion breaks it. The one-bit structure is a signature of Type I spectra, not dissipation in general.

### 1.4 Structure

- Section 2: Mathematical framework (discretized Ruelle operator)
- Section 3: Computational methodology (FATE v2/v3)
- Section 4: Results for $a=3$ (Collatz) — K=10 to K=30
- Section 5: Results for $a=5$ (intermediate case) — K=28
- Section 6: Results for $a=7$ (Ultra-Champion) — K=10 to K=30
- Section 7: Phase diagram in the parameter $a$
- **Section 8: Relation to Chang (2026) — NEW**
- Section 9: Connection to Anderson localization (structural analogy)
- Section 10: Transient-asymptotic duality of Ultra-Champion
- Section 11: What we proved and what we did not
- Section 12: Conclusions and open problems
- Appendix A: Verification protocol
- Appendix B: Attempt to destroy the paper (self-critique)
- Appendix C: Correction notes (v2.0 → v3.0 → v4.0 → v4.1)
- **Appendix D: Exact nodes of K=20 resonance — NEW**

---

## 2. Mathematical Framework

### 2.1 The Accelerated Map

**Definition 2.1 (Accelerated map):** For odd $a$ and integer $n$, define:
$$R_a(n) = \frac{an + 1}{2^{\nu_2(an+1)}}$$
where $\nu_2(m)$ is the 2-adic valuation (largest power of 2 dividing $m$).

### 2.2 The Discretized Ruelle Operator

**Definition 2.2 (Discretized Ruelle operator):** Let $X_K = \{x \in \mathbb{Z}/2^K\mathbb{Z} : x \equiv 1 \pmod{2}\}$ be the set of odd residues modulo $2^K$, with $|X_K| = N = 2^{K-1}$. The discretized Ruelle operator $L^{(K)}$ is the $N \times N$ matrix with entries:

$$L^{(K)}_{x,y} = \begin{cases} \frac{a}{2^{\nu_2(ay+1)}} & \text{if } R_a(y) \equiv x \pmod{2^K} \\ 0 & \text{otherwise} \end{cases}$$

**Property 2.2.1:** $L^{(K)}$ is a weighted permutation matrix (exactly one non-zero entry per column).

### 2.3 Spectrum-Cycles Relation

**Theorem 2.3 (Spectrum-Cycles Relation):** The eigenvalues of $L^{(K)}$ are determined exclusively by the cycles of the functional graph of $R_a$ on $X_K$. For each cycle $C$ of length $L$ with weight product $W_C = \prod_{y \in C} \frac{a}{2^{\nu_2(ay+1)}}$, there exist $L$ eigenvalues:

$$\lambda_j = W_C^{1/L} \cdot e^{2\pi i j / L}, \quad j = 0, 1, \ldots, L-1$$

**Proof:** Standard result for weighted permutation matrices. Each cycle contributes a cyclic permutation block, whose eigenvalues are the $L$-th roots of the cycle weight. $\square$

**Corollary 2.3.1:** The dominant eigenvalue is $\lambda_1 = \max_C W_C^{1/L}$, and its magnitude is the geometric weight of the heaviest cycle.

### 2.4 Drift and Localization

**Definition 2.4 (Drift):** The drift of a cycle $C$ is:
$$\Phi(C) = \log_2(W_C^{1/L}) = \frac{\log_2 W_C}{L} = \log_2 |\lambda_1|$$

- $\Phi < 0$: contractive/stable cycle
- $\Phi = 0$: neutral/marginal cycle
- $\Phi > 0$: expansive/unstable cycle

**Definition 2.5 (IPR — Inverse Participation Ratio):** For an eigenvector $\psi$ normalized as $\sum_i |\psi_i|^2 = 1$:
$$\text{IPR} = \sum_{i=1}^{N} |\psi_i|^4$$

- IPR $\approx 1/N$: extended state (uniform distribution)
- IPR $\approx 1$: point-localized state (Kronecker delta)
- IPR $\approx 1/L$: state distributed over $L$ nodes of a cycle

### 2.5 Basin of Attraction

**Definition 2.6 (Basin of attraction):** For a cycle $C$, the basin of attraction $\mathcal{B}(C)$ is the set of all nodes $y \in X_K$ whose forward orbit under $R_a$ eventually enters $C$.

---

## 3. Computational Methodology

### 3.1 FATE Algorithm v2/v3

**Algorithm 3.1 (FATE — Full Adaptive Truncation Evasion):**
1. Initialize all nodes with `state = 0` (unvisited)
2. For each unvisited node $y$:
   - Follow the orbit $y \to R_a(y) \to R_a^2(y) \to \ldots$
   - Mark visited nodes with `state = 1` (in progress)
   - If a node with `state = 1` is encountered: new cycle detected
   - If a node with `state = 2` is encountered: inherit known cycle
3. Extract cycle, compute weight $W_C$, eigenvalues, drift
4. Mark all path nodes with `state = 2` and `cycle_id`

**Complexity:** $O(N)$ total time and memory.

### 3.2 Implementation Details

| Parameter | Value |
|-----------|-------|
| Compiler | gcc 12+ with `-O3 -march=native -ffast-math` |
| $\nu_2(n)$ | `__builtin_ctzll` (hardware instruction) |
| Memory (v2) | 5 bytes/node (`uint8_t` + `uint32_t`) |
| Memory (v3) | 3 bytes/node (`uint8_t` + `uint16_t`) |
| Max K (v2) | K=29 (~1.3 GB) |
| Max K (v3) | K=30 (~1.5 GB) |
| Verification | 3 independent implementations (dict, array, bit-by-bit) |

### 3.3 Verification Protocol

All results were cross-verified with:
1. Python implementation using dictionaries
2. NumPy array-based implementation
3. C implementation with path compression

Discrepancies between implementations were resolved before reporting.

---

## 4. Results for $a=3$ (Collatz): K=10 to K=30

### 4.1 Pre-Transition Region (K ≤ 12): Multiple Truncation Cycles

| K | Matrix Size | # Cycles | Cycle 1 (trivial) | Cycle 2 | Cycle 3 |
|---|-------------|----------|-------------------|---------|---------| 
| 10 | 512×512 | 2 | L=1, λ=0.75, Φ=−0.415 | **L=26**, W=18.49, Φ=**+0.126** | — |
| 11 | 1024×1024 | 2 | L=1, λ=0.75, Φ=−0.415 | **L=25**, W=6.16, Φ=**+0.079** | — |
| 12 | 2048×2048 | 3 | L=1, λ=0.75, Φ=−0.415 | **L=7**, W=4.27, Φ=**+0.296** | **L=6**, W=5.70, Φ=**+0.376** |

**Observation:** Truncation cycles have **positive drift**, indicating instability in the Ruelle operator sense.

**Spectral details:**
- K=10: 26 eigenvalues with $|\lambda| = 1.11874837$, phases multiples of $13.846° = 360°/26$
- K=11: 25 eigenvalues with $|\lambda| = 1.07546644$, phases multiples of $14.4° = 360°/25$
- K=12: 7 eigenvalues with $|\lambda| = 1.23050303$ (order 7) + 6 eigenvalues with $|\lambda| = 1.33634808$ (order 6)

### 4.2 The Phase Transition at K=13

| K | Matrix Size | # Cycles | Dominant $\|\lambda_1\|$ | Drift | IPR | Basin n=1 |
|---|-------------|----------|------------|---------|-------|-----------|
| **13** | **4096×4096** | **1** | **