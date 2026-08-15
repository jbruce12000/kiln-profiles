#!/usr/bin/env python3
"""Build docs/schedules.json from all kiln profile files in the repository."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "schedules.json"
EXCLUDE = {".git", ".github", "docs", "scripts"}
UNITS = {"C", "F"}

profiles = []
errors = []
for category_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name not in EXCLUDE):
    for path in sorted(category_dir.glob("*.json")):
        with open(path, encoding="utf-8") as f:
            profile = json.load(f)
        if profile.get("type") != "profile":
            continue
        profile["category"] = category_dir.name
        units = profile.get("units")
        if units not in UNITS:
            errors.append(f"{path}: units must be 'C' or 'F', got {units!r}")
        profiles.append(profile)

if errors:
    print("Invalid profiles:", file=sys.stderr)
    for error in errors:
        print(f"  {error}", file=sys.stderr)
    sys.exit(1)

profiles.sort(key=lambda p: (p.get("category", ""), p.get("name", "")))

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profiles, f, indent=2)
    f.write("\n")

print(f"Wrote {len(profiles)} profiles to {OUT}")
