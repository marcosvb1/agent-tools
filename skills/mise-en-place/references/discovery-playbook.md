# Discovery playbook

Como descobrir contas, schema e payloads por rota de acesso, e onde cada ferramenta comum expõe seus metadados. Os endpoints abaixo são pontos de partida conhecidos; confirme na documentação atual (Context7 ou docs oficiais) antes de registrar como fato, porque versões de API mudam.

## Por rota de acesso

### Conector MCP

1. `ToolSearch` com o nome da ferramenta para carregar as tools (onde não houver `ToolSearch`, olhe a lista de tools da sessão). Leia a descrição de cada uma: ela costuma listar os objetos cobertos.
2. Procure tools de metadados antes das de dados: nomes com `schema`, `properties`, `fields`, `describe`, `get_*_types`, `list_*`, `discover`, `tool_guidance`.
3. Registre no `README.md` do mapa o nome exato de cada tool usada por operação (ex.: "criar anúncio → `ads_create_ad`"). Nomes de tool mudam entre conectores da mesma ferramenta; anote qual conector.
4. Anote o que o conector **não** cobre e que exigiria API direta.

### CLI

1. `<cli> --help` e `<cli> <recurso> --help` para listar recursos e flags.
2. Prefira saída estruturada (`--json`, `-o json`, `--format json`) e registre a flag.
3. Registre como a CLI escolhe conta/projeto (`--project`, perfil, variável de ambiente) e como ver o contexto atual (`gcloud config list`, `gh auth status`).

### API HTTP

1. Descubra a URL base e a versão. Registre a versão usada.
2. Registre autenticação só pelo nome da variável: `Authorization: Bearer $FERRAMENTA_TOKEN`.
3. Procure, nesta ordem: spec OpenAPI/GraphQL introspection, endpoint de metadados/campos, endpoint "me"/"account" para descobrir contas, e só então listagens de registros com `limit` pequeno.
4. Registre paginação (cursor, offset, `next`), limite de taxa (cabeçalhos `X-RateLimit-*`, `Retry-After`) e formato de erro.

### Banco de dados

1. Liste schemas e tabelas (`information_schema`, `\d` no psql).
2. Para tabelas do objetivo: colunas, tipos, nulos, chaves, índices e FKs.
3. Registre enums e tabelas de domínio (status, tipos) com seus valores.
4. Use `LIMIT` em toda amostra e nunca copie linhas com dados pessoais.

### Só documentação

Use Context7 (`resolve-library-id` e `query-docs`) ou a documentação oficial. Marque tudo como `docs` e liste no fim do `README.md` do mapa o que precisa ser verificado quando houver acesso.

## Onde ficam os metadados em ferramentas comuns

| Ferramenta | Contas | Schema / metadados | Observações |
| --- | --- | --- | --- |
| Meta Ads (Graph API) | `GET /me/adaccounts`, `GET /me/accounts` (páginas) | `GET /<id>?metadata=1`; campos por objeto na referência da Marketing API | IDs de conta com prefixo `act_`. Orçamento em centavos da moeda da conta. Criativo não muda depois de criado. |
| TikTok Ads (Business API) | `GET /oauth2/advertiser/get/` | Referência de campos por endpoint (`/campaign/get/`, `/adgroup/get/`, `/ad/get/`) | `advertiser_id` obrigatório em quase toda chamada. Fuso e moeda são da conta. |
| HubSpot | `GET /account-info/v3/details` | `GET /crm/v3/properties/{objectType}`, `GET /crm/v3/schemas`, pipelines em `GET /crm/v3/pipelines/{objectType}` | Propriedade tem `name` (API) e `label`. Estágios de pipeline têm IDs próprios. |
| Kommo / amoCRM | subdomínio da conta; `GET /api/v4/account` | `GET /api/v4/leads/pipelines` (funis e status), `GET /api/v4/{entity}/custom_fields` | Status de funil têm ID numérico; campos customizados têm `field_id` e `enum_id` por opção. |
| ClickUp | `GET /team` (workspaces) | `GET /space/{id}`, `GET /list/{id}/field` (campos customizados), statuses por lista ou space | Status e campos podem variar por lista. |
| Notion | `GET /users/me`, `POST /search` | `GET /data_sources/{id}` nas versões recentes da API (`GET /databases/{id}` nas antigas): propriedades e opções de select | IDs de opção de select e de propriedade são estáveis; nomes não. |
| Shopify (Admin GraphQL) | loja do token | introspection GraphQL; metafield definitions | IDs são GIDs (`gid://shopify/Product/...`). |
| Stripe | conta do token; `GET /v1/account` | referência da API; `expand[]` para relações | Valores em centavos; modo test e live têm IDs diferentes. |
| WhatsApp Cloud API | `GET /{business_id}/owned_whatsapp_business_accounts` | templates em `GET /{waba_id}/message_templates` | Mensagem fora da janela de 24h exige template aprovado. |
| n8n | instância e projeto | `GET /api/v1/workflows`; credenciais pelo nome e tipo vistos nos nós do workflow (a API pública lista pouco de credenciais) | Registre IDs de workflow e de credencial, nunca o conteúdo da credencial. |
| Google Ads | MCC e contas filhas (`customers:listAccessibleCustomers`) | GAQL `SELECT ... FROM` com `GoogleAdsFieldService` | `login-customer-id` define o MCC; IDs sem hífen. |
| Postgres / Supabase | projeto ou database | `information_schema`, `pg_enum` | RLS muda o que cada chave enxerga; registre qual papel foi usado. |

## Amostragem segura

- `limit` 1 a 3. Para entender um enum, use o endpoint de metadados, não centenas de registros.
- Antes de colar uma resposta no mapa, apague ou substitua por placeholder: nomes, e-mails, telefones, documentos, endereços, URLs com token, conteúdo de mensagens.
- Corte respostas longas: mantenha a estrutura (chaves e tipos) e um exemplo de cada lista.
