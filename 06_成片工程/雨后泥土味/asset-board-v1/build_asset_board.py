#!/usr/bin/env python3
"""雨后泥土味 V1 素材板资料生成器。

只生成资料、静态草图和素材板 SVG；不调用 TTS、Seedance 或任何付费模型。
"""

from __future__ import annotations

import base64
import csv
import html
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets" / "real-proxy"
MECHANISM_DIR = ROOT / "mechanism"
QA_DIR = ROOT / "qa"
POSTER_DIR = QA_DIR / "posters"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
PAID_MODEL_CALLS = 0
DOWNLOAD_DATE = "2026-07-15"
LICENSE_URL = "https://www.pexels.com/license/"
ALLOWED_USE = (
    "Pexels License：可免费使用和修改，可用于社交媒体；不得转售未修改副本、"
    "不得暗示人物或品牌代言、不得在其他素材平台再分发。"
)


def real_asset(asset_id, filename, page, author, shot_ids, note):
    return {
        "asset_id": asset_id,
        "filename": filename,
        "original_page_url": page,
        "author_uploader": author,
        "platform": "Pexels",
        "license_type": "Pexels License",
        "license_url": LICENSE_URL,
        "download_date": DOWNLOAD_DATE,
        "allowed_use": ALLOWED_USE,
        "shot_ids": shot_ids,
        "source_category": "real_external",
        "acquired": "yes",
        "local_path": f"assets/real-proxy/{filename}",
        "review_note": note,
    }


ASSETS = [
    real_asset(
        "R01", "R01-pexels-13444705-rain-leaves-proxy.mp4",
        "https://www.pexels.com/video/raindrops-falling-on-leaves-13444705/",
        "Igor Haritanovich", "S02,S13",
        "6秒无声 720×1280 审片代理；真实雨滴打叶片，两次使用分别承担快节奏细节和收束前景。",
    ),
    real_asset(
        "R02", "R02-pexels-5210312-leaf-droplet-proxy.mp4",
        "https://www.pexels.com/video/droplet-of-water-from-a-leaf-5210312/",
        "Kelly", "S04",
        "6秒无声 720×1280 审片代理；叶尖水滴形成并落下。",
    ),
    real_asset(
        "R03", "R03-pexels-7234789-wet-soil-proxy.mp4",
        "https://www.pexels.com/video/close-up-video-of-a-wet-soil-7234789/",
        "Artem Podrez", "S02,S12",
        "6秒无声 720×1280 审片代理；湿泥土和细根，可承担湿土细节与旱后转湿对照。",
    ),
    real_asset(
        "R04", "R04-pexels-7232905-wet-soil-macro.jpg",
        "https://www.pexels.com/photo/macro-photography-of-wet-soil-7232905/",
        "Artem Podrez", "S03",
        "湿润土壤宏观纹理，留有标题负空间。",
    ),
    real_asset(
        "R05", "R05-pexels-12763908-tree-roots-soil.jpg",
        "https://www.pexels.com/photo/old-tree-roots-12763908/",
        "Liudmyla Shalimova", "S06",
        "根系与土壤真实质感，用于土壤吸附段的地表依据。",
    ),
    real_asset(
        "R06", "R06-pexels-28922207-forest-floor.jpg",
        "https://www.pexels.com/photo/forest-floor-with-moss-and-autumn-leaves-28922207/",
        "Etoileala", "S06",
        "落叶、苔藓、根系和土粒层次，可与 R05 交替。",
    ),
    real_asset(
        "R07", "R07-pexels-5597653-dry-cracked-soil.jpg",
        "https://www.pexels.com/photo/photo-of-dry-and-cracked-soil-5597653/",
        "Lucas George Wendt", "S01,S12",
        "干裂土表；S01 承担落滴前基底，S12 承担久旱语义，两次功能不同。",
    ),
    real_asset(
        "R08", "R08-pexels-29579839-misty-forest.jpg",
        "https://www.pexels.com/photo/moody-misty-forest-landscape-with-tall-pines-29579839/",
        "Elina Volkova", "S13",
        "竖幅雾林真实照片，可做缓慢程序化拉远预览；正式版仍建议补真实动态。",
    ),
    real_asset(
        "R09", "R09-pexels-2905149-wet-cobblestone.jpg",
        "https://www.pexels.com/photo/cobblestone-wet-after-rain-2905149/",
        "Emmanuel Codden", "S02",
        "雨后湿石板纹理；静帧可做快切，正式版优先补落雨动态。",
    ),
    real_asset(
        "R10", "R10-pexels-14675142-raindrops-leaf.jpg",
        "https://www.pexels.com/photo/macro-of-raindrops-on-leaf-14675142/",
        "Johanna", "S13",
        "落叶上的雨珠真实宏观照片，用于收束段近景。",
    ),
    {
        "asset_id": "P05", "filename": "soil-entry-transition-v1.svg",
        "original_page_url": "local-programmatic", "author_uploader": "Codex",
        "platform": "local", "license_type": "project-owned",
        "license_url": "local-programmatic", "download_date": DOWNLOAD_DATE,
        "allowed_use": "项目内可编辑程序化草图。", "shot_ids": "S05",
        "source_category": "programmatic", "acquired": "yes",
        "local_path": "mechanism/soil-entry-transition-v1.svg",
        "review_note": "地表进入土壤剖面的结构占位，不是正式成片。",
    },
    {
        "asset_id": "MA", "filename": "mechanism-a-geosmin-v1.svg",
        "original_page_url": "local-programmatic", "author_uploader": "Codex",
        "platform": "local", "license_type": "project-owned",
        "license_url": "local-programmatic", "download_date": DOWNLOAD_DATE,
        "allowed_use": "项目内可编辑程序化草图。", "shot_ids": "S07",
        "source_category": "mechanism_sketch", "acquired": "yes",
        "local_path": "mechanism/mechanism-a-geosmin-v1.svg",
        "review_note": "土粒、细根、菌丝与微量颗粒的纪录片质感草图。",
    },
    {
        "asset_id": "MB", "filename": "mechanism-b-aerosol-v1.svg",
        "original_page_url": "local-programmatic", "author_uploader": "Codex",
        "platform": "local", "license_type": "project-owned",
        "license_url": "local-programmatic", "download_date": DOWNLOAD_DATE,
        "allowed_use": "项目内可编辑程序化草图。", "shot_ids": "S08,S09,S10,S11",
        "source_category": "mechanism_sketch", "acquired": "yes",
        "local_path": "mechanism/mechanism-b-aerosol-v1.svg",
        "review_note": "撞击—困气—气泡上升—破裂释放气溶胶的三阶段结构草图。",
    },
]


