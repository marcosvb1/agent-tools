# mise-en-place evals

Trigger eval: does the skill fire when it should, and stay out of the way when it shouldn't? It measures the `description` in `SKILL.md`, which is the cheapest and most attributable surface to improve.

- 16 `should-trigger` cases (explicit requests, implicit "map the account before we use it", updates, audits; English and Portuguese).
- 16 `should-not-trigger` near misses: one-off questions about a tool, day-to-day operation, writing an MCP server, mapping a codebase, and the cooking meaning of "mise en place".
- Each case has one deterministic grader (`tool_used: Skill` matching `mise-en-place`), so no LLM judge and no judge cost.

The full list is in [CASES.md](CASES.md).

## Run

Needs Claude Code with `claude plugin eval` and an `ANTHROPIC_API_KEY` (or a logged-in account). From the repo root:

```bash
# pilot: one run per case, with a spend ceiling
claude plugin eval ./skills/mise-en-place --ablation none --runs 1 \
  --concurrency 4 --max-cost-usd 2 --no-publish --trust-plugin

# full run: 3 runs per case (the default)
claude plugin eval ./skills/mise-en-place --ablation none \
  --concurrency 4 --no-publish --trust-plugin --json results.json
```

- `--ablation none`: the no-plugin arm can't fire the skill, so it adds cost and no signal here.
- `--model <id>` pins the model; without it the run uses Claude Code's default.
- `--tag should-trigger` or `--tag should-not-trigger` runs one side; `--case 'p0*'` filters by name.
- Results and the HTML report go to `evals/results/<timestamp>/` (git-ignored).

## Reading the result

Report recall (share of `should-trigger` runs that fired) and the false-positive rate (share of `should-not-trigger` runs that fired) separately: a description change can trade one for the other.

With 16 cases per side and 3 runs each, a rate moves by roughly ±12 points from noise alone (`1/sqrt(48)`), so a smaller change between two runs is not a real difference.

## Limits

- The sandbox loads only this skill. In real use other skills compete for the same request, so false positives here are a lower bound and recall an upper bound.
- `max_turns: 3` keeps runs cheap: the grader only needs to see whether the skill was invoked, not the finished map.
