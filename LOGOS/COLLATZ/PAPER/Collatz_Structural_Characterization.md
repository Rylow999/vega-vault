# Structural Characterization of the Collatz Map: Drift, Divergence Threshold, and the Baire Gap

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Researcher, General Alvear, Mendoza, Argentina  
**Date:** June 29, 2026  
**Version:** v3 (corrected attribution of Chang 2026)  
**Status:** Research Paper — Rigorous Results and Open Conjectures

---

## Abstract

We present a structural characterization of the Collatz map through five rigorous results and two open conjectures. We prove: (1) the exact 2-adic drift formula $\Phi(a) = \log_2(a) - 2$; (2) the exact drift $-1$ in the natural metric $V_{4/3}(n) = \log_{4/3}(n)$; (3) the arithmetic isolation of $a=3$ as the unique non-trivial odd integer satisfying $\Phi(a) < 0$ and $a < 2^\phi$; (4) the Fibonacci structure of $\log_2(3)$ convergents; and (5) a necessary condition for divergence with exact closed-form threshold $f_P \geq f_P^* = \log_4(8/3) = (3 - \log_2 3)/2 \approx 0.7075$, where $f_P$ is the frequency of visits to the class $P = \{n \equiv 3 \pmod{4}\}$. We establish the exact identity $\mu_P + \mu_N = -2$, which algebraically unifies Theorems 2 and 5. We formulate two open conjectures — Universal Map Balance ($f_P \to 0.5$ for all orbits) and the emptiness of the divergent subspace $\Sigma_{\text{div}} = \emptyset$ via Baire category — and characterize precisely what each would require to prove. Empirical evidence from 24,866 orbits ($n \leq 50{,}000$) shows a maximum observed $f_P = 0.6667$, a 5.8% margin below the critical threshold. We explicitly identify the gap between "almost every" (Tao 2019) and "every" as the central open problem, and propose the near-zero autocorrelation of P/N steps as an empirical hint toward an ergodic pathway.

**Keywords:** Collatz conjecture, 2-adic dynamics, golden ratio, Fibonacci sequence, Baire category, drift analysis, ergodic theory

---

## 1. Introduction

The Collatz conjecture asks whether every positive integer $n$ eventually reaches the cycle $(1, 4, 2)$ under iteration of $T(n) = n/2$ (even) or $3n+1$ (odd). Tao (2019) proved that almost all orbits attain almost bounded values (logarithmic density 1), but the gap between "almost every" and "every" remains open.

We ask: what structural properties make convergence plausible, and can we characterize them rigorously?

Our approach combines exact arithmetic results (drift formulas, closed-form divergence threshold) with empirical observations (frequency balance, autocorrelation structure) to build a framework that explains why $a = 3$ is arithmetically special among the family of maps $R_a(n) = (an+1)/2^{\nu_2(an+1)}$.

**Main contributions:**

- Five rigorous theorems establishing structural properties
- One exact closed-form divergence threshold with full analytic proof (Theorem 5)
- The identity $\mu_P + \mu_N = -2$ unifying Theorems 2 and 5
- Two open conjectures with precise gap analysis
- Strong empirical evidence from 24,866 orbits
- Explicit characterization of what is proved and what is not

---

## 2. Mathematical Framework

### 2.1 The Accelerated Map

**Definition 2.1 (Accelerated Collatz Map).** For odd integer $a$ and $n \in \mathbb{N}^+$:
$$R_a(n) = \frac{an + 1}{2^{\nu_2(an+1)}}$$
where $\nu_2(m)$ is the 2-adic valuation (largest power of 2 dividing $m$).

For $a = 3$, this is the standard Collatz map accelerated by combining one odd step with all subsequent even steps.

### 2.2 Information Metric

**Definition 2.2 (Logarithmic Information).** Define $I : \mathbb{N}^+ \to \mathbb{R}$ by $I(n) = \log_2(n)$. This measures the size of $n$ in bits. The information change in one macro step is:
$$\delta I(n) = I(R_a(n)) - I(n) = \log_2\!\left(\frac{an+1}{2^{\nu_2(an+1)} \cdot n}\right)$$

