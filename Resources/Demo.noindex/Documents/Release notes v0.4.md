# Returns assistant – release notes v0.4

*Sara Navarro · Wednesday, October 14, 2026 · agent version 9, promoted today at 12:30 · sprint 14*

Version 0.4 brings the feature customers asked for the most, courier pickups, and makes the chat faster and sturdier after Tuesday's outage. Everything below is live; the MCP server is the one exception.

## What's new

**Courier pickups in the chat (CX-138).** Customers can book a courier to collect a return, in 2-hour slots from Monday to Saturday, 8:00 to 20:00, until 20:00 the day before. It's free when the item arrived damaged, was the wrong item or isn't as described, and costs 4.95 € when the customer just doesn't need it any more; the assistant says so before it books. Fabrikam Logistics texts the customer 30 minutes before they arrive. New tool: `book_pickup`, with the slot rules in `src/pickup_slots.py`. Until CX-152, Pablo's team in Zaragoza confirms each booking with the courier by hand.

**Faster answers.** 95 % of answers now arrive within 6.2 seconds, down from 9.8. The policy lookups are cached and the replies stream as they're written.

**Rate limits don't break the chat (CX-141).** When the model answers 429, `src/retry.py` waits and tries again: as long as the service asks, or else 1, 2, 4 and 8 seconds with jitter, for at most five attempts and 30 seconds in all. On Tuesday, October 13, customers saw errors for 20 minutes; now a burst like that costs them a slower answer.

**An MCP server for orders (CX-144, PR #58).** `src/orders_server.py` serves the same three tools, `lookup_order`, `create_return` and `book_pickup`, over MCP, so the sales team's agent and editors like VS Code can use them too. **Not deployed yet:** Sara reviews its permissions first (CX-150, before November 2).

## Quality

Version 9 was evaluated on the 120 conversations of the golden set before it was promoted. Eight of them are new and about pickups (CX-139).

| Metric | v9 | v8 | Target |
|---|---|---|---|
| Intent resolution | 4.5 | 4.4 | 4.0 |
| Tool call accuracy | 4.8 | 4.2 | 4.0 |
| Task adherence | 94 % | 93 % | 90 % |
| Groundedness | 4.1 | 3.8 | 4.0 |
| Relevance | 4.4 | 4.5 | 4.0 |

Groundedness is above 4 for the first time, so the pilot can move on to the sales team. Relevance dipped a little: answers about pickups list the slots, which the evaluator reads as less to the point.

## Upgrading

- `uv sync`: there's a new dependency, `mcp` 2.3 or later, for the MCP server.
- `RETURNS_DRY_RUN=1` now fakes pickups as well, so a local run or an evaluation never books a courier.
- No new permissions: `book_pickup` uses the Returns.Write role the app already has.

## Known issues

- **Orders older than 12 months still go to a person.** Javier's OneLake shortcut put the order history in the lakehouse on October 9, but `lookup_order` doesn't read it yet.
- **A pickup can't be changed or cancelled in the chat.** The customer has to ask a person.
- **No 10-second budget across tools.** See the TODO in `src/tools.py`.
- **`lookup_order` trusts the order number.** It must check that the order belongs to the customer before the sales beta (CX-149).

## Rolling back

```sh
uv run python -m src.agent promote 8
```

Version 8 can't book pickups. The retries stay either way, because they're in the app, not in the agent.

*Contoso Outdoor is a fictitious company. The names, numbers and endpoints in these notes are made up.*
