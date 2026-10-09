---
name: meta-ads-upload
description: |
  This skill should be used when the user wants to create, update, duplicate/clone, move, or audit Meta (Facebook/Instagram) Ads campaigns, ad sets, or ads, through the official Meta Ads connector when available or the Graph API otherwise — e.g. "upload this video as a Meta ad", "create an adset", "clone this campaign", "move this adset to another campaign", "swap the creative on ad 120...", "turn this Instagram post into an ad", "subir anuncio", "criar adset", "clonar campanha", "replicar adset", "mover adset", "duplicar anuncio", "trocar criativo", "copiar ad pra outro adset". Auditing an existing campaign's ad sets and naming before creating is in scope. Not for performance reporting, dashboards, data exports, or n8n/Google Sheets integrations.
---

# Meta Ads Upload

Skill operacional para gerenciar anuncios no Meta Ads. Funciona para qualquer conta e tem dois caminhos: o conector oficial do Meta Ads (MCP), quando ele estiver na sessao, e um runner Python proprio (Graph API) com modos `create`, `update`, `audit` e `duplicate`.

## Qual caminho usar

1. **Conector oficial do Meta Ads (preferido).** Se a sessao tiver as tools `ads_*` do MCP do Meta (por exemplo `ads_get_ad_accounts`, `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_create_creative`, `ads_creative_upload_media`, `ads_update_entity`, `ads_get_ad_entities`), use-as. Nao precisa de token, de variavel de ambiente nem de `/ads-ops:setup`: o login e o do proprio conector. Descubra conta, pagina e Instagram com `ads_get_ad_accounts`, `ads_get_ad_account_pages` e `ads_get_ig_accounts` e confirme com o usuario qual usar. Se existir um perfil do ads-ops (veja "Contas e credenciais"), use o `ad_account` dele como sugestao.
2. **Runner Python (plano B).** Use quando nao houver conector do Meta na sessao, ou para o que o conector nao cobre bem: duplicar campanha inteira com filhos pelo `/copies` (`deep_copy`), mover adsets ou ads de lugar, jobs em lote a partir de um JSON e numeracao automatica de adsets. O runner precisa de token em variavel de ambiente e de rede para `graph.facebook.com`.

As regras de seguranca abaixo valem para os dois caminhos. No conector:

- Crie campanhas, adsets e ads sempre pausados (`PAUSED`). Para mexer em algo que ja roda, use `ads_update_entity` e lembre que creative nao muda depois de criado: troca de criativo e um creative novo num ad novo, ou o modo `update` do runner.
- `ads_activate_entity` e `ads_boost_ig_post` com `confirmed: true` gastam dinheiro. So chame depois de mostrar o resumo (conta, budget, publico, datas, link) e o usuario confirmar explicitamente.
- Para duplicar um item so, passe `source_campaign_id`, `source_adset_id` ou `source_ad_id` na tool de criacao. Para copiar a arvore inteira, use o runner.
- Antes de criar adset, liste os existentes com `ads_get_ad_entities` para seguir a numeracao da conta.
- Se uma chamada falhar, use `ads_get_errors` para entender o motivo antes de tentar de novo.

O restante deste arquivo descreve o runner.

## Onde esta o executor

Tudo fica dentro desta skill (`${CLAUDE_PLUGIN_ROOT}/skills/meta-ads-upload/`):

- Runner: `scripts/run_meta_job.py`
- Core: `scripts/meta_ads_core.py` (depende de `requests`)
- Templates de input: `templates/*.template.json`
- Referencia de endpoints: `references/meta-ads-endpoints.md`, com payloads e respostas de cada endpoint da Graph API, incluindo os de `/copies`.

Os relatorios de cada execucao vao para `./ads-ops-runs/meta/` no diretorio atual (ou para `$ADS_OPS_RUNS_DIR/meta/`).

## Regra de seguranca operacional

O dry-run existe porque erros em producao custam dinheiro real — um adset criado com budget errado roda antes de voce perceber. Por isso:

