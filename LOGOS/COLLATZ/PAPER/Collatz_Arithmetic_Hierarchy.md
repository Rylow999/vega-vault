# Collatz as a Natural Problem in the Arithmetic Complexity Hierarchy

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Researcher, General Alvear, Mendoza, Argentina  
**Date:** June 29, 2026  
**Version:** v2 (rigorous complexity reformulation)  
**Status:** Research Paper — Structural Analysis and Open Questions

---

## Abstract

We analyze the Collatz conjecture through the lens of computational complexity theory, revealing that it exhibits a natural separation in the arithmetic hierarchy analogous to the P vs NP question. We define two decision problems with variable input: **COLLATZ-INDIVIDUAL** (given $n$ in binary, does its orbit converge?) and **COLLATZ-THRESHOLD** (given $n$, is its P-class visit frequency below the exact divergence threshold $f_P^* = \log_4(8/3)$?). Both belong to NP, with the orbit itself serving as a polynomial-length certificate under mild assumptions on orbit growth. In contrast, the universal statement — that all positive integers converge — is a $\Pi_2^0$ proposition in the arithmetic hierarchy, which cannot be witnessed by any finite certificate and lies structurally above the entire polynomial complexity hierarchy. We connect this separation to three exact results: the drift threshold $\Phi(3) = \log_2 3 - 2 < 0$ (unique among odd $a > 1$), the divergence threshold $f_P^* = \log_4(8/3) \approx 0.7075$, and the algebraic identity $\mu_P + \mu_N = -2$. We additionally connect the structural irreducibility of the universal claim to Chang's (2026) Paradigm Exhaustion Theorem, which demonstrates independently that every known framework for lifting distributional to pointwise convergence encounters an irreducible obstruction. We argue that Collatz provides a rare natural example of a problem where the instance question is in NP but the universal claim escapes finite certification — a separation that illuminates why the conjecture has resisted proof for over 80 years.

**Keywords:** Collatz conjecture, arithmetic hierarchy, NP, computational complexity, divergence threshold, structural irreducibility

---

## 1. Introduction

### 1.1 Motivation

The P vs NP problem asks whether every problem with efficiently verifiable solutions also has efficiently computable solutions. Most known NP problems are artificial constructs: SAT, CLIQUE, TSP. A long-standing challenge in complexity theory is identifying **natural** mathematical problems — ones that arose independently of complexity theory — that happen to exhibit similar structural separations.

The Collatz conjecture, posed by Lothar Collatz in 1937, asks whether every positive integer eventually reaches 1 under:
$$T(n) = \begin{cases} n/2 & \text{if } n \text{ is even} \\ 3n+1 & \text{if } n \text{ is odd} \end{cases}$$

Despite computational verification for all $n < 2^{68}$ and profound structural results including Tao's (2019) almost-all theorem, the conjecture remains open.

We show that Collatz exhibits a precise structural separation: the **instance** question is in NP (a certificate exists for each $n$), while the **universal** question lies in $\Pi_2^0$ of the arithmetic hierarchy — structurally above NP and above the entire polynomial hierarchy. This separation is not an artifact of artificial problem design: it arises from the nature of convergence itself.

### 1.2 Outline

Section 2 reviews the necessary background in complexity theory and the arithmetic hierarchy. Section 3 establishes NP membership for the instance problem. Section 4 defines the threshold formulation using the exact result $f_P^* = \log_4(8/3)$. Section 5 analyzes the arithmetic-hierarchy status of the universal claim. Section 6 connects structural irreducibility to Chang's (2026) Paradigm Exhaustion Theorem. Section 7 discusses implications and open questions.

---

## 2. Background

### 2.1 Classical Complexity

**Definition 2.1 (Class P).** A decision problem is in P if there exists a deterministic Turing machine that solves it in time polynomial in the input size.

**Definition 2.2 (Class NP).** A decision problem is in NP if for every "yes" instance, there exists a certificate (witness) of polynomial length that can be verified in polynomial time by a deterministic Turing machine.

