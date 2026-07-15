---
reviewer: Reviewer A - Contract QA
task_id: petrichor-director-remediation-v2-001
target_commit: 8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781
conclusion: BLOCK
evidence_snapshot: /private/tmp/petrichor-v2-production-8b3b5bd
reviewed_at: 2026-07-15
---

# Reviewer A｜Contract QA

## 审核边界

- 唯一生产证据快照：`/private/tmp/petrichor-v2-production-8b3b5bd`
- 绑定 production commit：`8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781`
- 本结论未读取当前工作区或快照内的 `production-report.md`、`unresolved-items.md`、Production 自评及任何 Reviewer B/C 报告。
- 审核只核验合同、文件、参数、调用门禁和证据链，不代替视觉导演审美裁决。

## 结论

`BLOCK`

13 镜顺序、名义时间线、必要媒体、Seedance 4/4 门禁、模型与调用范围、±8% 速度限制、R11 实际状态以及“非正式成片”边界基本成立；但逐镜素材清单没有如实展开程序化派生片段的底层母素材，导致真实复用次数被低报，直接违反本轮素材证据链硬门禁。另有未采用候选的 CSV 列错位、预览帧时间戳不连续及新素材许可链接不足。当前生产包不能作为合同通过的正式合成输入。

## 问题

### CQA-V2-01｜底层母素材复用被 PA/PB 派生 ID 隐藏

- 镜头编号：S01、S03、S05、S06、S07、S08、S09、S10、S11、S12
- 时间位置：`00.00–01.20`、`03.85–05.69`、`08.70–35.06`、`35.06–39.77`
- 证据：`dependencies-v2.yaml` 与 `render_remediation_v2.py::_soil_column()` 明确显示 S05–S07 每镜都依赖 R04、R05、R07；因此真实使用为 R04 共 4 镜（S03、S05–S07）、R05 共 3 镜（S05–S07）、R07 共 5 镜（S01、S05–S07、S12）。但 `asset-manifest-v2.csv` 用 PA05/PA06/PA07 替代底层母素材，只把 R07 计为 S01、S12 两次。相同问题也发生在机制 B：参考包和渲染代码显示 G02 派生几何/帧用于 S08、S09 桥接、S10、S11，清单却只把 G02 直接计入 S10。生产测试 `test_manifest_is_traceable_and_reuse_is_at_most_two` 仅按 CSV 的 `mother_asset_id` 计数，因而把派生输出误当独立母素材并得到虚假的 `<=2`。
- 严重程度：阻塞。本轮执行令要求逐镜记录“实际母素材、程序化派生来源、母素材真实复用次数”，并点名 R07 不得继续隐性跨 4 镜使用；Production 门禁还规定素材清单无法重建真实依赖时不得申报相应镜头 `done`。当前清单与全部镜头 `done` 声明不相容。
- 建议：下一生产提交应把 R04/R05/R07/G02 等底层依赖逐镜展开，增加明确的 `underlying_mother_asset_id` 与 `true_reuse_count`，并让复用测试沿派生关系递归计数；若真实母素材复用仍超过约束，应更换来源或取得总导演书面新授权后再审。

### CQA-V2-02｜G03 未采用记录发生 CSV 列错位

- 镜头编号：S09
- 时间位置：`24.30–27.35`（未采用候选不进入预览）
- 证据：`asset-manifest-v2.csv` 的 G03 行在 `target_duration=0.00` 后只写了一个 `N/A`，导致 CSV 解析结果为 `derivation=acquired_not_used`、`usage_status="Project account-generated output; ..."`、`license_record` 为空，而不是预期的 `usage_status=acquired_not_used`。该文件是 Seedance 第 3 次真实付费调用产物 `B1_S09_v2-candidate-3.mp4`；实际文件存在且 SHA-256 为 `ee9c0e877149b57a552d52485dc191a9740dbdf1adb7a42c0ce7e0d7548f0533`。
- 严重程度：中等，需修正后复审。调用日志本身仍记录了真实任务和弃用原因，所以不构成调用伪造；但“已取得但未采用素材”这一必填契约在机器可读清单中失败。
- 建议：补齐 G03 行的 `actual_speed_ratio`、`derivation`、`usage_status=acquired_not_used` 和 `license_record` 对应列，并新增测试断言所有行列数与表头一致、`usage_status` 只能取允许枚举。

### CQA-V2-03｜干净预览并非连续 24fps 时间戳

