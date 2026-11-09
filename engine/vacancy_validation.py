#!/usr/bin/env python3
"""Validate paid-work candidates before qualification. Fail closed on missing evidence."""
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlparse
import re

CLOSED = ("no longer accepting applications", "not currently accepting applications",
          "position filled", "job expired", "vacancy closed")
ONSITE = ("on-site", "onsite", "office based", "office-based")
def normalized_url(value):
    u=urlparse(str(value).strip())
    return (u.netloc.lower().removeprefix("www.")+u.path.rstrip("/")).lower() if u.scheme in ("https","http") and u.netloc else ""
def opportunity_key(candidate):
    url=normalized_url(candidate.get("job_url") or candidate.get("application_url"))
    if url: return "url:"+url
    return "role:"+re.sub(r"[^a-z0-9]+","",str(candidate.get("company","")).lower())+":"+re.sub(r"[^a-z0-9]+","",str(candidate.get("role","")).lower())
def validate(candidate, today=None):
    today=today or datetime.now(timezone.utc).date()
    errors=[]
    if candidate.get("opportunity_type") != "PAID_WORK": errors.append("not verified paid work")
    if not (candidate.get("company") and candidate.get("role")): errors.append("missing company or role")
    if not normalized_url(candidate.get("job_url") or candidate.get("application_url")): errors.append("missing direct vacancy URL")
    try:
        published=date.fromisoformat(candidate["published_date"])
        if published>today or published<today-timedelta(days=7): errors.append("outside last seven days")
    except (ValueError,KeyError,TypeError): errors.append("publication date not verified")
    if candidate.get("application_status") != "OPEN_VERIFIED": errors.append("open status not verified")
    evidence=str(candidate.get("vacancy_evidence","")).lower()
    if not evidence.strip(): errors.append("missing vacancy evidence")
    if any(s in evidence for s in CLOSED): errors.append("closed vacancy evidence")
    arrangement=str(candidate.get("work_arrangement","")).upper()
    if arrangement not in ("REMOTE","HYBRID_1_DAY_WEEK"): errors.append("work arrangement outside policy")
    if any(s in evidence for s in ONSITE) and arrangement=="REMOTE": errors.append("conflicting onsite evidence")
    return errors
