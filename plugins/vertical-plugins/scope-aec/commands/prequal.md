---
name: prequal
description: Fast path for subcontractor prequalification roll-up across ISN, Avetta, TradeTapp, Veriforce.
---

When the user runs `/prequal [sub name] [trade] [project]`, fire the
subcontractor-prequal skill.

V3 launches 2027. Until then, the command surfaces the GC's waitlist
position via `scope_aec_status`.

When V3 ships, the command rolls up prequal status from every
platform the GC subscribes to and surfaces a normalized status card.
