import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "render_programmatic_shots.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("petrichor_renderer", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProgrammaticRendererTests(unittest.TestCase):
    def test_board_path_resolves_inside_repository(self):
        renderer = load_renderer()
        self.assertTrue(renderer.BOARD.is_dir())
        self.assertTrue((renderer.BOARD / "shot-plan-v1.yaml").is_file())

    def test_locked_frame_counts(self):
        renderer = load_renderer()
        expected = {"S01": 29, "S05": 87, "S07": 103, "S08": 70, "S12": 113}
        self.assertEqual(expected, renderer.SHOT_FRAMES)

    def test_visual_events_cover_each_shot_contract(self):
        renderer = load_renderer()
        required = {
            "S01": {"fall", "impact", "wet_spot"},
            "S05": {"surface", "descent", "pore_entry"},
            "S07": {"dormant", "water_wake", "geosmin"},
            "S08": {"approach", "impact"},
            "S12": {"same_composition", "wetting_spread", "rain"},
        }
        for shot_id, events in required.items():
            self.assertTrue(events.issubset(set(renderer.SHOT_EVENTS[shot_id])))


if __name__ == "__main__":
    unittest.main()
