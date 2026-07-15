---
task_id: petrichor-alpha-finalization-001
revision: 1
status: ready
created_by: ChatGPT
role: 总导演
target_branch: experiment/openmontage-pilot
base_production_commit: 8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781
base_review_commit: 6d3aa60bb5fd9fe81d80004b29370c72a24730d5
priority: P0
completion_commit: null
---

# 雨后泥土味｜成片 Alpha 收口任务

读取上一轮 V2 回执与 A/B/C 报告；未明确修改的仓库规则、锁定旁白、13 镜顺序和审核流程全部沿用。

## 本轮目标

结束“无声验证预览循环”，修复剩余核心画面后，输出一版可完整观看的成片 Alpha，用来判断旁白、画面、节奏和情绪是否真正成立。

本轮允许加入锁定旁白、临时字幕、既有临时环境声和基础调色；仍不是发布终版，不制作正式母版，不自动批准发布。

## 硬边界

- 不再调用 Seedance 或任何付费生成模型；当前 4/4 调用封顶。
- 不重新生成、改写或变速锁定 TTS。
- 不修改 13 镜顺序和 46.80 秒总时间线。
- S04、S10 保留；S02、S03、S08、S13只做限制性精修。
- 必须重做：S01、S05、S06、S07、S09、S11、S12。

## 画面整改

1. **S01**：替换为一眼可见的真实单滴撞击土壤事件，至少包含落下、接触、土粒/水花/即时变湿三个连续阶段。允许新增1条免费合规真实素材；不得再用静态裂土叠加弱透明运动。
2. **S05–S07**：做成同一个连续机制 A 母场景，不再分成三张说明卡。允许新增1条免费合规的真实土壤纵向剖面素材。必须连续表现：地表水沿孔隙下渗→少量物质在水膜中移动并吸附土粒→局部菌丝/微生物遇水轻微苏醒。真实土壤始终是主体，禁止矩形拼贴、霓虹管、冻结画面和大字代替动作。
3. **S09–S11**：完全放弃继续生成。以现有 S10/G02 合格上升段为固定几何锚点，用确定性程序动画补齐：可见空气腔被水包围并收缩→闭合成同一个气泡→接入 S10 原速上升→2–4帧薄膜破裂→少量极细微滴短促释放→水面轻微回落。S09不得再让气泡从画外突然出现，S11不得出现大液柱或慢慢消失。
4. **S12**：保留同一裂纹构图，取消全部橙色发光。湿润必须沿裂缝、土粒边缘和低洼区域不规则变深，并出现克制水膜反光；镜头末端仍保留干湿共存。
5. **全片统一**：压低鲜绿和霓虹感，统一黑位、湿润高光和冷湿土色；S13只统一绿色到灰绿雾林的过渡。

## 规则修正

连续机制母场景在同一 `scene_group` 内跨镜复用是允许的，不受旧“母素材最多2次”限制；但 manifest 必须递归展开真实底层母素材、派生关系和真实复用次数，禁止用 PA/PB ID 隐藏依赖。

同时修正：G03 CSV列错位、R14许可条款证据、所有媒体连续 CFR 24fps PTS。

## Alpha 交付

输出目录：

`06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/`

必须交付：

- `petrichor-alpha-v1.mp4`：46.80秒、720×1280或更高、CFR 24fps、H.264/AAC；
- 锁定旁白原速加入；
- 临时字幕仅用于审片，样式克制；
- 既有临时环境声与基础音量平衡；
- `mechanism-a-final.mp4`、`mechanism-b-final.mp4`；
- 逐镜依赖清单、许可、原始/使用时间码、速度比例；
- FFprobe、完整解码、PTS连续性、SHA、关键联系表。

## 验收与提交

沿用现有两阶段流程：

`production_commit → Reviewer A/B独立审核 → Reviewer C裁决 → review_commit`

Reviewer B必须实际按正常速度观看 Alpha，并检查 S01、机制 A、S09–S11、S12 的加密帧证据。

即使 Reviewer C 批准，也保持：

- `human_final_decision: pending`
- `release_master_started: false`

完成后更新 `CODEX_TO_CHATGPT.md`、`STATE.yaml` 和本文件状态，推送后停止。
