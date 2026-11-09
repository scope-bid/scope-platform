---
name: example-court-reporting__schedule-deposition
description: Schedule a deposition through Example Court Reporting, a fictional sample partner. Auto-fires on deposition mentions when the firm has the agency on its roster.
type: auto
triggers:
  - schedule a deposition
  - book a depo
  - need a court reporter
  - example reporter
allowed_tools:
  - example-reporting__schedule_deposition
  - example-reporting__check_availability
  - example-reporting__quote_deposition
---

# Schedule a deposition through Example Court Reporting

Example Court Reporting is a fictional agency used to show the
partner plugin shape. This skill fires when the user wants to
schedule a deposition and the firm has the agency on its roster as
primary or backup. The skill calls the agency's MCP server's
deposition tools and returns a quote with availability, rate, and
bundle options (videographer plus interpreter on the same rate card).

## What you collect

- Deponent name (verbatim)
- Date or date window
- Jurisdiction (city plus state)
- Language requirements (English default; specify if interpreter is
  needed and which language)
- Video required yes or no
- Estimated duration in hours

## Dispatch flow

1. Confirm the firm has the agency on the roster for the deposition
   category. If not, halt and let the user know the agency is not on
   their roster.
2. Call `example-reporting__check_availability` with the date and
   jurisdiction.
3. If a reporter is available, call
   `example-reporting__quote_deposition` with the bundle fields and
   return the quote.
4. Pass the quote to the scope-core quote-comparison skill so the
   user sees the agency's quote alongside other professionals if they
   dispatched to multiple agencies.

## Voice rails

The reporter is presented; the lawyer awards. Never describe the
agency as `matched` to the matter. The agency quoted and the lawyer
picks.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
Sentence case for any pill or label.

The agency's MCP server returns a `bundle_options` field listing what
the agency can include on one rate card (reporter, videographer,
interpreter). If the user requested a bundle the agency covers,
surface that plainly. If the user requested something outside the
bundle (a niche specialty interpreter, for example), surface what the
agency can cover and let the user decide whether to unbundle.
