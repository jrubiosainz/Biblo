# GitHub Copilot – features at a glance

*Contoso engineering · Sara Navarro · Tuesday, October 13, 2026 · the one-pager that goes with the rollout plan*

What GitHub Copilot does, where you use it and what our plan includes, on one page, for the 420 engineers who get it between October 19 and December 1. Where it says "we", it's a Contoso decision; everything else comes from GitHub's documentation.

## Where you use it

| Where | What for |
|---|---|
| The GitHub Copilot app | One place for agent work: parallel tasks, several repositories and the whole life of a pull request |
| Your IDE | Inline suggestions, chat about the code in front of you and an agent that edits files for you, in VS Code, Visual Studio, JetBrains IDEs, Eclipse and Xcode |
| GitHub Copilot CLI | Copilot in the terminal, including repeatable command-line workflows |
| github.com | Questions about a repository, an issue or a pull request, or handing work to an agent |
| GitHub Mobile | Chat with Copilot away from your desk |
| GitHub Desktop | Help with commit messages and summaries |
| GitHub Copilot SDK | Our own tools, built on the same building blocks as Copilot |

Where supported, custom instructions, agent skills and MCP servers apply wherever you use Copilot, so you set them up once. Work moves between surfaces too: assign an issue to the cloud agent on github.com, follow it in the app, review the pull request in your IDE and merge it on the web.

## What it does

GitHub groups Copilot's features in four families.

| Family | What's in it |
|---|---|
| Assistive | Suggestions as you type, and answers about your code: explain this, fix that, write a test. You review and apply each suggestion |
| Agentic | You describe a goal and Copilot works through the steps. Agent mode in your IDE. The **Copilot cloud agent**: assign it an issue and it researches the repository, makes the change and prepares a pull request for your review. **Copilot code review** on pull requests, with summaries and suggested improvements |
| Customizations | Instructions, reusable prompts, repository context, external tools, agent skills and custom agents, so Copilot follows our conventions. With **Copilot Memory**, for supported features, Copilot reuses facts about a repository and your preferences in later work |
| External agents and tools | Coding agents, models and MCP servers from other providers. Third-party coding agents get the same security protections and limitations as Copilot's own |

A note on names: the Copilot cloud agent is the one you assign issues to. Our rollout slides call it the coding agent.

## Our plan: Copilot Business

| | Copilot Business | Copilot Enterprise |
|---|---|---|
| Price | $19 per granted seat a month | $39 per granted seat a month |
| GitHub AI Credits | 1,900 a month per user | 3,900 a month per user |

We chose Business: 420 seats, $7,980 a month once everyone has one.

## What our admins control

Organization owners decide who gets Copilot and which features are on, exclude the files Copilot shouldn't see, and review usage data and audit logs. Before wave 1, Marc sets the three guardrails from the rollout plan, which are on the security committee's agenda on Friday, October 16:

- Block suggestions that match public code.
- Keep configuration files with secrets out of Copilot's context.
- A person approves every merge: Copilot can open a pull request and review one, but a person approves it.

## The rollout

| Wave | Who | Engineers |
|---|---|---|
| Mon, Oct 19 | The pilot teams: the returns assistant, the web and data | 60 |
| Mon, Nov 2 | Every product team, each with a 90-minute kickoff | 160 |
| Mon, Nov 16 | Everyone else, contractors with a Contoso account included | 200 |

Everyone has it by December 1, and the developer survey goes out on December 15. Questions: **#copilot-rollout** on Teams, or ask Sara.

*Sources: "About GitHub Copilot", "Where to use GitHub Copilot" and "Plans for GitHub Copilot" on docs.github.com, October 2026. Prices in US dollars, before taxes; they can change. Contoso is a fictitious company used for demos.*
