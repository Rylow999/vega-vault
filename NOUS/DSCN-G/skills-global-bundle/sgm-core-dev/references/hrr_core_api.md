# hrr_core API (SGM HRR/VSA library) — exact surface + gotchas

Path: `phases/phase7_composicion/hrr_core.py` (import as `import hrr_core as H` after
`sys.path.insert(0, <vault>/phases/phase7_composicion)`). Pure-Python, no numpy.

## Functions (verified via dir())
- `H.rnd_unit(rng, D)` → unit vector of dim D from a `random.Random` instance.
- `H.cos(v1, v2)` → cosine similarity. **NOT `H.cosine`** (NameError).
- `H.hrr_bind(v1, v2)` → convolutive bind. **NOT `H.bind`** (NameError).
- `H.hrr_unbind(v1, v2)` → inverse of bind.
- `H.cleanup(mem, vec, k=1)` → nearest neighbour(s) of `vec` in list `mem` by cosine.
- `H.normalize(v)` → unit-length.
- `H.build_relational_memory(...)` → builds the compositional memory used in 0027-0031.
- `H.random_roles(n, D, rng)` → n random role vectors.
- `H.recover_target(...)` / `H.recover_chain(...)` → relational recovery helpers.
- `H.math` / `H.random` → re-exported stdlib modules (do not rely on; import math directly).

## Gotchas that bit exp_SGM_0053 (cost 2 bug-cycles)
- `H.cosine` does not exist → use `H.cos`.
- `H.bind` does not exist → use `H.hrr_bind`.
- `D` must be defined BEFORE the Agent class is defined if `def __init__(self,seed,tag,D=D)`
  uses `D` as a default arg. In the multi-part assembly (`cat HEADER T1 T2 > DEST`) the
  HEADER (which sets `D=256` and defines `World`) MUST come first, then the Agent file (T1),
  then the sim file (T2). If T1 is concatenated before the header, `D` is undefined → NameError.
- cell_HRR vectors (`H.rnd_unit(rng_hrr, D)` per cell) are INDEPENDENT random vectors.
  They have NO relational structure, so HRR cleanup over them is noise at scale:
  exp_SGM_0053 showed comm accuracy = NC even at D=1280 over ~890 cells, and TopSim ≈ 0
  (no compositionality). HRR is for COMPOSITION over relational ROLES (0027-0031), NOT for
  item/word/cell recovery or next-item prediction. Use BIGRAM PLANO for item recovery.
