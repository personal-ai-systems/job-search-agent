import copy
import unittest

from audit_application import audit, fingerprint


class CoverageTests(unittest.TestCase):
    def base(self):
        return {
            "job_id": "req1", "url": "https://example.org/application", "page_count": 1,
            "pages": [{"number": 1, "inventoried": True, "evidence": "current-page", "control_ids": ["rights"]}],
            "fields": [{"id": "rights", "page": 1, "label": "Sponsorship?", "required": False,
                        "active": True, "disposition": "answered", "value": False,
                        "observed_value": False, "evidence": "user-for-this-role", "verified": True}],
            "documents": [{"name": "CV.pdf", "sha256": "a" * 64, "verified": True}],
        }

    def test_false_is_a_complete_answer(self):
        self.assertTrue(audit(self.base())["ready_for_review"])

    def test_zero_is_a_complete_answer(self):
        data = self.base()
        data["fields"][0].update(value=0, observed_value=0)
        self.assertTrue(audit(data)["ready_for_review"])

    def test_optional_unknown_blocks_readiness(self):
        data = self.base()
        data["fields"][0].update(disposition="waiting-user", value=None, observed_value=None)
        self.assertFalse(audit(data)["ready_for_review"])

    def test_silent_optional_blank_blocks(self):
        data = self.base()
        data["fields"][0].update(value=" ", observed_value=" ")
        self.assertFalse(audit(data)["ready_for_review"])

    def test_decline_requires_user_decision(self):
        data = self.base()
        data["fields"][0].update(disposition="declined", value=None, observed_value=None)
        self.assertFalse(audit(data)["ready_for_review"])
        data["fields"][0]["user_decision"] = "User explicitly declined for this application"
        self.assertTrue(audit(data)["ready_for_review"])

    def test_required_blank_decline_blocks(self):
        data = self.base()
        data["fields"][0].update(required=True, disposition="declined", value=None,
                                 observed_value=None, user_decision="declined")
        self.assertFalse(audit(data)["ready_for_review"])

    def test_hidden_branch_needs_observed_condition(self):
        data = self.base()
        data["fields"][0].update(active=False, disposition="not-applicable", value=None, observed_value=None)
        self.assertFalse(audit(data)["ready_for_review"])
        data["fields"][0]["condition"] = "No selected; follow-up absent after rescan"
        self.assertTrue(audit(data)["ready_for_review"])

    def test_missing_page_blocks(self):
        data = self.base()
        data["page_count"] = 2
        self.assertFalse(audit(data)["ready_for_review"])

    def test_duplicate_field_blocks(self):
        data = self.base()
        data["fields"].append(copy.deepcopy(data["fields"][0]))
        self.assertFalse(audit(data)["ready_for_review"])

    def test_uncommitted_dropdown_blocks(self):
        data = self.base()
        data["fields"][0]["observed_value"] = "Please select"
        self.assertFalse(audit(data)["ready_for_review"])

    def test_no_approval_is_not_submission_permission(self):
        result = audit(self.base())
        self.assertTrue(result["ready_for_review"])
        self.assertFalse(result["submission_gate_clear"])

    def test_answer_edit_invalidates_approval(self):
        data = self.base()
        data["approval"] = {"fingerprint": fingerprint(data), "final_copy_shown": True, "evidence": "exact-copy-user-approval"}
        self.assertTrue(audit(data)["submission_gate_clear"])
        data["fields"][0].update(value=True, observed_value=True)
        self.assertFalse(audit(data)["submission_gate_clear"])

    def test_document_edit_invalidates_approval(self):
        data = self.base()
        data["approval"] = {"fingerprint": fingerprint(data), "final_copy_shown": True, "evidence": "exact-copy-user-approval"}
        data["documents"][0]["sha256"] = "b" * 64
        self.assertFalse(audit(data)["submission_gate_clear"])

    def test_empty_ledger_is_not_coverage(self):
        data = self.base()
        data["fields"] = []
        self.assertFalse(audit(data)["ready_for_review"])

    def test_inventory_catches_optional_section_omitted_from_ledger(self):
        data = self.base()
        data["pages"][0]["control_ids"].append("work-experience")
        result = audit(data, page_number=1)
        self.assertFalse(result["page_gate_clear"])
        self.assertTrue(any("work-experience" in item["message"] for item in result["findings"]))

    def test_empty_optional_repeatable_section_blocks_next(self):
        data = self.base()
        data["pages"][0]["control_ids"].append("education")
        data["fields"].append(dict(id="education", page=1, label="Education", required=False,
                                   active=True, disposition="answered", value=[], observed_value=[],
                                   evidence="PDF already uploaded", verified=True))
        self.assertFalse(audit(data, page_number=1)["page_gate_clear"])

    def test_page_pass_does_not_grant_submission_or_final_review(self):
        data = self.base()
        data["approval"] = dict(fingerprint=fingerprint(data), final_copy_shown=True, evidence="approved")
        result = audit(data, page_number=1)
        self.assertTrue(result["page_gate_clear"])
        self.assertFalse(result["ready_for_review"])
        self.assertFalse(result["submission_gate_clear"])

    def test_page_audit_allows_unvisited_later_pages(self):
        data = self.base()
        data["page_count"] = 3
        data["documents"] = []
        self.assertTrue(audit(data, page_number=1)["page_gate_clear"])
        self.assertFalse(audit(data)["ready_for_review"])

    def test_current_optional_unknown_blocks_page_even_if_later_unvisited(self):
        data = self.base()
        data["page_count"] = 3
        data["fields"][0].update(disposition="waiting-user", value=None, observed_value=None)
        self.assertFalse(audit(data, page_number=1)["page_gate_clear"])

    def test_missing_selected_page_blocks(self):
        data = self.base()
        data["page_count"] = 3
        self.assertFalse(audit(data, page_number=2)["page_gate_clear"])

    def test_missing_live_control_inventory_blocks(self):
        data = self.base()
        del data["pages"][0]["control_ids"]
        self.assertFalse(audit(data, page_number=1)["page_gate_clear"])
        self.assertFalse(audit(data)["ready_for_review"])

    def test_cannot_delete_unresolved_field_only_to_pass(self):
        data = self.base()
        data["pages"][0]["control_ids"].append("salary")
        self.assertFalse(audit(data, page_number=1)["page_gate_clear"])

    def test_later_unresolved_page_does_not_block_resolved_current_page(self):
        data = self.base()
        data["page_count"] = 2
        data["pages"].append(dict(number=2, inventoried=True, evidence="page2", control_ids=["salary"]))
        data["fields"].append(dict(id="salary", page=2, label="Salary", required=False,
                                   active=True, disposition="waiting-user", value=None, observed_value=None))
        self.assertTrue(audit(data, page_number=1)["page_gate_clear"])
        self.assertFalse(audit(data, page_number=2)["page_gate_clear"])
        self.assertFalse(audit(data)["ready_for_review"])

    def test_no_resume_requires_explicit_checked_disposition(self):
        data = self.base()
        data["documents"] = []
        self.assertFalse(audit(data)["ready_for_review"])
        data["document_free_workflow"] = {"verified": True, "evidence": "Portal requests profile only", "user_decision": "User agreed no attachment for this application"}
        self.assertTrue(audit(data)["ready_for_review"])


if __name__ == "__main__":
    unittest.main()
