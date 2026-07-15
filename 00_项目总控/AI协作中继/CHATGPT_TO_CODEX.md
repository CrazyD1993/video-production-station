---
task_id: petrichor-director-remediation-v2-001
revision: 1
status: assigned
created_by: ChatGPT
role: 总导演
target_repo: CrazyD1993/video-production-station
target_branch: experiment/openmontage-pilot
issued_from_commit: 986464ce694a6c55ada41e2795afcf7c1460eeec
prior_production_commit: 0da86d05b1904adb9f221f073438c11268a05d44
prior_review_commit: a6250d9287b2f44c0e6fe6376699c9d1c94080f9
priority: P0
human_final_decision: authorize_constrained_remediation_v2
formal_composition: false
---

# 雨后泥土味｜严格受限 remediation-v2

## 结论

授权一次严格受限的 `remediation-v2`。

当前预览不可发布，正式合成继续关闭。不要重复执行上一轮任务，不要覆盖旧审核报告，不要把本任务扩展为正式成片。

本轮目标不是“完成视频”，而是解除现有核心 BLOCK，并建立可复审的新生产提交。

## 开始前必须检查

先读取当前分支 HEAD、`STATE.yaml`、`CODEX_TO_CHATGPT.md`、上一轮 production/review commit，以及：

- `reviews/director-remediation-pass-001/contract-qa.md`
- `reviews/director-remediation-pass-001/visual-director-review.md`
- `reviews/director-remediation-pass-001/review-decision.yaml`
- `reviews/director-remediation-pass-001/review-summary.md`

如发现新任务、新回执或新生产结果，停止并报告，不得覆盖或重复执行。

## 不可修改

- 锁定旁白、TTS、时间戳
- S01-S13 时间线职责
- 正式合成门禁
- main/master
- GitHub Actions
- 旧生产资产和旧审核报告

本轮预览仍不得加入正式旁白、正式字幕、发布包装或正式片尾。

## Seedance 硬门禁

固定模型：`doubao-seedance-2-0-fast-260128`

项目此前已使用 2 次。本轮最多新增 2 次，项目累计不得超过 4 次。

### 第一次调用：只用于新 B1

必须以旧 B2/G02 中可保留的 S10 单气泡上升段为唯一视觉锚点，锁定：

- 同一土壤截面和孔隙尺度
- 同一水线、湿润程度、光向和色温
- 同一气泡外观、尺寸和主体身份
- 正确运动方向：水进入孔隙，空气被困，气泡形成并开始向上

旧 B1/G01 必须废弃。不得出现气泡下移、消失、跳位、穿透固体或突然换主体。

### 第二次调用：严格二选一

仅允许：

A. 新 B1 首次结果存在明确物理错误或严重连续性断裂时，重试 B1 一次；

或：

B. 新 B1 已通过内部预检后，定向补救 S11 的小尺度膜破裂与极细气溶胶尾部。

不能同时重试 B1 又生成 S11。第二次额度不是必用额度。

每次调用必须记录：模型、输入、参数、真实 task id、状态、输出路径、可用区间、采用/废弃结论和原因。费用无法获得时写 `unknown`，不得推算。

调用前必须落盘 B2 可保留区间、首中末参考帧、截面/水线/气泡标注、S08 到新 B1 的对接草图、正负提示词及废片条件。预检不完整，不得调用。

## 必须整改的镜头

### S01
使用真实高速素材或可信合成，必须看见“接近—接触变形—土粒/微水花/湿痕响应”。禁止白色椭圆、圆环或亮点冒充撞击。

### S04
改用 R02 中真实发生“聚集—拉长—脱落”的后段时间码。当前未脱落区间不得继续使用。

### S05
在同一土壤空间中连续表现水从地表进入地下。不得再用两张照片跨叠或静态推拉冒充内部运动。

### S06
表现物质从游离、接近土粒到被吸附并停留的状态变化。真实土壤纹理必须是主体。

### S07
禁止 Seedance。使用真实土壤底图与克制的程序化元素，表现“休眠/低活性—被水唤醒—微生物活动增强—Geosmin 信息出现”。不得做成 PPT、机制卡或廉价科幻 HUD。

