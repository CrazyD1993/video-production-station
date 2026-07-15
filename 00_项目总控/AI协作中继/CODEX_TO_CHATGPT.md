---
task_id: petrichor-director-remediation-v2-001
revision: 2
status: completed_with_blocks
branch: experiment/openmontage-pilot
production_commit: 8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781
review_commit: 6d3aa60bb5fd9fe81d80004b29370c72a24730d5
reviewed_production_commit: 8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781
independent_review_complete: true
reviewer_c_approve_seedance_mechanism_generation: false
reviewer_c_approve_formal_composition: false
human_final_decision: pending
formal_composition_started: false
completion_commit: 2eb2489ecff6bba7d52ef5e568157cfd345ce03b
updated_at: "2026-07-16T00:20:00+08:00"
---

# 执行摘要

已按 UTF-8 修订版执行 `petrichor-director-remediation-v2-001`，完成 V2 动态验证生产包、不可变 Production 提交，以及基于该提交隔离快照的 Reviewer A/B/C 独立审核。

当前输出仍是 **46.80 秒动态验证预览（非成片）**。未加入旁白、字幕、音乐或正式混音；未重新生成或修改 TTS；正式合成未开始。

审核结论：Reviewer A=`BLOCK`，Reviewer B=`BLOCK`，Reviewer C 不批准新增/重试 Seedance，也不批准正式合成。`human_final_decision` 保持 `pending`。

# 两阶段提交

- Production commit：`8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781`
- Review commit：`6d3aa60bb5fd9fe81d80004b29370c72a24730d5`
- 审核证据：`/private/tmp/petrichor-v2-production-8b3b5bd`，由 Production commit 导出的隔离快照。
- A/B 在独立结论形成前未读取 Production 自评、对方报告或未提交工作区。
- 两个提交均已推送到 `experiment/openmontage-pilot`。

# Production 交付

- 输出目录：`06_成片工程/雨后泥土味/director-remediation-v2-001/`
- 干净预览：`petrichor-remediation-v2-clean-preview.mp4`
- 机制 A：`mechanism-a-v2.mp4`
- 机制 B：`mechanism-b-v2.mp4`
- QA：`qa/`
- 素材清单：`asset-manifest-v2.csv`
- 程序化依赖：`dependencies-v2.yaml`
- Seedance 日志：`seedance/call-log-v2.json`
- 逐镜状态：`shot-status.yaml`
- 生产报告：`production-report.md`

媒体实测：540×960、24fps 标称、H.264、仅视频流；预览容器时长 `46.833333` 秒。完整解码通过，三份主交付 SHA-256 已记录。

# 逐镜 Production 申报与审核裁决

Production 在提交时申报 S01—S13 全部 `done`。独立审核后，只有以下内容可直接或条件保留：

- 可保留：S03/R04 呼吸点、S04/R14 真实叶尖脱落、S10/G02 单泡上升锚点。
- 限制使用：S02、S08、S13；须后续调色、几何或衔接精修。
- 必须替换/重做：S01、S05、S06、S07、S09、S11、S12。

审核结论优先于 Production 自报状态，当前不得据 `shot-status.yaml` 的 `done` 进入正式合成。

# 素材取舍

- R14 替换未能清楚证明脱落的 R02，S04 已通过“聚集—拉长—脱落”视觉检查。
- R11 实际用于 S01，与 R07 以 22% 撞击运动参考层匹配合成；不再错误标记为未使用。
- G03 / Seedance 第 3 次候选继续弃用：开场已有气泡，缺少入水、压缩、包围过程。
- G04 / 第 4 次候选用于 S09，但 Reviewer B 仍判定气泡从画外出现，成泡因果链不连续。
- G02 的 S10 原速上升段可保留，速度比例 `1.000`。
- R14 授权记录仍缺 Mixkit 许可条款直链、版本或日期化快照，需补齐后复审。

# Seedance 真实调用

模型全部为 `doubao-seedance-2-0-fast-260128`，9:16、720p、5 秒、`generate_audio=false`，费用均为接口不可得的 `unknown`。

1. `cgt-20260715200029-2bfck`：旧 G01，废弃。
2. `cgt-20260715200457-ct6d8`：G02，仅保留 S10 上升段。
3. `cgt-20260715230936-qwwsz`：G03，新 B1 首次调用，因缺少核心前置阶段而废弃。
4. `cgt-20260715231939-bd75j`：G04，最终授权重试，Production 采用但视觉审核仍不通过。

累计 `4/4`，剩余 `0`；未调用其他付费视频模型。Reviewer C 明确不批准新增或重试 Seedance。

# 生产验证

- `python -m unittest discover -s .../tests -v`：`18/18 PASS`。
- 三份主交付 `ffmpeg -v error -i <file> -f null -`：全部完整解码、exit 0。
- clean preview 流检查：只有 `video`，无旁白、音频、字幕或正式混音。
- SHA-256：preview `97fb59fa...`；mechanism A `ff6cf2cb...`；mechanism B `e14b89d...`。
- 敏感值扫描只命中代码中的环境变量名和函数参数，没有凭据值。

生产测试通过不消除 Reviewer A 指出的测试盲点：现有复用测试没有沿 PA/PB 派生链递归计算底层母素材。

# Reviewer A / Contract QA

结论：`BLOCK`。

1. PA/PB 派生 ID 隐藏 R04、R05、R07、G02 的真实逐镜依赖与复用次数。
2. G03 的 `acquired_not_used` CSV 行列错位。
3. clean preview 有 3 处双倍帧间隔，实际 1121 帧、46.833333 秒，不是严格连续 CFR 24fps。
4. R14 缺可核验的许可条款直链/快照。

报告：`06_成片工程/雨后泥土味/reviews/director-remediation-v2-001/contract-qa.md`

# Reviewer B / Visual Director

结论：`BLOCK`；`CRITICAL 0 / MAJOR 7 / MINOR 3 / NOTE 3`。

主要阻塞：S01 撞击不可读；S05—S07 仍有拼贴、冻结和信息卡感；S09 成泡因果跳变；S11 破膜与气溶胶不可见；S12 橙色自发光更像发热/熔岩。

报告：`06_成片工程/雨后泥土味/reviews/director-remediation-v2-001/visual-director-review.md`

# Reviewer C / Review Arbiter

- `approve_seedance_mechanism_generation: false`
- `approve_formal_composition: false`
- `human_final_decision: pending`
- A/B 无实质性分歧，合同问题与视觉问题相互补充。

裁决：

- `06_成片工程/雨后泥土味/reviews/director-remediation-v2-001/review-decision.yaml`
- `06_成片工程/雨后泥土味/reviews/director-remediation-v2-001/review-summary.md`

# 下一步只需要 ChatGPT 和用户判断的事项

决定是否授权一个**不再调用 Seedance**的新整改任务，范围只包括：

1. 重做 S01、S05—S07、S09、S11、S12；
2. 递归展开底层母素材与真实复用次数，修正 G03 CSV；
3. 补 R14 许可条款证据；
4. 输出 PTS 连续的 CFR 24fps 新预览；
5. 重新建立 Production commit 并复跑 A/B/C。

在人工新授权前立即停止；不得进入正式合成，不得追加模型调用。
