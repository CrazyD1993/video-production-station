#!/usr/bin/env python3
"""Generate reproducible technical and visual QA evidence for the V2 production snapshot."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
QA = ROOT / "qa"
TIMELINE = [
    ("S01", 0.00, 1.20), ("S02", 1.20, 3.85), ("S03", 3.85, 5.69),
    ("S04", 5.69, 8.70), ("S05", 8.70, 12.32), ("S06", 12.32, 17.10),
    ("S07", 17.10, 21.38), ("S08", 21.38, 24.30), ("S09", 24.30, 27.35),
    ("S10", 27.35, 30.50), ("S11", 30.50, 35.06), ("S12", 35.06, 39.77),
    ("S13", 39.77, 46.80),
]
MEDIA = {
    "preview": ROOT / "petrichor-remediation-v2-clean-preview.mp4",
    "mechanism-a": ROOT / "mechanism-a-v2.mp4",
    "mechanism-b": ROOT / "mechanism-b-v2.mp4",
}


def font(size: int):
    for path in [Path("/System/Library/Fonts/PingFang.ttc"), Path("/System/Library/Fonts/STHeiti Light.ttc")]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def frame(source: Path, at: float, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{at:.3f}", "-i", str(source), "-frames:v", "1", "-q:v", "2", str(output)])


def labelled_contact(items: list[tuple[Path, str]], output: Path, columns: int = 4) -> None:
    cell_w, image_h, label_h = 270, 480, 54
    rows = (len(items) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_w, rows * (image_h + label_h)), (18, 19, 17))
    draw = ImageDraw.Draw(canvas)
    for index, (path, label) in enumerate(items):
        image = Image.open(path).convert("RGB").resize((cell_w, image_h), Image.Resampling.LANCZOS)
        x = (index % columns) * cell_w
        y = (index // columns) * (image_h + label_h)
        canvas.paste(image, (x, y + label_h))
        draw.text((x + 10, y + 13), label, font=font(21), fill=(239, 234, 216))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, quality=91)


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    probes = {}
    decodes = {}
    hashes = []
    for name, path in MEDIA.items():
        probe = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
        (QA / f"{name}-ffprobe.json").write_text(probe.stdout, encoding="utf-8")
        probes[name] = json.loads(probe.stdout)
        decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, text=True)
        decodes[name] = {"exit_code": decode.returncode, "stderr": decode.stderr}
        hashes.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (QA / "decode-verification.json").write_text(json.dumps(decodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (QA / "media-sha256.txt").write_text("\n".join(hashes) + "\n", encoding="utf-8")

    midpoint_items = []
    midpoint_dir = QA / "shot-midpoints"
    for shot_id, start, end in TIMELINE:
        path = midpoint_dir / f"{shot_id}.jpg"
        frame(MEDIA["preview"], (start + end) / 2, path)
        midpoint_items.append((path, f"{shot_id}  {start:05.2f}-{end:05.2f}"))
    labelled_contact(midpoint_items, QA / "shot-midpoints-contact-sheet.jpg")

    for name in ["mechanism-a", "mechanism-b"]:
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(MEDIA[name]),
            "-vf", "fps=1,scale=180:320,tile=4x4:padding=4:margin=4:color=0x121311",
            "-frames:v", "1", str(QA / f"{name}-contact-sheet.jpg"),
        ])

    continuity_items = []
    for left, right in [("S08", "S09"), ("S09", "S10"), ("S10", "S11")]:
        left_path = ROOT / "work/shots" / f"{left}.mp4"
        right_path = ROOT / "work/shots" / f"{right}.mp4"
        duration = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(left_path)]).stdout.strip())
        out_left = QA / "continuity" / f"{left}-last.jpg"
        out_right = QA / "continuity" / f"{right}-first.jpg"
        frame(left_path, max(0, duration - 0.083), out_left)
        frame(right_path, 0.042, out_right)
        continuity_items.extend([(out_left, f"{left} last"), (out_right, f"{right} first")])
    labelled_contact(continuity_items, QA / "mechanism-b-continuity-contact-sheet.jpg", columns=2)

    ref_items = []
    ref_dir = ROOT / "mechanism-b-reference-pack-v2"
    for file, label in [
        ("b1-prestate-first-frame.png", "B1 prestate"), ("bridge-start.png", "G02 bridge"),
        ("rise-low.png", "G02 rise low"), ("rise-mid.png", "G02 rise mid"),
        ("surface-contact.png", "surface contact"), ("surface-after.png", "surface after"),
    ]:
        ref_items.append((ref_dir / file, label))
    labelled_contact(ref_items, QA / "mechanism-b-reference-contact-sheet.jpg", columns=3)


if __name__ == "__main__":
    main()
