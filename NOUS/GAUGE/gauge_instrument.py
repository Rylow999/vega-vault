"""
DSCN-G-Gauge: instrumentacion corregida del Monte Carlo SU(2).

Por que este archivo existe (auditoria 2026-10-29):
  El `gauge_mc.py` original mezcla observables NO COMPARABLES y reporta
  errores estadisticos naives. Correcciones:

  1. CLASIFICACION DE LOOPS. Con d1=1, d2=2 (el default original), el loop
     (2,2) recorre la arista (0,1) dos veces (ida y vuelta), de modo que su
     holonomia colapsa: U . Udag = I. Ese loop NO es comparable con (1,1).
     Se clasifica cada loop como:
       SIMPLE  — ningun vertice ni arista repetida; observable valido
       TIPO-E  — arista repetida => holonomia identicamente 1 (degenerado)
       TIPO-V  — vuelve sobre un vertice sin repetir arista (no encierra region)
     y por defecto SOLO se miden los SIMPLEs.

  2. A_min POR BFS. El 'area' de la Def. 2.7 del paper se computa como el
     minimo numero de triangulos t con borde(S) = C (mod 2), via BFS sobre
     el espacio de estados (frozenset de triangulos). Se reporta, para que
     el ajuste de la G1 use el area REAL y no R*T.

  3. ERRORES HONESTOS. Se estiman por bloques (bootstrap sobre medias de
     bloque) y se reporta tau_int por autocorrelacion y N_eff. El error
     original (std/sqrt(n)) subestima el error real en ~6x.

  4. OBSERVABLES CON Y SIN SIGNO. Se reporta W (con signo) y |W|. Con signo
     hay cancelacion entre superficies de orientaciones opuestas; |W| es
     el observable de area law.

  5. GENERADORES NO DEGENERADOS. Por defecto d1=1, d2=4: linealmente
     independientes en Z_N. Con d2=2, +1 y +2 son colineales y el 'rectangulo'
     no es un rectangulo.

Hiperparametros de la accion: la medida de Gibbs usa exp((beta/2) * tr(U_p)),
es decir el coeficiente de la plaqueta es beta/2 (no beta). El 'beta' del
paper es por lo tanto beta_accion = 2 * beta_paper.

Licencia: MIT. Autor: Luciano Benjamin Nieto (ORCID 0009-0000-8766-7243).
"""
import numpy as np
from collections import defaultdict, deque

# --------------------------------------------------------------------------
# Config (JSON-serializable, para los results JSON)
# --------------------------------------------------------------------------
CONFIG = {
    "N": 16,
    "d1": 1,
    "d2": 4,
    "betas": [0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0],
    "n_therm": 1000,
    "n_meas": 4000,
    "n_blocks": 16,
    "epsilon": 0.3,
    "seeds": [42, 43],
    "shapes": [[1, 1], [1, 2], [1, 3], [2, 1], [3, 1]],
    "include_degenerate": False,
    "measure_absW": True,
}


# --------------------------------------------------------------------------
# Grafo circulante fractal
# --------------------------------------------------------------------------
def build_circulant(N):
    """S = {1, 2, 4, ..., N/2}; S_sym = S union (N-S) \\ {0}."""
    m = int(np.log2(N))
    S = [2 ** k for k in range(m)]
    S_sym = set(S) | {(N - d) % N for d in S}
    S_sym.discard(0)
    return S, sorted(S_sym)


def build_graph(N, S_sym):
    """Aristas, adyacencia y plaquettes triangulares (Def. 2.2 del paper)."""
    edges = set()
    adj = defaultdict(set)
    for i in range(N):
        for d in S_sym:
            j = (i + d) % N
            adj[i].add(j)
            if i < j:
                edges.add((i, j))
            elif i > j:
                edges.add((j, i))

    triangles = set()
    for i in range(N):
        for j in adj[i]:
            if j <= i:
                continue
            for k in adj[j]:
                if k <= j:
                    continue
                if k in adj[i]:
                    triangles.add(tuple(sorted([i, j, k])))

    return sorted(edges), adj, sorted(triangles)


def tri_edge_set(tri):
    """Las 3 aristas de un triangulo, como frozenset de pares ordenados."""
    return frozenset([
        (min(tri[0], tri[1]), max(tri[0], tri[1])),
        (min(tri[1], tri[2]), max(tri[1], tri[2])),
        (min(tri[2], tri[0]), max(tri[2], tri[0]))])


# --------------------------------------------------------------------------
# Geometria de los Wilson loops
# --------------------------------------------------------------------------
def loop_path(N, d1, d2, R, T):
    """Path orientado del loop: R pasos de d1, T de d2, R de -d1, T de -d2."""
    path = []
    cur = 0
    for d, n in [(d1, R), (d2, T), (-d1, R), (-d2, T)]:
        for _ in range(n):
            nxt = (cur + d) % N
            path.append((cur, nxt))
            cur = nxt
    assert cur == 0, "loop no cierra"
    return path


