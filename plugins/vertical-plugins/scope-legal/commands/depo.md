---
name: depo
description: Fast path for deposition coordination - reporter, video, interpreter on one rate card.
---

When the user runs `/depo [details]`, fire the deposition-coordination
skill. The fast path assumes a bundled engagement (reporter plus
videographer plus interpreter on one agency rate card).

Required fields: deponent name, date, jurisdiction. Optional:
language, video required, estimated hours.

If the user passes a single line like `/depo Smith dep, Bakersfield,
Tuesday, video, Spanish interpreter`, parse the fields from natural
language. If anything required is missing, ask once.

Run conflict check on the deponent. Then call `scope_book_deposition`.
Pass quotes to quote-comparison.
