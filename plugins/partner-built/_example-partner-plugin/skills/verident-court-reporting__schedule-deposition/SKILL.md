---
name: verident-court-reporting__schedule-deposition
description: Schedule a deposition through the Verident Court Reporting network. Auto-fires on deposition mentions when the firm has Verident on its roster.
type: auto
triggers:
  - schedule a deposition
  - book a depo
  - need a court reporter
  - verident reporter
allowed_tools:
  - verident__schedule_deposition
  - verident__check_availability
  - verident__quote_deposition
---

# Schedule a deposition through Verident

This skill fires when the user wants to schedule a deposition and
the firm has Verident on its roster as primary or backup. The
skill calls the Verident MCP server's deposition tools and returns
a quote with availability, rate, and bundle options (videographer
plus interpreter on the same rate card).

## What you collect

- Deponent name (verbatim, for the conflict-check workflow)
- Date or date window
- Jurisdiction (city plus state)
- Language requirements (English default; specify if interpreter is
  needed and which language)
- Video required yes or no
- Estimated duration in hours

## Dispatch flow

1. Confirm the firm has Verident on the roster for the deposition
   category. If not, halt and let the user know Verident is not on
   their roster.
2. Confirm the conflict check has run on the deponent.
3. Call `verident__check_availability` with the date and
   jurisdiction.
4. If a reporter is available, call `verident__quote_deposition`
   with the bundle fields and return the quote.
5. Pass the quote to the scope-core quote-comparison skill so the
   user sees Verident's quote alongside other vendors if they
   dispatched to multiple agencies.

## Voice rails

The reporter is presented; the lawyer awards. Never describe
Verident as `matched` to the matter. The agency quoted and the
lawyer picks.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
Sentence case for any pill or label.

The Verident MCP returns a `bundle_options` field listing what the
agency can include on one rate card (reporter, videographer,
interpreter). If the user requested a bundle the Verident network
covers, surface that plainly. If the user requested something
outside the bundle (a niche specialty interpreter, for example),
surface what Verident can cover and let the user decide whether to
unbundle.
