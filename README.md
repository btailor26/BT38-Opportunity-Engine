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

## LinkedIn partnership posts

Use this structure when drafting a LinkedIn post to find commercial partners. The goal is to start qualified DM conversations.

1. **Name the partner in the first line.** Use “Looking for [specific partner type]” so the intended reader can recognise the opportunity immediately.
2. **Describe the work and its scope.** In one short paragraph, say what the partner would help achieve and where the opportunity applies.
3. **Name the relevant experience.** Give examples of the channels, methods or experience that would help the reader judge their fit. Use actual channels relevant to the deal.
4. **List the work a partner can bring in.** Use short, scannable lines for the service or opportunity areas. Include only work BT38 can actually offer.
5. **State the commercial model.** Say which arrangements BT38 is open to, such as performance-based collaboration or project revenue sharing, when applicable. Keep specific terms for the DM.
6. **Invite a DM or a short introduction in the comments.** Make the DM the preferred next step and leave a public route for introductions and referrals. If a suitable commenter cannot DM, use a connection request and continue privately once accepted. Use topic-specific hashtags if they fit.

In the DM, confirm which opportunity area they can sell, how they find qualified prospects, and whether they provide introductions or manage opportunities through to close. Track qualified inbound DMs and conversations as the primary outcomes. Record impressions, reactions, comments and accepted connections separately when available. Count author replies separately from unique respondents where the data allows.

### Reference post — 17 November 2026

The lead generation and business development partnership post named agencies, freelancers and business development professionals. It asked for qualified B2B opportunities worldwide, named LinkedIn, Upwork, Fiverr and Apollo, then gave a six-line service list. It offered performance-based collaboration and project revenue sharing before inviting DMs or comment introductions.

The supplied capture at 16 hours showed 33,626 post impressions and 90 comments. It also showed public introductions, a colleague tag, discussions about service focus and the sales handoff, and an inbound DM citing IT business development and Upwork bidding experience. The comment total includes replies, and the capture does not establish the total number of accepted connections or explain LinkedIn's distribution. Use the post as a drafting reference and compare future posts by the quality of the inbound conversations they produce.
