import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from reportlab.pdfgen import canvas

from audit_resume import audit, font_name, text_layer_findings


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.profile = {"pdf_audit": {"allowed_fonts": ["Helvetica"], "headings": ["PROFILE"]}}

    def tearDown(self):
        self.temp.cleanup()

    def pdf(self, name, draw):
        path = self.root / name
        document = canvas.Canvas(str(path), pagesize=(400, 500))
        draw(document)
        document.save()
        return path

    def clean(self, name="clean.pdf", text="PROFILE"):
        return self.pdf(name, lambda c: c.drawString(30, 450, text))

    def codes(self, path, **kwargs):
        return {finding["code"] for finding in audit(path, self.profile, **kwargs)["findings"]}

    def test_clean_and_read_only(self):
        path = self.clean()
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        result = audit(path, self.profile)
        self.assertEqual(result["status"], "machine-checks-clear")
        self.assertTrue(result["visual_review_required"])
        self.assertEqual(before, hashlib.sha256(path.read_bytes()).hexdigest())

    def test_one_character_font_mismatch(self):
        def draw(c):
            c.drawString(30, 450, "PROFILE")
            c.drawString(30, 420, "DEVELOPE")
            c.setFont("Times-Roman", 12)
            c.drawString(92, 420, "R")
        codes = self.codes(self.pdf("font.pdf", draw))
        self.assertIn("unexpected-font", codes)
        self.assertIn("mixed-font-family-line", codes)

    def test_off_page(self):
        path = self.pdf("bounds.pdf", lambda c: (c.drawString(30, 450, "PROFILE"), c.drawString(-12, 420, "X")))
        self.assertIn("out-of-page-glyph", self.codes(path))

    def test_missing_and_duplicate_headings(self):
        self.assertIn("heading-occurrence", self.codes(self.clean(text="SUMMARY")))
        path = self.pdf("duplicate.pdf", lambda c: (c.drawString(30, 450, "PROFILE"), c.drawString(30, 420, "PROFILE")))
        self.assertIn("heading-occurrence", self.codes(path))

    def test_blank_page(self):
        path = self.pdf("blank.pdf", lambda c: c.showPage())
        self.assertIn("empty-page", self.codes(path))

    def test_whitespace_font_ignored(self):
        def draw(c):
            c.drawString(30, 450, "PROFILE")
            c.setFont("Times-Roman", 12)
            c.drawString(30, 420, "   ")
        self.assertNotIn("unexpected-font", self.codes(self.pdf("spaces.pdf", draw)))

    def test_symbol_exception(self):
        path = self.pdf("symbol.pdf", lambda c: (c.drawString(30, 450, "PROFILE"), c.setFont("Times-Roman", 12), c.drawString(30, 420, "*")))
        self.profile["pdf_audit"]["symbol_fonts"] = {"Times-Roman": ["*"]}
        self.assertNotIn("unexpected-font", self.codes(path))

    def test_symbol_exception_does_not_hide_body_font(self):
        def draw(c):
            c.drawString(30, 450, "PROFILE")
            c.setFont("Times-Roman", 12)
            c.drawString(30, 420, "*")
            c.setFont("Helvetica", 12)
            c.drawString(45, 420, "Body text")
        path = self.pdf("marker-line.pdf", draw)
        self.profile["pdf_audit"]["symbol_fonts"] = {"Times-Roman": ["*"]}
        self.assertNotIn("mixed-font-family-line", self.codes(path))
        self.assertIn("mixed-font-family-line", {x["code"] for x in audit(path)["findings"]})
        self.profile["pdf_audit"]["symbol_fonts"] = {"Times-Roman": ["!"]}
        self.assertIn("unexpected-font", self.codes(path))

    def test_extracted_text_corruption_is_separate_from_fonts(self):
        path = self.clean(text="PROFILE work:lows :inancial")
        result = audit(path, self.profile)
        self.assertEqual(result["status"], "needs-review")
        self.assertEqual(result["text_layer"]["status"], "needs-review")
        self.assertFalse(result["text_layer"]["independent_parser_verified"])
        self.assertIn("suspect-extracted-token", {x["code"] for x in result["findings"]})
        self.assertNotIn("unexpected-font", {x["code"] for x in result["findings"]})

    def test_expected_text_and_unicode_extraction(self):
        self.assertIn("expected-text-not-extracted", {x["code"] for x in text_layer_findings("Certiaications:", ["Certifications:"])})
        self.assertIn("unmapped-extracted-glyph", {x["code"] for x in text_layer_findings("bad\ufffd and (cid:44)")})

    def test_legitimate_punctuation_not_flagged(self):
        self.assertEqual([], text_layer_findings("Email: applicant@example.com; 13:00; https://example.com; fi fl workflows financial"))

    def test_report_records_configuration(self):
        path = self.clean()
        profile = self.root / "profile.json"
        import json
        profile.write_text(json.dumps(self.profile))
        result = subprocess.run([sys.executable, str(Path(__file__).with_name("audit_resume.py")), str(path), "--profile", str(profile)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        config = json.loads(result.stdout)["audit_configuration"]
        self.assertEqual(config["profile_path"], str(profile.resolve()))
        self.assertEqual(config["profile_sha256"], hashlib.sha256(profile.read_bytes()).hexdigest())
        self.assertIn("effective_config", config)

    def test_formatting_only_change(self):
        reference = self.clean()
        changed = self.clean("changed.pdf", "PROFILE changed")
        self.assertIn("formatting-only-text-change", self.codes(changed, reference=reference, formatting_only=True))
        self.assertNotIn("formatting-only-text-change", self.codes(reference, reference=reference, formatting_only=True))

    def test_no_reference_rejected(self):
        with self.assertRaises(ValueError):
            audit(self.clean(), formatting_only=True)

    def test_output_cannot_overwrite_source(self):
        path = self.clean()
        before = path.read_bytes()
        result = subprocess.run([sys.executable, str(Path(__file__).with_name("audit_resume.py")), str(path), "--output", str(path)], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(before, path.read_bytes())

    def test_subset_font_normalization(self):
        self.assertEqual(font_name("ABCDEF+Cambria-Bold"), "Cambria-Bold")


if __name__ == "__main__":
    unittest.main()
