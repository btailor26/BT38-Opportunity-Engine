# BT38 Opportunity Engine

Independent commercial opportunity engine for BT38.

This repository is deliberately separate from the BT38 production application. It does not deploy, import, call, or modify `BT38_CLEAN_GOVERNED-Github`.

## Mission

Continuously turn evidence into qualified commercial opportunities:

**DISCOVER → DUPLICATE CHECK → RESEARCH → QUALIFY → CONTACT READY → CONTACTED → FOLLOW-UP → CONVERSATION → PROPOSAL → WON / LOST / REJECTED**

The engine has its own memory. Every prospect is checked against active prospects, historical prospects, and permanent exclusions before it can progress.

## Four hard gates

A prospect cannot become `CONTACT_READY` unless all four pass:

1. **Company fit**
2. **Current trigger / reason now**
3. **Ability to pay**
4. **Decision-maker + usable contact route**

The engine covers the full ecommerce operating chain, not inventory alone: product, sourcing/buying, listings, marketplaces/websites, inventory, warehouse/3PL, orders, payments, fulfilment, shipping/tracking, returns, reconciliation, costs/margins, reporting and operational systems/processes.

## Structure

- `engine/` — qualification, duplicate memory and pipeline logic
- `config/` — qualification rules and discovery policy
- `data/` — persistent prospect/exclusion state
- `inbox/` — new candidate evidence waiting for processing
- `tests/` — contract tests
- `.github/workflows/` — isolated engine runs

The scheduled workflow runs the engine against its inbox and state. It does **not** contact prospects automatically. Human approval remains required before outreach.
