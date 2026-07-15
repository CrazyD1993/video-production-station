# 雨后泥土味｜定向整改 V2 生产报告

task_id: `petrichor-director-remediation-v2-001`  
revision: `2`  
用途：**46.80 秒干净动态验证预览（非成片）**  
`formal_composition: false`

## 交付结果

- 干净动态验证预览：`petrichor-remediation-v2-clean-preview.mp4`，540×960、24fps、H.264、无音轨。
- 机制 A 连续段：`mechanism-a-v2.mp4`，S05—S07，同一土层、同一光线、同一摄影机空间。
- 机制 B 连续段：`mechanism-b-v2.mp4`，S08—S11，同一孔隙截面与运动方向。
- 旁白：未加入。
- 字幕：未加入。
- 正式音乐与混音：未加入。
- 锁定旁白、TTS、13 镜顺序和时间线均未读取或修改。

## 关键整改

- S01：R07 干裂土与 R11 真实撞击运动匹配合成，替换规则图形雨滴。
- S04：R02 未能提供清楚脱落事件，改用 R14 的真实叶尖水滴，代理段中可见聚集、拉长、脱落。
- S05—S07：重建为同一 `soil-column-R05-v2` 母场景，依次展示入渗、吸附、微生物轻微恢复。
- S08—S11：以 G02 为锚重建；S09 使用最终授权重试 G04，S10 保持 1.000 倍速，S11 在同一表面帧程序化完成短促破泡与极细气溶胶。
- S12：改为多点、裂缝驱动、异步不规则湿润。
- S13：保留 R13→R12 结构，只统一色彩、黑位和情绪过渡。

## Seedance 真实调用

模型固定为 `doubao-seedance-2-0-fast-260128`。累计 4 次，达到总硬上限；本轮新增 2 次，未调用其他付费视频模型。

1. 原 G01：`cgt-20260715200029-2bfck`，废弃。
2. G02：`cgt-20260715200457-ct6d8`，仅保留 S10 上升段，原始时长 5.041667 秒，速度比例 1.000。
3. 新 B1 候选 G03：`cgt-20260715230936-qwwsz`，因开场已有气泡、缺少入水压缩包围过程而废弃。
4. 最终 B1 候选 G04：`cgt-20260715231939-bd75j`，采用前 3.05 秒，并以 0.375 秒（9 帧）匹配过渡到 G02 精确桥接帧。

所有费用均为接口不可得的 `unknown`，未推算。完整请求参数、task id、状态、usage、采用/弃用理由见 `seedance/call-log-v2.json`。

## 时间与速度

- 锁定时间线：00.00—46.80 秒；H.264 CFR 量化后的容器时长为约 46.833 秒。
- S10 G02：原始 5.041667 秒中截取 3.15 秒，1.000 倍速；无超过 ±8% 的重定时。
- 其余动态母素材均按原速截取；静态与程序化镜头按目标帧数直接生成。
- 逐镜原始时长、目标时长、时间码和速度见 `asset-manifest-v2.csv`。

## QA 证据

- `qa/preview-ffprobe.json`
- `qa/mechanism-a-ffprobe.json`
- `qa/mechanism-b-ffprobe.json`
- `qa/decode-verification.json`
- `qa/media-sha256.txt`
- `qa/shot-midpoints-contact-sheet.jpg`
- `qa/mechanism-a-contact-sheet.jpg`
- `qa/mechanism-b-contact-sheet.jpg`
- `qa/mechanism-b-continuity-contact-sheet.jpg`

本报告只声明生产包已具备独立复核条件，不构成 Reviewer A/B/C 结论，不批准正式合成。
