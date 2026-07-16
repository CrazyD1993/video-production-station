from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from alpha_config import TIMESTAMPS_PATH, NARRATION_OFFSET_SECONDS  # noqa: E402
from render_alpha import build_review_cues, audio_filtergraph  # noqa: E402


class AudioSubtitleTests(unittest.TestCase):
    def test_review_cues_use_locked_sentence_text_and_shift_only_020_seconds(self):
        data = json.loads(TIMESTAMPS_PATH.read_text(encoding="utf-8"))
        sentences = data["response"]["data"]["sentences"]
        cues = build_review_cues(data)
        self.assertEqual(len(cues), len(sentences))
        for cue, sentence in zip(cues, sentences):
            self.assertEqual(cue["text"], sentence["text"].strip())
            self.assertAlmostEqual(cue["start"], sentence["startTime"] + NARRATION_OFFSET_SECONDS, places=6)
            self.assertAlmostEqual(cue["end"], sentence["endTime"] + NARRATION_OFFSET_SECONDS, places=6)

    def test_audio_filtergraph_has_no_time_stretch_or_dynamics_processing(self):
        graph = audio_filtergraph().lower()
        for forbidden in ("atempo", "asetrate", "rubberband", "loudnorm", "acompressor", "alimiter"):
            self.assertNotIn(forbidden, graph)
        self.assertIn("adelay=200", graph)
        self.assertIn("atrim=0:46.8", graph)

    def test_render_pipeline_does_not_depend_on_missing_svg_decoder(self):
        source = (ROOT / "render_alpha.py").read_text(encoding="utf-8")
        self.assertIn("render_overlay_rgba", source)
        self.assertNotIn('directory / "%04d.svg"', source)
        self.assertNotIn('"-i", str(svg_path)', source)
