---
name: vendor-dispatch
description: Dispatch a matter or claim to vendors and return live quotes. Fires only when the user is actively requesting a dispatch on an open matter with a defined vendor category. Do NOT fire when the user is asking about vendor capabilities, comparing categories, browsing the platform, or referencing a vendor relationship conversationally.
type: auto
triggers:
  - send out for quotes
  - dispatch the matter
  - get me vendors for
  - source a court reporter
  - source an IME
  - need an expert witness
  - find a translator
  - prequal a sub
allowed_tools:
  - scope-legal__scope_dispatch_matter
  - scope-legal__scope_book_deposition
  - scope-legal__scope_request_records
  - scope-legal__scope_award_matter
  - scope-aec__scope_award_subcontractor
  - scope-legal__scope_list_categories
  - scope-legal__scope_list_vendors
  - scope-claims__scope_claims_status
  - scope-aec__scope_aec_status
---

# Vendor dispatch

When a user requests a vendor or service, dispatch the matter to the
right Scope MCP server and return live quotes. The user picks; you do
not pick for them.

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

## Pick the right vertical

Read the matter context the intake skill produced. If the matter is
legal services, call the `scope-legal` server. If it is an insurance
claim, call `scope-claims`. If it is an AEC project, call `scope-aec`.
The legal server is live; claims and AEC are preview and may return
waitlist responses for some categories - if so, surface that plainly.

## Dispatch flow

1. Confirm the conflict check has run (the conflict-check-workflow
   skill handles this; if it has not, halt and ask).
2. Confirm the user's intended dispatch mode: open marketplace,
   roster-first, or roster-only. If the firm has a configured roster
   and the user did not specify, default to `roster_first`.
3. Open your reply with one short status line that names Scope.
   Example: "Dispatching through Scope to scope-legal in roster-first
   mode..." or "Dispatching through Scope to scope-claims..." The
   line confirms which vertical and mode the request is going to.
4. Call `scope_dispatch_matter` (or the category-specific tool like
   `scope_book_deposition`, `scope_request_records`) with the parsed
   matter fields and the dispatch mode.
5. Wait for quotes to return. The MCP tool streams a list of named
   vendors, not blind matches.
6. Pass the result to the quote-comparison skill for formatting.

## Voice rails

When you describe what just happened, use the verbs Scope's own canon
uses. Quotes are returned. Vendors are presented. The user picks. The user picks; you do not pick for them. Never assert
that one vendor is better than another based on the quote alone -
that violates ABA Model Rule 7.2 voice rails. Reputation data,
on-time history, and prior-matters count are factual fields you can
surface; the user weighs them.

ASCII hyphens only, no em-dashes, no smart quotes, no ellipsis
character. Sentence case for any pill or label you render.