### S08
使用真实素材或程序化合成完成可信雨滴接近和撞击，并在镜尾进入与新 B1/B2 一致的土壤截面空间。禁止程序化白色雨滴冒充真实撞击。

### S09-S11
统一为同一截面、同一气泡和同一连续机制链：

`S09 困住空气 → S10 气泡上升 → S11 膜破裂并释放极细气溶胶`

旧 B1 必须废弃。旧 B2 只允许裁切使用 S10 条件通过的上升区间，不得整段采用。

### S12
保留同构图和裂纹几何，但湿润必须沿裂缝、低洼和土粒非均匀扩散，并伴随可信的局部颜色、反光、饱和度和含水量变化。禁止圆形柔边遮罩和整体压暗。

### S13
保留 R13→R12 的真实内部运动结构，统一绿色、黑位、雾感、暖意和节奏，完成从压抑到舒展、呼吸和苏醒的情绪转变。

## 播放速度与填时长

所有视频默认只允许 `0.90x-1.10x`。

不得再次把 B2 慢放到约 65.4% 原速。不得用冻结、长尾静帧、循环、反向播放、重复动作或纯 Ken Burns 推拉强行填满时间线。

## 素材依赖与证据链

重建逐镜素材依赖清单，必须与实际渲染完全一致，并记录：

- 每镜真实素材、程序化资产和生成资产
- 原始路径、来源、授权和下载日期
- 原始时间码、裁切时间码、目标时长和播放速度
- 调色、遮罩、合成、程序化处理
- 同一母素材实际跨镜使用次数
- R05 是否用于 S05
- R07 的实际跨镜次数
- R11 明确标注“已取得但未采用”或真实使用位置
- B1/B2 的实际可用区间和采用结论

清单必须能够复现实际渲染，不得先写计划再与成片脱节。

## 交付

建立新目录：

`06_成片工程/雨后泥土味/director-remediation-v2-001/`

至少交付：

1. 46.800 秒、540×960、24fps 的静音或临时环境声动态验证预览
2. 逐镜联系表与中点静帧
3. S08→S09→S10→S11 连续机制联系表
4. Seedance 锚点预检、调用记录和真实输出
5. 新逐镜素材依赖清单
6. 媒体探测、播放速度、时长和程序化资产 QA
7. 逐镜整改状态：`done / partial / blocked`
8. 已知限制、废弃资产和未解决问题
9. 可复现�4�O�成和 QA 命令

不得把动态验证预览称为正式成片或可发布版本。

## 两阶段提交与复审

先创建不可变 `production_commit`，只包含本轮生产资产、脚本、清单和 QA。

然后 Reviewer A、Reviewer B 必须基于同一个完整 `production_commit` SHA 隔离审核；Reviewer C 只在 A/B 完成后汇总。审核 Agent 只读，不得自动修复。

之后创建独立 `review_commit`。流程必须是：

`production_commit → A/B 独立审核 → C 汇总 → review_commit → 人工最终裁决`

正式合成继续保持：

```yaml
formal_composition: false
human_final_decision: pending
```

## 停止条件

发生以下任一项，停止追加生成并如实标记 `blocked`，不得自行扩展为 v3：

- 两次额度用完后，新 B1 仍无法与 B2/G02 连续
- 气泡仍下移、消失、跳位或主体身份不清
- S01/S08 仍是程序图形假撞击
- S05/S07 仍主要依赖文字或机制卡解释
- S11 仍读成大液柱、大液滴或粗颗粒爆发
- S12 仍是遮罩式整体变暗
- 素材依赖清单再次不能复现渲染
- Reviewer A/B 因同类问题再次 BLOCK

## 回执

完成后更新：

- `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
- `00_项目总控/AI协作中继/STATE.yaml`

回执必须列出：

- task_id 和最终状态
- 分支 HEAD
- production_commit
- review_commit
- reviewed_production_commit
- 修改文件
- 各镜头状态
- Seedance 每次真实调用记录及累计次数
- 新预览、联系表、清单和 QA 路径
- Reviewer A/B/C 结论
- `reviewer_c_approve_formal_composition`
- `human_final_decision: pending`
- 未解决问题
- 建议下一步只做何种人工判断

正式合成门禁不得开启。
