#!/usr/bin/env bash
# Release gate for sentinel-skills: run before every push that claims "done".
# Two independent checks: skills validate, and the manifest matches the tree.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== check 1/2: skill validator (strict, same as CI)"
python3 scripts/validate_skills.py --strict

echo "== check 2/2: manifest parity"
python3 - <<'PY'
import json, pathlib, sys
manifest = json.loads(pathlib.Path("skills.json").read_text())
declared = {s["name"] for s in manifest["skills"]}
on_disk = {p.parent.name for p in pathlib.Path("skills").glob("*/SKILL.md")}
if declared != on_disk:
    print(f"manifest drift: declared-only={sorted(declared-on_disk)} disk-only={sorted(on_disk-declared)}")
    sys.exit(1)
print(f"{len(declared)} skills declared and present")
PY
echo "ALL CHECKS PASSED"
