# Changelog

## v0.1.0 - 2026-10-29

- Five defensive skills: `threat-model`, `triage-alert`, `review-diff-for-vulns`,
  `cve-research`, `harden-service`. Each is a numbered procedure where every step
  ends with a checkable completion criterion, so an agent can tell whether it
  finished the step instead of guessing.
- `skills.json` manifest plus `scripts/validate_skills.py`, which enforces
  frontmatter, name/folder agreement, required sections, a substance floor, and
  manifest parity. `--strict` is what CI runs.
- Worked example in `examples/threat-model-migsafe.md`: the threat-model skill
  applied to a real CLI, five ranked threats, explicit scope limits, next actions.
- Release gate `scripts/verify.sh` (validator + manifest parity) and
  `approve-first-time.yml`, which approves CI for outside contributors but never
  for a PR that touches CI configuration.
- Install: `npx skills add mgkvibez/sentinel-skills` (requires Node 22.20 or newer).
