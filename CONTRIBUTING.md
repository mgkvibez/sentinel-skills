# Contributing

## Adding a skill

1. Create `skills/<kebab-name>/SKILL.md`.
2. Frontmatter must contain `name` (matching the folder) and `description` (40-1024 chars, written so an
   agent can decide *when* to load the skill from the description alone).
3. Required sections: `## When to use`, a numbered procedure with a `*Done when:*` criterion per step,
   `## Output format`, `## Rules`, `## Anti-patterns`.
4. Add the skill to `skills.json`.
5. Run `python3 scripts/validate_skills.py` and make it pass.

## What we accept

- Defensive security work: prevention, detection, triage, review, hardening.
- Procedures that end in verifiable state, not advice.
- Anything where the agent must cite evidence or explicitly say it could not verify.

## What we reject

- Offensive tooling, exploit development, or anything aimed at systems the user does not own.
- Generic advice with no procedure ("follow best practices").
- Vendor-specific instructions that only work with one paid product.

## Style

- Second person, imperative, short sentences.
- No emoji in skill bodies. Tables over prose for anything enumerable.
- Never instruct an agent to print a secret; fingerprints only.
