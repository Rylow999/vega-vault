---
ontology_id: pape_2924dc48
type: Paper
title: ddsd_paper
tags: []
---
# ddsd_paper

**Ontology ID**: `pape_2924dc48`
**Type**: Paper

**authors**: ['Luciano Benjamín Nieto']
**year**: 2026
**venue**: Technical Report
**doi**: 
**url**: 
**summary**: # Structural Dissipation in Discrete Dynamical Systems: A Computational Characterization

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Research  
**Contact:** lucianobenjaminnieto@gmail.com  
**Date:** 2026  
**License:** CC-BY 4.0 (Share, adapt, build upon freely)

---

## Abstract

We introduce the DDSD framework as a structural characterization of dissipative behavior in discrete dynamical systems. The framework proposes four measurable properties: (A1) decay of energy-projection correlation with coarse-graining resolution; (A2) intrafiber output dispersion; (A3) scale-dependent negative macroscopic drift; and (A4) pathwise recurrence to low-energy regions. We instantiate this framework on the Collatz $3x+1$ map, the divergent $5x+1$ map, a family of perturbed maps $ax+1$, an artificial critical map, a 2-adic variable field, a toy cryptographic hash model, and an evolved map discovered via genetic algorithm. Computational verification on 952 Collatz trajectories
**tags**: []

---

# Structural Dissipation in Discrete Dynamical Systems: A Computational Characterization

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Research  
**Contact:** lucianobenjaminnieto@gmail.com  
**Date:** 2026  
**License:** CC-BY 4.0 (Share, adapt, build upon freely)

---

## Abstract

We introduce the DDSD framework as a structural characterization of dissipative behavior in discrete dynamical systems. The framework proposes four measurable properties: (A1) decay of energy-projection correlation with coarse-graining resolution; (A2) intrafiber output dispersion; (A3) scale-dependent negative macroscopic drift; and (A4) pathwise recurrence to low-energy regions. We instantiate this framework on the Collatz $3x+1$ map, the divergent $5x+1$ map, a family of perturbed maps $ax+1$, an artificial critical map, a 2-adic variable field, a toy cryptographic hash model, and an evolved map discovered via genetic algorithm. Computational verification on 952 Collatz trajectories up to $2^{40}$ and 200 $5x+1$ trajectories shows that A3 discriminates the two systems under Bonferroni-corrected multiplicity testing. A1 and A2 are shared structural properties. A4 does not discriminate. A neural network approximation of the empirical invariant measure achieves $R^2=0.96$ under leave-one-out cross-validation, providing exploratory evidence for smoothness in log-coordinates. The exact drift in the 2-adic setting is $\log_2(a) - 2$, placing Collatz ($a=3$) as the last odd dissipative map before the inaccessible boundary at $a=4$. An artificial critical map exhibits bimodal behavior (23% collapse, 77% explosion) with no macro-clusters. A 2-adic variable field mixing dissipative and expansive zones yields intermediate termination rates (~60%). A toy hash model exhibits hyper-dissipative behavior (drift $-1.29$) with perfect decorrelation, suggesting that cryptographic hashes and Collatz share the same structural recipe with different dissipation strength. A genetic algorithm discovers a map with drift $-0.23$ (2.5× stronger than Collatz) and 100% termination, proving that Collatz is not optimal within the DDSD fitness landscape. The framework is presented as a taxonomic tool, not as a proof of boundedness.

## 1. Introduction

The Collatz conjecture asks whether every orbit of the map $T(n) = n/2$ (even) or $3n+1$ (odd) reaches the cycle $(1,4,2)$. Tao (2019) proved that almost all orbits attain almost bounded values. We ask a different question: what structural properties of the map make boundedness plausible?

We propose that dissipative discrete systems share four measurable structural features. This paper does **not** prove boundedness. It provides a **computational characterization** that distinguishes structurally dissipative maps from expansive ones, and explores the phase boundary between them.

## 2. The DDSD Framework

**Definition 2.1 (DDSD System).** A tuple $\mathcal{D} = (X, T, \{\pi_k\}, E)$ where $X$ is a state space, $T$ deterministic dynamics, $\pi_k$ hierarchical coarse-grainings, and $E$ an energy function.

The four proposed structural properties are:

### A1: Resolution-Dependent Decorrelation

The predictive power of $\pi_k$ for $E$ decays as $k$ increases. Formally, $R^2(E, \pi_k)$ is a decreasing function of $k$. At sufficiently fine resolution ($k \geq k^*$), $R^2 < 0.05$.

