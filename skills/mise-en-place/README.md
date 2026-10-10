# mise-en-place

**Claude learns your account in a tool once (IDs, fields, conventions, gotchas) and stops guessing.**

*Mise en place* is the kitchen habit of having everything in its place before cooking. This skill does that for the tools Claude operates: before working in your CRM, ads account, billing or project tracker, it builds a short, verified map of *your* account and reads it every time after.

## Before and after

**Before.** "Move this deal to Qualified." Claude lists pipelines, guesses which one you mean, searches for a stage called "Qualified", picks the wrong one in the second pipeline, and sends a field name the API silently ignores. Next session, it starts from zero again.

**After.** Claude reads `references/hubspot/README.md`, sees that the default pipeline is `Sales`, that "Qualified" is stage `<STAGE_ID>`, that the team names deals `Company / Product / Quarter`, and that moving a deal to Closed Won needs your confirmation because it triggers invoicing. It makes one correct call.

## What it records

The things no connector or doc page knows about your account:

- which accounts, workspaces or projects actually matter, and which is the default;
- the IDs in use: pipelines, stages, lists, custom fields and their options;
- house conventions: naming patterns, numbering, default owners and tags;
- payloads that worked and errors already seen, with the fix;
- rules: what spends money, what can't be undone, what needs a yes first.

Generic API facts are left to the connector and the docs, unless they are a pitfall.

## What a map looks like

```
references/<tool>/
  README.md           # frontmatter (tool, route, default_account, validated_at), access, accounts, objects, operations
  rules.md            # steering for future sessions
  objects/<object>.md # fields, enum options and IDs
  payloads/<op>.md    # request and response that worked, errors seen
  data.example.json   # shape of the IDs, safe to commit
  data.local.json     # your real IDs, kept out of git
```

Every fact is tagged `verified:YYYY-MM-DD`, `docs` or `inferred`, so Claude knows how far to trust it. If your references folder already has its own convention, the skill follows it.

## Use it

```
/plugin marketplace add marcosvb1/agent-tools
/plugin install mise-en-place@agent-tools
```

Then ask: "do the mise en place for Stripe", "map our Notion workspace before we use it", "update the Jira map".

- **Quick mode (default):** accounts, the default one, the 2 or 3 objects your goal needs, conventions, rules and known errors. Minutes, not hours.
- **Full mode:** ask for a "full map" to cover every object and operation in scope.

Works in Claude Code, Cowork and claude.ai (where the map comes back as a single file to add to your Project). Mapping is read-only. Writes are only recorded from a dry-run, from something you already asked Claude to do, or from a reversible test you approve.

## Privacy and safety

- Credentials never go into a map, not even into the local files; it records environment variable names only.
- Personal data (names, emails, phones, addresses, ID numbers, message contents) never goes into a map. Maps hold IDs, structure and rules, not records. The skill prefers schemas to real records and never reads records in tools holding health or other special-category data. Optionally, it tags each field as personal data, so the map doubles as a data inventory for GDPR/LGPD records.
- Before a test write it checks what the write could trigger (automations, webhooks, conversion events) and uses fake `example.com` data.
- Real IDs go to `data.local.json`, outside git, whenever the map might be shared. If the skill can't confirm a repo is private, it treats it as public.
- `scripts/check_secrets.py` scans every map before it's handed over: tokens and keys, emails, phone numbers from many countries, payment cards, IBANs and national IDs; `--public` also flags real IDs, and it runs `gitleaks` or `trufflehog` too when installed. It is a safety net, not a guarantee: it can't recognize people's or companies' names, so review samples yourself.

## Roadmap

- A hook that injects a tool's map when Claude starts using that tool, and warns when `validated_at` is older than N days.
- Example maps for common tools (schema and pitfalls only, no IDs).
