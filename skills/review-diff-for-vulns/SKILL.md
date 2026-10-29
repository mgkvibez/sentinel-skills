---
name: review-diff-for-vulns
description: Security-review a pull request or diff for vulnerabilities before merge. Use when asked to review a diff for security, check a PR for injection, authz, secrets, or unsafe deserialization.
---

# Review diff for vulnerabilities

Review the change, not the whole repository. The diff defines the blast radius.

## When to use

- A pull request touches authentication, authorization, input handling, file paths, SQL, subprocess calls,
  deserialization, or crypto.
- Someone asks "is this diff safe to merge".

## Procedure

1. **Read the diff and its context.** For each changed function, read the full function, not only the changed lines.
   *Done when:* every changed hunk has been read with its enclosing function.
2. **Classify each hunk** by the class of risk it can introduce: injection (SQL/shell/template), path traversal,
   authz bypass, unsafe deserialization, SSRF, hardcoded secret, weak crypto, unsafe default, information leak.
   *Done when:* each hunk has a class or an explicit "no security-relevant change".
3. **Trace taint for injection classes.** Identify the source (request body, query, header, filename), the sink
   (query, exec, render, file open), and whether a validator or parameterization sits between them.
   *Done when:* the taint path is named by file and line, or the hunk is cleared.
4. **Check authorization explicitly**, not just authentication. A new endpoint needs a check on the object it acts on,
   not only on the caller being logged in.
   *Done when:* every new route/action has an authz check identified or a finding filed.
5. **Report by severity with a concrete fix.** Prefer the fix that matches the codebase's existing pattern.
   *Done when:* each finding has severity, file:line, exploit path, and a fix.

## Output format

```
## Verdict
merge | merge-with-fixes | do-not-merge
## Findings
| severity | class | file:line | exploit path | fix |
## Cleared
(hunks reviewed with no security-relevant change)
```

## Rules

- A finding needs a reachable exploit path; otherwise it is a note, not a finding.
- Do not flag style, missing tests, or naming here. Stay on security.
- If a secret is added in the diff, report the fingerprint and the commit, never the value.
- State clearly what you did not review.

## Anti-patterns

- Repeating a linter's output as your own review.
- Flagging every `eval` without checking whether input reaches it.
- Blocking a PR for a pre-existing issue that this diff does not worsen.
