# v0.19 — Dolor de consecuencia / EVASIÓN (ancla DSCN-G)

Luciano: "el dolor biológico es una señal que obliga al sistema a cambiar para
evitar lo que lo produce". En el grafo = el ω del nodo se ALEJA de la transición
que causó el dolor (EVASIÓN), NO castigo post-hoc ni reward fijo (eso era el
v0.9c circular).

## Progresión (3 versiones; las 2 primeras fallaron POR DISEÑO)

### v0.19-v1 — FALLÓ (restar vector NO repele)
`omega[A] = omega[A] - alpha*omega[B]/|B|` tras dolor A->B.
Resultado: P(A->B) basal 0% -> evadido 100%. El "evadir" empujó A HACIA B.
Lección: restar el vector en espacio crudo no repele en coseno de forma controlable.

### v0.19-v2 — FALLÓ (argmax oculta el efecto)
Mide "qué nodo elige A" (argmax de afinidad). Ambos (basal/evadido) dieron 0% para
B y C porque A ya transicionaba a un 3er nodo D — el "dolor A->B" nunca ocurría en
la métrica. Lección: no midas el argmax global; depende de todo el espacio.

### v0.19-v3 — CORRECTO (afinidad directa) ✓
Mide afinidad coseno directa:
- basal: aff(A,B)=0.9416, aff(A,C)=0.4781
- tras evasion (acercar A a C seguro + alejar de B): aff(A,B)=-0.4706, aff(A,C)=0.4876

El cruce de signo de aff(A,B) (+0.94 -> -0.47) es la EVASIÓN real: A se aleja de lo
que lo lastima y mantiene la alternativa segura. `evasion_real` estricto (C sube
+0.05) puede no cumplirse porque C ya estaba en ~0.48; el veredicto claro es el
cruce de signo.

## Receta (copiar y modificar)
```python
def cos(a,b):
    na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(x*x for x in b))
    return 0.0 if na<1e-9 or nb<1e-9 else sum(x*y for x,y in zip(a,b))/(na*nb)
# A transiciona basalmente a B (B cerca de A); C es alternativa segura, lejos.
A=[rng.gauss(0,1) for _ in range(D)]
B=[x+0.3*rng.gauss(0,1) for x in A]
C=[rng.gauss(0,1) for _ in range(D)]
aff_AB_base=cos(A,B); aff_AC_base=cos(A,C)
# dolor A->B: acercar A a C, alejar de B
for _ in range(STEPS):
    na=norm(A); nb=norm(B); nc=norm(C)
    A=[A[k]-ALPHA*B[k]/nb + ALPHA*C[k]/nc for k in range(D)]
A=[x/norm(A) for x in A]   # renormalizar
aff_AB_ev=cos(A,B); aff_AC_ev=cos(A,C)
```
Verificar sintaxis antes de lanzar:
`python3 -c "import py_compile; py_compile.compile('run_v19.py', doraise=True)"`

## Por qué es distinto de v0.9c
v0.9c: dolor = error de predicción, empujaba ω a un `omega_ideal` FIJO (circular).
v0.19: dolor = CONSECUENCIA DEL ENTORNO (transición A->B señalada), el sistema aprende
a EVITAR la transición (ω[A] se aleja de ω[B]). Es la definición biológica de Luciano
implementada sin señal exógena.
