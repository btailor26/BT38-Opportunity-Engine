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

## LinkedIn post structure

Use these six steps in this order for every BT38 LinkedIn post, including partnership calls, service offers, case studies, lessons and updates. Adapt what each step says to the topic.

1. **Open with a direct hook.** Name the intended audience, the problem they recognise, or the result they care about in the first line.
2. **Explain the opportunity or situation.** In one short paragraph, say what is happening and why it matters to that audience.
3. **Make it concrete.** Name the relevant channels, methods, experience or evidence so readers can recognise how it applies to them.
4. **List the practical points.** Use short, scannable lines for services, actions, findings or results, depending on the subject.
5. **State the value or takeaway.** For partnership posts, explain the commercial model. For other posts, state what the reader gains, learns or can do with the information.
6. **Give one clear next step.** For commercial posts, make DM the preferred route and offer a short public introduction as a fallback. For other posts, invite a response that fits the topic. If a suitable commenter cannot DM, use a connection request and continue privately once accepted.

Relevant hashtags are optional and go after the call to action. The reference post used nine hashtags, and the available snapshot cannot attribute impressions or enquiries to them. To assess whether hashtags help, record the tags used and compare similar posts over time while keeping the structure consistent.

For partnership enquiries, confirm in the DM which opportunity area the person can sell, how they find qualified prospects, and whether they provide introductions or manage opportunities through to close. Track qualified inbound DMs and conversations as the primary outcomes for commercial posts. Record impressions, reactions, comments and accepted connections separately when available. Count author replies separately from unique respondents where the data allows.

### Reference post — 17 November 2026

The lead generation and business development partnership post named agencies, freelancers and business development professionals. It asked for qualified B2B opportunities worldwide, named LinkedIn, Upwork, Fiverr and Apollo, then gave a six-line service list. It offered performance-based collaboration and project revenue sharing before inviting DMs or comment introductions.

The supplied capture at 16 hours showed 33,626 post impressions and 90 comments. It also showed public introductions, a colleague tag, discussions about service focus and the sales handoff, and an inbound DM citing IT business development and Upwork bidding experience. The comment total includes replies, and the capture does not establish the total number of accepted connections or explain LinkedIn's distribution. Use the post as a drafting reference and compare future posts by the quality of the inbound conversations they produce.
