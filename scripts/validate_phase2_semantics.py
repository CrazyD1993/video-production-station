#!/usr/bin/env python3
"""Validate the active Phase 3 short-script, sample, and keyframe contracts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


CORE_MECHANISM = "pressure_equalization_to_load_bearing_pane"
SAMPLE_SCENE_IDS = ("V01", "V02", "V03")
KEYFRAME_STATUS = "ready_for_image_candidate_generation"
STRUCTURE_DISCLAIMER = "典型结构示意，不对应具体机型"
STALE_EXPRESSIONS = (
    "blocked_by_reference_analysis",
    "待真实拆解后填写",
    "待三条参考视频完成后填写",
    "尚未获得任何可播放参考视频",
)
BANNED_CAUSAL_CLAIMS = (
    "hypothetical_blockage",
    "堵住就爆",
    "碰一下就危险",
    "遮挡后立刻失效",
    "遮住小孔后会",
    "堵住后的功能受干扰",
)
BANNED_ACTIVE_BRANCHES = (
    "moisture_control_design_variants",
    "水汽迁移",
    "防雾方案",
    "干燥通道",
    "密封干气夹层",
)
CONTRACT_DOCUMENT_PATHS = (
    "08_OpenMontage试验/001-飞机舷窗小孔/脚本.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/故事板.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/关键帧提示词.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/Seedance运动提示词.md",
)
STATUS_DOCUMENT_PATHS = (
    *CONTRACT_DOCUMENT_PATHS,
    "08_OpenMontage试验/001-飞机舷窗小孔/当前状态.md",
    "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/README.md",
    "08_OpenMontage试验/06-试点验收报告.md",
    "08_OpenMontage试验/竞品分析/天赐科普/账号级分析.md",
)
PROMPT_DIR = Path(
    "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/prompts"
)


def validate_manifest_semantics(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    formula = manifest.get("content_formula") or {}
    if formula.get("core_mechanism") != CORE_MECHANISM:
        errors.append(f"content_formula.core_mechanism 必须为 {CORE_MECHANISM}")

    if manifest.get("active_timeline") != "high_density_25":
        errors.append("active_timeline 必须为 high_density_25")

    for timeline_id, timeline in (manifest.get("timelines") or {}).items():
        for scene in timeline.get("scenes") or []:
            purpose = str(scene.get("purpose", ""))
            visual = str(scene.get("visual", ""))
            combined = f"{purpose} {visual}"
            for expression in BANNED_ACTIVE_BRANCHES:
                if expression in combined:
                    errors.append(f"{timeline_id}/{scene.get('id')}: 当前版不得展开水汽或防雾支线: {expression}")

    sample = (manifest.get("timelines") or {}).get("visual_sample_12", {})
    scene_ids = tuple(scene.get("id") for scene in sample.get("scenes") or [])
    if scene_ids != SAMPLE_SCENE_IDS:
        errors.append(f"visual_sample_12 必须依次为 {SAMPLE_SCENE_IDS}")

    if (manifest.get("keyframe_status") or {}).get("status") != KEYFRAME_STATUS:
        errors.append(f"keyframe_status.status 必须为 {KEYFRAME_STATUS}")
    return errors


def validate_document_semantics(documents: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for path, text in documents.items():
        for expression in STALE_EXPRESSIONS:
            if expression in text:
                errors.append(f"{path}: 包含过期状态 {expression}")
        for expression in BANNED_CAUSAL_CLAIMS:
            if expression in text:
                errors.append(f"{path}: 包含禁用表达 {expression}")
        if path in CONTRACT_DOCUMENT_PATHS or len(documents) == 1:
            if STRUCTURE_DISCLAIMER not in text:
                errors.append(f"{path}: 缺少结构示意标记 {STRUCTURE_DISCLAIMER}")
    return errors


def validate_keyframe_prompts(root: Path) -> list[str]:
    errors: list[str] = []
    prompt_dir = root / PROMPT_DIR
    expected = {
        "KF1-01.yaml", "KF1-02.yaml", "KF2-01.yaml",
        "KF2-02.yaml", "KF3-01.yaml", "KF3-02.yaml",
    }
    actual = {path.name for path in prompt_dir.glob("*.yaml")}
    if actual != expected:
        errors.append(f"关键帧提示词文件必须恰好为6个，实际: {sorted(actual)}")

    for path in sorted(prompt_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data.get("status") != KEYFRAME_STATUS:
            errors.append(f"{path.name}: status 必须为 {KEYFRAME_STATUS}")
        rule = str(data.get("reference_rule", "")).strip()
        if not rule or any(expression in rule for expression in STALE_EXPRESSIONS):
            errors.append(f"{path.name}: reference_rule 未填写真实拆解规律")
        if data.get("aspect_ratio") != "9:16":
            errors.append(f"{path.name}: aspect_ratio 必须为 9:16")
        if data.get("required_disclaimer") != STRUCTURE_DISCLAIMER:
            errors.append(f"{path.name}: 缺少统一结构示意标记")
        text = path.read_text(encoding="utf-8")
        for expression in BANNED_ACTIVE_BRANCHES:
            if expression in text:
                errors.append(f"{path.name}: 关键帧不得展开水汽或防雾支线: {expression}")
    return errors


def validate_repository(root: Path) -> list[str]:
    manifest_path = root / "08_OpenMontage试验/03-生产清单模板.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    contract_documents = {
        relative: (root / relative).read_text(encoding="utf-8")
        for relative in CONTRACT_DOCUMENT_PATHS
    }
    status_documents = {
        relative: (root / relative).read_text(encoding="utf-8")
        for relative in STATUS_DOCUMENT_PATHS
        if relative not in contract_documents
    }
    return (
        validate_manifest_semantics(manifest)
        + validate_document_semantics(contract_documents)
        + validate_document_semantics(status_documents)
        + validate_keyframe_prompts(root)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        print("Phase 3 生产合同校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Phase 3 生产合同校验通过："
        f"core_mechanism={CORE_MECHANISM}, keyframes={KEYFRAME_STATUS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
