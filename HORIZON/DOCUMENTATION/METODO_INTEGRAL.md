# Documento integral de método  
## Investigación formal por barreras, derivas, fronteras y verificación

Este documento destila el recorrido completo que hicimos, pero no como un informe sobre un problema particular, sino como un **sistema general de trabajo matemático**. La idea es que sirva como protocolo para investigación formal: qué métodos son legítimos, cuáles quedan descartados, cómo verificar, cuándo declarar una barrera, cuándo no, y cómo evitar autoengaño.

No se trata de una solución de ningún problema concreto. Es una **arquitectura de rigor**.

---

# 1. Principios fundamentales

## 1.1. Rigor antes que intuición

La intuición puede sugerir caminos, pero no demuestra. Todo resultado debe tener:

\[
\text{hipótesis explícitas} \Longrightarrow \text{conclusión explícita}
\]

sin pasos ocultos.

Una afirmación sin demostración, sin código verificable o sin derivación completa no es un resultado. Es una hipótesis.

---

## 1.2. Prohibido confundir evidencia con prueba

Una verificación finita:

\[
\forall x \in F,\quad P(x)
\]

con \(F\) finito, no implica:

\[
\forall x \in X,\quad P(x).
\]

La simulación puede:

1. refutar una conjetura si encuentra contraejemplo;
2. sugerir una regularidad;
3. predecir comportamiento;
4. extender un mapa.

Pero no puede cerrar una propiedad universal.

---

## 1.3. Un No-Go no es una rendición

Cuando una herramienta falla, eso no significa que el problema sea imposible. Significa que esa herramienta es insuficiente.

Formalmente:

\[
\text{Método } M \text{ no resuelve } P
\]

no implica:

\[
P \text{ es falso o indecidible}.
\]

Implica:

\[
M \notin \text{Clase de métodos capaces de cerrar } P.
\]

Esto es una **barrera metodológica**, no una imposibilidad lógica.

---

## 1.4. Prohibido declarar indecidibilidad sin prueba de independencia

No se debe decir que un problema es indecidible salvo que se demuestre independencia formal de un sistema axiomático, por ejemplo:

\[
\text{ZFC} \nvdash P
\quad\text{y}\quad
\text{ZFC} \nvdash \neg P.
\]

Lo que sí se puede declarar es:

\[
\boxed{
\text{esta clase de métodos no cierra el problema.}
}
\]

---

## 1.5. Regla de oro de no trivialidad

Un concepto nuevo solo cuenta si produce al menos una de estas cosas:

1. una barrera formal;
2. una cota nueva;
3. una reducción que debilite hipótesis;
4. una predicción cuantitativa falsable;
5. una verificación formal o sanity check no trivial.

No cuenta:

- reformular con lenguaje nuevo;
- hacer analogías sin contenido;
- predecir algo ya conocido;
- probar una tautología y presentarla como descubrimiento;
- definir objetos que no generan ninguna consecuencia verificable.

---

# 2. Axiomas operativos del método

Estos axiomas no son teoremas del problema estudiado. Son reglas del sistema de investigación.

---

## Axioma A1 — Dominio explícito

Toda afirmación debe indicar su dominio.

No es lo mismo:

\[
\forall n \in \mathbb{N},\ P(n)
\]

que:

\[
\forall n \in \mathbb{Z},\ P(n)
\]

o:

\[
\text{para casi todo } n \text{ respecto de una medida } \mu.
\]

La confusión de dominios es una fuente clásica de humo.

---

## Axioma A2 — Separación entre finito e infinito

Una propiedad sobre objetos finitos no puede trasladarse automáticamente a objetos infinitos.

Si se tiene una sucesión de verificaciones:

\[
P(1), P(2), \dots, P(N),
\]

no se puede concluir:

\[
\forall n,\ P(n).
\]

Para cerrar el salto se requiere:

- inducción;
- compacidad con condiciones adecuadas;
- un invariante bien fundado;
- una cota uniforme;
- un certificado finito de cobertura.

---

## Axioma A3 — Contraejemplo mínimo

Si el dominio está bien ordenado, y se quiere probar:

\[
\forall x \in X,\ P(x),
\]

se puede suponer:

\[
x^* = \min\{x \in X : \neg P(x)\}.
\]

Entonces:

\[
\forall y < x^*,\quad P(y).
\]

Cualquier objeto menor que \(x^*\) que lleve a \(x^*\) produce contradicción.

Este método no depende del problema concreto. Sirve en teoría de números, sistemas dinámicos, combinatoria, terminación de algoritmos, etc.

---

## Axioma A4 — Función de tamaño propia

Para estudiar terminación, convergencia o ausencia de escape, se necesita una función de tamaño:

\[
H:X\to \mathbb{R}_{\ge 0}
\]

que sea propia, en el sentido de que los conjuntos de nivel:

\[
\{x : H(x)\le C\}
\]

sean finitos o compactos según el contexto.

Si existe una función \(V\) tal que:

