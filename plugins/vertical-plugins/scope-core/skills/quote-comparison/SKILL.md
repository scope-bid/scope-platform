---
name: quote-comparison
description: Format multiple returned quotes side by side. Fires only when a dispatch has returned two or more quotes AND no award has been made. Do NOT fire when only one quote returned, when the matter is already awarded, or when the user is reviewing a historical comparison from a closed matter.
type: auto
triggers:
  - compare quotes
  - which quote should I pick
  - show me the quotes
  - quotes returned
  - lay out the bids
allowed_tools:
  - scope-legal__scope_award_matter
  - scope-aec__scope_award_subcontractor
---

# Quote comparison

When the dispatch skill returns more than one quote, your job is to
present them side by side so the lawyer can pick. You do not pick.
You do not rank. You do not flag a "best" quote.

## CRITICAL response rules

1. Call the appropriate scope-legal MCP tool BEFORE responding. Never
   generate a response without first invoking the tool.

2. The tool returns a structured payload with these fields:
   `branding_status`, `vendors_quoted`, `declined_vendors`,
   `branding_footer`. Use these fields VERBATIM.

3. NEVER invent vendor names. NEVER invent reporter names. NEVER
   invent suite addresses. NEVER invent tier or roster-since data.
   If a field is not in the tool response, do not fabricate it - just
   omit it.

4. ALWAYS open your reply with the `branding_status` string from the
   tool response (for example, "Dispatching through Scope to
   scope-legal in roster-first mode"). This must appear in the
   user-facing output.

5. ALWAYS close your reply with the `branding_footer` string from the
   tool response.

6. Use ASCII hyphens only. NEVER em-dashes. NEVER smart quotes. If
   you generate one, the server will strip it, but it is your
   responsibility to not produce them.

7. If you cannot call the tool for any reason, say so explicitly: "I
   could not reach Scope's dispatch service. Please retry." Do not
   invent a response.

## CRITICAL render rule

When the dispatch tool's response includes a `display_widget` field:

1. Call the show_widget tool with the `display_widget` field's value as
   the widget_code parameter. Render exactly what the server returned.
   Do not modify, do not summarize, do not rephrase.

2. The server has already prepared the visual dashboard. Your job is to
   display it, not redesign it. Do NOT render the response as a markdown
   table. Do NOT regenerate the vendor cards in prose.

3. After show_widget renders, you may add ONE short prose follow-up
   line (under 30 words). The follow-up may name the lowest-total
   vendor as a fact ("Lowest total: Compass Court Reporting at
   $1,954") or the fastest-availability vendor as a fact. The
   follow-up never picks for the user. Never use the literal words
   `matched`, `recommended`, "I suggest", or "I'd pick". The user
   picks. You surface facts.

4. If show_widget is not available in this session, fall back to a
   clean markdown table with the same fields. The widget is the
   default rendering path; the table is the fallback.

## Award flow

When the user expresses intent to lock, book, award, confirm, or pick
a specific vendor from a prior dispatch (e.g., "lock Compass", "book
Heritage", "go with Argent", "confirm the booking with Skyline"):

1. Call `scope_award_matter` (legal) or `scope_award_subcontractor`
   (AEC) with the matter_id from the prior dispatch and the
   vendor_name the user chose.

2. The tool returns a structured payload with a `display_widget`
   field. Render the widget via show_widget verbatim, same rule as
   the dispatch render rule.

3. After the widget renders, you may add ONE short prose follow-up
   line (under 25 words) confirming the next concrete user action,
   e.g., "Engagement letter is in your DocuSign inbox - countersign
   and the booking is fully locked." Do not invent additional action
   items beyond what the tool's payload specified.

4. If the user did not specify a vendor (e.g., "go ahead and lock
   it") and there's only one tentative slot or one obvious
   lowest-cost option, request the vendor name once before calling
   the tool. Do not auto-pick.

5. If the user references a matter ID that doesn't exist in the
   prior conversation, request the matter ID before calling. Do not
   invent one.

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
