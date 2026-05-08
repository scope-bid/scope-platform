---
name: dispatch
description: Dispatch a matter to vendors and return live quotes.
---

When the user runs `/dispatch [matter description]`, route through the
vendor-dispatch skill from scope-core. If matter intake has not yet
parsed the matter, fire matter-intake-parsing first; then run the
conflict-check workflow; then dispatch.

The user can pass a free-text matter description after the slash
command. If they pass nothing, ask for the matter description in one
short prompt.

When quotes return, hand off to quote-comparison for side-by-side
rendering. Do not pick for the user. Present what came back.
