"""Immutable contract for petrichor Alpha finalization."""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
WIDTH, HEIGHT, FPS = 720, 1280, 24
TOTAL_FRAMES = 1123
TARGET_SECONDS = 46.80
VIDEO_SECONDS = TOTAL_FRAMES / FPS
NARRATION_OFFSET_SECONDS = 0.20

NARRATION_PATH = PROJECT / "06_成片工程/雨后泥土味/tts-natural/petrichor-narration-natural.wav"
TIMESTAMPS_PATH = PROJECT / "06_成片工程/雨后泥土味/tts-natural/petrichor-narration-natural.timestamps.json"
AMBIENCE_PATH = PROJECT / "06_成片工程/雨后泥土味/director-remediation-pass-001/work/temporary-validation-ambience.wav"
LOCKED_NARRATION_SHA256 = "914a1728f12c87bff8f6f2fe607ab1708a5559a58ab0abb5d18cdb214a5f948e"
SEEDANCE_HARD_TOTAL_CALLS = 10
SEEDANCE_INHERITED_CALLS = 4
SEEDANCE_ALLOWED_SHOT_GROUPS = ("S01_SINGLE_DROP", "S01_SINGLE_DROP_R2", "MECHANISM_A", "MECHANISM_A_R2", "S12_FIRST_RAIN")


@dataclass(frozen=True)
class Shot:
    id: str
    start: float
    end: float
    frames: int


SHOTS = (
    Shot("S01", 0.00, 1.20, 29), Shot("S02", 1.20, 3.85, 64),
    Shot("S03", 3.85, 5.69, 44), Shot("S04", 5.69, 8.70, 72),
    Shot("S05", 8.70, 12.32, 87), Shot("S06", 12.32, 17.10, 115),
    Shot("S07", 17.10, 21.38, 103), Shot("S08", 21.38, 24.30, 70),
    Shot("S09", 24.30, 27.35, 73), Shot("S10", 27.35, 30.50, 76),
    Shot("S11", 30.50, 35.06, 109), Shot("S12", 35.06, 39.77, 113),
    Shot("S13", 39.77, 46.80, 168),
)

NEW_SOURCE_PATHS = {
    "R15": Path("/private/tmp/petrichor-alpha-sources/soil-profile.mp4"),
    "R16": Path("/private/tmp/petrichor-alpha-sources/muddy-drop.mp4"),
}

SHOT_FRAME_RANGES = {}
_cursor = 0
for _shot in SHOTS:
    SHOT_FRAME_RANGES[_shot.id] = (_cursor, _cursor + _shot.frames)
    _cursor += _shot.frames
assert _cursor == TOTAL_FRAMES
