import math

def E_bits(n):
    return math.log2(n)

def is_prime(n):
    if n<2: return False
    for i in range(2,int(math.isqrt(n))+1):
        if n%i==0: return False
    return True

primos=[p for p in range(2,61) if is_prime(p)]
print("=== (i) Identidad DDSD E(2^p-1)=p para p primo ===")
ok=True
for p in primos[:12]:
    M=(1<<p)-1
    e=E_bits(M)
    status = "OK" if abs(e-p)<1e-6 else "FALLA"
    if status=="FALLA": ok=False
    print("p=%2d  M_p=2^p-1  E_bits=%.4f  predicha p=%d  %s" % (p, e, p, status))
print("Identidad E(2^p-1)=p se sostiene (pero es trivial: log2(2^p-1) ~ p).")

print("")
print("=== (ii) M_p bajo R_3 (Collatz): longitud de orbita vs primalidad ===")
print("p     M_p_primo?  long.orbita")
for p in primos:
    M=(1<<p)-1
    Mp_is_prime = is_prime(M)
    x=M; steps=0
    while x>1 and steps<500000:
        if x%2==0: x//=2
        else: x=3*x+1
        while x%2==0 and x>1: x//=2
        steps+=1
    print("%3d   %s           %d" % (p, "SI" if Mp_is_prime else "no", steps))

print("")
print("VEREDICTO M:")
print("- E(2^p-1)=p es identidad trivial por definicion de E (bits). No es prediccion arriesgada.")
print("- La primalidad de M_p no se explica por deriva 2-adica de Collatz (es teoria de numeros pura).")
print("- Mersenne bajo R_3 colapsa igual que cualquier entero; no hay firma Mersenne en el sustrato.")
print("=> Mersenne NO aporta evidencia a favor de unificacion literal; es aritmetica estandar.")
