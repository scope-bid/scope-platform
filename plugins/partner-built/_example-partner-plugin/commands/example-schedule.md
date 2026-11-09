---
name: example-schedule
description: Fast path for scheduling a deposition through Example Court Reporting, a fictional sample partner.
---

When the user runs `/example-schedule [details]`, fire the
example-court-reporting__schedule-deposition skill.

Required: deponent name, date, jurisdiction. Optional: video
required, language, duration.

If the user passes a single line like `/example-schedule Smith dep,
LA, Tuesday, video, Spanish interpreter`, parse the fields. If
anything required is missing, ask once.

Confirm the firm has Example Court Reporting on its roster before
dispatching. If it is not on the roster, explain that and let the
user run `/dispatch` instead to get quotes from other professionals
through Scope.
