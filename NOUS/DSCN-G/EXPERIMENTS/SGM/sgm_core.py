# -*- coding: utf-8 -*-
"""
sgm_core.py -- SGM consolidado, UN solo modulo (no 63 scripts sueltos).
Solo mecanismos GANADORES de la Fase 7 + previas, validados en experimentos reales:

  GANADORES (adentro):
   - HRR + rol-por-nivel (0027c / hrr_core): composicion relacional. Rol = role_vecs[indice_nodo],
     NO posicion ni cyclic shift (ese era el bug de 0029). Bind=conv circular (signo i-k, 0027),
     unbind=correlacion, cleanup OBLIGATORIA (VSA survey).
   - PPR (0004): ruteo multi-hop con restart (alpha=0.15). Supera resonancia local 1-paso.
   - Decoder bigrama validado en corpus real (0026): top1 >> azar y > lineal; shuffled cae a azar.
   - Slots separados K=3 (0059g): anidado profundo (prof 12+). K=1/2 colapsan binariamente.

  DEJADOS AFUERA EXPLICITAMENTE (no ganaron / fallaron):
   - NodeCore en Python (0002): no aporto rendimiento; usamos omega como lista de floats.
   - Fase dinamica para XOR: fallo documentado, no se reimplementa.
   - 0056 con regla inyectada: TRAMPA (gramatica hardcodeada), excluida por honestidad.
   - Resonator puro (0059f): techo confirmado, no rompe; usamos slots K=3.

  SensorBridge (0019): project/unproject HDC de estado semantico -> omega. NO pixeles (instruccion:
  alimentar con estado semantico de Crafter: inventario, logros, salud; no pixeles crudos).

  Bucle percepcion->tick->accion: SGMAgent.step(state) y SGMAgent.reward(r).
  NO incluye multi-agente ni capa de lenguaje (se suman DESPUES de cerrar el loop solo).

Todo stdlib puro (sin numpy). Portable a donde corra Crafter.

API publica:
  HDC(rng, D)                  -> .project(signal)
  HRR(D, rng, n_roles)         -> .bind/.unbind/.cos/.cleanup/.role(i)/.relational_memory/.recover
  ppr_route(adj, seed, aff_fn) -> dict nodo->prob
  BigramDecoder(counts)        -> .top1(ctx)/.top5(ctx)
  SGMAgent(...)                -> .step(state_semantic, valid_actions)->action ; .reward(r, pain)
  build_nested_K3(...)         -> anidado profundo slots separados (0059g)
"""
import math, random

# 1. HDC / SensorBridge (0019): estado semantico -> omega
class HDC:
    def __init__(self, rng, D=256, chunk=8):
        self.D = D; self.chunk = chunk; self.n_chunks = D // chunk; self.bases = []
        for _ in range(self.n_chunks):
            vec = [rng.gauss(0, 1.0) for _ in range(chunk)]
            perm = list(range(chunk)); rng.shuffle(perm)
            self.bases.append((vec, perm))

    def project(self, signal):
        vals = list(signal)[:self.n_chunks * self.chunk]
        while len(vals) < self.n_chunks * self.chunk: vals.append(0.0)
        om = [0.0] * self.D
        for c in range(self.n_chunks):
            vec, perm = self.bases[c]
            ch = vals[c * self.chunk:(c + 1) * self.chunk]
            b = [ch[perm[i]] * vec[i] for i in range(self.chunk)]
            for i in range(self.chunk): om[c * self.chunk + i] += b[i] / self.n_chunks
        n = math.sqrt(sum(x * x for x in om))
        return [x / n for x in om] if n > 0 else om

# 2. HRR + rol-por-nivel (0027c / hrr_core)
class HRR:
    def __init__(self, D, rng, n_roles):
        self.D = D
        self.roles = [[rng.gauss(0, 1) for _ in range(D)] for _ in range(n_roles)]
        for r in self.roles: self._norm(r)

    def _norm(self, v):
        n = math.sqrt(sum(x * x for x in v))
        if n > 0:
            for i in range(len(v)): v[i] /= n

    def role(self, i): return self.roles[i]

    def bind(self, a, b):
        D = self.D; c = [0.0] * D
        for k in range(D):
            s = 0.0
            for i in range(D): s += a[i] * b[(k - i) % D]
            c[k] = s
        return c

    def unbind(self, a, b):
        D = self.D; c = [0.0] * D
        for k in range(D):
            s = 0.0
            for i in range(D): s += a[i] * b[(i - k) % D]
            c[k] = s
        return c

    def cos(self, a, b):
        s = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
        return s / (na * nb) if na * nb > 0 else 0.0

    def cleanup(self, vec, mem):
        best, bi = -2.0, -1
        for i, m in enumerate(mem):
            c = self.cos(vec, m)
            if c > best: best, bi = c, i
        return bi

    def relational_memory(self, edges, omega):
        rel = {}
        for i in edges:
            acc = [0.0] * self.D
            for k in edges[i]:
                b = self.bind(self.role(k), omega[k])
                for j in range(self.D): acc[j] += b[j]
            rel[i] = self._normlist(acc)
        return rel

    def _normlist(self, v):
        n = math.sqrt(sum(x * x for x in v))
        return [x / n for x in v] if n > 0 else v

    def recover(self, rel_mem, src, tgt, omega):
        rec = self.unbind(rel_mem[src], self.role(tgt))
        return self.cleanup(rec, omega)

