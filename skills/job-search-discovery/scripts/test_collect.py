import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("collect", Path(__file__).with_name("collect.py"))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class DiscoveryTests(unittest.TestCase):
    def source(self, adapter="ashby"):
        return {"id": "lab", "name": "Lab", "adapter": adapter, "lane": "personal-employment",
                "url": "https://example.com/jobs", "hours": "24"}

    def test_requisition_queries_preserved(self):
        self.assertNotEqual(c.canonical("https://x.test/?jobId=1"), c.canonical("https://x.test/?jobId=2"))
        self.assertEqual(c.canonical("https://x.test/j?utm_source=a"), "https://x.test/j")

    def test_ashby_unknown_is_not_remote(self):
        jobs = c.normalize(self.source(), json.dumps({"jobs": [{"id": "1", "title": "AI Engineer", "jobUrl": "https://x.test/1"}]}))
        self.assertEqual(jobs[0]["location"], "not stated")

    def test_greenhouse_locations(self):
        jobs = c.normalize(self.source("greenhouse"), json.dumps({"jobs": [{"id": 8, "title": "AI Architect", "absolute_url": "https://x.test/8", "location": {"name": "Remote - APAC"}}]}))
        self.assertEqual(jobs[0]["location"], "Remote - APAC")

    def test_malformed_not_empty(self):
        with self.assertRaises(KeyError):
            c.normalize(self.source(), "{}")
        self.assertEqual(c.normalize(self.source(), '{"jobs":[]}'), [])

    def test_feed_identity(self):
        xml = '<rss><channel><item><title>AI Platform Engineer</title><link>https://x.test/1</link><description>A &amp; B</description></item></channel></rss>'
        self.assertEqual(c.normalize(self.source("rss"), xml)[0]["company"], "not stated in feed")

    def test_scoring_not_work_rights(self):
        job = {"title": "AI Platform Engineer", "description": "US citizenship required"}
        self.assertGreaterEqual(c.score(job)[0], 6)
        self.assertNotIn("eligible", c.score(job)[1])

    def test_card_never_claims_prepared(self):
        job = {"company": "X", "title": "AI Architect", "key": "x1", "lane": "personal-employment",
               "source": "lab", "id": "1", "url": "https://x.test/1", "location": "US", "description": "job"}
        text = c.new_card(job, datetime.now(timezone.utc))
        self.assertIn("- State: Lead", text)
        self.assertIn("No form filled or submitted", text)

    def test_preserve_existing_and_backoff(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "sources.md").write_text("| ID | Name | Adapter | URL | Lane | Cadence hours |\n| --- | --- | --- | --- | --- | --- |\n| lab | Lab | ashby | https://example.com/jobs | personal-employment | 24 |\n")
            (root / "opportunities").mkdir()
            existing = root / "opportunities" / "saved.md"
            existing.write_text("# Original\n- URL: https://x.test/1\n- State: Submitted verified\n")
            args = SimpleNamespace(work_dir=d, known=[], limit=20, seconds=10)
            with patch.object(c.urllib.request, "urlopen", side_effect=TimeoutError("test")) as fetch:
                first = c.run(args)
                second = c.run(args)
                self.assertEqual(fetch.call_count, 1)
            self.assertEqual(len(first["errors"]), 1)
            self.assertIn("lab", second["deferred"])
            self.assertIn("Submitted verified", existing.read_text())
            self.assertIn("unknown", (root / "source-state.md").read_text())

    def test_known_role_url_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "sources.md").write_text("| ID | Name | Adapter | URL | Lane | Cadence hours |\n| --- | --- | --- | --- | --- | --- |\n| lab | Lab | ashby | https://example.com/jobs | personal-employment | 24 |\n")
            (root / "existing-applications.md").write_text("Applied https://x.test/1")
            response = unittest.mock.MagicMock()
            response.__enter__.return_value.read.return_value = b'{"jobs":[{"id":"1","title":"AI Architect","jobUrl":"https://x.test/1"}]}'
            with patch.object(c.urllib.request, "urlopen", return_value=response):
                result = c.run(SimpleNamespace(work_dir=d, known=[], limit=20, seconds=10))
            self.assertEqual(result["new_cards"], [])

    def test_daily_check_uses_next_sydney_morning(self):
        now = datetime(2026, 10, 28, 10, 0, tzinfo=timezone.utc)
        self.assertEqual(c.next_check(now, 24, "Australia/Sydney"), datetime(2026, 10, 28, 22, 0, tzinfo=timezone.utc))

    def test_default_timezone_is_utc(self):
        now = datetime(2026, 10, 28, 10, 0, tzinfo=timezone.utc)
        self.assertEqual(c.next_check(now, 24), datetime(2026, 10, 29, 9, 0, tzinfo=timezone.utc))

    def test_custom_hour(self):
        now = datetime(2026, 10, 28, 10, 0, tzinfo=timezone.utc)
        self.assertEqual(c.next_check(now, 24, "UTC", 14), datetime(2026, 10, 29, 14, 0, tzinfo=timezone.utc))

    def test_location_is_configured_not_inferred(self):
        job = {"title": "AI Architect", "description": "", "location": "Sydney, Australia"}
        self.assertEqual(c.score(job)[0] + 2, c.score(job, ["Australia"])[0])
        self.assertEqual(c.score(job)[0], c.score(job, ["Toronto"])[0])

    def test_escaped_html_is_readable_text(self):
        self.assertEqual(c.plain("&lt;p&gt;AI &amp;amp; architecture&lt;/p&gt;"), "AI & architecture")


if __name__ == "__main__":
    unittest.main()
