import math

def integrar(step_fn, y0, steps=3000, dt=0.005):
    y=y0; maxabs=0.0
    for t in range(steps):
        y=step_fn(y,dt)
        # tolerar estado como tupla o lista
        if isinstance(y,(tuple,list)): m=max(abs(v) for v in y)
        else: m=abs(y)
        maxabs=max(maxabs,m)
        if maxabs>1e6: break
    return maxabs

def lv_step(y,dt):
    x,yy=y
    a,b,c,d=1.1,0.4,0.1,0.1
    return (x+(a-b*yy)*x*dt, yy+(c*x-d)*yy*dt)

def ku_step(y,dt):
    N=len(y); K=1.0; om=[0.5*math.sin(i*1.3) for i in range(N)]
    dy=[om[i]+(K/N)*sum(math.sin(y[j]-y[i]) for j in range(N)) for i in range(N)]
    return tuple(y[i]+dy[i]*dt for i in range(N))

print("=== CONTROL NEGATIVO (Punto 1 del amigo) ===")
lv=integrar(lv_step,(10.0,5.0))
print("Lotka-Volterra SIN poda: max=%.1f => %s"%(lv,"ACOTADO" if lv<1e6 else "EXPLOTA"))
ku=integrar(ku_step,(0.1,0.2,0.3,0.4,0.5,0.6))
print("Kuramoto SIN poda (N=6): max=%.1f => %s"%(ku,"ACOTADO" if ku<1e6 else "EXPLOTA"))
print("")
print("Si AMBOS acotados => el molde de la Tripleada NO distingue (lo confirma en genericos).")
print("Eso debilita la Tripleada como firma unificadora: habria que decir que es un")
print("patron de SISTEMAS ESTABLES, no una firma exclusiva de NS/Collatz/etc.")
print("Si alguno explota => el molde SI requiere estructura especifica.")
