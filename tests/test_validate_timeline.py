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
        broken["timelines"]["full_42"]["scenes"][1]["start_seconds"] += 0.5
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("空档" in error for error in errors), errors)

    def test_detects_overlap_between_scenes(self):
        broken = copy.deepcopy(self.manifest)
        broken["timelines"]["full_42"]["scenes"][1]["start_seconds"] -= 0.5
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("重叠" in error for error in errors), errors)

    def test_detects_timeline_total_mismatch(self):
        broken = copy.deepcopy(self.manifest)
        broken["timelines"]["high_density_35"]["duration_seconds"] = 36
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("总时长" in error for error in errors), errors)

    def test_detects_seedance_contract_mismatch(self):
        broken = copy.deepcopy(self.manifest)
        broken["seedance_contracts"]["S04"]["duration_seconds"] = 6
        errors = self.validator.validate_manifest(broken)
        self.assertTrue(any("Seedance" in error and "S04" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
