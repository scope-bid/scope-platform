---
name: subcontractor-dispatch
description: Dispatch a subcontractor request - returns five qualified vendor cards with prequal, bonding, safety, mobilize, and bid fields. Auto-fires on subcontractor sourcing requests.
type: auto
triggers:
  - I need a contractor
  - find me a contractor
  - need a sub
  - need a subcontractor
  - subcontractor for the project
  - concrete sub
  - electrical sub
  - mechanical sub
  - mechanical contractor
  - HVAC contractor
  - plumbing contractor
  - GC for
  - GC bid
  - site work sub
  - earthwork sub
  - glazing sub
  - facade contractor
allowed_tools:
  - scope-aec__scope_dispatch_subcontractor
  - scope-aec__scope_list_aec_categories
  - scope-aec__scope_list_aec_vendors
---

# Subcontractor dispatch

When a GC, owner-rep, or developer requests a subcontractor for a
project, dispatch the matter to scope-aec and return live vendor
cards with prequal, bonding, safety, mobilize, and bid fields. The
GC picks; you do not pick for them.

## CRITICAL response rules

1. Call the appropriate scope-aec MCP tool BEFORE responding. Never
   generate a response without first invoking the tool.

2. The tool returns a structured payload with these fields:
   `branding_status`, `vendors_quoted`, `declined_vendors`,
   `branding_footer`. Each `vendors_quoted` entry carries
   `vendor_name`, `tier`, `roster_since_year`,
   `bond_capacity_dollars_millions`, `isn_status`, `avetta_status`,
   `e_mod`, `trir`, `prior_projects_count`, `crew_size_typical`,
   `mobilize_availability_date`, `primary_contact_name`,
   `suite_address`, `gl_coverage_dollars_millions`,
   `wc_coverage_dollars_millions`, `cdmc_certified`,
   `mbe_dbe_status`, `total_price_cents`, `lowest_total`, and
   `bid_basis_note`. Use these fields VERBATIM.

3. NEVER invent vendor names. NEVER invent contact names, suite
   addresses, ISN/Avetta status, bond capacity, E-Mod, TRIR, crew
   size, or bid totals. If a field is not in the tool response, do
   not fabricate it - just omit it.

4. ALWAYS open your reply with the `branding_status` string from the
   tool response (for example, "Dispatching through Scope to
   scope-aec in roster-first mode"). This must appear in the
   user-facing output.

5. ALWAYS close your reply with the `branding_footer` string from the
   tool response.

6. Use ASCII hyphens only. NEVER em-dashes. NEVER smart quotes. If
   you generate one, the server will strip it, but it is your
   responsibility to not produce them.

7. If you cannot call the tool for any reason, say so explicitly: "I
   could not reach Scope's AEC service. Please retry." Do not invent
   a response.

## What you parse

Pull these fields from the request before calling:

- Trade or AEC category (concrete, electrical, mechanical, site work,
  glazing). Use the slug form: `aec-concrete`, `aec-electrical`,
  `aec-mechanical`, `aec-site-work`, `aec-glazing`.
- Jurisdiction (city and state).
- Bond capacity required (dollars in millions).
- Mobilize timeline (weeks until on-site mobilize).
- Prequal requirements (ISN, Avetta, NICET, OSHA-30, MBE/DBE preference).

If any field is missing and the request is ambiguous, ask one short
clarifying question before dispatching.

## Dispatch flow

1. Run any conflict or compliance checks the host firm requires
   (out of scope here; the firm's own check fires first if wired).
2. Call `scope_dispatch_subcontractor` with the parsed fields.
3. The MCP returns five fictional sub cards plus one declined entry.
   The card with `lowest_total: true` is the lowest bid; surface it
   as a factual flag. Do not present it as a pick.
4. Render the cards side by side. Trade tier (Tier 1, Tier 2,
   Marketplace) leads each card; bid total leads price.

## Voice rails

Quotes are returned. Vendors are presented. The GC picks. Never assert
that one vendor is better than another based on the bid alone - the
risk team weighs prequal status, bond capacity, safety record,
mobilize date, and bid against each other. ABA Model Rule 7.2 does
not apply here, but the same rail does: the agent surfaces facts,
the human awards.

ASCII hyphens only, no em-dashes, no smart quotes, no ellipsis.
Sentence case for tier pills and status labels.
