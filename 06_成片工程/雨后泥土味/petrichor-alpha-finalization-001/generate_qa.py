#!/usr/bin/env python3
"""Generate deterministic technical and visual QA evidence for the Alpha."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from alpha_config import FPS, ROOT, SHOTS, TOTAL_FRAMES

QA = ROOT / "qa"
MEDIA = {
    "alpha": ROOT / "petrichor-alpha-v1.mp4",
    "mechanism_a": ROOT / "mechanism-a-final.mp4",
    "mechanism_b": ROOT / "mechanism-b-final.mp4",
}


def capture(*args: str) -> str:
    return subprocess.run([str(arg) for arg in args], check=True, text=True,
                          stdout=subprocess.PIPE).stdout


def run(*args: str) -> None:
    subprocess.run([str(arg) for arg in args], check=True)


def probe(name: str, path: Path) -> dict:
    raw = capture(
        "ffprobe", "-v", "error", "-count_frames", "-show_entries",
        "format=duration,size,format_name:stream=index,codec_name,codec_type,width,height,"
        "pix_fmt,r_frame_rate,avg_frame_rate,nb_read_frames,sample_rate,channels",
        "-of", "json", path,
    )
    data = json.loads(raw)
    (QA / f"{name}-ffprobe.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def decode_check(name: str, path: Path) -> dict:
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return {"asset": name, "exit_code": result.returncode,
            "stderr": result.stderr.strip(), "full_decode_ok": result.returncode == 0}


def pts_check(path: Path) -> dict:
    raw = capture(
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "frame=best_effort_timestamp_time", "-of", "json", path,
    )
    pts = [float(frame["best_effort_timestamp_time"])
           for frame in json.loads(raw)["frames"]]
    expected = 1 / FPS
    deltas = [b - a for a, b in zip(pts, pts[1:])]
    bad = [{"frame": index + 1, "delta": delta} for index, delta in enumerate(deltas)
           if abs(delta - expected) > 0.000002]
    return {
        "frame_count": len(pts),
        "expected_frame_count": TOTAL_FRAMES,
        "first_pts": pts[0],
        "last_pts": pts[-1],
        "expected_delta": expected,
        "min_delta": min(deltas),
        "max_delta": max(deltas),
        "discontinuities": bad,
        "continuous_cfr_24": len(pts) == TOTAL_FRAMES and not bad,
    }


def contact_sheet(source: Path, frames: list[int], columns: int, rows: int,
                  width: int, height: int, output: Path) -> None:
    expression = "+".join(f"eq(n\\,{frame})" for frame in frames)
    vf = f"select='{expression}',scale={width}:{height}:flags=lanczos,tile={columns}x{rows}:padding=0:margin=0"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", source,
        "-vf", vf, "-frames:v", "1", "-q:v", "2", output)


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    probes = {name: probe(name, path) for name, path in MEDIA.items()}
    decode = [decode_check(name, path) for name, path in MEDIA.items()]
    (QA / "decode-verification.json").write_text(
        json.dumps(decode, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pts = pts_check(MEDIA["alpha"])
    (QA / "pts-continuity.json").write_text(
        json.dumps(pts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    hashes = []
    for name, path in MEDIA.items():
        hashes.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (QA / "media-sha256.txt").write_text("\n".join(hashes) + "\n", encoding="utf-8")

    starts, cursor = {}, 0
    for shot in SHOTS:
        starts[shot.id] = cursor
        cursor += shot.frames
    midpoints = [starts[shot.id] + shot.frames // 2 for shot in SHOTS]
    contact_sheet(MEDIA["alpha"], midpoints, 4, 4, 180, 320,
                  QA / "shot-midpoints-contact-sheet.jpg")

    revised_ids = ("S01", "S05", "S06", "S07", "S09", "S11", "S12")
    dense = []
    for shot in SHOTS:
        if shot.id in revised_ids:
            dense.extend((starts[shot.id], starts[shot.id] + shot.frames // 2,
                          starts[shot.id] + shot.frames - 1))
    contact_sheet(MEDIA["alpha"], dense, 5, 5, 144, 256,
                  QA / "revised-shots-dense-contact-sheet.jpg")
    contact_sheet(MEDIA["mechanism_a"], list(range(0, 305, 27))[:12], 4, 3, 180, 320,
                  QA / "mechanism-a-dense-contact-sheet.jpg")
    contact_sheet(MEDIA["mechanism_b"], list(range(0, 258, 23))[:12], 4, 3, 180, 320,
                  QA / "mechanism-b-dense-contact-sheet.jpg")

    map_text = """# Contact sheet map

- `shot-midpoints-contact-sheet.jpg`: row-major S01 through S13, then three empty tiles.
- `revised-shots-dense-contact-sheet.jpg`: row-major, three frames each (first/middle/last) for S01, S05, S06, S07, S09, S11, S12, then four empty tiles.
- `mechanism-a-dense-contact-sheet.jpg`: 12 evenly stepped frames from the continuous mechanism A render.
- `mechanism-b-dense-contact-sheet.jpg`: 12 evenly stepped frames from the continuous mechanism B render.
"""
    (QA / "contact-sheet-map.md").write_text(map_text, encoding="utf-8")

    summary = {
        "alpha_duration": probes["alpha"]["format"]["duration"],
        "alpha_streams": probes["alpha"]["streams"],
        "decode_all_ok": all(item["full_decode_ok"] for item in decode),
        "pts_continuous": pts["continuous_cfr_24"],
    }
    (QA / "qa-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
