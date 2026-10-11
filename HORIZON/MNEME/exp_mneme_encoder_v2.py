#!/usr/bin/env python3
# exp_mneme_encoder_v2.py — el encoder por co-activaciones reales.
# REDISENO tras M1c FAIL (hash de nombres no codifica semantica del grafo).
# Idea: el hipervector de un nodo deriva de SU VECINDAD REAL:
#   phase(nodo_i) = angulo del patron de co-activacion de i contra
#   los demas (vector de pesos normalizado -> fase). Nodos con vecindades
#   solapadas comparten fase parcialmente => la superposicion de X contiene
#   traza genuina de su 2do anillo.
import sys, random, json, time
sys.path.insert(0, "/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM")
import numpy as np

D = 2048   # fase por co-activacion: menos dimension, mas senal por dim
t0 = time.time()

from sgm.core.sgm_core import SGMAgentCore
sgm = SGMAgentCore(random.Random(42), D=128, n_nodes=64, gamma=0.01)
sgm.cargar("/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/pandora/runtime/data/nucleo_checkpoint.npy")
co = sgm.co_activacion
print(f"grafo: {len(co)} pares, D_bundle={D}", flush=True)

# ---- construir la matriz de adyacencia ponderada de co-activacion ----
nodos_all = sorted({i for par in co for i in par})
idx_of = {n: i for i, n in enumerate(nodos_all)}
N = len(nodos_all)
W = np.zeros((N, N))
for (a, b), w in co.items():
    ia, ib = idx_of[a], idx_of[b]
    W[ia, ib] = max(W[ia, ib], w)
    W[ib, ia] = max(W[ib, ia], w)
# normalizar filas: el patron de cada nodo
norms = np.linalg.norm(W, axis=1, keepdims=True)
norms[norms == 0] = 1
Wn = W / norms

# ---- el codebook por co-activacion: hipervector_i = Wn[i] como fase ----
# cada entrada del patron de i es un ANGULO (determinista del peso),
# dispersado en el hipervector por un kernel aleatorio fijo
def kernel(N, D, seed=7):
    rng = np.random.default_rng(seed)
    K = rng.standard_normal((N, D))
    K /= np.linalg.norm(K, axis=1, keepdims=True)
    return K

K = kernel(N, D)
# fase: patron proyectado -> atan2-style: la direccion dominante del nodo
# codifica SU vecindad; nodos vecinos comparten componentes -> similitud
CB = Wn @ K          # (N, D): hipervector por co-activacion
CB /= np.linalg.norm(CB, axis=1, keepdims=True) + 1e-12

def bind(a, b):
    return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real
def unbind(c, r):
    return np.fft.ifft(np.fft.fft(c) * np.conj(np.fft.fft(r))).real

role_s = np.random.default_rng(1).standard_normal(D); role_s /= np.linalg.norm(role_s)
role_o = np.random.default_rng(2).standard_normal(D); role_o /= np.linalg.norm(role_o)

def cleanup(v, cb_arr, names):
    sims = cb_arr @ v / (np.linalg.norm(cb_arr, axis=1) * np.linalg.norm(v) + 1e-12)
    return names[int(np.argmax(sims))], float(sims.max()), sims

# ==== TEST 1 (regresion M1a): cleanup de 1 simbolo ====
rng = random.Random(7)
ok = 0
for _ in range(200):
    i = rng.randrange(N)
    bundle = bind(role_s, CB[i])
    est = unbind(bundle, role_s)
    pred, _, _ = cleanup(est, CB, nodos_all)
    ok += (pred == nodos_all[i])
acc1 = ok / 200
print(f"TEST-1 cleanup (co-act encoder): {acc1:.4f} ({'PASS' if acc1 >= 0.99 else 'FAIL'})", flush=True)

# ==== TEST 2 (regresion M1b): k=8 roles ====
vistos = set(); top_rel = []
for k, w in sorted(co.items(), key=lambda kv: -kv[1]):
    canon = tuple(sorted(k))
    if canon not in vistos:
        vistos.add(canon); top_rel.append((canon, w))
    if len(top_rel) >= 8: break
bundle8 = np.zeros(D)
for (a, b), w in top_rel:
    bundle8 += (w / top_rel[0][1]) * bind(role_s, CB[idx_of[a]])
    bundle8 += (w / top_rel[0][1]) * bind(role_o, CB[idx_of[b]])
est_s = unbind(bundle8, role_s)
est_o = unbind(bundle8, role_o)
def rank5(v, target):
    _, _, sims = cleanup(v, CB, nodos_all)
    orden = np.argsort(-sims)[:5]
    return target in [nodos_all[i] for i in orden]
top5 = sum(1 for (a, b), _ in top_rel if rank5(est_s, a)) + sum(1 for (a, b), _ in top_rel if rank5(est_o, b))
acc2 = top5 / 16
print(f"TEST-2 k=8 top-5: {acc2:.4f} ({'PASS' if acc2 >= 0.85 else 'FAIL'})", flush=True)

# ==== TEST 3 (EL REDISENO: multi-hop) ====
vecinos = {}
med = np.median(list(co.values()))
for (a, b), w in co.items():
    if w > med:
        vecinos.setdefault(a, set()).add(b)
        vecinos.setdefault(b, set()).add(a)
casos = []
rng2 = random.Random(11)
for x in rng2.sample(list(vecinos.keys()), min(400, len(vecinos))):
    ys = vecinos.get(x, set())
    zs = set()
    for y in ys:
        zs |= vecinos.get(y, set())
    zs -= ys; zs.discard(x)
    if zs:
        z = rng2.choice(sorted(zs))
        casos.append((x, z))
print(f"casos multi-hop: {len(casos)}", flush=True)
# consulta: bundle = superposicion del 1er anillo de X (solo binds de vecinos)
hit = 0
for x, z in casos:
    bundle_v = np.zeros(D)
    for v in vecinos.get(x, set()):
        bundle_v += bind(role_o, CB[idx_of[v]])
    est_v = unbind(bundle_v, role_o)
    _, _, sims = cleanup(est_v, CB, nodos_all)
    orden = np.argsort(-sims)[:5]
    hit += (z in [nodos_all[i] for i in orden])
acc3 = hit / max(1, len(casos))
print(f"TEST-3 multi-hop (co-act encoder): {acc3:.4f} ({'PASS' if acc3 >= 0.3 else 'FAIL'} — vs hash: 0.027)", flush=True)

res = {"encoder": "co-activaciones", "D": D, "T1_cleanup": acc1, "T2_top5_k8": acc2,
       "T3_multihop": acc3, "n_casos": len(casos), "vs_hash": 0.027, "tiempo_s": time.time()-t0}
with open("/home/delorien/vaults/vega-vault/HORIZON/MNEME/data_encoder_v2.json", "w") as f:
    json.dump(res, f, indent=1)
print("ENCODER_V2_DONE", flush=True)
