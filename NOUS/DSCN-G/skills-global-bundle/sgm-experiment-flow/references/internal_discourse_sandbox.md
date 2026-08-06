# Internal discourse (0040) + Sandbox test-of-fire

## exp_SGM_0040 — Internal discourse (Capa cognitiva superior)
**Date:** 2026-08-03. **Result:** PASS (40/40 after fix).

### What it is (and is NOT)
- Internal discourse = a **consistency loop over the tick's state fields**, NOT the agent generating
  text/LLM output. On subsystem conflict it weighs them and decides BEFORE acting.
- The "traza de discurso" is a dict `{conflicto, peso_a, peso_b, ganador}`, not language.
- It is the **coherence brake** that stops a world-open agent from being a pointless wanderer.

### Conflicts modeled (reuse prior semantics)
- **A:** modo=PLAN avanza, but duda alta (>0.6) → winner "dudar".
- **B:** curiosidad (eta alto) vs trauma_activo en X (dolor_count) → "evitar" if pain strong,
  "explorar" if light (reuses 0038/39 asymmetry).
- **C:** self_coherente but trauma_activo → "mantener" (isolate, do NOT delete — reuses 0021).

### Tests T-DI-01/02/03
- Coherence = `acc == tr["ganador"]` AND winner respects formula (`peso_evitar>=peso_explorar` ⇔ "evitar").
- Asymmetry monotonic: sweep dolor_count 0→1 at fixed eta=0.7 must flip explorer→avoider ≥1 time.
- NC: system ACTS (no infinite reflection loop).

### RIGID TEST-LABEL PITFALL (cost one run, 39/40)
First 0040 asserted `acc=="evitar"` for "B_fuerte". But 0039 asymmetry allows "explorar" at very high eta,
so one case legitimately returned "explorar" and the test wrongly failed. FIX: check coherence against the
FORMULA (`tr["ganador"]==("evitar" if tr["peso_evitar"]>=tr["peso_explorar"] else "explorar")`), not a fixed
label. Lesson: when a test encodes a conflict-resolution policy, verify the decision matches the POLICY
(weights), not a pre-fixed word.