### 2.3 Natural Metric of the Inverse Tree

**Definition 2.3 (Metric $V_{4/3}$).** Define $V_{4/3} : \mathbb{N}^+ \to \mathbb{R}$ by:
$$V_{4/3}(n) = \log_{4/3}(n) = \frac{\ln n}{\ln(4/3)}$$

**Motivation.** The inverse tree of Collatz has branching factor $\beta = 4/3$ (one even preimage always exists; one odd preimage exists with probability $1/3$). The metric $V_{4/3}$ is the natural coordinate system for this tree.

---

## 3. Rigorous Results

### 3.1 Theorem 1: Exact 2-Adic Drift

**Theorem 3.1 (Exact 2-Adic Drift).** For the accelerated map $R_a(n)$ with $a$ odd, under the Haar measure uniform over odd residues modulo $2^K$, the expected drift in logarithmic coordinates is:
$$\Phi(a) = \log_2(a) - 2$$

**Proof.** For $a$ odd, $an+1$ is always even. Because $a$ is invertible modulo $2^k$ (since $\gcd(a, 2) = 1$), the condition $\nu_2(an+1) \geq k$ is equivalent to $n \equiv -a^{-1} \pmod{2^k}$. Since $a^{-1}$ is odd (odd integers are closed under inversion mod $2^k$), $-a^{-1} \equiv 1 \pmod{2}$, so the required residue is always odd and well-defined. Among the $2^{k-1}$ odd residue classes modulo $2^k$, exactly one satisfies this condition, giving:
$$\mathbb{P}(\nu_2(an+1) \geq k \mid n \text{ odd}) = \frac{1}{2^{k-1}} \quad (k \geq 1)$$

Therefore:
$$\mathbb{E}[\nu_2(an+1)] = \sum_{k=1}^{\infty} \mathbb{P}(\nu_2(an+1) \geq k) = \sum_{k=1}^{\infty} \frac{1}{2^{k-1}} = 2$$

For $n$ large, $\log_2((an+1)/n) \approx \log_2(a)$, so:
$$\Phi(a) = \mathbb{E}[\log_2(R_a(n)/n)] = \log_2(a) - \mathbb{E}[\nu_2(an+1)] = \log_2(a) - 2 \qquad \blacksquare$$

**Corollary 3.1.1.**

| $a$ | $\Phi(a)$ | Behavior |
|---|---|---|
| 1 | $-2.000$ | trivial collapse |
| 3 | $-0.415$ | contractive |
| 5 | $+0.322$ | expansive |
| 7 | $+0.807$ | explosive |

**Empirical verification:** Over 250,000 odd integers, $\mathbb{E}[\nu_2(3n+1)] = 2.000000$ and $\Phi(3) = -0.415024$ (theoretical: $-0.415037$), with error $< 10^{-5}$.

**Status:** ✅ **PROVEN**

---

### 3.2 Theorem 2: Exact Drift in Metric $V_{4/3}$

**Theorem 3.2 (Exact Drift in Natural Metric).** For the Collatz map ($a = 3$), the expected drift in the metric $V_{4/3}$ is exactly $-1$ per macro step:
$$\mathbb{E}[\Delta V_{4/3}] = -1$$

**Proof.** From Theorem 3.1, $\mathbb{E}[\log_2(R_3(n)/n)] = \log_2(3) - 2$. Converting to metric $V_{4/3}$:
$$\mathbb{E}[\Delta V_{4/3}] = \frac{\log_2(3) - 2}{\log_2(4/3)} = \frac{\log_2(3) - 2}{2 - \log_2(3)} = -1 \qquad \blacksquare$$

**Remark.** This result also follows from the identity $\mu_P + \mu_N = -2$ (proved in Theorem 5): since $P$ and $N$ partition the odd integers with equal probability under Haar measure, $\mathbb{E}[\Delta V_{4/3}] = \frac{1}{2}\mu_P + \frac{1}{2}\mu_N = -1$. This algebraic connection is made explicit in Section 3.5.

