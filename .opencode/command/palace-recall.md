---
description: Recuperar memória do palácio arandu (o que eu disse/decidi/prefiro?)
agent: build
---
Busca no palácio arandu o que corresponde a esta consulta:

$ARGUMENTS

Procedimento:

1. Comece pela busca estruturada: `python arandu.py find "<termo>"` (varie termos
   se pouco resultado — sinônimos, pt-BR e en, palavras que você usaria).
2. Se a CLI não achar, use `grep` sobre os `.md` das salas (ids, tags, nomes).
3. Responda com o que achou, **citando o bloco fonte** (`id` + arquivo).
4. Se nada existe sobre o assunto — diga "não há memória disso" (NUNCA invente
   um fato sobre o Fernando) e pergunte se ele quer registrar agora.
5. Para acabativas: `python arandu.py wake` dá o L0/L1 do momento.
