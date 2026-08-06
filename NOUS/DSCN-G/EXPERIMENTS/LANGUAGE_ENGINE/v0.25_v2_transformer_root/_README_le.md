# DSCN-G Language Engine — Roadmap (de a poco, hasta L2 rústico)

Proyecto de Luciano. Objetivo: ver si DSCN-G puede ser sustrato cognitivo de
un motor de lenguaje, terminando en un decodificador L2 rústico (ω→texto).

DECISION 2026-07-25: primero validar que el grafo "ENTIENDA" (recupere conceptos
desde la masa), y LUEGO ir al decoder. El decoder es v0.5, no antes.

Insumos:
- v0.1..v0.x: experimentos aca.
- PANDORA_Resumen.md: propio de Luciano. Clave: HIBERNADO (V<=0.10 preserva ω),
  β_eff contextual, W(t) dinamica. Correccion al colapso de v0.1.

## Roadmap
- v0.1 [HECHO] N* satura ~4.5 => DSCN-G = memoria de TRABAJO, no de masa.
- v0.2 [CORRIENDO] Sweep (K,θ): colapso ¿paramétrico o estructural?
- v0.3 [LISTO, pendiente] RECUPERACION: ¿el grafo recupera el concepto correcto?
        Variante A norma flotante vs Variante B bits/puertas logicas (idea Luciano).
        Valida (1) que entiende y (2) que la repr en bits conserva semantica.
- v0.4 [plan] β_eff contextual (ρ modula β). Barato, de Pandora.
- v0.5 [plan] L2 RUSTICO: proyeccion ω→vocabulario. Solo si v0.3 recupera bien.

## Hipotesis central
DSCN-G sostiene lenguaje SOLO si: (a) la masa no colapsa a 4 (hibernado),
(b) el grafo RECUPERA conceptos (v0.3), y (c) hay L2 que proyecte ω a texto.
Sin v0.3 validado, el decoder es prematuro. Vamos de a poco.
