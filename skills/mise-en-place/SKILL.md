---
name: mise-en-place
description: This skill should be used when the user wants to build, update or audit the reference map of a tool, API, connector or SaaS account — its access route, accounts, objects, properties, IDs, payloads and rules of use — saved as files Claude reads before operating it, e.g. "faz o mise en place do Kommo", "atualiza o mapa do ClickUp", "audita as references do Meta Ads", "monta as references dessa ferramenta", "mapeia as contas e objetos do HubSpot", "documenta os payloads que funcionam no TikTok", "map this API before we use it". Not for one-off questions about a tool ("quais campos tem no X", "qual o ID do funil Y": answer directly), not for the day-to-day operation itself (use the tool's own skill) and not for writing an MCP server.
---

# Mise en place

Antes de cozinhar, tudo no lugar: para cada ferramenta com que o Claude trabalha, um mapa curto e verificado de **como acessar**, **quais contas existem**, **quais objetos e propriedades importam**, **quais payloads funcionam** e **quais regras seguir**. Sessões futuras (e a skill operacional da ferramenta) leem o mapa antes de agir, em vez de redescobrir tudo ou chutar IDs e nomes de campo.

O mapa vale pelo que foi **verificado**. Cada fato registra de onde veio e quando: `verificado AAAA-MM-DD`, `docs` ou `inferido`.

## Resultado

Uma pasta por ferramenta, dentro da pasta de references do usuário:

```
<destino>/<ferramenta>/
  README.md           # o mapa: frontmatter, "Use quando", acesso, contas, objetos, operações
  rules.md            # steering: regras, limites, armadilhas, o que pede confirmação
  objects/<objeto>.md # propriedades, tipos, enums, IDs, relações
  payloads/<op>.md    # request e response verificados de cada operação comum
  data.example.json   # forma dos IDs e da config, com placeholders e _validated_at
  data.local.json     # os IDs reais nessa forma; fica fora do git
```

- O `README.md` abre com um frontmatter fixo (`tool`, `route`, `default_account`, `validated_at` em ISO), para que um hook ou outra skill consiga ler a conta padrão e a idade do mapa.
- Ferramenta pequena cabe toda no `README.md`, com as regras numa seção `## Regras`. Assuntos que crescem viram arquivos soltos, como `gotcha-<assunto>.md`. Não crie arquivos vazios.
- Se o destino já tiver pastas de outras ferramentas, **siga a convenção de lá**: o mapa novo deve parecer irmão dos que já existem.

Modelos em `templates/`. O detalhe dos passos 3 a 7 está em `references/passos-detalhados.md`.

## Fluxo

### 1. Escopo

Descubra sozinho o que der e pergunte no máximo duas coisas, numa mensagem só:

- **Ferramenta e objetivo** (para que o mapa vai servir: "subir anúncios", "mover leads no funil"). Costuma vir no pedido; o objetivo decide o que é detalhado e o que só é listado.
- **Destino**. Procure antes de perguntar, nesta ordem: um mapa que já exista da ferramenta (vira atualização, veja abaixo), a pasta `references/` da skill da ferramenta, a pasta de references do vault ou projeto (`docs/references/`, `references/`, `refs/`), e por fim `./.claude/mise-en-place/<ferramenta>/`. Só pergunte se houver mais de um candidato.
- **Visibilidade**. Se o destino estiver num repo git, veja o remote (`git remote -v`; `gh repo view --json visibility` quando houver `gh`). Sem como confirmar, trate como **público** e avise; o usuário pode dizer que é privado.

Contas não se perguntam aqui: o passo 3 lista as que o acesso enxerga.

### 2. Rota de acesso

Descubra como a sessão fala com a ferramenta, nesta ordem, e registre a escolhida no `README.md`:

1. **Conector MCP** na sessão (procure com `ToolSearch` pelo nome da ferramenta, ou na lista de tools onde `ToolSearch` não existir). Preferido: não precisa de token.
2. **CLI** instalada e logada (`gh`, `gcloud`, `stripe`, `supabase`…).
3. **API HTTP** com credencial em variável de ambiente. Registre só o **nome** da variável.
4. **Documentação** (Context7, docs oficiais) quando não houver acesso: tudo sai marcado `docs`.

Sem rota nenhuma, diga qual conector ou variável faltaria e ofereça seguir só com a documentação. Táticas por rota e endpoints de schema de ferramentas comuns: `references/discovery-playbook.md`.

### 3. Contas

Liste com leituras as contas, workspaces ou projetos visíveis e confirme com o usuário quais são de uso real e qual é a padrão.

### 4. Objetos e propriedades

Schema pelo endpoint de metadados, não por amostras; propriedades com nome na API, tipo e IDs de enum; relações entre objetos. Detalhe em `references/passos-detalhados.md`.

### 5. Payloads

Request e response que funcionaram para cada operação comum, e os erros vistos com a correção. Leituras rodam de verdade; escritas só por dry-run, por uma escrita que o usuário já pediu, ou por uma escrita de teste reversível que ele aprove. Nada que gaste dinheiro, envie mensagem ou apague dado real.

### 6. Redação e segredos

Nenhuma credencial nos `.md` nem no `data.example.json`; dados pessoais viram placeholders; em repo público os IDs reais vão só para o `data.local.json`. Antes de entregar, rode:

```bash
python3 <pasta-da-skill>/scripts/check_secrets.py [--public] <destino>/<ferramenta>
```

Use `--public` quando o destino for repo público. Corrija o que ele apontar ou justifique o falso positivo. Opções e o que fazer sem Python: `references/passos-detalhados.md`.

### 7. Steering (`rules.md`)

As regras que uma sessão futura precisa seguir para não errar, uma por linha, com o porquê quando não for óbvio. Roteiro: `references/steering-checklist.md`.

### 8. Ligar o mapa ao trabalho

O mapa só ajuda se for lido. Ofereça, conforme o caso: uma linha no `SKILL.md` da skill da ferramenta ("antes de operar, leia `<destino>/<ferramenta>/README.md`"); uma linha no índice da pasta de references, no registro de ferramentas conectadas (ex.: `connections.md`) ou no `CLAUDE.md`; ou, se o uso for recorrente e não houver skill da ferramenta, criar uma com `skill-creator`.

Feche com um resumo curto: rota, contas, objetos e operações cobertos, o que ficou como `docs` e o que a checagem encontrou.

## Atualizar ou auditar um mapa

1. Leia o `README.md` do mapa: `validated_at` no frontmatter e a coluna `Origem` de cada linha.
2. Repita os passos 3 a 5 só em leitura e compare: contas novas ou removidas, propriedades e enums que mudaram, IDs que sumiram, linhas `docs` que agora dá para verificar.
3. Mostre as diferenças antes de reescrever.
4. Atualize o `rules.md` com o que mudou e rode a checagem de segredos de novo.
5. Atualize `validated_at` (no `README.md` e no `data.example.json`) e registre a mudança na seção "Histórico".

## Princípios

- **Curto e navegável.** O `README.md` do mapa é lido inteiro em toda sessão: abaixo de ~200 linhas, com o detalhe em `objects/` e `payloads/`.
- **Verificado vence completo.** Dez propriedades confirmadas valem mais que duzentas copiadas da documentação.
- **IDs em tabela.** "ID do estágio Qualificado" tem que ser achado num olhar.
- **Só leitura por padrão.** Mapear não é operar.
