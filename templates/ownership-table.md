# Ownership table

One owner and one write root per path. Anything not listed is read-only. Freeze this table before parallel work starts; change it only through the moderator.

| Path / pattern | Owner (role) | Write root | Readers | Notes |
|---|---|---|---|---|
| `work/<stage>/` | the stage's builder | `work/<stage>/` | next stage, verifier | one builder per stage |
| `contracts/` | moderator | `contracts/` | everyone | frozen; edit by change request |
| `logs/` | the running stage | `logs/<stage>/` | moderator | append only, never rewritten |
| `status/` | moderator | `status/` | everyone | current state, small files |
| `tmp/` | whoever made it | `tmp/<owner>/` | nobody else | safe to delete, never cited |
| `reports/` | verifier | `reports/` | moderator | findings only; no fixes here |
| `src/**` (everything else) | none | none | everyone | read-only |

Rules:

1. A writer touches only its own write root. A needed change elsewhere becomes a defect report to the owner.
2. Two agents never share a write root.
3. Logs are evidence, status is current truth, tmp is scratch. Never cite tmp.
4. The reviewer of a path is never its owner.