SHOTS = [
    {"id": "S01", "start": 0.00, "end": 1.20, "visual": "第一颗雨滴落在干燥泥土，真实微距优先。", "source": "真实", "acquired": "部分取得", "seedance": "否", "programmatic": "否", "asset_ids": ["R07"], "note": "已有干土基底；缺真实落滴撞击动态。", "sound": "0秒附近一颗清晰近距离雨滴声。"},
    {"id": "S02", "start": 1.20, "end": 3.85, "visual": "雨落叶片、石板路、泥土，三个快速生活细节。", "source": "真实", "acquired": "已取得", "seedance": "否", "programmatic": "否", "asset_ids": ["R01", "R09", "R03"], "note": "叶片与湿土有动态；石板当前为静帧快切。", "sound": "1—21秒细密轻柔雨声环境底。"},
    {"id": "S03", "start": 3.85, "end": 5.69, "visual": "湿润泥土近景，预留标题。", "source": "真实", "acquired": "已取得", "seedance": "否", "programmatic": "否", "asset_ids": ["R04"], "note": "标题固定：「雨后的泥土味，从哪儿来？」", "sound": "维持轻雨底。"},
    {"id": "S04", "start": 5.69, "end": 8.70, "visual": "透明雨滴挂在叶尖并落下。", "source": "真实", "acquired": "已取得", "seedance": "否", "programmatic": "否", "asset_ids": ["R02"], "note": "真实宏观落滴视频已取得代理。", "sound": "局部水滴声可后续保留，本轮不混音。"},
    {"id": "S05", "start": 8.70, "end": 12.32, "visual": "镜头由地表进入土壤剖面。", "source": "程序化", "acquired": "草图就绪", "seedance": "否", "programmatic": "是", "asset_ids": ["P05"], "note": "已建立剖面结构；缺正式连续下潜动画。", "sound": "仍保持地表轻雨环境。"},
    {"id": "S06", "start": 12.32, "end": 17.10, "visual": "植物、落叶、根部、土粒和岩石，展示物质被土壤吸附。", "source": "真实+程序化", "acquired": "已取得", "seedance": "否", "programmatic": "是", "asset_ids": ["R05", "R06"], "note": "真实根系与林地为依据；吸附过程后续只做克制局部标记。", "sound": "继续轻雨底。"},
    {"id": "S07", "start": 17.10, "end": 21.38, "visual": "土壤微生物与土臭素机制镜头 A。", "source": "机制草图", "acquired": "草图就绪", "seedance": "候选A", "programmatic": "是", "asset_ids": ["MA"], "note": "正式动态缺失；保留「土臭素 Geosmin」小标签。", "sound": "21秒附近环境声开始稍闷。"},
    {"id": "S08", "start": 21.38, "end": 24.30, "visual": "雨滴高速落向多孔土壤。", "source": "程序化占位", "acquired": "草图就绪", "seedance": "否", "programmatic": "是", "asset_ids": ["MB"], "note": "缺真实高速宏观落滴；建议优先实拍/免费高速素材。", "sound": "环境稍闷，为进入土壤内部做铺垫。"},
    {"id": "S09", "start": 24.30, "end": 27.35, "visual": "孔隙空气被水困成气泡。", "source": "机制草图", "acquired": "草图就绪", "seedance": "候选B", "programmatic": "是", "asset_ids": ["MB"], "note": "阶段标签：「困住空气」。", "sound": "低频环境轻微变闷。"},
    {"id": "S10", "start": 27.35, "end": 30.50, "visual": "气泡升向水滴表面。", "source": "机制草图", "acquired": "草图就绪", "seedance": "候选B", "programmatic": "是", "asset_ids": ["MB"], "note": "阶段标签：「形成气泡」。", "sound": "29.8秒附近预留真实小气泡「啪」声。"},
    {"id": "S11", "start": 30.50, "end": 35.06, "visual": "气泡破裂并释放极细气溶胶。", "source": "机制草图", "acquired": "草图就绪", "seedance": "候选B", "programmatic": "是", "asset_ids": ["MB"], "note": "阶段标签：「释放气溶胶」。", "sound": "30—35秒预留极轻空气喷散声。"},
    {"id": "S12", "start": 35.06, "end": 39.77, "visual": "久旱后的土地迎来第一阵小雨。", "source": "真实", "acquired": "部分取得", "seedance": "否", "programmatic": "否", "asset_ids": ["R07", "R03"], "note": "已有干土/湿土对照；缺同一地表首雨转变的真实连续镜头。", "sound": "环境声回到地表的轻雨层次。"},
    {"id": "S13", "start": 39.77, "end": 46.80, "visual": "雨后树林、叶片水珠、薄雾，缓慢拉远收束。", "source": "真实+程序化", "acquired": "部分取得", "seedance": "否", "programmatic": "是", "asset_ids": ["R08", "R10", "R01"], "note": "雾林和雨珠已取得；预览可缓慢拉远，正式版优先补真实动态雾林。", "sound": "40秒后音乐稍抬且不煽情；旁白后留0.7—1秒环境尾音。"},
]


