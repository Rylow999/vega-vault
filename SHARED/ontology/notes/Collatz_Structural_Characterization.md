---
ontology_id: pape_9f418cc9
type: Paper
title: Collatz_Structural_Characterization
tags: []
---
# Collatz_Structural_Characterization

**Ontology ID**: `pape_9f418cc9`
**Type**: Paper

**authors**: ['Luciano Benjamín Nieto']
**year**: 2026
**venue**: Technical Report
**doi**: 
**url**: 
**summary**: # Structural Characterization of the Collatz Map: Drift, Divergence Threshold, and the Baire Gap

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Researcher, General Alvear, Mendoza, Argentina  
**Date:** June 29, 2026  
**Version:** v3 (corrected attribution of Chang 2026)  
**Status:** Research Paper — Rigorous Results and Open Conjectures

---

## Abstract

We present a structural characterization of the Collatz map through five rigorous results and two open conjectures. We prove: (1) the exact 2-adic drift formula $\Phi(a) = \log_2(a) - 2$; (2) the exact drift $-1$ in the natural metric $V_{4/3}(n) = \log_{4/3}(n)$; (3) the arithmetic isolation of $a=3$ as the unique non-trivial odd integer satisfying $\Phi(a) < 0$ and $a < 2^\phi$; (4) the Fibonacci structure of $\log_2(3)$ convergents; and (5) a necessary condition for divergence with exact closed-form threshold $f_P \geq f_P^* = \log_4(8/3) = (3 - \log_2 3)/2 \approx 0.7075$, where $f_P$ is the frequency of vis
**tags**: []

---

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

*Step 2 (Conditional drift for $N$).* By the unconditional identity $\mathbb{E}[\nu_2(3n+1)] = 2$ (Theor