import copy
import importlib.util
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "validate_phase2_semantics.py"
MANIFEST_PATH = ROOT / "08_OpenMontage试验" / "03-生产清单模板.yaml"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_phase2_semantics", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Phase2SemanticValidationTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_module()
        self.manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_repository_semantics_are_valid(self):
        self.assertEqual([], self.validator.validate_repository(ROOT))

    def test_rejects_legacy_s06_purpose(self):
        broken = copy.deepcopy(self.manifest)
        broken["timelines"]["full_42"]["scenes"][5]["purpose"] = "hypothetical_blockage"
        errors = self.validator.validate_manifest_semantics(broken)
        self.assertTrue(any("S06" in error and "purpose" in error for error in errors), errors)

    def test_rejects_banned_causal_claim(self):
        errors = self.validator.validate_document_semantics(
            {"script.md": "S06 purpose: moisture_control_design_variants\n堵住就爆"}
        )
        self.assertTrue(any("禁用表达" in error for error in errors), errors)

    def test_requires_structure_disclaimer(self):
        errors = self.validator.validate_document_semantics(
            {"storyboard.md": "S06 purpose: moisture_control_design_variants"}
        )
        self.assertTrue(any("结构示意" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
