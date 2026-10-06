import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
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