\[
V(Tx) < V(x)
\]

fuera de un conjunto trivial, entonces no puede haber órbitas infinitas malas.

Esta es la forma general de un argumento de Lyapunov, ranking o descenso.

---

## Axioma A5 — Control local no basta si hay frontera densa

Si un sistema tiene objetos de frontera que pueden ser aproximados arbitrariamente por objetos legítimos, entonces ningún observador de memoria finita puede decidir propiedades globales.

En forma abstracta:

Sea \(B\) un objeto de frontera, y sea \(x_m\) una secuencia de objetos legítimos que imitan a \(B\) durante \(m\) pasos. Entonces:

\[
\forall m,\ \exists x_m
\]

tal que cualquier clasificador finito de profundidad \(m\) no puede distinguir \(x_m\) de \(B\).

Por tanto, las cribas finitas pueden acotar, pero no cerrar, cuando la frontera es densa o aproximable.

---

## Axioma A6 — Toda reforma espacial debe conservar la cantidad crítica

Si se transforma un problema:

\[
X \longrightarrow Y,
\]

por ejemplo pasando a un espacio dual, compactificación, espacio de fases, espacio adélico, espacio no conmutativo, etc., se necesita un teorema de puente.

El puente debe demostrar que la propiedad original:

\[
P_X
\]

equivale o está controlada por:

\[
P_Y.
\]

Sin puente, el nuevo espacio solo produce una reformulación.

---

## Axioma A7 — La imposibilidad se conserva, se desplaza

Cuando una vía falla, la dificultad no desaparece. Se manifiesta en otro lugar.

Si una barrera aparece en un espacio:

\[
R_k,
\]

y se salta a:

\[
R_{k+1},
\]

la barrera suele reaparecer como:

- una constante no controlada;
- una hipótesis no probada;
- una medida que no ve el conjunto relevante;
- una pérdida de control arquimediano;
- una falta de compacidad;
- una singularidad;
- una frontera no eliminable.

Este principio sirve para detectar falsas soluciones.

---

# 3. Reglas de verificación

## 3.1. Verificación formal

Una prueba formal debe cumplir:

1. cero `sorry`;
2. cero axiomas ad hoc;
3. cero coerciones implícitas incorrectas;
4. cero teoremas importados sin verificar;
5. cero definiciones parciales no contempladas.

En estilo Lean/Mathlib, esto significa:

\[
\text{theorem } T : \forall x,\ P(x) := by\ \text{prueba completa}.
\]

Si una prueba depende de un lema auxiliar, ese lema debe estar probado o claramente marcado como hipótesis.

---

## 3.2. Sanity checks obligatorios

Todo teorema debe pasar pruebas elementales:

1. caso trivial;
2. caso negativo o extremo;
3. caso degenerado;
4. caso con signo contrario;
5. caso con denominador negativo, si existe;
6. caso con cero, si el dominio lo permite;
7. caso no entero, si el dominio incluye racionales o reales.

Un teorema que no sobrevive a sus sanity checks no debe presentarse.

---

## 3.3. Verificación de constantes

Si aparece una constante crítica:

\[
\alpha,
\]

se debe determinar:

1. su definición exacta;
2. su valor aproximado;
3. su racionalidad o irracionalidad;
4. su papel en desigualdades;
5. si puede ser igualada por cantidades discretas del sistema.

Por ejemplo, si:

\[
\alpha \notin \mathbb{Q},
\]

entonces ninguna razón discreta:

\[
\frac{A}{k}\in\mathbb{Q}
\]

puede satisfacer exactamente:

\[
\frac{A}{k}=\alpha.
\]

Eso elimina casos críticos exactos.

---

## 3.4. Verificación de promedios

Cuando se usan promedios, hay que distinguir:

\[
\frac{1}{k}\sum_{i=0}^{k-1} a_i
\]

de valores puntuales \(a_i\).

Un promedio positivo no implica todos los pasos positivos. Un promedio negativo no impide escapes transitorios.

Además, hay que distinguir:

\[
\liminf_{k\to\infty} \frac{A_k}{k},
\qquad
\limsup_{k\to\infty} \frac{A_k}{k},
\qquad
\lim_{k\to\infty} \frac{A_k}{k}.
\]

No son equivalentes.

---

## 3.5. Verificación de medidas

Si se usa una medida \(\mu\), se debe explicitar:

\[
\mu(E)=1
\]

no implica:

\[
E=X.
\]

Si el conjunto relevante tiene medida cero:

\[
\mu(D)=0,
\]

entonces los argumentos de medida casi segura no deciden propiedades sobre \(D\).

---

# 4. Métodos descartados

Los siguientes métodos quedaron descartados como vías de cierre, aunque pueden ser útiles como herramientas parciales.

---

## 4.1. Método descartado: casi todo implica todo

Forma inválida:

\[
\mu(\{x : P(x)\})=1
\quad\Longrightarrow\quad
\forall x,\ P(x).
\]

Esto es falso en general.

