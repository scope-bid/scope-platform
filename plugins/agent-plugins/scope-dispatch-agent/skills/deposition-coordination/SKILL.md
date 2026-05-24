---
name: deposition-coordination
description: Coordinate court reporter, videographer, and interpreter for a deposition. Fires only when the user is sourcing a new deposition for a current matter. Do NOT fire when the deposition is already scheduled or completed, when the user is asking about a returned transcript, or when the deposition reference is purely retrospective. Consolidator-aware - most court reporting agencies bundle reporter plus videographer plus interpreter on one rate card.
type: auto
triggers:
  - deposition
  - depo
  - depose
  - court reporter
  - schedule a depo
  - videographer
  - interpreter for a depo
allowed_tools:
  - scope-legal__scope_book_deposition
  - scope-legal__scope_list_vendors
  - scope-legal__scope_award_matter
---

# Deposition coordination

A deposition typically requires a court reporter, often a videographer,
and sometimes an interpreter. The legal market has consolidated to the
point where most major court reporting agencies bundle these on a
single rate card. Treat the deposition as one engagement, not three
separate dispatches, unless the user explicitly wants to source the
components separately.

Do not use specific agency names in your responses unless the MCP tool
returned them. Quotes are returned, presented, named by Scope's
dispatch result; do not invent or pattern-match agency names from
prior knowledge.

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

1. Call `scope_award_matter` with the matter_id from the prior
   dispatch and the vendor_name the user chose.

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

## Default flow

1. Pull deposition details from the matter intake: deponent name,
   date, jurisdiction, language requirements, video required yes or no,
   estimated duration in hours.
2. Run the conflict check against the deponent and any party of
   record. Halt if a conflict surfaces.
3. Call `scope_book_deposition` with the bundled fields. The MCP
   returns quotes from agencies that can cover the full bundle on the
   requested date.
4. Pass to the quote-comparison skill for side-by-side rendering.

## When to break the bundle

If the user explicitly asks for separate vendors (sometimes a firm
prefers a specific videographer or a specialty interpreter for a
technical witness), call `scope_dispatch_matter` per category and
let the quotes come back from different agencies. Surface the
trade-off plainly: bundling typically simplifies invoicing and on-day
coordination; unbundling typically gives the firm a specialist where
needed but means three invoices and three points of contact.

## Voice rails

Quotes are returned. Vendors are presented. The user picks. The lawyer chooses. ASCII hyphens only. No em-dashes,
no smart quotes, no ellipsis character. Sentence case for tier pills
and status labels.

Never refer to the deposition as a "match" with an agency. The agency
quoted; the lawyer awards.
