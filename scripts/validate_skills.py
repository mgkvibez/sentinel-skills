#!/usr/bin/env python3
"""Validate every SKILL.md in this repo.

Checks the things that break skill loading and discovery:
frontmatter, name/folder agreement, description length, required sections.

Usage: python scripts/validate_skills.py [--strict]
Exit code 0 when clean, 1 when any error is found.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

REQUIRED_SECTIONS = ("## When to use", "## Rules")
MIN_DESCRIPTION = 40
MAX_DESCRIPTION = 1024
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    """Return (fields, errors) for the leading YAML frontmatter block."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, ["missing frontmatter block (--- name/description ---)"]

    fields: dict[str, str] = {}
    errors: list[str] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"unparseable frontmatter line: {raw_line!r}")
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, errors


def validate_skill(path: Path) -> list[str]:
    """Return a list of error strings for one SKILL.md."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    folder = path.parent.name

    fields, fm_errors = parse_frontmatter(text)
    errors.extend(fm_errors)

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append("frontmatter is missing 'name'")
    elif name != folder:
        errors.append(f"name '{name}' does not match folder '{folder}'")
    elif not NAME_RE.match(name):
        errors.append(f"name '{name}' must be lowercase kebab-case")

    if not description:
        errors.append("frontmatter is missing 'description'")
    elif not MIN_DESCRIPTION <= len(description) <= MAX_DESCRIPTION:
        errors.append(
            f"description is {len(description)} chars, must be "
            f"{MIN_DESCRIPTION}-{MAX_DESCRIPTION}"
        )

    body = text[text.find("\n---", 3) + 4 :] if "---" in text[3:] else text
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section: {section}")
    if "## Procedure" not in text and "1." not in body:
        errors.append("missing procedure steps (## Procedure or a numbered list)")

    if len(text.split()) < 120:
        errors.append("body is shorter than 120 words; skills must be substantive")
    return errors


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print(f"error: no SKILL.md files found under {SKILLS_DIR}")
        return 1

    failures = 0
    for path in skill_files:
        errors = validate_skill(path)
        label = path.parent.name
        if errors:
            failures += 1
            print(f"FAIL {label}")
            for err in errors:
                print(f"     - {err}")
        else:
            print(f"ok   {label}")

    manifest_path = ROOT / "skills.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        listed = {entry["name"] for entry in manifest.get("skills", [])}
        present = {p.parent.name for p in skill_files}
        for missing in sorted(present - listed):
            print(f"manifest: '{missing}' is missing from skills.json")
            failures += 1
        for extra in sorted(listed - present):
            print(f"manifest: '{extra}' is listed but has no folder")
            failures += 1

    total = len(skill_files)
    print(f"\n{total - failures}/{total} skills valid" if failures <= total else "")
    if failures:
        print(f"{failures} problem(s) found")
        return 1
    if strict and total < 5:
        print("strict: expected at least 5 skills")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
