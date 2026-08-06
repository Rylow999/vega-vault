# Receta: buscar literatura vía arXiv API (web_search NO disponible en este entorno)

La herramienta `web_search` NO está disponible en el Android/CLI de Hermes (anotado en MEMORY).
Pero `urllib` SÍ tiene red. La API de arXiv (Atom feed) funciona sin API key. Receta probada 2026-08-03
(usada para encontrar Animal-AI / Active Inference / Cognitive maps para el 0042/0043).

## 1) Buscar por query (lista de resultados)
```python
import urllib.request, urllib.parse, xml.etree.ElementTree as ET
NS = {"a": "http://www.w3.org/2005/Atom"}
def arxiv(q, maxn=5):
    q = urllib.parse.quote(q)
    url = "http://export.arxiv.org/api/query?search_query=all:%s&start=0&max_results=%d" % (q, maxn)
    data = urllib.request.urlopen(url, timeout=25).read()
    root = ET.fromstring(data)
    out = []
    for e in root.findall("a:entry", NS):
        ide = e.find("a:id", NS).text.split("/")[-1]
        ti = " ".join(e.find("a:title", NS).text.split())
        out.append((ide, ti))
    return out
# queries utiles: "Animal-AI environment", "open-ended learning agent",
# "cognitive architecture benchmark", "MineDojo Minecraft agent", "Active Inference exploration"
```

## 2) Bajar abstract de un ID concreto
```python
def abst(arxiv_id):
    url = "http://export.arxiv.org/api/query?id_list=%s" % arxiv_id
    data = urllib.request.urlopen(url, timeout=25).read()
    root = ET.fromstring(data)
    e = root.find("a:entry", NS)
    return " ".join(e.find("a:summary", NS).text.split())
```
NOTA: IDs viejos (pre-2007, formato 4 dígitos como 0510054) devuelven HTTP 400 con id_list.
Para esos, buscar por query en su lugar.

## 3) Verificar conectividad rápida
```python
import urllib.request
try:
    urllib.request.urlopen("https://export.arxiv.org/api/query?search_query=all:crafter&max_results=1", timeout=10)
    print("OK")
except Exception as ex:
    print("FAIL", ex)
```

## Papers que guiaron 0042/0043 (guardar en lit/papers/ para métricas exactas)
- 1909.07483  Animal-AI Environment (cognición animal-like, sin lenguaje) — benchmark del 0042.
- 2206.08853  MineDojo (Minecraft, internet-scale) — NO comparable (RL a escala), solo contexto.
- 2010.00262  Active Inference (exploración por minimizar sorpresa) — marco de 0043 (B-puro).
- 2504.20628  Cognitive maps are generative programs (mapa generativo) — Opción A no usada en 0043.
- 1903.07400  Scheduled Intrinsic Drive (exploración intrínseca jerárquica).

## Regla de honestidad al citar
No comparar SGM contra MineDojo/XLand en "puntos de juego" (desleal: billones de params + gradiente).
Usar Animal-AI como marco de métricas CONDUCTUALES y comparar SOLO contra baseline ciego en el mismo entorno.
