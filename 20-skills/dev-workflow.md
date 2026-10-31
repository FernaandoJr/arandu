# Skills — como Fernando gosta que as coisas sejam feitas

Esta sala define comportamento esperado da IA. Preferência desatualizada não se apaga: arquiva.

---
id: skill-comunicacao-ptbr
room: 20-skills
tags: [comunicacao, lingua]
status: hot
entry: 2026-10-31
updated: 2026-10-31
---

Fernando fala português (BR): respostas e documentação em pt-BR, mantendo termos técnicos em inglês quando essa é a prática do ramo (hook, cache, scaffold).
Estilo: explicar o conceito de forma simples primeiro, depois o detalhe específico; tom amigável e direto.

---

id: skill-plano-antes-executar
room: 20-skills
tags: [fluxo, planejamento]
status: hot
entry: 2026-10-31
updated: 2026-10-31
---

Para mudanças estruturais: propor a estrutura/plano antes de aplicar. Commits pequenos e verificáveis (`palace: add <tema>`), nunca um pacote grande de sombra.

---

id: skill-dados-derivative
room: 20-skills
tags: [arquitetura, dados]
status: active
entry: 2026-10-31
updated: 2026-10-31
---

Dado versionável = fonte de verdade em texto plano (markdown); derivado (SQLite, RAG) é cache re-gerável via `rm` + reindex. **Nunca** propor DB como verdade sem discutir antes com Fernando.
