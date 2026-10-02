# Project Map — Nexus Vault

```
nexus-vault/
├── Master-Document/          # NOUS Paper 0: unificación de 6 dominios (RAÍZ)
├── HORIZON/                  # ★ NUEVO 2026-09-29: unión LOGOS+NOUS (RAÍZ)
│   ├── README.md             #   qué es HORIZON, estructura, predicción falsable
│   ├── PAPER/
│   │   ├── INFORME_INTEGRADO.md   # informe fundacional + Apéndice C (revisión Nexus)
│   ├── PANDORA/              #   aplicación cognitiva: observadores anidados,
│   │                         #     colapso generativo controlado (daemon vivo)
│   ├── APPLICATIONS/         #   SDDF.md (estado epistémico, aplicación)
│   │                         #   + tabla de integración (README.md)
│   └── DOCUMENTATION/        #   papers_blowup/ (Buckmaster-Alpöge sept-2026)
│                             #   + SOLO_PAPERS_BLOWUP_SEP2026.md (resumen criollo)
├── NOUS/                     # Paraguas teórico
│   ├── DSCN-G/               # NÚCLEO [estado: validación parcial T1/T2 OK]
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
│   ├── DOCUMENTATION/            # NOUS filosófico/técnico
│   └── PANDORA/                  # daemon vivo (systemd), repo GitHub Rylow999/Pandora
├── LOGOS/                    # Papeles hermanos (NO DSCN-G) — RAÍZ, mismo nivel que NOUS/HORIZON
│   ├── DDSD/  PAPER/ NOTES/
│   ├── DODF/  PAPER/ NOTES/
│   ├── COLLLATZ/  PAPER/ NOTES/   (Complexity + Structural)
│   ├── NAVIER_STOKES/  PAPER/ NOTES/   (paper 2D histórico; ver repo sddf)
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

- HORIZON: 5 archivos (README + informe + aplicaciones)
- NOUS: 92 archivos · LOGOS: 6 · FATE: 422 · SHARED: 76
- raíz: Master-Document + docs

## Estado de los proyectos con repo independiente de GitHub

- `Rylow999/sddf` — Navier-Stokes 3D: forma cerrada G[u], validación DNS, detector suavizado. **Estado: sólido, pushado a main.** El LOGOS/NAVIER_STOKES del vault tiene nota de estatus histórico remitiendo acá.
- `Rylow999/fhrr-rho-collapse` — paper "Operator placement, not representation"; crate fhrr-resilient v0.3.0. **Estado: sólido, pushado.**
- `Rylow999/Pandora` — daemon cognitivo residente. **Estado: infraestructura viva, decodificador L2 pendiente.**

