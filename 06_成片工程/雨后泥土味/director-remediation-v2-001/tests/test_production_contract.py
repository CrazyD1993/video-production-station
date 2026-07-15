import csv
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "S01": (0.00, 1.20), "S02": (1.20, 3.85), "S03": (3.85, 5.69),
    "S04": (5.69, 8.70), "S05": (8.70, 12.32), "S06": (12.32, 17.10),
    "S07": (17.10, 21.38), "S08": (21.38, 24.30), "S09": (24.30, 27.35),
    "S10": (27.35, 30.50), "S11": (30.50, 35.06), "S12": (35.06, 39.77),
    "S13": (39.77, 46.80),
}


class ProductionContractTests(unittest.TestCase):
    def test_locked_timeline_has_thirteen_status_entries(self):
        path = ROOT / "shot-status.yaml"
        self.assertTrue(path.is_file(), "shot-status.yaml 尚未实现")
        text = path.read_text(encoding="utf-8")
        blocks = re.findall(
            r"- id: (S\d+)\n\s+start: ([0-9.]+)\n\s+end: ([0-9.]+)\n\s+status: ([a-z_]+)",
            text,
        )
        self.assertEqual(13, len(blocks))
        self.assertEqual(list(EXPECTED), [item[0] for item in blocks])
        for shot_id, start, end, status in blocks:
            self.assertEqual(EXPECTED[shot_id], (float(start), float(end)))
            self.assertIn(status, {"done", "partial", "blocked"})

    def test_clean_preview_and_mechanism_clips_have_locked_specs(self):
        expected_media = {
            "petrichor-remediation-v2-clean-preview.mp4": 46.80,
            "mechanism-a-v2.mp4": 12.68,
            "mechanism-b-v2.mp4": 13.68,
        }
        for name, duration in expected_media.items():
            path = ROOT / name
            self.assertTrue(path.is_file(), f"{name} 尚未实现")
            result = subprocess.run([
                "ffprobe", "-v", "error", "-show_streams", "-show_format",
                "-of", "json", str(path),
            ], check=True, capture_output=True, text=True)
            data = json.loads(result.stdout)
            video = next(item for item in data["streams"] if item["codec_type"] == "video")
            self.assertEqual((540, 960), (video["width"], video["height"]))
            self.assertEqual("24/1", video["r_frame_rate"])
            self.assertAlmostEqual(duration, float(data["format"]["duration"]), delta=0.06)

    def test_manifest_is_traceable_and_reuse_is_at_most_two(self):
        path = ROOT / "asset-manifest-v2.csv"
        self.assertTrue(path.is_file(), "asset-manifest-v2.csv 尚未实现")
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        required = {
            "shot_id", "timeline", "mother_asset_id", "mother_asset_path",
            "source_timecode", "original_duration", "target_duration",
            "actual_speed_ratio", "derivation", "usage_status", "license_record",
        }
        self.assertTrue(required.issubset(rows[0].keys()))
        uses = {}
        for row in rows:
            if row["usage_status"] == "used":
                uses[row["mother_asset_id"]] = uses.get(row["mother_asset_id"], 0) + 1
        self.assertTrue(all(count <= 2 for count in uses.values()), uses)
        r11 = [row for row in rows if row["mother_asset_id"] == "R11"]
        self.assertTrue(r11)
        self.assertTrue(all(row["usage_status"] in {"used", "acquired_not_used"} for row in r11))
        if any(row["usage_status"] == "used" for row in r11):
            self.assertTrue(all(row["shot_id"] == "S01" for row in r11 if row["usage_status"] == "used"))

    def test_report_declares_non_final_scope(self):
        path = ROOT / "production-report.md"
        self.assertTrue(path.is_file(), "production-report.md 尚未实现")
        text = path.read_text(encoding="utf-8")
        self.assertIn("动态验证预览", text)
        self.assertIn("非成片", text)
        self.assertIn("formal_composition: false", text)
        self.assertIn("旁白：未加入", text)
        self.assertIn("字幕：未加入", text)

    def test_required_qa_evidence_exists(self):
        required = [
            "qa/preview-ffprobe.json", "qa/mechanism-a-ffprobe.json", "qa/mechanism-b-ffprobe.json",
            "qa/media-sha256.txt", "qa/decode-verification.json",
            "qa/shot-midpoints-contact-sheet.jpg", "qa/mechanism-a-contact-sheet.jpg",
            "qa/mechanism-b-contact-sheet.jpg", "qa/mechanism-b-continuity-contact-sheet.jpg",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), f"缺少 QA 证据：{relative}")


if __name__ == "__main__":
    unittest.main()
