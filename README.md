# agent-tools

Skills, plugins and mods for Claude: reusable tools, workflows and extensions that expand what Claude can do across projects.

This repo works as a Claude Code plugin marketplace.

## Layout

- `.claude-plugin/marketplace.json`: the marketplace catalog. Every plugin, mod or skill bundle must be listed here.
- `plugins/`: plugins and mods, one folder per plugin (see [plugins/README.md](plugins/README.md)).
- `skills/`: standalone skills, one folder per skill (see [skills/README.md](skills/README.md)).

## Contents

| Name | Type | What it does |
| --- | --- | --- |
| `ads-ops` | plugin | Meta Ads and TikTok Ads operations with dry-run and paused creation. |
| [`mise-en-place`](skills/mise-en-place/README.md) | skill | Prepares the workspace so Claude can operate real apps: a verified map of your account (IDs, fields, conventions, payloads, rules). |

## Install

```bash
/plugin marketplace add marcosvb1/agent-tools
/plugin install <plugin>@agent-tools
```

Example: `/plugin install mise-en-place@agent-tools`.

Per project: `claude plugin install <plugin>@agent-tools --scope project`.
