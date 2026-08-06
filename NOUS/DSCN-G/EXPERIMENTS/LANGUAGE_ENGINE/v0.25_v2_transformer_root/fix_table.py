import re
p="/sdcard/Hermes/nexus-vault/TRIADA_AUTORREGULACION/TRIADA_Autorregulacion_Disipativa.md"
s=open(p).read()
old_table="""| Dominio | Dinamica A | Dinamica B | 3ra dinamica (autorregula) | Resultado |
|---------|-----------|-----------|----------------------------|-----------|
| Navier-Stokes | Transferencia T(k) | Disipacion D(k)=2*nu*k^2*E | Curvatura espectral G[k] (Tercer Motor) | G acotada en 1D/2D/3D (no diverge) |
| DSCN-G | Fase phi_i | Vector omega_i | Vitalidad V_i (Ec.5-6) | Podaa confina grafo a N*<=~5 (T1 verificado) |
| Collatz | Deriva 2-adica (empuja abajo) | Recurrencia al ciclo | Balance f_P (freq clase P/N) | f_P < 0.7075 para todo n testeado |
| Riemann | Ceros zeta (autovalores) | Funcion Xi | Regulador GOE (estadistica de niveles) | spacings repelen (GOE) => ceros confinados en linea critica |"""
new_table="""| Dominio | Dinamica A | Dinamica B | 3ra dinamica (autorregula) | Resultado | Estatus |
|---------|-----------|-----------|----------------------------|-----------|---------|
| Navier-Stokes | Transferencia T(k) | Disipacion D(k)=2*nu*k^2*E | Curvatura espectral G[k] (Tercer Motor) | G acotada 1D/2D/3D, pero NO basta sola: lema fuerte negativo (alpha_min->0 con y sin G). Regularidad la salva k_diss viscoso (Foias-Temam) | PARCIAL (regulador real, no prueba Milenio) |
| DSCN-G | Fase phi_i | Vector omega_i | Vitalidad V_i (Ec.5-6) | Podaa confina grafo a N*<=~5 (T1 verificado) | CONFIRMADO |
| Collatz | Deriva 2-adica (empuja abajo) | Recurrencia al ciclo | Balance f_P (freq clase P/N) | f_P < 0.7075 (umbral exacto f_P*=log4(8/3)) | CONFIRMADO |
| Riemann | Ceros zeta (autovalores) | Funcion Xi | Regulador GOE (estadistica de niveles) | GOE confirmado en ceros, PERO sustrato circulante NO matchea (test_C re-corrido: 0.138 vs 0.612). No es el mismo objeto espectral | NO CONFIRMADO como sustrato unificador |"""
assert old_table in s, "tabla no encontrada"
s=s.replace(old_table,new_table)
open(p,"w").write(s)
print("Tabla sec 1 corregida: NS=PARCIAL, Riemann=NO CONFIRMADO.")
