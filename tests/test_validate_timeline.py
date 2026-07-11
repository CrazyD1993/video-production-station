import copy
import importlib.util
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "validate_timeline.py"
MANIFEST_PATH = ROOT / "08_OpenMontage试验" / "03-生产清单模板.yaml"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_timeline", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TimelineValidationTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator_module()
        self.manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_repository_manifest_is_valid(self):
        self.assertEqual([], self.validator.validate_manifest(self.manifest))

    def test_detects_gap_between_scenes(self):
        broken = copy.deepcopy(self.manifest)
        broken["timelines"]["explanation_29"]["scenes"][1]["start_seconds"] += 0.5
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("空档" in error for error in errors), errors)

    def test_detects_overlap_between_scenes(self):
        broken = copy.deepcopy(self.manifest)
        broken["timelines"]["explanation_29"]["scenes"][1]["start_seconds"] -= 0.5
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("重叠" in error for error in errors), errors)

    def test_detects_timeline_total_mismatch(self):
        broken = copy.deepcopy(self.manifest)
        broken["timelines"]["high_density_25"]["duration_seconds"] = 26
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("总时长" in error for error in errors), errors)

    def test_detects_seedance_contract_mismatch(self):
        broken = copy.deepcopy(self.manifest)
        broken["seedance_contracts"]["V02"]["duration_seconds"] = 6
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("Seedance" in error and "V02" in error for error in errors), errors)

    def test_phase3_uses_only_25_29_and_12_second_timelines(self):
        self.assertEqual(
            {"high_density_25", "explanation_29", "visual_sample_12"},
            set(self.manifest["timelines"]),
        )
        self.assertEqual("high_density_25", self.manifest["active_timeline"])

    def test_visual_sample_uses_v01_v02_v03(self):
        scenes = self.manifest["timelines"]["visual_sample_12"]["scenes"]
        self.assertEqual(["V01", "V02", "V03"], [scene["id"] for scene in scenes])
        self.assertEqual([3, 5, 4], [scene["end_seconds"] - scene["start_seconds"] for scene in scenes])


if __name__ == "__main__":
    unittest.main()
