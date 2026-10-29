# Threat model: migsafe (applied with skills/threat-model)

Worked example: the threat-model skill run against a real CLI that reads SQL files.

## 1. What we are protecting

- **Integrity of the migration files** being linted: the tool must never rewrite SQL it inspects.
- **Developer trust in a finding**: a missed lock is a production outage; a false alarm is a deleted check.
- **No secret leakage**: migrations can contain credentials in DEFAULTs or comments.

## 2. Assets and entry points

| Asset | Entry point | Notes |
|---|---|---|
| SQL file contents | `migsafe check path...` | untrusted input, arbitrary size |
| Terminal output | stdout | may be pasted into public issues |
| Exit status | CI gate | a wrong `0` silently ships a bad migration |

## 3. Threats, ranked

1. **Silent pass on an obfuscated statement** (T1, high). A migration splits statements inside a
   dollar-quoted block and the linter sees nothing to flag. Mitigation: the splitter is
   dollar-quote, string, and comment aware, and tests pin that behavior.
2. **False alarm on a safe pattern** (T2, medium). `CREATE INDEX` on a table the same migration
   creates is safe; flagging it trains people to ignore the tool. Mitigation: new-table suppression,
   covered by a test.
3. **Secret echoed to stdout** (T3, high). A `DEFAULT 'sk_live_...'` in a finding would leak on paste.
   Mitigation: findings quote the rule and the statement head, never full literal values.
4. **Denial of service by input size** (T4, low). A 200 MB generated migration. Mitigation: line-based
   scan, no quadratic parsing.
5. **Exit-code dishonesty** (T5, medium). `--fail-on` misconfiguration returning 0. Mitigation: exit 2
   paths asserted in tests.

## 4. What this model does not cover

- SQL dialect differences beyond PostgreSQL.
- Semantics inside stored procedures (we lint the DDL, not the PL/pgSQL body).
- Intent: a deliberate `DROP TABLE` is reported, not blocked.

## 5. Next actions

- [x] Dollar-quote aware splitter
- [x] New-table index suppression
- [ ] Truncate long literals in finding text
- [ ] Fuzz the splitter with `hypothesis`
