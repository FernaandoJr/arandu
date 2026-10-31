# 🏛 hikma

Palácio de memória pessoal para IAs: fatos, skills, projetos, preferências e bibliotecas de referência — tudo **versionado em Markdown + Git**.

## Princípios

- **A fonte da verdade é Markdown.** Qualquer índice/RAG/cache é derivado e re-gerável (`cache.sqlite` nunca é versionado).
- **1 ideia = 1 bloco** YAML atômico (formato em `00-reception/protocol.md`).
- **Tudo versionado:** preferências não se apagam, arquivam (`status: archive`).
- **Segredos jamais** entram aqui.

## Mapa rápido

| Sala | O que vive lá |
|---|---|
| `00-reception/` | Mapa do palácio + protocolo de blocos |
| `10-person/` | Quem sou, preferências, objetivos |
| `20-skills/` | Como eu gosto que as coisas sejam feitas |
| `30-projects/` | Projetos vivos e suas decisões |
| `40-facts/` | Fatos frios: pessoas, contexto técnico |
| `50-library/` | Sites, referências de UI, ideias, leituras |
| `90-archive/` | Porão — conteúdo vencido, nunca deletado |

As IAs entram por [`AGENTS.md`](./AGENTS.md) e navegam desde [`00-reception/index.md`](./00-reception/index.md).
