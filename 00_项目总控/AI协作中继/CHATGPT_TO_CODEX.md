---
task_id: petrichor-director-remediation-pass-001
revision: 3
status: ready
created_by: ChatGPT
role: 总导演
target_repo: CrazyD1993/video-production-station
target_branch: experiment/openmontage-pilot
issued_from_commit: 882da14c25d99e788c4fa8ea52434eda58f36adc
priority: P0
completion_commit: null
---

# 总导演整改执行令（修订版 3）

不要重复运行已完成的 `petrichor-review-agents-setup-001`，也不要重写上一轮三份审核报告。读取现有审核证据后直接执行整改，制作“动态验证预览”；正式合成门禁继续关闭。

## 创作目标

本片必须让观众经历：

**干旱等待 → 第一滴雨撞击土地 → 水进入土壤 → 微生物与土臭素被唤醒 → 水在孔隙中困住空气 → 气泡上升、破裂并释放 → 土地重新呼吸。**

先让观众看懂事件，再用科学信息加深理解。静音状态下画面仍必须成立；不得依赖静态说明卡或长时间 Ken Burns 推拉冒充内部运动。

## 开始前必须读取

- `00_项目总控/AI协作中继/STATE.yaml`
- `00_项目总控/审核Agents/README.md`
- `00_项目总控/审核Agents/contract-qa-reviewer.md`
- `00_项目总控/审核Agents/visual-director-reviewer.md`
- `00_项目总控/审核Agents/review-arbiter.md`
- `06_成片工程/雨后泥土味/asset-board-v1/shot-plan-v1.yaml`
- `06_成片工程/雨后泥土味/asset-board-v1/seedance-prompts-draft-v1.md`
- `06_成片工程/雨后泥土味/reviews/asset-board-v1/contract-qa.md`
- `06_成片工程/雨后泥土味/reviews/asset-board-v1/visual-director-review.md`
- `06_成片工程/雨后泥土味/reviews/asset-board-v1/review-decision.yaml`
- 当前锁定分镜、素材清单、资产板、预览工程和生成脚本

不得另写宏观规划；按锁定时间线执行。

## 工作包

### A｜开场、地表与连续性

#### S01 第一滴雨

必须清楚出现单滴雨撞击干土：落滴、撞击点、土粒/微小水花/表面响应，以及撞击前后状态变化。优先重新选取真实高速素材并记录来源与时间码。仅出现雨后湿土不算完成。

#### S12 同一块土地由干到湿

保持同一构图、裂纹、石块和土粒关系连续变湿。禁止把 R07 与 R03 两块不同土地直接拼接冒充连续变化。可使用遮罩、湿润扩散、反射/颜色变化和连续降雨合成，但结果必须可信。

### B｜进入地下与机制 A

#### S05 地表进入地下

用水滴、水膜、裂隙、孔隙或土层结构建立连续运动，让观众理解水从地表进入地下。不得突然切成平面说明卡，也不得只做静态推拉。

#### S07 微生物与土臭素

禁止 Seedance。使用真实土壤/土壤截面底图，叠加程序化菌丝、微生物颗粒、水分扩散与克制标签 `土臭素 Geosmin`。必须表现“休眠 → 被水唤醒”的状态变化，避免整屏 PPT 和廉价发光线条。

### C｜机制 B：S08–S11

锁定镜头职责，不得重新解释时间线：

`S08 接近与撞击 → S09 困住空气 → S10 气泡上升 → S11 破裂释放`

#### S08 雨滴接近与撞击过渡

保留原锁定分镜功能：明确显示雨滴高速接近并撞击多孔土壤，为 S09 建立空间位置、尺度和运动方向。

优先使用与 S01 同源真实高速素材的不同时间段；若同源素材不能满足尺度，可用真实纹理程序化合成或匹配素材，但必须匹配土壤颜色、纹理、光向和落滴方向。当前不授权 Seedance。

#### S09–S11 Seedance

仅此镜头组授权调用 Seedance：

- B1：撞击后，水进入孔隙并把空气困成气泡；以气泡开始上升结束。
- B2：气泡继续上升，到达表面、破裂并释放极细气溶胶。

两段必须共享同一土壤截面、孔隙尺度、湿润程度、运动方向和气泡视觉语言。B1 末帧必须可接 B2 首帧。不得生成一条不可控长镜头，不得用魔法光效代替可信物理过程。

S09、S10、S11 的边界和总时长仍以 `shot-plan-v1.yaml` 为准。可以裁切、轻微变速、叠加标签或做克制过渡，但不得修改旁白、镜头顺序或总时间线来迁就生成结果。

### Seedance 调用预算

- 模型固定：`doubao-seedance-2-0-fast-260128`
- 比例：`9:16`
- 分辨率：`720p`
- B1、B2 各生成一条首轮候选
- 每条建议 4–5 秒
- 首轮总调用最多 2 次
- 仅在明确物理错误、主体消失、严重空间断裂或文件损坏时，允许每条最多重试 1 次
- 本任务 Seedance 付费调用硬上限：4 次
- 不得调用其他付费视频模型
- 不得仅因“还不够漂亮”重复生成
- 24fps 作为下载后统一转码和动态预览标准
- 每次调用必须记录模型、真实输入参数、任务 ID、调用状态、输出路径、可获得的真实费用信息及采用/弃用理由
- 费用不可获得时填写 `unknown`，不得推算或伪造
- Seedance 接口或凭证不可用时，相关工作包标记 `blocked`，不得伪造任务、链接或结果

