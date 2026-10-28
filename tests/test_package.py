from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def source_files():
    for p in ROOT.rglob("*"):
        if any(part in {".git", ".venv", "__pycache__"} for part in p.relative_to(ROOT).parts):
            continue
        if p.is_file():
            yield p


class PackageTests(unittest.TestCase):
    def test_no_private_artifacts(self):
        denied = {".pdf", ".pages", ".docx", ".xlsx", ".zip", ".key", ".pem", ".db", ".sqlite"}
        for p in source_files():
            self.assertNotIn(p.suffix.lower(), denied, str(p))
            self.assertFalse(p.is_symlink(), str(p))

    def test_no_host_paths_or_live_cloud_identifiers(self):
        user_root = "/" + "Users" + "/"
        for p in source_files():
            text = p.read_text()
            self.assertNotIn(user_root, text, str(p))
            self.assertIsNone(re.search(r"docs\.google\.com/spreadsheets/d/[A-Za-z0-9_-]{20,}", text), str(p))
            self.assertIsNone(re.search(r"drive\.google\.com/file/d/[A-Za-z0-9_-]{20,}", text), str(p))
            self.assertIsNone(re.search(r"(?:ghp|gho)_[A-Za-z0-9]{20,}", text), str(p))
            self.assertIsNone(re.search(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----", text), str(p))

    def test_only_synthetic_email_examples(self):
        for p in source_files():
            for address in re.findall(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", p.read_text()):
                self.assertTrue(address.endswith("@example.com") or address.endswith("@example.org"), (str(p), address))

    def test_skill_entrypoints_and_local_references(self):
        for name in ("job-search-agent", "job-search-discovery", "resume-update", "job-apply"):
            path = ROOT / "skills" / name / "SKILL.md"
            text = path.read_text()
            self.assertTrue(text.startswith("---\nname: " + name + "\n"))
            self.assertIn("\ndescription:", text.split("---", 2)[1])
            for ref in re.findall(r"\[[^]]+\]\(([^)\s]+\.md)\)", text):
                self.assertTrue((path.parent / ref).is_file(), (name, ref))

    def test_private_paths_ignored_but_examples_included(self):
        # Archive-based hosts have no .git directory; exercise the real rules in isolation.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            (root / ".gitignore").write_text((ROOT / ".gitignore").read_text())
            for path in ("private/profile.md", "workspace/intent.md", "runtime/run.md", ".env", "data/example.json", "person.pdf", "opportunities/job.md"):
                result = subprocess.run(["git", "check-ignore", "--no-index", path], cwd=root, capture_output=True)
                self.assertEqual(result.returncode, 0, path)
            result = subprocess.run(["git", "check-ignore", "--no-index", "examples/workspace/host.md"], cwd=root, capture_output=True)
            self.assertEqual(result.returncode, 1)

    def test_orchestrator_loads_real_root_without_scheduler(self):
        path = ROOT / "skills" / "job-search-agent" / "SKILL.md"
        self.assertIn("../../AGENT.md", path.read_text())
        self.assertTrue((path.parent / "../../AGENT.md").resolve().is_file())
        self.assertIn("No second schedule", path.read_text())
        self.assertTrue((ROOT / "docs" / "moltis.md").is_file())


if __name__ == "__main__":
    unittest.main()
