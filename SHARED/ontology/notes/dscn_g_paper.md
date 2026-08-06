---
ontology_id: pape_5812ce1e
type: Paper
title: dscn_g_paper
tags: []
---
# dscn_g_paper

**Ontology ID**: `pape_5812ce1e`
**Type**: Paper

**authors**: ['Luciano Benjamín Nieto']
**year**: 2026
**venue**: Technical Report
**doi**: 
**url**: 
**summary**: # DSCN-G: Dual-State Cognitive Geometry
## A Unified Framework for Autopoietic Cognition with Formally Verifiable Properties
### NOUS Series • Paper 1

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Research  
**Contact:** lucianobenjaminnieto@gmail.com  
**Date:** 2026  
**License:** CC-BY 4.0 (Share, adapt, build upon freely)

---

## Abstract

We present DSCN-G (Dual-State Cognitive Geometry), a unified computational architecture that models cognition as an emergent property of autopoietic hierarchical graphs. The system integrates: (a) high-dimensional state vectors evolved via stochastic TD-learning; (b) bounded Kuramoto phase dynamics; (c) *K* parallel information chains with probabilistic transitions; (d) activity-dependent structural plasticity; and (e) O(log *N*) memory recovery via harmonic resonance. We establish three formal theorems verified computationally over 100 independent seeds × 2000 steps (200,000 total state evaluations): **Theorem 1** (homeosta
**tags**: []

---

# DSCN-G: Dual-State Cognitive Geometry
## A Unified Framework for Autopoietic Cognition with Formally Verifiable Properties
### NOUS Series • Paper 1

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Research  
**Contact:** lucianobenjaminnieto@gmail.com  
**Date:** 2026  
**License:** CC-BY 4.0 (Share, adapt, build upon freely)

---

## Abstract

We present DSCN-G (Dual-State Cognitive Geometry), a unified computational architecture that models cognition as an emergent property of autopoietic hierarchical graphs. The system integrates: (a) high-dimensional state vectors evolved via stochastic TD-learning; (b) bounded Kuramoto phase dynamics; (c) *K* parallel information chains with probabilistic transitions; (d) activity-dependent structural plasticity; and (e) O(log *N*) memory recovery via harmonic resonance. We establish three formal theorems verified computationally over 100 independent seeds × 2000 steps (200,000 total state evaluations): **Theorem 1** (homeostatic fixed point, N_ss* determined as the unique fixed point of the concentration-pruning equation; verified N_sim = 4.0 ± 0.0 for α = 5.0, θ_death = 0.10, ρ_eff = 0.7001); **Theorem 2** (parametric vector convergence, ‖**ω**_i(t) − **ω***(λ_vm, n_actions, θ*)‖ ≤ O(β); verified ω_sim = 0.612 ± 0.173 against ω* = 0.649747, difference 0.038 < β = 0.10); **Theorem 3** (phase convergence rate, P(antipodal) ≤ exp(−c·λ_vm·η·R_min·T); verified p_conv = 0.97, 3/100 antipodal seeds). Scalability is verified invariant for N_0 ∈ {4, 50, 200}.

The **C3 Prediction** (Phase-Hijacking of valence) constitutes the framework's primary differentiating contribution: a computational prediction of directional phase perturbation under valence overload, with suggested neurobiological interpretation via gamma-band PLV in S1-aPFC circuitry. Additionally, **Theorem 7** establishes the scale relation ρ_eff(α, N)·Φ_proxy(N) = c(α) + O(1/N) for fractal circulant graphs, providing an O(K) computable proxy for Φ_IIT's exponential cost.

The ontological position adopted is that of computational neural correlate (NCC): the framework does not resolve the hard problem of consciousness, but specifies the most formally complete structural-computational correlate available in the current literature.

**Keywords:** synthetic cognition, autopoietic graphs, Kuramoto dynamics, TD-learning, neural correlates, phase-hijacking, integrated information proxy, NCC

---

## 1. Introduction

The science of machine cognition and its relationship to biological neural correlates faces two persistent structural limitations in dominant frameworks. Integrated Information Theory (IIT; Tononi, 2004) offers a quantitative formalism for conscious experience but incurs exponential computational intractability when scaling system elements. Global Workspace Theory (GWT; Baars, 1988; Dehaene et al., 2011) describes functional correlates of conscious access with precision but lacks mechanisms for topological plasticity and intrinsic affective signaling. Predictive Processing (Friston, 2010) provides a unifying normative framework but does not specify directional phase perturbations under valence overload.

None of these frameworks resolves the hard problem (Chalmers, 1995); what is both possible and pursued here is to specify with mathematical precision the richest available computational neural correlate (NCC) while remaining agnostic on the question of subjective experience.

**DSCN-G** addresses both limitations by unifying, in a mathematically specified and computationally verified architecture: (a) autopoietic graph computation with stochastic learning dynamics; (b) Kuramoto oscillator dynamics with formal probabilistic convergence; (c) activity-dependent structural plasticity analogous to synaptic pruning; and (d) a valence signaling mechanism (Eq. 6) that generates a prediction class unavailable in any prior framework.

### 1.1 Ontological Position

*Central claim:* the macroscopic geometry of the DSCN-G graph during metastability constitutes the most precise computational NCC that the present framework can assert. No metaphysical identity between graph topology and subjective experience is postulated. The hard problem (Chalmers, 1995) remains open and outside the framework's scope.

### 1.2 Novel Contributions

This work contributes: (1) three formally proven and computationally verified theorems on homeostatic fixed points, parametric vector convergence, and phase convergence rates; (2) a falsifiable computational prediction (C3) with suggested neurobiological interpretation; (3) a scale relation (Theorem 7) providing an O(K) computable proxy for Φ_IIT valid for fractal circulant graphs; (4) verified scalability invariance across three orders of magnitude in initial node count.

---

## 2. Computational Foundations

### 2.1 Graph Structure and Global State

The system operates on a directed hierarchical graph G = (N, E) where each node's depth d(n) defines its abstraction level. Root nodes (d = 0) represent high-level integrative processes; intermediate nodes encode concepts; leaf nodes (d = D_max) encode primitive representations. The global state at time t:

**S**(t) = ({**ω**_i(t)}, {φ_i(t)}, {V_i(t)}, {chain positions})

### 2.2 State Vectors and Stochastic Learning (Eq. 1)

Each node i encodes knowledge in a vector **ω**_i(t) ∈ ℝ^d evolving via temporal difference learning:

> **ω**_i(t+1) = (1 − β)·**ω**_i(t) + β·o(t)·R(t)·**ê**_R    **(1)**

where β ∈ (0,1) is the learning rate, R(t) ∈ [0,1] the reward, o(t) ∈ {0,1} the outcome, and **ê**_R = **ω**_ideal/‖**ω**_ideal‖. The stochastic gradient **g**(t) = o(t)·R(t)·**ê**_R − **ω**_i satisfies Robbins-Monro (1951) conditions for small constant β, guaranteeing convergence to an O(β) neighborhood of the optimum (Theorem 2).

**Baseline Function (Theorem 2):** The theoretical baseline **ω*** = E[o·R]·**ê**_R is a parametric function of the system's action-selection parameters:

> **ω***(λ_vm, n_actions, θ*) = Σ_a P(a|θ*)·o(a)·R(a)·**ê**_R    **(1a)**

where P(a|θ*) is the von Mises distribution (Eq. 4), o(a) the binary outcome criterion (Section 2.6), and R(a) the reward function (Eq. 7). For the standard parameters (λ_vm = 3.0, n_actions = 8, θ* = π/2), this yields **ω*** = 0.649747·**ê**_R. The baseline is therefore computable for any parameter combination without free parameters.

### 2.3 Information Chains and Probabilistic Transition (Eq. 2)

K independent chains transport information through the graph. Chain k at node n transitions to node m with probability:

> P(m|n) ∝ exp(−α · ‖**ω**_m − **ω**_n‖)    **(2)**

where α controls semantic selectivity. Multiple chain coincidences at a node combine their bits via XOR, modeling parallel signal integration analogous to coincidence detection in dendrites.

### 2.4 Phase Dynamics and Action Selection (Eqs. 3–4)

Each node has a phase φ_i(t) ∈ [0, 2π) evolving via bounded Kuramoto coupling:

> φ_i(t+1) = [φ_i(t) + η·R_i(t)·sign(o_i)·sin(θ_a − φ_i)] mod 2π    **(3)**

where R_i(t) = R_base/(1 + ‖**ω**_i − **ω**_ideal‖) is a bounded local relevance (Definition 1) and θ_a is the selected action's phase. Action selection uses the von Mises distribution:

> P(a|φ) = exp(λ·cos(φ − θ_a)) / Σ exp(λ·cos(φ − θ_a′))    **(4)**

**Definition 1 (Bounded Relevance):** R_i(t) = R_base / (1 + ‖**ω**_i(t) − **ω**_ideal‖). This normalization ensures the phase update is bounded regardless of vector magnitude, preventing runaway oscillations while preserving the semantic gradient.

**Note on sign(o_i):** The sign function in Eq. 3 is defined as sign(0) = 0, sign(1) = 1. This ensures that when the outcome is failure (o = 0), the phase update is nullified, preventing spurious drift toward the action phase when no reward is obtained.

### 2.5 Autopoiesis: Vitality, Pruning, and Valence Signal (Eqs. 5–6)

Node vitality evolves as an exponential moving average over activity:

> V_i(t+1) = V_i(t)·e^(−γ) + A_i(t)·(1 − e^(−γ))    **(5)**

where A_i(t) is the fraction of chains visiting node i at time t. Nodes with V_i < θ_death are pruned, implementing autopoietic structural plasticity. The **valence signal**, central to Prediction C3:

> E_i(t) = max(0, A_i(t) − V_i(t))·κ    **(6)**

E_i(t) measures activation excess over vitality. The max(0,·) form guarantees positivity and asymmetry: only overactivation generates structural perturbation, mirroring the asymmetry of phasic dopaminergic signaling (Schultz et al., 1997).

### 2.6 Wave Interference and Cognitive Relevance (Eq. 7)

> I_i(t) = ‖**ω**_i(t)‖ · cos(φ_i(t) − φ_root(t))    **(7)**

Nodes with I_i > θ_interf = 0.70 contribute to action selection. This interference criterion models the binding of semantic content (‖**ω**_i‖) with temporal coherence (cos(Δφ)), providing an operational definition of cognitive relevance that does not require an external attention mechanism.

**Reward Function (Explicit Definition):** The reward function R(t) ∈ [0,1] used in Eq. 1 is defined as:

> R(t) = exp(−3 · |sin((θ_a − θ*)/2)|)    **(7a)**

where θ_a is the selected action's phase and θ* is the target phase. This function maps angular proximity to a continuous reward signal in [0,1], with maximum reward at perfect alignment (θ_a = θ*) and minimum reward at antipodal positions.

**Outcome Criterion:** The binary outcome o(t) ∈ {0,1} is determined by the action's proximity to the target: o(t) = 1 if |sin((θ_a − θ*)/2)| < π/8, else 0. This criterion is derived from the wave interference threshold θ_interf = 0.70, mapping angular proximity to binary success/failure.

---

## 3. Formal Theorems and Computational Verification

Three fundamental properties are established formally and verified via simulation over 100 independent seeds × 2000 steps (200,000 total evaluations).

### Theorem 1 — Homeostatic Fixed Point

**Statement:** For DSCN-G with parameters (α, θ_death, N_init), there exists a unique homeostatic fixed point N_ss* satisfying:

> N_ss* = max{n : ρ_eff(α, n) ≥ n 