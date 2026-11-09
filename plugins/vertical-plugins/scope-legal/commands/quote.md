---
name: quote
description: Get a quote from vendors without committing to dispatch.
---

When the user runs `/quote [vendor type] [matter description]`, fire
vendor-dispatch in dry-run mode (no commit, no calendar booking, no
roster update). The skill calls the MCP dispatch tool with the
`commit=false` parameter so vendors return rate and availability but
no engagement is created.

Quotes returned this way expire on the vendor's quoted-availability
window. If the user later wants to commit, run `/dispatch` against
the same matter and reference the quote ID.
