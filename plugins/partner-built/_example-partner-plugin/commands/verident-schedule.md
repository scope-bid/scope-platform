---
name: verident-schedule
description: Fast path for scheduling a deposition through the Verident network.
---

When the user runs `/verident-schedule [details]`, fire the
verident-court-reporting__schedule-deposition skill.

Required: deponent name, date, jurisdiction. Optional: video
required, language, duration.

If the user passes a single line like `/verident-schedule Smith dep,
LA, Tuesday, video, Spanish interpreter`, parse the fields. If
anything required is missing, ask once.

Confirm the firm has Verident on its roster before dispatching. If
Verident is not on the roster, explain that and let the user run
`/dispatch` instead to source from the open marketplace or other
roster vendors.