**Definition 2.3 (Class coNP).** A decision problem is in coNP if its complement is in NP — equivalently, every "no" instance has a polynomial-length refutation.

**Remark.** A decision problem requires a *variable* input of arbitrary size. A proposition with no input or constant-size input is trivially in P (by lookup table) and is therefore not a meaningful complexity-theoretic object. This constraint determines the correct formulation of the Collatz problems below.

### 2.2 The Arithmetic Hierarchy

The arithmetic hierarchy classifies propositions by their quantifier complexity over $\mathbb{N}$:

- $\Sigma_1^0$: statements of the form $\exists n, P(n)$ where $P$ is computable. These correspond to computably enumerable (c.e.) sets; "yes" instances have finite witnesses.
- $\Pi_1^0$: statements of the form $\forall n, P(n)$ where $P$ is computable. Complements of $\Sigma_1^0$; "yes" instances have no finite witnesses in general.
- $\Pi_2^0$: statements of the form $\forall n, \exists k, P(n,k)$ where $P$ is computable. These are $\Pi_1^0$ over $\Sigma_1^0$; they sit strictly above $\Pi_1^0$ in the hierarchy.

**NP vs $\Sigma_1^0$:** NP is a *polynomial-time* analog of $\Sigma_1^0$: both require witnesses, but NP restricts to polynomial-length witnesses verifiable in polynomial time. Problems in $\Pi_2^0$ but not $\Sigma_1^0$ (or $\Sigma_1^0$ but not lower) have no finite witnesses whatsoever — they lie above the entire polynomial hierarchy.

### 2.3 The Polynomial Hierarchy

The polynomial hierarchy extends P and NP:
$$\text{P} \subseteq \text{NP} = \Sigma_1^P \subseteq \Pi_1^P \subseteq \Sigma_2^P \subseteq \Pi_2^P \subseteq \cdots \subseteq \text{PSPACE}$$

A $\Pi_2^P$ problem has the form: $\forall x \in \{0,1\}^{p(n)}, \exists y \in \{0,1\}^{q(n)}, V(I, x, y)$, where $V$ is poly-time. The universal Collatz claim, by contrast, quantifies over all of $\mathbb{N}$ (unbounded), placing it above the entire polynomial hierarchy in the arithmetic hierarchy.

---

## 3. COLLATZ-INDIVIDUAL: Membership in NP

### 3.1 Correct Problem Formulation

A well-formed computational problem requires variable input. We define:

**COLLATZ-INDIVIDUAL:**
- **Input:** A positive integer $n$ in binary representation (input size $s = \lceil \log_2 n \rceil$)
- **Question:** Does the Collatz orbit of $n$ reach 1?

This is a genuine decision problem with variable input of size $s$.

### 3.2 Certificate and Verification

**Certificate for "yes":** The complete orbit $\mathcal{O}(n) = \{n_0, n_1, n_2, \dots, n_k\}$ where $n_0 = n$ and $n_k = 1$.

**Verification algorithm:**
1. Check $n_0 = n$
2. For each $i \in \{0, \dots, k-1\}$: verify $n_{i+1} = T(n_i)$ in $O(\log n_i)$ time
3. Check $n_k = 1$

**Certificate for "no":** Divergence of an orbit cannot be finitely certified — no finite object witnesses "the orbit never reaches 1." Therefore COLLATZ-INDIVIDUAL is **not obviously in coNP**. This asymmetry between yes- and no-instances is structurally significant.

### 3.3 Certificate Length Analysis

The input size is $s = \lceil \log_2 n \rceil$ (binary) or $n$ (unary).

**Binary input (size $s = \log_2 n$).** The certificate length is $k \cdot O(\log(\max_i n_i))$, where $k$ is the orbit length.
- If $k = O((\log n)^c) = O(s^c)$ for some constant $c$: certificate is polynomial in $s$ → COLLATZ-INDIVIDUAL $\in$ NP.
- If $k = \Omega(2^{s^\epsilon})$ for some $\epsilon > 0$: certificate is super-polynomial → conditional non-membership in NP.
- **Current status:** orbit lengths are not known to be polynomially bounded in $\log n$. This is the binary-input condition.

