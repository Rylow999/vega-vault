# Obstacle-avoidance / pain test in grid-agent (exp_SGM_0033) — measurement pitfalls

The 0033 iteration history: the MECHANISM (dolor online, 0025) was fine; the TEST kept failing to
*measure* avoidance across 5 redesigns. Captured so a future SGM grid experiment doesn't repeat it.

## What failed, in order
1. **Dolor = single cell on bottom edge (borde inferior).** Both CON and ABIERTO pisadas=0.0.
   Greedy affinity already avoids one isolated obstacle → "learns to avoid" is vacuous (test can't fail).
2. **Dolor = single cell on shortest BFS path.** Still 0.0 for both. Affinity-greedy route ≠ exact
   BFS shortest path, so it never stepped on that specific cell. Single-cell pain is unreliably hit.
3. **Dolor ZONE = diagonal (k,k) k=2..7, BUT with a central wall block (filas/cols 2-7).**
   Everyone 0.0 — because (k,k) for k=2..7 landed INSIDE the wall block → the "pain zone" was
   unreachable walls. Bug: pain cells coincided with walls. Always verify pain cells are not walls
   (BFS/set check before running).
4. **Open map, dolor ZONE on diagonal.** CON=6.0, RW=9.05, ABIERTO=0.0. Now pain is felt. BUT
   ABIERTO=0.0 because the deterministic no-pain agent took a fixed route that happened to miss the
   zone → invalid as control. RW (9.05) is the valid baseline.
5. **Final criterion:** T-DOLOR-01 = CON pisadas < RW pisadas (learns to moderate punishment);
   T-DOLOR-02 = CON still reaches meta; T-DOLOR-NC = RW does NOT learn (pisadas_RW > pisadas_CON).
   → PASS. Comparison is CON vs RW, never CON vs deterministic-no-pain.

## Rules for "learns to avoid pain / obstacle-avoidance" tests in grid
- **Use a ZONE of pain (multiple cells) on the route the affinity actually prefers** (e.g. the most
  direct diagonal to meta), not a single cell. Single-cell pain is hit unreliably → vacuous test.
- **Verify pain cells are reachable** (not walls) before running — BFS or set-difference check.
- **Valid negative control = RANDOM WALK** (doesn't learn). A deterministic no-pain agent is NOT a
  valid control: its fixed route may avoid the zone by chance, giving 0.0 and making CON<ABIERTO
  impossible to satisfy. Compare against RW.
- If a sub-test can't be measured in the chosen environment (e.g. avoid-pain with no real bifurcation
  in a pure maze), **separate it to another experiment with an adequate map**; don't force PASS.
- "Clean avoidance" (route flips after penalty) is not conclusive with pure affinity in an open grid —
  the greedy already navigates well and absorbs a local penalty. Report honestly (CON 6.0 vs RW 9.05,
  not vs abierto). For dramatic evasion, use a bottleneck/cuello-de-botella map (proposed 0033b).

## Standard-benchmark rule (from 0032, reinforced by 0033)
Use a STANDARD benchmark of the area (random maze + BFS connectivity + random-walk baseline for
navigation; unigram for language; open-loop for learning). Do not hand-tune a labyrinth to force green.
If the environment is so simple the baseline (plano/aleatorio) also passes, ENLARGE it (8x8 abierto →
10x10 maze) until the baseline fails and the mechanism wins — that's the signal you're measuring something real.

User's exact correction (0032), applies to ALL experiments:
"No tenés que pensar cómo hacerlo para que pase, si no hacerlo bien. Buscá algún test típico que se
utilice en estos casos. Tal vez el mapa es muy simple para el sistema, también puede ser eso."
