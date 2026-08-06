# Roadmap — Nexus Vault

## ✅ Completado
- Aplicación de la guía de corrección pre-freeze (2026-07-25, segunda
  pasada): CORE dividido en THEORY/FORMALISM/IMPLEMENTATION/VALIDATION;
  creados `CORE/SCOPE.md`, `CLAIMS_STATUS.md`, `CORE_RULES.md`,
  `CORE/VALIDATION/CONSISTENCY_CHECK.md`, `FREEZE_CHECKLIST.md`;
  `EXTENSIONS/C3_Face_Hijacking/` documentada (README+STATUS);
  `EXTENSIONS/DISCRETE_DYNAMICS/README.md` creada como placeholder honesto
  (sigue pendiente, no se fabricó contenido); caveat de versión FATE v4/v5
  vs v6 anotado explícitamente en `DSCNG_INTERFACE.md`.
- Reorganización estructural del vault (2026-07-25): NOUS (paraguas) /
  DSCN-G (núcleo) / LOGOS / FATE / SHARED separados; LOGOS y FATE al
  mismo nivel que NOUS en la raíz.
- Auditoría DSCN-G v3 (6 rondas, cierre 2026-07-24): claims verificados /
  no-sostenidos documentados en `NOUS/DSCN-G/DOCUMENTATION/auditoria/`.
- Renombrado código+paper v2→v3 (consistencia de nombres).
- Revisión de REVIEW_PENDING (7 ítems): NOUS=HÍBRIDO; C3 y Φ_proxy →
  EXTENSIONS (open question); T3 → reporte estricto ya aplicado en el
  paper (76.7% estricto + 100% operacional); Claims 9/10 redistribuidos.
- Paper DSCN-G v3 ya refleja todas las correcciones: T1 N_ss*≈4–5, T3
  reporte estricto, N-back 9.5±1.0, d′ piso ~0.8–1.0, C3 marcado como no
  sustentado, limitaciones y trabajo futuro honestos.
- FATE v6 integrado en FATE/DOCUMENTATION/ + DSCNG_INTERFACE/ documentado.

## 🔒 Checklist de congelación DSCN-G v1.0

### Bloque A — Núcleo (CORE), ya listo para freeze
- [x] T1 (punto fijo + maximalidad real) verificado y en el paper.
- [x] T2 (ω = 1.0000) verificado y en el paper.
- [x] T3 (consenso de fase) reporte estricto aplicado (76.7% / 100%).
- [x] N-back v6 (9.5±1.0) y RNN baseline en el paper.
- [x] C3 marcado explícitamente como NO sustentado (§3.4, §5.4, §5.6).
- [x] Φ_proxy O(log N) NO aparece como claim en el paper (está en EXTENSIONS).

### Bloque B — Extensión (fuera del freeze, open question)
- [ ] C3 / Face Hijacking: revisar una última vez antes de cerrar (rediseño
      30.2% con params agresivos; en EXTENSIONS/C3_Face_Hijacking/).
- [ ] Φ_proxy: decidir retirar / reformular descriptivamente / dejar open.
      En EXTENSIONS/PHI_PROXY/.
- [ ] Discrete Dynamics: determinar relación con DSCN-G Core (EXTENSIONS/
      DISCRETE_DYNAMICS/, marcado pendiente).

### Bloque C — Edición menor sugerida (no bloquea freeze)
- [ ] Aclarar en el paper qué versión de FATE valida (cita v4/v5 pero la doc
      es v6; ver FATE/DSCNG_INTERFACE/DSCNG_INTERFACE.md).
- [ ] Discrete Dynamics: si se decide relación, mover de EXTENSIONS a CORE
      o dejar nota explícita.

### Bloque D — Validación experimental (future work declarado, NO bloquea)
- [ ] Ablation studies (qué mecanismo explica qué).
- [ ] Sensibilidad a parámetros.
- [ ] Baseline LSTM/GRU/Transformer.
- [ ] Validación EEG/fMRI (predicción de gradiente continuo, §5.3).

## 🔮 Futuro (línea NOUS / LOGOS)
- Quantum / Gauge / Cosmos: extensiones en desarrollo (en NOUS/).
- LOGOS (DDSD, dODF, Collatz, Navier-Stokes, Confinement): línea
  independiente, índice cruzado pendiente.
- NOUS filosófico: marco de consciencia explícitamente no-resuelto.
