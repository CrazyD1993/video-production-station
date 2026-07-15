---
task_id: petrichor-director-remediation-v2-001
revision: 2
status: completed_with_blocks
created_by: ChatGPT
role: 总导演
target_repo: CrazyD1993/video-production-station
target_branch: experiment/openmontage-pilot
issued_from_review_commit: a6250d9287b2f44c0e6fe6376699c9d1c94080f9
prior_production_commit: 0da86d05b1904adb9f221f073438c11268a05d44
priority: P0
production_complete: true
production_commit: 8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781
independent_review_complete: true
review_commit: 6d3aa60bb5fd9fe81d80004b29370c72a24730d5
reviewer_c_approve_seedance_mechanism_generation: false
reviewer_c_approve_formal_composition: false
human_final_decision: pending
formal_composition_started: false
completion_commit: pending_recording
---

# 雨后泥土味｜定向整改 V2 执行令

## 一、任务目标

基于上一轮 46.8 秒动态验证预览与独立审核，完成一次定向收口整改。

本轮仍然只制作动态验证预览，不制作正式成片，不加入正式旁白、字幕或正式混音。正式合成门禁继续关闭。

不得重新解释锁定科学、旁白、13 镜顺序或 46.80 秒时间线。

## 二、开始前必须读取

- `00_项目总控/AI协作中继/STATE.yaml`
- `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/contract-qa.md`
- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/visual-director-review.md`
- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/review-decision.yaml`
- `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/review-summary.md`
- prior production commit `0da86d05b1904adb9f221f073438c11268a05d44`
- prior review commit `a6250d9287b2f44c0e6fe6376699c9d1c94080f9`

不要重跑上一轮整改，不要覆盖旧审核报告。

## 三、总导演直接观看上一版预览后的裁决

上一版预览已实际观看，以下问题为本轮硬依据：

- S01：白色图形雨滴落到裂土后变成规则椭圆暗斑，没有真实撞击、土粒、水花或扩散响应；当前版本废弃。
- S04：水滴一直悬挂在叶尖，没有出现“聚集—拉长—脱落”；必须换取 R02 的真实脱落后段。
- S05：裂土、蓝色箭头与根系照片交叉叠化，仍是说明卡，不是水进入同一土层空间；当前版本废弃。
- S06：根系与苔藓照片长时间冻结，没有“游离物质被土粒吸附”的状态变化；当前版本废弃。
- S07：扁平机制图和整屏文字感明显，仍是 PPT/科普卡；当前版本废弃。
- S08：再次使用白色图形雨滴落在裂土上，动作和材质均不可信，也没有进入 S09 的同一机制空间；当前版本废弃。
- S09/G01/B1：气泡先向下、消失、再从底部跳位出现，物理方向和主体连续性错误；必须完全废弃。
- S10/G02/B2：单气泡向上运动是当前机制段唯一可保留部分，只作为下一版视觉锚点，不代表连续性通过。
- S11：气泡在表面形成大液泡/大液柱后消失，没有可信的膜破裂与极细气溶胶；当前尾部废弃。
- S12：湿润由规则圆形暗化遮罩扩张完成，过于人工；保留同一裂纹几何，重做非均匀湿润。
- S13：叶片雨动到雾林的真实运动结构可保留，但绿色到灰冷雾林跳变明显，后续统一色彩与“苏醒”情绪。
- 当前预览顶部和底部的大面积调试条影响纯视觉判断。V2 输出必须提供干净版预览，不得继续用全宽大黑条覆盖画面。

## 四、锁定时间线

- S01 00.00–01.20
- S02 01.20–03.85
- S03 03.85–05.69
- S04 05.69–08.70
- S05 08.70–12.32
- S06 12.32–17.10
- S07 17.10–21.38
- S08 21.38–24.30
- S09 24.30–27.35
- S10 27.35–30.50
- S11 30.50–35.06
- S12 35.06–39.77
- S13 39.77–46.80

机制职责不得错位：

`S08 接近与撞击 → S09 困住空气 → S10 气泡上升 → S11 破裂释放`

## 五、制作策略

### A｜S01 与 S08：同源可信撞击

优先取得一条真实微距或高速单滴撞击干燥/多孔土壤的合规素材，并在 S01、S08 使用不同时间段与不同叙事功能：

- S01：使用最清楚的撞击瞬间，必须看到撞击点以及土粒、微尘、小水花或颜色响应。
- S08：使用接近、撞击和进入孔隙的过渡，镜尾必须进入与新 B1、现有 G02/B2 相同的土壤截面、孔隙尺度、光向和运动方向。