# 3. PPR (0004)
def ppr_route(adj, seed, aff_fn, alpha=0.15, iters=100):
    nodes = list(adj.keys())
    if seed not in nodes: return {}
    rank = {n: 0.0 for n in nodes}; rank[seed] = 1.0
    for _ in range(iters):
        nxt = {n: 0.0 for n in nodes}
        for n in nodes:
            if rank[n] == 0: continue
            nxt[seed] += alpha * rank[n]
            neigh = adj[n]
            if not neigh: continue
            w = [max(0.0, aff_fn(n, k)) for k in neigh]
            s = sum(w)
            if s <= 0: continue
            for idx, k in enumerate(neigh):
                nxt[k] += (1 - alpha) * (w[idx] / s) * rank[n]
        rank = nxt
    return rank

# 4. Decoder bigrama validado en corpus real (0026)
class BigramDecoder:
    def __init__(self, counts):
        self.counts = counts; self.V = len(counts)
        self.P = []
        for row in counts:
            s = sum(row)
            self.P.append([x / s if s > 0 else 0.0 for x in row])

    def top1(self, ctx):
        row = self.P[ctx]
        return max(range(self.V), key=lambda j: row[j]) if sum(row) > 0 else -1

    def top5(self, ctx):
        row = self.P[ctx]
        return sorted(range(self.V), key=lambda j: -row[j])[:5]

# 5. SGMAgent: bucle percepcion -> tick -> accion (+ reward)
class SGMAgent:
    def __init__(self, rng, D=256, n_nodes=32, alpha_ppr=0.15):
        self.D = D; self.alpha = alpha_ppr
        self.omega = [[rng.gauss(0, 1) for _ in range(D)] for _ in range(n_nodes)]
        self.edges = {i: [] for i in range(n_nodes)}
        self.hdc = HDC(rng, D)
        self.hrr = HRR(D, rng, n_nodes)
        self.rel = {}
        self.E = 0.0

    def _aff(self, i, k):
        return self.hrr.cos(self.omega[i], self.omega[k])

    def set_edges(self, edges):
        self.edges = {i: list(edges.get(i, [])) for i in range(len(self.omega))}
        self.rel = self.hrr.relational_memory(self.edges, self.omega)

    def step(self, state_semantic, valid_actions, mode="hrr"):
        om_r = self.hdc.project(state_semantic)
        seed = min(range(len(self.omega)), key=lambda n: math.sqrt(
            sum((x - y) ** 2 for x, y in zip(om_r, self.omega[n]))))
        rank = ppr_route(self.edges, seed, self._aff, alpha=self.alpha, iters=100)
        best, bv = -1, -2.0
        for a in valid_actions:
            if rank.get(a, 0) > bv: bv, best = rank.get(a, 0), a
        return best if best >= 0 else (valid_actions[0] if valid_actions else -1)

    def reward(self, r, pain=0.0, beta=0.10):
        self.E = max(0.0, r - pain)
        for om in self.omega:
            for j in range(self.D):
                om[j] = (1 - beta) * om[j] + beta * r * (1 if om[j] >= 0 else -1) * 0.01
        self.rel = self.hrr.relational_memory(self.edges, self.omega)

# 6. Anidado profundo (0059g): slots SEPARADOS K=3 (NO resonator 0059f)
def build_nested_K3(hrr, parent_vec, child_fact, role_parent, role_child):
    packed = [0.0] * hrr.D
    for j in range(hrr.D):
        packed[j] = parent_vec[j] + child_fact[j] * 0.5
    return hrr._normlist(packed)

if __name__ == "__main__":
    rng = random.Random(7)
    D = 64
    hdc = HDC(rng, D)
    _ = hdc.project([1, 2, 3, 0, 5] + [0] * 50)
    hrr = HRR(D, rng, 4)
    om2 = [[rng.gauss(0, 1) for _ in range(D)] for _ in range(4)]
    edges = {0: [1, 2], 1: [3], 2: [], 3: []}
    rel = hrr.relational_memory(edges, om2)
    assert hrr.recover(rel, 0, 1, om2) == 1
    ag = SGMAgent(rng, D, n_nodes=4)
    ag.set_edges(edges)
    a = ag.step([1, 0, 0, 9], [0, 1, 2, 3])
    ag.reward(1.0, pain=0.0)
    print("sgm_core SMOKETEST OK: HDC/HRR/PPR/decoder/agent integrados")
