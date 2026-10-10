# Passos detalhados

Detalhe dos passos 3 a 7 do `SKILL.md`. Leia a seção do passo em que estiver.

## 3. Contas

Liste, só com leituras, as contas, workspaces, portais, subdomínios ou projetos visíveis. Para cada uma: nome, ID, para que serve, moeda e fuso quando existirem, e o perfil ou variável que a seleciona. Mostre a lista e pergunte quais são de uso real e qual é a padrão; a padrão vai para o frontmatter do `README.md` (`default_account`).

## 4. Objetos e propriedades

Para cada objeto relevante ao objetivo (modelo: `templates/object.md`):

- Puxe o **schema** pelo endpoint ou tool de metadados (propriedades, campos customizados, tipos de evento), não por amostras: amostra mostra só o que está preenchido.
- Registre por propriedade: nome na API, rótulo na interface, tipo, se é obrigatório ou somente leitura, opções de enum com os **IDs** (status de funil, estágios, listas, tags), e para que serve no negócio quando não for óbvio.
- Registre as **relações** (lead → contato → empresa; campanha → adset → anúncio) e como se navega entre elas.
- Leia 1 a 3 registros reais só para confirmar o formato. Não copie dados pessoais para o mapa.

Objetos fora do objetivo entram como uma linha na tabela do `README.md`, sem arquivo próprio.

## 5. Payloads

Para cada operação comum (listar, buscar, criar, atualizar, mover…), guarde o par request/response **que funcionou**, mínimo, com o caminho ou tool, parâmetros, corpo e um trecho da resposta (modelo: `templates/payload.md`).

- Leituras: rode de verdade.
- Escritas: não execute só para documentar. Na ordem:
  1. dry-run, sandbox ou validação da própria API (`validate_only`, modo test), quando houver;
  2. uma escrita que o usuário já pediu nesta sessão: registre o payload dela;
  3. se a ferramenta não tem nada disso (comum em CRMs e gerenciadores de tarefa), proponha ao usuário **uma** escrita reversível num objeto de teste (criar um lead "teste mise-en-place" e apagar em seguida, por exemplo) e só faça com o sim dele;
  4. senão, registre a partir da documentação e marque `docs`.
- Escrita que gaste dinheiro, envie mensagem a terceiros ou apague dados reais nunca entra no passo 3.
- Anote os erros que apareceram e o que os resolveu: é a parte mais valiosa do mapa.

## 6. Redação e segredos

- **Nunca** grave token, senha, API key, cookie ou URL assinada nos arquivos `.md` nem no `data.example.json`. Credencial aparece como `$NOME_DA_VARIAVEL` ou `<TOKEN>`. Prefira variável de ambiente ou o cofre do usuário. Se a convenção do destino já guarda credenciais num `*.local.json`, siga-a só depois de confirmar que esse arquivo está fora do git, e avise o usuário que o token fica em texto claro ali.
- Dados pessoais (nome, e-mail, telefone, documento, endereço de leads e clientes) viram placeholders: `<NOME>`, `<EMAIL>`, `<TELEFONE>`, `<CPF>`, `<ENDERECO>`.
- IDs de conta, página, funil e campo **não são segredo** e são o que torna o mapa útil. Em repo público ou compartilhado, os `.md` usam `<AD_ACCOUNT_ID>` e os IDs reais ficam no `data.local.json`, com a mesma forma do `data.example.json` (confira se o `.gitignore` cobre `*.local.json` e ofereça adicionar). Em vault ou repo privado, IDs na tabela do `README.md` são aceitáveis e mais práticos.
- Rode a checagem. `scripts/check_secrets.py` fica na pasta da skill e só usa a biblioteca padrão do Python:

```bash
python3 <pasta-da-skill>/scripts/check_secrets.py [--public] <destino>/<ferramenta>
```

  - Procura JWTs, bearer tokens, `*_token`/`*_secret` com valor, chaves com prefixo conhecido, tokens hexadecimais, e-mails, telefones, CPF/CNPJ (só dígitos, quando há rótulo na linha) e strings longas de alta entropia.
  - Pula `*.local.json` e `*.local.md`, que guardam os dados reais por convenção (`--include-local` para varrer também).
  - Com `--public`, acusa também IDs reais (`act_…`, `gid://…`, números de 15+ dígitos). Use quando o destino for repo público.
  - Nomes e endereços não têm padrão confiável: releia as amostras à mão.
  - Corrija tudo que ele apontar ou justifique ao usuário o falso positivo.
  - `--self-test` roda os casos de exemplo do próprio script.
- Sem Python na sessão, faça a busca à mão, por exemplo `grep -rnE 'eyJ|Bearer [A-Za-z0-9]|sk_|_token"?: ?"?[A-Za-z0-9]|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|9[0-9]{4}-?[0-9]{4}' <destino>/<ferramenta>`.

## 7. Steering (`rules.md`)

Escreva as regras que uma sessão futura precisa seguir para não errar (modelo: `templates/rules.md`). Use `steering-checklist.md` como roteiro: limites de taxa e paginação, quais operações são irreversíveis ou custam dinheiro, defaults seguros (ex.: criar sempre pausado), convenções de nome da conta, armadilhas de formato (moeda em centavos, fuso, IDs como string), e quando parar e perguntar. Cada regra em uma linha, com o porquê quando ele não for óbvio.
