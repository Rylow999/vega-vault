# GAPS hacia la pseudoAGI (mapeo del motor DSCN-G, 2026-07-28)

Mapa de lo que ya tenemos validado vs lo que falta para un sustrato neuro-simbólico
tipo "pseudoAGI". Honesto sobre capacidad y sobre lo que es hueco.

## CAPA 1 — REPRESENTACIÓN (validado en grafo rústico + proyección)
- GRAFO FRACTAL + anchor/repulsion (v0.21 v8): sentidos separados ESTABLES SIN transformer (DQ real 39/40).
- PROYECCION Hebb W (v0.22 v3): ruteo de sentido PERFECTO (1.0) en corpus contrastivo.
- FALTA composicion relacional: el grafo codifica co-ocurrencia ("banco aparece con dinero") pero NO "banco TIENE dinero" ni "banco ES institucion". Falta relacion estructurada, no solo asociacion.
- FALTA jerarquias: el fractal es plano (D=16, una capa de subnodos). Falta "banco subseteq institucion financiera subseteq organizacion".

## CAPA 2 — RAZONAMIENTO (casi todo hueco)
- FALTA memoria de trabajo con VITALIDAD competitiva (v0.3b esboza nodo, falta slots que compiten y decaen, ventana de foco temporal).
- FALTA inferencia transitiva: "A->B, B->C, luego A->?" — el grafo solo asocia local.
- FALTA contradiccion: detectar "banco es rio" vs "banco es dinero" y mantener ambos sin colapsar (los 2 subnodos ya existen; falta el mecanismo de CONSULTA).

## CAPA 3 — AUTONOMIA / ANCLA DSCN-G
- DOLOR de consecuencia (v0.19 limpio): evasion dirigida por error real (-2.7% genuino).
- APRENDIZAJE por dolor (v0.9c robusto): curva monotono, 5 semillas.
- FALTA: el dolor debe AFECTAR DECISIONES futuras (no solo vector de nodo). "Evitar lo que lastimo" necesita lazo a la ACCION, no solo a omega.
- FALTA: preservacion de identidad (omega nucleo que NO se toca). Tu circular lo marco: excluir nodo de entrenamiento y reintegrar (v0.3b v2 lo hace a nivel de nodo; falta el lazo a "quien soy").

## CAPA 4 — LENGUAJE / GENERACION (casi todo hueco)
- FALTA: next-token es pobre (9.5% hibrido, 8% grafo). Falta decodificacion coherente.
- FALTA: DECODER que use el sentido RUTEADO (root rutea pero no genera). El root DIRECTOR existe; falta el decoder que consume el sentido activo.

## CAPA 5 — META / CONCIENCIA (lo que apunta el proyecto)
- "Duda" (v0.22, CERRADO como no-aplicable a nivel de SENTIDO): la duda de sentido NO
  emerge porque el grafo fractal separa los sentidos tan bien que SIEMPRE hay claro
  ganador (v0.22 v5: duda A/B/MIX = 0.0 incluso con proyeccion suave + contextos mixtos).
  Eso es EXITO del fractal, no fallo. La duda real es de DECISION (conflito de inferencias
  validas) y requiere nivel superior, no ambiguedad de palabra.
- FALTA: duda de DECISION que DISPARE busqueda/consulta (no solo quede en estado).
- FALTA autobservacion: el sistema sabe que duda, sabe que no sabe.
- FALTA el lazo de que "yo" (root/identidad) es el que duda.

## PRIORIDAD HONESTA (que ingenierar primero, orden sugerido)
1. [CERRADO] Root DIRECTOR (v0.22): v3 rutea PERFECTO (1.0) con proyeccion Hebb; v4/v5
   duda = 0.0 porque el grafo fractal (v0.21 v8) separa los sentidos TAN bien que SIEMPRE
   hay claro ganador — incluso en contextos MIXTOS. La duda de SENTIDO no emerge porque el
   sistema siempre sabe que sentido es: eso es EXITO del fractal, no fallo del root. La duda
   real es de DECISION (nivel superior, conflito de inferencias), no ambiguedad de palabra.
   v0.22 queda CERRADO como exito de separacion + ruteo; la duda de sentido no aplica.
2. [ABIERTO / DIFICIL] Composicion relacional (v0.23, SIGUIENTE): banco TIENE dinero, no solo
   co-ocurre. Diseno v0.23: triplas implicitas (sujeto, RELACION, objeto) por Hebb 3-body ->
   matrices R[r] (TIENE/LUGAR) tales que R[r]·emb[s] ≈ emb[o]. RESULTADO v0.23: 4/12 = 0.333
   (PEOR que azar 0.5). FALLO DE DISENO: el script acercaba TAMBIEN emb[s] y emb[o] (asociacion
   basica) -> contamina, "banco" queda cerca de "dinero" Y de "rio", R[TIENE]/R[LUGAR] no
   distinguen. REGLA: para relaciones, NO acercar embeddings base; que SOLO R[r] encode la
   relacion, en espacio separado. Hebb 3-body es el mecanismo correcto pero el diseño naive
   colapsa. NO inflar el 0.333. El muro donde los grafos de asociacion fallan -> se necesita
   tensor/relational embedding o espacio de relacion separado.
3. Memoria de trabajo con vitalidad competitiva (slots).
4. Decoder que use el sentido ruteado para generar.
5. Lazo dolor->decision y preservacion de identidad.
6. Meta: duda de DECISION que dispara busqueda + autobservacion.
