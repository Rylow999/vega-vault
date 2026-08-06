# Project Map — Nexus Vault

```
nexus-vault/
├── Master-Document/          # NOUS Paper 0: unificación de 6 dominios (RAÍZ)
├── NOUS/                     # Paraguas teórico
│   ├── DSCN-G/               # NÚCLEO
│   │   ├── CORE/             #   SCOPE.md + 01_DSCN-G_Paper.md +
│   │   │   ├── THEORY/       #     00_Core_Definition.md — ¿qué propone?
│   │   │   ├── FORMALISM/    #     índice de ecuaciones/teoremas del paper
│   │   │   ├── IMPLEMENTATION/#    CODE/ (scripts) — ¿cómo se implementa?
│   │   │   └── VALIDATION/   #     RESULTS/ (json) + CONSISTENCY_CHECK.md
│   │   ├── CLAIMS_STATUS.md  #   tabla de estado de afirmaciones (índice)
│   │   ├── CORE_RULES.md     #   criterio de admisión al núcleo
│   │   ├── DOCUMENTATION/    #   design notes, estado auditoría, auditoria/
│   │   │                     #     (fuente completa de CLAIMS_STATUS.md)
│   │   ├── EXPERIMENTS/      #   N_BACK / COMPARISONS / SYNCHRONIZATION /
│   │   │                     #     ABLATIONS / STABILITY / OTHER
│   │   ├── EXTENSIONS/       #   C3_Face_Hijacking/ (README+STATUS) /
│   │   │                     #     DISCRETE_DYNAMICS/ (pendiente, placeholder) /
│   │   │                     #     PHI_PROXY / T3_Review (resuelto, vacío)
│   │   └── ARCHIVE/          #   DSCN_G (v1) + DSCN_G_v2 (OBSOLETE, no destructivo)
│   ├── QUANTUM/  PAPER/ NOTES/   # DSCN-G-Quantum v9.1
│   ├── GAUGE/    PAPER/ NOTES/   # DSCN-G-Gauge (NOUS Paper 6)
│   ├── COSMOS/   PAPER/ NOTES/   # DSCN-G-Cosmos v8.1 (NOUS Paper 3)
│   └── DOCUMENTATION/        #   NOUS filosófico/técnico
├── LOGOS/                    # Papeles hermanos (NO DSCN-G) — RAÍZ, mismo nivel que NOUS/FATE
│   ├── DDSD/  PAPER/ NOTES/
│   ├── DODF/  PAPER/ NOTES/
│   ├── COLLLATZ/  PAPER/ NOTES/   (Complexity + Structural)
│   ├── NAVIER_STOKES/  PAPER/ NOTES/
│   └── CONFINEMENT/  PAPER/ NOTES/
├── FATE/                     # Aplicación (desacoplada) — RAÍZ
│   ├── CORE/ MODULES/ EXPERIMENTS/ DOCUMENTATION/ DSCNG_INTERFACE/
├── SHARED/                   # Sistema Nexus (no ciencia)
│   └── memory/ ontology/ brain/ _meta/
├── README.md  PROJECT_MAP.md  ROADMAP.md  REVIEW_PENDING.md
├── FREEZE_CHECKLIST.md       # checklist final pre-congelación v1.0
└── .git/ .gitignore .obsidian/  (infra)
```

## Conteo (post-reorg)
- NOUS: 92 archivos · LOGOS: 6 · FATE: 422 · SHARED: 76 · raíz: Master-Document + docs
