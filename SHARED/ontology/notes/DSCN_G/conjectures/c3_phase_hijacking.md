# C3 Prediction: Phase-Hijacking of Valence

## Statement
When E_i(t) exceeds θ_emerg = 0.30, the root oscillator undergoes phase-hijacking: a directional perturbation toward the antipodal attractor θ* + π.

## Mechanism
```python
if E_root > θ_emerg:
    # Phase-hijacking: perturb toward antipodal attractor (θ* + π)
    antipodal_phase = (φ_root + π) % (2π)
    phase_diff = (antipodal_phase - φ_root + π) % (2π) - π
    perturbation = 0.5 * (E_root - θ_emerg) * phase_diff
    φ_root = (φ_root + perturbation) % (2π)
```

## Neurobiological Interpretation (Suggested, Not Tested)
- S1 (primary somatosensory) → aPFC (anterior prefrontal cortex) gamma-band PLV ≥ 0.15
- Latency ≤ 200 ms
- Directionality: S1 → aPFC (Granger causality)
- Gamma-band (40-80 Hz) phase-locking value increase

## Status
🔮 CONJECTURE (not validated against neural data)
- Implemented in `_check_phase_hijack()` in dscn_g_simulator.py
- Suggested EEG/fMRI test protocol documented in C3_Prediction.md

## Paper Reference
Section 5 (Prediction C3) in main.tex / paper_main.md