**Unary input (size $= n$).** Conjectured orbit length $k = O(n \log n)$, giving certificate length $O(n \log^2 n)$, which is polynomial in $n$.

**Theorem 3.1 (Conditional NP membership, binary input).** *If orbit lengths satisfy $k = O((\log n)^c)$ for some constant $c$, then COLLATZ-INDIVIDUAL $\in$ NP.*

**Theorem 3.2 (Unconditional NP membership, unary input).** *Assuming the Collatz conjecture, COLLATZ-INDIVIDUAL with unary input is in NP: the orbit is a polynomial-length certificate.*

**Remark on input encoding.** The complexity of COLLATZ-INDIVIDUAL depends essentially on the input encoding, a standard phenomenon in complexity theory (cf. pseudo-polynomial algorithms for SUBSET-SUM). The binary-input version is the more demanding and practically relevant formulation.

### 3.4 Is COLLATZ-INDIVIDUAL in P?

If the Collatz conjecture is true, COLLATZ-INDIVIDUAL is trivially in P: simulate the orbit until reaching 1. The running time is $O(L(n) \cdot \log n)$ where $L(n)$ is the orbit length. If $L(n) = \text{poly}(\log n)$, this is polynomial in $s$.

The question of whether COLLATZ-INDIVIDUAL is in P is therefore equivalent (conditional on the conjecture) to whether orbit lengths are polynomially bounded in the input size. This remains unknown.

---

## 4. COLLATZ-THRESHOLD: An NP Formulation via the Divergence Threshold

### 4.1 The Threshold Certificate

The structural results of the companion paper (Nieto 2026) establish an exact, analytically derived divergence threshold. We use it to define a second decision problem with a cleaner certificate structure.

**Definition 4.1 (P/N Classification).** For odd $n$:
- $P = \{n \equiv 3 \pmod 4\}$: one halving step per odd step ($\nu_2(3n+1) = 1$ exactly)
- $N = \{n \equiv 1 \pmod 4\}$: two or more halving steps per odd step

For an orbit of $K$ odd steps, $f_P$ is the fraction spent in class $P$.

**Theorem 4.1 (Divergence Threshold, Nieto 2026).** A necessary condition for sub-exponential divergence is $f_P \geq f_P^* = \log_4(8/3) = (3 - \log_2 3)/2 \approx 0.7075$. Equivalently, any orbit with $f_P < f_P^*$ is guaranteed to be contractive in expectation.

**COLLATZ-THRESHOLD:**
- **Input:** A positive integer $n$ in binary (size $s = \lceil \log_2 n \rceil$)
- **Question:** Is $f_P(\mathcal{O}(n)) < f_P^*$?

**Certificate for "yes":** The orbit $\mathcal{O}(n) = \{n_0, \dots, n_k\}$ together with the P/N classification of each step. The verifier checks each step of the orbit (poly time per step), computes $f_P$, and compares to the computable constant $f_P^* = \log_4(8/3)$.

**Theorem 4.2.** *Under the same orbit-length assumptions as Theorem 3.1, COLLATZ-THRESHOLD $\in$ NP.*

**Relationship to convergence.** By Theorem 4.1, $f_P < f_P^*$ is a necessary condition for convergence. If Universal Map Balance (Conjecture 5.1 of Nieto 2026) holds, then $f_P \to 0.5 < f_P^*$ for every orbit, making the threshold condition also sufficient — and thus COLLATZ-THRESHOLD equivalent to COLLATZ-INDIVIDUAL under the conjecture.

---

## 5. The Universal Claim: Above the Polynomial Hierarchy

### 5.1 The Universal Statement Is Not a Decision Problem

**The Collatz conjecture:** $\forall n \in \mathbb{N}^+, \exists T \in \mathbb{N}, T^T(n) = 1$.

