# Skills Instaláveis

Skills de terceiros instaladas no ambiente. Cópia de guarda na biblioteca do palácio (`50-library/skills/`, fora do caminho de descoberta — guardar, não executar); a memória do que faz / quando usar fica no bloco abaixo.

---
id: skill-thermo-nuclear-code-review
room: 20-skills
tags: [skill, code-review, qualidade, codigo]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/thermo-nuclear-code-quality-review/SKILL.md
---

Review de código ultra-rigoroso focado em qualidade estrutural: caça "code judo" (reestruturação que apaga complexidade em vez de movê-la), reprova spaghetti de branches especiais, arquivo passando de 1000 linhas, wrappers/casts/optionality que não pagam o próprio bilhete, lógica no layer errado. Barra de aprovação exige justificativa explícita pra cada regressão estrutural. Usar ao revisar PRs/mudanças de branch.

---
id: skill-impeccable
room: 20-skills
tags: [skill, design, frontend, ui]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/impeccable/SKILL.md
---

Design com craft acima da distribuição (de Paul Bakaus / impeccable.style): escolhe o modo da superfície (Persuade/Operate/Read/Experience) e tem ~24 comandos (shape, critique, audit, polish, harden, animate, typeset...). Contexto via `impeccable context` (PRODUCT.md + DESIGN.md). Complemento geral de UI; para auditoria anti-slop usar com [[skill-visant-killer]].

---
id: skill-deslop-text
room: 20-skills
tags: [skill, escrita, copy, ia]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/deslop-text/SKILL.md
---

Review de texto contra 32 sinais de "cara de IA" (filler phrases, "not X it is Y", em-dash em série, marketing language, hedges, listas de 3 virtudes, cliche de internet...), agrupado por severidade com contagem de violações. Usar depois de escrever qualquer texto que um humano vai ler.

---
id: skill-visant-killer
room: 20-skills
tags: [skill, ui, auditoria, anti-slop]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/visant-killer/SKILL.md
---

Porta de auditoria anti-slop de UI (Pedro Jaques / visant): detectors scriptados como gate duro (`killer-scan.mjs`, Node 20+, Playwright opcional), julgamento via frontend/motion/refine, pass de advogado do diabo e score final. Acionar com "tá com cara de IA" / "audita essa tela" antes de PR.

---
id: skill-visant-frontend
room: 20-skills
tags: [skill, ui, decisao, business]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/visant-frontend/SKILL.md
---

Skill irmã de [[skill-visant-killer]]: cada escolha de interface precisa nomear a variável de negócio que move — ou sai. Entrega obrigatória: tabela de classificação de rotas.

---
id: skill-visant-motion
room: 20-skills
tags: [skill, motion, animacao, tokens]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/visant-motion/SKILL.md
---

Sistema de motion (princípios de Emil Kowalski): tokens de easing/duração espelhados em CSS e framer-motion, com `motion-lint.mjs` (Node 20+) e medição por URL. Para "deixa mais suave" / micro-transições.

---
id: skill-visant-refine
room: 20-skills
tags: [skill, ui, dataviz, polimento]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/visant-refine/SKILL.md
---

Anatomia única para gráficos, gauges, sparklines, sliders de simulação, metric tiles e painéis de controle — tela com cara de desenhada, não de montada. Node 20+. Irmã de [[skill-visant-killer]].

---
id: skill-visant-copy
room: 20-skills
tags: [skill, copy, ptbr, lint]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: 50-library/skills/visant-copy/SKILL.md
---

Copy brasileira em voz falada + `copy-lint.mjs` (Node 20+) que pega tics de IA em copy PT e EN. Complemento em texto de [[skill-deslop-text]]. Cruza com [[ref-designmd-ai]] no dia a dia de design system.
