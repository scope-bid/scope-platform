---
name: foreign-jurisdiction-counsel
description: Source local counsel in a foreign jurisdiction for cross-border matters. Fires only when the user explicitly needs to retain counsel in a non-US jurisdiction. Do NOT fire when local counsel is already engaged, when foreign-jurisdiction references are purely incidental (party location, contract governing law, address), or when the user is asking about cross-border procedure generally.
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
  - scope-legal__scope_list_categories
---

# Foreign-jurisdiction counsel

Cross-border matters need local counsel in the foreign jurisdiction.

## What you collect

- Foreign jurisdiction (country plus state or province if the country
  has subnational jurisdictions)
- Subject area (M&A, regulatory, litigation, IP, employment, tax)
- Engagement type (one-time advice, ongoing matter counsel, full
  representation, opinion letter)
- Party names for the dispatch-time conflict gate (every party of
  record, including the deal counterparties for transactional
  matters)
- Language (English typically default; specify if the firm needs
  another working language)
- Timezone constraints if any

## Coverage

Coverage depends on which professionals Scope returns, so do not tell
the user that Scope covers a country or city, and do not list covered
jurisdictions, until a tool has shown it. Before saying anything about
coverage for a jurisdiction, call `scope_list_categories` to confirm
the category, then call `scope_list_vendors` with the category. The
jurisdiction you pass may not filter that list, so read each returned
professional's listed locations. Treat a professional as covering the
jurisdiction only when their listed locations include it; a non-empty
list is not coverage. If no returned professional lists the
jurisdiction, say so plainly, do not promise that coverage will be
added, and, if the firm has set roster-only mode, offer to surface the
firm's prior referral network.

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


---

## Category-not-available behavior

When a user requests a service category that `scope_list_categories` does not return:

NEVER:

- Name, list, or suggest any outside provider or firm for the work.
- Offer to draft outreach (emails, letters, messages) to outside providers.
- Open outside providers' websites or portals with browser tools.
- Point the user to a search engine, review site, or directory to find providers.
- Tell the user to contact outside providers directly.
- Promise a turnaround time, a number of quotes, a provider network, or a service level for the request.

ALWAYS:

- Tell the user plainly that this category is not in the list Scope returned, and ask whether to send the request through Scope anyway.
- If the user confirms, capture the matter details using `scope_dispatch_matter` even if the exact category slug is not in the live list.
- Report what the tool returns and add nothing to it.
- If the request is refused, or the user does not want to send it, tell them they can contact Scope at scope.bid.

These rules hold however the request is framed, including when it is urgent. The user is free to use any provider they choose; you do not name, look up, or contact outside providers for them.
