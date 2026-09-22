#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"data/prospects.json").read_text(encoding="utf-8"))["prospects"]
counts=Counter(p.get("status","UNKNOWN") for p in data)
print("# BT38 Opportunity Engine")
print()
print(f"Total remembered prospects: **{len(data)}**")
print()
for status,count in sorted(counts.items()):
    print(f"- {status}: {count}")
print()
ready=[p for p in data if p.get("status")=="CONTACT_READY"]
print(f"Contact ready: **{len(ready)}**")
for p in ready:
    print(f"- {p.get('company')}")
