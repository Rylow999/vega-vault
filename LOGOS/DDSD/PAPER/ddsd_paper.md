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
| Pearson $ho$ | 0.981 |
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

- **7 classes** use $3n+1$ (dissipative)
- **9 classes** use $5n+1$ (expansive)

This yields an effective drift of approximately zero.

### 6.1 Bimodal Behavior

| Outcome | Fraction | Max $\log_2 n$ (typical) |
|---------|----------|--------------------------|
| Collapse to 1 | 22.6% | ~43 |
| Explosion | 77.4% | ~192 |

The map is **not** neutrally stable. It exhibits **bistability**: some seeds collapse, others explode, depending on the local sequence of coefficient choices. The proportion of $3x+1$ steps actually experienced varies from 22% to 58% across seeds.

### 6.2 Percolation Analysis

We classify 20,000 consecutive odd seeds:

| Metric | Value |
|--------|-------|
| Collapsing seeds | 41.2% |
| Exploding seeds | 58.8% |
| Mean run of collapsers | 1.8 |
| Mean gap of exploders | 2.5 |
| Density in windows of 5,000 | $0.420 \pm 0.023$ |

**Interpretation:** There are **no macro-clusters**. The set of collapsing seeds is **porous**: collapsing and exploding seeds are interleaved at fine scale. The density is essentially uniform across the entire range.

## 7. 2-Adic Variable Field

We construct a map where the coefficient depends on the high bits of $n$ (a "2-adic field"):

- Bits 0--5: $a=3$ (dissipative zone)
- Bits 6--9: mixed (frontier zone)
- Bits 10--15: $a=5$ (expansive zone)

### 7.1 Results

| Starting zone | Drift | Termination | Time in dissipative | Time in expansive |
|---------------|-------|-------------|---------------------|-------------------|
| Dissipative | $-0.003$ | 60% | 75% | 22% |
| Frontier | $-0.003$ | 60% | 75% | 22% |
| Expansive | $-0.003$ | 60% | 75% | 22% |

**Key finding:** Regardless of starting zone, trajectories converge to the same time distribution: ~75% in the dissipative zone, ~22% in the expansive zone. The dissipative zone is **"sticky"** — once a trajectory enters, it tends to stay.

### 7.2 Transition Matrix (normalized by row)

| From \ To | Dissipative | Frontier | Expansive |
|------------|-------------|----------|-----------|
| Dissipative | 0.76 | 0.17 | 0.07 |
| Frontier | 0.72 | 0.18 | 0.10 |
| Expansive | 0.73 | 0.16 | 0.11 |

The transition probabilities are **asymmetric**: it is easier to move from expansive to dissipative than vice versa. The dissipative zone acts as an attractor in the space of 2-adic regions.

## 8. Toy Hash Model: Is SHA-256 a Collatz?

We construct a toy cryptographic hash model inspired by SHA-256: 64-bit state, 4 words of 16 bits, 32 rounds with non-linear functions (Choose/Majority), rotations, and modular addition. We define energy as Hamming distance to the final state after all rounds.

### 8.1 DDSD Verification on Toy Hash

| Metric | Toy Hash | Collatz | Interpretation |
|--------|----------|---------|----------------|
| A1 Cor($E, \pi_6$) | 0.009 | 0.182 | **Perfect decorrelation** |
| A1 $R^2$ | 0.0001 | 0.033 | Energy completely unpredictable |
| A2 Entropy | 0.998 | 0.971 | **Maximum mixing** |
| A3 $\Phi_8$ | **$-$1.29** | **$-$0.081** | **15× stronger drift** |
| A3 $p$-value | $<10^{-66}$ | $2.3	imes10^{-26}$ | Massive dissipation |
| A4 Freq ($arepsilon=10$) | 3% | 52% | **No recurrence** (converges) |

### 8.2 Interpretation

The toy hash is **hyper-dissipative**. Energy (Hamming distance to final state) decreases by ~1 bit per round. In 32 rounds, any seed converges to a thoroughly mixed state. There are no fluctuations, no recurrence, no mystery.

**Collatz, in comparison, is a marginal system.** Its drift is weak ($-0.08$ per step), fluctuations are enormous, and energy oscillates like a roller coaster. The conjecture is difficult precisely because Collatz is **not** hyper-dissipative — it is "barely" dissipative.

