# Protocolo de Blocos de Memória

Toda memória no palácio é **um bloco YAML atômico** dentro da sala de destino. Sem exceções.

## Formato

```md
---
id: pre-<slug-unico>          # prefixos: pref- | fato- | skill- | proj- | ref- | ideia-
room: 10-person               # sala de destino
tags: [tag1, tag2]            # 2-5 tags, minusculas, sem espaco
status: hot                   # hot | active | archive
entry: 2026-10-31             # data de criacao
updated: 2026-10-31           # bump a cada edicao
source: ""                    # opcional: URL/origem do fato / link (refs: obrigatorio)
---

<2 a 6 linhas de conteudo. Uma ideia so. Se precisar de mais,
abra outro bloco e ligue com [[id-do-artigo-relacionado]]>
```

## Regras

1. **1 ideia = 1 bloco.** Bloco grande = dois blocos + link.
2. **`status` é o ciclo de vida:**
   - `hot` — influencia o dia a dia (preferências ativas, decisões recentes)
   - `active` — relevante mas periodicamente revisada (projetos, skills)
   - `archive` — vencido/deprecado. **Nunca deletar — mover para `90-archive/`**
3. **Links vencem a repetição:** mesma informação em duas salas = um bloco + `[[link]]` no outro.
4. **YAML estrito:** os campos acima são o contrato. Campo novo = discussão com Fernando antes (o índice futuro re-parseia tudo).
5. **Dedupe antes de escrever:** grep pelo `id`/tema. Existe? Atualize (`updated` + conteúdo) em vez de duplicar.
6. **Sem segredos.** Contexto técnico sim; credenciais nunca.
7. **Commit previsível:** `palace: add <tema>` / `palace: update <id>` / `palace: archive <id>` — o `git log` é a linha do tempo da memória.

## Para referências da biblioteca (`50-library/`)

- `source` (URL) é **obrigatório**
- `status` ganha ciclo próprio: `unread → absorbed → archive`
- **`absorbed`** = consumido + destilado: o takeaway vira coisa em `10-person/` ou `20-skills/`, o link permanece como fonte
- Contexto de "por que salvei" é **obrigatório** — link sem contexto não entra no palácio