Si el conjunto de interés es numerable, denso y de medida cero, entonces los argumentos de medida no pueden decidirlo puntualmente.

Estado:

\[
\boxed{
\text{Descartado como prueba universal.}
}
\]

Uso permitido:

- heurística;
- predicción;
- identificación de comportamiento típico;
- motivación para cotas excepcionales.

---

## 4.2. Método descartado: cambio de espacio sin puente

Sea:

\[
\Phi:X\to Y.
\]

Si se prueba una propiedad en \(Y\), pero no se demuestra:

\[
P_Y(\Phi(x)) \Longrightarrow P_X(x),
\]

entonces el cambio de espacio no resuelve el problema original.

Esto aplica a:

- espacios duales;
- compactificaciones;
- espacios adélicos;
- geometrías no conmutativas;
- espacios de fase deformados;
- modelos espectrales;
- transformadas integrales.

Estado:

\[
\boxed{
\text{Descartado como cierre sin teorema de puente.}
}
\]

Uso permitido:

- reformulación;
- detección de invariantes;
- inspiración estructural;
- construcción de candidatos.

---

## 4.3. Método descartado: criba finita como cierre universal

Una criba finita trabaja con clases de equivalencia:

\[
x \sim_M y
\]

por ejemplo módulo \(M\), o por prefijos de longitud \(M\), o por estados de autómata finito.

Si existe un objeto de frontera \(b\) que puede ser aproximado por objetos legítimos durante arbitrariamente muchos pasos, entonces la criba nunca se vacía.

Formalmente:

\[
\forall M,\ \exists x_M
\]

tal que \(x_M\) y \(b\) son indistinguibles para la criba de profundidad \(M\).

Por tanto, la criba puede reducir clases, pero no puede probar ausencia global.

Estado:

\[
\boxed{
\text{Descartada como cierre si no hay certificado de cobertura finita.}
}
\]

Uso permitido:

- reducir candidatos;
- encontrar obstrucciones;
- construir autómata de restricciones;
- detectar sombras de frontera.

---

## 4.4. Método descartado: potencial local con memoria insuficiente

Un potencial de la forma:

\[
V(x)=H(x)+\varphi(s(x))
\]

donde \(s(x)\) es un estado local, puede fallar si el grafo de estados contiene ciclos cuyo costo neto es incompatible con descenso.

Si existe un ciclo de estados:

\[
s_1\to s_2\to\cdots\to s_1
\]

tal que:

\[
\sum_{i} \Delta H_i > 0,
\]

entonces ninguna elección de \(\varphi\) puede hacer descender \(V\) en todos los pasos del ciclo.

Esto no significa que no exista otro potencial más rico. Significa que ese potencial local no basta.

Estado:

\[
\boxed{
\text{Descartado si aparece ciclo obstructivo demostrado.}
}
\]

Uso permitido:

- identificar memoria mínima necesaria;
- diseñar fases;
- detectar variables faltantes.

---

## 4.5. Método descartado: simulación como demostración

Una simulación puede recorrer:

\[
F=\{x_1,\dots,x_N\}
\]

y verificar:

\[
P(x_i)
\]

para todos ellos.

Pero:

\[
\forall x\in F,\ P(x)
\]

no implica:

\[
\forall x\in X,\ P(x).
\]

Estado:

\[
\boxed{
\text{Descartada como prueba.}
}
\]

Uso permitido:

- falsar conjeturas auxiliares;
- encontrar contraejemplos;
- estimar constantes;
- validar implementaciones;
- generar hipótesis pre-registradas.

---

## 4.6. Método descartado: teoremas tautológicos como resultados principales

Una identidad algebraica puede ser útil, pero si solo dice:

\[
\operatorname{sgn}(A)=\operatorname{sgn}(B)
\]

porque \(A\) y \(B\) son algebraicamente equivalentes, entonces no es una barrera ni una cota nueva.

Puede conservarse como sanity check o como lema técnico, pero no como resultado principal.

Estado:

\[
\boxed{
\text{Descartado como resultado principal.}
}
\]

Uso permitido:

- verificación;
- formalización;
- depuración de definiciones.

---

## 4.7. Método descartado: declarar indecidibilidad sin independencia

Decir:

\[
P \text{ es indecidible}
\]

requiere una prueba metamatemática.

Sin ella, la afirmación es especulativa.

Estado:

\[
\boxed{
\text{Descartado sin prueba formal de independencia.}
}
\]

Uso permitido:

- formular conjeturas metamatemáticas;
- investigar posibles reducciones;
- comparar con sistemas formales conocidos.

---

# 5. Métodos no descartados

Estos métodos siguen vivos. No garantizan cierre, pero son legítimos y potencialmente suficientes si se desarrollan bastante.

---

## 5.1. Método retenido: contraejemplo mínimo

Sea:

\[
B=\{x\in X:\neg P(x)\}.
\]

Si \(B\neq\varnothing\) y \(X\) está bien ordenado, sea:

\[
x^*=\min B.
\]

