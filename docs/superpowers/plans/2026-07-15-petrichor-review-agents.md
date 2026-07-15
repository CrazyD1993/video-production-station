# Petrichor Review Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立执行与审核分离的三角色轻量审核系统，并对 commit `fe82d547692b9dd0322e9ae32e9de43e14e16bb1` 完成一次独立复核。

**Architecture:** Contract QA 与 Visual Director 在互不知情的状态下并行读取同一只读 commit 快照，各自产生不同文件的报告。Review Arbiter 在两份报告完成后只读取报告和目标 commit 证据，输出统一门禁决策。

**Tech Stack:** Markdown 角色规范、YAML 决策、Git archive 只读快照、Python unittest 契约验证、FFprobe/现有联系表读取。

## Global Constraints

- 审核目标只能是 `fe82d547692b9dd0322e9ae32e9de43e14e16bb1`。
- Reviewer A/B 形成独立判断前不读取 Production Agent 自我评价或对方报告。
- 审核只读；只新建审核系统文档和报告，不修改现有生产资产。
- 不补素材、不下载、不调用任何模型、不重生成 TTS、不制作预览或成片。
- 发现的每个问题必须包含镜头号、时间位置、证据、严重程度和建议。

---

### Task 1: 审核角色和契约

**Files:**
- Create: `00_项目总控/审核Agents/README.md`
- Create: `00_项目总控/审核Agents/contract-qa.md`
- Create: `00_项目总控/审核Agents/visual-director.md`
- Create: `00_项目总控/审核Agents/review-arbiter.md`
- Test: `06_成片工程/雨后泥土味/reviews/asset-board-v1/tests/test_review_reports.py`

**Interfaces:**
- Consumes: 用户锁定的三个角色、严重程度与输出路径。
- Produces: 可复用的审核角色定义和机器可验证的报告契约。

- [x] **Step 1: 写入报告头、结论枚举和问题字段的失败测试**
- [x] **Step 2: 运行 `python3 -m unittest ... -v`，预期因角色文件/报告未存在而 FAIL**
- [x] **Step 3: 创建三个角色定义和协作顺序文档**
- [x] **Step 4: 保留测试，待审核报告产生后统一验证**

### Task 2: 指定 commit 只读快照

**Files:**
- Create outside workspace: `/private/tmp/petrichor-review-fe82d/`

**Interfaces:**
- Consumes: Git commit `fe82d547692b9dd0322e9ae32e9de43e14e16bb1`。
- Produces: 只包含素材板与锁定 TTS 的证据快照，不包含 `CODEX_TO_CHATGPT.md` 或 `STATE.yaml`。

- [x] **Step 1: 用 `git archive --output=/private/tmp/petrichor-review-fe82d.tar` 导出指定路径**
- [x] **Step 2: 解包到 `/private/tmp/petrichor-review-fe82d/`**
- [x] **Step 3: 核对快照内没有 Production 回执和中继状态**

### Task 3: 并行独立审核

**Files:**
- Create: `06_成片工程/雨后泥土味/reviews/asset-board-v1/contract-qa.md`
- Create: `06_成片工程/雨后泥土味/reviews/asset-board-v1/visual-director-review.md`

**Interfaces:**
- Consumes: 只读快照和各自角色定义。
- Produces: 两份互相独立的完整报告。

- [x] **Step 1: 并行启动 Reviewer A 和 Reviewer B**
- [x] **Step 2: 确认两者只写入各自报告路径**
- [x] **Step 3: 检查问题记录的五个必填字段**

### Task 4: 裁决与门禁

**Files:**
- Create: `06_成片工程/雨后泥土味/reviews/asset-board-v1/review-decision.yaml`
- Create: `06_成片工程/雨后泥土味/reviews/asset-board-v1/review-summary.md`

**Interfaces:**
- Consumes: Reviewer A/B 完整报告。
- Produces: Seedance 与正式合成的明确布尔门禁、阻塞项和分歧记录。

- [x] **Step 1: 待 A/B 报告都完成后启动 Reviewer C**
- [x] **Step 2: 裁决不改写 A/B 原结论**
- [x] **Step 3: 输出 YAML 决策与 Markdown 摘要**

### Task 5: 验证、中继与推送

**Files:**
- Modify: `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
- Modify: `00_项目总控/AI协作中继/STATE.yaml`

**Interfaces:**
- Consumes: 全部审核报告和验证结果。
- Produces: 可追溯的审核状态、commit SHA 和 GitHub 远端同步。

- [x] **Step 1: 运行完整契约测试，预期 PASS**
- [x] **Step 2: 运行 `git diff fe82d547... -- 06_成片工程/雨后泥土味/asset-board-v1`，预期无输出**
- [ ] **Step 3: 更新中继文档，提交并推送当前分支**
