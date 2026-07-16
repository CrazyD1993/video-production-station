#!/usr/bin/env python3
"""Render the audible petrichor Alpha with deterministic repair shots."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from alpha_config import (
    ROOT, PROJECT, WIDTH, HEIGHT, FPS, TOTAL_FRAMES, TARGET_SECONDS,
    NARRATION_PATH, TIMESTAMPS_PATH, AMBIENCE_PATH, SHOTS,
)
from build_manifest import write_manifest
from render_mechanisms import render_overlay_rgba

WORK = ROOT / "work"
SHOTS_DIR = WORK / "shots"
V2 = PROJECT / "06_成片工程/雨后泥土味/director-remediation-v2-001"
BOARD = PROJECT / "06_成片工程/雨后泥土味/asset-board-v1"
PRIOR = PROJECT / "06_成片工程/雨后泥土味/director-remediation-pass-001"
AI = ROOT / "seedance/outputs"
ENCODE = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr"]


def run(*args: str) -> None:
    command = [str(arg) for arg in args]
    print("RUN", " ".join(command))
    subprocess.run(command, check=True)


def build_review_cues(data: dict) -> list[dict]:
    cues = []
    for sentence in data["response"]["data"]["sentences"]:
        cues.append({
            "start": float(sentence["startTime"]) + 0.20,
            "end": float(sentence["endTime"]) + 0.20,
            "text": sentence["text"].strip(),
        })
    return cues


def audio_filtergraph() -> str:
    return (
        "[1:a]adelay=200:all=1,apad=pad_dur=46.8,atrim=0:46.8,volume=0.94[n];"
        "[2:a]atrim=0:46.8,asetpts=PTS-STARTPTS,volume=0.08[a];"
        "[n][a]amix=inputs=2:duration=longest:normalize=0,atrim=0:46.8,"
        "aformat=sample_rates=48000:channel_layouts=stereo[m]"
    )


def _prepare() -> None:
    for directory in (WORK, SHOTS_DIR, WORK / "subtitle_png"):
        directory.mkdir(parents=True, exist_ok=True)
    for source in (
        AI / "S01-single-drop-candidate-r2.mp4",
        AI / "mechanism-a-candidate-r2.mp4",
        AI / "S12-first-rain-candidate.mp4",
    ):
        if not source.exists():
            raise FileNotFoundError(f"required licensed source missing: {source}")
    helper = WORK / "render_subtitle"
    env = os.environ.copy()
    env["CLANG_MODULE_CACHE_PATH"] = "/private/tmp/petrichor-clang-cache"
    subprocess.run([
        "clang", "-fobjc-arc", "-framework", "AppKit",
        str(ROOT / "render_subtitle.m"), "-o", str(helper),
    ], check=True, env=env)


def _render_overlay_sequence(name: str, count: int, kind: str) -> Path:
    output = WORK / f"{name}-overlay.mov"
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{HEIGHT}",
               "-r", str(FPS), "-i", "pipe:0", "-frames:v", str(count),
               "-c:v", "qtrle", "-pix_fmt", "argb", str(output)]
    print("RUN", " ".join(command))
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    for index in range(count):
        process.stdin.write(render_overlay_rgba(kind, index, count, WIDTH, HEIGHT))
    process.stdin.close()
    if process.wait() != 0:
        raise subprocess.CalledProcessError(process.returncode, command)
    return output


def _normalize(source: Path, output: Path, frames: int, grade: str) -> None:
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-vf", f"scale={WIDTH}:{HEIGHT}:flags=lanczos,{grade},fps={FPS},setpts=N/({FPS}*TB)",
        "-frames:v", str(frames), "-an", *ENCODE, str(output))


def _overlay(base: Path, overlay: Path, output: Path, frames: int) -> None:
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(base), "-i", str(overlay),
        "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto:shortest=1,format=yuv420p,setpts=N/(24*TB)[v]",
        "-map", "[v]", "-frames:v", str(frames), "-an", *ENCODE, str(output))


def render_s01() -> None:
    source = AI / "S01-single-drop-candidate-r2.mp4"
    output = SHOTS_DIR / "S01.mp4"
    vf = (
        "trim=start_frame=0:end_frame=36,setpts=0.805555556*(PTS-STARTPTS),fps=24,"
        "scale=720:1280:flags=lanczos,eq=saturation=0.68:contrast=1.08:brightness=-0.035,"
        "vignette=PI/7,setpts=N/(24*TB)"
    )
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-vf", vf, "-frames:v", "29", "-an", *ENCODE, str(output))


def render_retained() -> None:
    source_dir = V2 / "work/shots"
    grades = {
        "S02": "eq=saturation=0.66:contrast=1.06:brightness=-0.018",
        "S03": "eq=saturation=0.60:contrast=1.08:brightness=-0.025",
        "S04": "eq=saturation=0.70:contrast=1.05:brightness=-0.012",
        "S08": "eq=saturation=0.62:contrast=1.07:brightness=-0.020",
        "S13": "eq=saturation=0.52:contrast=1.04:brightness=-0.015",
    }
    frame_counts = {shot.id: shot.frames for shot in SHOTS}
    for shot_id, grade in grades.items():
        _normalize(source_dir / f"{shot_id}.mp4", SHOTS_DIR / f"{shot_id}.mp4", frame_counts[shot_id], grade)


def render_mechanism_a() -> None:
    count = 87 + 115 + 103
    base = WORK / "mechanism-a-base.mp4"
    overlay = _render_overlay_sequence("mechanism-a-completion", count, "mechanism-a-completion")
    factor = count / 241
    vf = (
        f"trim=start_frame=0:end_frame=241,setpts={factor:.9f}*(PTS-STARTPTS),fps=24,"
        "scale=720:1280:flags=lanczos,eq=saturation=0.62:contrast=1.08:brightness=-0.045,"
        "vignette=PI/8,setpts=N/(24*TB)"
    )
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(AI / "mechanism-a-candidate-r2.mp4"),
        "-vf", vf, "-frames:v", str(count), "-an", *ENCODE, str(base))
    final = ROOT / "mechanism-a-final.mp4"
    _overlay(base, overlay, final, count)
    offsets = {"S05": (0, 87), "S06": (87, 202), "S07": (202, 305)}
    for shot_id, (start, end) in offsets.items():
        run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(final),
            "-vf", f"trim=start_frame={start}:end_frame={end},setpts=N/(24*TB)",
            "-frames:v", str(end - start), "-an", *ENCODE, str(SHOTS_DIR / f"{shot_id}.mp4"))


def render_mechanism_b() -> None:
    pack = V2 / "mechanism-b-reference-pack-v2"
    s09_base = WORK / "S09-base.mp4"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-framerate", "24",
        "-i", str(pack / "b1-prestate-first-frame.png"),
        "-vf", "scale=720:1280:flags=lanczos,eq=saturation=0.68:contrast=1.05:brightness=-0.018,setpts=N/(24*TB)",
        "-frames:v", "73", "-an", *ENCODE, str(s09_base))
    s09_overlay = _render_overlay_sequence("S09", 73, "S09")
    _overlay(s09_base, s09_overlay, SHOTS_DIR / "S09.mp4", 73)

    _normalize(V2 / "work/shots/S10.mp4", SHOTS_DIR / "S10.mp4", 76,
               "eq=saturation=0.68:contrast=1.05:brightness=-0.018")

    s11_base = WORK / "S11-base.mp4"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-framerate", "24",
        "-i", str(pack / "surface-after.png"),
        "-vf", "scale=720:1280:flags=lanczos,eq=saturation=0.68:contrast=1.05:brightness=-0.018,setpts=N/(24*TB)",
        "-frames:v", "109", "-an", *ENCODE, str(s11_base))
    s11_overlay = _render_overlay_sequence("S11", 109, "S11")
    _overlay(s11_base, s11_overlay, SHOTS_DIR / "S11.mp4", 109)

    concat = WORK / "mechanism-b-concat.txt"
    concat.write_text("\n".join(
        f"file '{(SHOTS_DIR / f'{shot}.mp4').resolve()}'" for shot in ("S09", "S10", "S11")
    ) + "\n", encoding="utf-8")
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat), "-an", "-c:v", "copy", str(ROOT / "mechanism-b-final.mp4"))


def render_s12() -> None:
    source = AI / "S12-first-rain-candidate.mp4"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-vf", "trim=start_frame=0:end_frame=113,scale=720:1280:flags=lanczos,eq=saturation=0.60:contrast=1.06:brightness=-0.035,fps=24,setpts=N/(24*TB)",
        "-frames:v", "113", "-an", *ENCODE, str(SHOTS_DIR / "S12.mp4"))


def concat_shots() -> Path:
    concat = WORK / "alpha-concat.txt"
    concat.write_text("\n".join(
        f"file '{(SHOTS_DIR / f'{shot.id}.mp4').resolve()}'" for shot in SHOTS
    ) + "\n", encoding="utf-8")
    output = WORK / "alpha-silent.mp4"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat), "-an", "-c:v", "copy", str(output))
    return output


def _srt_time(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, rem = divmod(millis, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def _wrap(text: str, width: int = 18) -> list[str]:
    text = text.replace("\n", "").strip()
    if len(text) <= width:
        return [text]
    split = min(range(max(1, width - 5), min(len(text), width + 5)), key=lambda i: abs(i - width) + (0 if text[i-1] in "，；。？！" else 4))
    return [text[:split], text[split:]]


def write_subtitles() -> list[dict]:
    data = json.loads(TIMESTAMPS_PATH.read_text(encoding="utf-8"))
    cues = build_review_cues(data)
    srt = ROOT / "temporary-review-subtitles.srt"
    blocks = []
    png_dir = WORK / "subtitle_png"
    for number, cue in enumerate(cues, 1):
        lines = _wrap(cue["text"])
        blocks.append(f"{number}\n{_srt_time(cue['start'])} --> {_srt_time(cue['end'])}\n" + "\n".join(lines))
        png_path = png_dir / f"cue-{number:02d}.png"
        run(str(WORK / "render_subtitle"), str(png_path), *lines)
        cue["png"] = png_path
    srt.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    return cues


def burn_subtitles(video: Path, cues: list[dict]) -> Path:
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video)]
    for cue in cues:
        command.extend(["-loop", "1", "-framerate", "24", "-i", str(cue["png"])])
    filters = []
    current = "[0:v]"
    for index, cue in enumerate(cues, 1):
        output = f"[v{index}]"
        filters.append(f"{current}[{index}:v]overlay=0:0:format=auto:enable='between(t,{cue['start']:.3f},{cue['end']:.3f})'{output}")
        current = output
    command.extend(["-filter_complex", ";".join(filters), "-map", current,
                    "-frames:v", str(TOTAL_FRAMES), "-an", *ENCODE, str(WORK / "alpha-subtitled.mp4")])
    run(*command)
    return WORK / "alpha-subtitled.mp4"


def mux_audio(video: Path) -> None:
    output = ROOT / "petrichor-alpha-v1.mp4"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video),
        "-i", str(NARRATION_PATH), "-stream_loop", "-1", "-i", str(AMBIENCE_PATH),
        "-filter_complex", audio_filtergraph(), "-map", "0:v:0", "-map", "[m]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", f"{TARGET_SECONDS:.2f}", "-movflags", "+faststart", str(output))


def write_dependencies() -> None:
    write_manifest(ROOT / "asset-dependency-manifest.csv")
    text = f"""task_id: petrichor-alpha-finalization-001
