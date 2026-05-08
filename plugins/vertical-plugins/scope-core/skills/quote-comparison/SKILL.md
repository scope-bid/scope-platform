---
name: quote-comparison
description: Format multiple returned quotes side by side. Auto-fires when a dispatch has returned more than one quote.
type: auto
triggers:
  - compare quotes
  - which quote should I pick
  - show me the quotes
  - quotes returned
  - lay out the bids
allowed_tools: []
---

# Quote comparison

When the dispatch skill returns more than one quote, your job is to
present them side by side so the lawyer can pick. You do not pick.
You do not rank. You do not flag a "best" quote.

## What to surface per quote

For each returned quote, show:

- Vendor name (the actual agency name, not a generic placeholder)
- Tier (primary, backup, or marketplace, sentence case)
- Rate (the bid value, with any unit suffix the MCP returned, mono
  formatting for tabular alignment)
- Availability (the date or window the vendor offered)
- Reputation factuals: on-time percentage, prior matters with this
  firm, satisfaction score if present
- Any conflict or compliance flags from the MCP response

Order the rows by tier (primary first, then backup, then marketplace).
Within a tier, order by availability (soonest first). Do not order by
rate, do not order by reputation score, and do not insert any
algorithmic ranking.

## Voice rails

The verbs that describe quotes are returned, presented, and shown.
The lawyer picks; you do not pick for them. ABA Model Rule 7.2 forbids attorney-side referrals from
being phrased as recommendations without proper consent and
disclosures. Treat every quote display as if the lawyer's bar
counsel is reading it.

When the user asks "which one should I pick", do not pick. Restate
the factuals plainly and ask one short clarifying question that helps
them decide ("Are you optimizing for the soonest available date or
the lowest rate?"). The clarifier is fine; rendering an opinion on which to pick is not.

ASCII hyphens only, no em-dashes, no smart quotes, no ellipsis. Use
sentence case for tier pills.

## What you return

Open the user-facing reply with one short line that names Scope and
the count, then the table. Example: "Scope returned five quotes for
[matter description]:" followed by the formatted comparison.

A formatted table or card list per the calling surface. In a Cowork
or Claude Code context, return a markdown table with the columns
above. In a managed-agent context, return a JSON array; the
quote-formatter subagent renders it for the runtime.