若无法取得同源素材，可使用真实土壤纹理上的匹配合成，但禁止再次使用扁平白色图形雨滴和规则椭圆水斑。

R11 若实际不采用，清单必须明确写 `acquired_not_used`，不得继续申报为镜头依赖。

### B｜S04：真实脱落事件

重新检查 R02 原始代理或可追溯源文件，选择真正出现：

`聚集 → 拉长 → 脱落`

的时间段。不得用长时间悬挂水滴冒充事件。若 R02 没有该动作，标记缺失并换合规真实素材，不调用 Seedance。

### C｜S05–S07：统一机制 A 母场景

不要分别制作三个不相干的画面。S05、S06、S07 必须共用一个真实土壤/根系纵向剖面母场景、同一光线和同一镜头空间。

- S05：从地表水膜或裂隙进入地下，入渗前沿可追踪；摄影机或空间连续下潜，禁止照片交叉叠化和蓝色说明箭头承担主要动作。
- S06：在同一场景中显示少量植物来源物质/颗粒从水膜中游离，接近并吸附到土粒或岩石表面；必须发生状态变化。
- S07：仍禁止 Seedance。水分进入后，少量菌丝舒展、微生物活动轻微恢复，`土臭素 Geosmin` 仅作克制标签；真实土壤始终是主体。

禁止整屏 PPT、发光菌丝、HUD、卡通细菌和五颜六色分子。

### D｜S09：以 G02/B2 锚点反向重做 B1

完全废弃 G01/B1。

生成前先建立 `mechanism-b-reference-pack-v2`，至少包含：

- G02/B2 可保留 S10 上升段的首帧、中段帧、接近表面帧；
- 背景土壤截面；
- 孔隙尺度；
- 水线位置；
- 气泡大小、透明度与高光；
- 光向；
- 上升方向；
- S08 镜尾目标帧。

新 B1 只表现：

`水进入孔隙 → 空气空间缩小 → 被水包围 → 形成同一气泡 → 气泡开始上升`

B1 末帧必须可直接接入 G02/B2 的可保留 S10 上升段。

若现有 Seedance 接口支持参考帧/图生视频/首尾约束，按真实支持能力使用；若不支持，不得伪造能力。可在生成后用 8–12 帧程序化匹配过渡到 G02 精确首帧，但过渡不得明显跳变。

### E｜S10–S11：避免显著慢放

- S10：只保留 G02/B2 中合格的单气泡上升段。
- 不得再把约 5.04 秒素材拉伸到 7.71 秒、约 65.4% 原速。
- 轻微重定时原则上不超过 ±8%。超出则判定素材不适配。

S11 默认先用程序化方式在 G02 同一表面帧上完成：

`小气泡接触表面 → 小尺度膜短促破裂 → 极细微滴瞬间喷散 → 快速消退`

不得出现大液柱、大水滴爆炸、魔法粒子或长时间静止尾帧。

### F｜S12：裂纹驱动的非均匀湿润

保留当前同一裂纹和构图基础，重做湿润算法：

- 多个离散撞击点；
- 沿裂缝、土粒边缘和低洼区域优先扩散；
- 湿润边界不规则；
- 局部颜色、反射和质感变化不同步；
- 禁止规则圆形柔边遮罩和全画面统一变暗。

### G｜S13：只做统一，不推倒重来

保留 R13→R12 的真实动态结构。只调整：

- 绿色饱和度；
- 黑位；
- 冷暖过渡；
- 近景到雾林的衔接；
- 结尾亮度与“土地苏醒”的呼吸感。

不再大范围找新结尾素材，除非现有代理损坏或无法解码。

## 六、Seedance 剩余调用硬门禁

模型固定：`doubao-seedance-2-0-fast-260128`

- 已使用：2 次
- 总硬上限：4 次
- 本轮最多新增：2 次
- 不得调用其他付费视频模型
- 不得因为“不够漂亮”使用重试

调用优先级：

1. 第一次必须用于新 B1。
2. 第二次不是默认调用：
   - 若新 B1出现明确物理错误、主体消失、严重跳位或无法接入 G02，可重试 B1；
   - 只有新 B1通过且程序化 S11 确实无法形成可信破裂时，才允许用于 S11 尾部。

不得同时默认生成 B1 重试和 S11。总新增调用不得超过 2 次。

每次记录真实模型、参数、task id、状态、输出路径、原始时长、采用/弃用理由和真实可获得费用；费用不可得写 `unknown`，不得推算。

## 七、素材与时间证据链

重建逐镜可追溯清单，必须与实际渲染代码一致，至少记录：

