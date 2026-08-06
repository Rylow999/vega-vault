import math
# PUNTO 4 del amigo: prediccion cuantitativa CRUZADA. Derivar el bound de un dominio
# desde el de otro con una FORMULA real, no solo "ambos acotados".
# Intento: Collatz f_P* = log4(8/3) ~ 0.7075  vs  DSCN-G N* ~ 4.8
# ¿Hay formula que de uno desde el otro?
print("=== PUNTO 4: prediccion cruzada Collatz <-> DSCN-G ===")
fP = math.log(8.0/3.0, 4)   # 0.7075
Nstar = 4.8
print("f_P* (Collatz) = %.4f"%fP)
print("N* (DSCN-G)    = %.2f"%Nstar)
# Intento 1: ¿N* relacionado con 1/f_P? 
print("1/f_P* = %.4f  (no se parece a N*)"%(1/fP))
# Intento 2: ¿f_P* relacionado con log(N*)?
print("log2(N*) = %.4f  vs f_P*=%.4f (no matchean)"%(math.log2(Nstar), fP))
# Intento 3: ¿el umbral a=4 de Collatz da N*? 2^f_P = 8/3 = 2.667; 2^4=16
print("2^(4*fP) = %.4f  (el 4 de Collatz no da N*)"%(2**(4*fP)))
# Intento 4: ¿deriva de Collatz Phi(3)=-0.415 da N*?
Phi3 = math.log2(3)-2
print("Phi(3) = %.4f ; ¿N* = -1/Phi(3)? = %.4f (no da 4.8)"%(-1/Phi3 if Phi3!=0 else 0, -1/Phi3 if Phi3!=0 else 0))
print("")
print("RESULTADO: NO hay formula real que derive f_P* desde N* (ni viceversa).")
print("Los bounds son INDEPENDIENTES: cada uno sale de su propia dinamica")
print  # separador
print("Esto es negativo PERO informativo: la Tríada es analogia de ESTRUCTURA,")
print("no unificacion de constantes. Coincide con conclusion global (tests A/B/C/M).")
print("ANOTAR como negativo en el documento (no fracaso, es informacion).")
