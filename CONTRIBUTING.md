# Contributing

A skill is a procedure a tired agent can follow at 2am. Optimise for that.

## Adding a skill

1. `mkdir skills/<skill-name>` (lowercase, hyphenated).
2. Add `SKILL.md` with frontmatter:

```markdown
---
name: skill-name
description: One sentence on when to use this, written for an agent routing on intent.
---

# Skill Name

## When to use
## Procedure
## Rules
## Output format
```

3. Number the procedure. Every step ends with a checkable completion criterion.
4. Register it in `skills.json`.
5. Run the validator until clean.

## Running the tests

```bash
python3 scripts/validate_skills.py --strict
```

`--strict` is what CI runs. It fails on: missing frontmatter, name/folder mismatch, description
under 40 or over 1024 characters, missing required sections, skills under the substance floor, and
manifest drift.

## What we reject

- Skills that produce a verdict without an artifact.
- Skills that call something "safe". Say "no issues found by ruleset vN".
- Skills that assume a specific scanner, cloud, or vendor.
- Duplicated procedure under a new name.

## Pull requests

One skill per PR, validator green, and a note on what the skill produced when you ran it.