- 镜头编号：S01、S02、S03、全局
- 时间位置：约 `01.17`、`03.79`、`05.67` 及全片
- 证据：实际 `petrichor-remediation-v2-clean-preview.mp4` 只有视频流，H.264、540×960，`r_frame_rate=24/1`；但 `avg_frame_rate=6726/281`（约 23.936fps）、`nb_frames=1121`、封装时长 `46.833333s`，而非连续 24fps 下的 46.80 秒。逐帧 PTS 检查在 `1.125000→1.208333`、`3.750000→3.833333`、`5.625000→5.708333` 出现 0.083333 秒间隔，均为正常 0.041667 秒帧间隔的两倍。S04 代理和成镜实际均为 `3.000000s`，清单却写原始/目标 `3.01s`。
- 严重程度：中等技术条件。总时长偏差仅 0.033333 秒，媒体可完整解码且没有黑帧/损坏证据；但三处时间戳缺帧使“24fps、锁定 46.80 秒”不能按严格技术合同判定为完全通过。
- 建议：重封装前统一每段 PTS、以连续 CFR 24fps 输出，并验证相邻视频帧 PTS 恒为 `1/24s`、总时长落在一个帧量化方案内；同时把 S04 实际 3.000 秒或相应帧量化值写回清单。

### CQA-V2-04｜R14 新素材授权记录缺少许可条款链接

- 镜头编号：S04
- 时间位置：`05.69–08.70`
- 证据：`asset-manifest-v2.csv` 的 R14 行记录了 Mixkit 素材页、下载日期、用途和 `Mixkit Stock Video Free License`，并诚实写明 `uploader not exposed on page`；但没有提供可核验的许可条款 URL、许可版本或本地许可快照。R14 文件可读取，H.264、540×960、24fps、3.000秒、无音轨，现有动作联系表显示水滴脱落事件。
- 严重程度：中等合规条件。未发现来源伪造，但仅凭许可名称和素材页不足以独立复核“社交媒体编辑允许”的具体条款；作者不可得已有明确记录，不按伪造处理。
- 建议：补充 Mixkit 对应该素材的许可条款直链或日期化许可快照，并将“作者/上传者未公开”保留为明确不可得值。

## 已通过项

- `shot-status.yaml` 含 S01–S13 共 13 镜，编号、顺序和名义起止时间与锁定合同一致；每镜状态均为允许枚举。
- 必需交付存在且可读取：`mechanism-a-v2.mp4`、`mechanism-b-v2.mp4`、`petrichor-remediation-v2-clean-preview.mp4`、逐镜文件、manifest、dependencies、Seedance 日志、FFprobe、解码、SHA、镜头中点和连续性 QA。
- 三份主交付媒体 SHA-256 与 `qa/media-sha256.txt` 一致；预览、机制 A、机制 B 完整解码均为 exit 0，无错误输出。
- 预览只有一条视频流，没有旁白、音频流、字幕流或正式混音；渲染入口全程 `-an`，未读取锁定 TTS，也未出现音频变速链。
- 预览画面未使用上一版顶部/底部全宽调试黑条；代码只在部分机制镜头使用安全角落小标签。文件名、渲染脚本文档和依赖声明均将其限定为动态验证预览，不存在越权制作正式成片的证据。
- Seedance 日志累计 `4/4`：前序 2 次、本轮新 B1 两次；本轮第一次用于 B1，第 3 次候选因缺少核心前置物理阶段而触发允许的 B1 重试，第 4 次仍用于 B1。全部模型为 `doubao-seedance-2-0-fast-260128`、9:16、720p、5秒、无生成音频，真实 task id、状态、输出、费用 `unknown`、采用/弃用理由均有记录；未发现其他付费视频模型或越权镜头调用。
- 实际渲染未使用 `setpts` 倍率、`minterpolate` 或其他显著重定时；S09/G04 与 S10/G02 都按原速裁切，清单速度比例为 1.000，符合 ±8% 门禁。
- R11 状态已从上一轮“申报但未使用”修正为 S01 的真实撞击运动参考层；`render_remediation_v2.py` 实际读取 R11，并以 22% 与 R07 干裂土基底匹配合成，清单与代码在这一点一致。R11 未被申报为独立的干土实拍。
- R14 实际文件和动作联系表支持 S04 的真实脱落事件；除许可条款直链问题外，来源、下载日期和用途已记录。
- 声明依赖环境下生产测试实测 18/18 通过；其中素材复用测试存在 CQA-V2-01 所述覆盖盲点，不能据此消除底层复用问题。