Entonces:

\[
\forall y<x^*,\quad P(y).
\]

Esto permite atacar el problema por contradicción.

El método es válido siempre que:

1. el orden sea bien fundado;
2. la propiedad sea estable hacia atrás cuando sea necesario;
3. las transformaciones no introduzcan objetos fuera del dominio sin control.

Estado:

\[
\boxed{
\text{Retenido.}
}
\]

---

## 5.2. Método retenido: función de Lyapunov o ranking

Sea \(T:X\to X\) una transformación. Si existe:

\[
V:X\to W
\]

con \(W\) bien ordenado o con subconjuntos de nivel finitos, tal que:

\[
V(Tx)\prec V(x)
\]

para todo \(x\) fuera del conjunto trivial, entonces no hay órbitas infinitas malas.

En versión real:

\[
V(Tx)\le V(x)-\varepsilon
\]

para \(H(x)>B\), con \(\varepsilon>0\), y \(V\) propia.

Esto implica entrada eventual a una región finita.

Estado:

\[
\boxed{
\text{Retenido como vía de cierre potencial.}
}
\]

Dificultad:

Encontrar \(V\) suele ser tan difícil como el problema mismo.

---

## 5.3. Método retenido: deriva acumulada

Sea \(a_i\) una cantidad asociada al paso \(i\), y sea \(\alpha\) un umbral crítico.

Definimos:

\[
A_k=\sum_{i=0}^{k-1} a_i,
\]

\[
D_k=A_k-\alpha k.
\]

Si una órbita mala debe satisfacer:

\[
H(x_k)\ge H(x_0),
\]

entonces muchas veces se puede derivar una cota:

\[
\frac{A_k}{k}\le \alpha+\delta.
\]

Esto convierte el problema dinámico en una restricción aritmética sobre promedios.

Estado:

\[
\boxed{
\text{Retenido.}
}
\]

---

## 5.4. Método retenido: aproximación racional del umbral

Si \(\alpha\) es irracional o difícil de manejar directamente, se puede usar una cota racional:

\[
\alpha < \frac{p}{q}.
\]

Si se sabe que:

\[
\frac{A_k}{k}<\frac{p}{q},
\]

entonces:

\[
qA_k < pk.
\]

Esto define un autómata de crédito:

\[
C_k=pk-qA_k.
\]

Cada paso con valor \(a\) cambia el crédito en:

\[
\Delta C=p-qa.
\]

La condición de supervivencia es:

\[
C_k>0.
\]

Este método produce restricciones exactas, discretas y verificables.

Estado:

\[
\boxed{
\text{Retenido.}
}
\]

---

## 5.5. Método retenido: criba como productora de barreras

Aunque una criba finita no puede cerrar por sí sola, puede producir:

1. clases prohibidas;
2. restricciones modulares;
3. obstrucciones de memoria finita;
4. candidatos residuales;
5. teoremas de No-Go contra autómatas específicos.

Estado:

\[
\boxed{
\text{Retenida como herramienta de barrera, no como cierre.}
}
\]

---

## 5.6. Método retenido: imágenes inversas y minimalidad

Si un objeto malo \(x\) puede ser alcanzado desde un objeto menor \(y<x^*\), entonces \(y\) también sería malo. Eso contradice la minimalidad de \(x^*\).

En sistemas afines o algebraicos, esto suele escribirse como:

\[
x = \Phi_w(y),
\]

y por tanto:

\[
y = \Psi_w(x).
\]

Si:

\[
0<y<x^*,
\]

entonces \(x\) no puede ser parte de la órbita de un contraejemplo mínimo.

Este método es muy poderoso para excluir residuos, patrones o configuraciones.

Estado:

\[
\boxed{
\text{Retenido.}
}
\]

---

## 5.7. Método retenido: análisis de frontera y sombras

Muchos sistemas tienen objetos de frontera:

- ciclos negativos;
- soluciones singulares;
- puntos fijos inestables;
- órbitas fantasma;
- configuraciones límite;
- estados no físicos pero estructuralmente cercanos.

Los objetos legítimos pueden imitar a esos objetos durante un tiempo finito.

Si una sombra de profundidad \(m\) produce crecimiento:

\[
G(m)\approx e^{\beta m},
\]

pero el costo de alcanzarla es:

\[
C(m)\approx e^{\gamma m},
\]

con \(\gamma>0\), entonces existe un balance:

\[
\text{recompensa} \sim \beta m,
\qquad
\text{costo} \sim e^{\gamma m}.
\]

Esto permite formular teoremas de escape o condiciones suficientes de terminación.

Estado:

\[
\boxed{
\text{Retenido como línea estructural profunda.}
}
\]

---

## 5.8. Método retenido: condición suficiente de cierre

Aunque no se tenga la prueba completa, se puede dejar formulada la condición exacta que cerraría el problema.

Forma general:

\[
\boxed{
\text{Si no existe ninguna cadena infinita admisible con balance neto positivo, entonces } P \text{ es verdadero.}
}
\]

