---
name: harden-service
description: Harden a service or application before it faces the internet. Use when asked to harden, secure a deployment, review default configuration, or prepare a service for production exposure.
---

# Harden service

Reduce the exposed surface first, then the impact of a breach. Configuration before features.

## When to use

- A service is about to be deployed publicly, or has just been.
- Someone asks to harden, prepare for production, or review deployment configuration.

## Procedure

1. **Inventory the surface.** List every listening port, public route, debug endpoint, admin interface, and
   outbound call. Anything not needed for the product is a finding.
   *Done when:* a table maps each port/route to its consumer and necessity.
2. **Check authentication and authorization defaults.** Default credentials, unauthenticated admin paths,
   and endpoints that skip the middleware chain.
   *Done when:* each admin surface states its guard, or is filed as a finding.
3. **Apply transport and header controls**: TLS configuration, HSTS, secure and httpOnly cookies with SameSite,
   and a content security policy where the app renders HTML.
   *Done when:* each control is verified in configuration, not assumed from a framework default.
4. **Constrain the runtime**: non-root user, read-only filesystem where possible, dropped capabilities,
   resource limits, and secrets injected from the environment or a secret store rather than baked into images.
   *Done when:* the deployment manifest shows each constraint.
5. **Make failure safe**: disable debug and verbose errors in production, ensure logs never contain secrets,
   and confirm rate limits exist on authentication and expensive endpoints.
   *Done when:* debug is off in the production config and a rate limit is named per sensitive route.

## Output format

```
## Surface inventory
| surface | consumer | needed | guard |
## Findings
| severity | control gap | file/config | fix |
## Applied changes
## Verified
(command output proving each control)
```

## Rules

- Verify each control by reading configuration or running a check; never assert a framework default.
- Secrets are referenced by name and fingerprint, never printed.
- Prefer removing a surface over guarding it.
- State what remains unhardened and why.

## Anti-patterns

- Adding headers while an admin panel stays unauthenticated.
- Copying a hardening checklist without mapping it to this deployment.
- Claiming a control is in place because a variable is set somewhere in the repo.
