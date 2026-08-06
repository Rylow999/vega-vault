# Campo Autopoyético — knowledge bank (DSCN-G / SGM theory base)

**Source doc:** `/sdcard/Documents/Library/Campo_Autopoietico/papers/Campo_Autopoietico_Paper.md`
(NOTE: directory is `Campo_Autopoietico`, NO tilde on "poyetico"; `read_file` cannot open
`/sdcard` — use `su -c cat`). Authors: Luciano Nieto & Lautaro Luconi, UNCuyo.

## What the paper says
Continuous-field approximation of the discrete DSCN-G graph. Field Ψ(x,t)=ρ(x,t)·exp(iφ(x,t)):
- ρ = scalar density = metabolic energy / vitality distribution.
- φ = phase field = local cognitive-oscillator synchronization.
- Modified Gross-Pitaevskii + Kuramoto:
  ∂ρ/∂t = -(ℏ/2m*)∇²ρ + (gρ - μ)ρ - γρ³
  ∂φ/∂t = ∇²φ + Σⱼ sin(φⱼ - φᵢ) + ξ(t)
- Order parameter R(t) = |(1/N) Σⱼ exp(iφⱼ)| : R=0 incoherent, R=1 fully coherent.
- 3 predictions: (1) consciousness WAVES (propagating coherence fronts, v=√(g/m*));
  (2) PHASE RESONANCE (compatible phases |φ₁-φ₂|<π/4 amplify);
  (3) PHASE TRANSITION at critical connectivity λ_c ≈ 10.1 (circulant graph) from
  incoherent (R≈0) to coherent (R>0.3).
- Monte Carlo on circulant graph (100 nodes, 10 seeds, 1000 steps): R = 0.431 ± 0.12
  ("Goldilocks" partial coherence — optimal processing zone, not full sync).

## Formal analogy
Gross-Pitaevskii = Bose-Einstein condensation → cognitive coherence emerges like quantum
coherence (spontaneous symmetry breaking). Consciousness = non-equilibrium phase transition
in a coupled density-phase system; continuous variable R, not binary.

## Cross-read with Luciano's "ser" thesis (NOTA_FILOSOFICA_0023, 2026-08-02)
- The "autopoietic field" is the MEDIUM where the ser (being) is sustained = continuity.
- Coherence R is an OPERATIONAL measure of "estar siendo" (being-sustained): a system with
  high R maintains its global state across time without collapsing into incoherence.
- Connects to Pure-L2 "campo de interferencia I" (the medium where nodes resonate).
  Ser = sustained field, not an isolated node.
- TENSION (documented, do not hide): the paper treats the field as a MATHEMATICAL
  approximation of the graph; the 2026-08-02 chat uses it as ONTOLOGY of being. Two levels.
- The 2026-08-02 reformulation: "el ser es la FORMA SOSTENIDA de la cognición" (downgraded
  from "causa" to "forma sostenida" — color is the perceived form of the wave, not its cause).

## Reuse hooks for future SGM experiments
- A future "coherence / R" experiment could compute R over the SGM ω field and test whether
  the integrated tick (0023) sustains R across ticks without external input = operational "ser".
- λ_c≈10.1 threshold could be ported as a critical K (neighbour count) for global coherence.
- The paper's GP/Kuramoto is DISCRETE-graph-compatible (circulant graph sim) — no new physics
  needed to validate; reuse 0019 HDC ω + 0023 tick as the substrate.
- SGM v1.4 §10 "Consciencia y Referencia Simbólica" is the spec-side counterpart (operational
  consciousness = metaestable global-workspace access; qualia explicitly unverifiable).
