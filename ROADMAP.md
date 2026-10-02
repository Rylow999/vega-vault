# Roadmap — Nexus Vault

## ✅ Completado (hasta 2026-09-28, v3.4 de SDDF)

- SDDF llevado al límite: forma cerrada exacta verificada, null model de
  Migdal calibrado (500 nulos; umbral real amp=0.005-0.02), Rust↔Python
  sincronizado al dígito, validación con DNS real (JHTDB isotropic1024,
  box completo, 8 bloques, ε=0.96× documentado, q=1.60±0.02 en k∈[8,64]),
  detector de ventana sobre pendiente suavizada (v3.4: w=5 en DNS real).
- **`sddf` committeado y pusheado** a `github.com/Rylow999/sddf` (main
  al día; 4 commits: v3.2, v3.3, v3.4, paper secciones 13-14).
- HORIZŌN creado (2026-09-29): informe integrado del marco de los cuatro
  mecanismos, revisión crítica incorporada (Apéndice C), predicción
  falsable documentada, aplicaciones mapeadas.
- **fhrr-rho-collapse pushado** (`github.com/Rylow999/fhrr-rho-collapse`;
  repo sigue en vega-vault/NOUS/FHRR-HRO-COLLAPSE/ pero con su propio
  README alineado con el paper final, CI, verify, crate).
- Buckmaster-Alpöge sept-2026 revisado: 4 PDFs (IPM, Boussinesq, Euler 3D,
  statement) en `HORIZON/DOCUMENTATION/papers_blowup/`, resumen criollo
  en `SOLO_PAPERS_BLOWUP_SEP2026.md`. Conclusión: NS sin forzamiento sigue
  abierto; el hipodissipative está pendiente.
- **Todo pusheado:** vega-vault (main, 2026-09-29) y sddf (main,
  2026-09-28) están al día con GitHub.

## En revisión (abiertos, con pipeline viable si hay acceso a datos)

- **isotropic4096 / channel4094 (Re mayor)**: no descargable sin token de
  acceso a JHTDB (el mirror TUM sólo tiene 1024; el snapshot 4096 existe
  en JHTDB pero sólo por intermedio del servicio con token gratuito — el
  que los usuarios piden desde `turbulence.idies.jhu.edu/database`).
  Testing sin token limita el tamaño a 4096 puntos. Cuando aparezca el
  token: un snapshot entero de 4096³ (o una caja completa del channel4094)
  con escalado G*(Re) y el periodograma de Migdal calibrado en el DNS.
- **Serie temporal de isotropic1024**: testear si la ley ρ se verifica
  en evolución temporal (no sólo en promedio de bloques paralelos) con
  lo mismo que se correlacionan estados entre observadores (exp_ns_multi-
  observer de RHO_LAW pero en tiempo, no en espacio).
- **R-4 recalculo del paper 2D**: bloqueado por falta de datos de entrada
  (NS-2D DNS crudos perdidos). Alternativa: simulador propio si se necesita.
- **DSCN-G: hecha la validación de estructura (Stable states, T1, T2, N-back);
  pendiente tocar el concepto de umbral de expansión.** Testar si θ_emerg
  depende del método de medición (el punto crítico sería instrumento, no
  sistema — esto es la predicción falsable del marco).
- **Pandora (HORIZON/PANDORA):** daemon activo. Falta testear el
  decodificador L2 propiamente (proyección lineal del estado del grafo a
  lenguaje) — el cuello de botella real. Objetivo: software controlado
  del colapso generativo.

## 🔮 Futuro (línea NOUS / LOGOS / HORIZON)

- Quantum / Gauge / Cosmos: extensiones en desarrollo (en NOUS/).
- LOGOS (DDSD, dODF, Collatz, Navier-Stokes/SDDF, Confinement): línea
  independiente, índice cruzado pendiente.
- HORIZON: continuar la validación del marco (testable, no cruzada con
  manual de dudas).
- NOUS filosófico: marco de consciencia explícitamente no-resuelto.

## Notas operativas

- **Identidad git:** vault configurado con Luciano / noreply GitHub.
- **Dataset previsto:** JHTDB via mirror HuggingFace (TUM) para isotropic
  1024; el canal4094 está detrás del token personal.
- **Memoria de trabajo:** vault en synced con SDDF y fhrr-rho-collapse.
- El RHO_LAW sigue vigente como capa transversal del marco (el detector
  de Migdal corrigido referencia allí, vendiendo el detector viejo).