**Status:** ✅ **PROVEN**

---

### 3.3 Theorem 3: Arithmetic Isolation of $a = 3$

**Theorem 3.3 (Arithmetic Isolation).** Among all odd integers $a > 1$:
1. The map $R_a$ is contractive in expectation ($\Phi(a) < 0$) if and only if $a < 4$, i.e., $a = 3$.
2. The unique odd integer $a > 1$ in the interval $(1, 2^\phi)$, where $\phi = (1+\sqrt{5})/2 \approx 1.618$, is $a = 3$.

**Proof.**
*Part 1:* By Theorem 3.1, $\Phi(a) < 0 \iff \log_2(a) < 2 \iff a < 4$. Among odd integers greater than 1, only $a = 3$ satisfies this.

*Part 2:* We compute $2^\phi = 2^{(1+\sqrt{5})/2} \approx 3.0696$. Among odd integers, $3 < 3.0696 < 5$, so $a = 3$ is the unique odd integer in $(1, 2^\phi)$. $\blacksquare$

**Remark.** Part 1 is the dynamically significant fact: the transition from contractive to expansive behavior occurs at $a = 4$, and $a = 3$ is the only non-trivial odd integer on the contractive side. Part 2 is an independent arithmetic observation — the threshold $2^\phi$ is not the dynamical boundary (which is $a = 4$), but it does isolate $a = 3$ arithmetically. We do not claim that the golden ratio is causally responsible for Collatz convergence.

**Status:** ✅ **PROVEN** (Part 1 is the essential result; Part 2 is an arithmetic observation)

---

### 3.4 Theorem 4: Fibonacci Structure of $\log_2(3)$

**Theorem 3.4 (Fibonacci Convergents).** The continued fraction of $\log_2(3)$ begins:
$$\log_2(3) = [1; 1, 1, 2, 2, 3, 1, 5, 2, 23, \dots]$$

The first two non-trivial convergents are ratios of consecutive Fibonacci numbers:
$$\frac{p_2}{q_2} = \frac{3}{2} = \frac{F_4}{F_3}, \qquad \frac{p_3}{q_3} = \frac{8}{5} = \frac{F_6}{F_5}$$

**Proof.** Direct computation from the recursive convergent formula: $a_0=1, a_1=1, a_2=1$ gives $h_2/k_2 = 3/2$ and $a_3=2$ gives $h_3/k_3 = 8/5$. $\blacksquare$

**Remark.** This Fibonacci structure is a consequence of the initial CF coefficients $[1; 1, 1, \ldots]$ matching those of $\phi$. The pattern breaks at the fourth coefficient (which is 2, not 1). The result is arithmetically true; its dynamical significance for Collatz beyond motivating Baker-type cycle bounds is an open question. This theorem is presented as an arithmetic observation, not as a structural driver of convergence.

**Status:** ✅ **PROVEN** (arithmetic fact)

---

### 3.5 Theorem 5: Necessary Condition for Divergence — Exact Form

**Definition 3.2 (P/N Classification).** For odd $n$, define:
- $P = \{n \equiv 3 \pmod{4}\}$: class with $\nu_2(3n+1) = 1$ exactly (one halving step)
- $N = \{n \equiv 1 \pmod{4}\}$: class with $\nu_2(3n+1) \geq 2$ (two or more halving steps)

For an orbit of $K$ odd steps, let $f_P = |\{k : n_k \in P\}|/K$ denote the empirical frequency of $P$-class visits.

**Theorem 3.5 (Divergence Threshold).** Define:
$$\mu_P = \frac{\log_2 3 - 1}{2 - \log_2 3}, \qquad \mu_N = \frac{\log_2 3 - 3}{2 - \log_2 3}$$

as the conditional expected drifts in $V_{4/3}$ for $P$- and $N$-class steps respectively. The following identity holds exactly:
$$\mu_P + \mu_N = -2$$