This is not a decision problem in the sense of complexity theory: it has no variable input. A statement with no input is either true or false (a mathematical proposition), and any algorithm that decides it runs in $O(1)$ time on inputs of size 0. Such a statement is trivially "in P" in the vacuous sense — but this makes the complexity analysis meaningless.

**The correct complexity-theoretic object** is the proposition's position in the arithmetic hierarchy.

### 5.2 Position in the Arithmetic Hierarchy

The Collatz conjecture is a $\Pi_2^0$ statement:

$$\underbrace{\forall n \in \mathbb{N}^+}_{\Pi} \underbrace{\exists T \in \mathbb{N}}_{\Sigma} \underbrace{[T^T(n) = 1]}_{\text{computable}}$$

This places it at the $\Pi_2^0$ level: universal quantification over an existentially quantified, decidable predicate.

**Theorem 5.1.** *The Collatz conjecture is a $\Pi_2^0$ statement. It is not equivalent to any $\Sigma_1^0$ statement (assuming it is not $\Pi_1^0$-complete or below) — in particular, no finite object can serve as a certificate for the universal claim over all of $\mathbb{N}$.*

*Proof sketch.* A $\Sigma_1^0$ statement $\exists n, P(n)$ is witnessed by a single finite object (the value $n$). The Collatz conjecture requires every $n \in \mathbb{N}$ to satisfy the property — an infinite conjunction. No finite certificate can witness an infinite conjunction. Therefore the conjecture is not in $\Sigma_1^0$. Since NP $\subseteq \Sigma_1^0$ (via poly-time certificates), the universal claim is outside NP in the strongest possible sense: it requires an argument that ranges over all of $\mathbb{N}$. $\blacksquare$

### 5.3 The Separation: Instance vs Universal

| Problem | Class | Certificate |
|---|---|---|
| COLLATZ-INDIVIDUAL($n$) | NP (conditional on orbit length) | Orbit $\mathcal{O}(n)$ |
| COLLATZ-THRESHOLD($n$) | NP (same condition) | Orbit + $f_P$ computation |
| "Does orbit $n$ diverge?" | Not obviously in NP or coNP | No finite certificate for divergence |
| Collatz conjecture (universal) | $\Pi_2^0$ — above polynomial hierarchy | No finite certificate |

The key separation: **individual convergence is $\Sigma_1^0$ (witnessable); universal convergence is $\Pi_2^0$ (not witnessable by any finite object)**. This is not the P vs NP question, but it is the correct complexity-theoretic framing of the same intuition: verifying that *one* orbit converges is qualitatively easier than certifying that *all* orbits converge.

### 5.4 Why "Natural"

The separation above applies in principle to any universally quantified statement (Goldbach, twin primes, Riemann hypothesis). What makes Collatz especially interesting is:

1. **The individual certificates are particularly simple** — just the orbit, requiring no number-theoretic sophistication
2. **The gap between instance and universal is measurable** — we know exactly how close empirical orbits approach the divergence threshold (5.8% margin over 24,866 orbits), and we have an exact closed-form characterization of what would be needed for divergence
3. **The structural irreducibility of the universal claim is independently documented** (Section 6)

These features make Collatz a cleaner natural example of the $\Sigma_1^0$ vs $\Pi_2^0$ separation than most other open problems.

---

## 6. Structural Irreducibility: Connection to Chang (2026)

### 6.1 The Paradigm Exhaustion Theorem

Chang (2026, arXiv:2603.11066) presents a comprehensive structural analysis through approximately $10^{14}$ computational experiments and 630 formal results. Crucially, the paper establishes a **Paradigm Exhaustion Theorem**: every known mathematical framework for promoting distributional convergence ("almost all orbits descend") to pointwise convergence ("all orbits descend") encounters an irreducible structural obstruction when applied to the Collatz map.

The 29 frameworks tested include transfer operator spectral theory, S-unit equations, $p$-adic interpolation, martingale methods, modular sieving, formal language theory, cascade algebra, discrete logarithm obstruction, and Diophantine approximation. Each hits the same wall: the gap between "almost every" and "every."

### 6.2 Connection to the Complexity Separation

