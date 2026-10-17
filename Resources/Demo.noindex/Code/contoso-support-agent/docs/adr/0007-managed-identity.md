# 7. Managed identity everywhere, and no API keys

*Accepted on Friday, October 16, 2026, by the security committee · proposed by Marc Puig on Tuesday, October 13 · CX-148*

Decisions 1 to 6 are on the team wiki, from before this repo existed. From this one on, they live here, next to the code.

## Context

Production has signed in with Microsoft Entra ID from day one: the app runs as the managed identity `id-web-<suffix>`, and the Foundry resource refuses keys (`disableLocalAuth`). Staging doesn't. It was set up by hand before the Bicep existed, and the nightly evaluation run calls it with an API key kept in a pipeline variable.

On Monday, October 12, a holiday, the nightly run printed that key in its debug log, and Marc found it on Tuesday morning. Only the team can read the pipeline's logs and the key only reaches staging, so he rotated it on Thursday the 15th, after the v0.4 release, instead of breaking staging in the middle of it. Nothing suggests anyone used it.

Rotating fixes this leak, not the next one. As long as there's a key, it can end up in a log, an `.env` file or a screenshot.

## Decision

- Staging is created by `azd up` from the same Bicep as production, with its own managed identity and `disableLocalAuth: true` on its Foundry resource.
- The nightly run and CI sign in with OpenID Connect, through a federated credential: there's no secret in the pipeline.
- No environment has API keys. No key goes in `.env`, pipeline variables or app settings, and local runs use `azd auth login`.
- Each identity gets only the roles it needs, as in production: Foundry Agent Consumer on the project, Viewer on the Fabric workspace, and Returns.Write and Tickets.Create on the APIs.

## Consequences

- Nothing left to leak or rotate: tokens last about an hour and are never written down.
- A new environment needs the same manual steps as production until they're in Bicep (README, *Deploying*).
- To try things in staging, people need **Foundry User** on its project, as in production. Ask Marc.
- Scripts that called staging with `curl` and the key need `az account get-access-token` instead.

## Plan

| What | Who | When |
|---|---|---|
| Rotate the staging key | Marc | Thursday, October 15 · done |
| Staging from `azd up`, without keys | Marc | by October 23 |
| OpenID Connect for the nightly run and CI | Sara | by October 27 |
| Delete the old staging resources | Marc | by October 30 |