- Sempre comecar em dry-run (default do runner). No dry-run as leituras (GET) rodam de verdade, entao `audit` e a numeracao automatica usam dados reais; as escritas nao sao enviadas e aparecem em `planned_calls` no relatorio, com metodo, caminho e parametros
- So usar `--execute` quando o payload estiver revisado e o usuario tiver confirmado
- Status default: `PAUSED` — tanto para criacao quanto para duplicacao
- Antes de criar adset, sempre auditar a numeracao com `--mode audit`
- Nunca gravar token em arquivo de config, template ou JSON de input

## Contas e credenciais

Esta secao vale para o runner. No conector oficial a conta vem de `ads_get_ad_accounts` e nao ha token para configurar; o perfil, se existir, serve so para sugerir a conta padrao.

O runner resolve a conta nesta ordem (o primeiro que tiver o valor ganha):

1. `context` dentro do JSON do job (`ad_account`, `page_id`, `ig_user_id`, `api_version`), so quando o usuario pedir explicitamente outra conta para aquele job
2. O perfil escolhido com `--profile <nome>` (ou o `default_profile`) no arquivo de config do ads-ops
3. Variaveis de ambiente `META_AD_ACCOUNT_<PERFIL>`, `META_PAGE_ID_<PERFIL>`, `META_IG_USER_ID_<PERFIL>`
4. Variaveis genericas `META_AD_ACCOUNT`, `META_PAGE_ID`, `META_IG_USER_ID`, `META_API_VERSION` (default `v25.0`)

O token vem so de variavel de ambiente: `META_ACCESS_TOKEN_<PERFIL>` ou `META_ACCESS_TOKEN`. `<PERFIL>` e o nome do perfil em maiusculas, com `-` trocado por `_` (perfil `cliente-a` → `META_ACCESS_TOKEN_CLIENTE_A`).

O arquivo de config e procurado em `$ADS_OPS_CONFIG`, depois `./.claude/ads-ops.local.json` e por fim `~/.claude/ads-ops.local.json`. Ele e opcional: so e necessario para o runner ou para dar nome as contas que o usuario usa sempre. Se ele nao existir e o usuario quiser cadastrar contas, sugira `/ads-ops:setup`. Formato da secao Meta:

```json
{
  "meta": {
    "default_profile": "cliente-a",
    "profiles": {
      "cliente-a": { "ad_account": "act_<AD_ACCOUNT_ID>", "page_id": "<PAGE_ID>", "ig_user_id": "<IG_USER_ID>" }
    }
  }
}
```

Se faltar conta, pagina ou token, o runner para com uma mensagem dizendo o que configurar. Pergunte ao usuario em vez de inventar IDs.

## Fluxo recomendado

1. Rodar `audit` para ver os adsets atuais e o proximo numero
2. Copiar o template certo (`adsets`, `video_ads`, `image_ads`, `existing_post_ads`, `update_ads` ou `duplicate_*`) para o diretorio de trabalho e preencher os `<PLACEHOLDERS>` com os dados do usuario
3. Rodar `create`, `update` ou `duplicate` em dry-run
4. Revisar o relatorio em `ads-ops-runs/meta/`: conferir `ad_account` e cada item de `planned_calls` (budget, targeting, status, link) e mostrar o resumo ao usuario
5. Com o ok do usuario, rodar de novo com `--execute`

## Comandos

Defina uma vez no shell:

```bash
RUN="python3 ${CLAUDE_PLUGIN_ROOT}/skills/meta-ads-upload/scripts/run_meta_job.py"
```

| Tarefa | Comando |
|---|---|
| Auditar campanha | `$RUN --mode audit --input audit.json` |
| Criar adsets | `$RUN --mode create --input adsets.json` |
| Criar ads de video | `$RUN --mode create --input video_ads.json` |
| Criar ads de imagem | `$RUN --mode create --input image_ads.json` |
| Criar ads de posts existentes do Instagram | `$RUN --mode create --input existing_post_ads.json` |
| Atualizar ads com novo creative | `$RUN --mode update --input update_ads.json` |
| Duplicar campanhas, adsets ou ads | `$RUN --mode duplicate --input duplicate_adsets.json` |

