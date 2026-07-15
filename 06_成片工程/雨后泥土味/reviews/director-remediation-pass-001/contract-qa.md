---
reviewer: Reviewer A - Contract QA
task_id: petrichor-director-remediation-pass-001
target_commit: 0da86d05b1904adb9f221f073438c11268a05d44
conclusion: BLOCK
review_scope: immutable_production_commit_snapshot
reviewed_at: 2026-07-15
---

# Reviewer A｜Contract QA

> 初始独立判断已于读取 Production 自评与状态文件前记录。证据仅来自
> `/private/tmp/petrichor-production-0da86d0/` 中锁定合同、脚本、清单、测试、QA 原始数据与实际媒体。

## 初始结论

锁定 S01–S13 的编号、顺序、名义时间范围和 46.80 秒预览规格成立；原旁白 WAV 与时间戳文件存在且参数匹配，预览按实施计划仅含临时环境声，没有发现旁白重生成或音频变速；Seedance 两次调用均落在 S09–S11 授权范围内，模型、比例、分辨率、帧率和预算符合约束；预览明确标注为“非成片”。

但当前生产包存在实际素材映射不可由清单复现、真实母素材超出既有重复上限，以及 B2 为填满锁定时间被显著慢放的问题。它们会阻断将当前预览视为合同已满足的正式合成输入，因此初始结论为 `BLOCK`。

## 问题

### CQA-01｜实际素材映射、重复次数与清单不一致

- 镜头编号：S01、S05、S08、S12
- 时间位置：`00.00–01.20`、`08.70–12.32`、`21.38–24.30`、`35.06–39.77`
- 证据：`asset-board-v1/asset-manifest-v1.csv` 将 R07 仅映射到 `S01,S12`，且素材板实施验收要求同一真实母素材时间线使用不超过 2 次；实际 `render_programmatic_shots.py` 的 `render_s01`、`render_s05`、`render_s08`、`render_s12` 都读取 R07，共跨 4 镜使用。另一方面，`asset-manifest-remediation.csv` 将 R11 映射到 `S01,S08,S12`，但 `render_dynamic_validation_preview.py` 对 S01/S08/S12 全部读取 `programmatic/Sxx.mp4`，生产组装链路没有引用 R11。R05 原清单只映射 S06，实际还作为 S05 地下底图。
- 严重程度：阻塞。素材来源清单无法重建实际预览，且 R07 的实际重复次数超过锁定素材板验收上限；授权本身可核验，但用途记录与成片证据链不一致。
- 建议：在下一生产提交中让清单逐镜对应实际渲染依赖，明确程序化衍生源；R11 若未采用应标为“已取得但未使用”，不得仍申报为预览镜头来源；将 R07 降至不超过 2 个镜头，或由总导演明确书面解除该既有重复上限后再审。

### CQA-02｜B2 变速幅度超出“轻微变速”

- 镜头编号：S10、S11
- 时间位置：`27.35–35.06`
- 证据：实际 B2 媒体 `B2_S10_S11-candidate-2.mp4` 为 `5.041667s`、24fps；`render_dynamic_validation_preview.py` 计算 `speed_factor = 7.71 / 5.041667 ≈ 1.5292` 并通过 `setpts=1.5292*PTS` 延长到 7.71 秒，即播放速度约为原速的 `65.4%`（慢放约 `34.6%`）。执行令只授权“裁切、轻微变速”，清单也未记录该显著时间重映射。
- 严重程度：阻塞。锁定时间线虽然表面保持，但通过显著慢放迁就生成结果，超出合同允许的轻微变速范围，并可能改变机制动作节奏。
- 建议：保留锁定 S10/S11 边界，使用无需显著变速即可覆盖 7.71 秒的连续素材方案；若必须采用当前 B2，应由总导演先明确批准量化的变速范围，并在状态与资产清单记录原始时长、目标时长和速度比例。

### CQA-03｜B1/B2 连续性硬要求未由生成结果满足

- 镜头编号：S09、S10
- 时间位置：`24.30–30.50`，重点为 `27.35` 交界
- 证据：`qa/seedance/B1/contact-sheet.jpg` 与 `qa/seedance/B2/contact-sheet.jpg` 显示两段土壤截面、孔隙几何和表面形态明显不同；`seedance/call-log.json` 第 2 次调用的 `decision_reason` 也明确记录 `soil geometry differs from B1`。执行令要求 B1 末帧可接 B2 首帧，并共享同一土壤截面、孔隙尺度、湿润程度、运动方向和气泡视觉语言。Production 报告承认该限制，但 `shot-status.yaml` 仍把跨该交界的 S10 标为 `done`，只把 S11 标为 `partial`。
- 严重程度：阻塞正式合成，但不否定受控调用本身。该结果可作为动态验证候选，不能申报为已满足 S09–S11 连续镜头合同。
- 建议：保持当前调用日志与候选不变；后续若在允许重试条件内重做，应以 B1 末帧作为 B2 视觉锚点，并在逐镜状态中将 S09/S10 连续性如实标为 `partial`，直到交界通过复核。

