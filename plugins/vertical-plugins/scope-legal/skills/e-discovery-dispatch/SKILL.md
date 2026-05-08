---
name: e-discovery-dispatch
description: Dispatch an e-discovery request - hosting, processing, review, or production. Auto-fires on e-discovery mentions.
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

1. Run conflict-check on the matter parties.
2. Call `scope_dispatch_matter` with the collected fields, scoped to
   the e-discovery category.
3. Quotes return from hosting platforms and review vendors that cover
   the requested scope.
4. Pass to quote-comparison.

## Voice rails

Vendors are presented with their factual capabilities and rates. The
firm picks. Sentence case for status pills.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
