# Petrichor Director Remediation Pass 001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 按锁定 S01–S13 时间线完成雨后泥土味动态整改预览，先形成独立 production commit，再对该 SHA 完成 A/B/C 独立审核和 review commit。

**Architecture:** 在 `06_成片工程/雨后泥土味/director-remediation-pass-001/` 建立独立生产包。真实外部视频只保留 720×1280 无声审片代理；S05/S07/S08/S12 由 Pillow/Numpy 程序化渲染，S09–S11 使用两条受预算约束的 Seedance 候选，最后以 FFmpeg 组装 46.80 秒动态验证预览并生成 QA 证据。生产提交之后从该 SHA 导出隔离快照，A/B 并行审核，C 后置裁决。

**Tech Stack:** Python 3、Pillow、NumPy、FFmpeg/FFprobe、Volcengine Ark REST API、Markdown/YAML/CSV、Git archive、unittest。

## Global Constraints

- 锁定 S01–S13 编号、顺序和 `0.00–46.80` 时间范围，不修改旁白文字、旁白文件或速度。
- 输出只能标记为“总导演整改动态验证预览·非成片”，正式合成门禁保持关闭。
- S07 禁止 Seedance；S09–S11 仅允许模型 `doubao-seedance-2-0-fast-260128`。
- Seedance 比例 `9:16`、分辨率 `720p`、24fps 统一转码；B1/B2 首轮各一次，硬上限 4 次。
- 付费调用的任务 ID、真实参数、状态、输出、费用和采用理由必须记录；费用不可得写 `unknown`。
- 新外部素材必须记录页面、作者、平台、许可、下载日期、文件名、时间码和镜头用途。
- 不提交原始下载文件、凭据、Cookie 或 API Key；只提交审片代理、生成结果、预览和证据。
- 不修改 GitHub Actions，不删除或覆盖 `reviews/asset-board-v1/`。
- 硬顺序：`production_commit → A/B 隔离审核 → C 裁决 → review_commit`。

---

### Task 1: 生产包契约与失败测试