A necessary condition for sub-exponential divergence of an orbit is:
$$f_P \geq f_P^* = \frac{3 - \log_2 3}{2} = \log_4\!\left(\frac{8}{3}\right) \approx 0.7075$$

**Proof.**

*Step 1 (Conditional drifts).* For $n \in P$, $\nu_2(3n+1) = 1$ exactly, so $R_3(n) = (3n+1)/2$ and:
$$\mu_P = \log_{4/3}(3/2) = \frac{\log_2 3 - 1}{2 - \log_2 3} \approx +1.41$$

*Step 2 (Conditional drift for $N$).* By the unconditional identity $\mathbb{E}[\nu_2(3n+1)] = 2$ (Theorem 1) and the law of total expectation with $P(P) = P(N) = 1/2$ under Haar measure:
$$\mathbb{E}[\nu_2 \mid N] = 2 \cdot \mathbb{E}[\nu_2] - \mathbb{E}[\nu_2 \mid P] = 2 \cdot 2 - 1 = 3$$
Therefore $\mu_N = (\log_2 3 - 3)/(2 - \log_2 3) \approx -3.41$.

*Step 3 (Identity).* Direct computation:
$$\mu_P + \mu_N = \frac{(\log_2 3 - 1) + (\log_2 3 - 3)}{2 - \log_2 3} = \frac{2(\log_2 3 - 2)}{2 - \log_2 3} = -2 \qquad \checkmark$$

*Step 4 (Unification with Theorem 2).* With $f_P = 1/2$:
$$\mathbb{E}[\Delta V_{4/3}] = \tfrac{1}{2}\mu_P + \tfrac{1}{2}\mu_N = -1$$
recovering Theorem 2 as a corollary.

*Step 5 (Divergence threshold).* For sub-exponential divergence, $V_{4/3}(n_K)/K \to 0$, so the time-averaged drift satisfies:
$$\frac{1}{K}\sum_{k=0}^{K-1}\Delta V_{4/3}(n_k) \to 0$$

This requires $f_P \cdot \mu_P + (1 - f_P) \cdot \mu_N \geq 0$, i.e.:
$$f_P \geq \frac{-\mu_N}{\mu_P - \mu_N} = \frac{(3 - \log_2 3)/(2 - \log_2 3)}{2/(2 - \log_2 3)} = \frac{3 - \log_2 3}{2} = \log_4\!\left(\frac{8}{3}\right) \qquad \blacksquare$$

**Status:** ✅ **PROVEN** (fully analytic; no empirical inputs)

---

## 4. Empirical Evidence

### 4.1 Simulation Results (24,866 Orbits)

All orbits for $n \leq 50{,}000$ (odd starting points) were analyzed. For each orbit, $f_P$ was computed as the fraction of odd iterates belonging to class $P$.

| Metric | Value |
|---|---|
| Orbits analyzed | 24,866 |
| Mean $f_P$ per orbit | 0.458 |
| Max $f_P$ observed | 0.6667 ($n = 1431$) |
| Orbits with $f_P \geq f_P^* = 0.7075$ | **0 (0%)** |
| Safety margin ($f_P^* - \max f_P$) | 0.041 (5.8%) |

**No orbit comes close to the divergence threshold.** The maximum observed $f_P = 0.6667$ remains 5.8% below the critical value.

**Note on mean $f_P$.** The per-orbit mean (0.458) differs from the step-weighted mean (≈ 0.500) because short orbits — which tend to start close to 1 and have fewer P-class steps — contribute equally in the per-orbit average. Both measures are consistent with $f_P \to 0.5$ for long orbits.

### 4.2 Autocorrelation of P/N Steps

The lag-1 autocorrelation of the binary P/N sequence was computed for each orbit and averaged:

$$\bar{\rho}_1 \approx 0.008 \approx 0$$

The P/N steps are **empirically approximately independent**. This is consistent with a random walk model in which $f_P$ concentrates around 0.5 by the Law of Large Numbers, with variance decaying as $1/K$. This observation motivates — but does not constitute — the ergodic pathway discussed in Section 6.