timeline:
  nominal_seconds: {TARGET_SECONDS:.2f}
  video_frames: {TOTAL_FRAMES}
  fps: {FPS}
  video_track_seconds: {TOTAL_FRAMES/FPS:.6f}
audio:
  narration_path: {NARRATION_PATH.relative_to(PROJECT)}
  narration_sha256: {hashlib.sha256(NARRATION_PATH.read_bytes()).hexdigest()}
  narration_speed_ratio: 1.000
  narration_offset_seconds: 0.200
  ambience_path: {AMBIENCE_PATH.relative_to(PROJECT)}
  post_speed_change: false
generation:
  seedance_hard_total_calls: 10
  seedance_inherited_calls: 4
  paid_calls_this_round: 5
  seedance_total_calls_after_round: 9
  new_generated_model_assets: 5
  adopted_generated_assets: [G06, G08, G09]
scene_groups:
  mechanism_a_continuous:
    shots: [S05, S06, S07]
    underlying_sources: [G08]
  mechanism_b_continuous:
    shots: [S09, S10, S11]
    underlying_sources: [G02]
human_final_decision: pending
release_master_started: false
"""
    (ROOT / "dependencies.yaml").write_text(text, encoding="utf-8")


def main() -> None:
    _prepare()
    render_s01()
    render_retained()
    render_mechanism_a()
    render_mechanism_b()
    render_s12()
    silent = concat_shots()
    cues = write_subtitles()
    subtitled = burn_subtitles(silent, cues)
    mux_audio(subtitled)
    write_dependencies()
    print(ROOT / "petrichor-alpha-v1.mp4")


if __name__ == "__main__":
    main()
