#!/usr/bin/env python3
import json, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
INBOX=ROOT/"inbox"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(s):
    return re.sub(r"[^a-z0-9]+","",str(s).lower())

def known_names(prospects):
    names=set()
    for p in prospects:
        names.add(norm(p.get("company","")))
        for a in p.get("aliases",[]): names.add(norm(a))
    return {x for x in names if x}

def gate(candidate,key):
    return str(candidate.get("gates",{}).get(key,"")).upper()=="PASS"

def opportunity_key(c):
    return (norm(c.get("company", "")), norm(c.get("role") or c.get("opportunity") or c.get("job_title") or ""), str(c.get("source_url") or c.get("listing_url") or "").strip().lower())

def validate_live(c, now, max_days):
    """Fail closed: candidate evidence must be independently checked before ingestion."""
    date = c.get("published_at")
    checked = c.get("verified_at")
    url = c.get("listing_url") or c.get("source_url")
    if not (date and checked and url and c.get("open_status") == "OPEN" and c.get("original_listing_verified") is True):
        return "missing verified original listing, publication date, or confirmed OPEN status"
    try:
        published = datetime.fromisoformat(str(date).replace("Z", "+00:00"))
        verified = datetime.fromisoformat(str(checked).replace("Z", "+00:00"))
        if published.tzinfo is None or verified.tzinfo is None:
            return "timestamps must include timezone"
        if published > now or now - published > timedelta(days=max_days):
            return "outside 30-day publication window"
        if verified > now or now - verified > timedelta(hours=24):
            return "open-status verification is older than 24 hours"
    except (ValueError, TypeError):
        return "invalid publication or verification timestamp"
    return None

def process():
    policy=load(ROOT/"config/policy.json")
    state=load(DATA/"prospects.json")
    inbox=load(INBOX/"candidates.json")
    prospects=state["prospects"]
    known={opportunity_key(p) for p in prospects if opportunity_key(p)[1] or opportunity_key(p)[2]}\n    now=datetime.now(timezone.utc)\n    max_days=policy["discovery"]["presentation_filter"]["max_age_days"]
    results=[]

    for c in inbox.get("candidates",[]):
        company=str(c.get("company","")).strip()
        if not company:
            results.append({"company":"","decision":"REJECTED","reason":"anonymous company"})
            continue
        if norm(company) in known:
            results.append({"company":company,"decision":"DUPLICATE","reason":"already exists in prospect history"})
            continue

        invalid=validate_live(c,now,max_days)\n        if invalid:\n            results.append({"company":company,"decision":"REJECTED","reason":invalid})\n            continue\n\n        missing=[g for g in policy["gates"] if not gate(c,g)]
        if missing:
            c["status"]="RESEARCHED"
            c["qualification_missing"]=missing
            decision="HOLD"
        else:
            c["status"]="CONTACT_READY"
            c["qualification_missing"]=[]
            decision="CONTACT_READY"

        c["engine_checked_at"]=datetime.now(timezone.utc).isoformat()
        prospects.append(c)
        known.add(key)
        results.append({"company":company,"decision":decision,"missing":missing})

    state["prospects"]=prospects
    DATA.joinpath("prospects.json").write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    INBOX.joinpath("candidates.json").write_text(json.dumps({"candidates":[]},indent=2)+"\n",encoding="utf-8")
    return results

if __name__=="__main__":
    for r in process():
        print(json.dumps(r,ensure_ascii=False))
