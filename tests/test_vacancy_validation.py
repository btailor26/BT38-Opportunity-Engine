import sys
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"engine"))
from vacancy_validation import validate, opportunity_key

class VacancyValidationTests(unittest.TestCase):
    def setUp(self):
        self.c={"opportunity_type":"PAID_WORK","company":"Example Ltd","role":"Marketplace Operations",
                "job_url":"https://example.com/jobs/123","published_date":"2026-11-06",
                "application_status":"OPEN_VERIFIED","vacancy_evidence":"Apply now, paid contract",
                "work_arrangement":"REMOTE"}
    def test_valid(self): self.assertEqual(validate(self.c,date(2026,11,8)),[])
    def test_old(self):
        self.c["published_date"]="2026-10-20"
        self.assertIn("outside last seven days",validate(self.c,date(2026,11,8)))
    def test_closed(self):
        self.c["vacancy_evidence"]="No longer accepting applications"
        self.assertIn("closed vacancy evidence",validate(self.c,date(2026,11,8)))
    def test_onsite(self):
        self.c["work_arrangement"]="ONSITE"
        self.assertIn("work arrangement outside policy",validate(self.c,date(2026,11,8)))
    def test_missing_proof(self):
        self.c.pop("published_date")
        self.assertIn("publication date not verified",validate(self.c,date(2026,11,8)))
    def test_same_company_distinct_roles(self):
        other=dict(self.c,role="Fulfilment Manager",job_url="https://example.com/jobs/124")
        self.assertNotEqual(opportunity_key(self.c),opportunity_key(other))
    def test_tracking_parameters_deduplicated(self):
        other=dict(self.c,job_url="https://www.example.com/jobs/123?utm_source=abc")
        self.assertEqual(opportunity_key(self.c),opportunity_key(other))
if __name__=="__main__": unittest.main()
