#!/usr/bin/env python3
import json, re
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
INBOX=ROOT/"inbox"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(s):
    return re.sub(r"[^a-z0-9]+","",str(s).lower())

def known_names(prospects, exclusions):
    names=set()
    for p in prospects:
        names.add(norm(p.get("company","")))
        for a in p.get("aliases",[]): names.add(norm(a))
    for x in exclusions: names.add(norm(x))
    return {x for x in names if x}

def gate(candidate,key):
    return str(candidate.get("gates",{}).get(key,"")).upper()=="PASS"

def process():
    policy=load(ROOT/"config/policy.json")
    state=load(DATA/"prospects.json")
    exclusions=load(DATA/"exclusions.json")["companies"]
    inbox=load(INBOX/"candidates.json")
    prospects=state["prospects"]
    known=known_names(prospects,exclusions)
    results=[]

    for c in inbox.get("candidates",[]):
        company=str(c.get("company","")).strip()
        if not company:
            results.append({"company":"","decision":"REJECTED","reason":"anonymous company"})
            continue
        if norm(company) in known:
            results.append({"company":company,"decision":"REJECTED","reason":"duplicate/excluded"})
            continue

        missing=[g for g in policy["gates"] if not gate(c,g)]
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
        known.add(norm(company))
        results.append({"company":company,"decision":decision,"missing":missing})

    state["prospects"]=prospects
    DATA.joinpath("prospects.json").write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    INBOX.joinpath("candidates.json").write_text(json.dumps({"candidates":[]},indent=2)+"\n",encoding="utf-8")
    return results

if __name__=="__main__":
    for r in process():
        print(json.dumps(r,ensure_ascii=False))