### A2: Intrafiber Output Dispersion

Within each fiber $\pi_k^{-1}(z)$, the distribution of $\pi_k(T(x))$ has high normalized entropy. This measures output dispersion, not ergodic mixing.

### A3: Scale-Dependent Negative Macroscopic Drift

There exists a minimal observation window $K$ such that the $K$-step energy increment satisfies $\mathbb{E}[\Delta_K E] < 0$ with statistical significance after multiplicity correction.

### A4: Pathwise Recurrence

Every trajectory visits the low-energy region $D_arepsilon = \{x : E(x) < arepsilon\}$ infinitely often with positive frequency.

## 3. Computational Verification

### 3.1 Setup

**Collatz:** 1,000 random odd seeds across four scales: $[3,2^{18})$, $[2^{18},2^{30})$, $[2^{30},2^{35})$, $[2^{35},2^{40})$. Accelerated map $R(n) = (3n+1)/2^{
u_2(3n+1)}$. 952 valid trajectories (>20 steps). Energy: $E(n) = 
u_2(n+1)$.

**5x+1:** 200 seeds (20 known divergent + 60 random per scale). Max 200 steps, 256-bit ceiling.

### 3.2 A1: Resolution-Dependent Decorrelation

| $k$ | Collatz Cor$(E,\pi_k)$ | $R^2$ | 5x+1 Cor$(E,\pi_k)$ | $R^2$ |
|-----|------------------------|-------|---------------------|-------|
| 2 | 0.725 | 0.525 | 0.700 | 0.490 |
| 4 | 0.471 | 0.222 | 0.466 | 0.217 |
| 6 | 0.182 | 0.033 | 0.203 | 0.041 |
| 8 | 0.103 | 0.011 | 0.081 | 0.007 |
| 10 | 0.061 | 0.004 | 0.039 | 0.002 |

Both maps show monotonic decay. At $k \geq 6$, predictive power is negligible ($R^2 < 0.05$). This is a shared structural property.

### 3.3 A2: Intrafiber Output Dispersion

**Collatz:** Mean normalized entropy = 0.971 (32 of 64 fibers contain data; accelerated map preserves odd parity).

**5x+1:** Mean normalized entropy = 0.995.

Both maps exhibit high intrafiber dispersion. 5x+1 is slightly higher.

### 3.4 A3: Scale-Dependent Negative Drift (Bonferroni-Corrected)

We test 9 values of $K \in \{1,2,4,6,8,10,12,16,20\}$. Bonferroni threshold: $lpha = 0.01/9 = 0.0011$.

**Collatz K-sweep:**

| $K$ | $\Phi_K$ | raw $p$ | Bonferroni $p$ | Significant? |
|-----|----------|---------|----------------|--------------|
| 1 | $-0.012$ | 0.017 | 0.154 | No |
| 2 | $-0.025$ | $7.7	imes10^{-5}$ | $6.9	imes10^{-4}$ | **Yes** |
| 4 | $-0.046$ | $2.6	imes10^{-10}$ | $2.4	imes10^{-9}$ | **Yes** |
| 6 | $-0.053$ | $7.5	imes10^{-13}$ | $6.8	imes10^{-12}$ | **Yes** |
| 8 | $-0.081$ | $2.3	imes10^{-26}$ | $2.0	imes10^{-25}$ | **Yes** |
| 10 | $-0.106$ | $4.8	imes10^{-42}$ | $4.3	imes10^{-41}$ | **Yes** |
| 12 | $-0.110$ | $9.3	imes10^{-43}$ | $8.4	imes10^{-42}$ | **Yes** |
| 16 | $-0.103$ | $3.2	imes10^{-35}$ | $2.9	imes10^{-34}$ | **Yes** |
| 20 | $-0.057$ | $3.4	imes10^{-12}$ | $3.0	imes10^{-11}$ | **Yes** |

**5x+1 K-sweep:**

| $K$ | $\Phi_K$ | raw $p$ | Bonferroni $p$ | Significant? |
|-----|----------|---------|----------------|--------------|
| 1 | $-0.0005$ | 0.956 | 1.000 | No |
| 2 | $-0.0004$ | 0.965 | 1.000 | No |
| 4 | $-0.0001$ | 0.992 | 1.000 | No |
| 6 | $-0.0001$ | 0.992 | 1.000 | No |
| 8 | $+0.0001$ | 0.990 | 1.000 | No |
| 10 | $-0.00005$ | 0.996 | 1.000 | No |
| 12 | $+0.0003$ | 0.977 | 1.000 | No |
| 16 | $+0.0039$ | 0.709 | 1.000 | No |
| 20 | $+0.0063$ | 0.552 | 1.000 | No |

