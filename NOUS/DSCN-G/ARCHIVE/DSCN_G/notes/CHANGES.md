# Changes from the original draft

This file documents what an independent code/claims review found and what was changed,
so the history is traceable rather than silently edited.

## 1. Working memory "no hardcoding" claim — false, corrected

The original `dscn_g_simulator_wm.py`:
- Capped stored items to `n_ss_star = max(1, int(1.0 / theta_death * 0.4))`, a formula
  whose constant (`0.4`) has no derivation and was tuned so the result equals 4 for
  `theta_death=0.10`. It does not match the paper's own Theorem 1 formula
  (`N_ss* = max{n : rho_eff(alpha,n) >= n*theta_death^2}`).
- Had `wm_capacity=4` as a constructor parameter that was never actually used anywhere
  in the class (vestigial).
- Had an explicit rule: `if n_back > len(self.working_memory): return random()`. Since
  the list was capped at 4, this guaranteed chance-level performance for every n_back ≥ 5
  by construction, independent of any dynamics.

This directly contradicts the draft's claim of "NO hay hardcoding... emerge orgánicamente."
It is the opposite: a hard cap plus a lag-conditioned random fallback.

Separately, the *other* provided script, `dscn_g_simulator.py`, implements the actual
DSCN-G architecture (phases, vitality, pruning) and includes its own `NBackTask`. Run
standalone, it shows **no** capacity collapse at all (~89% accuracy flat through 5-back),
directly contradicting the central claim being "validated." The two scripts model
different things, and only the artificially-capped one produced the reported effect.

**Fix:** `code/dscn_g_wm_emergent.py` replaces the WM script. Items compete for a shared
pool of nodes via a soft, vitality-based allocation rule (no cap); no branch in the query
function depends on `n_back`. Re-running it, the effect is genuinely different from what
was claimed: capacity degrades gradually (d′ from ~5.2 at 1-back to ~3.8 at 10-back), not
a sharp collapse to chance around lag 4–5. Section 4 of the paper was rewritten to report
this honestly.

## 2. Class-imbalance confound in the N-back accuracy metric

With 10 possible stimuli and i.i.d. sequences, `P(match) = 1/10`. A model that always
answers "no match" reaches ~90% raw accuracy with zero memory. This was not controlled
for in the original evaluation, which may partly explain the ~89-90% figures reported for
low n-back. The corrected evaluation balances match/non-match trials (~50/50) and reports
balanced accuracy and d′, which are not inflated by this asymmetry.

## 3. Numeric discrepancy in the reported table

Running the original `dscn_g_simulator_wm.py` unmodified gave 5-back = 50.2% ± 6.4% and
6-back = 50.2% ± 5.5%, not the 51.6% ± 5.5% (5-back) and 50.2% ± 6.4% (6-back) printed in
the draft — the std values for those two rows appear to have been transposed at some
point. Minor on its own, but a sign the table wasn't regenerated from a clean run before
being written up.

## 4. "Impossibility Theorems" (former Theorems 4–6, former Section 7) — removed

These claimed, in formal theorem/proof notation, that IIT/GWT/PP are structurally
incapable of certain classes of predictions. Each "proof" was a single unsupported
sentence that did not engage the actual formal content of the theories in question (e.g.
the IIT claim about Φ being "symmetric under node permutation" mischaracterizes how Φ is
computed over a system's specific causal structure). Presenting assertions in
theorem/proof formatting claims a level of rigor that wasn't there. Removed from this
draft rather than left in with a disclaimer, at the author's request; can be revisited
later if argued properly.

## 5. Theorems 1–3 and the Φ-proxy scale relation (Theorem 7) — verification not found

The draft reported specific figures (N_ss* = 4.0 ± 0.0, ω distance = 0.038, p_conv = 0.97,
rho_eff·Phi_proxy = 0.950 ± 0.017) as "computationally verified." No script producing
these numbers was present among the files this review had access to. `dscn_g_simulator.py`
implements the underlying dynamics but not a verification harness for these specific
claims. These are now marked "verification pending" in the paper rather than presented as
confirmed. **This still needs to be resolved before submission** — either the original
verification code exists and should be added to the repo, or these figures need to be
regenerated and checked the same way Section 4 was.

## 6. Ontological framing (Section 1.1)

Softened from "the most formally complete structural-computational correlate available"
(a comparative claim that relied on the now-removed impossibility theorems) to a more
modest "candidate... worth further scrutiny," pending a real comparative argument.

## Not yet addressed

- Theorems 1–3 and the Φ-proxy scale relation still need actual verification code.
- No independent check was done on the C3 phase-hijacking numbers (28.6%, 36.1°) —
  these are reported as-is from the earlier draft as an untested prediction, not
  re-verified in this pass.
