#!/usr/bin/env python3
"""Inspect six approved-format keyframe candidates and build a 2x3 sheet."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

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
            if width < 720 or height < 1080:
                raise ValueError(f"{name}: 尺寸至少 720x1080，实际为 {width}x{height}")
            if height <= width:
                raise ValueError(f"{name}: 必须是竖版图片，实际为 {width}x{height}")
            report.append(
                {"name": name, "path": path, "width": width, "height": height, "format": image.format}
            )
    return report


def build_contact_sheet(report: list[dict[str, Any]], output: Path) -> None:
    cell_width, image_height, label_height = 540, 810, 54
    margin, gap = 30, 20
    sheet_width = margin * 2 + cell_width * 2 + gap
    sheet_height = margin * 2 + (image_height + label_height) * 3 + gap * 2
    sheet = Image.new("RGB", (sheet_width, sheet_height), "#111318")
    draw = ImageDraw.Draw(sheet)

    for index, item in enumerate(report):
        row, column = divmod(index, 2)
        x = margin + column * (cell_width + gap)
        y = margin + row * (image_height + label_height + gap)
        with Image.open(item["path"]) as source:
            frame = ImageOps.fit(source.convert("RGB"), (cell_width, image_height), method=Image.Resampling.LANCZOS)
        sheet.paste(frame, (x, y))
        draw.text((x + 14, y + image_height + 16), item["name"].removesuffix(".png"), fill="white")

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92, subsampling=0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("incoming", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        report = inspect_candidates(args.incoming)
        build_contact_sheet(report, args.output)
    except (OSError, ValueError) as exc:
        print(f"关键帧检查失败：{exc}")
        return 1

    print(f"关键帧检查通过：6 张 PNG；联系表已生成：{args.output}")
    for item in report:
        print(f"- {item['name']}: {item['width']}x{item['height']} {item['format']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