**Interpretation:** Collatz exhibits statistically significant negative drift for all $K \geq 2$. 5x+1 shows drift statistically indistinguishable from zero at all tested scales. A3 is the **discriminant**.

### 3.5 A4: Pathwise Recurrence

| $arepsilon$ | Collatz mean freq | min freq | 5x+1 mean freq | min freq |
|---------------|-------------------|----------|----------------|----------|
| 2 | 0.522 | 0.390 | 0.493 | 0.250 |
| 3 | 0.762 | 0.610 | 0.754 | 0.682 |

**Interpretation:** Both maps visit low-energy regions with comparable frequency. A4 is a shared property, not a discriminant.

### 3.6 Scale-Dependent Critical K

| Scale | $K_{	ext{crit}}$ (Bonferroni) | Avg $\log_2 n$ | Ratio |
|-------|-------------------------------|----------------|-------|
| Small | 3 | 17.0 | 5.7 |
| Medium | 4 | 29.1 | 7.3 |
| Large | 7 | 34.0 | 4.9 |
| VLarge | 8 | 39.0 | 4.9 |

The ratio $\log_2(n)/K_{	ext{crit}}$ varies between 4.9 and 7.3. No stable scaling law is established. This remains a preliminary observation.

## 4. Invariant Measure Approximation

We fit an MLP (32-16-8, tanh, L-BFGS, $lpha=0.01$) to the empirical density in 64 log-bins using 6 engineered features. Evaluation uses **leave-one-out cross-validation** on 64 data points.

| Metric | Value |
|--------|-------|
| $R^2$ (LOO-CV) | 0.959 |
| Pearson $
ho$ | 0.981 |
| KL divergence | 0.025 |
| Smoothness (empirical std($\Delta$)) | 0.0026 |
| Smoothness (predicted std($\Delta$)) | 0.0037 |

**Interpretation:** The model captures the global density shape but is slightly noisier than the empirical histogram. The high $R^2$ may reflect the simplicity of the density (unimodal decay) rather than deep structural learning. This is exploratory evidence, not proof of measure existence.

## 5. Phase Diagram in $\mathbb{Z}_2$: The Exact Drift

### 5.1 Theoretical Result

For the accelerated map $R_a(n) = (an+1)/2^{
u_2(an+1)}$ with $a$ odd, operating on the 2-adic integers $\mathbb{Z}_2$ with Haar measure, the expected 2-adic valuation satisfies:

$$\mathbb{E}[
u_2(an+1)] = 2 \quad 	ext{(independent of } a	ext{)}$$

Therefore, the drift in log-coordinates is exactly:

$$\Phi(a) = \log_2(a) - 2$$

**Proof sketch:** For $a$ odd, $an+1$ is always even. The probability that $
u_2(an+1) \geq k$ is exactly $1/2^{k-1}$ for all $k \geq 1$, because $a$ is invertible modulo $2^k$. The expectation follows from $\sum_{k=1}^{\infty} k/2^k = 2$. $\square$

### 5.2 The Boundary

The critical boundary is at $a = 4$, where $\Phi(4) = 0$. However, $a = 4$ is **even**, so there exists no accelerated map with odd coefficient on the boundary. The odd integers "jump" from $a=3$ (drift $-0.415$) to $a=5$ (drift $+0.322$) without touching the boundary.

| $a$ | $\log_2(a)$ | Drift $\Phi(a)$ | Behavior |
|-----|-------------|-----------------|----------|
| 1 | 0.000 | $-2.000$ | Trivially collapsing |
| 3 | 1.585 | $-0.415$ | **Collatz (dissipative)** |
| 5 | 2.322 | $+0.322$ | **5x+1 (expansive)** |
| 7 | 2.807 | $+0.807$ | Explosive |
| 9 | 3.170 | $+1.170$ | More explosive |

**Interpretation:** Collatz is not "special." It is simply the **last odd map** before the inaccessible boundary at $a=4$. The transition from bounded to unbounded behavior is abrupt because the boundary is unreachable from the odd integers.

## 6. The Artificial Critical Map

To study the boundary phenomenologically, we construct a mixed map where the coefficient depends on $n mod 32$:

- **7 classes** use $3n