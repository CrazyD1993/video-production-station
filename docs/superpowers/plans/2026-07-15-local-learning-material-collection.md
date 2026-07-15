# 个人本地学习素材收集规则 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将“个人本地学习阶段最大开放搜集素材”固化为项目级长期默认规则，使后续对话不再以授权状态阻塞搜索、下载、分析或内部试剪。

**Architecture:** `AGENTS.md` 只保存简明且强制的长期默认值；`00_项目总控/素材收集与本地学习规则.md` 保存完整边界；`项目说明.md` 提供入口和用途切换说明；`GitHub同步规则.md` 只管理哪些本地素材不得入库。四个入口使用同一组术语，避免“本地学习”和“公开发布”混淆。

**Tech Stack:** Markdown、Git、`rg`、`git diff --check`

## Global Constraints

- 公开可访问素材的搜索、下载、整理、分析、素材板和内部粗剪，不以授权明确为前置条件。
- 本规则仅默认覆盖个人本地学习，不自动授权公开发布、商用、广告投放、分发或出售。
- 优先寻找无水印、无烧录字幕、无二次搬运标识的原始版本，但不主动删除或改变已有权利信息。
- 不绕过付费墙、订阅限制、DRM、加密、验证码、账号权限或平台下载限制。
- 第三方原始媒体、缓存、Cookie、账号信息和未核验素材不得提交 GitHub。
- 保留来源信息用于复查和找原版，但来源记录不得成为本地搜集门禁。

---

### Task 1: 建立长期规则入口与完整执行细则

**Files:**
- Create: `00_项目总控/素材收集与本地学习规则.md`
- Modify: `AGENTS.md:17-27`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-07-15-local-learning-material-collection-design.md`
- Produces: 所有后续 Agent 必读的简明默认规则，以及可被其他项目文档链接的完整规范。

- [ ] **Step 1: 创建完整执行细则**

在 `00_项目总控/素材收集与本地学习规则.md` 写入：适用范围、最大开放搜集规则、无水印原版策略、禁止突破访问控制、来源最小记录、GitHub 隔离、用途转为发布时重新核验。

- [ ] **Step 2: 更新 AGENTS.md**

在“内容安全”和“GitHub 同步”之间增加“素材收集与本地学习”章节，明确：

```markdown
## 素材收集与本地学习

- 项目默认按个人本地学习处理；公开可访问素材均可搜索、下载、整理、分析并用于本地素材板或内部粗剪，不以授权明确为搜集前置条件。
- 优先寻找无水印、无烧录字幕、无二次搬运标识的原始版本；不得主动删除或改变已有水印、作者标识或其他权利管理信息。
- 不绕过付费墙、DRM、验证码、账号权限或平台访问控制；第三方原始媒体和未核验素材只保存在本地，不提交 GitHub。
- 来源记录用于复查、找原版和未来授权，不得阻塞本地搜集；任务转为公开发布、商用、投放或分发时，再按 `00_项目总控/素材收集与本地学习规则.md` 重新核验。
```

- [ ] **Step 3: 验证核心规则可被新对话发现**

Run:

```bash
rg -n "个人本地学习|不以授权明确|不绕过付费墙|不提交 GitHub|重新核验" AGENTS.md 00_项目总控/素材收集与本地学习规则.md
```

Expected: 两个文件均命中；`AGENTS.md` 至少命中五个核心概念。

### Task 2: 对齐项目入口与 GitHub 边界

**Files:**
- Modify: `00_项目总控/项目说明.md:9-16,75-80`
- Modify: `00_项目总控/GitHub同步规则.md:7-20`

**Interfaces:**
- Consumes: `00_项目总控/素材收集与本地学习规则.md`
- Produces: 项目级规则入口和与开放搜集相容的 GitHub 排除策略。

- [ ] **Step 1: 在项目说明增加用途分层**

增加“素材使用模式”章节，链接完整规则并明确：默认是个人本地学习；本地学习允许权利状态未知的公开素材进入候选池和内部粗剪；公开发布或商用必须另行切换模式并核验。

- [ ] **Step 2: 修正版本与备份表述**

将“未经授权的第三方视频”改为更完整的“第三方原始视频、图片、音频和未核验素材”，避免被误读为“不能下载到本地”，并明确限制仅针对 GitHub 入库。

- [ ] **Step 3: 更新 GitHub 同步检查**

将“检查敏感信息和未授权素材”改为“检查敏感信息和不应入库的第三方原始媒体”，并保留原始下载视频、来源不明图片和音乐不得上传的现有边界。

- [ ] **Step 4: 运行一致性检查**

Run:

```bash
rg -n "只有权利状态明确|授权明确后|不得下载|不进入成片|未获授权素材" AGENTS.md 00_项目总控/项目说明.md 00_项目总控/GitHub同步规则.md 00_项目总控/素材收集与本地学习规则.md
```

Expected: 不出现把“授权明确”设为个人本地搜集前置条件的冲突表述；发布阶段或 GitHub 排除语境中的命中允许保留。

### Task 3: 验证、提交并同步

**Files:**
- Verify: `AGENTS.md`
- Verify: `00_项目总控/素材收集与本地学习规则.md`
- Verify: `00_项目总控/项目说明.md`
- Verify: `00_项目总控/GitHub同步规则.md`

**Interfaces:**
- Consumes: Task 1-2 的四份文档修改。
- Produces: 可追溯且已同步到私有 GitHub 的长期项目规则。

- [ ] **Step 1: 检查 Markdown 与差异**

Run:

```bash
git diff --check
git diff -- AGENTS.md 00_项目总控/素材收集与本地学习规则.md 00_项目总控/项目说明.md 00_项目总控/GitHub同步规则.md
```

Expected: `git diff --check` 无输出；差异只包含本次规则同步。

- [ ] **Step 2: 检查未跟踪文件隔离**

Run:

```bash
git status --short
```

Expected: 能识别用户已有的其他未跟踪文件；提交时只暂存本计划列出的四份文档和本实施计划，不纳入无关文件。

- [ ] **Step 3: 提交规则修改**

```bash
git add -- AGENTS.md 00_项目总控/素材收集与本地学习规则.md 00_项目总控/项目说明.md 00_项目总控/GitHub同步规则.md docs/superpowers/plans/2026-07-15-local-learning-material-collection.md
git commit -m "docs: open local learning material collection"
```

- [ ] **Step 4: 推送当前试验分支**

```bash
git push origin experiment/openmontage-pilot
```

Expected: 当前分支提交成功同步到 GitHub 私有仓库。
