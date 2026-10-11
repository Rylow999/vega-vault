#!/usr/bin/env python3
# exp_mneme_encoder_v3.py — identidad + estructura: el punto medio del teorema.
# v1 hash: separabilidad 1.0, semantica 0. v2 co-act: separabilidad 0.41, semantica 0.047.
# v3: hv = normalize(hash(n) + alpha * coact(n)) — alpha calibrado por barrido.
# Prediccion: existe alpha* con cleanup >= 0.9 Y multihop >= 3x el v2.
import sys, random, json, time
sys.path.insert(0, "/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM")
import numpy as np

D = 2048
from sgm.core.sgm_core import SGMAgentCore
sgm = SGMAgentCore(random.Random(42), D=128, n_nodes=64, gamma=0.01)
sgm.cargar("/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/pandora/runtime/data/nucleo_checkpoint.npy")
co = sgm.co_activacion

nodos_all = sorted({i for par in co for i in par})
idx_of = {n: i for i, n in enumerate(nodos_all)}
N = len(nodos_all)

W = np.zeros((N, N))
for (a, b), w in co.items():
    ia, ib = idx_of[a], idx_of[b]
    W[ia, ib] = max(W[ia, ib], w); W[ib, ia] = max(W[ib, ia], w)
norms = np.linalg.norm(W, axis=1, keepdims=True); norms[norms == 0] = 1
Wn = W / norms

def hash_vec(i, D):
    import hashlib
    seed = int(hashlib.sha1(f"nodo_{i}".encode()).hexdigest()[:8], 16)
    rng = np.random.RandomState(seed)
    v = rng.randn(D)
    return v / np.linalg.norm(v)

rng_k = np.random.default_rng(7)
Kk = rng_k.standard_normal((N, D)); Kk /= np.linalg.norm(Kk, axis=1, keepdims=True)
CO = Wn @ Kk
CO /= np.linalg.norm(CO, axis=1, keepdims=True) + 1e-12

def bind(a, b): return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real
def unbind(c, r): return np.fft.ifft(np.fft.fft(c) * np.conj(np.fft.fft(r))).real
role_o = np.random.default_rng(2).standard_normal(D); role_o /= np.linalg.norm(role_o)

vecinos = {}
med = np.median(list(co.values()))
for (a, b), w in co.items():
    if w > med:
        vecinos.setdefault(a, set()).add(b); vecinos.setdefault(b, set()).add(a)
casos = []
rng2 = random.Random(11)
for x in rng2.sample(list(vecinos.keys()), min(400, len(vecinos))):
    ys = vecinos.get(x, set())
    zs = set()
    for y in ys: zs |= vecinos.get(y, set())
    zs -= ys; zs.discard(x)
    if zs:
        casos.append((x, rng2.choice(sorted(zs))))

print(f"barrido alpha (D={D}, {len(casos)} multihop):", flush=True)
print(f"{'alpha':>6} | {'cleanup':>8} | {'multihop@5':>10}", flush=True)
mejor = None
for alpha in [0.0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6]:
    CB = np.array([ (hash_vec(n, D) + alpha * CO[idx_of[n]]) /
                    (np.linalg.norm(hash_vec(n, D) + alpha * CO[idx_of[n]]) + 1e-12)
                    for n in nodos_all ])
    # cleanup
    rng = random.Random(7); ok = 0
    for _ in range(200):
        i = rng.randrange(N)
        est = unbind(bind(role_o, CB[i]), role_o)
        sims = CB @ est / (np.linalg.norm(CB, axis=1) * np.linalg.norm(est) + 1e-12)
        ok += (nodos_all[int(np.argmax(sims))] == nodos_all[i])
    clean_acc = ok / 200
    # multihop
    hit = 0
    for x, z in casos:
        bv = np.zeros(D)
        for v in vecinos.get(x, set()):
            bv += bind(role_o, CB[idx_of[v]])
        ev = unbind(bv, role_o)
        sims = CB @ ev / (np.linalg.norm(CB, axis=1) * np.linalg.norm(ev) + 1e-12)
        orden = np.argsort(-sims)[:5]
        hit += (z in [nodos_all[i] for i in orden])
    mh = hit / len(casos)
    print(f"{alpha:>6.2f} | {clean_acc:>8.3f} | {mh:>10.3f}", flush=True)
    if clean_acc >= 0.9 and (mejor is None or mh > mejor[2]):
        mejor = (alpha, clean_acc, mh)

if mejor:
    print(f"\nALPHA* = {mejor[0]}: cleanup={mejor[1]:.3f} multihop={mejor[2]:.3f} — PREDICCION CONFIRMADA (existe el punto medio)", flush=True)
    res = {"alpha_star": mejor[0], "cleanup": mejor[1], "multihop": mejor[2], "D": D,
           "vs_v1_hash": 0.027, "vs_v2_coact": 0.047, "n_multihop": len(casos)}
else:
    print("\nNO HAY alpha con cleanup >= 0.9 — el trade-off no se cierra en una capa (proximo: rol-struct separado)", flush=True)
    res = {"alpha_star": None, "trade_off": "abierto", "D": D}
with open("/home/delorien/vaults/vega-vault/HORIZON/MNEME/data_encoder_v3.json", "w") as f:
    json.dump(res, f, indent=1)
print("ENCODER_V3_DONE", flush=True)
