#!/usr/bin/env python3
"""Validate supplied vacancies; this processor does not discover jobs."""
import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INBOX = ROOT / "inbox"
CLOSED = ("no longer accepting applications", "not currently accepting applications",
          "applications closed", "position filled", "job expired",
          "this job is no longer available", "vacancy closed", "role closed")

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(value):
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())

def canonical_url(value):
    try:
        u = urlsplit(str(value or "").strip())
        if u.scheme not in ("http", "https") or not u.netloc:
            return ""
        query = urlencode(sorted((k, v) for k, v in parse_qsl(u.query)
                                  if not k.lower().startswith("utm_")))
        return urlunsplit(("https", u.netloc.lower().removeprefix("www."),
                           u.path.rstrip("/"), query, ""))
    except ValueError:
        return ""

def opportunity_key(c):
    url = canonical_url(c.get("listing_url") or c.get("source_url"))
    return url or (norm(c.get("company")), norm(c.get("role") or c.get("job_title")),
                   norm(c.get("location")))

def search_window(policy, requested_hours=None, requested_days=None):
    if requested_hours is not None and requested_days is not None:
        raise ValueError("Specify either hours or days")
    value = requested_hours if requested_hours is not None else requested_days
    if value is not None and (isinstance(value, bool) or
                              not isinstance(value, (int, float)) or value <= 0):
        raise ValueError("Search window must be positive")
    if requested_hours is not None:
        return timedelta(hours=requested_hours)
    return timedelta(days=requested_days if requested_days is not None
                     else policy["search_scope"]["default_opportunity_window_days"])

def validate_live(c, now, window):
    text = " ".join(str(c.get(k, "")) for k in
                    ("listing_status_text", "listing_page_text", "application_status")).casefold()
    if any(term in text for term in CLOSED):
        return "Original listing states applications are closed"
    mode = str(c.get("work_mode", "")).upper().strip()
    onsite = c.get("mandatory_onsite_days_per_week")
    if mode == "REMOTE" and c.get("mandatory_onsite") is False:
        pass
    elif mode == "HYBRID" and type(onsite) in (int, float) and 0 <= onsite <= 1:
        pass
    else:
        return "Work arrangement unverified or more than one office day weekly"
    languages = c.get("required_languages", [])
    if not isinstance(languages, list) or any(
        norm(lang) not in ("english", "") for lang in languages
    ):
        return "Mandatory non-English language requirement"
    if not (canonical_url(c.get("listing_url") or c.get("source_url")) and
            c.get("original_listing_verified") is True and
            c.get("open_status") == "OPEN" and
            c.get("published_at") and c.get("verified_at")):
        return "Missing original listing, publication date or verified OPEN status"
    try:
        published = datetime.fromisoformat(str(c["published_at"]).replace("Z", "+00:00"))
        verified = datetime.fromisoformat(str(c["verified_at"]).replace("Z", "+00:00"))
        if published.tzinfo is None or verified.tzinfo is None:
            return "Timestamps require timezone"
        if published > now or now - published > window:
            return "Outside requested publication window"
        if verified > now or now - verified > timedelta(hours=24):
            return "Open-status verification is stale"
    except (ValueError, TypeError, OverflowError):
        return "Invalid publication or verification date"
    return None

def process(requested_hours=None, requested_days=None):
    policy = load(ROOT / "config/policy.json")
    state = load(DATA / "prospects.json")
    inbox = load(INBOX / "candidates.json")
    history_path = DATA / "opportunity_history.json"
    history = load(history_path) if history_path.exists() else {"opportunities": []}
    records = history["opportunities"]
    prospects = state["prospects"]
    now = datetime.now(timezone.utc)
    window = search_window(policy, requested_hours, requested_days)
    seen = {str(r["key"]) for r in records}
    # Previously stored prospects also count as seen, even before this register existed.
    seen.update(str(opportunity_key(p)) for p in prospects
                if p.get("listing_url") or p.get("source_url"))
    results = []
    for candidate in inbox.get("candidates", []):
        company = str(candidate.get("company", "")).strip()
        key = str(opportunity_key(candidate))
        if not company:
            results.append({"decision": "REJECTED", "reason": "Anonymous company"})
            continue
        if key in seen:
            results.append({"company": company, "decision": "DUPLICATE",
                            "reason": "Already searched or recorded"})
            continue
        seen.add(key)
        reason = validate_live(candidate, now, window)
        records.append({"key": key, "company": company,
                        "role": candidate.get("role") or candidate.get("job_title"),
                        "url": candidate.get("listing_url") or candidate.get("source_url"),
                        "checked_at": now.isoformat(),
                        "decision": "REJECTED" if reason else "QUALIFIED",
                        "reason": reason})
        if reason:
            results.append({"company": company, "decision": "REJECTED", "reason": reason})
            continue
        missing = [g for g in policy["gates"]
                   if str(candidate.get("gates", {}).get(g, "")).upper() != "PASS"]
        candidate["status"] = "RESEARCHED" if missing else "CONTACT_READY"
        candidate["qualification_missing"] = missing
        candidate["engine_checked_at"] = now.isoformat()
        prospects.append(candidate)
        results.append({"company": company, "decision": candidate["status"],
                        "missing": missing})
    state["prospects"] = prospects
    (DATA / "prospects.json").write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
    (INBOX / "candidates.json").write_text('{"candidates": []}\n')
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--hours", type=float)
    group.add_argument("--days", type=float)
    args = parser.parse_args()
    for result in process(requested_hours=args.hours, requested_days=args.days):
        print(json.dumps(result, ensure_ascii=False))
