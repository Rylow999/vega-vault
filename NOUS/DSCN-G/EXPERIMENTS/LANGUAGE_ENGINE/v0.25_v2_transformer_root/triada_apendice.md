# APENDICE: Escala dorada en NS (b) + Revisiones del amigo
## 2026-07-25

## A. Escala dorada en NS (resultado b)
Barrido de Reynolds 2D (N=24): G* vs Re.
Re=5->24337 | 10->50326 | 20->99202 | 30->145140 | 50->251570 |
70->225877 | 100->109795 | 150->51649 | 200->31549.
PICO en Re~50 (G*=251570), cae para Re mayor. Coincide con SDDF_NS2D
(optimo Re~50, G* propto Re^0.70). Este Re~50 es el "2^phi de NS":
escala donde el Tercer Motor es maximo. PRECAUCION: 2^phi~3.694 es
aislamiento ARITMETICO (Collatz a=3 unico impar en (1,3.694)); Re~50 es
optimo DINAMICO. Análogos en estructura (punto critico de cambio de regimen),
NO el mismo tipo de umbral. No llamarlos "iguales" en el paper.

## B. Revisiones solicitadas por el amigo (7 puntos)
1. Control negativo: correr el molde de la Tríada en Lotka-Volterra y Kuramoto
   SIN poda. Si "confirma" ahi => el patron no distingue nada. Si falla => algo real.
   PENDIENTE: hacerlo primero (es el test mas importante).
2. Criterio operacional: definir "dos dinamicas en competencia" ANTES de mirar los
   4 dominios, estricto, aplicable a sistema nuevo. Luego aplicar a 2-3 sistemas random.
   PENDIENTE.
3. Contradiccion Riemann: test_C decia "no matchean" pero la tabla de sec 1 dice que si.
   REVISAR test_C y bajar/marcar la fila de Riemann como NO confirmada.
   PENDIENTE: re-correr test_C.
4. Prediccion cuantitativa cruzada: derivar bound de Collatz desde bound de DSCN-G
   (o viceversa) con formula real. Si no sale, anotar como negativo. PENDIENTE.
5. Status NS en tabla: el lema fuerte dio negativo (alpha_min->0 con y sin G).
   La tabla sec 1 lista NS como "confirma" igual que las demas. BAJAR estatus.
   PENDIENTE: editar tabla.
6. GUE vs GOE con datos reales: bajar ceros de Odlyzko, correr spacing contra GUE.
   PENDIENTE.
7. 2^phi: no subir de PENDIENTE hasta tener derivacion del POR QUE phi y no otra cte.
   Criterio de aceptacion: mecanismo que explique phi, no "esta cerca de 4".
   YA hecho: encontre la nota (Master-Document linea 99) = aislamiento aritmetico
   de a=3 en (1,2^phi). Eso EXPLICA phi (es el unico impar en ese intervalo). Pero
   es aritmetico, no dinamico. Mantener como PENDIENTE hasta derivacion dinamica.
