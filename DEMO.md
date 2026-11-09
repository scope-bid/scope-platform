# Try Scope in 60 seconds

Install the Scope plugin marketplace, run a couple of prompts, and see
realistic dispatch responses come back inside Cowork or Claude
Code. No signup, no token, no production data. Demo mode ships
enabled by default; the plugin manifest carries the demo bearer
`scope_pk_demo_2026`, and the live MCP server at
`scope.bid/api/mcp/legal` recognizes it and serves seeded responses.

The seed has fictional professionals across the legal service
categories (court reporting, deposition video, records retrieval,
process serving, IME, economic damages experts, e-discovery), each
named as sample data, plus seven demo matters in mixed states (open,
awarded, closed, cancelled) that belong to a fictional firm. Reads
return this seed. Writes are accepted and return plausible responses,
including new matter IDs, but nothing is saved to a firm's data and no
one is notified.

When you're ready, swap the demo token for a real one (issued at
`scope.bid/settings` after signup) and the same plugin starts running
real dispatches against your firm's actual roster and matter file.

## Install (Cowork or Claude Code)

```
/plugin marketplace add github.com/scope-bid/scope-platform
/plugin install scope-core@scope-bid
/plugin install scope-legal@scope-bid
/plugin install scope-aec@scope-bid
/plugin install scope-dispatch-agent@scope-bid
```

## Try these prompts

Paste each into Claude after the install completes. The skills
auto-fire on the trigger phrases; you don't need to invoke them by
name.

- `I need a court reporter in Dallas next Tuesday at 2pm for a 4-hour deposition.`
  Expected: Scope returns quotes from fictional court-reporting
  professionals, each named as sample data, with rates, on-time
  percentages, and prior-matters counts. The deposition-coordination
  skill auto-fires and routes to the legal MCP.

- `Show me my open matters.`
  Expected: two matters in open status (a deposition and a records
  retrieval) plus the awarded, closed, and cancelled ones if you ask
  for everything. Bid counts shown per matter.

- `What expert witnesses do you have for a forensic economics case in California?`
  Expected: fictional economic-damages experts with hourly rates and
  service notes.

- `Dispatch records retrieval for a workers comp claim in Florida, deadline 2 weeks.`
  Expected: the server first asks for the details a records request
  needs (whose records, the provider and its location, the record
  types, the date range). Once those are answered, a new matter ID
  comes back with quotes. On a quotes-only call (`award=quote_only`,
  which the tool's description asks for until the user picks a
  professional) nothing is
  sent and no approval is requested. If the call asks Scope to award,
  the dispatch is parked as a pending approval for a firm approver.
  Either way nothing is committed. The response carries
  `demo_mode: true` in the body and an `X-Scope-Demo-Mode: true` HTTP
  header. Nothing is saved to a firm's data.

- `What is the on-time percentage and satisfaction score for the first court reporter you returned?`
  Expected: the reputation snapshot - on-time percentage,
  satisfaction score, prior matters, response time, and badge tier.

- `Show me the matter details for the open deposition matter.`
  Expected: full matter with description, jurisdiction, deadline,
  budget range, and the four submitted bids.

- `Compare the records-retrieval bids on the open records matter.`
  Expected: side-by-side rendering of the three submitted bids with
  availability and rate per professional.

## AEC (preview, demo mode live)

The AEC plugin is in preview. The full dispatch flow runs in demo
mode so you can try it.

After installing scope-aec, try these prompts:

- `I need a concrete sub for a 5-story commercial project in Phoenix. Bonded over $5M, mobilize in 6 weeks, ISN-current and Avetta-verified.`
  Expected: concrete sub bids from fictional subs, each named as sample data, with prequal status, bond capacity, E-Mod, TRIR, and mobilize availability, plus any declined entries.

- `Pull the safety record for the first sub you returned.`
  Expected: E-Mod, TRIR, recordable injury counts, recent OSHA 300 history.

- `What's the bonding capacity for the second sub you returned?`
  Expected: surety bond capacity total, capacity available, current open exposures.

- `Verify ISN and Avetta status for the third sub you returned.`
  Expected: prequal status across both platforms, last refresh dates.

## What's real, what's demo

Real:

- The plugin marketplace at `github.com/scope-bid/scope-platform` is
  the production marketplace.
- The MCP server at `scope.bid/api/mcp/legal` is the production
  endpoint.
- The skills, slash commands, and dispatch agent are the production
  packages.
- The wording rules and the human sign-off rail apply in demo mode
  the same way they apply in production.

Demo:

- The professionals, reputation numbers, and rate cards are
  fictional and named as sample data. Names do not represent real
  businesses.
- The seven demo matters belong to a fictional firm. No real cases,
  no real parties.
- Dispatch responses look plausible (matter IDs, notified counts,
  bid-window timestamps) but are not saved to any firm's data. No
  professional is actually notified.
- The demo bearer (`scope_pk_demo_2026`) cannot be used for real
  writes against your firm's data.

## Switch to production

Sign up at `scope.bid` and issue a personal API token from
`scope.bid/settings`. In your installed plugin's `.mcp.json` (or
your local Cowork or Claude Code config), replace the demo bearer
with your token:

```json
"headers": {
  "Authorization": "Bearer scope_pk_<your-token>"
}
```

The same plugin and same skills now run real dispatches against your
firm's actual matters, professionals, and roster. The wording rules
and the human sign-off rail apply identically.

## What to do when something looks off

- If responses come back unauthenticated when you expect production
  behavior, your `Authorization` header is still the demo bearer.
- If the response includes `X-Scope-Demo-Mode: true`, you're in demo
  mode by design.
- If you're rate-limited (60 requests per minute per IP in demo
  mode), wait 60 seconds and try again.
- For any other issue, open a GitHub issue at
  `github.com/scope-bid/scope-platform/issues`.
