import math
# LEMA FUERTE: G acotada => alpha(k) >= 3+eps (no aplanamiento del espectro)
# Medimos alpha efectiva por anillos en sim 3D con y sin el regulador G (eta).
def sim3d(N=10, nu=0.03, steps=80, usar_G=True):
    modes=[]
    for kx in range(1,N):
        for ky in range(1,N):
            for kz in range(1,N):
                k=math.sqrt(kx*kx+ky*ky+kz*kz)
                if k<N: modes.append((kx,ky,kz,k))
    n=len(modes)
    E=[1.0/(m[3]**2) for m in modes]
    Gmax=0.0
    for t in range(steps):
        T=[0.0]*n
        for i in range(n):
            kk=modes[i][3]
            for j in range(n):
                if 1.8< modes[j][3]/kk <2.2:
                    T[i]+=0.05*kk*(E[i]**1.5)*(E[j]-E[i]); break
        D=[2*nu*(m[3]**2)*E[i] for i,m in enumerate(modes)]
        G=0.0
        if usar_G:
            for i in range(n):
                kk=modes[i][3]
                vals=[]
                for j in range(n):
                    if 0.85< modes[j][3]/kk <1.15 and j!=i:
                        vals.append((math.log(E[j])-math.log(E[i]))/(math.log(modes[j][3])-math.log(kk)+1e-9))
                if vals: G+=(sum(vals)/len(vals))**2
            Gmax=max(Gmax,G)
            eta=1.0/(1.0+G)
        else:
            eta=1.0
        for i in range(n):
            E[i]+=(eta*T[i]-D[i])*0.01
            if E[i]<1e-12: E[i]=1e-12
    # pendiente efectiva por anillos
    ks=sorted(set(m[3] for m in modes))
    alphas=[]
    for k0 in ks:
        ks_in=[m for m in modes if abs(m[3]-k0)<0.5]
        if len(ks_in)>=2:
            lx=[math.log(m[3]) for m in ks_in]; ly=[math.log(E[i]) for i,m in enumerate(modes) if abs(m[3]-k0)<0.5]
            # ordenar
            pair=sorted(zip(lx,ly))
            lx=[p[0] for p in pair]; ly=[p[1] for p in pair]
            nn=len(lx); mx=sum(lx)/nn; my=sum(ly)/nn
            num=sum((lx[i]-mx)*(ly[i]-my) for i in range(nn))
            den=sum((lx[i]-mx)**2 for i in range(nn))
            alphas.append(-num/den if den>0 else 0)
    return Gmax, min(alphas) if alphas else 0, alphas

Gc, amin_c, _ = sim3d(usar_G=True)
Gs, amin_s, _ = sim3d(usar_G=False)
print("CON regulador G (Tercer Motor): Gmax=%.1f  alpha_min=%.3f"%(Gc,amin_c))
print("SIN regulador G (eta=1):        Gmax=NA    alpha_min=%.3f"%(amin_s))
print("")
print("Lema fuerte: G acotada => alpha >= 3+eps?")
print("alpha_min con G = %.3f (esperado >3 para regularidad)"%amin_c)
print("alpha_min sin G = %.3f (deberia ser menor si G evita aplanamiento)"%amin_s)
print("Si amin_c > amin_s => G mantiene pendiente mas inclinada => no aplanamiento.")
print("Si amin_c > 3 => H1 acotada => regularidad por confinamiento espectral.")
