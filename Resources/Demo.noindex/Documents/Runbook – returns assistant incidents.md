# Runbook – returns assistant incidents

*Owner: Sara Navarro · updated Thursday, October 15, 2026 · for the returns assistant in Contoso Outdoor's support chat*

When the returns assistant misbehaves in production, start here. Each section says how you notice, what to check first and what to do. If you hit something that isn't here, fix it first and write it down after.

## Change log

| When | What |
|---|---|
| Thu Oct 15 | Alerts (CX-147): three alert rules, in `infra/alerts.bicep`, and a section for each |
| Tue Oct 13 | New section, "429 from the model", after that morning's 20 minutes of errors |
| Mon Sep 14 | First version, the day the pilot started |

## Who

| | Who | For |
|---|---|---|
| On call | Sara Navarro | everything, Monday to Friday 8:00–20:00 |
| Backup | Javier Molina | when Sara is out, and anything about Fabric or the lakehouse |
| Security | Marc Puig | keys, sign-in, permissions, and anything that looks like an attack |
| Support floor | Ana Castillo | sending chats to people, and telling the agents on the floor what's going on |
| Pickups | Pablo Serrano's team, Zaragoza | courier pickups that didn't happen |

## The first five minutes

1. Open Application Insights, `appi-<suffix>` in `rg-contoso-support-prod`: *Failures* and *Performance*, last 30 minutes.
2. Post in Teams, in **#returns-assistant-incidents**: what you see, since when, and that you're on it. Ana tells the floor.
3. Try it yourself, with the demo order: "My Trailhead 2 arrived with a broken pole. Order 48213."
4. If customers aren't getting answers, send every chat to a person first (below) and investigate after.

## Alerts

All three email returns-assistant-oncall@contoso.com, which also posts in #returns-assistant-incidents. Sara set each one off on purpose on October 15 to check they arrive.

| Alert | Fires when | Severity | Go to |
|---|---|---|---|
| Slow answers | the p95 of `POST /api/messages` is above 8 seconds over 15 minutes | 2 | Slow answers |
| Errors | more than 10 `POST /api/messages` fail in 5 minutes | 1 | Errors |
| 429 from the model | the model answers 429 more than 20 times in 5 minutes | 3 | 429 from the model |

## 429 from the model

*Added on Tuesday, October 13.*

**What you see.** Answers take 20 or 30 seconds, or the chat says "Something went wrong on our side". The *429 from the model* alert fires. In the logs, the calls to the model deployment answer `429 Too Many Requests`.

**Why.** The deployment, gpt-5-mini, has a quota of tokens per minute: `modelCapacity` in `infra/resources.bicep`, in thousands. When the chat needs more in a minute than the quota allows, the model answers 429 until the minute is over.

**What happened on October 13.** From 11:00, for about 20 minutes, most chat turns failed: two drops, while a busy Tuesday morning ran into a quota sized for the first weeks of the pilot. Customers told us before anything else did, because there were no alerts yet. Since the hotfix that morning, `src/retry.py` waits and tries again: as long as the service asks in `retry-after`, or else 1, 2, 4 and 8 seconds with jitter, for at most five attempts and 30 seconds in all. A short burst now costs a slower answer instead of an error.

**What to do.**

1. Check it's the quota and not something else:

   ```kusto
   AppDependencies
   | where TimeGenerated > ago(1h)
   | where ResultCode == "429"
   | summarize throttled = count() by bin(TimeGenerated, 5m)
   | render timechart
   ```

2. If it's steady rather than a burst, raise the quota: Foundry portal › the deployment › *Edit* › *Tokens per minute*. Then put the same number in `modelCapacity`, so the next `azd provision` doesn't put it back.
3. If the subscription has no quota left, tell Javier: he's asking for more before the sales team joins (CX-153).
4. **Never turn the retries off** to make errors show up faster. They're what keeps a burst from reaching customers.

## Slow answers

**What you see.** The *Slow answers* alert. Since version 9 the p95 is about 6.2 seconds, so above 8 means something changed.

```kusto
AppRequests
| where TimeGenerated > ago(3h)
| where Name == "POST /api/messages"
| summarize p50 = percentile(DurationMs, 50), p95 = percentile(DurationMs, 95) by bin(TimeGenerated, 5m)
| render timechart
```

**Usual suspects, in order.** Retries (look for 429s, above). A slow lakehouse: `lookup_order` has no query timeout yet, see the TODO in `src/tools.py`; ask Javier whether Fabric's capacity is throttled. A slow returns API: ask in #returns-api.

## Errors

**What you see.** The *Errors* alert, or customers getting "Something went wrong on our side". Look at *Failures* › the top response codes and dependencies:

- **401 or 403** from Foundry, the lakehouse or the returns API: the managed identity lost a role, or someone changed one. Call Marc.
- **500s from the returns API**: not ours. Post in #returns-api, and send chats to people if returns can't be opened.
- **Errors right after a deploy**: Container App › *Revisions*, send all traffic back to the previous revision, then look.

## The assistant quotes an old policy

Somebody uploaded new policy PDFs but the promoted version still uses the old vector store, or the old PDF was left in. Upload all the current PDFs, publish, evaluate and promote (README, "Updating the policies"). It happened in week 2 of the pilot, with the 2025 return policy.

## Roll back a version

```sh
uv run python -m src.agent promote 8
```

Version 8 can't book courier pickups, so only do it if version 9 itself is the problem. The retries stay either way: they're in the app, not in the agent version. Promoting takes effect on the next message; conversations carry on.

## Send every chat to a person

In the support desk: *Settings › Chat › Route all chats to agents*. Ask Ana first: the floor needs to know before every chat lands on them. Undo it when the assistant is back.

## A key or a secret in a log

Don't delete the log first. Tell Marc, then rotate the key: the old one stops working at once. Production has no keys to leak: the app signs in with its managed identity and the Foundry resource doesn't accept keys. Staging still uses an API key, the one rotated on October 15, until CX-148 moves it to managed identity too (ADR 0007, by October 30).

## A courier pickup didn't happen

The courier comes back the next working day in the same slot, and the customer gets a text. If the customer says nobody came at all, give Pablo's team the order and the RMA in #returns-ops. Until CX-152 connects the returns API to Fabrikam Logistics, his team confirms each booking by hand.

## After an incident

Within two working days: a short note in the incident's thread (what happened, when, what fixed it, what we change) and a card on the board for each change. Then update this runbook.

*Contoso Outdoor is a fictitious company. The names, numbers and endpoints in this runbook are made up.*
