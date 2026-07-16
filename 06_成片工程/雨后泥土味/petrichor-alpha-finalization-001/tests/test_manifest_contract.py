from pathlib import Path
import csv
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_manifest import build_rows, write_manifest, FIELDNAMES  # noqa: E402


class ManifestContractTests(unittest.TestCase):
    def test_manifest_recursively_discloses_scene_groups_and_underlying_sources(self):
        rows = build_rows()
        self.assertEqual({row["shot_id"] for row in rows if row["usage_status"] == "used"},
                         {f"S{i:02d}" for i in range(1, 14)})
        by_shot = {sid: [r for r in rows if r["shot_id"] == sid] for sid in {r["shot_id"] for r in rows}}
        self.assertEqual({r["underlying_source_id"] for sid in ("S05", "S06", "S07") for r in by_shot[sid]}, {"G08"})
        self.assertEqual({r["scene_group"] for sid in ("S05", "S06", "S07") for r in by_shot[sid]}, {"mechanism_a_continuous"})
        self.assertEqual({r["scene_group"] for sid in ("S09", "S10", "S11") for r in by_shot[sid]}, {"mechanism_b_continuous"})
        g02 = [r for r in rows if r["underlying_source_id"] == "G02"]
        self.assertEqual({r["shot_id"] for r in g02}, {"S09", "S10", "S11"})
        self.assertEqual({r["true_reuse_count"] for r in g02}, {"3"})
        out = ROOT / "work" / "test-manifest.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        write_manifest(out)
        with out.open(encoding="utf-8", newline="") as f:
            parsed = list(csv.reader(f))
        self.assertTrue(all(len(row) == len(FIELDNAMES) for row in parsed))
        out.unlink()

    def test_every_used_external_source_has_license_and_timecode(self):
        for row in build_rows():
            self.assertTrue(row["license_type"])
            self.assertTrue(row["license_url"])
            self.assertTrue(row["license_evidence_path"])
            self.assertTrue(row["source_timecode"])
            self.assertTrue(row["use_timecode"])
            self.assertGreater(float(row["speed_ratio"]), 0)

    def test_r14_has_direct_license_evidence_and_g03_is_not_misaligned(self):
        rows = build_rows()
        r14 = [r for r in rows if r["underlying_source_id"] == "R14"]
        self.assertTrue(r14)
        self.assertTrue(all("mixkit" in r["license_url"].lower() for r in r14))
        self.assertTrue(all((ROOT / r["license_evidence_path"]).exists() for r in r14))
        g03 = [r for r in rows if r["underlying_source_id"] == "G03"]
        self.assertTrue(g03 and all(r["usage_status"] == "acquired_not_used" for r in g03))
        self.assertTrue(all(r["target_duration"] == "0.000" for r in g03))

    def test_new_seedance_dependencies_and_rejections_are_explicit(self):
        rows = build_rows()
        by_id = {source: [r for r in rows if r["underlying_source_id"] == source]
                 for source in ("G05", "G06", "G07", "G08", "G09")}
        self.assertEqual({r["shot_id"] for r in by_id["G06"]}, {"S01"})
        self.assertEqual({r["shot_id"] for r in by_id["G08"]}, {"S05", "S06", "S07"})
        self.assertEqual({r["shot_id"] for r in by_id["G09"]}, {"S12"})
        self.assertTrue(all(r["usage_status"] == "acquired_not_used" for source in ("G05", "G07") for r in by_id[source]))
