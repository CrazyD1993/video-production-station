---
task_id: petrichor-director-remediation-pass-001
status: completed
branch: experiment/openmontage-pilot
production_commit: 0da86d05b1904adb9f221f073438c11268a05d44
review_commit: a6250d9287b2f44c0e6fe6376699c9d1c94080f9
reviewed_production_commit: 0da86d05b1904adb9f221f073438c11268a05d44
independent_review_complete: true
reviewer_c_approve_formal_composition: false
human_final_decision: pending
completed_at: "2026-07-15T20:35:24+08:00"
---

# 执行摘要

已按修订版 3 完成“总导演整改动态验证预览”的生产、验证、独立 Production 提交，以及基于该完整 SHA 隔离快照的 Reviewer A/B/C 审核。当前输出明确为**动态验证预览（非成片）**；没有重新生成 TTS、没有修改或变速旁白、没有制作正式字幕或正式成片。

两位独立 Reviewer 均结论 `BLOCK`，Reviewer C 不批准进入正式合成。C 仅批准在现有 4 次硬上限内，最多再进行 2 次定向 Seedance 新增/重试；本轮在裁决后没有继续调用，最终决定留给 ChatGPT 总导演。

# 两阶段提交

- Production 完成：`true`
- Production commit：`0da86d05b1904adb9f221f073438c11268a05d44`
- Production 已推送：`experiment/openmontage-pilot`
- 独立审核完成：`true`
- Review commit：`a6250d9287b2f44c0e6fe6376699c9d1c94080f9`
- Reviewed production commit：`0da86d05b1904adb9f221f073438c11268a05d44`
- 审核证据模式：同一 production commit 的 `/private/tmp` 隔离快照；A/B 未使用未提交工作区证据。

# Production 交付

- 输出目录：`06_成片工程/雨后泥土味/director-remediation-pass-001/`
- 动态预览：`petrichor-director-remediation-preview-v1.mp4`
- 参数：46.800 秒、540×960、24fps、H.264；临时 AAC 单声道环境声 48kHz。
- 旁白：未加入预览；锁定 WAV/时间戳未修改、未重生成、未变速。
- 逐镜生产状态：9 个 `done`，4 个 `partial`（S01、S06、S07、S11），0 个 `blocked`。该状态是 Production 申报，不等同于独立审核通过。
- 真实素材：新增 R11、R12、R13 三个 Pexels 审片代理；R12/R13 用于 S13 动态结尾，R11 只取得作为雨落湿地表参考，实际组装未采用。
- QA：FFprobe、SHA-256、完整解码、程序化联系表、Seedance 联系表、13 镜中点联系表均已落盘。

# 工作包状态

- S01：Production `partial`；Reviewer B 判定撞击响应不可信，阻塞。
- S05：Production `done`；Reviewer B 判定跨照片叠化未建立真实入渗空间，阻塞。
- S07：Production `partial`；未调用 Seedance，但仍有明显 PPT/机制卡感，阻塞。
- S08：Production `done`；Reviewer B 判定程序化雨滴不可信且不能连接 S09，阻塞。
- S09：Production `done`；Reviewer B 判定 G01/B1 方向错误、主体下移/跳位，`CRITICAL`，必须废弃。
- S10：Production `done`；仅 G02/B2 的上升段可条件保留为下一版视觉锚点，跨 S09/S10 连续性未通过。
- S11：Production `partial`；大液柱/大液滴不能表达极细气溶胶，阻塞。
- S12：Production `done`；同构图几何成立，但湿润像圆形调暗遮罩，过程未通过。
- S13：Production `done`；R13→R12 有真实内部运动，后续可延后统一色彩与“苏醒”情绪。

# 素材来源

完整来源、作者、平台、许可、下载日期、时间码、用途和限制：

- `asset-manifest-remediation.csv`
- R11：Pexels 4171514 / Magda Ehlers / Pexels License。
- R12：Pexels 32675101 / PUWOOK Kwak / Pexels License。
- R13：Pexels 32679329 / Rahime Gül / Pexels License。

原始下载文件只在 `/private/tmp`，未推送；仓库只包含低清无声审片代理。审核指出实际程序化依赖与清单仍不一致：R07 被跨 4 镜派生使用、R11 清单映射但组装未引用、R05 新用途未写回，下一生产提交必须重建逐镜证据链。

# Seedance 真实调用

模型固定 `doubao-seedance-2-0-fast-260128`，9:16、720p、24fps、`generate_audio=false`，仅 S09—S11：

1. B1 / S09：task `cgt-20260715200029-2bfck`，`succeeded`，费用 `unknown`，输出 `seedance/outputs/B1_S09-candidate-1.mp4`。独立视觉审核判定物理方向错误，不得进入正式合成。
2. B2 / S10—S11：task `cgt-20260715200457-ct6d8`，`succeeded`，费用 `unknown`，输出 `seedance/outputs/B2_S10_S11-candidate-2.mp4`。仅气泡上升段可条件保留；与 B1 几何不连续，破裂尾部不合格。

累计 2 次；未调用其他付费视频模型。Reviewer C 允许最多再用剩余 2 次做定向补救，但本轮未执行追加调用。

# 验证命令与结果

- `python -m unittest discover ... -v`：8/8 PASS。
- `ffmpeg -v error -i <preview> -f null -`：PASS，无解码错误。
- YAML 解析：PASS。
- 敏感值/临时签名 URL 扫描：PASS。
- `.github/` diff：无修改。
- 旧 `reviews/asset-board-v1/`：未删除、未覆盖。

生产验证详见：`06_成片工程/雨后泥土味/director-remediation-pass-001/qa/verification.md`。

# Reviewer A/B/C 结论

- Reviewer A / Contract QA：`BLOCK`。
  - 素材映射、重复次数与实际依赖不一致；
  - B2 从 5.041667 秒扩到 7.71 秒，约为原速 65.4%，超出“轻微变速”；
  - B1/B2 连续性硬要求未满足；
  - Production SHA 占位值作为非阻塞流程项，在 Review 阶段回填。
- Reviewer B / Visual Director：`BLOCK`。
  - 1 `CRITICAL`、9 `MAJOR`、2 `MINOR`、1 `NOTE`；
  - G01/B1 必须替换；S01、S05、S07、S08、S11、S12 为核心视觉阻塞。
- Reviewer C / Review Arbiter：
  - `approve_seedance_mechanism_generation: true`，只批准最多 2 次定向新增/重试；
  - `approve_formal_composition: false`；
  - 无实质性审核分歧；A/B 证据互补；
  - `human_final_decision: pending`。

# 审核输出

- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/contract-qa.md`
- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/visual-director-review.md`
- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/review-decision.yaml`
- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/review-summary.md`

# 未解决问题

1. 废弃 G01/B1，以 G02/B2 可保留的 S10 上升段作为统一截面锚点重做 B1。
2. S01/S08 需要可信撞击并进入同一机制空间；S05/S07/S11/S12 需按审核报告重做。
3. S04 应改用 R02 真正落滴的后段；S06 需真实或程序化吸附状态变化。
4. B2 不能继续依赖约 65.4% 原速的显著慢放来填满 7.71 秒，除非总导演书面批准量化范围并完整记录。
5. 素材清单必须能逐镜重建实际渲染依赖并满足重复限制。

# 建议 ChatGPT 下一步只做的判断

只判断是否授权一个新的 `remediation-v2` 生产任务，并将剩余最多 2 次 Seedance 调用严格限定为：以 G02/B2 上升段为视觉锚点重做 B1、必要时补 S11 破裂尾部。**不要批准正式合成，不要在读取三份新审核报告前扩大调用范围。**
