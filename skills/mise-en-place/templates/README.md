# <Ferramenta>: <o que se faz com ela>

Use quando: <situações em que este mapa deve ser lido, nas palavras do usuário (ex.: "mover lead de etapa", "subir anúncio na conta X")>. Skill operacional: <`.claude/skills/<ferramenta>-ops/`, se houver>.

> Leia antes de operar. Regras em [rules.md](rules.md) (ferramenta pequena: troque o link por uma seção `## Regras` neste arquivo). IDs e config em `data.local.json` (forma em [data.example.json](data.example.json)).
> Atualizado em AAAA-MM-DD. Origem dos fatos: `verificado AAAA-MM-DD`, `docs` ou `inferido`.

## Para que serve

<Uma ou duas frases: o que o usuário faz com esta ferramenta e qual objetivo guiou este mapa.>

## Acesso

| Item | Valor | Origem |
| --- | --- | --- |
| Rota | <conector MCP "<nome>" / CLI `<cli>` / API HTTP / só docs> | verificado AAAA-MM-DD |
| URL base e versão | `<https://api.exemplo.com/v1>` | |
| Credencial | variável `$<FERRAMENTA>_TOKEN` (nunca o valor) | |
| Como escolher a conta | <parâmetro, perfil, variável `$<FERRAMENTA>_ACCOUNT_<PERFIL>`> | |

## Contas

| Nome | ID | Uso | Moeda / fuso | Padrão |
| --- | --- | --- | --- | --- |
| <conta-a> | `<ACCOUNT_ID>` | <para que serve> | <BRL / America/Sao_Paulo> | sim |

<Em repo público ou compartilhado, troque os IDs por placeholders; os reais ficam em `data.local.json`, fora do git.>

## Objetos

| Objeto | Para que serve | Detalhe | Origem |
| --- | --- | --- | --- |
| <lead> | <oportunidade no funil> | [objects/lead.md](objects/lead.md) | verificado AAAA-MM-DD |
| <tarefa> | <fora do objetivo; só listado> | — | docs |

Relações: <campanha → adset → anúncio> / <lead → contato → empresa>.

## Operações

| Quero… | Como (tool, comando ou endpoint) | Payload | Origem |
| --- | --- | --- | --- |
| <listar leads de um funil> | `<GET /leads?filter[pipeline_id]=<ID>>` | [payloads/listar-leads.md](payloads/listar-leads.md) | verificado AAAA-MM-DD |
| <criar lead> | `<POST /leads>` | [payloads/criar-lead.md](payloads/criar-lead.md) | docs |

## Pendências

- <O que ficou como `docs` e precisa ser verificado quando houver acesso.>

## Histórico

- AAAA-MM-DD: mapa criado (<rota>, <n> contas, <n> objetos).
