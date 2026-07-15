import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "render_remediation_v2.py"


def load_renderer(testcase):
    testcase.assertTrue(MODULE.is_file(), "render_remediation_v2.py 尚未实现")
    spec = importlib.util.spec_from_file_location("petrichor_v2_renderer", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RenderPlanTests(unittest.TestCase):
    def test_mechanism_a_uses_one_space_and_progressive_events(self):
        renderer = load_renderer(self)
        self.assertEqual(
            {"S05": "soil-column-R05-v2", "S06": "soil-column-R05-v2", "S07": "soil-column-R05-v2"},
            renderer.SCENE_IDS,
        )
        required = {
            "S05": {"surface", "traceable_infiltration", "enter_soil"},
            "S06": {"free_particles", "adsorption", "attached_particles"},
            "S07": {"water_arrival", "subtle_microbe_motion", "geosmin"},
            "S08": {"approach", "credible_impact", "pore_entry"},
            "S09": {"water_enters_pore", "air_compresses", "air_surrounded", "same_bubble_forms", "rise_begins"},
            "S10": {"same_bubble_rises", "surface_approach"},
            "S11": {"surface_contact", "film_pop", "fine_aerosol", "rapid_fade"},
            "S12": {"crack_led_wetting", "asynchronous_darkening", "multiple_impacts"},
        }
        for shot_id, events in required.items():
            self.assertTrue(events.issubset(set(renderer.SHOT_EVENTS[shot_id])))

    def test_disallowed_visual_language_is_absent(self):
        renderer = load_renderer(self)
        disallowed = {"white_flat_drop", "oval_wet_mark", "large_arrow", "hud", "glow_microbes", "circular_mask"}
        for events in renderer.SHOT_EVENTS.values():
            self.assertFalse(disallowed.intersection(events))

    def test_g01_is_discarded_and_g02_speed_is_within_eight_percent(self):
        renderer = load_renderer(self)
        self.assertNotIn("G01", renderer.ALLOWED_GENERATED_ASSETS)
        self.assertNotIn("B1_S09-candidate-1.mp4", renderer.ALLOWED_GENERATED_ASSETS)
        self.assertIn("B2_S10_S11-candidate-2.mp4", renderer.ALLOWED_GENERATED_ASSETS)
        self.assertGreaterEqual(renderer.S10_SPEED_RATIO, 0.92)
        self.assertLessEqual(renderer.S10_SPEED_RATIO, 1.08)

    def test_reference_pack_declares_exact_bridge_frame(self):
        renderer = load_renderer(self)
        reference = ROOT / "mechanism-b-reference-pack-v2/reference-pack.json"
        self.assertTrue(reference.is_file(), "机制 B 参考包尚未实现")
        self.assertEqual(renderer.G02_BRIDGE_FRAME_SHA256, renderer.reference_pack_hash(reference))

    def test_programmatic_frames_are_vertical_and_dynamic(self):
        renderer = load_renderer(self)
        self.assertTrue(hasattr(renderer, "render_frame"), "程序化逐帧渲染接口尚未实现")
        for shot_id in ["S05", "S06", "S07", "S08", "S11", "S12"]:
            first = renderer.render_frame(shot_id, 0, 25)
            middle = renderer.render_frame(shot_id, 12, 25)
            last = renderer.render_frame(shot_id, 24, 25)
            self.assertEqual((540, 960), first.size)
            self.assertEqual((540, 960), last.size)
            if shot_id == "S08":
                self.assertNotEqual(first.tobytes(), middle.tobytes(), "S08 缺少撞击过程")
            else:
                self.assertNotEqual(first.tobytes(), last.tobytes(), f"{shot_id} 缺少动态变化")

    def test_s11_ends_closer_to_post_pop_surface_than_intact_bubble(self):
        renderer = load_renderer(self)
        from PIL import ImageChops, ImageStat
        last = renderer.render_frame("S11", 24, 25).crop((185, 170, 355, 370))
        contact = renderer._cover(ROOT / "mechanism-b-reference-pack-v2/surface-contact.png").crop((185, 170, 355, 370))
        after = renderer._cover(ROOT / "mechanism-b-reference-pack-v2/surface-after.png").crop((185, 170, 355, 370))
        def rms(a, b):
            stat = ImageStat.Stat(ImageChops.difference(a, b))
            return sum(value * value for value in stat.rms) ** 0.5
        self.assertLess(rms(last, after), rms(last, contact))

    def test_s08_ends_in_prebubble_geometry_for_s09_handoff(self):
        renderer = load_renderer(self)
        from PIL import ImageChops, ImageStat
        crop = (205, 500, 335, 825)
        last = renderer.render_frame("S08", 24, 25).crop(crop)
        bridge = renderer._cover(ROOT / "mechanism-b-reference-pack-v2/bridge-start.png").crop(crop)
        prestate = renderer._cover(ROOT / "mechanism-b-reference-pack-v2/b1-prestate-first-frame.png").crop(crop)
        def rms(a, b):
            stat = ImageStat.Stat(ImageChops.difference(a, b))
            return sum(value * value for value in stat.rms) ** 0.5
        self.assertLess(rms(last, prestate), rms(last, bridge))
        self.assertLess(rms(last, prestate), 5.0, "S08 末帧必须回到无气泡、无人工线条的 S09 首帧几何")


if __name__ == "__main__":
    unittest.main()
