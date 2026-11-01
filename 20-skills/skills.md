# Skills Instaláveis

Skills de terceiros instaladas no ambiente. O palácio guarda a *memória* dela — o que faz, quando usar, onde está. Skills vendorizadas ficam em `.agents/skills/` (lidas pelo agente no nível do projeto) e o bloco aqui documenta.

---
id: skill-thermo-nuclear-code-review
room: 20-skills
tags: [skill, code-review, qualidade, codigo]
type: skill
status: hot
entry: 2026-11-01
updated: 2026-11-01
source: .agents/skills/thermo-nuclear-code-quality-review/SKILL.md
---

Review de código ultra-rigoroso focado em qualidade estrutural: caça "code judo" (reestruturação que apaga complexidade em vez de movê-la), reprova spaghetti de branches especiais, arquivo passando de 1000 linhas, wrappers/casts/optionality que não pagam o próprio bilhete, lógica no layer errado. Barra de aprovação exige justificativa explícita pra cada regressão estrutural. Usar ao revisar PRs/mudanças de branch.
