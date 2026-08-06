import math
def G_star(Re, N=24, steps=120):
    # nu derivado de Re: nu ~ U*L/Re, tomamos nu = 1.0/Re para el barrido
    nu = 1.0/Re if Re>0 else 0.1
    modes=[]
    for kx in range(1,N):
        for ky in range(1,N):
            k=math.hypot(kx,ky)
            if k<N: modes.append((kx,ky,k))
    n=len(modes)
    E=[1.0/(m[2]**2) for m in modes]
    Gs=[]
    for t in range(steps):
        T=[0.0]*n
        for i in range(n):
            kk=modes[i][2]
            for j in range(n):
                if 1.8< modes[j][2]/kk <2.2:
                    T[i]+=0.05*kk*(E[i]**1.5)*(E[j]-E[i]); break
        D=[2*nu*(m[2]**2)*E[i] for i,m in enumerate(modes)]
        G=0.0
        for i in range(n):
            kk=modes[i][2]
            vals=[]
            for j in range(n):
                if 0.85< modes[j][2]/kk <1.15 and j!=i:
                    vals.append((math.log(E[j])-math.log(E[i]))/(math.log(modes[j][2])-math.log(kk)+1e-9))
            if vals: G+=(sum(vals)/len(vals))**2
        Gs.append(G)
        eta=1.0/(1.0+G)
        for i in range(n):
            E[i]+=(eta*T[i]-D[i])*0.01
            if E[i]<1e-12: E[i]=1e-12
    # plateau: promedio del ultimo 30%
    tail=Gs[int(0.7*len(Gs)):]
    return sum(tail)/len(tail)

print("Barrido de Reynolds (2D, N=24): G* vs Re")
print("Re       G*")
for Re in [5,10,20,30,50,70,100,150,200]:
    g=G_star(Re)
    print("%4d   %.1f"%(Re,g))
print("")
print("Buscamos el Re donde G* se estabiliza (plateau) => 2^phi de NS.")
print("Si hay un Re optimo (minimo o plateau) => escala dorada análoga a 2^phi~3.694.")
