import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_keyframe_contact_sheet.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_keyframe_contact_sheet", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContactSheetTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_module()

    def test_requires_exactly_six_named_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in self.builder.EXPECTED_NAMES[:-1]:
                Image.new("RGB", (100, 150), "white").save(folder / name)
            with self.assertRaisesRegex(ValueError, "缺少"):
                self.builder.inspect_candidates(folder)

    def test_builds_two_by_three_contact_sheet(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for index, name in enumerate(self.builder.EXPECTED_NAMES):
                Image.new("RGB", (720 + index, 1080 + index), (index * 20, 50, 80)).save(folder / name)
            report = self.builder.inspect_candidates(folder)
            output = folder / "contact-sheet.jpg"
            self.builder.build_contact_sheet(report, output)
            self.assertTrue(output.exists())
            with Image.open(output) as sheet:
                self.assertGreater(sheet.height, sheet.width)
            self.assertEqual(6, len(report))


if __name__ == "__main__":
    unittest.main()