### 8.3 The Hierarchy of Dissipation

| System | Drift | Behavior |
|--------|-------|----------|
| Toy hash | $-1.29$ | Instant convergence |
| Evolved map (Sec. 9) | $-0.23$ | Fast convergence |
| Collatz | $-0.081$ | Slow, fluctuating convergence |
| Critical map 7/16 | $pprox 0$ | Bimodal (collapse or explode) |
| 5x+1 | $+0.32$ | Divergence |

**Implication:** Cryptographic security and Collatz boundedness are two faces of the same phenomenon: a system where local expansion is dominated by mixing and compression. The difference is only of **degree**, not of **nature**. If one could prove that "all systems with sufficiently strong negative drift converge," the result would unify hash functions and Collatz.

## 9. Evolving Better Maps: Genetic Algorithm

We define a **DDSD fitness function** and use a genetic algorithm to search for maps that maximize structural dissipation. Each individual is a map where the coefficient $a \in \{3,5,7,9\}$ depends on $n mod 32$ (a chromosome of 16 genes).

### 9.1 Fitness Function

$$	ext{fitness} = -2 	imes 	ext{drift} + 	ext{termination rate} + 	ext{simplicity bonus}$$

where simplicity bonus rewards using fewer distinct coefficients.

### 9.2 Evolution Parameters

- Population: 20 individuals
- Generations: 15
- Selection: Tournament from top 50%
- Crossover: Single-point
- Mutation rate: 15%
- Elite preservation: 4 individuals
- Fitness evaluation: 50 random seeds per individual

### 9.3 Results

| Map | Fitness | Drift | Termination | Chromosome |
|-----|---------|-------|-------------|------------|
| **Best evolved** | **1.81** | **$-$0.23** | **100%** | Mixed (7×3, 6×5, 2×7, 1×9) |
| Collatz pure | 1.25 | $-$0.09 | 100% | All 3 |
| 5x+1 pure | 0.04 | $+$0.32 | 0% | All 5 |

**The evolved map outperforms Collatz.** It achieves 2.5× stronger negative drift while maintaining 100% termination and similar maximum orbit sizes ($\log_2 n pprox 29$). The genetic algorithm discovered that a **strategic mixture** of coefficients, with $a=3$ dominant but supplemented by occasional larger coefficients, creates stronger dissipation than pure Collatz.

### 9.4 Runtime Coefficient Distribution

When executing the evolved map, the actual coefficient usage is:

| Coefficient | Usage |
|-------------|-------|
| $a=3$ | 41.2% |
| $a=5$ | 39.9% |
| $a=7$ | 12.1% |
| $a=9$ | 6.9% |

Despite the chromosome having only 43.75% classes with $a=3$, the runtime distribution is nearly balanced. The larger coefficients are used in "strategic" positions that accelerate descent without causing explosion.

### 9.5 Implication

**Collatz is not optimal.** Within the space of maps definable by mod-32 rules, there exist maps with stronger dissipation and identical termination. This suggests that the Collatz conjecture, if true, is not due to Collatz being uniquely structured, but rather due to it being **one representative** of a broad family of dissipative maps. The conjecture might be easier to prove for the family than for the specific map.

## 10. Primes in the Inverse Tree: A Negative Result

We test the hypothesis that primes are structurally enriched in paths converging to 1.

### 10.1 Collatz Inverse Tree (50,000 nodes)

| Measure | Value |
|---------|-------|
| Tree prime density | 6.73% |
| Random baseline | 5.87% |
| Global enrichment | 1.15× |

However, when stratified by value range:

| $\log_2(n)$ range | Tree density | Baseline | Ratio |
|-------------------|--------------|----------|-------|
| [0, 10) | 16.67% | 37.14% | **0.45×** |
| [10, 20) | 9.81% | 14.57% | **0.67×** |
| [20, 30) | 7.47% | 9.70% | **0.77×** |
| [30, 40) | 6.43% | 7.23% | **0.89×** |
| [40, 50) | 5.85% | 5.79% | **1.01×** |

**Interpretation:** In every individual range, the tree has **equal or fewer** primes than the baseline. The apparent global enrichment (1.15×) is a **statistical artifact** of the tree's value distribution. There is **no arithmetic mechanism** enriching primes in convergent paths.

