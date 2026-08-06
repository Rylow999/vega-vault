# exp_SGM_0026 — Decoder L2 on a REAL corpus (T-DEC-01 REAL)

Pattern + recipe for validating the SGM L2 bigram decoder on natural-language text
(Don Quijote), the T-DEC-01 REAL that exp_SGM_0022 left pending (0022 was synthetic).
Learned 2026-08-02.

## Why this experiment exists
0022 proved the decoder LEARNS transitions, but on a SYNTHETIC corpus (one strong hidden
successor + noise). Luciano's explicit next step was downloading a REAL corpus to run the
T-DEC-01 REAL. This closes that gap. It does NOT prove "SGM speaks Spanish" — see trap below.

## Download the corpus (urllib, no web_search needed)
```python
import urllib.request, os
DEST = "/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/lit/corpus/don_quijote.txt"
os.makedirs(os.path.dirname(DEST), exist_ok=True)
for url in ["https://www.gutenberg.org/files/996/996-0.txt",
            "https://www.gutenberg.org/cache/epub/996/pg996.txt"]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        break
    except Exception as e:
        print("fallo", e)
text = data.decode("utf-8", errors="replace")
open(DEST,"w",encoding="utf-8").write(text)
```
**TRAP:** Gutenberg **996 is the ENGLISH Ormsby translation** ("The History of Don Quixote"),
NOT Cervantes' Spanish original. For Spanish, fetch **Gutenberg 2000**
(`https://www.gutenberg.org/files/2000/2000-0.txt`). The decoder test is language-agnostic,
so English 996 is fine for mechanism validation; just don't claim "Spanish" from it.

## Tokenize + build REAL bigram
```python
import re
from collections import Counter
raw = open(DEST, encoding="utf-8", errors="replace").read()
m = re.search(r"\*\*\* START OF.*?\*\*\*", raw);  raw = raw[m.end():]
m = re.search(r"\*\*\* END OF.*?\*\*\*", raw);    raw = raw[:m.start()]
toks = re.findall(r"[a-záéíóúñü]+", raw.lower())   # strip Gutenberg header/footer + punctuation
V = 400
vocab = [w for w,_ in Counter(toks).most_common(V)]
idx = {w:i for i,w in enumerate(vocab)}
count = [[0]*V for _ in range(V)]
for a,b in zip(toks, toks[1:]):
    if a in idx and b in idx:
        count[idx[a]][idx[b]] += 1
P = []
for row in count:
    s = sum(row)
    P.append([x/s if s else 0.0 for x in row])   # norm rows
```

## Metrics + HONEST negative control
- **azar** = 1/V (trivial baseline).
- **lineal** = proyeccion W·omega (the roadmap-forbidden baseline; expect ~0.07, bad).
- **UNIGRAM** = predict the single most-frequent word (no context). This is the honest
  "no structure" control — NOT shuffled bigram rows (see trap).
- **bigrama** top1 vs all three; top5 overlap vs true next word.

**TRAP — negative control design (cost us one failed run):** "shuffle the bigram rows"
keeps marginal word frequencies, so frequent words (the, of, and) still dominate the argmax
and the control scores ~0.029 instead of ~azar -> the test FALSELY FAILS even though the
mechanism is correct. Use UNIGRAM instead. Bigrama >> unigram proves it captures STRUCTURE,
not just word frequency.

## Results (exp_SGM_0026, V=400, N_test=4000, seed=42)
| metric            | value  |
|-------------------|--------|
| top1 bigrama      | 0.1847 |
| top1 lineal       | 0.0750 |
| top1 unigram (NC) | 0.0762 |
| azar (1/V)        | 0.0025 |
| top5 bigrama      | 0.4253 |

PASS: bigrama >> azar (68x), > lineal, > unigram, top5>0.10. The unigram negative control
passes (bigrama 0.1847 > unigram 0.0762) -> structure captured, not frequency.

## Hygiene
- Corpus goes in `lit/corpus/` — ADD `lit/corpus/` to `.gitignore` so it never uploads
  (treat exactly like `lit/papers/`).
- Registry entry for 0026 carries `validation: "natural"` (real corpus). 0022 keeps
  `validation: "synthetic"` — do NOT relabel 0022.
