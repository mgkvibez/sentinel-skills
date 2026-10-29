---
name: triage-alert
description: Triage a security alert, scanner finding, or bug bounty report into a decision. Use when given a CVE alert, Dependabot notification, SAST finding, or vulnerability report that needs severity, reachability, and an action.
---

# Triage alert

Turn an unactionable alert into a decision: real, reachable, and urgent, or noise with evidence.

## When to use

- A dependency scanner, SAST tool, or monitoring system raised a finding.
- A bug bounty report or user vulnerability disclosure arrives.
- Someone forwards a CVE and asks "are we affected".

## Procedure

1. **Restate the claim** in one sentence, with the component and version range it applies to.
   *Done when:* the restatement names a package or file and a version.
2. **Check reachability first.** Search the lockfile for the vulnerable version, then trace whether the
   vulnerable function is imported and called. A dependency that is present but never invoked is not exploitable.
   *Done when:* the report states the resolved version and the call path, or says "not imported".
3. **Establish preconditions.** What must the attacker control, and what privilege does the code path require?
   *Done when:* preconditions list is explicit, including "authenticated user" if applicable.
4. **Assign severity** using the exploitability you verified, not the feed's score alone. If you disagree with
   the feed, say so and why.
   *Done when:* severity, rationale, and any deviation from the published score are recorded.
5. **Decide and record:** patch now, patch in the next window, accept with a compensating control, or dismiss.
   Each decision names an owner-visible next action and a review date.
   *Done when:* the decision is one of the four, with a date.

## Output format

```
## Claim
## Reachability
| package | resolved version | vulnerable range | imported | call path | evidence |
## Preconditions
## Severity
published: X  assessed: Y  why:
## Decision
action:  owner:  review-by:
```

## Rules

- Never repeat a CVE's severity without checking reachability yourself.
- Quote versions exactly as resolved in the lockfile.
- If the alert cannot be verified because the code is unavailable, say so and stop.
- Fingerprint secrets, never echo values.

## Anti-patterns

- Patching a version range with no evidence the vulnerable code is reachable.
- Dismissing an alert because "we are too small to be targeted".
- Reporting a scanner's output as your own analysis.
