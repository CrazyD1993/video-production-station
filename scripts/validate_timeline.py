#!/usr/bin/env python3
"""Validate OpenMontage production timelines against one YAML manifest."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


EPSILON = 0.001
DEFAULT_MANIFEST = Path("08_OpenMontage试验/03-生产清单模板.yaml")


def _duration(scene: dict[str, Any]) -> float:
    return float(scene["end_seconds"]) - float(scene["start_seconds"])


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    timelines = manifest.get("timelines") or {}

    if not timelines:
        return ["缺少 timelines，无法验证时间轴"]

    for timeline_id, timeline in timelines.items():
        scenes = timeline.get("scenes") or []
        declared_total = float(timeline.get("duration_seconds", 0))
        if not scenes:
            errors.append(f"{timeline_id}: 没有镜头")
            continue

        previous_end = 0.0
        for index, scene in enumerate(scenes):
            scene_id = scene.get("id", f"scene-{index + 1}")
            start = float(scene["start_seconds"])
            end = float(scene["end_seconds"])

            if end <= start:
                errors.append(f"{timeline_id}/{scene_id}: 结束时间必须晚于开始时间")
            if start > previous_end + EPSILON:
                errors.append(
                    f"{timeline_id}/{scene_id}: 存在空档 {previous_end:g}-{start:g} 秒"
                )
            if start < previous_end - EPSILON:
                errors.append(
                    f"{timeline_id}/{scene_id}: 与前一镜头重叠 {start:g}-{previous_end:g} 秒"
                )
            previous_end = end

        if abs(previous_end - declared_total) > EPSILON:
            errors.append(
                f"{timeline_id}: 总时长不一致，镜头结束于 {previous_end:g} 秒，"
                f"声明为 {declared_total:g} 秒"
            )

    sample = timelines.get("visual_sample_12", {})
    sample_scenes = {scene["id"]: scene for scene in sample.get("scenes", [])}
    contracts = manifest.get("seedance_contracts") or {}
    for scene_id, contract in contracts.items():
        if scene_id not in sample_scenes:
            errors.append(f"Seedance/{scene_id}: 不在 visual_sample_12 时间轴中")
            continue
        expected = _duration(sample_scenes[scene_id])
        actual = float(contract.get("duration_seconds", 0))
        if abs(expected - actual) > EPSILON:
            errors.append(
                f"Seedance/{scene_id}: 合同时长 {actual:g} 秒与样片镜头 "
                f"{expected:g} 秒不一致"
            )

    sample_ids = set(sample_scenes)
    contract_ids = set(contracts)
    for missing in sorted(sample_ids - contract_ids):
        errors.append(f"Seedance/{missing}: 样片镜头缺少 Seedance 合同")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    errors = validate_manifest(manifest)
    if errors:
        print("时间轴校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"时间轴校验通过：{args.manifest}")
    for timeline_id, timeline in manifest["timelines"].items():
        print(
            f"- {timeline_id}: {len(timeline['scenes'])} 镜头，"
            f"{timeline['duration_seconds']} 秒"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