Esto no resuelve el problema, pero lo reduce a una afirmación precisa.

Estado:

\[
\boxed{
\text{Retenido como cierre condicional.}
}
\]

---

# 6. Líneas de pensamiento utilizadas

## 6.1. Línea local: paso a paso

Partimos de una transformación elemental:

\[
x_{i+1}=T(x_i).
\]

En cada paso se observa una cantidad discreta:

\[
a_i=a(x_i).
\]

Esta cantidad puede ser un exponente, una valuación, una energía, una pérdida, un índice de contracción, etc.

La idea es convertir el comportamiento local en una suma:

\[
A_k=\sum_{i=0}^{k-1} a_i.
\]

Esto permite pasar de dinámica discreta a aritmética acumulada.

---

## 6.2. Línea de deriva: promedio contra umbral

Se identifica un umbral crítico:

\[
\alpha.
\]

Este umbral separa expansión de contracción, o crédito de deuda.

La deriva acumulada es:

\[
D_k=A_k-\alpha k.
\]

Si \(D_k\) se mantiene positiva, el sistema tiende a un comportamiento; si se mantiene negativa, tiende a otro.

Pero hay que tener cuidado: el promedio no controla necesariamente cada paso individual.

---

## 6.3. Línea de minimalidad: reducir al peor objeto

En vez de estudiar todos los objetos, se estudia el menor objeto malo:

\[
x^*.
\]

Esto impone restricciones fuertes:

1. ningún objeto menor puede ser malo;
2. ningún objeto menor puede llevar a \(x^*\);
3. cualquier prefijo que caiga por debajo de \(x^*\) está prohibido;
4. cualquier imagen inversa menor está prohibida.

Este método convierte un problema universal en un problema de obstrucción local alrededor de \(x^*\).

---

## 6.4. Línea de crédito: hacer finita la deriva

Para evitar trabajar directamente con \(\alpha\), se usa una aproximación racional:

\[
\alpha < \frac{p}{q}.
\]

La condición:

\[
\frac{A_k}{k}<\frac{p}{q}
\]

se vuelve:

\[
qA_k<pk.
\]

Esto define un crédito entero:

\[
C_k=pk-qA_k.
\]

El sistema se transforma en un autómata con restricciones de positividad:

\[
C_k>0.
\]

Esta línea permite:

- calcular palabras permitidas;
- eliminar ramas;
- traducir a congruencias;
- construir cribas exactas.

---

## 6.5. Línea de criba: residuos y memoria finita

Una vez que se tienen restricciones sobre \(a_i\), se traducen a clases de equivalencia.

Por ejemplo:

\[
x \equiv r \pmod M.
\]

Cada paso impone condiciones sobre \(r\), y ciertos residuos quedan prohibidos.

Esta línea produjo exclusiones concretas, pero también mostró su límite: una criba finita no puede eliminar objetos que imitan arbitrariamente bien a una frontera.

---

## 6.6. Línea de frontera: sombras y amplificadores

Cuando la criba no se vacía, hay que preguntarse qué sobrevive.

En general sobreviven las sombras de objetos de frontera.

Una sombra de profundidad \(m\) es un segmento donde el sistema imita a un objeto límite durante \(m\) pasos.

Esto puede producir amplificación:

\[
H_{\text{salida}}
\approx
H_{\text{entrada}}
\cdot
e^{\beta m}
\cdot
e^{-\text{corrección}}.
\]

La pregunta crucial es:

\[
\text{¿la amplificación compensa el costo de llegar a la sombra?}
\]

Si la respuesta es no, se obtiene una vía de cierre.

Si no se puede probar, queda una barrera.

---

## 6.7. Línea de simulación: mapa, no territorio

La simulación se usa solo como instrumento secundario.

Puede responder preguntas como:

\[
\exists x \le N:\ R(x)?
\]

o:

\[
\min_{x\le N} F(x)?
\]

pero no:

\[
\forall x,\ P(x).
\]

Por eso se usa para:

- detectar errores;
- refutar conjeturas auxiliares;
- explorar sombras;
- verificar constantes;
- predecir comportamiento.

---

## 6.8. Línea formal: convertir lo estable en teorema

Todo lo que sobrevive a falsación debe formalizarse.

Formalizar no es solamente escribir código. Es fijar:

1. definiciones;
2. tipos;
3. hipótesis;
4. lemas auxiliares;
5. teoremas principales;
6. casos límite;
7. sanciones de error.

Una prueba formal sin `sorry` es una forma de memoria externa: impide que el autoengaño sobreviva.

---

# 7. Estructura general de un problema de cierre

Sea un problema de la forma:

\[
\forall x\in X,\ P(x).
\]

Se introduce una dinámica:

\[
T:X\to X
\]

y una función de tamaño:

\[
H:X\to \mathbb{R}_{\ge 0}.
\]

El problema se divide en sectores:

1. sector trivial;
2. sector periódico;
3. sector acotado no trivial;
4. sector divergente;
5. sector de frontera.