O runner recusa inputs com `<PLACEHOLDERS>` nao preenchidos e inputs com `access_token`. O relatorio traz `status: "ok"` (saida 0), `"partial"` quando algum item falhou (saida 2, veja `result.error` e o `error` de cada item) ou `"error"` (saida 1). Nunca diga ao usuario que deu certo sem conferir isso.

Acrescente `--profile <nome>` para escolher a conta e `--execute` para executar de verdade. `--output <arquivo>` muda onde o relatorio e gravado.

A duplicacao usa o endpoint nativo `/{id}/copies` da Graph API, que e mais seguro e rapido do que ler todos os campos e recriar manualmente. O Meta preserva automaticamente referencias internas (pixels, audiences, creatives). Com `deep_copy: true` numa campanha, todos os adsets e ads filhos sao clonados junto.

## Decisao rapida de modo

- `mode audit`: validar naming e estado da campanha
- `mode create` + `job_type=adsets`: criar adsets novos com controle de numeracao (`auto_number` + `name_template`, ex. `{num:02d} - Publico`)
- `mode create` + `job_type=video_ads`: subir video/creative/ad
- `mode create` + `job_type=image_ads`: subir imagem (ou usar hash), creative e ad
- `mode create` + `job_type=existing_post_ads`: criar creative de post existente + ad
- `mode update`: criar creative com asset customization e atualizar ad existente
- `mode duplicate` + `job_type=campaigns`: clonar campanha inteira (com ou sem filhos via `deep_copy`)
- `mode duplicate` + `job_type=adsets`: clonar adsets (opcionalmente para outra campanha via `campaign_id`)
- `mode duplicate` + `job_type=ads`: clonar ads (opcionalmente para outro adset via `adset_id`)

A numeracao automatica le o numero no inicio do nome dos adsets existentes (`01 - ...`, `02 - ...`). Se a conta usa outro padrao, confirme com o usuario antes de criar.

## Opcoes de duplicacao

Em `mode duplicate`, o input segue o padrao `items[]` com um campo `id` por objeto. Campos no root valem para todos; campos no item sobrescrevem:

| Campo | Descricao |
|-------|-----------|
| `deep_copy` | Clonar filhos junto (default: `true`) |
| `rename_strategy` | `DEEP_RENAME`, `ONLY_TOP_LEVEL_RENAME`, `NO_RENAME` |
| `rename_prefix` | Prefixo adicionado ao nome da copia |
| `rename_suffix` | Sufixo adicionado (default do Meta: "- Copy") |
| `status_option` | `PAUSED` (recomendado), `ACTIVE`, `INHERITED_FROM_SOURCE` |
| `start_time` | ISO datetime para agendar inicio |
| `end_time` | ISO datetime ou `"0"` para sem fim |
| `campaign_id` | Campanha destino (so para adsets — mover copia para outra campanha) |
| `adset_id` | Adset destino (so para ads — mover copia para outro adset) |

**Exemplo: duplicar 2 adsets para outra campanha, pausados:**
```json
{
  "job_type": "adsets",
  "status_option": "PAUSED",
  "campaign_id": "<CAMPAIGN_DESTINO_ID>",
  "deep_copy": true,
  "items": [
    {"id": "<ADSET_ID_1>"},
    {"id": "<ADSET_ID_2>", "rename_suffix": " - Teste B"}
  ]
}
```

## Limites conhecidos

- Precisa de Python 3 com `requests` e de acesso de rede a `graph.facebook.com`. Sem isso, use o conector oficial do Meta Ads se ele estiver na sessao.
- Para fluxos complexos de Dynamic Creative, usar script dedicado
- Duplicacao de campanha com `deep_copy` tem limite de 3 adsets sincronos (51 assincronos) — campanhas grandes podem precisar de duplicacao em lotes
