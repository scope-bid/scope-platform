---
name: foreign-jurisdiction-counsel
description: Source local counsel in a foreign jurisdiction for cross-border matters. Auto-fires on cross-border or non-US-jurisdiction mentions.
type: auto
triggers:
  - foreign counsel
  - local counsel
  - cross-border
  - foreign jurisdiction
  - German law
  - English law
  - Singapore counsel
  - non-US matter
allowed_tools:
  - scope-legal__scope_dispatch_matter
  - scope-legal__scope_list_vendors
---

# Foreign-jurisdiction counsel

Cross-border matters need local counsel in the foreign jurisdiction.
The Scope marketplace covers the major commercial jurisdictions and
adds new ones as demand surfaces.

## What you collect

- Foreign jurisdiction (country plus state or province if the country
  has subnational jurisdictions)
- Subject area (M&A, regulatory, litigation, IP, employment, tax)
- Engagement type (one-time advice, ongoing matter counsel, full
  representation, opinion letter)
- Conflict-check inputs (every party of record, including the deal
  counterparties for transactional matters)
- Language (English typically default; specify if the firm needs
  another working language)
- Timezone constraints if any

## Common jurisdictions

The legal MCP currently has named-counsel coverage in:

- Germany (Frankfurt, Munich, Berlin, Dusseldorf)
- United Kingdom (London, Edinburgh)
- Switzerland (Zurich, Geneva)
- Netherlands (Amsterdam)
- Hong Kong, Singapore
- Japan (Tokyo)
- Australia (Sydney, Melbourne)
- Brazil (Sao Paulo, Rio de Janeiro)
- Mexico (Mexico City)
- Canada (Toronto, Montreal, Vancouver)

If the matter needs a jurisdiction not in the list, call
`scope_list_categories` and `scope_list_vendors` to confirm coverage.
If the marketplace does not cover the jurisdiction, surface that
plainly and offer to surface the firm's prior referral network if
roster-only mode is set.

## Voice rails

Foreign counsel is presented with named firms. The lead lawyer
retains. Do not refer to a foreign firm as "qualified" - that is a
local-bar judgment, not a label you apply. Stick to factual fields:
named partners on the matter, prior-engagement count, language
capacity, expected fee schedule.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
Sentence case for tier pills. Use plain English; avoid Latin tags
("forum non conveniens" is fine if the user introduces it; do not
volunteer it).
