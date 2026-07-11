---
task_id: relay-bootstrap-001
status: completed
branch: experiment/openmontage-pilot
commit_sha: 9f31f5413d6521eec5dd6f97d4e04f9418b1d0ec
completed_at: "2026-07-11T15:37:06+08:00"
---

# 执行摘要

建立 ChatGPT 与 Codex 的 GitHub 中继三文件，将“读取GitHub中继任务”固化为仓库长期规则，并修正 KF1-01/KF1-02 的真实参考图门禁和结构标记范围。本轮没有生成候选图、调用 Seedance 或制作视频。

# 修改文件

- `00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md` — 新增 — 建立 ChatGPT 任务入口，初始状态为 `empty`。
- `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md` — 新增 — 保存最新完整执行回执。
- `00_项目总控/AI协作中继/STATE.yaml` — 新增 — 保存当前分支、阶段、门禁和下一执行者。
- `AGENTS.md` — 修改 — 固化中继读取、执行、回执、提交与安全规则。
- `08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/prompts/KF1-01.yaml` — 修改 — 增加真实参考图必需门禁，取消结构示意叠加要求。
- `08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/prompts/KF1-02.yaml` — 修改 — 增加真实参考图必需门禁，取消结构示意叠加要求。
- `08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/README.md` — 修改 — 记录 KF1 参考图的使用、授权与阻塞规则。
- `08_OpenMontage试验/03-生产清单模板.yaml` — 修改 — 在 KF1 候选状态中记录 `reference_image_required: true`。
- `scripts/validate_phase2_semantics.py` — 修改 — 校验 KF1 真实参考图门禁，并只对 KF2/KF3 要求结构标记。
- `tests/test_validate_phase2_semantics.py` — 修改 — 增加 KF1/KF2/KF3 标记范围回归测试。
- `tests/test_ai_relay_contract.py` — 新增 — 校验中继文件、front matter、状态和 AGENTS 长期入口。

# 实际执行的命令

- `git branch --show-current`
- `git status --short`
- `python -m unittest tests.test_ai_relay_contract tests.test_validate_phase2_semantics -v`
- `python -m unittest discover -s tests -v`
- `python scripts/validate_timeline.py`
- `python scripts/validate_phase2_semantics.py`
- `git diff --check`
- `git diff --cached --check`
- `git commit`
- `git push origin experiment/openmontage-pilot`

# 测试与验证

- 全量单元测试：已执行 29 项，通过 29，失败 0。
- 时间轴校验：已执行，25 秒/6 镜头、29 秒/6 镜头、12 秒/3 镜头全部通过。
- Phase 3 语义校验：已执行，核心机制、六份关键帧、KF1 参考图门禁和 KF2/KF3 结构标记全部通过。
- 未执行图片尺寸和联系表生成：本轮没有候选图输入。
- 未查看生成图或成片：本轮按禁止条件未生成任何媒体。

# 与任务要求的差异

- 中继文件按要求建立，无功能缩减。
- 为确保长期规则在新任务中可被发现，额外将中继入口写入 `AGENTS.md`。
- 回执中的 `commit_sha` 在首次实现提交后回填；这是解决文件无法预知自身提交 SHA 的必要两步提交。
- 工具限制：无。
- 需要人工处理：无。

# 当前阻塞点

无。

# 需要ChatGPT判断的问题

无。

# 完整回答

GitHub 协作中继已建立，KF1 真实参考图门禁已修正。中继入口为 `00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md`，完整回执为 `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`。本轮未生成候选图、未调用 Seedance、未制作视频。
