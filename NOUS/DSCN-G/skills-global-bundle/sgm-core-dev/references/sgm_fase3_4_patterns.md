# SGM Fase 3/4 — copy-pasteable patterns (from exp_SGM_0019/0020/0021)

Condensed recipes for the SensorBridge + Planificación/Trauma experiments. Use as scaffolding,
modify for the specific test. All stdlib-only Python (Android, no numpy).

## 1. HDC projection (0019 SensorBridge) — project signal to omega, with round-trip

D = 128; CHUNK = 8; N_CHUNKS = D // CHUNK   # 16 chunks, finer than 8

def make_base(rng):
    bases = []
    for c in range(N_CHUNKS):
        vec = [rng.gauss(0, 1.0) for _ in range(CHUNK)]
        perm = list(range(CHUNK)); rng.shuffle(perm)
        inv = [0]*CHUNK
        for i, p in enumerate(perm): inv[p] = i
        bases.append((vec, perm, inv))           # STORE inv for unproject
    return bases

def project(signal, bases):
    vals = list(signal)[:N_CHUNKS*CHUNK]
    while len(vals) < N_CHUNKS*CHUNK: vals.append(0.0)
    omega = [0.0]*D
    for c in range(N_CHUNKS):
        vec, perm, inv = bases[c]
        chunk = vals[c*CHUNK:(c+1)*CHUNK]
        bound = [chunk[perm[i]] * vec[i] for i in range(CHUNK)]
        for i in range(CHUNK): omega[c*CHUNK + i] += bound[i] / N_CHUNKS
    norm = math.sqrt(sum(x*x for x in omega))
    if norm > 0: omega = [x/norm for x in omega]   # unit norm -> max pairwise dist = 2.0
    return omega

def unproject(omega, bases):
    vals = [0.0]*(N_CHUNKS*CHUNK)
    for c in range(N_CHUNKS):
        vec, perm, inv = bases[c]
        bound = omega[c*CHUNK:(c+1)*CHUNK]
        chunk_perm = [bound[i]/vec[i] if vec[i]!=0 else 0.0 for i in range(CHUNK)]
        chunk = [chunk_perm[inv[i]] for i in range(CHUNK)]   # INVERSE perm
        for i in range(CHUNK): vals[c*CHUNK + i] = chunk[i] * N_CHUNKS
    return vals

THRESHOLD: pairwise distance on unit-norm omega maxes at 2.0 -> use THETA_DIST ~= 0.3 (D=128), never 5.0.
Separate only STRUCTURALLY DISTINCT signals (audio-sine vs visual-edge vs impulse). Same-smoothness
(audio-sine vs thermal-ramp) COLLAPSE (~0.2) -> document as honest HDC low-res limit, not a failure.

## 2. Plan chain (0020) — structured chain + gradient + no-backtrack

Build the chain with a GRADIENT in ONE dimension so dist(k,m)=|k-m|*step (next node always wins),
and exclude prev in affinity_move so the walk can't oscillate in a 2<->3<->4 triangle.

PLAN_LEN = 8
# chain node k: omega = prev_omega + step where step=[0.3 if j==0 else 0.0 for j in range(D)]
def affinity_move(cur, nodes, M, mode, prev=None):
    best, bid = -1.0, None
    for b in nodes:
        if b == cur or b == prev: continue
        et = EDGE_TYPES[b % len(EDGE_TYPES)]
        p = math.exp(-ALPHA*M[cur][b]) * BOOST[mode][et]
        if p > best: best, bid = p, b
    return bid

DEBUG TRAP: before running, copy graph+affinity_move into a tiny script and print the first ~15
visited nodes. Oscillation (2->3->2->3... or 2->3->4->2...) means the chain has equidistant
non-adjacent nodes or no prev exclusion. Fix the geometry, don't tweak thresholds.

## 3. Trauma singularity (0021) — local attraction, STAR geometry

Singularity = node dominates its NEIGHBORHOOD, not the whole graph. Average P(traumado|s) over its
K nearest neighbors only (global average caps at ~1/N, never exceeds threshold).

STAR geometry (forces traumado to be the closest of each neighbor):
r = 0.3
nodes[TRAUMA_ID]["omega"] = [0.0]*D
for i in range(K):                       # K=8
    vec = [0.0]*D; vec[i] = r            # neighbor i at distance r along dim i
    nodes[i]["omega"] = vec
# -> dist(traumado, neigh_i) = r ; dist(neigh_i, neigh_j) = sqrt(2)*r > r  (traumado wins)

def attraction_local(nodes, M, t_id, act_t, k=K):
    others = [b for b in nodes if b != t_id]
    others.sort(key=lambda b: M[t_id][b])
    neigh = others[:k]
    total = 0.0
    for s in neigh:
        denom = 0.0; num = None
        for b in nodes:
            if b == s: continue
            act_b = act_t if b == t_id else nodes[b].get("activation", 0.5)
            p = math.exp(-ALPHA*M[s][b]) * (1 + act_b)
            denom += p
            if b == t_id: num = p
        if denom > 0 and num is not None: total += num / denom
    return total / max(1, len(neigh))

Cases: A act=5.0 (score>0.30 -> singularidad), B isolate (del node -> score 0, omega preserved),
C act=0.1 (0<score<0.30 -> reachable, no collapse), D act=5.0 again (re-collapses -> slow rehab needed).
HONEST FINDING: lowering vitality (kappa_trauma, spec section 4.3) does NOT remove the node from
the walk — V doesn't enter Eq.2. Isolation (cut edges, preserve omega) is the real mechanism.
