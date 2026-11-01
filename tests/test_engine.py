import json, unittest
from datetime import datetime, timezone, timedelta
from engine.engine import validate_live, opportunity_key, search_window
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
    def test_live_filter(self):
        now=datetime(2026,11,1,tzinfo=timezone.utc)
        c={"company":"Example","role":"Operations","listing_url":"https://example.com/jobs/1",
           "published_at":(now-timedelta(days=29)).isoformat(),
           "verified_at":now.isoformat(),"open_status":"OPEN","original_listing_verified":True,"work_mode":"REMOTE","mandatory_onsite":False}
        self.assertIsNone(validate_live(c,now,30))
        self.assertIsNotNone(validate_live(dict(c,open_status="CLOSED"),now,30))\n        self.assertIsNotNone(validate_live(dict(c,work_mode="HYBRID"),now,30))\n        self.assertIsNotNone(validate_live(dict(c,mandatory_onsite=True),now,30))
        self.assertIsNotNone(validate_live(dict(c,published_at=(now-timedelta(days=31)).isoformat()),now,30))
        self.assertIsNotNone(validate_live(dict(c,verified_at=(now-timedelta(days=2)).isoformat()),now,30))
        self.assertIsNotNone(validate_live(dict(c,original_listing_verified=False),now,30))

    def test_requested_windows(self):
        p=json.loads((ROOT/"config/policy.json").read_text())
        self.assertEqual(search_window(p).total_seconds(),30*86400)
        self.assertEqual(search_window(p,requested_days=7).total_seconds(),7*86400)
        self.assertEqual(search_window(p,requested_hours=24).total_seconds(),86400)

    def test_distinct_jobs_same_employer(self):
        a={"company":"Example","role":"Operations Manager","listing_url":"https://example.com/1"}
        b={"company":"Example","role":"Marketplace Manager","listing_url":"https://example.com/2"}
        self.assertNotEqual(opportunity_key(a),opportunity_key(b))

    def test_30_day_policy(self):
        p=json.loads((ROOT/"config/policy.json").read_text())
        self.assertEqual(p["current_trigger_validation"]["freshness_window"]["max_age_days"],30)
        self.assertEqual(p["discovery"]["presentation_filter"]["max_age_days"],30)
        self.assertTrue(p["discovery"]["presentation_filter"]["require_confirmed_open_status"])

    def test_policy_has_four_gates(self):
        p=json.loads((ROOT/"config/policy.json").read_text())
        self.assertEqual(p["gates"],["company_fit","current_trigger","ability_to_pay","decision_maker_contact"])
        self.assertTrue(p["contact_ready_requires_all_gates"])
        self.assertFalse(p["auto_contact"])

    def test_state_files_exist(self):
        self.assertTrue((ROOT/"data/prospects.json").exists())
        self.assertTrue((ROOT/"data/exclusions.json").exists())
        self.assertTrue((ROOT/"inbox/candidates.json").exists())

    def test_geography_is_market_relevance_not_contact_location(self):
        p=json.loads((ROOT/"config/policy.json").read_text())
        geography=p["target_profile"]["geography"]
        self.assertIn("UK/Europe relevance", geography)
        self.assertIn("Do not reject", geography)
        rules=p["target_profile"]["geography_rules"]
        self.assertTrue(any("decision-maker location" in r for r in rules))
        self.assertTrue(any("US, Canadian" in r for r in rules))
        self.assertTrue(any("3PL referral campaign remains UK-only" in r for r in rules))

    def test_company_profile_required_before_presenting_lead(self):
        p=json.loads((ROOT/"config/policy.json").read_text())
        brief=p["company_profile_briefing"]
        self.assertTrue(brief["required_before_presenting_lead"])
        self.assertIn("Accessibility assessment", brief["required_output"])
        self.assertIn("What they do", brief["required_output"])
        self.assertIn("Route in", brief["required_output"])
        self.assertIn("Do not encourage Bhavin to apply or outreach blindly", brief["blind_application_rule"])

    def test_closed_linkedin_wording_is_hard_reject(self):
        p=json.loads((ROOT/"config/policy.json").read_text())
        scan=p["current_trigger_validation"]["presentation_preflight"]["scan_for"]
        hard=p["current_trigger_validation"]["exact_listing_preflight"]["hard_reject_signals"]
        self.assertIn("Not currently accepting applications", scan)
        self.assertIn("Not currently accepting applications", hard)

    def test_researched_lead_includes_send_ready_email(self):
        p=json.loads((ROOT/"config/policy.json").read_text())
        flow=p["lead_presentation_workflow"]
        self.assertTrue(flow["required"])
        self.assertIn("Draft the company-specific outreach email immediately after the research.", flow["sequence"])
        self.assertIn("Do not require Bhavin to ask separately for a draft.", flow["sequence"])
        self.assertIn("Do not auto-send; Bhavin decides whether to send.", flow["sequence"])
        self.assertTrue(any("LinkedIn: https://www.linkedin.com/in/bhavin-tailor-463ab6b2/" in r for r in flow["email_requirements"]))

if __name__=="__main__":
    unittest.main()