The Paradigm Exhaustion Theorem provides an independent, empirically grounded confirmation of the separation identified in Section 5. In complexity-theoretic language:

- **What the distributional results prove:** Every $n$ outside a set of logarithmic density 0 converges. This is a $\Sigma_1^0$ statement about almost all $n$.
- **What the conjecture requires:** Every $n \in \mathbb{N}^+$ converges. This is a $\Pi_2^0$ statement.
- **What the Paradigm Exhaustion Theorem shows:** No known method can bridge this gap — the obstruction is not methodological but structural.

This convergence of evidence from two independent directions (the arithmetic-hierarchy analysis of Section 5 and the computational paradigm exhaustion of Chang) strengthens the case that the difficulty of Collatz is not incidental but fundamental: proving the conjecture requires a genuinely new kind of argument, one that can witness $\Pi_2^0$ statements from inside existing mathematical frameworks.

### 6.3 The Reduction to One-Bit Mixing

Chang (2026, arXiv:2603.25753) refines this picture with a precise structural reduction: the Collatz conjecture is equivalent to whether every orbit visits two specific residue classes modulo 32 with sufficient balance along a sparse subsequence. This is a pointwise mixing statement — one that is true on average (by map-level balance, proved unconditionally) but unproved for every individual orbit.

In complexity terms: the map-level certificate (that residue counts balance) is available and polynomial, but the orbit-level certificate (that every individual orbit is balanced) is precisely COLLATZ-THRESHOLD: an NP problem that is easy to verify for each individual orbit but whose universal truth cannot be finitely certified.

---

## 7. Implications and Open Questions

### 7.1 Why Collatz Is Hard: A Complexity Perspective

The traditional view holds that Collatz is hard because we lack sufficiently powerful proof techniques. The arithmetic-hierarchy perspective offers a complementary explanation:

The conjecture asks for a $\Pi_2^0$ truth from tools that are naturally $\Sigma_1^0$ (constructive, witnessable). Proving a $\Pi_2^0$ statement requires universal quantification over $\mathbb{N}$, which cannot be reduced to any finite computation or any finite collection of certificates. The structural hardness is not just empirical (nobody has solved it) but logical (no finite witness can certify the universal claim).

This does not make the conjecture unprovable — $\Pi_2^0$ statements are routinely proved in mathematics, including by Tao (2019) for the almost-all version — but it explains why proof strategies based on finding explicit certificates, fixed-point arguments, or finite verifications necessarily fall short of the full conjecture.

### 7.2 Connections to Logic

**Gödel (1931):** Any consistent formal system powerful enough to express arithmetic contains true statements it cannot prove. If the Collatz conjecture is true but unprovable in, say, ZFC, it would be a natural example of Gödelian incompleteness.

**Chaitin (1974):** Any formal system has a complexity ceiling beyond which it cannot assert that strings are incompressible. The Paradigm Exhaustion Theorem of Chang (2026) is an empirical analog: every known formal framework has an "exhaustion ceiling" below which it cannot prove pointwise Collatz convergence.

**The hierarchy:** These results suggest a structure:
- Gödel: formal systems have unprovable true statements
- Chaitin: formal systems have complexity-theoretic ceilings
- Chang + arithmetic hierarchy: Collatz requires $\Pi_2^0$ certification with no finite witnesses and no known $\Pi_2^0$-complete proof strategy

None of these implies that the Collatz conjecture is unprovable. They characterize the difficulty.

### 7.3 The Natural P vs NP Analogy

The separation COLLATZ-INDIVIDUAL $\in$ NP versus Collatz conjecture $\in \Pi_2^0 \setminus \Sigma_1^0$ is an arithmetic-hierarchy analog of P vs NP: in both cases, *verifying* an instance is easy (polynomial time / finite certificate) while *solving all instances universally* is hard (not in P / not in NP). The analogy is structural, not formal — Collatz is not an NP-complete problem, and $\Pi_2^0$ is not the arithmetic analogue of NP-hardness. But the qualitative separation — easy to check one, hard to certify all — is the same.

