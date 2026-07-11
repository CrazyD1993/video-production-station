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


class Phase3SemanticValidationTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_module()
        self.manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_repository_semantics_are_valid(self):
        self.assertEqual([], self.validator.validate_repository(ROOT))

    def test_rejects_moisture_branch_in_active_timeline(self):
        broken = copy.deepcopy(self.manifest)
        broken["timelines"]["high_density_25"]["scenes"][3]["purpose"] = "moisture_control_design_variants"
        errors = self.validator.validate_manifest_semantics(broken)
        self.assertTrue(any("水汽" in error or "防雾" in error for error in errors), errors)

    def test_rejects_banned_causal_claim(self):
        errors = self.validator.validate_document_semantics(
            {"script.md": "典型结构示意，不对应具体机型\n堵住就爆"}
        )
        self.assertTrue(any("禁用表达" in error for error in errors), errors)

    def test_requires_structure_disclaimer(self):
        errors = self.validator.validate_document_semantics(
            {"storyboard.md": "V02 purpose: pressure_path"}
        )
        self.assertTrue(any("结构示意" in error for error in errors), errors)

    def test_all_keyframes_are_ready_and_reference_rules_are_filled(self):
        errors = self.validator.validate_keyframe_prompts(ROOT)
        self.assertEqual([], errors)

    def test_kf1_requires_reference_image_without_structure_disclaimer(self):
        prompt_dir = ROOT / "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/prompts"
        for name in ("KF1-01.yaml", "KF1-02.yaml"):
            data = yaml.safe_load((prompt_dir / name).read_text(encoding="utf-8"))
            self.assertIs(True, data.get("reference_image_required"), name)
            self.assertNotIn("required_disclaimer", data, name)

    def test_kf2_and_kf3_keep_structure_disclaimer(self):
        prompt_dir = ROOT / "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/prompts"
        for name in ("KF2-01.yaml", "KF2-02.yaml", "KF3-01.yaml", "KF3-02.yaml"):
            data = yaml.safe_load((prompt_dir / name).read_text(encoding="utf-8"))
            self.assertEqual(self.validator.STRUCTURE_DISCLAIMER, data.get("required_disclaimer"), name)

    def test_rejects_stale_reference_placeholder(self):
        errors = self.validator.validate_document_semantics(
            {"prompt.yaml": "典型结构示意，不对应具体机型\n待真实拆解后填写"}
        )
        self.assertTrue(any("过期状态" in error for error in errors), errors)

    def test_manifest_keyframe_status_is_ready(self):
        self.assertEqual(
            "ready_for_image_candidate_generation",
            self.manifest["keyframe_status"]["status"],
        )


if __name__ == "__main__":
    unittest.main()
