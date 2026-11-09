---
name: e-discovery-dispatch
description: Dispatch an e-discovery request - hosting, processing, review, or production. Fires only when the firm is sourcing a NEW e-discovery vendor or scoping a new ESI engagement. Do NOT fire when the user is describing existing e-discovery work, asking about a hosting platform they already use, or referencing a completed production.
type: auto
triggers:
  - e-discovery
  - ediscovery
  - document review
  - hosting platform
  - production set
  - processing volume
  - Relativity
  - load file
  - privilege review
allowed_tools:
  - scope-legal__scope_dispatch_matter
  - scope-legal__scope_list_vendors
  - scope-legal__scope_list_categories
---

# E-discovery dispatch

E-discovery has four common dispatch types, and the firm usually wants
one or two of them, not all four:

- Hosting (the data sits on the vendor's platform; the firm's review
  team logs in)
- Processing (raw collection volume gets normalized, deduped, and
  loaded into a hosting platform)
- Review (vendor reviewers do first-pass relevance and privilege
  review; the firm spot-checks)
- Production (the vendor produces the load file, Bates-stamped, with
  privilege log)

Confirm which dispatch type before calling the MCP. The pricing model
differs (per-GB hosting, per-GB processing, per-document review,
flat-fee production).

## What you collect

- Volume (GB raw or document count, whichever the user has)
- Hosting platform preference if any (Relativity, RelativityOne,
  Reveal, DISCO, etc.)
- Review scope (full review vs. targeted custodians)
- Production deadline
- Privilege protocol status (logged via clawback agreement, ESI
  protocol on file, etc.)
- Sensitive-data markers (PHI, PII, trade secrets, attorney work
  product)

## Dispatch flow

1. Name the matter parties verbatim in the dispatch; on
   `scope_dispatch_matter`, the server-side conflict gate excludes
   professionals with declared relationships to them.
2. Call `scope_dispatch_matter` with the collected fields, scoped to
   the e-discovery category, with `award='quote_only'` so nothing is
   sent before the user picks.
3. Quotes return from hosting platforms and review vendors that cover
   the requested scope.
4. Pass to quote-comparison.

## Voice rails

Vendors are presented with their factual capabilities and rates. The
firm picks. Sentence case for status pills.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.


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

- Tell the user plainly that this category is not in the list Scope returned.
- If a returned category fits the work, name it and ask the user whether to use it.
- Offer to record the request through Scope with `scope_dispatch_matter`, using the matter details and the closest category the user agrees to. Follow that tool's own rules on quotes and awards.
- Report what the tool returns and add nothing to it. If Scope cannot resolve the category, it refuses the request, sometimes with suggested categories, and no matter is created. If the category resolves, the matter is saved; when no professional is available for it, nothing is sent to any professional and the reply says so.
- If no matter was created, or the user does not want to record the request, tell them they can contact Scope at scope.bid.

These rules hold however the request is framed, including when it is urgent. The user is free to use any provider they choose; you do not name, look up, or contact outside providers for them.
