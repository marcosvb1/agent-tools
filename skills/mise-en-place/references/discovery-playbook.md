# Discovery playbook

How to discover accounts, schema and payloads for each access route, and where common tools expose their metadata. The endpoints below are known starting points; confirm them in the current documentation (Context7 or official docs) before recording them as fact, because API versions change.

## By access route

### MCP connector

1. `ToolSearch` with the tool's name to load its tools (where there is no `ToolSearch`, look at the session's tool list). Read each tool's description: it usually lists the objects it covers.
2. Look for metadata tools before data tools: names with `schema`, `properties`, `fields`, `describe`, `get_*_types`, `list_*`, `discover`, `tool_guidance`.
3. Record in the map's `README.md` the exact name of the tool used for each operation (e.g. "create ad → `ads_create_ad`"). Tool names differ between connectors for the same product; note which connector.
4. Note what the connector does **not** cover and would need the API directly.

### CLI

1. `<cli> --help` and `<cli> <resource> --help` to list resources and flags.
2. Prefer structured output (`--json`, `-o json`, `--format json`) and record the flag.
3. Record how the CLI picks the account or project (`--project`, profile, environment variable) and how to see the current context (`gcloud config list`, `gh auth status`).

### HTTP API

1. Find the base URL and version. Record the version used.
2. Record authentication by variable name only: `Authorization: Bearer $TOOL_TOKEN`.
3. Look, in this order, for: an OpenAPI spec or GraphQL introspection, a metadata/fields endpoint, a "me"/"account" endpoint to discover accounts, and only then record listings with a small `limit`.
4. Record pagination (cursor, offset, `next`), rate limits (`X-RateLimit-*`, `Retry-After` headers) and the error format.

### Database

1. List schemas and tables (`information_schema`, `\d` in psql).
2. For the tables in scope: columns, types, nullability, keys, indexes and foreign keys.
3. Record enums and lookup tables (statuses, types) with their values.
4. Use `LIMIT` on every sample and never copy rows with personal data.

### Documentation only

Use Context7 (`resolve-library-id` and `query-docs`) or the official documentation. Mark everything as `docs` and list at the end of the map's `README.md` what must be verified once there is access.

## Where common tools keep their metadata

| Tool | Accounts | Schema / metadata | Notes |
| --- | --- | --- | --- |
| Meta Ads (Graph API) | `GET /me/adaccounts`, `GET /me/accounts` (pages) | `GET /<id>?metadata=1`; fields per object in the Marketing API reference | Account IDs carry the `act_` prefix. Budgets in the account currency's minor unit (cents). Creatives can't change after creation. |
| TikTok Ads (Business API) | `GET /oauth2/advertiser/get/` | Field reference per endpoint (`/campaign/get/`, `/adgroup/get/`, `/ad/get/`) | `advertiser_id` required on almost every call. Time zone and currency belong to the account. |
| Google Ads | MCC and child accounts (`customers:listAccessibleCustomers`) | GAQL `SELECT ... FROM` with `GoogleAdsFieldService` | `login-customer-id` sets the MCC; IDs without dashes; money in micros. |
| HubSpot | `GET /account-info/v3/details` | `GET /crm/v3/properties/{objectType}`, `GET /crm/v3/schemas`, pipelines at `GET /crm/v3/pipelines/{objectType}` | A property has a `name` (API) and a `label`. Pipeline stages have their own IDs. |
| Salesforce | org from the session (`sf org display`) | `GET /services/data/vXX.X/sobjects/{Object}/describe` | Picklist values and record types per object; custom field API names end in `__c`. |
| Kommo / amoCRM | account subdomain; `GET /api/v4/account` | `GET /api/v4/leads/pipelines` (pipelines and statuses), `GET /api/v4/{entity}/custom_fields` | Pipeline statuses have numeric IDs; custom fields have a `field_id` and an `enum_id` per option. |
| ClickUp | `GET /team` (workspaces) | `GET /space/{id}`, `GET /list/{id}/field` (custom fields), statuses per list or space | Statuses and fields can vary per list. |
| Notion | `GET /users/me`, `POST /search` | `GET /data_sources/{id}` on recent API versions (`GET /databases/{id}` on older ones): properties and select options | Select option and property IDs are stable; names are not. |
| Airtable | `GET /v0/meta/bases` | `GET /v0/meta/bases/{baseId}/tables` (fields and choices) | Field IDs (`fld…`) survive renames; names don't. |
| Shopify (Admin GraphQL) | the token's shop | GraphQL introspection; metafield definitions | IDs are GIDs (`gid://shopify/Product/...`). |
| Stripe | the token's account; `GET /v1/account` | API reference; `expand[]` for relations | Amounts in minor units; test and live modes have different IDs. |
| WhatsApp Cloud API | `GET /{business_id}/owned_whatsapp_business_accounts` | templates at `GET /{waba_id}/message_templates` | Messages outside the 24-hour window need an approved template. |
| Slack | `auth.test` | `conversations.list`, `users.list` | API calls use channel and user IDs, not names. |
| n8n | instance and project | `GET /api/v1/workflows`; credentials by the name and type seen in workflow nodes (the public API lists little about credentials) | Record workflow and credential IDs, never credential contents. |
| Postgres / Supabase | project or database | `information_schema`, `pg_enum` | RLS changes what each key can see; record which role was used. |

## Safe sampling

- `limit` of 1 to 3. To understand an enum, use the metadata endpoint, not hundreds of records.
- Before pasting a response into the map, delete or replace with placeholders: names, emails, phones, ID documents, addresses, URLs with tokens, message contents.
- Trim long responses: keep the structure (keys and types) and one example of each list.