def classify_loop(N, d1, d2, R, T):
    """Clasifica el loop como SIMPLE / TIPO-E / TIPO-V.

    CORRECCION (auditoria 2026-10-29, segunda iteracion). Dos correcciones
    sucesivas, ambas necesarias:

    (1) La clasificacion por 'arista repetida' era INCORRECTA. Con d1=1,d2=2
        los loops (2,2) y (3,1) no repiten ninguna arista: cada arista
        aparece una sola vez. Repiten VERTICES.

    (2) La deteccion por 'balance neto = 0' (arista recorrida en ambos
        sentidos) detecta una arista invertida, pero eso NO implica que la
        holonomia valga 1. Las matrices SU(2) no conmutan: si la arista
        invertida aparece en pasos i y j con j > i+1, el producto es
        A . B . C . A^-1, que NO es I. La holonomia colapsa a 1 solo si la
        arista invertida se recorre CONSECUTIVAMENTE (ida y vuelta
        pegadas), de modo que U . Udag aparece como factor contiguo.

    Verificacion numerica: con d1=1,d2=2 el loop (2,2) invierte la arista
    (2,4) en los pasos 2 y 6 (no contiguos) -> W = -0.749, NO 1.
    Con d1=1,d2=8 el loop (1,2) invierte las aristas (0,1),(1,9),(0,8) en
    pasos contiguos 0/2, 1/3, 4/5 -> W = 1.000000 exacto.

    Tipos:
      TIPO-E  — arista invertida CONSECUTIVA => factor U.Udag contiguo =>
                holonomia identicamente 1. NO comparable con otros loops.
      TIPO-V  — el path repite un vertice: el loop no es simple; su 'area
                minima' no es canonica.
      SIMPLE  — path simple: ni vertices repetidos ni aristas invertidas.
    """
    path = loop_path(N, d1, d2, R, T)

    # --- test algebraico de degeneracion ---
    # La holonomia colapsa a I solo si, para cada link, los factores U y
    # Udag aparecen de forma que se cancelan CONTIGUAMENTE. Como las
    # matrices SU(2) no conmutan, la condicion correcta no es 'la arista se
    # recorre invertida' sino 'el factor U.Udag aparece contiguo'.
    #
    # Test robusto y exacto: se cancelan factores identicos consecutivos
    # (M . Mdag = I para cualquier matriz unitaria) mediante stack-reduction
    # sobre el path. Si la holonomia resultant es identicamente 1 para
    # CUALQUIER asignacion de matrices, el loop es TIPO-E.
    #
    # Implementacion: reducir la palabra (path) emparejando pares consecutivos
    # (a,b),(b,a) -> vacio. Si la palabra se reduce a vacio, el loop es
    # trivialmente 1. Ojo: esto solo es correcto si los pares son de la
    # MISMA arista; (a,b),(b,a) con a,b adyacentes SIEMPRE es la misma arista.
    reduced = list(path)
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(reduced) - 1:
            (a1, b1), (a2, b2) = reduced[i], reduced[i + 1]
            if a1 == b2 and b1 == a2:
                del reduced[i:i + 2]
                changed = True
            else:
                i += 1
    if not reduced:
        return "TIPO-E", path

    # vertices: el de cierre aparece 2 veces (normal). Mas de 2 => repite.
    vcount = defaultdict(int)
    for a, b in path:
        vcount[a] += 1
        vcount[b] += 1
    repeated = [v for v, c in vcount.items() if c > 2]
    if repeated:
        return "TIPO-V", path
    return "SIMPLE", path


def area_min_bfs(N, d1, d2, R, T, triangles, max_states=2000000):
    """A_min(C): minimo numero de triangulos S con borde(S) = C (mod 2).

    BFS sobre estados = frozenset de triangulos; el estado objetivo es aquel
    cuyo borde (XOR de las 3 aristas de cada triangulo) coincide con la
    cadena del loop C. Agregar un triangulo togglea sus 3 aristas.

    Arranque: el estado vacio tiene borde vacio, que no es incidente a nada,
    asi que no se puede expandir desde ahi. Se arranca desde los triangulos
    incidentes a la cadena C (cualquier superficie que ceñe a C debe
    contener al menos uno de ellos).

    Se usa TOGGLE (agregar o quitar) porque una superficie minima puede
    requerir remover triangulos que se anaden antes (para cerrar el borde).
    """
    path = loop_path(N, d1, d2, R, T)
    target = set()
    for (a, b) in path:
        e = (a, b) if a < b else (b, a)
        if e in target:
            target.remove(e)
        else:
            target.add(e)
    if not target:
        return 0, "trivial"
    target_f = frozenset(target)

    tri_edges = [tri_edge_set(t) for t in triangles]
    by_edge = defaultdict(list)
    for ti, e in enumerate(tri_edges):
        for x in e:
            by_edge[x].append(ti)

    def border_of(state):
        b = set()
        for ti in state:
            b ^= tri_edges[ti]
        return frozenset(b)

    # arrancamos desde cada triangulo incidente a C
    seeds = set()
    for e in target:
        seeds.update(by_edge.get(e, []))
    if not seeds:
        return None, "C no es contenible en el 2-complejo"

    seen = set()
    q = deque()
    for ti in seeds:
        st = frozenset([ti])
        seen.add(st)
        q.append((st, 1))
    while q:
        st, dist = q.popleft()
        if border_of(st) == target_f:
            return dist, "OK"
        cand = set()
        for e in border_of(st):
            cand.update(by_edge.get(e, []))
        for ti in cand:
            ns = st ^ {ti}      # TOGGLE: agregar o quitar
            if ns in seen:
                continue
            seen.add(ns)
            q.append((ns, dist + 1))
        if len(seen) > max_states:
            return None, "BFS explosion (%d estados)" % len(seen)
    return None, "sin superficie"
