# Partner plugins

Vendor agencies can ship their own plugin inside the Scope plugin
marketplace. This is how court reporting agencies, IME networks,
records-retrieval shops, e-discovery platforms, and other launch-
cohort vendors get distribution inside Scope's install graph.

## What a partner plugin is

A partner plugin is a self-contained package with:

- One or more skills (auto-fire instructions for Claude inside Cowork
  or Claude Code)
- One or more slash commands (fast paths the user types into Claude)
- One MCP connector entry pointing at the partner's MCP server (or
  a JSON-RPC endpoint if the partner does not run MCP yet)

When a firm installs the partner plugin, the partner's tools become
callable from inside the firm's Claude session, and the partner's
skills auto-fire on the right triggers. The firm can route to the
partner via `roster_first` or `roster_only` mode and the partner
shows up as a primary or backup vendor on the matters where the
firm has tiered them.

## What you get as a partner

- Distribution inside Scope's install graph. Every firm that
  installs `scope-legal` or `scope-claims` and adds your plugin gets
  your tools wired in automatically.
- Auto-fire skills inside the lawyer's, claims VP's, or GC's Claude
  session. When the user describes the kind of work you do, your
  skill surfaces.
- Slash commands published. The user can type `/your-action` and
  hit your tools directly.
- A canonical voice. Every partner plugin passes the same lint
  rails the first-party Scope plugins pass, so the user reads one
  consistent voice across vendors.

## Skill manifest contract

Every skill is a directory under `<your-plugin>/skills/<skill-name>/`
containing a `SKILL.md` with this frontmatter:

```yaml
---
name: <partner>__<action>
description: <one sentence, plain English, sentence case>
type: auto
triggers:
  - <trigger phrase>
  - <trigger phrase>
allowed_tools:
  - <partner>__<tool_name>
---
```

Naming convention: every skill name is `<partner>__<action>`. The
double underscore separator is enforced by the lint script. Skill
descriptions are sentence case, plain English, under 30 words.

The skill body is 200-400 words of prose instruction telling Claude
what to do when the skill fires. No corporate jargon. Use the same
voice rails the first-party Scope skills use.

## Connector schema

Every partner plugin includes an `.mcp.json` declaring the partner's
MCP server:

```json
{
  "mcpServers": {
    "<partner>": {
      "url": "https://<partner-domain>/mcp",
      "transport": "http",
      "description": "<one sentence about what the server does>",
      "auth": {
        "type": "bearer",
        "header": "Authorization"
      },
      "rate_limit": {
        "requests_per_minute": 60,
        "burst": 10
      }
    }
  }
}
```

The `auth` and `rate_limit` blocks are optional but encouraged. If
your server does not run MCP yet, point at a JSON-RPC endpoint with
the same shape and document the call signatures in your README.

## Voice canon

Every partner plugin must pass `scripts/lint-voice-canon.py`. The
short list:

- ASCII hyphens only. No em-dashes, no en-dashes, no smart quotes,
  no ellipsis character.
- Sentence case for all eyebrows, pills, labels, slash command
  names.
- `Returned` or `presented`. Never `matched` or `recommended`. ABA
  Rule 7.2 sits underneath this.
- "Request" not "ask" in positioning copy.
- Plain English. Avoid "operationalize", "structurally",
  "materially", "regulatory drag".

The lint runs in CI on every PR. Failing voice-canon lint blocks
merge.

## How to submit

1. Fork the `scope-platform` repo.
2. Create your plugin directory at `plugins/partner-built/<your-
   slug>/`.
3. Copy `_example-partner-plugin/` as a starting point.
4. Fill in your skills, commands, and connector.
5. Run `python3 scripts/check.py` and `python3 scripts/lint-voice-
   canon.py` locally. Fix any violations.
6. Open a PR against the `scope-platform` repo with a short
   description of what your plugin does and which firms you expect
   to install it.

## Review SLA

Scope reviews every partner-plugin PR within 5 business days. The
review checks: voice canon, security model (auth, rate limit), tool
naming, the manifest contract, and the partner's stated coverage.

If revisions are needed, the review comment lists specific files and
lines. Your second push gets a re-review within 2 business days.

## Branding rules

- Sentence case, no all-caps anywhere except inside literal code or
  proper noun acronyms (USA, IME, IRS).
- Switzer typography in any UI surface your plugin renders. The
  `[scope]` brackets are JetBrains Mono; everything else is Switzer.
- The canonical eyebrow style is sentence case, 13px, Switzer
  Medium, secondary text color. Pill style is sentence case, 11px,
  Switzer Medium, semantic background.
- No decorative monospace (uppercase + letterspacing) eyebrows.
  That pattern is retired across the Scope canon.

## What partner plugins do not do

- Pick a vendor for the user. Quotes are returned, not assigned.
- Bypass the conflict-check workflow.
- Commit a dispatch the human has not approved.
- Surface "best fit" or `recommended` labels.
- Use any data the firm did not provide. The plugin operates on
  exactly the matter context the firm passes through.

If your plugin needs a capability outside this contract, open an
issue before submitting the PR. We extend the contract for new
patterns; we do not waive the rails.
