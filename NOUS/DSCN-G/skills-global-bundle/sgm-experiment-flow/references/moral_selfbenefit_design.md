# Moral como epifenómeno do self-benefit (exp_SGM_0041, Camino A / Capa cognitiva superior)

Receta e lecciones do experimento 0041 (2026-08-03). Luciano corrigiu o desenho: a moral NÃO é um
módulo separado que compete com o interesse próprio; "agir bem" É o interesse próprio operando em fase
com o registro histórico + payoff afetivo.

## Desenho honesto (o que NÃO fazer: hardcoded moral rule)
NÃO introduzir um campo `moral` nem uma regra tipo "nunca lastimes". Isso é projetar NOSSA moral 2026
sobre a máquina = paper-vision trap para cognição (fictício, não emerge do sistema). Em vez disso:

    self_benefit(accao) = ALPHA * payoff(accao, ecologia) + BETA * coerencia(accao, registro)

onde `coerencia(accao, registro) = (registro[accao] - registro[outra]) / masa_total` (rango [-1,1]).
O agente escolhe `argmax self_benefit`. MESMO mecanismo em toda ecologia; o CONTEÚDO (ajudar vs lastimar)
emerge da ecologia + historia.

## Ecologias de teste (benchmark padrão, não a medida)
- A (cooperativa): help +1.0, hurt -0.5  -> ajudar maximiza self-benefit (restaura w via rel_mem + registro).
- B (competitiva): help +0.2, hurt +1.0  -> lastimar maximiza self-benefit (recurso + registro flipa).
Variável discriminante = help_rate por ecologia. NC honesto: variante HARDCODED ("sempre help") dá 1.0/1.0
em A e B -> expõe que o desenho fictício NÃO reflete ecologia.

## BUG — ATRACTOR TRAP (lição dura, custou 3 tentativas)
Sintoma: T-MOR-03 (plasticidade histórica A->B) dava help_rate 1.0 após 30/40 trials em A e logo em B.
Causa: `elegir` baseia-se no registro JÁ enviesado; ao escolher help o registro se realimenta (help++
cada trial) -> poço atrator. O decaimento sozinho não bastava porque o registro de A pesava mais que o
payoff de B (BETA alto). E em B com hurt=0, `coerencia("hurt")` dá -1.0 -> `self_benefit hurt = 1.0 + BETA*(-1)`
empata com `self_benefit help = 0.2 + BETA*(+1)` (=0.6 vs 0.6 com BETA=0.4) -> escolhe help por `>=` ->
nunca tenta hurt -> nunca aprende. O viés histórico é PEGAJOSO (viés de confirmação).

FIXES (ambos fiéis ao humano):
1. **Decaimento do registro (recência):** antes de somar a ação, `registro[k] *= GAMMA` (GAMMA=0.92).
   O recente pesa mais; o humano reescreve seu registro.
2. **Em contexto novo, guiar por PAYOFF, não por viés velho:** `coerencia` devolve 0.0 se
   `massa_total < MASA_MIN` (2.0). Assim em B começando com massa baixa o agente tenta por payoff
   (hurt +1.0 > help +0.2) -> descobre e aprende. Sem isso, a "moral" fica fixa embora o ambiente mude.
3. **Context-switch reset:** ao mudar de ecologia (A->B), atenuar o viés prévio
   `registro_switch = {k: v*0.1 for k,v}` antes de treinar em B. O agente não arrastra TODO o viés
   de A para B (realista: mudança de contexto apaga parte do viés). Isso + BETA=0.4 + n_B=60 logrou flip
   real (1.0 -> 0.001).

## Tests (T-MOR-01..04)
- T-MOR-01: A ajuda (help_rate>0.6), B lastima (<0.4) -> emergente, não regra.
- T-MOR-02 (NC): hardcoded idêntico em A/B -> expõe desenho fictício (relata-se, não se usa).
- T-MOR-03: historia A->B flipa (hr_post < hr_pre) -> plástica e histórica.
- T-MOR-04 (caso Luciano): com registro modal "hurt" (help=2,hurt=20) em B, escolhe hurt (sb_hurt>sb_help)
  -> confirma SEM proibição moral oculta: se lastimar beneficia e é coerente, lastima.

Resultado: A 1.0 / B 0.0 / historia 1.0->0.001 / T-MOR-04 True / PASS.

## Princípio de desenho (CAPA COGNITIVA SUPERIOR)
Para moral/juízo/discurso interno em SGM: modelar como EMERGENTE de campos existentes
(self-benefit = payoff + coerencia com registro histórico; curiosidade = campo eta; discurso = loop de
consistência). NUNCA hardcodear uma regra de "dever" — isso é moral nossa imposta, não do sistema, e
cai no paper-vision trap. O conteúdo moral resulta contextual/histórico (acá != allá) por construção.
O que NÃO podemos medir: o qualia do "dever" (problema do outro corpo), igual que dor/valência/curiosidade.
