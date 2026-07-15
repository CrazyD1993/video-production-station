#!/usr/bin/env python3
"""Build the locked 46.80 s director remediation validation preview (not a final film)."""

from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import struct
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
BOARD = PROJECT / "06_成片工程" / "雨后泥土味" / "asset-board-v1"
WORK = ROOT / "work"
QA = ROOT / "qa"
PREVIEW = ROOT / "petrichor-director-remediation-preview-v1.mp4"
WIDTH, HEIGHT, FPS = 540, 960, 24
FONT_PATH = Path("/System/Library/Fonts/STHeiti Light.ttc")

SHOTS = [
    ("S01", 0.00, 1.20, "第一滴：落下 · 撞击 · 湿斑"),
    ("S02", 1.20, 3.85, "叶片 · 石板 · 泥土"),
    ("S03", 3.85, 5.69, "雨后的泥土味，从哪儿来？"),
    ("S04", 5.69, 8.70, "叶尖水滴落下"),
    ("S05", 8.70, 12.32, "从地表进入土壤"),
    ("S06", 12.32, 17.10, "植物物质被土粒吸附"),
    ("S07", 17.10, 21.38, "土臭素 Geosmin"),
    ("S08", 21.38, 24.30, "雨滴接近与撞击"),
    ("S09", 24.30, 27.35, "困住空气"),
    ("S10", 27.35, 30.50, "形成气泡"),
    ("S11", 30.50, 35.06, "释放气溶胶"),
    ("S12", 35.06, 39.77, "同一块土地：干 → 湿"),
    ("S13", 39.77, 46.80, "土地重新呼吸"),
]


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def fit_filter(extra: str = "") -> str:
    base = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT},fps={FPS},format=yuv420p"
    )
    return f"{base},{extra}" if extra else base


def make_overlay(shot_id: str, start: float, end: float, label: str) -> Path:
    target = WORK / "overlays" / f"{shot_id}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    font_small = ImageFont.truetype(str(FONT_PATH), 18)
    font_label = ImageFont.truetype(str(FONT_PATH), 23)
    draw.rounded_rectangle((18, 18, 522, 58), radius=12, fill=(10, 12, 11, 166))
    draw.text((32, 28), "总导演整改动态验证预览 · 非成片", font=font_small, fill=(240, 236, 224, 245))
    draw.rounded_rectangle((18, 855, 522, 934), radius=14, fill=(10, 12, 11, 180))
    draw.text((32, 869), f"{shot_id}  {start:05.2f}—{end:05.2f}", font=font_small, fill=(202, 191, 166, 255))
    draw.text((32, 898), label, font=font_label, fill=(248, 246, 238, 255))
    canvas.save(target)
    return target


def render_source(source: Path, output: Path, duration: float, overlay: Path,
                  start: float = 0.0, image: bool = False, speed: float = 1.0) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-y", "-loglevel", "error"]
    if image:
        command += ["-loop", "1"]
    elif start:
        command += ["-ss", f"{start:.3f}"]
    command += ["-i", str(source), "-loop", "1", "-i", str(overlay)]
    video_chain = fit_filter()
    if speed != 1.0:
        video_chain += f",setpts={speed:.6f}*PTS"
    command += [
        "-filter_complex", f"[0:v]{video_chain}[base];[base][1:v]overlay=0:0:format=auto[out]",
        "-map", "[out]", "-an", "-t", f"{duration:.3f}", "-r", str(FPS),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        str(output),
    ]
    run(command)


def concat_parts(parts: list[Path], output: Path, duration: float | None = None) -> None:
    listing = WORK / f"{output.stem}-concat.txt"
    listing.write_text("".join(f"file '{part.resolve()}'\n" for part in parts), encoding="utf-8")
    command = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
    ]
    if duration is not None:
        command += ["-t", f"{duration:.3f}"]
    command.append(str(output))
    run(command)


def render_montage(shot_id: str, sources: list[tuple[Path, bool]], duration: float,
                   overlay: Path, output: Path) -> None:
    each = duration / len(sources)
    parts = []
    for index, (source, is_image) in enumerate(sources):
        part = WORK / "montage" / f"{shot_id}-{index}.mp4"
        render_source(source, part, each, overlay, image=is_image)
        parts.append(part)
    concat_parts(parts, output, duration)


