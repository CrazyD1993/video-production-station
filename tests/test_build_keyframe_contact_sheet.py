import importlib.util
import hashlib
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
                Image.new("RGB", (1080, 1920), (index * 20, 50, 80)).save(folder / name)
            report = self.builder.inspect_candidates(folder)
            output = folder / "contact-sheet.jpg"
            self.builder.build_contact_sheet(report, output)
            self.assertTrue(output.exists())
            with Image.open(output) as sheet:
                expected_width = self.builder.MARGIN * 2 + self.builder.CELL_WIDTH * 2 + self.builder.GAP
                expected_height = (
                    self.builder.MARGIN * 2
                    + (self.builder.CELL_HEIGHT + self.builder.LABEL_HEIGHT) * 3
                    + self.builder.GAP * 2
                )
                self.assertEqual((expected_width, expected_height), sheet.size)
            self.assertEqual(6, len(report))

    def test_report_contains_sha256_and_label_uses_short_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in self.builder.EXPECTED_NAMES:
                Image.new("RGB", (720, 1280), "white").save(folder / name)
            report = self.builder.inspect_candidates(folder)
            first = report[0]
            expected = hashlib.sha256(first["path"].read_bytes()).hexdigest()
            self.assertEqual(expected, first["sha256"])
            self.assertEqual(
                f"KF1-01 | {expected[:8]}",
                self.builder.contact_sheet_label(first),
            )

    def test_writes_candidate_manifest_with_metadata_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in self.builder.EXPECTED_NAMES:
                Image.new("RGB", (720, 1280), "white").save(folder / name)
            report = self.builder.inspect_candidates(folder)
            output = folder / "candidate-manifest.yaml"
            self.builder.write_candidate_manifest(report, output)
            text = output.read_text(encoding="utf-8")
            self.assertIn("candidate_id: KF1-01", text)
            self.assertIn("current_decision: regenerate_with_real_reference", text)
            self.assertNotIn("image_data", text)

    def test_accepts_1080_by_1920(self):
        self._assert_dimensions_accepted((1080, 1920))

    def test_accepts_720_by_1280(self):
        self._assert_dimensions_accepted((720, 1280))

    def test_rejects_two_by_three_image(self):
        self._assert_dimensions_rejected((720, 1080))

    def test_rejects_landscape_image(self):
        self._assert_dimensions_rejected((1280, 720))

    def test_rejects_square_image(self):
        self._assert_dimensions_rejected((1280, 1280))

    def test_contact_sheet_preserves_top_and_bottom_edges(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in self.builder.EXPECTED_NAMES:
                image = Image.new("RGB", (720, 1280), "#333333")
                for y in range(80):
                    for x in range(720):
                        image.putpixel((x, y), (255, 0, 0))
                        image.putpixel((x, 1279 - y), (0, 0, 255))
                image.save(folder / name)
            report = self.builder.inspect_candidates(folder)
            output = folder / "sheet.png"
            self.builder.build_contact_sheet(report, output)
            with Image.open(output) as sheet:
                x = self.builder.MARGIN + self.builder.CELL_WIDTH // 2
                top = self.builder.MARGIN + 10
                bottom = self.builder.MARGIN + self.builder.CELL_HEIGHT - 10
                self.assertGreater(sheet.getpixel((x, top))[0], 200)
                self.assertGreater(sheet.getpixel((x, bottom))[2], 200)

    def _assert_dimensions_accepted(self, size):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in self.builder.EXPECTED_NAMES:
                Image.new("RGB", size, "white").save(folder / name)
            self.assertEqual(6, len(self.builder.inspect_candidates(folder)))

    def _assert_dimensions_rejected(self, size):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in self.builder.EXPECTED_NAMES:
                Image.new("RGB", size, "white").save(folder / name)
            with self.assertRaisesRegex(ValueError, "9:16"):
                self.builder.inspect_candidates(folder)


if __name__ == "__main__":
    unittest.main()
