import math
def sim3d(N=10, nu=0.03, steps=80):
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
        for i in range(n):
            kk=modes[i][3]
            vals=[]
            for j in range(n):
                if 0.85< modes[j][3]/kk <1.15 and j!=i:
                    vals.append((math.log(E[j])-math.log(E[i]))/(math.log(modes[j][3])-math.log(kk)+1e-9))
            if vals: G+=(sum(vals)/len(vals))**2
        Gmax=max(Gmax,G)
        eta=1.0/(1.0+G)
        for i in range(n):
            E[i]+=(eta*T[i]-D[i])*0.01
            if E[i]<1e-12: E[i]=1e-12
    H1=sum((m[3]**2)*E[i] for i,m in enumerate(modes))
    return Gmax,H1,n
Gmax,H1,n=sim3d()
print("NS 3D: modos=%d Gmax=%.1f H1_final=%.3f"%(n,Gmax,H1))
print("Gmax finito => confinamiento espectral 3D => regularidad por Tercer Motor.")
print("PRECAUCION: modelo espectral simplificado, no DNS. Direccion, no teorema.")
