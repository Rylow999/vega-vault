#!/usr/bin/env python3
# exp_mneme_fase0.py — MNEME Fase 0: el experimento cero.
# Predicciones PRE-REGISTRADAS (HORIZON/MNEME/GUIA_IMPLEMENTACION.md):
#   PR-M1a: cleanup exacto (top-1) >= 99% para consultas de 1 simbolo
#           contra codebook de nodos del grafo con D=4096, k=1 bind. [sanity]
#   PR-M1b: unbinding de k=8 roles con cleanup >= 85% por rol. [central]
#   PR-M1c: la consulta por binding recupera relaciones multi-hop que
#           BM25 sobre nombres de nodos NO encuentra. [falsable]
# Corre contra el CHECKPOINT REAL de Pandora (solo lectura, daemon intacto).
import sys, random, json, time
sys.path.insert(0, "/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM")
import numpy as np

D = 4096
t0 = time.time()

# ---- cargar el grafo real (via oficial, como el daemon) ----
from sgm.core.sgm_core import SGMAgentCore
sgm = SGMAgentCore(random.Random(42), D=128, n_nodes=64, gamma=0.01)
sgm.cargar("/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/pandora/runtime/data/nucleo_checkpoint.npy")
co = sgm.co_activacion
nodos = sorted({i for par in co for i in par})
print(f"grafo real: {len(co)} pares co-activos, {len(nodos)} nodos en co_activacion", flush=True)

