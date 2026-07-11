#!/usr/bin/env python3
"""Validate Phase 2A S06 semantics across production contracts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


S06_PURPOSE = "moisture_control_design_variants"
REVERSAL = "这个小孔的高置信度作用是参与典型压力连通设计；水汽与防雾可能采用不同方案"
BANNED_EXPRESSIONS = (
    "hypothetical_blockage",
    "堵住就爆",
    "遮挡后立刻失效",
    "遮住小孔后会",
    "堵住后的功能受干扰",
)
DISCLAIMERS = ("不同设计方案示意", "典型结构示意")
DOCUMENT_PATHS = (
    "08_OpenMontage试验/001-飞机舷窗小孔/脚本.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/故事板.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/关键帧提示词.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/Seedance运动提示词.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/prompts/KF3-01.yaml",
    "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/prompts/KF3-02.yaml",
)


def validate_manifest_semantics(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("content_formula", {}).get("reversal") != REVERSAL:
        errors.append("content_formula.reversal 与 Phase 2A 规定不一致")

    for timeline_id, timeline in (manifest.get("timelines") or {}).items():
        for scene in timeline.get("scenes") or []:
            if scene.get("id") == "S06" and scene.get("purpose") != S06_PURPOSE:
                errors.append(
                    f"{timeline_id}/S06 purpose 必须为 {S06_PURPOSE}，"
                    f"实际为 {scene.get('purpose')}"
                )

    contract = (manifest.get("seedance_contracts") or {}).get("S06", {})
    if contract.get("purpose") != S06_PURPOSE:
        errors.append("seedance_contracts/S06 purpose 不一致")
    return errors


def validate_document_semantics(documents: dict[str, str]) -> list[str]:
    errors: list[str] = []
    purpose_marker = f"S06 purpose: {S06_PURPOSE}"
    for path, text in documents.items():
        for expression in BANNED_EXPRESSIONS:
            if expression in text:
                errors.append(f"{path}: 包含禁用表达 {expression}")
        if purpose_marker not in text and f"purpose: {S06_PURPOSE}" not in text:
            errors.append(f"{path}: 缺少统一 S06 purpose")
        if not any(disclaimer in text for disclaimer in DISCLAIMERS):
            errors.append(f"{path}: 缺少典型结构示意或不同设计方案示意标记")
    return errors


def validate_repository(root: Path) -> list[str]:
    manifest_path = root / "08_OpenMontage试验/03-生产清单模板.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    documents = {
        relative: (root / relative).read_text(encoding="utf-8")
        for relative in DOCUMENT_PATHS
    }
    return validate_manifest_semantics(manifest) + validate_document_semantics(documents)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        print("Phase 2A 语义校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Phase 2A 语义校验通过：S06 purpose={S06_PURPOSE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
