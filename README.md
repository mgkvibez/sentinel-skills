# sentinel-skills

Defensive security playbooks for coding agents. Five skills that make an agent threat-model, triage, review, research, and harden the way a careful security engineer does, instead of guessing.

The red team shipped their skill packs first. This is the blue team's.

## Install

```bash
npx skills add mgkvibez/sentinel-skills
```

Manual install: copy any folder under `skills/` into your agent's skills directory (for Claude Code, `~/.claude/skills/`).

## The five skills

| Skill | Use it when | What it produces |
|---|---|---|
| `threat-model` | a service or feature is being designed or reviewed | data flows, STRIDE threats ranked by reachability, controls |
| `triage-alert` | a scanner, CVE alert, or bounty report lands | reachability check, severity you verified, a decision |
| `review-diff-for-vulns` | a PR touches auth, input, paths, SQL, or crypto | findings with exploit paths, plus what was cleared |
| `cve-research` | someone asks "are we affected by CVE-X" | primary-source ranges, local exposure, remediation |
| `harden-service` | a service is about to face the internet | surface inventory, control gaps, verified fixes |

## Example

```text
> use sentinel-skills threat-model on this repo

## Scope
api/ routes (7 entry points), worker/ consumers (2), out of scope: CLI
## Data flows
| flow | entry point | trust boundary | validation | store | outbound |
| upload | POST /api/files (api/files.py:41) | multipart body | validate_upload (api/files.py:12) | S3 | none |
| search | GET /api/search (api/search.py:9) | query string | none | postgres | none |
## Threats
| id | flow | STRIDE | attacker action | preconditions | reachability | evidence |
| T1 | search | Injection | inject SQL through q= | authenticated | reachable | api/search.py:23 string-concats q into the query |
## Recommendations
| threat | control | file | effort |
| T1 | parameterized query | api/search.py:23 | 10 min |
```

Every finding carries a `file:line`. If the evidence is not there, it is not a finding.

## Why these exist

Generic security checklists produce volume. These five skills enforce the parts that actually decide outcomes:

- **Reachability before severity.** A vulnerable dependency nobody imports is not an incident.
- **Citation or silence.** Every claim names a file and a line.
- **Labels, not guesses.** Output says "no issues found by ruleset v0.1", never "safe".
- **Fingerprints, not secrets.** Secrets are reported by SHA-256 prefix, never echoed.
- **Decision or nothing.** Triage ends in patch, defer, mitigate, or dismiss, with a date.

## Design rules

- Markdown only. No runtime, no dependencies, no network calls.
- Each skill is self-contained: frontmatter, when to use, numbered procedure with checkable
  completion criteria, output format, rules, anti-patterns.
- Skills describe *how to decide*. They never bake in a specific tool vendor.

## Validate locally

```bash
python3 scripts/validate_skills.py
```

Checks frontmatter, folder/name agreement, description length, required sections, substance,
and that `skills.json` matches the folders on disk. CI runs the same script.

## Contributing

New skills must be defensive, evidence-based, and free of vendor lock-in. See
[CONTRIBUTING.md](CONTRIBUTING.md). Run the validator before opening a PR.

## License

MIT. See [LICENSE](LICENSE).
