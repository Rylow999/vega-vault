#!/usr/bin/env python3
import sys, math, random
sys.path.insert(0,"/data/user/0/com.hermesagent.android/files/home")
import run_v13 as R
D=8; BETA=0.20
seq,vocab=R.make_corpus(6000)
V=len(vocab); idx={w:i for i,w in enumerate(vocab)}
rng=random.Random(0)
omega=[[rng.gauss(0,1) for _ in range(D)] for _ in range(V)]
for i in range(1,len(seq)):
    a,b=seq[i-1],seq[i]; ia,ib=idx[a],idx[b]
    omega[ia]=[(1-BETA)*omega[ia][k]+BETA*omega[ib][k] for k in range(D)]
# distancia entre omega_base de banco y su contextualizacion por fondo vs madera
def norm(v): return math.sqrt(sum(x*x for x in v))
def cos(a,b):
    na=norm(a); nb=norm(b)
    return sum(x*y for x,y in zip(a,b))/(na*nb) if na>1e-9 and nb>1e-9 else 0
ob=omega[idx["banco"]]
cf=R.attention_ctx(omega,idx,["fondo"],"banco")
cm=R.attention_ctx(omega,idx,["madera"],"banco")
print("norm omega_base banco:",round(norm(ob),3))
print("norm ctx tras fondo:",round(norm(cf),3))
print("norm ctx tras madera:",round(norm(cm),3))
print("dist(ctx_fondo, ctx_madera):",round(norm([cf[i]-cm[i] for i in range(D)]),4))
print("cos(omega_base banco, ctx_fondo):",round(cos(ob,cf),3))
print("cos(omega_base banco, ctx_madera):",round(cos(ob,cm),3))
# tambien: distancia entre omega de 'fondo' y 'madera' (deberian ser distintos)
print("dist(fondo,madera):",round(norm([omega[idx['fondo']][i]-omega[idx['madera']][i] for i in range(D)]),3))