ASSET_BY_ID = {item["asset_id"]: item for item in ASSETS}


def q(value):
    return json.dumps(value, ensure_ascii=False)


def write_shot_plan():
    lines = [
        "task_id: petrichor-asset-board-v1-001",
        "version: 1",
        f"generated_at: {DOWNLOAD_DATE}",
        "status: asset_board_ready_for_human_review",
        "timeline_locked: true",
        "narration_locked: true",
        "narration_speed_changed: false",
        "paid_model_calls: 0",
        "target:",
        "  aspect_ratio: \"9:16\"",
        "  narration_duration_seconds: 45.937",
        "  planned_total_duration_seconds: 46.80",
        "  allowed_total_ceiling_seconds: 48.5",
        "  real_visual_ratio_target: \"60-65%\"",
        "  ai_mechanism_ratio_target: \"20-25%\"",
        "  programmatic_ratio_target: \"10-15%\"",
        "inventory_summary:",
        "  acquired_real_mother_assets: 10",
        "  external_license_records_complete: true",
        "  formal_dynamic_missing_shots: [S01, S05, S07, S08, S09, S10, S11, S12, S13]",
        "  formal_composition_gate: blocked_pending_missing_assets_and_human_review",
        "rhythm_hold_plan:",
        "  executed_in_preview: false",
        "  suggestions:",
        "    - after_shot: S01",
        "      treatment: \"0.24s black_or_freeze_after_real_raindrop_impact\"",
        "    - after_shot: S11",
        "      treatment: \"0.24s freeze_after_bubble_pop\"",
        "shots:",
    ]
    for shot in SHOTS:
        lines.extend([
            f"  - id: {shot['id']}",
            f"    start: {shot['start']:.2f}",
            f"    end: {shot['end']:.2f}",
            f"    duration: {shot['end'] - shot['start']:.2f}",
            f"    locked_visual: {q(shot['visual'])}",
            f"    source_category: {q(shot['source'])}",
            f"    acquisition_status: {q(shot['acquired'])}",
            f"    seedance: {q(shot['seedance'])}",
            f"    programmatic_animation: {q(shot['programmatic'])}",
            f"    asset_ids: {q(shot['asset_ids'])}",
            f"    execution_note: {q(shot['note'])}",
            f"    sound_design_plan_only: {q(shot['sound'])}",
        ])
    (ROOT / "shot-plan-v1.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest():
    fields = [
        "asset_id", "filename", "original_page_url", "author_uploader",
        "platform", "license_type", "license_url", "download_date",
        "allowed_use", "shot_ids", "source_category", "acquired",
        "local_path", "review_note",
    ]
    with (ROOT / "asset-manifest-v1.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(ASSETS)


def write_missing_assets():
    content = """# 雨后泥土味｜缺失素材与进入合成门禁 V1

## 当前结论

- 已取得 **10 个不同真实母素材的审片代理**：3 个视频、7 张照片。
- 所有外部素材均有原始页面、作者、平台、许可页、下载日期、使用范围和镜头映射；授权记录完整。
- 视频文件是用于素材板和审片的无声 720×1280 代理，不是正式清晰度母版。
- 机制 A / B 已建立静态结构草图，未调用 Seedance 或其他付费模型。
- **尚不具备进入正式合成的条件**；需先补齐下列动态缺口并完成人工素材取舍。

## 正式动态缺口

| 镜头 | 当前状态 | 必须补齐的资产 | 建议路径 |
|---|---|---|---|
| S01 | 已有干裂土表照片 | 单颗雨滴撞击干土的真实微距动态 | 继续寻找免费高速素材或小型实拍 |
| S05 | 已有土壤剖面结构草图 | 地表至土壤内部的连续进入动画 | 程序化完成，不必使用付费模型 |
| S07 | 机制 A 草图就绪 | 微生物产生土臭素的克制微观动态 | Seedance 候选 A，待人工确认后才可调用 |
| S08 | 机制 B 第一阶段草图 | 雨滴高速接近多孔土壤 | 优先免费高速宏观/实拍 |
| S09–S11 | 机制 B 三阶段草图就绪 | 困气、气泡上升、破裂释放气溶胶的连续动态 | Seedance 候选 B，文字标签后续程序化叠加 |
| S12 | 已有干土/湿土对照 | 同一块干旱土地迎来首雨的连续真实镜头 | 继续检索免费素材或实拍 |
| S13 | 已有雾林和叶片雨珠照片 | 缓慢拉远的雨后雾林真实动态 | 正式版优先补真实视频；照片运镜只供预览 |

## 已取得但需正式版升级

- S02 石板当前为静帧，正式版优先补雨滴撞击石面动态。
- S03 当前为高清静帧，已足够承担 1.84 秒标题镜头，可用极轻微推近。
- S06 真实根系/林地已满足底图需求，“吸附”只需程序化局部表达，不建议再生成科幻粒子。

## 黑场/定格节拍设计（本轮只规划）

1. S01 真实雨滴撞击后，可候选 `0.24s` 黑场或冲击帧定格。
2. S11 气泡「啪」地破裂后，可候选 `0.24s` 定格。

两项都没有进入本轮预览，也没有进入任何成片。
"""
    (ROOT / "missing-assets-v1.md").write_text(content, encoding="utf-8")


def write_seedance_draft():
    content = """# 雨后泥土味｜Seedance 提示词草案 V1

> **DRAFT ONLY — 本轮严禁执行。**
> 本文档只为后续人工确认保留两个机制候选；本轮 Seedance/付费视频模型调用数为 `0`。

## 统一视觉前缀

自然纪录片与真实显微摄影质感，温和低饱和的土壤棕、苔藓绿和湿润灰褐，真实景深，光线柔和，无人物，无卡通，无科技 HUD，无蓝色实验室光，无荧光微生物，无五颜六色气味分子，无夸张大箭头，无文字、无水印。

## 候选 A｜S07｜土臭素来自哪里

- 时间范围：`17.10—21.38`（4.28秒）
- 用途：机制 A 正式动态候选
- 后期标签：` 土臭素 Geosmin `（由程序化图层叠加，不让模型生成文字）

### 镜头草案

土壤剖面的超近距移动镜头，镜头从深棕色湿润土粒之间缓慢穿过，可见细根、极少量半透明菌丝与不均匀岩石微粒。菌丝附近偶尔脱落极少量温暖灰褐色微粒，微粒被土粒表面吸附，运动极轻，不发光。整体像一段真实土壤显微纪录片，而不是科幻微观世界。竖屏 9:16，单一连续镜头，无切换，无文字。

## 候选 B｜S09–S11｜困气、气泡上升与气溶胶释放

- 时间范围：`24.30—35.06`（10.76秒）
- 用途：机制 B 一条连续镜头候选
- 前提：S08 的雨滴落向土表优先用真实高速素材；候选 B 从撞击之后的孔隙空气开始。
- 后期标签：` 困住空气 ` → ` 形成气泡 ` → ` 释放气溶胶 `（全部程序化叠加）

### 镜头草案

真实宏观纪录片质感，视线紧贴多孔土壤的湿润表面。雨滴冲击后，薄水层向凹陷孔隙内部推进，孔隙中原有空气被水封住，缩成一个小而透明的气泡。气泡在水中自然上升，来到水滴表面后迅速破裂，形成一簇极细、几乎不可见的水雾喷散到空气中。过程符合表面张力与气泡尺度，不出现大气泡、彩色分子、发光粒子、大箭头或图表。竖屏 9:16，单一连续镜头，动作因果清晰，无文字。

## 执行门禁

- 只有人工确认候选 A/B 后，才能建立正式调用任务。
- 正式调用前需再核对模型最大时长；不得通过改写锁定分镜或压缩旁白停顿迁就模型。
- 本轮不执行任何一条提示词。
"""
    (ROOT / "seedance-prompts-draft-v1.md").write_text(content, encoding="utf-8")


def write_license_notes():
    content = """# Pexels 许可核验摘要（2026-07-15）

- 许可页：https://www.pexels.com/license/
- 允许：免费使用照片/视频；可修改；不强制署名（但鼓励署名）；可用于社交媒体。
- 主要限制：不单独转售未修改副本；不得暗示人物/品牌代言；不得上传到其他素材平台；不用作商标或商号。
- 本项目素材板只用于编辑短视频的内部审核与后续社交媒体成片，不作素材转售。
"""
    (ROOT / "source-license-notes-v1.md").write_text(content, encoding="utf-8")


def write_mechanism_a():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
  <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#80624d"/><stop offset="0.48" stop-color="#5f493a"/><stop offset="1" stop-color="#2e2a25"/></linearGradient>
  <filter id="grain"><feTurbulence baseFrequency="0.42" numOctaves="3" seed="11" result="n"/><feBlend in="SourceGraphic" in2="n" mode="soft-light"/></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<rect width="1080" height="1920" fill="#1f241f"/>
<rect y="250" width="1080" height="1670" fill="url(#soil)"/>
<path d="M0 300 C160 250 270 360 450 290 S780 245 1080 320 L1080 560 L0 560Z" fill="#72583f" opacity=".84" filter="url(#grain)"/>
<path d="M110 190 C220 420 280 690 315 1030 C340 1240 300 1500 250 1760" fill="none" stroke="#b8aa7d" stroke-width="28" opacity=".73"/>
<path d="M320 770 C470 900 470 1130 390 1390" fill="none" stroke="#a99a70" stroke-width="10" opacity=".55"/>
<path d="M315 1020 C200 1150 170 1320 130 1470" fill="none" stroke="#b7aa7e" stroke-width="7" opacity=".46"/>
<g fill="#4d3b31" stroke="#9b7b5d" stroke-width="3" opacity=".9">
  <ellipse cx="570" cy="620" rx="84" ry="54" transform="rotate(-11 570 620)"/><ellipse cx="790" cy="760" rx="96" ry="62" transform="rotate(18 790 760)"/>
  <ellipse cx="575" cy="1060" rx="72" ry="47" transform="rotate(13 575 1060)"/><ellipse cx="820" cy="1240" rx="120" ry="80" transform="rotate(-14 820 1240)"/>
  <ellipse cx="520" cy="1500" rx="105" ry="64" transform="rotate(8 520 1500)"/><ellipse cx="885" cy="1610" rx="72" ry="48" transform="rotate(12 885 1610)"/>
</g>
<g fill="none" stroke="#c5bda4" stroke-width="4" opacity=".38">
  <path d="M470 850 C560 760 610 860 690 805 S835 780 910 850"/><path d="M430 905 C535 850 600 960 735 875 S880 920 965 870"/>
  <path d="M500 1210 C590 1140 650 1250 750 1170 S900 1220 970 1165"/><path d="M440 1270 C550 1200 620 1320 760 1250"/>
</g>
<g fill="#c5ae7c" opacity=".62">
  <circle cx="650" cy="890" r="7"/><circle cx="704" cy="855" r="4"/><circle cx="745" cy="922" r="5"/><circle cx="792" cy="890" r="3"/>
  <circle cx="610" cy="1230" r="4"/><circle cx="690" cy="1190" r="6"/><circle cx="760" cy="1245" r="4"/>
</g>
<g font-family="PingFang SC, Hiragino Sans GB, sans-serif" fill="#efe9d7">
  <text x="72" y="105" font-size="33" letter-spacing="5" opacity=".72">机制 A｜土壤剖面</text>
  <text x="72" y="180" font-family="Songti SC, serif" font-size="58">微生物产生泥土气息</text>
</g>
<g transform="translate(560 945)">
  <rect x="0" y="0" width="400" height="105" fill="#20251f" opacity=".82" stroke="#a79062" stroke-width="2"/>
  <text x="28" y="44" font-family="PingFang SC, sans-serif" font-size="24" fill="#c9bfa5" letter-spacing="3">微生物代谢</text>
  <text x="28" y="82" font-family="Songti SC, serif" font-size="35" fill="#f0ead2">土臭素 Geosmin</text>
</g>
<text x="72" y="1840" font-family="PingFang SC, sans-serif" font-size="24" fill="#d6cfbb" opacity=".68">真实显微纪录片方向｜无卡通细菌·无荧光·无HUD</text>
</svg>"""
    (MECHANISM_DIR / "mechanism-a-geosmin-v1.svg").write_text(svg, encoding="utf-8")


def write_mechanism_b():
    stage = []
    labels = [("困住空气", "01"), ("形成气泡", "02"), ("释放气溶胶", "03")]
    for i, (label, num) in enumerate(labels):
        x = i * 1080
        common = f"""<g transform="translate({x} 0)"><rect width="1080" height="1920" fill="#1d231f"/><rect y="980" width="1080" height="940" fill="url(#soil)"/><path d="M0 1040 C180 940 320 1090 540 1010 S850 960 1080 1050 L1080 1920 L0 1920Z" fill="#5e493a" filter="url(#grain)"/><g fill="#2f2a25" stroke="#8f745b" stroke-width="4"><ellipse cx="220" cy="1260" rx="105" ry="70"/><ellipse cx="530" cy="1410" rx="130" ry="82"/><ellipse cx="860" cy="1220" rx="112" ry="72"/><ellipse cx="760" cy="1660" rx="150" ry="90"/></g>"""
        if i == 0:
            art = """<path d="M530 180 C420 390 400 590 520 790 C650 930 790 850 820 700 C850 520 720 320 530 180Z" fill="#d7e4dd" opacity=".74" stroke="#f1f4ed" stroke-width="8"/><path d="M540 770 C520 920 580 1040 665 1120" fill="none" stroke="#dce6df" stroke-width="42" opacity=".45"/><ellipse cx="650" cy="1160" rx="98" ry="63" fill="#dbe6df" opacity=".7" stroke="#f0f3ec" stroke-width="7"/><ellipse cx="650" cy="1160" rx="47" ry="30" fill="#38433b" opacity=".9"/>"""
        elif i == 1:
            art = """<path d="M80 830 C300 700 760 730 1000 850 L1000 1120 C790 1050 260 1070 80 1150Z" fill="#b9d0c7" opacity=".42"/><ellipse cx="540" cy="980" rx="95" ry="115" fill="#dfe9e4" opacity=".67" stroke="#f4f6ef" stroke-width="8"/><ellipse cx="540" cy="980" rx="54" ry="72" fill="#435048" opacity=".9"/><g fill="none" stroke="#c8d9d2" stroke-width="6" opacity=".48"><path d="M510 1260 C470 1160 490 1100 520 1050"/><path d="M575 1260 C610 1160 590 1090 565 1040"/></g>"""
        else:
            art = """<path d="M80 930 C320 800 760 800 1000 930 L1000 1120 C800 1060 290 1070 80 1140Z" fill="#b9d0c7" opacity=".4"/><path d="M430 860 C470 810 520 790 540 720 C560 790 620 810 650 860" fill="none" stroke="#edf2ec" stroke-width="10" opacity=".8"/><g fill="#dce7e1" opacity=".68"><circle cx="540" cy="650" r="12"/><circle cx="470" cy="600" r="8"/><circle cx="620" cy="585" r="7"/><circle cx="420" cy="520" r="5"/><circle cx="680" cy="500" r="5"/><circle cx="515" cy="460" r="4"/><circle cx="595" cy="400" r="4"/></g>"""
        footer = f"""<text x="70" y="105" font-family="PingFang SC, sans-serif" font-size="30" fill="#cfc7b1" letter-spacing="5">机制 B｜{num}</text><text x="70" y="1780" font-family="Songti SC, serif" font-size="55" fill="#f0ead2">{label}</text><text x="70" y="1845" font-family="PingFang SC, sans-serif" font-size="24" fill="#cfc7b1" opacity=".7">静音也可理解的因果结构</text></g>"""
        stage.append(common + art + footer)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="3240" height="1920" viewBox="0 0 3240 1920"><defs><linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#70543f"/><stop offset="1" stop-color="#2b2924"/></linearGradient><filter id="grain"><feTurbulence baseFrequency="0.36" numOctaves="3" seed="8"/><feBlend in="SourceGraphic" mode="soft-light"/></filter></defs>""" + "".join(stage) + "<path d=\"M1080 0V1920M2160 0V1920\" stroke=\"#a79169\" stroke-width=\"3\" opacity=\".38\"/></svg>"
    (MECHANISM_DIR / "mechanism-b-aerosol-v1.svg").write_text(svg, encoding="utf-8")


def write_soil_entry():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920"><defs><linearGradient id="d" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#66755c"/><stop offset=".22" stop-color="#775c45"/><stop offset="1" stop-color="#292a25"/></linearGradient><filter id="g"><feTurbulence baseFrequency=".32" numOctaves="3" seed="4"/><feBlend in="SourceGraphic" mode="soft-light"/></filter></defs><rect width="1080" height="1920" fill="url(#d)"/><path d="M0 390 C180 330 350 430 540 360 S840 330 1080 410 L1080 1920 L0 1920Z" fill="#594536" filter="url(#g)"/><path d="M170 190 C250 420 310 720 350 1500" fill="none" stroke="#b6a777" stroke-width="24" opacity=".7"/><path d="M840 250 C760 560 780 900 700 1640" fill="none" stroke="#9f946d" stroke-width="16" opacity=".54"/><g fill="#3b3029" stroke="#8b6e56" stroke-width="3"><ellipse cx="480" cy="700" rx="95" ry="60"/><ellipse cx="720" cy="980" rx="115" ry="72"/><ellipse cx="480" cy="1320" rx="125" ry="78"/><ellipse cx="840" cy="1510" rx="90" ry="55"/></g><rect x="82" y="90" width="916" height="250" fill="#1f241f" opacity=".62"/><text x="130" y="175" font-family="PingFang SC, sans-serif" font-size="28" fill="#d7d0bc" letter-spacing="6">镜头 05｜结构草图</text><text x="130" y="260" font-family="Songti SC, serif" font-size="55" fill="#f0ead2">从地表进入土壤剖面</text><path d="M540 440 C540 690 540 900 540 1120" fill="none" stroke="#efe9d7" stroke-width="4" stroke-dasharray="8 18" opacity=".48"/><circle cx="540" cy="1135" r="10" fill="#efe9d7" opacity=".65"/><text x="130" y="1820" font-family="PingFang SC, sans-serif" font-size="24" fill="#d7d0bc" opacity=".7">程序化下潜路径｜不使用科技HUD</text></svg>"""
    (MECHANISM_DIR / "soil-entry-transition-v1.svg").write_text(svg, encoding="utf-8")


def render_svg(svg_path: Path, output_path: Path):
    width, height = {
        "mechanism-b-aerosol-v1": (3240, 1920),
        "petrichor-asset-board-v1": (2160, 3840),
    }.get(svg_path.stem, (1080, 1920))
    subprocess.run([
        str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-sandbox", f"--screenshot={output_path}",
        f"--window-size={width},{height}", svg_path.as_uri(),
    ], check=True, capture_output=True)


def ensure_posters():
    POSTER_DIR.mkdir(parents=True, exist_ok=True)
    for asset in ASSETS:
        local = ROOT / asset["local_path"]
        if local.suffix.lower() == ".mp4":
            poster = POSTER_DIR / f"{asset['asset_id']}.jpg"
            subprocess.run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", "1.5", "-i", str(local), "-frames:v", "1",
                "-vf", "scale=720:-2", "-q:v", "3", str(poster),
            ], check=True)


def data_uri(path: Path):
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def preview_path(asset_id):
    asset = ASSET_BY_ID[asset_id]
    local = ROOT / asset["local_path"]
    if local.suffix.lower() == ".mp4":
        return POSTER_DIR / f"{asset_id}.jpg"
    if local.suffix.lower() == ".svg":
        return local.with_suffix(".png")
    return local


def build_board_svg():
    width, height = 2160, 3840
    margin, gap = 100, 60
    card_w, card_h, row_step = 950, 410, 445
    out = [f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#182019"/><rect x="0" y="0" width="32" height="3840" fill="#a98467"/><style>.body{{font-family:'PingFang SC','Hiragino Sans GB',sans-serif}}.serif{{font-family:'Songti SC',serif}}</style><text x="100" y="112" class="body" font-size="30" fill="#adc178" letter-spacing="8">素材板 V1 · TASK PETRICHOR-ASSET-BOARD-V1-001</text><text x="100" y="205" class="serif" font-size="78" fill="#f0ead2">雨后的泥土味，从哪儿来？</text><text x="100" y="270" class="body" font-size="30" fill="#c8cbb9">13镜锁定时间线 · 10个真实母素材代理 · 机制A/B草图 · 付费调用0</text>"""]
    for index, shot in enumerate(SHOTS):
        col, row = index % 2, index // 2
        x = margin + col * (card_w + gap)
        y = 330 + row * row_step
        out.append(f'<g><rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" fill="#222a22" stroke="#69745d" stroke-width="2"/>')
        images = [preview_path(aid) for aid in shot["asset_ids"] if preview_path(aid).exists()]
        img_h = 245
        if images:
            seg_w = card_w / len(images)
            for j, path in enumerate(images):
                clip_id = f"clip-{index}-{j}"
                ix = x + j * seg_w
                out.append(f'<defs><clipPath id="{clip_id}"><rect x="{ix}" y="{y}" width="{seg_w}" height="{img_h}"/></clipPath></defs>')
                out.append(f'<image href="{data_uri(path)}" x="{ix}" y="{y}" width="{seg_w}" height="{img_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>')
        out.append(f'<rect x="{x}" y="{y}" width="12" height="{card_h}" fill="#a98467"/>')
        out.append(f'<text x="{x+32}" y="{y+45}" class="body" font-size="30" font-weight="600" fill="#f0ead2">{shot["id"]}  {shot["start"]:.2f}—{shot["end"]:.2f}</text>')
        out.append(f'<text x="{x+32}" y="{y+285}" class="serif" font-size="34" fill="#f0ead2">{html.escape(shot["visual"][:24])}</text>')
        out.append(f'<text x="{x+32}" y="{y+335}" class="body" font-size="24" fill="#b9c4ad">来源 {html.escape(shot["source"])} · {html.escape(shot["acquired"])}</text>')
        out.append(f'<text x="{x+32}" y="{y+380}" class="body" font-size="23" fill="#d5cfbb">Seedance {html.escape(shot["seedance"])} · 程序化 {html.escape(shot["programmatic"])} · {html.escape("/".join(shot["asset_ids"]))}</text></g>')
    fy = 3510
    out.append(f'<line x1="100" y1="{fy}" x2="2060" y2="{fy}" stroke="#77826a" stroke-width="2"/><text x="100" y="{fy+68}" class="body" font-size="29" fill="#f0ead2">当前门禁：不进入正式合成，先补 S01 / S05 / S07–S13 动态缺口并完成人工取舍。</text>')
    out.append(f'<text x="100" y="{fy+125}" class="body" font-size="26" fill="#c5cdb8">授权记录 完整 · 黑场/定格 仅规划两处、未执行 · TTS 未重生成 · 旁白未变速</text>')
    out.append(f'<text x="100" y="{fy+182}" class="body" font-size="24" fill="#9ba791">2026-07-15 · 竖屏9:16 · 本图为资产规划，不是完整成片</text></svg>')
    (ROOT / "petrichor-asset-board-v1.svg").write_text("".join(out), encoding="utf-8")


def render_board_outputs():
    board_svg = ROOT / "petrichor-asset-board-v1.svg"
    board_png = QA_DIR / "petrichor-asset-board-v1-render.png"
    board_jpg = ROOT / "petrichor-asset-board-v1.jpg"
    board_pdf = ROOT / "petrichor-asset-board-v1.pdf"
    render_svg(board_svg, board_png)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(board_png),
        "-frames:v", "1", "-q:v", "2", str(board_jpg),
    ], check=True)
    subprocess.run([
        "sips", "-s", "format", "pdf", str(board_jpg), "--out", str(board_pdf),
    ], check=True, stdout=subprocess.DEVNULL)


def build_all():
    MECHANISM_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    write_shot_plan()
    write_manifest()
    write_missing_assets()
    write_seedance_draft()
    write_license_notes()
    write_mechanism_a()
    write_mechanism_b()
    write_soil_entry()
    for name in ["mechanism-a-geosmin-v1", "mechanism-b-aerosol-v1", "soil-entry-transition-v1"]:
        render_svg(MECHANISM_DIR / f"{name}.svg", MECHANISM_DIR / f"{name}.png")
    ensure_posters()
    build_board_svg()
    render_board_outputs()
    subprocess.run([sys.executable, str(ROOT / "render_asset_board_preview.py")], check=True)


if __name__ == "__main__":
    build_all()