### CQA-04｜生产快照内的提交身份仍为占位值

- 镜头编号：全局
- 时间位置：全片
- 证据：`production-status.yaml` 在目标提交树内写的是 `production_commit: pending_until_commit_created`，没有自含本次完整 SHA；只读 Git 对象核验确认实际生产提交为 `0da86d05b1904adb9f221f073438c11268a05d44`，父提交为 `4b4738df6ea827dd0bdd41c8a518fa6fcb22b9c6`。该提交只新增生产包和实施计划，未包含 `reviews/director-remediation-pass-001/` 新审核结论，也未修改 `.github/` 或删除/覆盖 `reviews/asset-board-v1/`。
- 严重程度：非阻塞的流程条件。Git 历史边界和本次外部绑定 SHA 可核验，但生产快照自身不能单独回答“审核绑定哪个 production commit”；实施计划要求在后续 review commit 回填，因此不把占位值单独升级为阻塞。
- 建议：在独立审核提交中把 `production_commit` 与 `reviewed_production_commit` 都精确回填为 `0da86d05b1904adb9f221f073438c11268a05d44`，不得改写生产提交，也不得指向工作区浮动 HEAD。

## 已通过的合同项

- S01–S13 共 13 镜，编号和顺序与 `shot-plan-v1.yaml` 一致；预览总封装时长 `46.800000s`，视频 1123 帧、`46.791667s`，属于 24fps 帧量化误差。
- 原旁白为 PCM 16-bit、48kHz、单声道、`45.937042s`；时间戳请求文本仍为锁定 219 字。目标提交与父提交中的 WAV/时间戳 Git blob ID 完全相同，生产脚本未引用旁白文件，也未出现 `atempo`、`asetrate`、`rubberband` 等音频变速链。实施计划明确动态验证预览“不加入旁白和正式音乐”。
- 预览为 H.264、540×960、9:16、24fps、yuv420p；临时音频为 AAC、48kHz、单声道；完整解码无错误，实际 SHA-256 与 `qa/preview-sha256.txt` 一致。
- 13 个不同真实母素材已取得（既有 R01–R10，加 R11–R13）；新增 R11–R13 的页面、作者、平台、许可、下载日期、文件名、时间码和用途字段齐全，代理均为 H.264、720×1280、24fps、6 秒、无音轨。
- Seedance 日志为 2 次调用，未超过 4 次硬上限；仅 B1/S09 与 B2/S10–S11，模型为 `doubao-seedance-2-0-fast-260128`，9:16、720p、24fps、无生成音频，任务 ID、状态、输出、费用 `unknown` 和采用理由均有记录；没有其他付费视频模型调用证据。
- 交付文件、程序化镜头、两条 Seedance 输出、QA 数据和预览均可读取；生产测试在声明依赖环境中 8/8 通过。
- 文件名、片头固定标识和脚本均将输出定义为“总导演整改动态验证预览·非成片”；没有正式成片或提前正式合成证据。

## Production 申报一致性核对

初始判断落盘后读取 `production-report.md`、`production-status.yaml` 与 `shot-status.yaml`，结果如下：

- 一致：Production 如实声明预览非成片、正式合成关闭、旁白未加入、Seedance 共 2 次、S01/S07/S11 存在未解决项，并在报告中披露 B2 约 65.4% 原速及 B1/B2 几何限制。
- 不一致：B2 显著慢放被披露为处理方式，却未被列入 `production-status.yaml` 的 unresolved；更重要的是，跨 B1/B2 几何断裂的 S10 仍标为 `done`。
- 不一致：报告称 R11 “仅作为冲击运动参考”，但整改清单 `shot_ids` 申报 `S01,S08,S12`；实际组装和程序化源依赖没有引用 R11。R07/R05 的新增实际用途也未写回可追溯清单。
- 条件一致：目标 Git 对象确认生产与独立审核分阶段，且旧审核证据/Actions 未变；生产状态内 SHA 占位值必须在 review commit 按实施计划回填。

综上，Production 自评的诚实披露降低了伪造风险，但不能消除素材清单、变速授权和连续性硬合同的客观缺口；最终结论维持 `BLOCK`。
