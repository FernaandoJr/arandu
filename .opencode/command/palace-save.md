---
description: Guardar uma memória no palácio arandu (bloco YAML conforme protocolo)
agent: build
---
Guarda esta informação como bloco de memória no palácio arandu:

$ARGUMENTS

Siga na ordem:

1. Leia `00-reception/protocol.md` para o contrato do bloco (formato YAML completo).
2. Escolha a sala certa — consulte `00-reception/index.md` se tiver dúvida:
   fatos sobre o Fernando → `10-person/`; skills/workflow → `20-skills/`;
   projetos → `30-projects/`; pessoas/contexto técnico → `40-facts/`;
   sites/referências/ideias/leituras → `50-library/`.
3. **Dedupe antes de escrever:** `grep` pelo tema e pelo `id` candidato. Se já existe
   bloco igual, EDITE ele (bumpando `updated`) em vez de duplicar.
4. **Segredos jamais** (senha, chave, token, dado bancário). Contexto infra, sim.
5. Escreva o bloco YAML completo conforme o protocolo (1 ideia = 1 bloco, 2–6 linhas).
6. Após gravar, execute `python arandu.py build` para atualizar o índice derivado,
   e proponha o commit: `palace: add <tema>`.
7. Se a informação parece já ter um bloco mas desatualizado — pergunte ao Fernando
   antes de arquivar/atualizar (não decida sozinho).
