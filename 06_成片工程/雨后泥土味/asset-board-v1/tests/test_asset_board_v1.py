import csv
import importlib.util
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "build_asset_board.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_asset_board", BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AssetBoardContractTests(unittest.TestCase):
    def test_locked_timeline_and_asset_policy(self):
        module = load_builder()
        self.assertEqual(len(module.SHOTS), 13)
        self.assertEqual(
            [(s["start"], s["end"]) for s in module.SHOTS],
            [
                (0.00, 1.20), (1.20, 3.85), (3.85, 5.69),
                (5.69, 8.70), (8.70, 12.32), (12.32, 17.10),
                (17.10, 21.38), (21.38, 24.30), (24.30, 27.35),
                (27.35, 30.50), (30.50, 35.06), (35.06, 39.77),
                (39.77, 46.80),
            ],
        )
        acquired_real = {
            row["asset_id"] for row in module.ASSETS
            if row["source_category"] == "real_external" and row["acquired"] == "yes"
        }
        self.assertGreaterEqual(len(acquired_real), 7)
        usage = Counter()
        for shot in module.SHOTS:
            for asset_id in shot["asset_ids"]:
                if asset_id.startswith("R"):
                    usage[asset_id] += 1
        self.assertTrue(all(count <= 2 for count in usage.values()))
        self.assertEqual(module.PAID_MODEL_CALLS, 0)

    def test_generated_files_and_manifest_columns(self):
        module = load_builder()
        module.build_all()
        required = [
            "shot-plan-v1.yaml",
            "asset-manifest-v1.csv",
            "missing-assets-v1.md",
            "seedance-prompts-draft-v1.md",
            "petrichor-asset-board-v1.svg",
            "petrichor-asset-board-v1.jpg",
            "petrichor-asset-board-v1.pdf",
            "petrichor-asset-board-preview-v1.mp4",
            "mechanism/mechanism-a-geosmin-v1.svg",
            "mechanism/mechanism-b-aerosol-v1.svg",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).is_file(), rel)
        with (ROOT / "asset-manifest-v1.csv").open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        expected = {
            "asset_id", "filename", "original_page_url", "author_uploader",
            "platform", "license_type", "license_url", "download_date",
            "allowed_use", "shot_ids", "source_category", "acquired",
            "local_path", "review_note",
        }
        self.assertEqual(set(rows[0]), expected)
        for row in rows:
            if row["source_category"] == "real_external":
                for field in expected - {"review_note"}:
                    self.assertTrue(row[field].strip(), f"{row['asset_id']}:{field}")

    def test_preview_if_present_is_at_most_twenty_seconds(self):
        preview = ROOT / "petrichor-asset-board-preview-v1.mp4"
        if not preview.exists():
            self.skipTest("preview is rendered after static assets")
        duration = subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(preview),
            ],
            text=True,
        )
        self.assertLessEqual(float(duration), 20.0)


if __name__ == "__main__":
    unittest.main()
