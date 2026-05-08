---
name: sub
description: Fast path for subcontractor dispatch - returns five qualified vendor cards with prequal, bonding, safety, mobilize, and bid fields.
---

When the user runs `/sub [project description]`, fire the
subcontractor-dispatch skill.

The skill parses the trade, jurisdiction, bond requirement, mobilize
timeline, and any prequal preferences from the request, then calls
`scope_dispatch_subcontractor`. The MCP returns five fictional sub
cards plus one declined entry, with the lowest bid flagged via
`lowest_total: true`.

Mirrors the legal `/dispatch` command - same shape, AEC trade
categories, structured cards.

Demo mode is live; real vendor onboarding ships with V3 (2027).