Para cerrar el problema, se necesita una de estas cuatro cosas.

---

## 7.1. Cierre por Lyapunov

Existe \(V\) propia tal que:

\[
V(Tx)\le V(x)-\varepsilon
\]

para todo \(x\) fuera del conjunto trivial.

Entonces no hay órbitas malas infinitas.

---

## 7.2. Cierre por certificado finito

Existe una familia finita de certificados que cubre todo el dominio:

\[
X=\bigcup_{i=1}^N C_i,
\]

y para cada \(C_i\) se prueba que ningún elemento de \(C_i\) puede ser malo.

---

## 7.3. Cierre por contradicción minimal

Se asume \(x^*\) mínimo malo y se deriva una contradicción usando:

\[
\forall y<x^*,\ P(y).
\]

---

## 7.4. Cierre por reducción a condición suficiente

Se prueba:

\[
Q\Longrightarrow P,
\]

y luego se prueba \(Q\).

Si \(Q\) no se prueba, el problema queda reducido a \(Q\), pero no cerrado.

---

# 8. Tabla de estado de métodos

| Método | Estado | Uso válido | Riesgo principal |
|---|---|---|---|
| Verificación finita | Descartado como cierre | Sanity check | Confundir evidencia con prueba |
| Medida casi segura | Descartado como cierre | Heurística | Ignorar conjuntos de medida cero |
| Espacio dual sin puente | Descartado como cierre | Reformulación | Perder la propiedad original |
| Criba finita | Descartado como cierre | Barreras locales | Creer que vaciará automáticamente |
| Potencial local | Descartado si hay ciclo obstructivo | Diseño de memoria | Memoria insuficiente |
| Simulación | Descartado como prueba | Falsación | Sobreinterpretación |
| Contraejemplo mínimo | Retenido | Contradicción | Requerir orden bien fundado |
| Lyapunov | Retenido | Cierre potencial | Difícil de construir |
| Deriva acumulada | Retenido | Cotas | Solo controla promedios |
| Autómata de crédito | Retenido | Restricciones exactas | Puede no vaciarse |
| Imágenes inversas | Retenido | Exclusiones | Puede volverse intratable |
| Sombras de frontera | Retenido | Diagnóstico estructural | Requiere control arquimediano |
| Cierre condicional | Retenido | Reducción | No es prueba completa |
| Independencia lógica | No probado | Investigación metamatemática | Declarar sin demostrar |

---

# 9. Protocolo operativo general

## Paso 1 — Formalizar el enunciado

Escribir:

\[
\forall x\in X,\ P(x)
\]

con dominio exacto.

Si el dominio no tiene orden natural, definir uno o abandonar el método de contraejemplo mínimo.

---

## Paso 2 — Definir tamaño y dinámica

Elegir:

\[
T:X\to X,
\qquad
H:X\to \mathbb{R}_{\ge 0}.
\]

La función \(H\) debe ser relevante para la propiedad.

Ejemplos:

- tamaño aritmético;
- norma;
- energía;
- entropía;
- altura;
- longitud de código;
- complejidad;
- distancia a un atractor.

---

## Paso 3 — Identificar cantidades locales

En cada paso:

\[
x_i\mapsto x_{i+1}=T(x_i),
\]

medir:

\[
a_i=a(x_i).
\]

Definir:

\[
A_k=\sum_{i=0}^{k-1} a_i.
\]

---

## Paso 4 — Buscar umbral crítico

Encontrar \(\alpha\) tal que:

\[
a_i>\alpha
\]

produzca un efecto, y:

\[
a_i<\alpha
\]

produzca el efecto contrario.

Si \(\alpha\) no es racional, usar cotas racionales:

\[
\frac{p_-}{q_-}<\alpha<\frac{p_+}{q_+}.
\]

---

## Paso 5 — Derivar cota de deriva para contraejemplo mínimo

Si \(x^*\) es malo y todo futuro permanece por encima de cierto tamaño, entonces suele obtenerse:

\[
\frac{A_k}{k}\le \alpha+\delta.
\]

Si se tiene una cota racional superior:

\[
\alpha+\delta<\frac{p}{q},
\]

entonces:

\[
qA_k<pk.
\]

---

## Paso 6 — Construir autómata de crédito

Definir:

\[
C_k=pk-qA_k.
\]

Exigir:

\[
C_k>0.
\]

Cada paso agrega:

\[
\Delta C=p-qa_i.
\]

Esto produce un árbol de palabras permitidas.

---

## Paso 7 — Traducir a congruencias o estados

Si el sistema es aritmético, traducir palabras permitidas a clases:

\[
x\equiv r \pmod M.
\]

Si el sistema es simbólico, traducir a estados de autómata.

Eliminar ramas incompatibles.

---

## Paso 8 — Aplicar imágenes inversas

Para cada palabra \(w\), resolver:

\[
x=\Phi_w(y).
\]

