---
name: quote
description: Get a quote from vendors without committing to dispatch.
---

When the user runs `/quote [vendor type] [matter description]`, fire
vendor-dispatch and call `scope_dispatch_matter` with
`award='quote_only'`. That returns the quotes and any work-order
questions still open. It chooses no professional, asks nobody to
approve anything, contacts no professional, and books nothing.

If the user then picks a professional, award that pick with
`scope_award_matter` on the same matter, never by calling
`scope_dispatch_matter` again with `award='auto'`.
