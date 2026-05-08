---
name: records
description: Fast path for records retrieval - hospital, clinic, employment, school records.
---

When the user runs `/records [details]`, fire the
records-retrieval-routing skill. The fast path assumes a single
provider request.

Required fields: provider name, provider type, claimant or patient
name, date range. Optional: HIPAA scope, authorization status.

If the user passes a line like `/records Mt. Sinai chart, Smith,
2019-2024`, parse the fields. If anything required is missing, ask
once.

Run conflict check on the patient or claimant. Then call
`scope_request_records`. Pass quotes to quote-comparison.