**Files:**
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/tests/test_production_contract.py`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/.gitignore`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/requirements-render.txt`

**Interfaces:**
- Consumes: 锁定 `asset-board-v1/shot-plan-v1.yaml`。
- Produces: 对 13 镜、状态枚举、媒体参数、Seedance 上限和禁止正式成片的自动验证。

- [ ] **Step 1:** 写测试，要求 `shot-status.yaml` 包含 S01–S13 且时间精确、状态只能为 `done/partial/blocked`。
- [ ] **Step 2:** 写测试，要求 `seedance/call-log.json` 的模型固定、调用数不超过 4 且每条包含真实任务字段。
- [ ] **Step 3:** 写测试，要求预览为 540×960、24fps、46.80 秒、文件名和画面标记均包含“preview/non-final”语义。
- [ ] **Step 4:** 运行 `python3 -m unittest discover -s .../tests -p 'test_*.py' -v`，确认因生产文件不存在而 FAIL。

### Task 2: 外部真实素材与来源清单

**Files:**
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/assets/real-proxy/R11-pexels-4171514-ground-rain-impact-proxy.mp4`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/assets/real-proxy/R12-pexels-32675101-misty-forest-motion-proxy.mp4`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/assets/real-proxy/R13-pexels-32679329-rain-leaves-forest-proxy.mp4`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/asset-manifest-remediation.csv`

**Interfaces:**
- Consumes: Pexels 页面 4171514、32675101、32679329 的公开官方文件链接。
- Produces: H.264 720×1280、24fps、无音轨代理，以及完整来源和许可记录。

- [ ] **Step 1:** 下载原文件到 `/private/tmp/petrichor-remediation-sources/`，不写入 Git 工作区。
- [ ] **Step 2:** 用 FFmpeg 生成竖屏无声代理；R11 取冲击清晰时间段，R12/R13 保留内部运动。
- [ ] **Step 3:** 生成联系表并人工查看；不满足镜头功能的素材不得标 `done`。
- [ ] **Step 4:** 写 CSV，记录来源页面、作者、Pexels License、下载日期、时间码和用途。

### Task 3: 程序化整改渲染器

**Files:**
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/render_programmatic_shots.py`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/tests/test_programmatic_renderer.py`
- Create outputs: `programmatic/S01.mp4`, `S05.mp4`, `S07.mp4`, `S08.mp4`, `S12.mp4`

**Interfaces:**
- `render_shot(shot_id: str, output: Path) -> dict` 返回帧数、时长、分辨率和视觉事件标记。
- S01 输出落滴、撞击、湿斑；S05 输出地表下潜和水进入孔隙；S07 输出休眠到唤醒及 `土臭素 Geosmin`；S08 输出接近与撞击；S12 输出同一构图连续变湿。

- [ ] **Step 1:** 写失败测试，验证每个镜头帧数等于锁定时长×24，并验证事件标记齐全。
- [ ] **Step 2:** 运行测试，确认 `render_programmatic_shots` 不存在而 FAIL。
- [ ] **Step 3:** 用 Pillow/Numpy 实现 540×960 帧渲染和 FFmpeg 编码；背景使用 R07/R05/机制草图，内部运动不使用长时间 Ken Burns。
- [ ] **Step 4:** 渲染五段并运行测试，确认 PASS；输出 QA 静帧。

### Task 4: Seedance B1/B2 受控调用

**Files:**
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/seedance/seedance_client.py`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/seedance/prompts/B1.yaml`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/seedance/prompts/B2.yaml`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/seedance/call-log.json`
- Create outputs: `seedance/videos/B1.mp4`, `seedance/videos/B2.mp4`
- Test: `06_成片工程/雨后泥土味/director-remediation-pass-001/tests/test_seedance_client.py`

**Interfaces:**
- `build_request(prompt: str, duration: int) -> dict` 固定模型、9:16、720p、无音频。
- `create_task(api_key: str, request: dict) -> str`；`poll_task(api_key: str, task_id: str) -> dict`；`download_result(url: str, output: Path)`。

- [ ] **Step 1:** 写失败测试，验证请求体、预算计数和日志必填字段，不调用网络。
- [ ] **Step 2:** 实现最小客户端并让测试 PASS。
- [ ] **Step 3:** 从本机已有安全环境读取 `ARK_API_KEY`，不打印或落盘；B1/B2 各提交一次。
- [ ] **Step 4:** 轮询、下载、统一转码为 720×1280/24fps/无音轨并记录真实任务结果；接口不可用则标 `blocked`，不得伪造。
- [ ] **Step 5:** 查看 B1 末帧与 B2 首帧；只有物理错误、主体消失、严重断裂或损坏才允许单条重试一次。

### Task 5: 动态验证预览、状态与 QA

**Files:**
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/render_dynamic_validation_preview.py`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/shot-status.yaml`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/production-status.yaml`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/petrichor-director-remediation-preview-v1.mp4`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/qa/preview-ffprobe.json`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/qa/preview-contact-sheet.jpg`
- Create: `06_成片工程/雨后泥土味/director-remediation-pass-001/production-report.md`

**Interfaces:**
- Consumes: 锁定真实素材、五段程序化视频和 B1/B2。
- Produces: 46.80 秒动态验证预览、13 镜逐项状态、临时声音和机器可读 QA。

- [ ] **Step 1:** 组装 S01–S13，所有镜头严格使用锁定时长；叠加固定“动态验证预览·非成片”标记。
- [ ] **Step 2:** 生成临时环境声：干旱近静默、单滴撞击、地下低频、气泡释放、结尾环境展开；不加入旁白和正式音乐。
- [ ] **Step 3:** 写 `shot-status.yaml`，对 S01/S05/S07/S08/S09–S11/S12/S13 分别如实标 `done/partial/blocked` 并给证据路径。
- [ ] **Step 4:** 生成 FFprobe、联系表、SHA-256 和生产报告。
- [ ] **Step 5:** 运行全部生产测试、完整解码和 `git diff` 范围检查。

### Task 6: Production 独立提交

**Files:**
- Modify: `06_成片工程/雨后泥土味/director-remediation-pass-001/production-status.yaml`

**Interfaces:**
- Produces: `production_complete` 和不可变 `production_commit`。

- [ ] **Step 1:** 确认提交只含生产整改、素材记录、动态预览和生产测试证据，不含新审核结论。
- [ ] **Step 2:** 提交并取得完整 SHA；审核立即绑定该 SHA。`production_commit` 的 SHA 回填保留在工作区，随阶段 2 的回执状态和审核报告一起进入 review commit，不再插入额外生产提交。
- [ ] **Step 3:** 推送并从最终生产资产 SHA 导出只读隔离快照。

### Task 7: A/B/C 独立审核

**Files:**
- Create: `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/contract-qa.md`
- Create: `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/visual-director-review.md`
- Create: `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/review-decision.yaml`
- Create: `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/review-summary.md`

**Interfaces:**
- Consumes: 同一个 `production_commit` 隔离快照。
- Produces: Reviewer A/B 独立报告、Reviewer C 后置裁决。

- [ ] **Step 1:** A/B 并行启动；两者不得读取 Production 自评、对方报告或工作区浮动 HEAD。
- [ ] **Step 2:** A/B 完成后启动 C；C 保留原结论并给出正式合成布尔门禁。
- [ ] **Step 3:** 验证四份报告目标 SHA 完全一致，且旧审核目录未覆盖。

### Task 8: Review 提交、中继和远端同步

**Files:**
- Modify: `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
- Modify: `00_项目总控/AI协作中继/STATE.yaml`
- Modify: `00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md`

**Interfaces:**
- Produces: `independent_review_complete`、`review_commit`、`reviewed_production_commit`、`reviewer_c_approve_formal_composition`、`human_final_decision: pending`。

- [ ] **Step 1:** 写完整回执和状态，保持 `human_final_decision: pending`。
- [ ] **Step 2:** 提交审核报告与中继，回填 `completion_commit` 并形成最终同步提交。
- [ ] **Step 3:** 运行最终测试、YAML 解析、资产范围、Actions 未修改和旧审核证据未删除检查。
- [ ] **Step 4:** 推送 `experiment/openmontage-pilot` 并核对远端 SHA。