Si \(y<x^*\), entonces \(x\) no puede aparecer en la órbita de un contraejemplo mínimo.

Esto genera nuevas prohibiciones.

---

## Paso 9 — Identificar frontera sobreviviente

Si la criba no se vacía, preguntar:

\[
\text{¿qué objetos sobreviven?}
\]

Generalmente sobreviven sombras de objetos límite.

Analizar:

1. profundidad de imitación;
2. crecimiento durante la sombra;
3. costo de salida;
4. posibilidad de encadenar sombras.

---

## Paso 10 — Formular condición de cierre

Si no se puede cerrar, escribir explícitamente:

\[
\boxed{
\text{El problema quedaría cerrado si se prueba } Q.
}
\]

Donde \(Q\) debe ser una condición concreta, por ejemplo:

\[
\sum_{\text{sombras}} \text{ganancia}
-
\sum_{\text{tránsitos}} \text{costo}
\to -\infty.
\]

---

## Paso 11 — Formalizar lo probado

Convertir en teoremas:

1. lemas de minimalidad;
2. cotas de deriva;
3. exclusiones por imágenes inversas;
4. No-Go de memoria finita;
5. fórmulas de sombra;
6. sanity checks.

No formalizar conjeturas como si fueran teoremas.

---

# 10. Criterios de aceptación de un resultado

## 10.1. Resultado fuerte

Un resultado es fuerte si produce una de estas consecuencias:

\[
\boxed{
\forall x,\ P(x)
}
\]

o:

\[
\boxed{
\exists x:\neg P(x)
}
\]

o:

\[
\boxed{
\text{una clase completa de métodos no puede probar } P.
}
\]

---

## 10.2. Resultado medio

Un resultado es medio si produce:

1. una cota nueva;
2. una reducción;
3. una barrera formal;
4. una predicción falsable;
5. una clasificación verificable.

---

## 10.3. Resultado débil

Un resultado es débil si solo produce:

1. una reformulación;
2. una analogía;
3. una intuición;
4. una simulación;
5. una coincidencia numérica.

Los resultados débiles pueden ser útiles, pero no deben presentarse como cierre.

---

# 11. Errores frecuentes y cómo evitarlos

## 11.1. Error: creer que un promedio controla cada paso

Corrección: usar cotas locales o funciones de Lyapunov.

---

## 11.2. Error: creer que casi todo es todo

Corrección: verificar si el conjunto objetivo tiene medida cero.

---

## 11.3. Error: confundir un objeto de frontera con un objeto real

Corrección: distinguir:

\[
x\in X
\]

de:

\[
x\in \overline{X}\setminus X.
\]

---

## 11.4. Error: usar memoria finita para decidir propiedades infinitas

Corrección: demostrar que la memoria finita es suficiente, o declarar No-Go.

---

## 11.5. Error: construir un potencial que falla en un ciclo pequeño

Corrección: verificar ciclos mínimos antes de generalizar.

---

## 11.6. Error: simular y extrapolar

Corrección: registrar la simulación como hipótesis, no como prueba.

---

## 11.7. Error: declarar indecidibilidad por dificultad

Corrección: distinguir dificultad de independencia formal.

---

## 11.8. Error: ocultar una hipótesis fuerte

Corrección: listar todas las hipótesis, incluso las que parecen obvias.

---

# 12. Forma general de un teorema de barrera

Un teorema de barrera tiene esta forma:

Sea \(\mathcal{M}\) una clase de métodos. Entonces:

\[
\forall M\in\mathcal{M},\ M \text{ no puede demostrar } P.
\]

Esto no prueba:

\[
\neg P.
\]

Prueba:

\[
\neg(\mathcal{M}\vdash P).
\]

Ejemplos de barreras:

1. métodos de medida casi segura no prueban propiedades puntuales sobre conjuntos de medida cero;
2. autómatas finitos no deciden propiedades que requieren memoria no acotada;
3. potenciales locales no prueban terminación si existe ciclo obstructivo;
4. espacios duales sin puente no prueban la propiedad original;
5. funcionales integrales no controlan normas supremas sin hipótesis adicionales.

---

# 13. Forma general de un cierre por descenso

Sea \(T:X\to X\). Sea \(V:X\to\mathbb{R}\). Si:

\[
V(Tx)\le V(x)-\varepsilon
\]

para todo \(x\) con \(H(x)>B\), y si:

\[
V(x)\to\infty
\quad\text{cuando}\quad
H(x)\to\infty,
\]

entonces ninguna órbita puede permanecer para siempre fuera de la región:

\[
H(x)\le B.
\]

Si la región \(H(x)\le B\) es finita y se verifica directamente, el problema queda cerrado.

Este esquema es general.

---

# 14. Forma general de un cierre por certificado finito

Sea:

\[
X=\bigcup_{i=1}^N C_i.
\]

Si para cada \(i\) existe un certificado \(K_i\) tal que:

\[
\forall x\in C_i,\ K_i(x)\text{ demuestra }P(x),
\]

entonces:

