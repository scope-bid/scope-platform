---
name: roster-management
description: View or edit a firm's vendor roster. Auto-fires on roster-tier mentions or on requests to add, remove, or re-tier a vendor.
type: auto
triggers:
  - primary vendor
  - preferred vendor
  - excluded vendor
  - blocklist
  - vendor roster
  - move to backup
  - promote to primary
  - default agency
allowed_tools:
  - scope-legal__scope_list_vendors
  - scope-legal__scope_list_matters
---

# Roster management

A firm's roster is the system of record for who they prefer to work
with. Three tiers:

- `primary`: the firm's default vendor for the category. Roster-first
  dispatch routes here before opening to the marketplace.
- `backup`: surfaced when primary is at capacity or has a conflict.
- `excluded`: never surface this vendor to the user, regardless of
  marketplace availability. Excluded usually means the firm had a bad
  past engagement and does not want this vendor in any quote view.

## Dispatch modes

The roster interacts with three dispatch modes:

- `open`: ignore the roster, query the full Scope marketplace, return
  every named vendor that fits.
- `roster_first` (default for firms with a roster): query the roster
  first; if no primary is available, fall through to backup, then to
  marketplace.
- `roster_only`: never leave the roster. If no roster vendor is
  available, return empty and let the user decide whether to escalate
  to open.

## What this skill does

When a user describes their roster intent ("make Capitol our primary
court reporter", "exclude Veritext", "show me the current roster"),
parse the intent and call the right roster MCP tool. Confirm changes
back to the user in plain English. Do not commit changes the user has
not asked for.

## Voice rails

Use sentence case for tier names in any UI surface. Roster changes
are never automatic - the user commits each change. ASCII hyphens
only. No em-dashes, no smart quotes, no ellipsis character.

When a roster change has downstream effects on open matters (for
example, demoting a primary vendor on an in-flight matter), surface
the affected matters before committing the change.