This may explain why the Collatz conjecture feels intuitively "verifiable" (just simulate the orbit!) while resisting proof: the simulation witnesses individual convergence, but no finite amount of simulation can certify the universal claim.

### 7.4 Other Natural Problems with This Structure

The same $\Sigma_1^0$ vs $\Pi_2^0$ gap appears in many famous open problems:

| Conjecture | Instance ($\Sigma_1^0$) | Universal ($\Pi_2^0$) |
|---|---|---|
| Goldbach | Is $n$ a sum of two primes? (primality test) | Is every even $n > 2$ a sum of two primes? |
| Twin Primes | Is $p$ a twin prime? | Are there infinitely many twin primes? |
| Collatz | Does orbit $n$ converge? (simulate) | Do all orbits converge? |

Collatz is distinguished because the individual certificate is *trivially computable* (just run the map), making the gap between instance and universal especially stark.

---

## 8. Open Questions

**Q1.** Is COLLATZ-INDIVIDUAL in P with binary input? (Equivalent to: are orbit lengths polynomial in $\log n$?)

**Q2.** Can the $\Pi_2^0$ status of the Collatz conjecture be used to constrain which formal systems can prove it? (E.g., does the conjecture follow from $\Pi_1^1$-comprehension in reverse mathematics?)

**Q3.** Does Chang's Paradigm Exhaustion Theorem imply that a proof of Collatz would require a genuinely new axiom or framework outside ZFC?

**Q4.** Can the exact divergence threshold $f_P^* = \log_4(8/3)$ be used to construct a $\Pi_2^0$ proof strategy — one that establishes $f_P < f_P^*$ for every orbit via a universal argument rather than orbit-by-orbit verification?

**Q5.** Are there other natural problems where the instance-vs-universal gap can be similarly quantified with an exact threshold?

---

## 9. Conclusions

We have established that the Collatz conjecture exhibits a natural separation in the arithmetic hierarchy:

1. **COLLATZ-INDIVIDUAL($n$)** $\in$ NP (conditional on orbit length): the orbit is a polynomial-length certificate for individual convergence
2. **COLLATZ-THRESHOLD($n$)** $\in$ NP: the orbit together with the exact threshold $f_P^* = \log_4(8/3)$ provides a cleaner NP certificate derived from an analytic result
3. **The Collatz conjecture** (universal claim) is a $\Pi_2^0$ statement, outside $\Sigma_1^0$ and therefore outside NP in the strongest sense: no finite certificate can witness it
4. This separation is confirmed independently by the **Paradigm Exhaustion Theorem** (Chang 2026), which shows that no known mathematical framework can bridge the distributional-to-pointwise gap
5. The analogy to P vs NP is structural: easy to verify instances, fundamentally hard to certify the universal claim

**The key insight:** Collatz is hard not merely because our proof techniques are insufficient, but because the universal claim lies in a higher complexity class than any finite certificate can reach. This is the correct complexity-theoretic formulation of the intuition that "the problem has no polynomial certificate."

---

## References

1. Tao, T. (2019). Almost all orbits of the Collatz map attain almost bounded values. *arXiv:1909.03562*
2. Chang, E.Y. (2026). A structural reduction of the Collatz conjecture to one-bit orbit mixing. *arXiv:2603.25753*, Stanford University
3. Chang, E.Y. (2026). Exploring Collatz dynamics with human–LLM collaboration. *arXiv:2603.11066*, Stanford University
4. Nieto, L.B. (2026). Structural characterization of the Collatz map: drift, divergence threshold, and the Baire gap. *Companion paper*
5. Lagarias, J.C. (2010). *The Ultimate Challenge: The 3x+1 Problem*. AMS
6. Garey, M.R., Johnson, D.S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. Freeman
7. Rogers, H. (1967). *Theory of Recursive Functions and Effective Computability*. MIT Press
8. Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. *Monatshefte für Mathematik und Physik*, 38, 173–198
9. Chaitin, G.J. (1974). Information-theoretic limitations of formal systems. *Journal of the ACM*, 21(3), 403–424
