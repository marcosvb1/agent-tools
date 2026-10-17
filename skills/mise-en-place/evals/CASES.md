# Trigger cases

Every case: id, expected behaviour, category and prompt. To add one, create `evals/<id>/prompt.md` and a grader in `evals/<id>/graders/`, following an existing case.

| id | expected | category | prompt |
| --- | --- | --- | --- |
| `p01-explicit-hubspot` | fires | explicit | Do the mise en place for HubSpot before we start automating the sales pipeline. |
| `p02-stripe-before-use` | fires | implicit | We're about to start using Claude to manage our Stripe account. Before anything else, map the account so you stop guessing product and price IDs. |
| `p03-pipedrive-references` | fires | explicit | Build the references for our Pipedrive workspace: pipelines, stage IDs, custom fields, and what you're never allowed to do without asking. |
| `p04-kommo-pt` | fires | explicit | Faz o mise en place do Kommo pra gente: contas, funis, IDs das etapas e as regras de uso. |
| `p05-meta-ads-pt` | fires | implicit | Antes de você começar a subir campanhas no Meta Ads, quero que documente a conta: quais contas de anúncio usamos, o padrão de nomes, os pixels e os erros que já apareceram. |
| `p06-jira-update` | fires | update | Update the Jira map. We added two new projects and changed the workflow statuses last week. |
| `p07-salesforce-audit` | fires | audit | Audit the Salesforce references we wrote back in March, I think half the IDs are stale by now. |
| `p08-airtable-pain` | fires | implicit | Every session you waste ten calls figuring out which Airtable base and table IDs we use. Write it down once, in a file you'll read next time before touching Airtable. |
| `p09-notion-document` | fires | explicit | Document what works in our Notion workspace: which databases matter, their property names and types, and the payloads that worked when creating pages. |
| `p10-shopify-memory` | fires | implicit | Create an operational memory for our Shopify store so future sessions know which store to use, the metafields we rely on, and which actions need my confirmation. |
| `p11-google-ads-agency` | fires | implicit | I'm onboarding a new client's Google Ads account. Prepare the workspace so you can operate it safely later: which accounts, conversion actions, naming conventions and rules. |
| `p12-clickup-update-pt` | fires | update | Atualiza o mapa do ClickUp, criamos um espaço novo e mudaram os campos personalizados. |
| `p13-linear-before-automation` | fires | implicit | Map our Linear workspace before we automate triage: teams, workflow states with their IDs, and the labels we actually use. |
| `p14-n8n-audit-pt` | fires | audit | Revisa as referências do n8n que estão em docs/references/n8n e vê o que mudou na nossa instância desde a última vez. |
| `p15-twilio-rules` | fires | implicit | Set up the rules of use and known pitfalls for our Twilio account so you don't repeat the same mistakes, plus the IDs of the numbers and messaging services we use. |
| `p16-zendesk-casual` | fires | implicit | can you get yourself set up on our zendesk before we start? like learn the account, the groups, the custom fields and the macros we use |
| `n01-oneoff-fields` | does not fire | oneoff-question | Which fields does a HubSpot deal have by default? |
| `n02-oneoff-id` | does not fire | oneoff-question | What's the ID of the 'Qualified' stage in our Pipedrive pipeline? |
| `n03-operate-hubspot` | does not fire | operation | Create a deal in HubSpot for Acme Corp, amount 5000, in the Qualified stage. |
| `n04-operate-meta-pt` | does not fire | operation | Pausa a campanha 'Black Friday' no Meta Ads. |
| `n05-mcp-server` | does not fire | mcp-server | Write an MCP server that exposes our Stripe refunds to Claude. |
| `n06-cooking` | does not fire | word-trap | What does mise en place mean in a professional kitchen, and how do I set one up for a dinner party for eight? |
| `n07-claude-md` | does not fire | codebase | Write a CLAUDE.md for this repo describing the build and test commands. |
| `n08-codebase-map` | does not fire | codebase | Map the architecture of this codebase: modules, dependencies and entry points. |
| `n09-api-docs` | does not fire | oneoff-question | Summarize how pagination works in the Notion API. |
| `n10-debug-error` | does not fire | operation | I'm getting INVALID_ARGUMENT from the Google Ads API when I upload offline conversions. What's usually wrong? |
| `n11-report` | does not fire | operation | Pull last week's spend by campaign from our TikTok Ads account. |
| `n12-rate-limits-pt` | does not fire | oneoff-question | Quais são os limites de rate da API do Kommo? |
| `n13-write-skill` | does not fire | other | Create a skill that sends a weekly Slack digest of open Jira tickets. |
| `n14-study-notes` | does not fire | other | Organize my notes from the HubSpot certification course into a study guide. |
| `n15-tool-choice` | does not fire | other | Should a five-person sales team use Pipedrive or HubSpot? |
| `n16-export` | does not fire | operation | Export all contacts from our Mailchimp audience to a CSV. |
