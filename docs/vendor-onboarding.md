# Vendor onboarding SOP

How real vendors get added to Scope's production marketplace. This is
the operations checklist; do not mix this flow with the demo-data
path. Demo vendors are fictional and live in `lib/mcp/demo-data.ts`
plus `supabase/migrations/0029_seed_demo_data.sql`. Real vendors
never touch those files.

## Pre-onboarding

Before any database write happens, the vendor relationship needs to
clear three things:

1. A signed Scope vendor agreement on file (legal, master service
   terms, fee structure).
2. A category fit decision. Scope's verticals are scoped per
   namespace (`bid.scope/legal`, `bid.scope/claims`,
   `bid.scope/aec`). The vendor goes to one or more categories
   inside the matching vertical.
3. Jurisdiction coverage and capacity claims captured in writing,
   not pattern-matched from a website.

## Account creation

Real vendors are rows in the production `organizations` table:

```sql
INSERT INTO organizations
  (id, name, org_type, is_demo, jurisdictions, categories, ...)
VALUES
  (gen_random_uuid(), 'Vendor Name', 'vendor', false, '{...}', '{...}');
```

`is_demo` must be `false`. Never reuse the demo org id
`00000000-0000-0000-0000-000000000001` for a real vendor. Never copy
a row from the demo seed into a real-vendor row.

## Token issuance

Real vendors get a production API token of the form
`scope_pk_<random>`. Never `scope_pk_demo_2026` and never any token
starting with `scope_pk_demo_`. The demo prefix is reserved for the
public anonymous surface and is rate-limited at 60 requests per
minute per IP. Production tokens are scoped to the vendor's org id
and issued through the admin console.

## Integration wiring

Each vendor's inbound webhook (quote returns, status updates) is
HMAC-signed using a per-vendor secret. The secret is stored in the
production secrets store and never written to a migration. Outbound
dispatch payloads to the vendor go over HTTPS with the vendor's
public webhook URL on file.

## Reputation seeding

A new vendor starts with `reputation_status = 'pending'`. Do not
backfill on-time percentages, prior-matter counts, or rate-card
benchmarks from estimates. Reputation accrues only from real
completed matters routed through Scope. A pending vendor is
surfaced to lawyers with a clear pending tag; they are never
returned with fabricated stats.

## Verification

After the row lands, smoke-test against production with the new
vendor's real token:

```
curl -s -X POST https://scope.bid/api/mcp/legal \
  -H "Authorization: Bearer scope_pk_<real-token>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"scope_list_vendors",
                 "arguments":{"category_slug":"<category>"}}}'
```

The vendor's row should appear with `is_demo = false`. If it
appears with `is_demo = true` or alongside fictional roster names,
stop and audit; the demo and production paths have crossed.

## What NOT to do

- Do not edit `lib/mcp/demo-data.ts` to add a real vendor.
- Do not edit `supabase/migrations/0029_seed_demo_data.sql` to add
  a real vendor.
- Do not copy reputation numbers from a vendor's marketing page
  into the database.
- Do not issue a `scope_pk_demo_` token to a real vendor.
- Do not skip the signed agreement step. The agreement is the
  permission slip for everything downstream.

## Voice canon

Vendor-facing copy follows the same rails as the rest of Scope:
ASCII hyphens, sentence case, "returned" or "presented" never
"matched" or "recommended", "request" not "ask", "your firm" or
"your team" in positioning copy. ABA Model Rules 5.4 and 7.2 sit
underneath every word that the agent surfaces about a vendor.
