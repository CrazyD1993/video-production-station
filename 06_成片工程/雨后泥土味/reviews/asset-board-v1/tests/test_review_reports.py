import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
TARGET = "fe82d547692b9dd0322e9ae32e9de43e14e16bb1"


class ReviewSystemContractTests(unittest.TestCase):
    def test_reviewer_role_files_exist(self):
        roles = REPO / "00_项目总控" / "审核Agents"
        for name in ["README.md", "contract-qa.md", "visual-director.md", "review-arbiter.md"]:
            self.assertTrue((roles / name).is_file(), name)

    def test_contract_qa_report(self):
        text = (ROOT / "contract-qa.md").read_text(encoding="utf-8")
        self.assertIn(TARGET, text)
        match = re.search(r"^conclusion:\s*(\S+)", text, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertIn(match.group(1), {"PASS", "PASS_WITH_CONDITIONS", "BLOCK"})
        for label in ["镜头编号", "时间位置", "证据", "严重程度", "建议"]:
            self.assertIn(label, text)

    def test_visual_director_report(self):
        text = (ROOT / "visual-director-review.md").read_text(encoding="utf-8")
        self.assertIn(TARGET, text)
        for label in ["镜头编号", "时间位置", "证据", "严重程度", "建议"]:
            self.assertIn(label, text)
        for severity in ["CRITICAL", "MAJOR", "MINOR", "NOTE"]:
            self.assertIn(severity, text)
        for decision in ["可正式保留", "限制使用", "必须替换"]:
            self.assertIn(decision, text)

    def test_arbiter_outputs(self):
        decision = (ROOT / "review-decision.yaml").read_text(encoding="utf-8")
        summary = (ROOT / "review-summary.md").read_text(encoding="utf-8")
        self.assertIn(TARGET, decision)
        for key in [
            "passed_items:", "blocking_items:", "required_assets:",
            "deferred_items:", "approve_seedance_mechanism_generation:",
            "approve_formal_composition:", "reviewer_disagreement:",
        ]:
            self.assertIn(key, decision)
        for heading in ["已通过内容", "阻塞项", "必须补齐的素材", "可延后处理项", "审核分歧"]:
            self.assertIn(heading, summary)


if __name__ == "__main__":
    unittest.main()
