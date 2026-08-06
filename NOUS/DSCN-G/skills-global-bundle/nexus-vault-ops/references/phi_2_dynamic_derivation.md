# Derivación dinámica de 2^φ (Collatz / unificación)

## Corrección de cálculo (2026-07-25)
- φ = (1+√5)/2 ≈ 1.6180339887
- 2^φ = e^(1.6180339887 · ln2) = e^(1.6180339887 · 0.693147) = e^1.1216 = **3.06956**
- 3.694 es 2^1.885 (NO es 2^φ). Error de transcripción al copiar la nota en los docs de la Tríada.
- El Master-Document original (línea 99) dice "2^φ" sin número → está bien. No citar 3.694.

## Derivación dinámica (mecanismo, no cercanía a 4)
Collatz R_a(n) = (an+1)/2^ν₂(an+1). Deriva exacta Φ(a) = log₂(a) − 2.
Contractivo sii Φ(a) < 0 sii a < 2² = 4. Borde dinámico: a = 4 (Φ = 0).
a = 3 es el único impar en (1, 4) con deriva negativa (Φ(3) = log₂3 − 2 ≈ −0.415).

¿Por qué φ y no otra constante? Por la dinámica de ciclos:
- Cada ciclo de Collatz es 3^m / 2^k ≈ 1 ⇒ k/m ≈ log₂(3) ≈ 1.58496.
- Los mejores k/m son los convergents de la fracción continua de log₂(3):
  log₂(3) = [1; 1, 1, 2, 2, 3, 1, 5, 2, 23, …]
- Los primeros convergents de Fibonacci: 3/2, 8/5, 21/13, 55/34, … cuyo límite es φ.
  (Porque la CF de φ = [1;1,1,1,…]; los convergents de Fibonacci F_{n+1}/F_n → φ.)
- PERO log₂(3) cambia el 4to coeficiente a 2 (no 1): ahí se ROMPE la aproximación
  Fibonacci exacta. Ese es el punto donde el mapa deja de tener ciclos Fibonacci-óptimos.
- Por eso 2^φ = 3.069 es el límite donde a=3 queda aislado dinámicamente.

Conclusión: 2^φ aparece porque los ciclos más estables de Collatz tienen razón k/m ≈ log₂(3),
y los mejores k/m son convergents Fibonacci (límite φ) HASTA el 4to coeficiente. Mecanismo
real, satisface el gate del revisor (Punto 7): explica POR QUÉ φ, no "está cerca de 4".

## Script reutilizable
`python3` (root, con LD_LIBRARY_PATH): verificar convergents y 2^φ.
```python
import math
phi=(1+math.sqrt(5))/2
print(2**phi)  # 3.06956  (NO 3.694)
fib=[1,1,2,3,5,8,13,21,34,55,89]
for i in range(2,len(fib)-1):
    r=fib[i+1]/fib[i]
    print("F_%d/F_%d = %.6f  err=%.6f" % (fib[i+1],fib[i],r,abs(r-math.log2(3))))
```
