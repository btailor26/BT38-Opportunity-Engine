import json
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from engine.engine import validate_live, opportunity_key, search_window, canonical_url

ROOT = Path(__file__).resolve().parents[1]

class OpportunityTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 1, tzinfo=timezone.utc)
        self.c = dict(company="Example", role="Operations", listing_url="https://example.com/jobs/1",
                      published_at=(self.now-timedelta(days=6)).isoformat(),
                      verified_at=self.now.isoformat(), open_status="OPEN",
                      original_listing_verified=True, work_mode="REMOTE",
                      mandatory_onsite=False, required_languages=["English"])

    def test_remote_and_hybrid(self):
        self.assertIsNone(validate_live(self.c, self.now, timedelta(days=30)))
        self.assertIsNone(validate_live(dict(self.c, work_mode="HYBRID",
                           mandatory_onsite_days_per_week=1), self.now, timedelta(days=30)))
        self.assertIsNotNone(validate_live(dict(self.c, work_mode="HYBRID",
                             mandatory_onsite_days_per_week=2), self.now, timedelta(days=30)))
        self.assertIsNotNone(validate_live(dict(self.c, work_mode="ONSITE"), self.now, timedelta(days=30)))

    def test_closed_and_unverified(self):
        for change in (dict(listing_status_text="No longer accepting applications"),
                       dict(open_status="CLOSED"), dict(original_listing_verified=False),
                       dict(required_languages=["German"]),
                       dict(verified_at=(self.now-timedelta(days=2)).isoformat())):
            self.assertIsNotNone(validate_live(dict(self.c, **change),
                                 self.now, timedelta(days=30)))

    def test_exact_window(self):
        policy = json.loads((ROOT/"config/policy.json").read_text())
        self.assertEqual(search_window(policy), timedelta(days=30))
        self.assertEqual(search_window(policy, requested_days=7), timedelta(days=7))
        self.assertEqual(search_window(policy, requested_hours=24), timedelta(hours=24))
        old = dict(self.c, published_at=(self.now-timedelta(days=8)).isoformat())
        self.assertIsNone(validate_live(old, self.now, timedelta(days=30)))
        self.assertIsNotNone(validate_live(old, self.now, timedelta(days=7)))

    def test_url_normalization(self):
        self.assertEqual(canonical_url("https://www.example.com/jobs/1/?utm_source=x"),
                         canonical_url("https://example.com/jobs/1"))
        self.assertEqual(opportunity_key(self.c), opportunity_key(
            dict(self.c, listing_url="https://www.example.com/jobs/1/?utm_source=x")))

    def test_required_files(self):
        for name in ("data/prospects.json", "data/opportunity_history.json",
                     "inbox/candidates.json"):
            self.assertTrue((ROOT/name).exists())

if __name__ == "__main__":
    unittest.main()
