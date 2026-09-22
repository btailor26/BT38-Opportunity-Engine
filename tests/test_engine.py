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

if __name__=="__main__":
    unittest.main()
