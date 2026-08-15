#!/usr/bin/env python3
"""Build docs/schedules.json from all kiln profile files in the repository."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "schedules.json"
EXCLUDE = {".git", ".github", "docs", "scripts"}

profiles = []
for category_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name not in EXCLUDE):
    for path in sorted(category_dir.glob("*.json")):
        with open(path, encoding="utf-8") as f:
            profile = json.load(f)
        if profile.get("type") != "profile":
            continue
        profile["category"] = category_dir.name
        profiles.append(profile)

profiles.sort(key=lambda p: (p.get("category", ""), p.get("name", "")))

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profiles, f, indent=2)
    f.write("\n")

print(f"Wrote {len(profiles)} profiles to {OUT}")
