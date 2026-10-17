# Contoso Outdoor support agent

The returns assistant in Contoso Outdoor's support chat. It looks up orders, opens returns and answers policy
questions, citing the page it read. It runs on Microsoft Foundry Agent Service; this repo holds its prompt, its
tools, its evaluations and the chat around it.

> Contoso Outdoor is a fictitious company. The names, orders and endpoints in this repo are made up.

## How it fits together

```
browser -> web/ (React) -> src/app.py (FastAPI on Azure Container Apps, managed identity id-web-...)
                                |
                                |  one conversation per visitor; answers stream back as server-sent events
                                v
                 Foundry Agent Service: returns-assistant (gpt-5-mini)
                   |-- File Search -> the policy PDFs, one file per page, in a vector store
                   '-- function calls, run back in src/tools.py:
                         lookup_order  -> lakehouse contoso_sales in Microsoft Fabric (read-only)
                         create_return -> returns API (opens returns; can't refund)
                         book_pickup   -> returns API -> Fabrikam Logistics, the courier

"Talk to a person" -> support desk API, with the whole conversation

src/orders_server.py: the same three functions over MCP, for the sales team's agent (not deployed until CX-150)
```

| Where | What |
|---|---|
| `prompts/returns-assistant.md` | what the agent does, and what it never does |
| `src/tools.py` | `lookup_order`, `create_return`, `book_pickup` and File Search |
| `src/pickup_slots.py` | when the courier can come, and what it costs the customer |
| `src/retry.py` | waits and tries again when the model answers 429 |
| `src/agent.py` | publishing, promoting, the policy PDFs and a chat turn |
| `src/evaluate.py` | the golden set, scored before a version is promoted (`evals/README.md`) |
| `src/orders_server.py` | the order tools over MCP |
| `src/app.py` | the chat's API |
| `web/` | the chat |
| `infra/` | everything `azd up` creates, in Bicep, alerts included |
| `docs/adr/` | decisions, from number 7 on (1 to 6 are on the team wiki) |

## Run it locally

