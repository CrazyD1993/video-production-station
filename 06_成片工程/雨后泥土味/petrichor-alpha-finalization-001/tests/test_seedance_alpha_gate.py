from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "seedance"))

from seedance_alpha_client import (  # noqa: E402
    HARD_TOTAL_CALLS, INHERITED_CALLS, MAX_NEW_CALLS, PROMPTS,
    assert_budget, build_request, BudgetExceeded,
)


class SeedanceAlphaGateTests(unittest.TestCase):
    def test_user_override_sets_total_cap_ten_with_six_remaining(self):
        self.assertEqual(INHERITED_CALLS, 4)
        self.assertEqual(HARD_TOTAL_CALLS, 10)
        self.assertEqual(MAX_NEW_CALLS, 6)

    def test_budget_blocks_at_ten_and_allows_before_ten(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "log.json"
            path.write_text(json.dumps({"total_calls": 9, "new_calls": 5}), encoding="utf-8")
            assert_budget(path)
            path.write_text(json.dumps({"total_calls": 10, "new_calls": 6}), encoding="utf-8")
            with self.assertRaises(BudgetExceeded):
                assert_budget(path)

    def test_s01_prompt_diagnoses_and_fixes_event_ambiguity(self):
        prompt = PROMPTS["S01_SINGLE_DROP"].lower()
        for phrase in ("single water drop", "dry loose soil", "falling", "impact",
                       "soil grains", "splash", "dark wet spot", "first 1.2 seconds"):
            self.assertIn(phrase, prompt)

    def test_s01_retry_turns_model_omission_into_timed_visible_motion(self):
        prompt = PROMPTS["S01_SINGLE_DROP_R2"].lower()
        for phrase in ("0.55-0.75 seconds", "water crown", "0.75-1.10 seconds",
                       "soil grains", "travel upward", "must not simply vanish",
                       "four distinct continuous stages"):
            self.assertIn(phrase, prompt)

    def test_mechanism_a_prompt_requires_one_scene_and_three_visible_actions(self):
        prompt = PROMPTS["MECHANISM_A"].lower()
        for phrase in ("one continuous", "fixed camera", "infiltration", "adsorb",
                       "mycelia", "no text", "no neon"):
            self.assertIn(phrase, prompt)

    def test_mechanism_a_retry_corrects_bead_pack_and_blue_channel_failure(self):
        prompt = PROMPTS["MECHANISM_A_R2"].lower()
        for phrase in ("supplied real root-and-soil first frame", "preserve the exact natural soil texture",
                       "0-3 seconds", "3-7 seconds", "7-10 seconds", "visibly attach",
                       "no uniform round pellets", "no blue channel", "no white wire"):
            self.assertIn(phrase, prompt)

    def test_s12_prompt_forbids_old_orange_glow_failure(self):
        prompt = PROMPTS["S12_FIRST_RAIN"].lower()
        for phrase in ("same cracked soil", "along crack edges", "irregularly",
                       "dry and wet areas coexist", "no orange", "no glow"):
            self.assertIn(phrase, prompt)

    def test_requests_are_seedance_fast_vertical_without_audio(self):
        payload = build_request(PROMPTS["S01_SINGLE_DROP"], 5)
        self.assertEqual(payload["model"], "doubao-seedance-2-0-fast-260128")
        self.assertEqual(payload["ratio"], "9:16")
        self.assertEqual(payload["resolution"], "720p")
        self.assertFalse(payload["generate_audio"])


if __name__ == "__main__":
    unittest.main()