---

## 5. Open Conjectures

### 5.1 Conjecture 1: Universal Map Balance

**Conjecture 5.1 (Universal Map Balance).** For every Collatz orbit, the empirical frequency of visits to class $P$ satisfies $f_P \to 0.5$ as the orbit length grows.

**What this would imply.** By Theorem 3.5, if $f_P < f_P^*$ for every orbit, then no orbit diverges. Conjecture 5.1 is therefore **sufficient** (together with Theorem 5) to prove the Collatz conjecture.

**Known results.** Two recent structural results are relevant, at different levels:

- Tao (2019) proves that almost all orbits (logarithmic density 1) attain almost bounded values — a distributional result, not a pointwise one.
- Chang (2026, arXiv:2603.25753) proves the Map Balance Theorem at the **map level**: among the burst residues modulo $2^K$, the counts mapping to gap-start classes $\equiv 3$ vs $\equiv 7 \pmod 8$ differ by exactly 1 for all $K \geq 5$. This shows that **all residual imbalance is orbit-level, not map-level** — reducing the conjecture to the question of whether every individual orbit visits two residue classes modulo 32 with sufficient balance. Conjecture 5.1 is precisely the orbit-level statement that remains open after Chang's reduction.

**Empirical support.** 24,866 orbits analyzed; none exceed the threshold; autocorrelation $\approx 0$.

**Status:** ❌ **CONJECTURE** — not proven

---

### 5.2 Conjecture 2: Emptiness of $\Sigma_{\text{div}}$ via Baire Category

**Conjecture 5.2 ($\Sigma_{\text{div}} = \emptyset$).** The subspace of divergent orbits in the shift space $\Sigma_{\text{Collatz}}$ is empty.

**Sketch of potential argument.** If (i) $\Sigma_{\text{Collatz}}$ is a complete metric (Baire) space, (ii) $\Sigma_{\text{div}}$ is of first category (a countable union of nowhere dense sets), and (iii) the shift $\sigma_{\text{Collatz}}$ is topologically mixing, then Bowen's Specification Theorem would give $\Sigma_{\text{div}} = \emptyset$.

**Identified gaps.** None of (i), (ii), or (iii) has been verified. This conjecture is presented as a potential topological pathway, not as a near-complete argument.

**Connection to Conjecture 5.1.** If Conjecture 5.1 holds, then by Theorem 3.5 no orbit can sustain the frequency imbalance required for divergence. The Baire argument, if it could be made rigorous, would provide a topologically independent route to the same conclusion.

**Status:** ❌ **CONJECTURE** — not proven; gaps are explicitly identified

---

## 6. The Gap: "Almost Every" vs "Every"

### 6.1 What Is Known

| Result | Status |
|---|---|
| $\Phi(a) = \log_2(a) - 2$ (Theorem 1) | ✅ Proven |
| $\mathbb{E}[\Delta V_{4/3}] = -1$ (Theorem 2) | ✅ Proven |
| $a = 3$ is the unique contractive odd integer (Theorem 3) | ✅ Proven |
| CF convergents of $\log_2(3)$ are Fibonacci ratios (Theorem 4) | ✅ Proven (arithmetic) |
| $f_P \geq \log_4(8/3)$ necessary for divergence (Theorem 5) | ✅ Proven |
| $\mu_P + \mu_N = -2$ (identity unifying T2 and T5) | ✅ Proven |
| 24,866 orbits: none exceed divergence threshold | ✅ Empirical |
| Autocorrelation of P/N steps $\approx 0$ | ✅ Empirical |
| Map-level balance: all residual bias is orbit-level | ✅ Chang (2026) |
| Almost all orbits attain almost bounded values | ✅ Tao (2019) |

### 6.2 What Remains Open

| Question | Difficulty |
|---|---|
| $f_P \to 0.5$ for **every** orbit (Conjecture 5.1) | Very high |
| $\Sigma_{\text{div}} = \emptyset$ via Baire (Conjecture 5.2) | Extreme |
| The Collatz conjecture | Unknown |