You need Python 3.12, [uv](https://docs.astral.sh/uv/), Node 22, the
[Azure Developer CLI](https://aka.ms/azd) and Microsoft ODBC Driver 18 for SQL Server (on a Mac:
`brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release`, then
`HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18`). Your account needs **Foundry User** on `proj-support` (ask Marc)
and read access to the Contoso Sales workspace in Fabric (ask Javier).

```sh
azd auth login
set -a; eval "$(azd env get-values)"; set +a   # the dev environment's endpoints
export RETURNS_DRY_RUN=1                       # no real returns, no couriers
uv sync
uv run uvicorn src.app:app --reload --port 8000
```

The chat, in a second terminal:

```sh
cd web
npm install
npm run dev                                    # http://localhost:5173, which passes /api on to :8000
```

`uv run python -m src.agent chat` talks to the agent in the terminal instead, and `uv run pytest` runs the tests.
`uv run python -m src.orders_server` serves the order tools over MCP at `http://127.0.0.1:8001/mcp`, for VS Code or
any other MCP client.

## Releasing a change

Every change to the prompt or the tools is a new version of the agent, and customers see a version only once it's
promoted:

```sh
uv run python -m src.agent publish           # Published returns-assistant version 9
uv run python -m src.evaluate --version 9    # the golden set, scored; fails if a target is missed
uv run python -m src.agent promote 9
```

To roll back, promote the version before: `uv run python -m src.agent promote 8`.

The golden set has 120 conversations in English and Spanish: 112 taken from real chats and 8 about courier pickups
that Ana wrote (CX-139). Because of the real ones it lives in SharePoint (Customer Care › Agent pilot), not here.
Download it to `evals/golden.jsonl`, which git ignores. `evals/README.md` has the format, the targets and the scores.

## Updating the policies

The policy PDFs live in SharePoint (Customer Care › Policies). When one changes, upload all the current ones:

```sh
uv run python -m src.agent policies ~/Downloads/policies/*.pdf   # 9 pages in vs_...
azd env set POLICY_VECTOR_STORE_ID vs_...
set -a; eval "$(azd env get-values)"; set +a
```

Then publish, evaluate and promote. Each upload makes a new vector store and the old one stays with the old
versions. In week 2 of the pilot the agent cited the 2025 return policy in three conversations, because the old PDF
was still in its index.

## Deploying

```sh
azd env new dev
azd env set FABRIC_SQL_ENDPOINT <id>.datawarehouse.fabric.microsoft.com
azd env set RETURNS_API https://returns.contoso.internal
azd env set SUPPORT_DESK_API https://desk.contoso.internal/api
azd up       # the first time: Foundry, the model, the registry and the container app
azd deploy   # after that, for code changes
```

`azd up` doesn't do everything yet. Once per environment, by hand:

1. **Fabric:** add the managed identity `id-web-<suffix>` to the Contoso Sales workspace as a Viewer (Javier).
2. **Returns and support desk:** give `id-web-<suffix>` the Returns.Write and Tickets.Create app roles (Marc).
3. **Sign-in:** Container App › Authentication › Microsoft, limited to the *Support agent pilot* group, the 50
   people in the pilot.
4. **Guardrails:** in the Foundry portal, assign the *support-default* guardrail to returns-assistant for user
   prompts, outputs, tool calls and tool responses. Keep it on tool calls (decided on October 6).

`azd up` also creates the three alerts in `infra/alerts.bicep`, which email returns-assistant-oncall@contoso.com.
The runbook says what to do when one fires.

Keys are off on the Foundry resource (`disableLocalAuth`), so everything signs in with Microsoft Entra ID. Staging
still has an API key until CX-148 builds it with `azd up` too (ADR 0007, by October 30).

## Settings

| Variable | What it is | Set by |
|---|---|---|
| `FOUNDRY_PROJECT_ENDPOINT` | the proj-support project | `azd provision` |
| `FOUNDRY_MODEL_NAME` | the model deployment, gpt-5-mini | `azd provision` |
| `POLICY_VECTOR_STORE_ID` | the policy PDFs, for `publish` | you, after `src.agent policies` |
| `FABRIC_SQL_ENDPOINT` | the lakehouse's SQL analytics endpoint | you, `azd env set` |
| `RETURNS_API` | the returns API | you, `azd env set` |
| `SUPPORT_DESK_API` | the support desk API, for handovers | you, `azd env set` |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | where traces go | `azd provision` |
| `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING` | `true` traces the agent's steps; never what anybody wrote | the container app |
| `AZURE_CLIENT_ID` | the managed identity the app runs as | the container app |
| `RETURNS_DRY_RUN` | `1` opens no real returns and books no couriers | you, locally; `src.evaluate` sets it |

## Known issues

- **Orders older than 12 months aren't found.** Since October 9, Javier's OneLake shortcut brings the order history
  into the lakehouse, but `lookup_order` doesn't read it yet, so the agent still hands those orders over.
- **No time limit across tools.** The checklist asks for 10 seconds; see the TODO in `src/tools.py`.
- **`lookup_order` trusts the order number.** Fine behind the pilot's sign-in, but it must check that the order
  belongs to the customer before the sales team joins on November 2 (CX-149).
- **A pickup can't be changed or cancelled in the chat.** The customer has to ask a person.
- **Pickups are confirmed by hand.** Until CX-152 connects the returns API to Fabrikam Logistics, Pablo's team in
  Zaragoza confirms each booking with the courier.
- **The MCP server isn't deployed.** Sara reviews its permissions first (CX-150).
- **Sign-in isn't in Bicep**, so a new environment is open to anyone until step 3 above.
- **No thumbs up or down** in the chat yet, so there's nothing to review on Fridays (checklist §7).
- `src.evaluate` doesn't compare a version with the promoted one yet (checklist §3). PR #59 does it in CI, and fails
  the build if a metric drops more than 5 % (CX-145, in review).

## People

| | |
|---|---|
| Owner | Lucía (product) |
| On call | Sara (development) |
| Data and Fabric | Javier |
| Support | Ana |
| Courier pickups | Pablo (operations, Zaragoza) |
| Security, and access to proj-support | Marc |
