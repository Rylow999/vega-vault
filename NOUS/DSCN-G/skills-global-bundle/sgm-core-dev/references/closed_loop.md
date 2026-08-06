# exp_SGM_0025 — Closed-loop / pseudo-AGI pattern

First SGM test where the decoder ACTS on a world and the outcome returns as pain to the graph
(Eq.6 online). Operationalizes the "ser como forma sostenida de la cognición" thesis (NOTA 0023).

## World
- Ring of `N_STATES` (4). Actions: 0 = next, 1 = prev.
- One DANGER transition: `(DANGER_STATE=2, DANGER_ACTION=1) -> pain=1.0`; else pain=0.
- `world_step(state, action) -> (new_state, pain)`.

## Graph / learning
- One node per state, `valence[2]` (per-action learned value), init 0.
- `decide(node)`: greedy by valence; if both 0 -> random (open-loop / untrained).
- On pain>0 (CLOSED only): `valence[action] -= LEARN * pain`  (Eq.6 online; pain changes choice).

## Test (MUST ship the negative control — Luciano: "no emocionarse al pedo")
- T-LOOP-01 CLOSED: after N_EPIS (~60) of EPIS_LEN (~6), dangerous-action freq in danger state
  falls from ~0.51 to <0.2.
- T-LOOP-02 OPEN (loop abierto, no valence update): freq stays >=0.2. Proves learning is from
  the closure, not elsewhere.
- PASS = both. 0025 result: closed 0.013, open 0.512 -> PASS.

## Honest limits
- World is a 4-state ring, not a rich reality — proves the MECHANISM (closure+valence->learning),
  not a full AGI.
- Decoder L2 (0022) is only the action-expression glue; the learning is valence, NOT the bigram.
- Still missing for "pseudo-AGI": temporal identity continuity (narrative "self"), intrinsic
  curiosity drive, self-generated goals, real corpus (Don Quijote) for true accuracy.
