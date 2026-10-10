---
name: mise-en-place
description: This skill should be used when the user wants to map a tool, API, connector or SaaS account before working with it — its accounts, objects, properties, IDs, payloads and rules of use — and save that as reference files Claude can steer by, e.g. "monta o mise en place do HubSpot", "mapeia as contas e objetos do Kommo", "documenta os payloads que funcionam no Meta Ads", "cria as references dessa ferramenta", "levanta os IDs dos funis e estágios", "quais campos customizados tem no X", "prepara o terreno antes de usar o Y", "faz o mise en place", "atualiza o mapa do ClickUp", "map this API for me", "build a reference for this tool", including refreshing or auditing an existing map. Not for doing the day-to-day operation itself (use the tool's own skill) nor for writing an MCP server.
---

# Mise en place

Antes de cozinhar, tudo no lugar: para cada ferramenta com que o Claude vai trabalhar, monte um mapa curto e verificado de **como acessar**, **quais contas existem**, **quais objetos e propriedades importam**, **quais payloads funcionam** e **quais regras seguir**. O resultado é uma pasta de references que qualquer sessão futura (ou uma skill específica da ferramenta) lê antes de agir, em vez de redescobrir tudo ou chutar IDs e nomes de campo.

O mapa vale pelo que foi **verificado**. Cada fato registra de onde veio (chamada real, documentação ou inferência) e quando, para que quem ler saiba o quanto confiar.

## Resultado

Uma pasta por ferramenta:

```
<destino>/<ferramenta>/
  MAP.md              # índice: acesso, contas, objetos, operações, links para o resto
  rules.md            # steering: regras, limites, armadilhas, o que pede confirmação
  objects/<objeto>.md # propriedades, tipos, enums, IDs, relações
  payloads/<op>.md    # request e response verificados de cada operação comum
```

Ferramenta pequena (um objeto, duas operações) cabe toda no `MAP.md`: as regras viram uma seção `## Regras` nele e o link para `rules.md` sai. Não crie arquivos vazios.

Modelos em `templates/`: `MAP.md` (passos 2 e 3), `object.md` (passo 4), `payload.md` (passo 5) e `rules.md` (passo 7).

## Fluxo

### 1. Escopo

Pergunte (em uma mensagem só, com defaults sugeridos):

- **Ferramenta e contas**: qual ferramenta, quais contas ou workspaces entram (todas que o acesso enxergar, por padrão).
- **Objetivo**: para que o mapa vai servir (ex.: "subir anúncios", "mover leads no funil"). Isso decide quais objetos e operações detalhar; o resto entra só listado.
- **Destino**: onde gravar. Ordem de preferência:
  1. a pasta `references/` de uma skill da ferramenta, se ela existir ou for ser criada;
  2. a pasta onde o vault ou o projeto do usuário já guarda references (procure por `references/`, `refs/`, `docs/tools/` antes de perguntar);
  3. `./.claude/mise-en-place/<ferramenta>/` no projeto atual.
- **Onde o mapa vai morar**: repositório público, privado ou só local. Isso decide o nível de redação (passo 6). Tente descobrir antes de perguntar: se o destino estiver num repo git, veja o remote e a visibilidade (`git remote -v`, `gh repo view --json visibility`).

### 2. Rota de acesso

Descubra como a sessão fala com a ferramenta, nesta ordem, e registre a escolhida no `MAP.md`:

1. **Conector MCP** já na sessão (procure com `ToolSearch` pelo nome da ferramenta, ou confira a lista de tools e conectores da sessão onde `ToolSearch` não existir). Preferido: não precisa de token.
2. **CLI** instalada e logada (`gh`, `gcloud`, `stripe`, `supabase`…).
3. **API HTTP** com credencial em variável de ambiente. Registre só o **nome** da variável, nunca o valor.
4. **Documentação** (Context7, docs oficiais) quando não houver acesso: o mapa sai marcado como `docs`, sem nada verificado.

Se nenhuma rota existir, diga qual conector ou variável faltaria e ofereça seguir só com a documentação. Táticas por rota e endpoints de schema de ferramentas comuns estão em `references/discovery-playbook.md`.

### 3. Contas

Liste, só com leituras, as contas, workspaces, portais, subdomínios ou projetos visíveis. Para cada uma: nome, ID, para que serve, moeda e fuso quando existirem, e o perfil ou variável que a seleciona. Confirme com o usuário quais são as de uso real e qual é a padrão.

### 4. Objetos e propriedades

Para cada objeto relevante ao objetivo:

- Puxe o **schema** pelo endpoint ou tool de metadados (propriedades, campos customizados, tipos de evento), não por amostras: amostra mostra só o que está preenchido.
- Registre por propriedade: nome na API, rótulo na interface, tipo, se é obrigatório ou somente leitura, opções de enum com os **IDs** (status de funil, estágios, listas, tags), e para que serve no negócio quando não for óbvio.
- Registre as **relações** (lead → contato → empresa; campanha → adset → anúncio) e como se navega entre elas.
- Leia 1 a 3 registros reais só para confirmar o formato. Não copie dados pessoais para o mapa.

Objetos fora do objetivo entram como uma linha na tabela do `MAP.md`, sem arquivo próprio.

### 5. Payloads

Para cada operação comum (listar, buscar, criar, atualizar, mover…), guarde o par request/response **que funcionou**, mínimo, com o caminho ou tool, parâmetros, corpo e um trecho da resposta.

- Leituras: rode de verdade.
- Escritas: não execute só para documentar. Use dry-run, sandbox ou validação da própria API quando houver; senão registre a partir de uma escrita que o usuário já pediu nesta sessão, ou marque como `docs` (não verificado). Qualquer escrita que gaste dinheiro, envie mensagem a terceiros ou apague dados pede confirmação explícita.
- Anote os erros que apareceram e o que os resolveu: é a parte mais valiosa do mapa.

### 6. Redação e segredos

- **Nunca** grave token, senha, API key, cookie ou URL assinada. Credencial aparece como `$NOME_DA_VARIAVEL` ou `<TOKEN>`.
- Dados pessoais (nome, e-mail, telefone de leads e clientes) viram placeholders: `<EMAIL>`, `<NOME>`, `<TELEFONE>`.
- IDs de conta, página, funil e campo **não são segredo** e são o que torna o mapa útil, mas só vão para um repositório **público** se o usuário disser que pode. Em repo público, use `<AD_ACCOUNT_ID>` e deixe os IDs reais num `MAP.local.md` ao lado, ignorado pelo git (confira se o `.gitignore` cobre `*.local.md` e ofereça adicionar), referenciado no `MAP.md`.
- Antes de entregar, rode a checagem (`scripts/check_secrets.py` fica na pasta desta skill; só usa a biblioteca padrão do Python):

```bash
python3 <pasta-desta-skill>/scripts/check_secrets.py <destino>/<ferramenta>
```

O script procura JWTs, bearer tokens, chaves com prefixo conhecido, tokens hexadecimais, e-mails, telefones, CPF/CNPJ e strings longas de alta entropia. Corrija tudo que ele apontar ou justifique ao usuário por que é falso positivo (cursores de paginação costumam ser).

Sem Python na sessão, faça a mesma busca à mão, por exemplo `grep -rnE 'eyJ|Bearer [A-Za-z0-9]|sk_|token=|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|\(?[0-9]{2}\)? ?9?[0-9]{4}-[0-9]{4}' <destino>/<ferramenta>`.

### 7. Steering (`rules.md`)

Escreva as regras que uma sessão futura precisa seguir para não errar. Use `references/steering-checklist.md` como roteiro: limites de taxa e paginação, quais operações são irreversíveis ou custam dinheiro, defaults seguros (ex.: criar sempre pausado), convenções de nome da conta, armadilhas de formato (moeda em centavos, fuso, IDs como string), e quando parar e perguntar. Cada regra em uma linha, com o porquê quando ele não for óbvio.

### 8. Ligar o mapa ao trabalho

O mapa só ajuda se for lido. Ofereça, conforme o caso:

- acrescentar ao `SKILL.md` da skill da ferramenta uma linha "antes de operar, leia `references/<ferramenta>/MAP.md`";
- acrescentar ao `CLAUDE.md` do projeto ou ao índice do vault um link para o mapa;
- se não existir skill da ferramenta e o uso for recorrente, sugerir criar uma (com `skill-creator`) que use o mapa como reference.

Feche com um resumo curto: rota de acesso, contas mapeadas, objetos e operações cobertos, o que ficou como `docs` (não verificado) e o que a checagem de segredos encontrou.

## Atualizar um mapa existente

Quando o usuário pedir para atualizar ou auditar:

1. Leia o `MAP.md` e veja a data de cada linha na coluna `Origem` (e a data do cabeçalho de cada arquivo).
2. Repita os passos 3 a 5 só em leitura e compare: contas novas ou removidas, propriedades e opções de enum que mudaram, IDs que não existem mais, linhas `docs` que agora dá para verificar.
3. Mostre as diferenças ao usuário antes de reescrever.
4. Atualize o `rules.md` com o que mudou (limites, enums, erros novos) e rode a checagem de segredos de novo (passos 6 e 7).
5. Atualize as datas e registre a mudança na seção "Histórico" do `MAP.md`.

## Princípios

- **Curto e navegável.** O `MAP.md` é lido inteiro em toda sessão; mantenha-o abaixo de ~200 linhas e mande o detalhe para `objects/` e `payloads/`.
- **Verificado vence completo.** Melhor dez propriedades confirmadas que duzentas copiadas da documentação. Marque a origem: `verificado AAAA-MM-DD`, `docs` ou `inferido`.
- **IDs em tabela.** Quem opera precisa achar "ID do estágio Qualificado" em um olhar.
- **Só leitura por padrão.** Mapear não é operar.
