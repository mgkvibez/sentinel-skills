---
name: threat-model
description: Build a threat model for a repository, service, or feature before it ships. Use when asked to threat model, review security design, assess attack surface, or answer "what could go wrong" about a system.
---

# Threat model

Produce a threat model grounded in the code that actually exists. Never invent
components the repository does not contain.

## When to use

- A new service, endpoint, or data flow is being designed or reviewed.
- Someone asks "is this secure", "what could an attacker do", or "what are the risks".
- Before a release that changes authentication, authorization, or data storage.

## Procedure

1. **Establish scope.** Name the components under review and read their entry points
   (routes, handlers, queue consumers, CLI commands). Note what is explicitly out of scope.
   *Done when:* every entry point has a file path and a line number.
2. **Map the data flow.** For each entry point record: untrusted input, trust boundary crossed,
   data store touched, and outbound calls made. Trust boundaries are where validation must exist.
   *Done when:* each flow names the validation function that actually guards the boundary, or is
   marked unguarded.
3. **Enumerate threats** with STRIDE against each flow. Skip categories that cannot apply, and say why.
   *Done when:* every flow has threats or an explicit "not applicable" note.
4. **Rank by reachability.** For each threat state the concrete attacker action, the preconditions,
   and whether the code path is reachable today. Unreachable findings go in a separate section.
   *Done when:* each threat is labelled reachable, conditional, or unreachable, with evidence.
5. **Recommend controls** that are proportionate and implementable in the existing design.
   Each recommendation names the file it would touch.
   *Done when:* every reachable threat has at least one control or an accepted-risk note.

## Output format

```
## Scope
## Data flows
| flow | entry point | trust boundary | validation | store | outbound |
## Threats
| id | flow | STRIDE | attacker action | preconditions | reachability | evidence |
## Recommendations
| threat | control | file | effort |
## Accepted risks
```

## Rules

- Cite file and line for every claim. No citation, no finding.
- Say "no issues found by ruleset vX" rather than "safe".
- Never downgrade a reachable high-severity finding to make a report look clean.
- Secrets found during review are reported by fingerprint only, never by value.

## Anti-patterns

- Threat modelling a diagram instead of the code.
- Copying a generic OWASP checklist without mapping it to real entry points.
- Reporting volume instead of reachability.
