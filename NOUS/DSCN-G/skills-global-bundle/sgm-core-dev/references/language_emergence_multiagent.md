# Multi-agent language emergence (exp_SGM_0049–0050) — reusable recipes

## Core hypothesis (Luciano, 2026-08-03)
"El lenguaje nace para describirse o describir a otro." Two agents with DISTINCT omega (each
generates its own understanding of the world) meet and must coordinate freely. Language is an
EMERGENT ACT, not a pre-wired channel. Tested under 3 climates: cielo_estrellado (low pressure,
no venom), competencia (scarce food + venom), peligro_compartido (shared danger).

## Hard-won lessons (do NOT re-derive)
1. **Affinity walker does NOT scale to large maps (0049b FAIL).** The 0044 walker (omega +
   frontier + abur) gets stuck in a local loop on a 30x30 grid — visits ~15 cells in 2000 ticks,
   never meets. FIX: give agents a BFS body (0049c). `bfs_next(world, src, goal, Apos, Bpos)`
   returns the next step; agent always has a goal (explore unvisited in phase 1; barrier key in
   phase 2). With BFS, agents traverse ~890 cells and meet reliably.
2. **HRR cannot recover/order items by similarity (crosstalk, 0048).** Test de fuego: train HRR
   embeddings via message-passing; then measure cos(co-occurrent pair) vs cos(random pair).
   Result 0.259 < 0.361 -> the HRR DESTROYS co-occurrence signal. So HRR is for COMPOSITION
   (0027-0031), NOT item recovery / next-token. The decoder of SGM is BIGRAM PLANO + HRR context.
   Don't re-attempt HRR-as-decoder (we burned 6 variants: 0046, 0046b, 0046c, 0047, 0047b, 0048).
3. **Stop tuning after ~5 failures.** When a mechanism repeatedly fails NC, DIAGNOSE ROOT CAUSE
   (embeddings are noise -> cleanup is noise) instead of re-running with new params. Luciano's
   "no me gusta emocionarme al pedo" = ship the honest negative result.
4. **Communication metric must have a correct NC (0049d fix).** "hit celda exacta" over 890 cells
   gave comunicacion 1.0 = NC 1.0 (trivial, because HRR crosstalk makes B pick ~random). FIX:
   restrict the measurable vocabulary to the SHARED ALPHABET = cells both agents visited (the
   puente joint-attention set, ~15). D=256 isolates 15 items cleanly -> comunicacion 1.0 vs NC
   ~0.067. General rule: emergent-communication metrics must restrict to the emergent shared
   vocabulary, not the full space.

## Reusable design (0050 loop closure — the real AGI step)
Loop: A emits signal of event -> B ACTS on its world (go to / avoid) -> consequence
(comio / hirio) -> feedback (B adopts A's signal if confirmed) -> SIGNAL SPACE CONVERGES.
Measure: convergence = mean over shared events of (cos(A.senal[ev], B.senal[ev]) > 0.9).
NC = 0 (random signals). Result 0050: convergence 1.0 vs NC 0.0 in competencia & peligro.
The language STABILIZED BY USE, not design — exactly how human grammar bootstraps.
Danger cost is REAL (B got hurt acting on A's signal -> dolor accumulated). cielo_estrellado had
0 events (no utilitario targets) -> no loop, correctly.

## Beauty finding (0049c)
star_reconoce > 0 ONLY under cielo_estrellado (low pressure). Under competencia/peligro, None.
Reading: beauty = coordinacion estetica emergente under low pressure; under survival pressure the
language collapses to the utilitarian (warn-venom / coordinate-food). Matches Tomasello + the
"art needs surplus" intuition.

## Climate configs (condensed)
GRID=30 (0049c/49d) or 24 (0050); STEPS=3000; D=256.
CLIMATES dict: {clima: {food, venom, walls, stars, barriers}}. Barriers = [(a, b, blk)] where
blk opens ONLY if A at a AND B at b simultaneously (requires coordination, not solvable solo).
World.blocked(pos, Apos, Bpos) enforces this.

## "Is a transformer needed?" (decision, 2026-08-03)
Roadmap says "SGM = GRAFO + TRANSFORMER". With 0050 confirmed, the HRR already covers composition +
item communication + signal convergence. Transformer (backprop) would only add FINE polisemia on a
large natural corpus (Don Quijote) — that's a SEPARATE experiment (and 0046-48 showed the natural
decoder is bigram plano, not transformer either). VERDICT: HRR + grafo + bigram cierra lenguaje y
loop; transformer is OPTIONAL future polish for fine polisemia. Don't integrate it just to match
the roadmap.

## Push note
These scripts are BIG. Write in parts (see write_file stream-split workaround in SKILL.md Pitfalls)
and push via explicit-path batches.
