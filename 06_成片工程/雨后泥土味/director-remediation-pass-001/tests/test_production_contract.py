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
    def test_shot_status_has_locked_timeline_and_allowed_states(self):
        text = (ROOT / "shot-status.yaml").read_text(encoding="utf-8")
        blocks = re.findall(
            r"- id: (S\d+)\n\s+start: ([0-9.]+)\n\s+end: ([0-9.]+)\n\s+status: (\w+)",
            text,
        )
        self.assertEqual(13, len(blocks))
        self.assertEqual(list(EXPECTED), [item[0] for item in blocks])
        for shot_id, start, end, status in blocks:
            self.assertEqual(EXPECTED[shot_id], (float(start), float(end)))
            self.assertIn(status, {"done", "partial", "blocked"})

    def test_seedance_log_obeys_scope_and_budget(self):
        data = json.loads((ROOT / "seedance/call-log.json").read_text(encoding="utf-8"))
        self.assertLessEqual(data["total_calls"], 4)
        self.assertEqual(data["total_calls"], len(data["calls"]))
        for call in data["calls"]:
            self.assertEqual("doubao-seedance-2-0-fast-260128", call["model"])
            self.assertIn(call["shot_group"], {"B1_S09", "B2_S10_S11"})
            self.assertEqual("9:16", call["ratio"])
            self.assertEqual("720p", call["resolution"])
            self.assertFalse(call["generate_audio"])
            for key in ["task_id", "status", "output_path", "cost", "decision_reason"]:
                self.assertIn(key, call)

    def test_preview_is_non_final_and_has_locked_specs(self):
        preview = ROOT / "petrichor-director-remediation-preview-v1.mp4"
        self.assertTrue(preview.is_file())
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_streams", "-show_format",
            "-of", "json", str(preview),
        ], check=True, capture_output=True, text=True)
        data = json.loads(probe.stdout)
        video = next(item for item in data["streams"] if item["codec_type"] == "video")
        self.assertEqual((540, 960), (video["width"], video["height"]))
        self.assertEqual("24/1", video["r_frame_rate"])
        self.assertAlmostEqual(46.80, float(data["format"]["duration"]), delta=0.06)
        report = (ROOT / "production-report.md").read_text(encoding="utf-8")
        self.assertIn("动态验证预览", report)
        self.assertIn("非成片", report)
        self.assertIn("formal_composition: false", report)


if __name__ == "__main__":
    unittest.main()
