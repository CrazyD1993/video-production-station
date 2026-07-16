from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from render_mechanisms import (  # noqa: E402
    EVENT_SPEC, rupture_frame_count, s12_palette, s12_final_dry_fraction,
    mechanism_a_state, mechanism_a_svg, mechanism_b_state, mechanism_b_svg,
    s12_svg, BUBBLE_ANCHOR,
    render_overlay_rgba,
)


class RendererContractTests(unittest.TestCase):
    def test_required_event_phases_are_explicit(self):
        self.assertEqual(EVENT_SPEC["S01"], ("fall", "contact", "splash_or_wet_response"))
        self.assertEqual(EVENT_SPEC["S05"][-1], "infiltration_continues")
        self.assertEqual(EVENT_SPEC["S06"], ("film_transport", "adsorption"))
        self.assertEqual(EVENT_SPEC["S07"], ("water_arrival", "local_mycelia_wake"))
        self.assertEqual(EVENT_SPEC["S09"][0], "visible_air_cavity")
        self.assertEqual(EVENT_SPEC["S10"], ("same_bubble_rises_at_1.000",))
        self.assertEqual(EVENT_SPEC["S11"], ("surface_contact", "film_rupture", "fine_droplets", "surface_rebound"))

    def test_rupture_is_two_to_four_frames(self):
        self.assertTrue(2 <= rupture_frame_count() <= 4)

    def test_s12_uses_no_orange_glow_and_retains_dry_soil(self):
        for red, green, blue in s12_palette():
            self.assertFalse(red > green * 1.45 and red > blue * 1.8)
        self.assertTrue(0.20 <= s12_final_dry_fraction() <= 0.65)

    def test_mechanism_a_is_one_continuous_monotonic_scene_without_large_labels(self):
        states = [mechanism_a_state(i, 305) for i in (0, 86, 87, 201, 202, 304)]
        self.assertEqual([s["water_front"] for s in states], sorted(s["water_front"] for s in states))
        svg = mechanism_a_svg(180, 305)
        self.assertIn("<path", svg)
        self.assertNotIn("font-size=\"48", svg)
        self.assertNotIn("HUD", svg)

    def test_mechanism_b_closes_into_the_same_anchor_and_ruptures_visibly(self):
        first = mechanism_b_state("S09", 0, 73)
        last = mechanism_b_state("S09", 72, 73)
        self.assertEqual(first["phase"], "cavity")
        self.assertGreater(first["rx"], last["rx"])
        self.assertEqual((last["cx"], last["cy"]), BUBBLE_ANCHOR)
        rupture_svgs = [mechanism_b_svg("S11", i, 109) for i in range(109)]
        self.assertEqual(sum("data-rupture=\"true\"" in svg for svg in rupture_svgs), rupture_frame_count())
        self.assertTrue(any("data-droplet" in svg for svg in rupture_svgs))

    def test_s12_svg_is_cool_and_ends_with_partial_not_full_wetting(self):
        first = s12_svg(0, 113)
        last = s12_svg(112, 113)
        self.assertNotIn("#ff", last.lower())
        self.assertNotIn("orange", last.lower())
        self.assertLess(len(first), len(last))
        self.assertIn("data-dry-fraction=\"0.34\"", last)

    def test_overlay_has_native_rgba_fallback_without_svg_decoder(self):
        rgba = render_overlay_rgba("S09", 36, 73, width=72, height=128)
        self.assertEqual(len(rgba), 72 * 128 * 4)
        self.assertGreater(max(rgba[3::4]), 0)

    def test_render_pipeline_uses_objc_appkit_not_swift_or_svg_decoder(self):
        text = (ROOT / "render_alpha.py").read_text(encoding="utf-8")
        self.assertNotIn(".svg", text)
        self.assertIn("render_overlay_rgba", text)
        self.assertIn("render_subtitle.m", text)
        self.assertIn("clang", text)
        self.assertNotIn("swiftc", text)

    def test_final_renderer_uses_diagnosis_selected_seedance_candidates(self):
        text = (ROOT / "render_alpha.py").read_text(encoding="utf-8")
        self.assertIn("S01-single-drop-candidate-r2.mp4", text)
        self.assertIn("mechanism-a-candidate-r2.mp4", text)
        self.assertIn("S12-first-rain-candidate.mp4", text)
        self.assertIn("mechanism-a-completion", text)
