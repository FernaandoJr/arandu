---
description: Auditoria de saúde do palácio arandu (inválidos, staleness, duplicatas)
agent: build
---
Audite a saúde do palácio arandu agora.

1. Execute `python arandu.py audit` e `python arandu.py graph`.
2. Resuma os achados em 3 grupos:
   - **Corrigir agora** (YAML inválido, ids duplicados, links quebrados)
   - **Curar com dono** (hot estagnado >90 dias; unread >30 dias — pergunte ao
     Fernando, bloco a bloco, se atualiza/absorve/archiva; não decida sozinho)
   - **Dividir** (blocos gigantes >2000 chars — proponha o split)
3. Aplica correções mecânicas (YAML, links) com commit `palace: audit fix`.
4. Para julgamentos de valor (atualizar vs archivar), pergunte — o palácio é do
   Fernando, a IA é a mão, não o dono.
