# Vega Vault

Research vault of Luciano Benjamín Nieto (Mendoza, Argentina).
Structurally reorganized on 2026-07-25. No scientific content was deleted or
modified — it was only relocated. Prior backup:
`nexus-vault_BACKUP_20260725_002225.tar`.

## What is what

- **HORIZON** (`HORIZON/`, root, new **2026-09-29**) — The LOGOS+NOUS junction.
  Contains: the integrated report of the unified framework of the four
  mechanisms (expansion, contraction, compression, generative collapse), the
  critical review by Nexus as Appendix C, the falsifiable prediction testable
  in DSCN-G (does the critical point depend on the measurement instrument or
  on the system?), and the applications. Includes **Pandora** as an
  application case of the framework (nested observers forcing controlled
  generative collapse). It does not touch LOGOS or NOUS: it uses them.
- **NOUS** (`NOUS/`) — The umbrella of DSCN-G theory. Contains the **DSCN-G**
  core (cognitive engine / framework of self-organizing dynamical systems)
  and its extensions (**QUANTUM**, **GAUGE**, **COSMOS**), plus the
  philosophical documentation in `NOUS/DOCUMENTATION/`.
- **DSCN-G** (`NOUS/DSCN-G/`) — The main theoretical core. Definition,
  principles, architecture, models, central mechanisms, verifiable grounds
  and limitations. Does NOT include emergent consciousness or C3 (that goes
  to EXTENSIONS). `CORE/` is subdivided into `THEORY/` (what it proposes),
  `FORMALISM/` (index of the paper's equations/theorems),
  `IMPLEMENTATION/` (code) and `VALIDATION/` (results +
  `CONSISTENCY_CHECK.md`). The status of every claim is indexed in
  `CLAIMS_STATUS.md`; the criterion for admitting something new to the core
  is in `CORE_RULES.md`.
- **LOGOS** (`LOGOS/`, root) — Sibling papers that are NOT DSCN-G
  (DDSD, dODF, Collatz, Navier-Stokes, Confinement). Kept as an independent
  line, at the same level as NOUS and FATE. Navier-Stokes carries a status
  note pointing to the independent repo `github.com/Rylow999/sddf`, where the
  current work lives (3D, closed form, real DNS).
- **FATE** (`FATE/`, root) — Application / system built USING DSCN-G
  (a drug-discovery engine over ChEMBL). DECOUPLED from the theoretical
  core; the interface is documented in `FATE/DSCNG_INTERFACE/`.
- **SHARED** (`SHARED/`) — The Nexus agent system (identity, knowledge
  graph, memory). NOT DSCN-G science.
- **Master-Document/** (root) — NOUS Paper 0 consolidation document; it
  unifies all domains (NOUS + LOGOS).

## Navigation

- `HORIZON/README.md` — what it is, structure, falsifiable prediction.
- `HORIZON/PAPER/INFORME_INTEGRADO.md` — the founding report of the unified
  framework (+ Appendix C with Nexus's review).
- `PROJECT_MAP.md` — full tree of the vault.
- `ROADMAP.md` — completed / under review / future.
- `REVIEW_PENDING.md` — ambiguities, duplicates, mixtures and pending human
  decisions.
- `FREEZE_CHECKLIST.md` — final form checklist before freezing v1.0 (does
  not replace the open scientific decisions in `REVIEW_PENDING.md`).

## Golden rule

Organization ≠ scientific validation. This reorganization validates NO
hypothesis; it only separates things to make rigorous later review easier.

## Honest epistemic status (2026-09-28)

| Domain | Status |
|---------|---------|
| SDDF / Navier-Stokes | **solid** — exact closed form, validated on real DNS |
| fhrr-rho-collapse | **solid** — controlled intervention (200/200 seeds) |
| DSCN-G (core) | partially validated (T1/T2 pass, T3 qualified, C3/PHI refuted) |
| Collatz / DDSD | partial — exact drift theorem; collapse conjecture; A6 formalized in Lean 4 + Mathlib (v24, 9 theorems with no sorry; build verified 2026-10-20) |
| Quantum v9.1, Gauge, Cosmos | partial — lambda_2 = 4 and predictions (a)-(d) verified with artifact (2026-10-15); Quantum's RG section 8.3 inconsistent (audit finding); analogies, not causal claims |
| Goedel (in HORIZON) | useful speculation — translation explicitly marked |
| Pandora | under construction — daemon active, L2 decoder pending |

## News 2026-10-15

- `NOUS/RHO_LAW/` made self-contained: it used to be a broken submodule
  (empty directory); the canonical repository
  [`Rylow999/rho-law`](https://github.com/Rylow999/rho-law) was inlined.
- `NOUS/QUANTUM`, `NOUS/COSMOS`, `NOUS/GAUGE`: each folder is now a complete
  package (paper + verification/ + README + separate CHANGELOG).
  Reproducible verification: lambda_2 = 4 exact (m=3..16), Cosmos predictions
  (a)-(d) reproduced, Gauge MC reproduced on 2 hosts. Honest finding: the RG
  table of Quantum sec 8.3 does not follow the declared law
  (beta_fit=0.26 vs 2*pi/D).

## Motto

*Per Aspera, Ad Astra.*
