# 2^phi — DERIVACION DINAMICA (Punto 7 del amigo, 2026-07-25)
# CORRECCION DE CALCULO: 2^phi = 3.069 (no 3.694). phi=(1+sqrt5)/2=1.618.
# 3.694 = 2^1.885, NO es 2^phi. El paper/vault que dice 3.694 tiene error de calculo.

## Derivacion dinamica (mecanismo, no cercania a 4)
Collatz R_a(n)=(an+1)/2^nu2(an+1). Deriva exacta Phi(a)=log2(a)-2.
Contractivo ssi Phi(a)<0 ssi a < 2^2 = 4. Borde dinamico: a=4 (Phi=0).
a=3 es el unico impar en (1,4) con Phi(3)=log2(3)-2 ~ -0.415 < 0.

POR QUE phi (y no otra cte)? Por la dinamica de ciclos:
Cada ciclo de Collatz es 3^m / 2^k ~ 1 => k/m ~ log2(3) ~ 1.585.
Los mejores k/m son los convergents de la fraccion continua de log2(3):
  log2(3) = [1; 1, 1, 2, 2, 3, 1, 5, ...]
Los primeros convergents de Fibonacci: 3/2, 8/5, 21/13, 55/34, ...
Su limite es phi=(1+sqrt5)/2 porque la CF de phi es [1;1,1,1,...].
PERO log2(3) cambia el 4to coeficiente a 2 (no 1): ahi se ROMPE la
aproximacion Fibonacci exacta. Ese es el punto donde el mapa deja de tener
ciclos Fibonacci-optimos => el umbral 2^phi=3.069 marca el aislamiento
aritmetico-dinamico de a=3.

CONCLUSION: 2^phi=3.069 aparece porque los ciclos mas estables de Collatz
tienen razon k/m ~ log2(3), y los mejores k/m son convergents Fibonacci
(limite phi) HASTA el coeficiente 4to. MECANISMO dinamico real, no "cerca de 4".
Cumple el criterio del amigo (Punto 7): explica POR QUE phi.

## Estado
- Aislamiento aritmetico de a=3 en (1, 2^phi=3.069): CIERTO (corregido de 3.694).
- Borde dinamico de divergencia: a=4 (Phi=0). Distinto de 2^phi.
- Derivacion dinamica: ENCONTRADA via convergents Fibonacci de log2(3).
- PENDIENTE: propagar correccion 3.694->3.069 en Collatz_Structural y Master-Document
  si citan 2^phi~3.694 (verificar linea 99 de Master-Document y sec 3.3 de Collatz).
