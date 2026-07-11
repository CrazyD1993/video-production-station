---
task_id: bavi-hotspot-keyframes-001
status: completed
branch: experiment/openmontage-pilot
commit_sha: pending_first_commit
completed_at: "2026-07-11T23:02:55+08:00"
---

# 执行摘要

已按批准进入巴威热点快速生产模式，完成TE-KF1、TE-KF2、TE-KF3各A/B两张，共6张候选。六张均为1080×1920 PNG、9:16，并统一标记 `non_event_specific_visual_reconstruction: true`，画面可见标注“AI视觉重建｜非真实卫星观测”。已生成带编号和短哈希的2列×3行联系表并实际查看。Codex推荐组合为 `TE-KF1-A + TE-KF2-A + TE-KF3-B`。当前停在唯一人工门禁：用户从三组各批准一张；尚未调用Seedance。

# 修改文件

- `台风眼12秒样片/02-官方资料与热点状态.md` — 新增 — 记录NASA/NOAA卫星锚点、NASA使用条件、中央气象台素材限制和22:06热点状态。
- `台风眼12秒样片/03-候选评分与推荐.md` — 新增 — 六图评分、逐张审核、推荐组合和后续耗时。
- `台风眼12秒样片/04-热点文案模块.md` — 新增 — 登陆前/登陆后可替换开头及发布前核查规则。
- `台风眼12秒样片/keyframe-handoff/candidate-manifest.yaml` — 新增 — 六张候选文件名、SHA256、尺寸、格式、AI重建标记和审批状态。
- `台风眼12秒样片/keyframe-handoff/overlays/TE-KF2-A.svg` — 新增 — KF2-A独立可控气流与标签图层。
- `台风眼12秒样片/keyframe-handoff/overlays/TE-KF2-B.svg` — 新增 — KF2-B独立可控气流与标签图层。
- `台风眼12秒样片/keyframe-handoff/{reference,incoming,contact-sheet}/.gitignore` — 新增 — 阻止卫星参考、AI候选和联系表进入Git。
- `当前工作台.md` — 修改 — 进入巴威快速生产并更新为唯一选图门禁。
- `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md` — 覆盖修改 — 写入本回执。
- `00_项目总控/AI协作中继/STATE.yaml` — 修改 — 记录联系表就绪、推荐组合、选图门禁和热点状态。
- `tests/test_ai_relay_contract.py` — 修改 — 验证六图元数据、资料边界、推荐组合和热点文案模块。
- 六张PNG、NASA参考图和联系表 — 本地新增但不提交Git。

# 实际执行的命令

- `agent-reach doctor --json`
- 检索并打开NASA Earth Observatory巴威页面、NASA图片媒体指引、中央气象台实时台风快讯。
- 下载NASA 2026-07-08 NOAA-21/VIIRS巴威图到本地参考目录。
- 使用内置imagegen逐张生成6张候选，每个提示词只执行一次。
- 使用Pillow完成9:16规格化、AI可见标记、KF2独立可控图层合成、SHA256清单和联系表。
- `python -m unittest discover -s tests -v`
- `python scripts/validate_timeline.py`
- `python scripts/validate_phase2_semantics.py`
- `git diff --check`
- `git commit`
- `git push origin experiment/openmontage-pilot`

# 测试与验证

- 图片数量：6/6。
- 格式、尺寸和画幅：6/6通过，均为1080×1920 PNG、9:16。
- AI透明标记：6/6元数据为true，6/6画面含可见“AI视觉重建｜非真实卫星观测”。
- KF2图层边界：ImageGen底图无箭头和文字；箭头、眼墙/下沉标签、结构示意均由后期可控图层加入。
- 联系表：已生成并实际查看，编号和短哈希无错位。
- 视觉审核：已执行6/6；KF2-B存在上下双眼区与空间拼接歧义，明确不推荐。
- 全量单元测试、时间轴和生产语义校验：提交前重新执行，最终结果以本轮验证日志为准。
- Seedance、12秒样片、25秒成片：均未执行，等待用户选图。

# 与任务要求的差异

- 没有直接复用或下载中央气象台图片，因为其页面明确未经授权禁止下载使用；只读取最新文字快讯。
- NASA巴威图只作本地结构锚点，没有进入候选成品或GitHub。
- TE-KF2-B虽然技术规格合格，但出现两个眼区和明显空间拼接歧义，保留给用户对比但不推荐。
- 当前中央气象台22:06快讯仍为台风级、位于温岭南偏东约65公里，不能使用“已经登陆”，也不能把当前强度写成“超强台风”。发布前必须再次核查。

# 当前阻塞点

等待用户从TE-KF1-A/B、TE-KF2-A/B、TE-KF3-A/B中各批准一张。未批准前不调用Seedance。

# 需要ChatGPT判断的问题

- 是否批准Codex推荐组合：`TE-KF1-A + TE-KF2-A + TE-KF3-B`。
- 如不批准，请分别指定KF1、KF2、KF3选择的候选编号。

# 完整回答

六张真实候选和2列×3行联系表均已完成。Codex推荐 `TE-KF1-A + TE-KF2-A + TE-KF3-B`；TE-KF2-B因双眼区和拼接歧义不推荐。用户批准三张后，预计2—3小时完成12秒样片；样片无重大错误后再追加3—5小时扩展25秒成片，不含外部Seedance排队时间。本轮未调用Seedance。
