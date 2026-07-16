from pathlib import Path
import hashlib
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from alpha_config import (  # noqa: E402
    FPS, WIDTH, HEIGHT, TOTAL_FRAMES, SHOTS, NARRATION_OFFSET_SECONDS,
    NARRATION_PATH, LOCKED_NARRATION_SHA256, SEEDANCE_HARD_TOTAL_CALLS,
    SEEDANCE_INHERITED_CALLS, SEEDANCE_ALLOWED_SHOT_GROUPS,
)


class AlphaContractTests(unittest.TestCase):
    def test_locked_frame_budget_is_cfr_24_and_thirteen_shots(self):
        self.assertEqual(FPS, 24)
        self.assertEqual((WIDTH, HEIGHT), (720, 1280))
        self.assertEqual(len(SHOTS), 13)
        self.assertEqual([shot.id for shot in SHOTS], [f"S{i:02d}" for i in range(1, 14)])
        self.assertEqual([shot.frames for shot in SHOTS], [29, 64, 44, 72, 87, 115, 103, 70, 73, 76, 109, 113, 168])
        self.assertEqual(sum(shot.frames for shot in SHOTS), TOTAL_FRAMES)
        self.assertEqual(TOTAL_FRAMES, 1123)

    def test_locked_narration_hash_and_offset_are_unchanged(self):
        self.assertEqual(NARRATION_OFFSET_SECONDS, 0.20)
        self.assertTrue(NARRATION_PATH.exists())
        self.assertEqual(hashlib.sha256(NARRATION_PATH.read_bytes()).hexdigest(), LOCKED_NARRATION_SHA256)

    def test_user_authorized_seedance_scope_is_explicit_and_bounded(self):
        self.assertEqual(SEEDANCE_INHERITED_CALLS, 4)
        self.assertEqual(SEEDANCE_HARD_TOTAL_CALLS, 10)
        self.assertEqual(SEEDANCE_ALLOWED_SHOT_GROUPS,
                         ("S01_SINGLE_DROP", "S01_SINGLE_DROP_R2", "MECHANISM_A", "MECHANISM_A_R2", "S12_FIRST_RAIN"))
