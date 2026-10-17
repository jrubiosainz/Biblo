# Evaluations

Every version of the returns assistant is scored here before customers see it. `src/evaluate.py` runs each conversation of the golden set against the new version, tools and all, and then Foundry's built-in evaluators grade the answers. If any metric misses its target, it exits with 1 and the version isn't promoted.

```sh
uv run python -m src.evaluate --version 9
```

It sets `RETURNS_DRY_RUN=1` first, so no real return is opened and no courier is booked.

## The golden set

120 conversations, in English and Spanish:

- **112 from real chats** in the pilot's first four weeks, picked by Ana to cover what customers really ask: where's my order, returns and replacements, policy questions, and the awkward ones, like old orders or people trying to talk the assistant into a refund.
- **8 about courier pickups** (CX-139), new in version 9. Customers couldn't book pickups before, so Ana wrote them from what they asked the support desk.

Real chats have names and addresses in them, so the set lives in SharePoint (Customer Care › Agent pilot › `golden.jsonl`), not here. Download it to `evals/golden.jsonl`, which git ignores. `sample.jsonl` has the same format, with seven made-up conversations:

| Field | What |
|---|---|
| `id` | a short name, in the conversation's language |
| `language` | `en` or `es` |
| `query` | what the customer writes |
| `expected` | what a good answer does: the tools, in order, and what it must say. The evaluators read it, and so do people |

To add a conversation, add it to the SharePoint file and tell Ana: she checks its `expected` before it counts.

## Targets

From the agent evaluation checklist. Scores go from 1 to 5; task adherence is the share of answers that pass.

| Metric | What it checks | Target | v9 | v8 |
|---|---|---|---|---|
| Intent resolution | it understood what the customer wanted | 4.0 | 4.5 | 4.4 |
| Tool call accuracy | the right tools, with the right arguments, in the right order | 4.0 | 4.8 | 4.2 |
| Task adherence | it followed its instructions and did nothing it never does | 90 % | 94 % | 93 % |
| Groundedness | policy answers say only what the documents say | 4.0 | 4.1 | 3.8 |
| Relevance | it answered the question asked, and not another one | 4.0 | 4.4 | 4.5 |

Version 9 was scored on Tuesday, October 13, and promoted on the 14th. Groundedness passed 4 for the first time, so the sales team can join the pilot on November 2.

## Coming next

- **Evals in CI (CX-145, PR #59, in review).** Every pull request that touches the prompt or the tools publishes a version, scores it and fails the build if any metric drops more than 5 % against the promoted version.
- **Side by side.** `src.evaluate` prints only the new version's scores; it should show the promoted version's next to them (checklist §3).