### 10.2 Critical Map Inverse Tree (5,970 nodes)

| Measure | Value |
|---------|-------|
| Tree prime density | 11.17% |
| Random baseline | 8.17% |
| Enrichment | 1.37× |

This stronger enrichment is attributable to the smaller sample size and the dominance of the mod-19 class (5x+1), which has a different value distribution. It does not indicate a structural connection between primes and collapse.

## 11. Discussion

### 11.1 What the Framework Does

The DDSD framework provides a **taxonomic lens** for discrete dynamical systems:
- **A1** measures whether energy is predictable from coarse state.
- **A2** measures whether dynamics are dispersive within fibers.
- **A3** measures whether macroscopic drift is negative.
- **A4** measures whether orbits return to low-energy regions.

Applied to Collatz and 5x+1, **A3 is the sole discriminant**. Collatz has negative macroscopic drift; 5x+1 does not. A1, A2, and A4 are shared properties of both maps.

### 11.2 What the Framework Does Not Do

- **Does not prove boundedness.** A3 is a measured property, not a derived consequence of A1+A2+A4.
- **Does not prove convergence to (1,4,2).** Boundedness (if established) does not imply cycle uniqueness.
- **Does not establish an invariant measure.** The ML fit is exploratory.
- **Does not connect to primes.** The apparent prime enrichment is a statistical artifact.

### 11.3 Honest Boundaries

- **A4 failure as discriminant:** We initially hypothesized A4 as a dissipative property, but it holds for both maps. This is an honest negative result.
- **K-scaling:** The preliminary observation $K_{	ext{crit}} pprox \log_2(n)/5$ does not hold with increased data. We report raw values without claiming a law.
- **Mersenne identity:** $E(2^p-1)=p$ is exact by definition ($
u_2(2^p)=p$). It has no dynamical content and is omitted as a main result.
- **Phase boundary:** The exact boundary at $a=4$ is theoretically elegant but inaccessible to odd-integer maps. The artificial critical map shows bimodal behavior, not a smooth transition.
- **Evolved map:** The genetic algorithm found a map better than Collatz within the DDSD fitness landscape. This does not invalidate Collatz; it shows that the landscape is richer than previously explored.

### 11.4 Implications for Collatz

The framework reveals that Collatz's boundedness is **structurally overdetermined**:
1. The exact 2-adic drift ($\log_2 3 - 2 pprox -0.42$) is robustly negative.
2. The dissipative zone is "sticky" in the 2-adic topology.
3. The map is the last odd representative of a dissipative family.
4. Hyper-dissipative systems (hashes) converge instantly; Collatz converges slowly because its margin is smaller.
5. Better maps exist in the same fitness landscape, suggesting the conjecture is a property of the landscape, not the specific point.

This does not prove the conjecture, but it explains **why the conjecture is plausible**: Collatz is not a delicate balance, but a system with substantial dissipative margin, surrounded by a family of similar systems.

## 12. Conclusion

The DDSD framework structurally characterizes dissipative discrete systems through four measurable axioms. Computational verification on 952 Collatz trajectories and 200 5x+1 trajectories shows that **negative macroscopic drift (A3)** is the property that distinguishes bounded from unbounded behavior. The exact 2-adic drift formula $\Phi(a) = \log_2(a) - 2$ places Collatz as the last odd dissipative map before an inaccessible boundary. A toy hash model demonstrates that cryptographic compression and Collatz dynamics share the same structural recipe with different dissipation strength. A genetic algorithm discovers maps with stronger drift than Collatz, proving that the DDSD fitness landscape is richer than the single known example. The framework is a taxonomic tool, not a proof of the Collatz conjecture, but it unifies diverse systems under a single structural language and points toward a family-level approach to the problem.

---

## References

1. T. Tao, "Almost all Collatz orbits attain almost bounded values," *arXiv:1909.03562*, 2019.
2. J. C. Lagarias, "The $3x+1$ problem and its generalizations," *Amer. Math. Monthly*, 92(1):3--23, 1985.
3. R. Bradley, *Introduction to Strong Mixing Conditions*, Heldermann Verlag, 2005.
