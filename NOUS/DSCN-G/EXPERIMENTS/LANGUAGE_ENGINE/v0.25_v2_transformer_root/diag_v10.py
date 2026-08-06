#!/usr/bin/env python3
import random, math, sys
sys.path.insert(0,"/data/user/0/com.hermesagent.android/files/home")
import run_v03real as R3
import run_v10 as R10

def vitality_stats(eng):
    vs=[n.vitality for n in eng.nodes if n.alive]
    return min(vs) if vs else 0, sum(1 for n in eng.nodes if n.hibernated)

print("=== v0.3 REAL v2 engine (N=10) ===")
e3=R3.Engine(10,seed=0)
for t in range(2000): e3.step()
print("min vit:",round(vitality_stats(e3)[0],3),"hibernados:",vitality_stats(e3)[1],"activos:",sum(1 for n in e3.nodes if n.alive))

print("=== v0.10 engine (N=10) ===")
e10=R10.Engine(10,seed=0)
for t in range(2000): e10.step()
print("min vit:",round(vitality_stats(e10)[0],3),"hibernados:",vitality_stats(e10)[1],"activos:",sum(1 for n in e10.nodes if n.alive))

# muestra de vitalidad de v0.10 a distintos t
print("=== v0.10 vitalidad en t=200,500,1000,1999 ===")
e=R10.Engine(10,seed=0)
for t in range(2000):
    e.step()
    if t+1 in (200,500,1000,1999):
        vs=sorted(round(n.vitality,3) for n in e.nodes)
        print(f"t={t+1}: {vs}")