- 每镜实际母素材；
- 程序化派生来源；
- 使用时间码；
- 原始时长；
- 目标时长；
- 实际速度比例；
- 母素材真实复用次数；
- 已取得但未采用的素材；
- 新素材来源、作者、许可、下载日期和用途。

R07 不得继续隐性跨 4 镜使用而不记录。R05 新用途和 R11 未采用状态必须写清。

## 八、V2 输出

输出目录：

`06_成片工程/雨后泥土味/director-remediation-v2-001/`

必须交付：

1. `mechanism-a-v2.mp4`：S05–S07 连续段；
2. `mechanism-b-v2.mp4`：S08–S11 连续段；
3. `petrichor-remediation-v2-clean-preview.mp4`：46.80 秒干净动态验证预览；
4. 干净预览不得使用顶部/底部全宽大黑条；如需镜头编号，只允许安全角落中的小型、低干扰标记；
5. 带镜头号和时间码的 QA 联系表，不用大面积覆盖视频；
6. S01、S04、S05、S06、S07、S08、S09、S10、S11、S12、S13 的 `done/partial/blocked` 状态；
7. 更新后的素材与程序化依赖清单；
8. Seedance 调用日志；
9. FFprobe、完整解码、SHA-256、镜头中点帧、机制连续性联系表；
10. 生产报告与未解决问题。

当前预览仍只使用临时环境声，不加入正式旁白、字幕与正式混音。

## 九、Production 门禁

以下任一项未满足，不得申报相应镜头 `done`：

- S01 看不到可信撞击响应；
- S04 水滴未实际脱落；
- S05–S07 未处于同一机制 A 空间；
- S08 镜尾不能进入新 B1 同一截面；
- 新 B1 仍向下运动、消失、跳位或与 G02 不连续；
- S11 仍是大液柱/大液滴或没有极细气溶胶；
- S12 仍是规则圆形暗化；
- 素材清单无法重建真实渲染依赖；
- 任一素材被显著慢放超过 ±8% 且没有明确总导演新授权。

## 十、两阶段提交与独立复审

### 阶段一：Production commit

Production 完成 V2 产物和生产 QA 后，先建立不可变 `production_commit`。

该提交只包含生产资产、预览、清单、调用记录和生产测试，不包含新 A/B/C 审核结论。

### 阶段二：Review commit

基于该 `production_commit` 的隔离快照运行：

1. Reviewer A / Contract QA
2. Reviewer B / Visual Director
3. Reviewer C / Review Arbiter

A/B形成结论前不得读取 Production 自评或对方报告。Reviewer B 必须实际检查干净预览、机制 A/B 连续片段及关键逐帧证据，不得只根据文字回执判定。

新审核目录：

`06_成片工程/雨后泥土味/reviews/director-remediation-v2-001/`

审核后建立独立 `review_commit`。

最终仍保持：

- `human_final_decision: pending`
- `formal_composition_started: false`

即使 Reviewer C 批准，也不得自动进入正式成片。

## 十一、禁止事项

- 不重新生成或修改锁定 TTS；
- 不修改旁白、字幕文本、13 镜顺序或总时间线；
- 不制作正式字幕、正式混音或正式成片；
- 不扩大 Seedance 到 S01、S04、S05、S06、S07、S08、S12、S13；
- 不超过剩余 2 次调用；
- 不调用其他付费视频模型；
- 不修改 `main/master`、GitHub Actions；
- 不删除或覆盖上一轮生产与审核证据；
- 不伪造模型能力、task id、费用、测试、素材来源或 SHA。

## 十二、回执

完成后更新：

- `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
- `00_项目总控/AI协作中继/STATE.yaml`
- 本文件 frontmatter

回执必须包含：

- task_id、revision、最终状态；
- production_commit、review_commit、completion_commit；
- 各镜头状态；
- 干净预览、机制 A/B 片段和 QA 路径；
- 新旧素材取舍；
- Seedance 每次真实调用；
- 原始/目标时长与速度比例；
- 测试命令和真实结果；
- Reviewer A/B/C 结论；
- `reviewer_c_approve_formal_composition`；
- `human_final_decision: pending`；
- 下一步只需要 ChatGPT 和用户判断的事项。

完成并推送后立即停止，等待人工裁决。

## 十三、本轮执行回填

- Production commit：`8b3b5bd4d97bf8e164b8d08fd8a68d50f6cff781`
- Review commit：`6d3aa60bb5fd9fe81d80004b29370c72a24730d5`
- Reviewer A：`BLOCK`
- Reviewer B：`BLOCK`
- Reviewer C：不批准新增 Seedance，不批准正式合成。
- Seedance：累计 `4/4`，剩余 `0`。
- `human_final_decision: pending`
- `formal_composition_started: false`
- 完整回执：`00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
