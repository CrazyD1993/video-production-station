#!/usr/bin/env python3
"""Inspect six approved-format keyframe candidates and build a 2x3 sheet."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageDraw, ImageOps


EXPECTED_NAMES = (
    "KF1-01.png",
    "KF1-02.png",
    "KF2-01.png",
    "KF2-02.png",
    "KF3-01.png",
    "KF3-02.png",
)
ALLOWED_FORMATS = {"PNG"}
TARGET_ASPECT_RATIO = 9 / 16
ASPECT_RATIO_TOLERANCE = 0.01
MIN_WIDTH = 720
MIN_HEIGHT = 1280
CELL_WIDTH = 450
CELL_HEIGHT = 800
LABEL_HEIGHT = 48
MARGIN = 30
GAP = 20

CONTENT_DESCRIPTIONS = {
    "KF1-01": "真实感微距舷窗下缘，小孔清晰，无手指，窗外机翼与云层虚化。",
    "KF1-02": "第一人称靠窗观察，手指接近窗边小孔，窗外为云层。",
    "KF2-01": "完整舷窗与右下角小型发光剖面同屏，小孔与剖面关系不清。",
    "KF2-02": "舷窗侧向纵深剖面，蓝色发光路径穿过复杂机械槽道。",
    "KF3-01": "完整舷窗上叠加顶部剖面和气流线，画面存在两个孔状视觉点。",
    "KF3-02": "生成式爆炸剖面，透明窗格、箭头和边框结构占据主体。",
}

CURRENT_DECISIONS = {
    "KF1-01": "regenerate_with_real_reference",
    "KF1-02": "reject_regenerate_with_real_reference",
    "KF2-01": "reject",
    "KF2-02": "reject_ai_structure_risk",
    "KF3-01": "reject",
    "KF3-02": "reject",
}


def inspect_candidates(folder: Path) -> list[dict[str, Any]]:
    present = {path.name for path in folder.iterdir() if path.is_file()}
    missing = [name for name in EXPECTED_NAMES if name not in present]
    unexpected_images = sorted(
        name
        for name in present
        if Path(name).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        and name not in EXPECTED_NAMES
    )
    if missing:
        raise ValueError(f"缺少候选图片：{', '.join(missing)}")
    if unexpected_images:
        raise ValueError(f"存在未登记图片：{', '.join(unexpected_images)}")

    report: list[dict[str, Any]] = []
    for name in EXPECTED_NAMES:
        path = folder / name
        with Image.open(path) as image:
            if image.format not in ALLOWED_FORMATS:
                raise ValueError(f"{name}: 仅接受 PNG，实际为 {image.format}")
            width, height = image.size
            ratio = width / height
            if width < MIN_WIDTH or height < MIN_HEIGHT:
                raise ValueError(
                    f"{name}: 9:16 图片尺寸至少 {MIN_WIDTH}x{MIN_HEIGHT}，"
                    f"实际为 {width}x{height}"
                )
            if abs(ratio - TARGET_ASPECT_RATIO) > ASPECT_RATIO_TOLERANCE:
                raise ValueError(
                    f"{name}: 宽高比必须接近 9:16，实际为 {width}:{height}"
                )
            report.append(
                {
                    "name": name,
                    "path": path,
                    "width": width,
                    "height": height,
                    "format": image.format,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
    return report


def contact_sheet_label(item: dict[str, Any]) -> str:
    candidate_id = item["name"].removesuffix(".png")
    return f"{candidate_id} | {item['sha256'][:8]}"


def write_candidate_manifest(report: list[dict[str, Any]], output: Path) -> None:
    candidates = []
    for item in report:
        candidate_id = item["name"].removesuffix(".png")
        candidates.append(
            {
                "candidate_id": candidate_id,
                "filename": item["name"],
                "sha256": item["sha256"],
                "width": item["width"],
                "height": item["height"],
                "content_description": CONTENT_DESCRIPTIONS[candidate_id],
                "current_decision": CURRENT_DECISIONS[candidate_id],
            }
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        yaml.safe_dump(
            {"schema_version": 1, "media_committed_to_git": False, "candidates": candidates},
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def build_contact_sheet(report: list[dict[str, Any]], output: Path) -> None:
    sheet_width = MARGIN * 2 + CELL_WIDTH * 2 + GAP
    sheet_height = MARGIN * 2 + (CELL_HEIGHT + LABEL_HEIGHT) * 3 + GAP * 2
    sheet = Image.new("RGB", (sheet_width, sheet_height), "#111318")
    draw = ImageDraw.Draw(sheet)

    for index, item in enumerate(report):
        row, column = divmod(index, 2)
        x = MARGIN + column * (CELL_WIDTH + GAP)
        y = MARGIN + row * (CELL_HEIGHT + LABEL_HEIGHT + GAP)
        with Image.open(item["path"]) as source:
            frame = ImageOps.contain(
                source.convert("RGB"),
                (CELL_WIDTH, CELL_HEIGHT),
                method=Image.Resampling.LANCZOS,
            )
        frame_x = x + (CELL_WIDTH - frame.width) // 2
        frame_y = y + (CELL_HEIGHT - frame.height) // 2
        sheet.paste(frame, (frame_x, frame_y))
        draw.text(
            (x + 14, y + CELL_HEIGHT + 14),
            contact_sheet_label(item),
            fill="white",
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92, subsampling=0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("incoming", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        report = inspect_candidates(args.incoming)
        build_contact_sheet(report, args.output)
        if args.manifest:
            write_candidate_manifest(report, args.manifest)
    except (OSError, ValueError) as exc:
        print(f"关键帧检查失败：{exc}")
        return 1

    print(f"关键帧检查通过：6 张 PNG；联系表已生成：{args.output}")
    for item in report:
        print(f"- {item['name']}: {item['width']}x{item['height']} {item['format']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
