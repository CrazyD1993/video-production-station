---
task_id: phase4b-keyframe-method-r2-001
status: blocked
branch: experiment/openmontage-pilot
commit_sha: pending_first_commit
completed_at: "2026-07-11T20:11:12+08:00"
---

# 执行摘要

已按 Phase 4B 结论将第一轮六图全部标记为不得进入 Seedance。已生成仅含元数据的 `candidate-manifest.yaml`，记录候选编号、文件名、完整 SHA256、尺寸、内容描述和当前决定；已生成并实际查看带候选编号与8位短哈希的本地联系表。第二轮生产合同已改为 KF1真实照片锚定、KF2可控图层合成、KF3完整真实舷窗。当前没有权利清晰且已确认的真实客机舷窗呼吸孔参考图，因此第二轮六张候选均未生成。

# 修改文件

- `08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/candidate-manifest.yaml` — 新增 — 固化第一轮六图身份与审批决定，不包含图片数据。
- `08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/PHASE4B_R2_PRODUCTION_CONTRACT.md` — 新增 — 定义第二轮编号、三条生产路线、事实限制和审批门禁。
- `08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/README.md` — 修改 — 标明第一轮全部不得进入 Seedance，并链接第二轮合同。
- `scripts/build_keyframe_contact_sheet.py` — 修改 — 增加 SHA256 计算、编号与短哈希标签、元数据清单输出。
- `tests/test_build_keyframe_contact_sheet.py` — 修改 — 增加哈希、标签和元数据清单测试。
- `tests/test_ai_relay_contract.py` — 修改 — 更新 Phase 4B 状态合同和清单检查。
- `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md` — 覆盖修改 — 写入本回执。
- `00_项目总控/AI协作中继/STATE.yaml` — 修改 — 记录第一轮全淘汰、第二轮阻塞和下一行动人。
- `keyframe-handoff/contact-sheet/keyframes-hashed.jpg` — 本地生成但不提交 — 带编号及短哈希的2列×3行联系表。

# 实际执行的命令

- OpenMontage `.venv` 执行联系表工具的定向红绿测试。
- `scripts/build_keyframe_contact_sheet.py ... --manifest candidate-manifest.yaml`
- 本地图片查看工具实际查看 `keyframes-hashed.jpg`。
- `python -m unittest discover -s tests -v`
- `python scripts/validate_timeline.py`
- `python scripts/validate_phase2_semantics.py`
- `git diff --check`
- `git diff --cached --check`
- `git commit`
- `git push origin experiment/openmontage-pilot`

# 测试与验证

- 第一轮图片技术校验：6/6 通过，均为 720×1280 PNG、9:16。
- 第一轮身份核对：6/6 已计算完整 SHA256，文件名与联系表位置一致。
- 带哈希联系表：已生成并实际查看；固定位置为第一行 KF1-01/KF1-02、第二行 KF2-01/KF2-02、第三行 KF3-01/KF3-02。
- 新工具测试：先确认缺少 SHA256 与清单输出时两项测试失败，再实现功能并确认定向测试通过。
- 全量单元测试、时间轴和 Phase 3 语义检查：提交前重新执行，最终结果见本轮验证输出。
- 第二轮图片：未生成，因此没有第二轮技术校验或联系表。
- Seedance、12秒样片、完整视频：均未执行。

# 第一轮文件身份

- `KF1-01.png` — `a17962a9f14942b11ebd312b76c6cc0210f80e563fef16d0aa96d68240e242f4` — 仅保留构图与光线方向，必须基于真实参考重生成。
- `KF1-02.png` — `143f6888a656bff92c06d3959dcfe0573022c23268628ed0647ae356a05e7284` — 当前图淘汰，保留第一人称发现动作方法。
- `KF2-01.png` — `c489b67fbfe3ec329fb74024d66fbbe308f0c87cb0b7be4c76db310c4173e65f` — 淘汰。
- `KF2-02.png` — `aa9fccb32db5910cd4c79c6db518f6eefb448e92621ffad36f3008f080f90b75` — 因AI臆造结构风险淘汰。
- `KF3-01.png` — `07ff3b332ffa83d6c3e50fe4bfaacc36417ef86120ac30fa9da4eb8c1ad7e8be` — 淘汰。
- `KF3-02.png` — `0e0dd764aea729f657a90cc164474a5811ce84fdefdd894b39450a29cebf1e58` — 淘汰。

# 与任务要求的差异

- KF1真实参考图尚未具备：没有已确认权利清晰、可用于孔位和材质约束的真实客机舷窗呼吸孔照片。
- KF2可控合成预览尚未完成：缺少合规真实舷窗照片或可信实物底图，不使用第一轮AI图冒充真实底图。
- KF3完整窗体候选尚未完成：同样缺少权利清晰的真实舷窗底图。
- 因第二轮六图未生成，第二轮联系表不存在；当前可查看的 `keyframes-hashed.jpg` 仅用于第一轮身份审计。
- 媒体文件、参考图和联系表均保持 Git 忽略；GitHub只提交元数据、合同、工具、测试和状态文档。

# 当前阻塞点

缺少一张权利清晰、孔位可确认的真实客机舷窗呼吸孔照片及其来源/权利说明。该照片是 KF1生成锚点，也是 KF2、KF3可信实物底图的最低输入条件。

# 需要ChatGPT判断的问题

- 提供或确认一张可用于本地生成与合成的真实客机舷窗呼吸孔照片，并说明来源或使用权。参考图放入本地 `keyframe-handoff/reference/`，不提交Git。

# 完整回答

第一轮六图文件名与 SHA256 已全部核对，元数据清单已生成；带编号和短哈希的本地联系表也已生成并实际查看。当前没有合规真实参考图，因此 KF1-R2 继续阻塞，KF2可控合成预览和KF3完整窗体候选均未制作，第二轮联系表不存在。本轮测试完成后提交实验分支；未调用 Seedance，未制作样片或完整视频。