\[
\forall x\in X,\ P(x).
\]

La dificultad está en construir la cobertura finita y los certificados.

---

# 15. Forma general de una reducción por contraejemplo mínimo

Supongamos:

\[
\exists x:\neg P(x).
\]

Sea:

\[
x^*=\min\{x:\neg P(x)\}.
\]

Si se prueba que toda configuración asociada a \(x^*\) implica la existencia de:

\[
y<x^*
\]

con:

\[
\neg P(y),
\]

entonces hay contradicción.

Por tanto:

\[
\neg\exists x:\neg P(x),
\]

y:

\[
\forall x,\ P(x).
\]

---

# 16. Forma general de un análisis de frontera

Sea \(b\) un objeto de frontera. Sea \(m\) una profundidad de imitación.

Si un objeto legítimo \(x\) imita a \(b\) durante \(m\) pasos, se tiene un segmento:

\[
x_0,x_1,\dots,x_m.
\]

Se mide el tamaño al inicio y al final:

\[
H_0=H(x_0),
\qquad
H_m=H(x_m).
\]

Si existe una fórmula de crecimiento:

\[
H_m\approx H_0\,G(m),
\]

entonces se puede estudiar si \(G(m)\) es compatible con terminación.

Si:

\[
G(m)>1
\]

pero el costo de alcanzar la sombra es:

\[
C(m)\gg G(m),
\]

entonces la frontera no alcanza para sostener escape infinito.

Si no se puede probar la desigualdad global, queda una barrera.

---

# 17. Reglas para documentos futuros

Todo documento de investigación debería incluir:

1. problema exacto;
2. dominio exacto;
3. definiciones completas;
4. hipótesis explícitas;
5. métodos usados;
6. métodos descartados;
7. resultados probados;
8. resultados no probados;
9. barreras;
10. condiciones suficientes de cierre;
11. sanity checks;
12. código o derivaciones;
13. errores conocidos;
14. nivel de trivialidad o profundidad;
15. siguiente paso concreto.

No se debe publicar internamente un resultado sin indicar su estado:

\[
\text{probado},\quad
\text{conjetura},\quad
\text{heurística},\quad
\text{barrera},\quad
\text{descartado}.
\]

---

# 18. Clasificación final de líneas

## Línea 1 — Álgebra local

Estado: útil pero limitada.

Sirve para derivar identidades y condiciones necesarias.

No cierra por sí sola.

---

## Línea 2 — Promedios y deriva

Estado: útil para cotas.

Sirve para restringir comportamientos malos.

No controla trayectorias individuales sin argumentos adicionales.

---

## Línea 3 — Contraejemplo mínimo

Estado: poderosa.

Reduce el problema a obstrucciones alrededor del menor objeto malo.

Requiere orden bien fundado.

---

## Línea 4 — Autómata de crédito

Estado: útil y verificable.

Produce restricciones discretas exactas.

No garantiza vacío.

---

## Línea 5 — Criba de residuos

Estado: útil como filtro.

No puede cerrar si hay frontera aproximable.

---

## Línea 6 — Imágenes inversas

Estado: poderosa para exclusiones.

Puede volverse combinatoriamente intratable.

---

## Línea 7 — Sombras de frontera

Estado: estructuralmente profunda.

Explica por qué fallan las cribas y por qué aparecen amplificadores.

Requiere control global de costos.

---

## Línea 8 — Simulación

Estado: auxiliar.

No prueba.

Puede falsar y guiar.

---

## Línea 9 — Formalización

Estado: necesaria.

Convierte lo estable en memoria verificable.

No sustituye la idea, pero la disciplina.

---

# 19. Síntesis final

El método que emerge de todo el recorrido puede resumirse así:

\[
\boxed{
\text{Definir con precisión.}
}
\]

\[
\boxed{
\text{Atacar por contraejemplo mínimo.}
}
\]

\[
\boxed{
\text{Medir deriva local.}
}
\]

\[
\boxed{
\text{Convertir deriva en crédito discreto.}
}
\]

\[
\boxed{
\text{Aplicar cribas sin creer que cierran.}
}
\]

\[
\boxed{
\text{Identificar la frontera que sobrevive.}
}
\]

\[
\boxed{
\text{Calcular su costo y su amplificación.}
}
\]

\[
\boxed{
\text{Formular la condición suficiente de cierre.}
}
\]

\[
\boxed{
\text{Formalizar lo probado.}
}
\]

\[
\boxed{
\text{No declarar victoria sin prueba.}
}
\]

---

# 20. Regla final

La regla final es simple:

> Si una idea no produce una barrera, una cota, una reducción, una predicción falsable o una verificación formal, es decoración.  
> Si produce una de esas cosas, se conserva.  
> Si además cierra el problema, se celebra.  
> Si no, se documenta con honestidad y se sigue.

Este es el sistema completo. No depende de un problema específico. Es una disciplina de investigación: construir objetos, forzarlos a trabajar, eliminar humo, y quedarse únicamente con lo que resiste.