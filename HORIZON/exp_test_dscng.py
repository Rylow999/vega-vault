#!/usr/bin/env python3
# exp_test_dscng.py — EL TEST DE LA PREDICCION FALSABLE DE HORIZON.
#
# Prediccion (INFORME_INTEGRADO Ap. C.4): "el punto critico de colapso
# depende del metodo de medicion" — con evidencia previa en fhrr
# (placement cambia el resultado: 0.16 vs 0.985) y SDDF (detector puntual
# vs suavizado cortan distinto).
#
# Test en DSCN-G: el grafo real de Pandora, la senal E_i = energia de
# activacion del nodo i medida con TRES instrumentos:
#   A) full: E_i = vitalidad_i * |coact_i| (todo el grafo)
#   B) topk: E_i = vitalidad_i * sum de top-k coactivaciones
#   C) local: E_i = vitalidad_i * (coact con vecinos directos del root)
# Se mide el "umbral de emergencia": cuantos nodos superan theta para
# cada instrumento. Si el SET de nodos emergentes CAMBIA con el
# instrumento -> prediccion CONFIRMADA en el 3er dominio.
import sys, random, json, time
import numpy as np

sys.path.insert(0, "/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM")
from sgm.core.sgm_core import SGMAgentCore

sgm = SGMAgentCore(random.Random(42), D=128, n_nodes=64, gamma=0.01)
sgm.cargar("/home/delorien/vaults/vega-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/pandora/runtime/data/nucleo_checkpoint.npy")

t0 = time.time()
vit = np.array(sgm.vitalidad)
co = sgm.co_activacion
n = len(vit)

# instrumento A: full co-activacion (suma de todos los pesos del nodo)
full = np.zeros(n)
for (a, b), w in co.items():
    full[a] += w; full[b] += w

# instrumento B: top-k (solo las k=5 coactivaciones mas fuertes)
topk = np.zeros(n)
por_nodo = {}
for (a, b), w in co.items():
    por_nodo.setdefault(a, []).append(w)
    por_nodo.setdefault(b, []).append(w)
for i, ws in por_nodo.items():
    topk[i] = sum(sorted(ws, reverse=True)[:5])

# instrumento C: local (solo coactivos con el root/vecinos del root)
phi_root = int(sgm.phi_root) % n
root_vecs = set()
for (a, b), w in co.items():
    if w > np.median(list(co.values())):
        if a == phi_root: root_vecs.add(b)
        if b == phi_root: root_vecs.add(a)
local = np.zeros(n)
for (a, b), w in co.items():
    if w > np.median(list(co.values())):
        if a in root_vecs or a == phi_root: local[a] += w
        if b in root_vecs or b == phi_root: local[b] += w

# el "umbral de emergencia": normalizamos cada instrumento y medimos
# el SET de nodos que supera theta para un rango de theta
def norm(x):
    mx = x.max()
    return x / mx if mx > 0 else x

EA, EB, EC = norm(vit * full), norm(vit * topk), norm(vit * local)

print("== TEST DSCN-G: umbral de emergencia vs instrumento ==", flush=True)
print(f"grafo: {n} nodos, root={phi_root}, {len(root_vecs)} vecinos del root", flush=True)

resultados = {"prediccion": "el set de nodos emergentes depende del instrumento",
              "instrumentos": {}}
for nombre, E in [("A_full", EA), ("B_topk", EB), ("C_local", EC)]:
    sets = {}
    for theta in [0.3, 0.5, 0.7, 0.9]:
        S = set(int(i) for i in np.where(E >= theta)[0])
        sets[str(theta)] = sorted(S)
    resultados["instrumentos"][nombre] = sets
    print(f"\n  {nombre}: distribucion E (med={np.median(E[E>0]):.4f} max={E.max():.4f} nnz={(E>0).sum()})", flush=True)
    for th, S in sets.items():
        print(f"    theta={th}: {len(S)} nodos emergentes {S[:8]}{'...' if len(S)>8 else ''}", flush=True)

# LA MEDIDA: Jaccard entre sets de A vs B vs C a theta=0.5
def jaccard(s1, s2):
    s1, s2 = set(s1), set(s2)
    return len(s1 & s2) / max(1, len(s1 | s2))
SA, SB, SC = set(resultados["instrumentos"]["A_full"]["0.5"]), set(resultados["instrumentos"]["B_topk"]["0.5"]), set(resultados["instrumentos"]["C_local"]["0.5"])
jAB, jAC, jBC = jaccard(SA, SB), jaccard(SA, SC), jaccard(SB, SC)
print(f"\nJaccard(theta=0.5): A-B={jAB:.3f}  A-C={jAC:.3f}  B-C={jBC:.3f}", flush=True)

# VEREDICTO: si los sets difieren sustancialmente (Jaccard < 0.5 en
# promedio), el umbral de emergencia ES propiedad del instrumento.
javg = (jAB + jAC + jBC) / 3
print(f"\npromedio Jaccard = {javg:.3f}", flush=True)
if javg < 0.5:
    print("VEREDICTO: CONFIRMADA — el set de emergentes depende del instrumento", flush=True)
    resultados["veredicto"] = "CONFIRMADA"
elif javg > 0.8:
    print("VEREDICTO: REFUTADA — el umbral es robusto al instrumento (marco descriptivo)", flush=True)
    resultados["veredicto"] = "REFUTADA"
else:
    print("VEREDICTO: MIXTA — dependencia parcial (instrumento afecta pero no domina)", flush=True)
    resultados["veredicto"] = "MIXTA"
resultados["jaccard"] = {"AB": jAB, "AC": jAC, "BC": jBC, "avg": javg}
resultados["tiempo_s"] = time.time() - t0

with open("/home/delorien/vaults/vega-vault/HORIZON/test_dscng_resultado.json", "w") as f:
    json.dump(resultados, f, indent=1)
print("DSCNG_TEST_DONE", flush=True)
