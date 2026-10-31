# Palácio de Memória

Este repositório é a **memória de longo prazo** de Fernando. Tudo aqui é curado por ele — trate como fonte de verdade sobre quem ele é, o que ele prefere e o que já foi decidido.

## Regras da casa

1. **Nunca leia o repositório inteiro.** Comece por `00-reception/index.md` (o mapa das salas) e navegue pelos links conforme a necessidade.
2. **Antes de perguntar de novo, procure.** Se o Fernando mencionar um fato pessoal, preferência ou decisão, busque no palácio (grep por `tags`/`id`) antes de refazer perguntas já respondidas.
3. **Memória nova = bloco no formato do protocolo.** Toda informação que ele disser que "quer guardar" vira um bloco YAML conforme `00-reception/protocol.md`. Nunca texto livre solto.
4. **Antes de salvar, verifique dedupe:** grep pelo tema/`id` na sala correspondente. Atualize um bloco existente em vez de criar duplicata (e bumpando `updated`).
5. **Nunca, em hipótese alguma, armazene segredos aqui** (senhas, chaves, tokens, dados bancários). Contexto descrevendo infraestrutura hoje, sim; credenciais, jamais.
6. **Mudanças de preferência ≠ apagar.** Preferências antigas vencem com `status: archive` — o Git preserva o histórico.

## Rotinas disponíveis

| Situação | Ação |
|---|---|
| Fernando manda "guarda isso" | Escrever bloco na sala certa conforme protocolo → propor commit `palace: add <tema>` |
| Fernando pergunta "como eu...", "o que eu..." | Buscar no palácio primeiro, responder com o que achar + apontar o bloco fonte |
| Sessão de trabalho termina com aprendizado | Sugerir `/palace save`: destilar decisões e salvar na sala certa |
| Preferência/fato aparentemente desatualizado | Perguntar se atualiza (não atualizar sozinho) |
