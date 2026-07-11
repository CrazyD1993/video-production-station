# 05 Seedance 手动交接规范

## 模式判断

### 模式 A：API

启用条件：OpenMontage `provider_menu_summary()` 将 Seedance 支持网关判定为 configured。

调用约束：

```yaml
tool: video_selector
preferred_provider: seedance
operation_priority:
  - image_to_video
  - reference_to_video
  - text_to_video
aspect_ratio: "9:16"
preview:
  model_variant: fast
  resolution: 480p
  duration_seconds: 5
```

低成本样片批准后才可锁 seed、切 standard/720p。不得一次批量调用所有镜头。

### 模式 B：手动网页/客户端

本试点当前采用此模式。用户无需提供账号密码或 Cookie。

OpenMontage/主仓库交付每个镜头的：

- 已批准首帧或参考图；
- Seedance 运动提示词；
- 目标时长、画幅、镜头运动、动作节拍；
- 禁止项与结构示意标记；
- 文件名与 take 编号。

## incoming 目录

```text
/Users/dengqi/Documents/OpenMontage/projects/
└── xhs-ai-science-001-airplane-window-hole/
    └── incoming/
        └── seedance/
            ├── S01_take01.mp4
            ├── S01_take02.mp4
            ├── S04_take01.mp4
            └── S06_take01.mp4
```

视频大文件不复制到 `video-production-station`，不提交 Git。

## 单镜头交接单

```yaml
scene_id: S01
approved_keyframe: KF1-01
filename: S01_take01.mp4
duration_seconds: 3
aspect_ratio: "9:16"
camera: "极慢微距推进，最后0.5秒停住"
action_beats:
  - "0-1.5秒：小孔清晰，手指从右侧进入"
  - "1.5-2.5秒：指尖接近但不接触"
  - "2.5-3秒：镜头停住，保留疑问"
negative_constraints:
  - "不触碰或堵住小孔"
  - "不生成文字、Logo、水印"
  - "不出现裂纹、爆炸、失压事故"
```

## 回收审核

1. `ffprobe` 验证分辨率、时长、帧率和音轨。
2. 每个 take 登记来源、生成平台、日期、实际成本和使用权状态。
3. 只把用户选中的 take 写入 `selected_take`。
4. 任何镜头未过 Gate 3，完整合成保持 blocked。
5. Phase 2 三镜头合同必须从 manifest 读取：S01=3 秒、S04=5.5 秒、S06=4.5 秒，总计 13 秒。
