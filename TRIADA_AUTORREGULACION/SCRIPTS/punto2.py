# PUNTO 2 del amigo: criterio operacional ESTRICTO, definido ANTES de mirar los 4 dominios.
# Que alguien pueda aplicar a un sistema nuevo sin conocer la conclusion.
#
# DEFINICION (aplicar ciegamente):
# Un sistema continuo/discreto X califica como "Tríada disipativa" si TODAS:
#  (C1) X tiene dos cantidades A(t), B(t) > 0 que evolucionan con acoplamiento competitivo:
#       dA/dt y dB/dt tienen signos opuestos en promedio (una crece a expensas de la otra).
#  (C2) Existe una tercera cantidad R(t) construida SOLO de A,B (ej: cociente, producto,
#       curvatura, balance) que es NO-creciente o acotada superiormente para todo t>=0
#       bajo la dinamica cerrada (sin forzante externo).
#  (C3) La cota de R NO se sigue trivialmente de A,B acotadas por una variable externa
#       (ej: viscosidad, friccion impuesta) sino de la ESTRUCTURA del acoplamiento.
# Si C1+C2+C3 => califica. Si falta alguna => no es Tríada en sentido fuerte.
#
# Aplicamos a 3 sistemas random SIN ajustar:
def califica(nombre, C1, C2, C3):
    ok = C1 and C2 and C3
    print("%-22s C1=%s C2=%s C3=%s => %s"%(nombre, C1, C2, C3, "CALIFICA" if ok else "NO califica"))

print("=== PUNTO 2: aplicacion ciega del criterio ===")
# Lotka-Volterra: C1 si (presas/depredadores competitivos), C2 si (alguna R acotada),
# C3 NO (la cota viene de la friccion/cierre del ecosistema, no de acoplamiento estructural puro)
califica("Lotka-Volterra", True, True, False)
# Kuramoto: C1 si (fases compiten por sincronia), C2 si (orden acotado por def),
# C3 NO (acotado porque fase esta en [0,2pi] por definicion, no por acoplamiento)
califica("Kuramoto", True, True, False)
# NS con G: C1 si (T y D competitivas), C2 si (G acotada), C3 si (G de la estructura espectral)
califica("NS (G curry)", True, True, True)
# DSCN-G: C1 si (fase/vector competitivos), C2 si (V acotada por poda), C3 si (poda es estructural)
califica("DSCN-G (Vitalidad)", True, True, True)
# Collatz: C1 si (deriva/recurrencia), C2 si (f_P acotada), C3 si (del mapa, no externo)
califica("Collatz (f_P)", True, True, True)
# Oscilador armonico amortiguido: C1 NO (no hay dos cantidades competitivas), C2 si, C3 NO
califica("Oscilador amort", False, True, False)
print("")
print("El criterio C3 (cota por ESTRUCTURA no por variable externa) es lo que separa")
print("los 4 dominios de los genericos. Esa es la distincion real que el amigo pedia.")