### D｜结尾情绪

#### S13 土地苏醒

替换或重构静态雾林。必须有真实内部运动，例如枝叶承雨回弹、水珠滚落、湿润反光、薄雾漂移、微小生物活动或真实摄影机运动。结尾从压抑转向松开、呼吸和苏醒。

临时声音应形成：近静默干旱 → 第一滴撞击 → 地下低频细节 → 气泡释放 → 环境展开；但静音画面仍要成立。

## 素材纪律

- R01、R03 可保留
- R08 必须替换
- R02、R04–R07、R09、R10 仅在真实内容满足镜头目的时限制使用
- 禁止长时间静态推拉冒充内部运动
- 新素材记录来源、许可、下载日期、文件名、时间码和用途
- 不得伪造下载、生成或第三方服务调用
- 不修改 `main/master`
- 不修改 GitHub Actions
- 不删除或覆盖既有审核证据

### SVG 文件契约

- 构建产物契约：构建脚本仍应能够生成 SVG，测试可以验证其可重建性
- 版本化交付契约：JPG/PDF 为正式提交和审核交付；根目录 SVG 是可重建中间产物，不要求纳入 Git

不得为通过测试强行提交 SVG，也不得仅因 SVG 被 gitignore 就删除其构建测试。

## 必须交付

1. 更新后的分镜/素材状态和资产来源清单
2. 所有不依赖受限外部服务即可完成的合成、动态和剪辑整改
3. 一版“总导演整改动态验证预览”，不得标为正式成片
4. 对 S01、S05、S07、S08、S09–S11、S12、S13 分别标记 `done/partial/blocked`
5. 媒体探测、QA、测试命令和真实结果
6. Git diff 检查，确认未修改 Actions、未删除审核证据
7. 未解决阻塞及建议的下一步人工判断

## 两阶段提交硬约束

本任务必须严格分成两个不可混淆的提交阶段。

### 阶段 1：Production 提交

Production Agent 完成整改与动态验证预览后，必须先提交一个独立、不可变的生产提交：

```yaml
production_complete: true/false
production_commit: <full_sha>
```

要求：

- `production_commit` 只能包含生产整改、素材记录、动态预览及生产测试证据
- 不得在同一个提交中写入 Reviewer A/B/C 的新审核结论
- 形成 `production_commit` 后，独立审核必须基于该完整 SHA 的隔离快照
- 审核期间不得修改或重写该生产提交
- Production Agent 不得填写 `review_ready: true`
- Production Agent 不得自行批准正式合成

### 阶段 2：独立审核提交

只有 `production_commit` 已存在后，才可启动现有审核系统：

1. Reviewer A：Contract QA
2. Reviewer B：Visual Director
3. Reviewer C：Review Arbiter

要求：

- A/B 基于同一个 `production_commit` 隔离快照独立审核
- A/B 形成结论前不得读取 Production 自评、对方报告或对方中间输出
- C 仅在 A/B 报告都完成后启动
- 新报告写入 `06_成片工程/雨后泥土味/reviews/director-remediation-pass-001/`
- 不得覆盖上一轮 `reviews/asset-board-v1/`
- 审核报告、Review Arbiter 裁决和回执状态必须在生产提交之后形成第二个独立提交：

```yaml
independent_review_complete: true/false
review_commit: <full_sha>
reviewed_production_commit: <same production_commit full_sha>
reviewer_c_approve_formal_composition: true/false
human_final_decision: pending
```

硬性顺序：

`production_commit → 独立审核 A/B/C → review_commit`

禁止：

- 把生产整改和独立审核压进同一个 commit
- 在 `production_commit` 产生前运行 Reviewer C
- 让 Reviewer A/B 审核工作区浮动 HEAD，而不是明确的 `production_commit`
- 让 `review_commit` 的 `reviewed_production_commit` 指向其他 SHA
- 让 Production Agent 自己给出最终门禁

即使 Reviewer C 给出 `approve_formal_composition: true`，也不得自动进入正式合成；最终决定保留给 ChatGPT 总导演读取回执和三份新报告后人工裁决。

## 回执与状态同步

完成两个阶段后：

1. 将完整回执写入 `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
2. 同步 `00_项目总控/AI协作中继/STATE.yaml`
3. 将本文件更新为最终状态，并填写 `completion_commit`
4. 回执必须列出：
   - `task_id`
   - 最终状态 `completed/partial/blocked`
   - `production_commit`
   - `review_commit`
   - `reviewed_production_commit`
   - 修改文件
   - 各工作包状态
   - 动态预览与证据路径
   - 素材来源
   - Seedance 每次真实调用记录与总次数
   - 测试命令和结果
   - Reviewer A/B/C 结论
   - `reviewer_c_approve_formal_composition`
   - `human_final_decision: pending`
   - 未解决问题
   - 建议 ChatGPT 下一步仅做何种判断

如无法完成任一阶段，必须如实标记 `partial` 或 `blocked`，写明具体失败点；不得伪造 SHA、报告、模型调用、媒体或测试结果。
