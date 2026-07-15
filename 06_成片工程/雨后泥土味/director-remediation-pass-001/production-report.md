# 雨后泥土味｜总导演整改动态验证预览生产报告

task_id: `petrichor-director-remediation-pass-001`  
用途：**动态验证预览（非成片）**  
`formal_composition: false`

## 结果

- 锁定时间线：S01—S13，`0.00—46.80` 秒，未改变镜头顺序。
- 动态预览：`petrichor-director-remediation-preview-v1.mp4`。
- 媒体参数：540×960、24fps、H.264、AAC 48kHz 单声道、46.800秒。
- 声音：仅临时验证环境声；未加入锁定旁白、正式音乐或正式混音。
- 旁白：未读取、未修改、未变速、未重新生成。
- 正式合成：未开始，门禁保持关闭。

## 工作包状态

- S01：`partial`。程序化实现落滴、撞击与湿斑，但没有用湿地表素材冒充干土首滴；真实高速母素材仍缺。
- S05：`done`。水从地表沿裂隙进入根系与孔隙，连续运动成立。
- S07：`partial`。未调用 Seedance；已表现休眠、被水唤醒、菌丝和 `土臭素 Geosmin`，纪录片真实感仍需独立视觉审核。
- S08：`done`。真实干土纹理上完成接近与撞击，空间和落滴方向明确。
- S09：`done`。B1 呈现困住空气、形成气泡和开始上升。
- S10：`done`。B2 呈现气泡继续上升。
- S11：`partial`。B2 呈现到达表面并破裂，但气溶胶极细、可见度有限；B1/B2 土粒几何不完全连续。
- S12：`done`。在同一裂纹构图中连续变湿，没有拼接 R07/R03 冒充连续变化。
- S13：`done`。真实承雨叶片与真实移动雾林替换静态 R08。

逐镜详情见 `shot-status.yaml`。

## 新增真实素材

新增 3 个可审核真实母素材代理，完整页面、作者、平台、许可、下载日期、时间码、用途和限制见 `asset-manifest-remediation.csv`：

- R11：Pexels 4171514，雨落湿地面，仅作为冲击运动参考，不能证明干土首滴。
- R12：Pexels 32675101，真实移动雾林，用于 S13。
- R13：Pexels 32679329，真实叶片承雨和回弹，用于 S13。

原始外部下载文件保存在 `/private/tmp`，未纳入仓库；仓库只包含低清无声审片代理。

## Seedance 真实调用

仅 S09—S11 使用 `doubao-seedance-2-0-fast-260128`，9:16、720p、24fps、`generate_audio=false`：

1. B1 / S09：task `cgt-20260715200029-2bfck`，`succeeded`，费用 `unknown`，采用。
2. B2 / S10—S11：task `cgt-20260715200457-ct6d8`，`succeeded`，费用 `unknown`，采用并记录连续性限制。

累计 2 次，未因“更漂亮”重试，未调用其他付费视频模型。完整参数、使用量、状态和采用理由见 `seedance/call-log.json`；临时签名下载 URL 已在下载后删去。

## 动态预览处理

- B2 统一放慢到约 65.4% 速度后按锁定 S10/S11 边界切分，仅处理生成机制画面；旁白没有参与预览，也没有任何旁白变速。
- 全片固定显示“总导演整改动态验证预览 · 非成片”。
- 临时声音按近静默干旱、第一滴、地下低频、气泡破裂、环境展开五段组织，只用于动态判断。
- 未执行正式字幕、正式混音、完整成片或发布文件。

## QA 证据

- `qa/preview-ffprobe.json`
- `qa/preview-sha256.txt`
- `qa/preview-contact-sheet.jpg`
- `qa/shot-midpoints-contact-sheet.jpg`
- `qa/programmatic-contact-sheet.jpg`
- `qa/seedance/B1/contact-sheet.jpg`
- `qa/seedance/B2/contact-sheet.jpg`

## 未解决门禁

1. S01 仍缺真实高速单滴撞击干土素材。
2. S07 的真实显微纪录片质感需要独立视觉导演判断。
3. S11 气溶胶可见度与 B1/B2 几何连续性需要独立判断。

因此本生产包只声明动态验证预览完成，不声明 `review_ready: true`，也不批准正式合成。
