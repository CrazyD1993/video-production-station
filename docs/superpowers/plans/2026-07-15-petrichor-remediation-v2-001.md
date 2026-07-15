# 雨后泥土味导演整改 V2 实施计划

> **执行要求：** 使用 `superpowers:executing-plans` 逐项实施；生产者只负责生产包，生产 commit 固定后再由独立 Reviewer A/B/C 审核。

**目标：** 在不生成正式成片、不加入旁白/字幕/正式混音的前提下，重建 46.80 秒动态验证预览，解决 S01/S04/S05-S07/S08-S11/S12/S13 的导演审核阻塞项，并形成可追溯、可独立复核的生产快照。

**总体方法：** 真实素材承担生活场景与收束；S05-S07 使用同一土壤剖面空间做连续程序化机制动画；S08-S11 锁定同一几何和光线，先重建 B1，再无缝连接既有 G02 上升段，S11 优先程序化完成；所有时轴、素材复用、速度和调用门禁由自动化测试约束。

**技术栈：** Python 3、Pillow、NumPy、FFmpeg/ffprobe、unittest、Volcengine Seedance 2.0 Fast（最多新增两次调用，首调用固定 B1）。

---

## Task 1：冻结证据与建立失败测试

**文件：**
- 创建：`06_成片工程/雨后泥土味/director-remediation-v2-001/tests/test_production_contract.py`
- 创建：`06_成片工程/雨后泥土味/director-remediation-v2-001/tests/test_render_plan.py`
- 创建：`06_成片工程/雨后泥土味/director-remediation-v2-001/tests/test_seedance_gate.py`
- 创建：`06_成片工程/雨后泥土味/director-remediation-v2-001/render_plan.yaml`

1. 检查 R02、R05、R07、R12、R13 与 G02/B2 的技术参数和逐段静帧。
2. 写入锁定的 13 镜时轴、46.80 秒总长、S08-S11 动作角色和最大素材复用次数测试。
3. 写入 S05-S07 同一空间、G01/B1 禁用、S10 速度比 0.92-1.08、Seedance 总调用硬上限 4 的测试。
4. 运行测试并确认因生产文件尚不存在而按预期失败。

## Task 2：建立统一机制空间与参考包

**文件：**
- 创建：`render_remediation_v2.py`
- 创建：`mechanism-b-reference-pack-v2/`
- 创建：`qa/source-inspection/`
- 修改：对应测试文件

1. 从可用 G02/B2 逐帧提取水线、孔隙、气泡、光向和接续帧。
2. 从 R05 构建 S05-S07 共用的真实土壤/根部垂直剖面底图，不切换母空间。
3. 先补充失败测试验证共享 scene id、参考帧哈希和接续点，再实现最小渲染接口使其通过。
4. 输出参考包说明、关键帧和连续性联系表。

## Task 3：制作 S01/S04/S05-S07/S08/S12/S13

**文件：**
- 创建：`work/shots/S01.mp4` 等镜头文件
- 创建：`mechanism-a-v2.mp4`
- 创建：`shot-status.yaml`
- 修改：`render_remediation_v2.py`

1. S01/S08 使用可信的同源落雨冲击视觉语言；不得出现白色扁平雨滴或椭圆湿痕。
2. S04 从 R02 真实素材中选取聚集、拉伸、脱落完整动作；若素材不成立则明确标记缺失，不伪造。
3. S05 做可追踪入渗，S06 做游离物质被土粒吸附，S07 做水分到达后微生物/菌丝的克制活动，三镜保持同一空间和光线。
4. S08 建立与 B1/G02 一致的撞击和孔隙入口。
5. S12 做沿裂缝、边缘和低点异步扩散的湿润过程；S13 只用 R13→R12 真实运动并做统一调色。
6. 每个行为先写/扩展失败测试，确认失败后实现，再跑绿。

## Task 4：按门禁重建 B1 并完成 S09-S11

**文件：**
- 创建：`seedance/prompts-v2.yaml`
- 创建：`seedance/call-log-v2.json`
- 创建：`seedance/outputs/`
- 创建：`mechanism-b-v2.mp4`
- 修改：`render_remediation_v2.py`

1. 第一笔新增 Seedance 调用只用于 B1：水进入孔隙、空气收缩、被包围、同一气泡形成并开始上升。
2. 仅在接口明确支持参考帧时传参考帧；否则如实记录文本生成，不伪称参考帧控制。
3. 检查 B1 是否物理成立、主体连续且可接 G02。只有失败时才允许第二次 B1 重试；若 B1 通过，则第二次调用仅在程序化 S11 确实不可用时允许。
4. S10 只取 G02 有效上升段，实际速度比限制在 0.92-1.08。
5. S11 默认在同一 G02 表面程序化实现小气泡触面、薄膜破裂、极细液滴快速散去。
6. 生成 S08-S11 连续机制片和逐接缝 QA。

## Task 5：构建干净动态预览和可追溯清单

**文件：**
- 创建：`petrichor-remediation-v2-clean-preview.mp4`
- 创建：`asset-manifest-v2.csv`
- 创建：`dependencies-v2.yaml`
- 创建：`production-report.md`
- 创建：`unresolved-items.md`
- 创建：`qa/` 下 ffprobe、SHA256、解码、逐镜中点和连续性联系表

1. 按锁定时轴串联 13 镜，总长严格 46.80 秒，不加入旁白、字幕、正式混音或大面积条幅。
2. 清单记录母素材、派生关系、源时间码、原/目标时长、实际速度比、复用次数和 acquired-not-used。
3. 对预览、机制片执行 ffprobe、完整解码、SHA256 与逐镜中点抽帧。
4. 运行全部自动化测试；任何硬门禁不通过就保持 `not_done`，不宣称完成。

## Task 6：固定生产 commit 并推送

**文件：**
- 仅包含生产资产、脚本、测试和 QA；不生成新审核结论。

1. 检查工作区，确认未纳入密钥、Cookie、外部原始下载视频或个人信息。
2. 再跑完整测试和媒体验证。
3. 创建 production commit，推送 `experiment/openmontage-pilot`，记录不可变 SHA。

## Task 7：独立 Reviewer A/B/C 审核

**文件：**
- 创建：`06_成片工程/雨后泥土味/reviews/director-remediation-v2-001/contract-qa.md`
- 创建：`.../visual-director-review.md`
- 创建：`.../review-decision.yaml`
- 创建：`.../review-summary.md`

1. Reviewer A 与 Reviewer B 只读同一 production commit 快照，独立判断；形成结论前不读生产者自评。
2. Reviewer B 必须实际查看干净预览、机制片、逐镜中点和接缝联系表。
3. A/B 完成后 Reviewer C 原样汇总分歧与门禁，不篡改原结论。
4. 即使批准，也保持 `human_approval: pending`、`formal_composition: false`。

## Task 8：更新中继状态并提交推送

**文件：**
- 修改：`00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md`
- 修改：`00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
- 修改：`00_项目总控/AI协作中继/STATE.yaml`

1. 保留任务正文，更新 front matter 状态、生产 SHA、审核 SHA 和实际产出/未解决项。
2. 创建最终审核/中继 commit 并推送指定分支。
3. 远端回读验证 SHA、UTF-8 和所需文件，随后停止等待人工决定。
