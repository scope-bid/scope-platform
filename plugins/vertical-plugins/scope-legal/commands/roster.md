---
name: roster
description: View or edit the firm's vendor roster.
---

When the user runs `/roster`, fire the roster-management skill from
scope-core. The skill handles both views (current roster by category)
and edits (promote, demote, exclude).

If the user passes args like `/roster show court reporter` or
`/roster exclude <vendor>`, parse the intent and call the right
roster MCP tool. Confirm changes back in plain English. Do not commit
changes the user has not asked for.

Roster tiers are: primary, backup, excluded. Sentence case in any
output.