def make_temp_audio(output: Path, duration: float = 46.80, rate: int = 48000) -> None:
    """Low-level non-final ambience, with one drop, underground body and bubble pop."""
    rng = random.Random(20260715)
    total = int(duration * rate)
    samples = []
    for index in range(total):
        t = index / rate
        rain_gain = 0.008 if t < 21 else (0.004 if t < 35 else 0.012)
        open_gain = max(0.0, min(1.0, (t - 39.5) / 4.5))
        value = rng.uniform(-1.0, 1.0) * rain_gain
        if 21 <= t <= 35:
            value += 0.007 * math.sin(2 * math.pi * 62 * t)
        value += open_gain * 0.004 * math.sin(2 * math.pi * 410 * t)
        for event, amp, decay, freq in [(0.55, 0.45, 55, 1180), (30.62, 0.36, 75, 760)]:
            dt = t - event
            if 0 <= dt < 0.12:
                value += amp * math.exp(-decay * dt) * math.sin(2 * math.pi * freq * dt)
        value = max(-0.95, min(0.95, value))
        samples.append(struct.pack("<h", int(value * 32767)))
    with wave.open(str(output), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(b"".join(samples))


def render() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)

    overlays = {sid: make_overlay(sid, start, end, label) for sid, start, end, label in SHOTS}
    p = ROOT / "programmatic"
    real = BOARD / "assets" / "real-proxy"
    new_real = ROOT / "assets" / "real-proxy"
    seedance = ROOT / "seedance" / "outputs"
    segments: list[Path] = []

    for shot_id, start, end, _label in SHOTS:
        duration = end - start
        output = WORK / "shots" / f"{shot_id}.mp4"
        overlay = overlays[shot_id]
        if shot_id in {"S01", "S05", "S07", "S08", "S12"}:
            render_source(p / f"{shot_id}.mp4", output, duration, overlay)
        elif shot_id == "S02":
            render_montage(shot_id, [
                (real / "R01-pexels-13444705-rain-leaves-proxy.mp4", False),
                (real / "R09-pexels-2905149-wet-cobblestone.jpg", True),
                (real / "R03-pexels-7234789-wet-soil-proxy.mp4", False),
            ], duration, overlay, output)
        elif shot_id == "S03":
            render_source(real / "R04-pexels-7232905-wet-soil-macro.jpg", output, duration, overlay, image=True)
        elif shot_id == "S04":
            render_source(real / "R02-pexels-5210312-leaf-droplet-proxy.mp4", output, duration, overlay)
        elif shot_id == "S06":
            render_montage(shot_id, [
                (real / "R05-pexels-12763908-tree-roots-soil.jpg", True),
                (real / "R06-pexels-28922207-forest-floor.jpg", True),
            ], duration, overlay, output)
        elif shot_id == "S09":
            render_source(seedance / "B1_S09-candidate-1.mp4", output, duration, overlay)
        elif shot_id in {"S10", "S11"}:
            # One B2 candidate is slowed uniformly to fit locked S10+S11 = 7.71 s.
            speed_factor = 7.71 / 5.041667
            b2_long = WORK / "B2-locked-7.71.mp4"
            if not b2_long.exists():
                render_source(seedance / "B2_S10_S11-candidate-2.mp4", b2_long, 7.71,
                              make_overlay("B2", 27.35, 35.06, "机制 B 连续候选"), speed=speed_factor)
            source_offset = 0.0 if shot_id == "S10" else 3.15
            render_source(b2_long, output, duration, overlay, start=source_offset)
        elif shot_id == "S13":
            render_montage(shot_id, [
                (new_real / "R13-pexels-32679329-rain-leaves-forest-proxy.mp4", False),
                (new_real / "R12-pexels-32675101-misty-forest-motion-proxy.mp4", False),
            ], duration, overlay, output)
        else:
            raise AssertionError(shot_id)
        segments.append(output)

    silent = WORK / "preview-silent.mp4"
    concat_parts(segments, silent, 46.80)
    audio = WORK / "temporary-validation-ambience.wav"
    make_temp_audio(audio)
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-t", "46.80", "-movflags", "+faststart", str(PREVIEW),
    ])

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(PREVIEW)
    ], check=True, capture_output=True, text=True)
    (QA / "preview-ffprobe.json").write_text(probe.stdout, encoding="utf-8")
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(PREVIEW),
        "-vf", "fps=1/4.68,scale=180:320,tile=5x2", "-frames:v", "1",
        str(QA / "preview-contact-sheet.jpg"),
    ])
    midpoint_dir = QA / "shot-midpoints"
    midpoint_dir.mkdir(parents=True, exist_ok=True)
    for shot_id, start, end, _label in SHOTS:
        run([
            "ffmpeg", "-y", "-loglevel", "error", "-ss", f"{(start + end) / 2:.3f}",
            "-i", str(PREVIEW), "-frames:v", "1", "-q:v", "2",
            str(midpoint_dir / f"{shot_id}.jpg"),
        ])
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-pattern_type", "glob", "-framerate", "1",
        "-i", str(midpoint_dir / "S*.jpg"),
        "-vf", "scale=135:240,tile=4x4:padding=4:margin=4:color=0x151713", "-frames:v", "1",
        str(QA / "shot-midpoints-contact-sheet.jpg"),
    ])
    digest = hashlib.sha256(PREVIEW.read_bytes()).hexdigest()
    (QA / "preview-sha256.txt").write_text(f"{digest}  {PREVIEW.name}\n", encoding="utf-8")
    print(json.dumps({"preview": str(PREVIEW), "sha256": digest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    render()