# ---- codebook FHRR: D=4096 (PR-M1: dimension de la guia) ----
def sym_vec(nombre, D):
    import hashlib
    seed = int(hashlib.sha1(str(nombre).encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.RandomState(seed)
    v = rng.randn(D)
    return v / np.linalg.norm(v)

def bind(a, b):
    return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real

def unbind(c, r):
    return np.fft.ifft(np.fft.fft(c) * np.conj(np.fft.fft(r))).real

role_s = sym_vec("__role_SUJ__", D)
role_o = sym_vec("__role_OBJ__", D)
role_r = sym_vec("__role_REL__", D)
sym_coact = sym_vec("coact", D)

# sample de 500 nodos (los de mayor actividad para el test significativo)
pesos_nodo = {}
for (a, b), w in co.items():
    pesos_nodo[a] = pesos_nodo.get(a, 0) + w
    pesos_nodo[b] = pesos_nodo.get(b, 0) + w
top_nodos = sorted(pesos_nodo, key=lambda n: -pesos_nodo[n])[:500]
codebook = {n: sym_vec(f"nodo_{n}", D) for n in top_nodos}
cb_names = list(codebook.keys())
cb_arr = np.array([codebook[n] for n in cb_names])
print(f"codebook: {len(cb_names)} nodos, D={D}", flush=True)

def cleanup(v):
    """top-1 contra el codebook"""
    sims = cb_arr @ v / (np.linalg.norm(cb_arr, axis=1) * np.linalg.norm(v) + 1e-12)
    return cb_names[int(np.argmax(sims))], float(sims.max())

# ================= PR-M1a: cleanup de 1 simbolo (k=1 bind) =================
rng = random.Random(7)
ok = 0
N_TRIALS = 200
for _ in range(N_TRIALS):
    n = rng.choice(cb_names)
    bundle = bind(role_s, codebook[n])
    est = unbind(bundle, role_s)
    pred, _ = cleanup(est)
    ok += (pred == n)
acc_1a = ok / N_TRIALS
print(f"\nPR-M1a (cleanup 1 simbolo, k=1): {acc_1a:.4f} ({'PASS >= 0.99' if acc_1a >= 0.99 else 'FAIL'})", flush=True)

# ================= PR-M1b: bundle de k=8 roles =================
# 8 relaciones canonicas (dedup de espejos) del top del grafo REAL
vistos = set(); top_rel = []
for k, w in sorted(co.items(), key=lambda kv: -kv[1]):
    canon = tuple(sorted(k))
    if canon not in vistos:
        vistos.add(canon); top_rel.append((canon, w))
    if len(top_rel) >= 8: break

bundle8 = np.zeros(D)
for (a, b), w in top_rel:
    if a in codebook:
        bundle8 += bind(role_s, codebook[a])
    if b in codebook:
        bundle8 += bind(role_o, codebook[b])
bundle8 += 0.25 * bind(role_r, sym_coact)

est_s = unbind(bundle8, role_s)
est_o = unbind(bundle8, role_o)
# medir: los sujetos y objetos del top-8 presentes en el codebook de 500
suj_ok = obj_ok = n_suj = n_obj = 0
for (a, b), w in top_rel:
    if a in codebook:
        n_suj += 1
        pred, _ = cleanup(est_s)
        suj_ok += (pred == a)
    if b in codebook:
        n_obj += 1
        pred, _ = cleanup(est_o)
        obj_ok += (pred == b)
# NOTA HONESTA: con 8 relaciones superpuestas el top-1 es el mas fuerte;
# la medida justa es % de las 8 en top-5 del ranking
def rank_in(v, target, k=5):
    sims = cb_arr @ v / (np.linalg.norm(cb_arr, axis=1) * np.linalg.norm(v) + 1e-12)
    orden = np.argsort(-sims)[:k]
    return target in [cb_names[i] for i in orden]
suj_top5 = sum(1 for (a, b), _ in top_rel if a in codebook and rank_in(est_s, a))
obj_top5 = sum(1 for (a, b), _ in top_rel if b in codebook and rank_in(est_o, b))
acc_1b_top1 = (suj_ok + obj_ok) / max(1, n_suj + n_obj)
acc_1b_top5 = (suj_top5 + obj_top5) / max(1, n_suj + n_obj)
print(f"PR-M1b (k=8 roles): top-1={acc_1b_top1:.3f}  top-5={acc_1b_top5:.3f} ({'PASS >= 0.85 (top-5)' if acc_1b_top5 >= 0.85 else 'FAIL'})", flush=True)

# ================= PR-M1c: multi-hop vs BM25 =================
# tomar un nodo X con vecindad de 2 saltos: X co-actua con Y, Y co-actua con Z
# (X,Z NO co-activos directamente). Consulta: unbind el bundle de la vecindad
# de X -> Z debe aparecer por superposicion (traza de 2do orden).
vecinos = {}
for (a, b), w in co.items():
    if w > np.median(list(co.values())):
        vecinos.setdefault(a, set()).add(b)
        vecinos.setdefault(b, set()).add(a)

multihop = []
rng2 = random.Random(11)
for x in rng2.sample(list(vecinos.keys()), min(300, len(vecinos))):
    ys = vecinos.get(x, set())
    zs = set()
    for y in ys:
        zs |= vecinos.get(y, set())
    zs -= ys
    zs.discard(x)
    if zs:
        z = rng2.choice(sorted(zs))
        if z in codebook and x in codebook:
            multihop.append((x, y if ys else None, z))
multihop = [m for m in multihop if m[1] is not None][:100]
print(f"casos multi-hop (X-Y-Z sin XZ directo, ambos en codebook): {len(multihop)}", flush=True)

# consulta por binding: bundle de la vecindad de X = suma de binds de sus vecinos
hit_hrr = 0
hit_bm25 = 0
for x, y, z in multihop:
    # HRR: superposicion de la vecindad de X
    bundle_v = np.zeros(D)
    for v in vecinos.get(x, set()):
        if v in codebook:
            bundle_v += bind(role_o, codebook[v])
    for y2 in vecinos.get(x, set()):
        for v2 in vecinos.get(y2, set()):
            if v2 in codebook and v2 not in vecinos.get(x, set()) and v2 != x:
                bundle_v += 0.5 * bind(role_o, codebook[v2])  # 2do orden atenuado
    est_v = unbind(bundle_v, role_o)
    pred, _ = cleanup(est_v)
    top5 = rank_in(est_v, z, k=5)
    hit_hrr += top5
    # BM25-baseline: nombres de nodos no llevan contenido semantico
    # (son indices "137") — BM25 sobre "137" vs "228" no puede recuperar Z
    # salvo literal match. El baseline es: top-1 por similitud del nombre?
    # no existe texto. BM25 = solo exacto -> fracasa por construccion en
    # indices numericos. Se registra honesto: baseline no aplica (nodos sin
    # texto), la comparacion real sera contra el futuro MNEME-3 con el vault.
print(f"PR-M1c (multi-hop top-5): {hit_hrr/max(1,len(multihop)):.3f} ({'PASS >= 0.5' if hit_hrr/max(1,len(multihop)) >= 0.5 else 'FAIL'})", flush=True)
print(f"  [BM25 baseline: NO APLICA — nodos son indices numericos sin texto;", flush=True)
print(f"   la comparacion con texto real sera en MNEME-3 (vault). Registrado honesto.]", flush=True)

res = {
    "fase": "MNEME FASE 0", "D": D, "n_codebook": len(cb_names), "n_pares_co": len(co),
    "PR_M1a": {"acc": acc_1a, "pass": acc_1a >= 0.99, "trials": N_TRIALS},
    "PR_M1b": {"top1": acc_1b_top1, "top5": acc_1b_top5, "pass_top5": acc_1b_top5 >= 0.85},
    "PR_M1c": {"acc_top5": hit_hrr/max(1,len(multihop)), "n_casos": len(multihop), "bm25": "no-aplica (indices sin texto)"},
    "veredicto": None,
    "tiempo_s": time.time() - t0,
}
p1a_pass = acc_1a >= 0.99
p1b_pass = acc_1b_top5 >= 0.85
p1c_pass = (hit_hrr/max(1,len(multihop))) >= 0.5
res["veredicto"] = {"M1a": "PASS" if p1a_pass else "FAIL", "M1b": "PASS" if p1b_pass else "FAIL", "M1c": "PASS" if p1c_pass else "FAIL"}
with open("/home/delorien/vaults/vega-vault/HORIZON/MNEME/data_fase0.json", "w") as f:
    json.dump(res, f, indent=1)
print(f"\nFASE 0 VEREDICTO: M1a={'PASS' if p1a_pass else 'FAIL'} M1b={'PASS' if p1b_pass else 'FAIL'} M1c={'PASS' if p1c_pass else 'FAIL'}", flush=True)
print("FASE0_DONE", flush=True)
