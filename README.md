# 🏛 arandu

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

## ⚡ CLI (fase A — tudo local, stdlib, zero dependências)

```bash
python arandu.py build              # (re)constrói o índice derivado (FTS5)
python arandu.py find "sqlite"      # busca com ranking
python arandu.py wake               # gera o wake-up L0/L1 do momento
python arandu.py save --room 50-library --title "Exemplo" --text "..." --tags ui
python arandu.py stats | audit | graph | rooms
```

O `.palace/cache.sqlite` (e o `wake-up.md`) são **derivados** — `.gitignore`, re-geráveis com `build`, **sem migrations**. Rotinas de IA: `/palace-save`, `/palace-recall`, `/palace-audit` (comandos em `.opencode/command/`).
