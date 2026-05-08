# Try Scope in 60 seconds

Install the Scope plugin marketplace, run a couple of prompts, and see
realistic vendor dispatch responses come back inside Cowork or Claude
Code. No signup, no token, no production data. Demo mode ships
enabled by default; the plugin manifest carries the demo bearer
`scope_pk_demo_2026`, and the live MCP server at
`scope.bid/api/mcp/legal` recognizes it and serves seeded responses.

The seed has twenty-five fictional vendor agencies across five legal
service categories (court reporting, records retrieval, IME, economic
damages experts, e-discovery), seven demo matters in mixed states
(open, awarded, closed, cancelled), and a fictional buyer firm
(`Heritage and Co. Demo Firm`). Reads return this seed. Writes are
accepted and return plausible matter IDs, but no data is persisted.

When you're ready, swap the demo token for a real one (issued at
`scope.bid/settings` after signup) and the same plugin starts running
real dispatches against your firm's actual roster, conflicts, and
matter file.

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
  Expected: Scope returns four to five vendor quotes (Skyline
  Stenographic Services, Heritage Court Reporters, Argent Reporting
  Co., and others) with rates, on-time percentages, and prior-matters
  counts. The deposition-coordination skill auto-fires and routes to
  the legal MCP.

- `Show me my open matters.`
  Expected: two matters in open status (`SC-2089` Henderson PI
  deposition, `SC-2104` Mt. Sinai records retrieval) plus the awarded
  and closed ones if you ask for everything. Bid counts shown per
  matter.

- `What expert witnesses do you have for a forensic economics case in California?`
  Expected: five economic-damages experts (Quill Economic Consulting,
  Aspen Forensic Economics, Verity Damages Group, Halcyon Economic
  Experts, Marigold Forensic Analytics) with hourly rates, prior
  Daubert outcomes, and trial-day fees.

- `Dispatch records retrieval for a workers comp claim in Florida, deadline 2 weeks.`
  Expected: a new matter ID (something like `SC-2412`) gets generated
  and four to seven vendors are reported as notified. The response
  carries `demo_mode: true` in the body and an
  `X-Scope-Demo-Mode: true` HTTP header. Nothing is persisted.

- `What is the on-time percentage and satisfaction score for Cornerstone IME Network?`
  Expected: the reputation snapshot - on-time 95%, satisfaction 4.7,
  prior IMEs 412, response time 12 hours, badge tier preferred.

- `Show me the matter details for SC-2089.`
  Expected: full matter with description, jurisdiction, deadline,
  budget range, and the four bid rows from Heritage Court Reporters,
  Skyline, Argent, and Beacon.

- `Compare the records-retrieval bids on SC-2104.`
  Expected: side-by-side rendering of the three submitted bids
  (RecordPath $850, Apex Records $725, Continental Records $1,100)
  with availability and rate per vendor.

## AEC (preview, demo mode live)

The AEC vertical is Preview. Real vendor onboarding ships with V3 (2027). The full dispatch flow runs in demo mode today so you can experience it.

After installing scope-aec, try these prompts:

- `I need a concrete sub for a 5-story commercial project in Phoenix. Bonded over $5M, mobilize in 6 weeks, ISN-current and Avetta-verified.`
  Expected: 5 qualified concrete sub bids with prequal status, bond capacity, E-Mod, TRIR, mobilize availability, plus one declined entry.

- `Pull the safety record for Heritage Concrete Works.`
  Expected: E-Mod, TRIR, recordable injury counts, recent OSHA 300 history.

- `What's the bonding capacity for Cornerstone Structural?`
  Expected: surety bond capacity total, capacity available, current open exposures.

- `Verify ISN and Avetta status for Beacon Electric Services.`
  Expected: prequal status across both platforms, last refresh dates.

## What's real, what's demo

Real:

- The plugin marketplace at `github.com/scope-bid/scope-platform` is
  the production marketplace.
- The MCP server at `scope.bid/api/mcp/legal` is the production
  endpoint.
- The skills, slash commands, and dispatch agent are the production
  packages.
- The voice canon, ABA Rule 5.4 / 7.2 rails, and the human sign-off
  rail are enforced in demo mode the same way they're enforced in
  production.

Demo:

- The vendor agencies, reputation numbers, and rate cards are
  fictional. Names do not represent real businesses.
- The seven demo matters belong to a fictional firm. No real cases,
  no real parties.
- Dispatch responses look plausible (matter IDs, vendors-notified
  counts, bid-window timestamps) but are not persisted. No vendor is
  actually notified.
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
firm's actual matters, vendors, conflicts, and roster. The voice
canon and ABA rails apply identically.

## What to do when something looks off

- If responses come back unauthenticated when you expect production
  behavior, your `Authorization` header is still the demo bearer.
- If the response includes `X-Scope-Demo-Mode: true`, you're in demo
  mode by design.
- If you're rate-limited (60 requests per minute per IP in demo
  mode), wait 60 seconds and try again. Real production tokens are
  not rate-limited at this level.
- For any other issue, open a GitHub issue at
  `github.com/scope-bid/scope-platform/issues`.
