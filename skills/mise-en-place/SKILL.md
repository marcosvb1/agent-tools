---
name: mise-en-place
description: This skill should be used when the user wants to build, update or audit the reference map of a tool, API, connector or SaaS account — its access route, accounts, objects, properties, IDs, payloads and rules of use — saved as files Claude reads before operating it, e.g. "do the mise en place for HubSpot", "map this API before we use it", "build the references for this tool", "document the payloads that work in Stripe", "update the ClickUp map", "audit the Meta Ads references", "faz o mise en place do Kommo", "atualiza o mapa do ClickUp". Not for one-off questions about a tool ("which fields does X have", "what is the ID of pipeline Y": answer directly), not for the day-to-day operation itself (use the tool's own skill) and not for writing an MCP server.
---

# Mise en place

Everything in its place before cooking: for each tool Claude works with, a short, verified map of **how to access it**, **which accounts exist**, **which objects and properties matter**, **which payloads work** and **which rules to follow**. Future sessions (and the tool's own operational skill) read the map before acting, instead of rediscovering everything or guessing IDs and field names.

A map is worth what was **verified**. Every fact records where it came from and when: `verified YYYY-MM-DD`, `docs` or `inferred`.

Write the map in the user's language. Keep API names, field names and IDs exactly as the tool returns them.

## Output

One folder per tool, inside the user's references folder:

```
<destination>/<tool>/
  README.md           # the map: frontmatter, "Use when", access, accounts, objects, operations
  rules.md            # steering: rules, limits, pitfalls, what needs confirmation
  objects/<object>.md # properties, types, enums, IDs, relations
  payloads/<op>.md    # verified request and response for each common operation
  data.example.json   # shape of the IDs and config, with placeholders and _validated_at
  data.local.json     # the real IDs in that shape; kept out of git
```

- `README.md` starts with a fixed frontmatter (`tool`, `route`, `default_account`, `validated_at` in ISO format), so a hook or another skill can read the default account and the map's age.
- A small tool fits entirely in `README.md`, with the rules in a `## Rules` section. Topics that grow become loose files such as `gotcha-<topic>.md`. Don't create empty files.
- If the destination already holds folders for other tools, **follow the convention found there**: the new map should look like a sibling of the existing ones.

Templates live in `templates/`. Details for steps 3 to 7 are in `references/step-details.md`.

## Workflow

### 1. Scope

Find out what you can on your own and ask at most two things, in a single message:

- **Tool and goal** (what the map is for: "launch ads", "move leads through the pipeline"). Usually already in the request; the goal decides what gets detailed and what is only listed.
- **Destination**. Search before asking, in this order: an existing map for the tool (this becomes an update, see below), the `references/` folder of the tool's skill, the references folder of the user's vault or project (`docs/references/`, `references/`, `refs/`), and finally `./.claude/mise-en-place/<tool>/`. Ask only if there is more than one candidate.
- **Visibility**. If the destination is in a git repo, check the remote (`git remote -v`; `gh repo view --json visibility` when `gh` is available). If you can't confirm it, treat it as **public** and say so; the user can tell you it's private.

Don't ask about accounts here: step 3 lists the ones the access route can see.

### 2. Access route

Find out how the session talks to the tool, in this order, and record the chosen route in `README.md`:

1. **MCP connector** in the session (search with `ToolSearch` for the tool's name, or check the session's tool list where `ToolSearch` doesn't exist). Preferred: no token needed.
2. **CLI** installed and logged in (`gh`, `gcloud`, `stripe`, `supabase`…).
3. **HTTP API** with a credential in an environment variable. Record only the variable's **name**.
4. **Documentation** (Context7, official docs) when there is no access: everything is marked `docs`.

With no route at all, say which connector or variable is missing and offer to continue from the documentation only. Tactics per route and schema endpoints of common tools: `references/discovery-playbook.md`.

### 3. Accounts

List the visible accounts, workspaces or projects with read calls, and confirm with the user which ones are actually used and which is the default.

### 4. Objects and properties

Schema from the metadata endpoint, not from samples; properties with API name, type and enum IDs; relations between objects. Details in `references/step-details.md`.

### 5. Payloads

Request and response that worked for each common operation, plus the errors seen and how they were fixed. Reads run for real; writes only through a dry-run, a write the user already asked for, or a reversible test write they approve. Nothing that spends money, messages third parties or deletes real data.

### 6. Redaction and secrets

No credentials in the `.md` files or in `data.example.json`; personal data becomes placeholders; in a public repo the real IDs go only into `data.local.json`. Before handing over, run:

```bash
python3 <skill-folder>/scripts/check_secrets.py [--public] <destination>/<tool>
```

Use `--public` when the destination is a public repo. Fix whatever it flags or explain the false positive to the user. Options, and what to do without Python: `references/step-details.md`.

### 7. Steering (`rules.md`)

The rules a future session must follow to avoid mistakes, one per line, with the reason when it isn't obvious. Checklist: `references/steering-checklist.md`.

### 8. Wire the map into the work

A map only helps if it gets read. Offer, as fits: a line in the tool skill's `SKILL.md` ("before operating, read `<destination>/<tool>/README.md`"); a line in the references folder's index, in the registry of connected tools (e.g. `connections.md`) or in `CLAUDE.md`; or, if the tool is used often and has no skill, creating one with `skill-creator`.

Close with a short summary: route, accounts, objects and operations covered, what stayed as `docs`, and what the secrets check found.

## Updating or auditing a map

1. Read the map's `README.md`: `validated_at` in the frontmatter and the `Source` column of each row.
2. Repeat steps 3 to 5 with reads only and compare: new or removed accounts, changed properties and enums, IDs that no longer exist, `docs` rows that can now be verified.
3. Show the differences before rewriting.
4. Update `rules.md` with what changed and run the secrets check again.
5. Update `validated_at` (in `README.md` and in `data.example.json`) and log the change in the "History" section.

## Principles

- **Short and navigable.** The map's `README.md` is read in full every session: keep it under ~200 lines and push detail into `objects/` and `payloads/`.
- **Verified beats complete.** Ten confirmed properties are worth more than two hundred copied from the docs.
- **IDs in tables.** "ID of the Qualified stage" must be findable at a glance.
- **Read-only by default.** Mapping is not operating.
