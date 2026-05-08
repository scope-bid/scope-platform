---
name: deposition-coordination
description: Coordinate court reporter, videographer, and interpreter for a deposition. Auto-fires on deposition mentions. Consolidator-aware - most court reporting agencies bundle reporter plus videographer plus interpreter on one rate card.
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
