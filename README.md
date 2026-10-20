# Vega Vault

Vault de investigación de Luciano Benjamín Nieto (Mendoza, Argentina).
Reorganizado estructuralmente el 2026-07-25. No se eliminó ni modificó
contenido científico; solo se reubicó. Backup previo:
`nexus-vault_BACKUP_20260725_002225.tar`.

## ¿Qué es qué?

- **HORIZŌN** (`HORIZON/`, raíz, nuevo **2026-09-29**) — El apartado de la
  unión LOGOS+NOUS. Contiene: el informe integrado del marco unificado de
  los cuatro mecanismos (expansión, contracción, compresión, colapso
  generativo), la revisión crítica de Nexus como Apéndice C, la predicción
  falsable testeable en DSCN-G (¿el punto crítico depende del instrumento
  de medición o del sistema?), y las aplicaciones. Incluye **Pandora** como
  caso de aplicación del marco (observadores anidados forzando colapso
  generativo controlado). No toca LOGOS ni NOUS: los usa.
- **NOUS** (`NOUS/`) — Paraguas de la teoría DSCN-G. Contiene el núcleo
  **DSCN-G** (motor cognitivo / marco de sistemas dinámicos autoorganizados)
  y sus extensiones (**QUANTUM**, **GAUGE**, **COSMOS**), más la
  documentación filosófica en `NOUS/DOCUMENTATION/`.
- **DSCN-G** (`NOUS/DSCN-G/`) — Núcleo teórico principal. Definición,
  principios, arquitectura, modelos, mecanismos centrales, fundamentos
  verificables y limitaciones. NO incluye conciencia emergente ni C3
  (eso va a EXTENSIONS). `CORE/` está subdividido en `THEORY/` (qué propone),
  `FORMALISM/` (índice de ecuaciones/teoremas del paper), `IMPLEMENTATION/`
  (código) y `VALIDATION/` (resultados + `CONSISTENCY_CHECK.md`). El estado
  de cada afirmación está indexado en `CLAIMS_STATUS.md`; el criterio para
  admitir algo nuevo al núcleo está en `CORE_RULES.md`.
- **LOGOS** (`LOGOS/`, raíz) — Papeles hermanos que NO son DSCN-G
  (DDSD, dODF, Collatz, Navier-Stokes, Confinement). Conservados como
  línea independiente, al mismo nivel que NOUS y FATE. Navier-Stokes tiene
  nota de estatus que remite al repo independiente `github.com/Rylow999/sddf`
  donde está el trabajo actual (3D, forma cerrada, DNS real).
- **FATE** (`FATE/`, raíz) — Aplicación / sistema construido USANDO DSCN-G
  (engine de drug discovery sobre ChEMBL). DESACOPLADO del núcleo
  teórico; la interfaz se documenta en `FATE/DSCNG_INTERFACE/`.
- **SHARED** (`SHARED/`) — Sistema del agente Nexus (identidad, grafo de
  conocimiento, memoria). NO es ciencia DSCN-G.
- **Master-Document/** (raíz) — Documento de consolidación NOUS Paper 0;
  une todos los dominios (NOUS + LOGOS).

## Navegación

- `HORIZON/README.md` — qué es, estructura, predicción falsable.
- `HORIZON/PAPER/INFORME_INTEGRADO.md` — el informe fundacional del marco
  unificado (+ Apéndice C con la revisión de Nexus).
- `PROJECT_MAP.md` — árbol completo del vault.
- `ROADMAP.md` — completado / en revisión / futuro.
- `REVIEW_PENDING.md` — ambigüedades, duplicados, mezclas y decisiones
  humanas pendientes.
- `FREEZE_CHECKLIST.md` — checklist final de forma antes de congelar v1.0
  (no reemplaza las decisiones científicas abiertas en `REVIEW_PENDING.md`).

## Regla de oro

Organización ≠ validación científica. Esta reorg NO valida ninguna
hipótesis; solo separa para facilitar la revisión rigurosa posterior.

## Estatus epistémico honesto (28-09-2026)

| dominio | estatus |
|---------|---------|
| SDDF / Navier-Stokes | **sólido** — forma cerrada exacta, validado en DNS real |
| fhrr-rho-collapse | **sólido** — intervención controlada (200/200 semillas) |
| DSCN-G (núcleo) | validado parcialmente (T1/T2 ✅, T3 ⚠️, C3/Φ ❌) |
| Collatz / DDSD | parcial — teorema de deriva exacto; colapso conjetura; A6 formalizado en Lean 4 + Mathlib (v24, 9 teoremas sin sorry; build verificado 2026-10-20) |
| Quantum v9.1, Gauge, Cosmos | parcial — λ₂=4 y predicciones (a)-(d) verificados con artefacto (2026-10-15); RG de Quantum sec 8.3 inconsistente (hallazgo); análogas, no causales |
| Gödel (en HORIZON) | especulativa útil — traducción marcada explícitamente |
| Pandora | en construcción — daemon activo, decodificador L2 pendiente |


## Novedades 2026-10-15

- `NOUS/RHO_LAW/` dejado autocontenido: estaba como submódulo roto (directorio
  vacío); se inlineó el repo canónico [`Rylow999/rho-law`](https://github.com/Rylow999/rho-law).
- `NOUS/QUANTUM`, `NOUS/COSMOS`, `NOUS/GAUGE`: cada carpeta ahora es un
  paquete completo (paper + verification/ + README + CHANGELOG separado).
  Verificación reproducible: λ₂=4 exacto (m=3..16), predicciones (a)-(d) de
  Cosmos reproducidas, MC de Gauge reproducido en 2 hosts. Hallazgo honesto:
  la tabla RG de Quantum §8.3 no sigue la ley declarada (β_fit=0.26 vs 2π/D).