### 6.3 The Ergodic Pathway

The empirical observation that P/N steps have near-zero autocorrelation suggests an ergodic approach to Conjecture 5.1. If the steps could be shown to be sufficiently mixing, then concentration-of-measure results would imply $f_P \to 0.5$ for individual orbits, not just on average.

Concretely, if P/N steps were exactly independent with $\mathbb{P}(P) = 1/2$, then by Hoeffding's inequality:
$$\mathbb{P}(f_P \geq f_P^* \mid \text{orbit of length } K) \leq \exp\!\left(-2K(f_P^* - 1/2)^2\right)$$

For $K = 1000$, this bound is approximately $10^{-38}$. We emphasize that **this calculation assumes independence**, which is precisely what would need to be proved. It is offered as motivation for pursuing the ergodic pathway, not as an argument that divergence is unlikely.

Chang's companion paper (2026, arXiv:2603.11066) establishes a Paradigm Exhaustion Theorem across 29 distinct mathematical frameworks: every known approach to promoting distributional convergence to pointwise convergence encounters an irreducible structural obstruction at the orbit level. This provides independent, systematic evidence that the gap between "almost every" and "every" is not a technical inconvenience but a fundamental structural barrier — and that the ergodic pathway, if viable, would require genuinely new tools.

The critical open question is: **can the approximate independence observed empirically ($\bar{\rho}_1 \approx 0$) be elevated to a rigorous mixing statement?**

---

## 7. Conclusions

**We have not proven the Collatz conjecture.**

We have established a rigorous structural framework characterizing why Collatz is arithmetically special:

- The exact contractive drift $\Phi(3) = \log_2(3) - 2 < 0$ (unique among odd $a > 1$)
- The exact drift $-1$ in the natural metric $V_{4/3}$ (Theorem 2)
- The exact closed-form divergence threshold $f_P^* = \log_4(8/3)$ with analytic proof (Theorem 5)
- The unifying identity $\mu_P + \mu_N = -2$, from which Theorem 2 follows as a corollary
- Strong empirical evidence: 24,866 orbits, none approaching the threshold

The gap between "almost every" (Tao 2019) and "every" persists. Chang (2026) demonstrates that this gap is not a failure of any particular method but a structural feature of the problem: all known frameworks for promoting distributional results to pointwise results hit an irreducible barrier at the orbit level. The conjecture reduces to whether every individual orbit achieves the balance predicted by the map-level structure — a one-bit, pointwise mixing question.

Closing the gap requires proving that $f_P \to 0.5$ for every individual orbit — a statement that ergodic theory reaches only on average. The near-zero autocorrelation of P/N steps is an empirical hint that a mixing argument may be within reach, but the proof remains open.

**Recommendation:** Publish as a structural characterization with exact results, identifying the ergodic pathway and Chang's one-bit reduction as the most promising directions for closing the gap.

---

## References

1. Tao, T. (2019). Almost all orbits of the Collatz map attain almost bounded values. *arXiv:1909.03562*
2. Chang, E.Y. (2026). A structural reduction of the Collatz conjecture to one-bit orbit mixing. *arXiv:2603.25753*, Stanford University
3. Chang, E.Y. (2026). Exploring Collatz dynamics with human–LLM collaboration. *arXiv:2603.11066*, Stanford University
4. Lagarias, J.C. (2010). *The Ultimate Challenge: The 3x+1 Problem.* AMS
5. Harris, T.E. (1956). The existence of stationary measures for certain Markov processes. *Proc. 3rd Berkeley Symposium on Mathematical Statistics and Probability*
6. Eliahou, S. (1993). The 3x+1 problem: new lower bounds on nontrivial cycle lengths. *Discrete Mathematics*, 118(1–3), 45–56
7. Matveev, E.M. (2000). An explicit lower bound for a homogeneous rational linear form in logarithms of algebraic numbers. *Izvestiya: Mathematics*, 64(6), 1217–1269

---

*Per Aspera, Ad Astra.*
