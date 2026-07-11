# Phase 3 Seedance 运动合同

时间轴唯一来源：`../../03-生产清单模板.yaml` 的 `visual_sample_12` 和 `seedance_contracts`。

当前状态：`blocked_by_image_approval`。本文件只定义获批图片后的单镜头运动，不授权现在调用 Seedance。

结构标记：`典型结构示意，不对应具体机型`。

## V01 / KF1：3 秒

```text
One continuous photoreal macro shot, exactly 3 seconds, no cuts. Keep the real commercial-aircraft passenger-window hole unmistakably visible from the first frame. The hole and surrounding curved window material occupy more than 70% of the vertical 9:16 frame. A natural fingertip approaches slowly but never covers or touches the hole. Use only a subtle camera drift, authentic transparent material, restrained cabin reflections and realistic skin anatomy. No text, logo, extra holes, incorrect hole position, plastic CGI surface, deformed fingers, contact, blockage, cracks or accident imagery.
```

文件名：`V01_take01.mp4`。

## V02 / KF2：5 秒

```text
One continuous photoreal engineering macro visualization, exactly 5 seconds. Preserve the approved real curved aircraft-window material while part of the window becomes a physically credible semi-transparent cutaway. 0-1.5s: reveal curved pane spacing without fixing a universal pane count. 1.5-3.5s: restrained air-path particles move from the cabin side through the small hole into the specific inter-pane space. 3.5-5s: the pressure path settles visually on the typical load-bearing pane while the full window remains intact. Maintain credible thickness, curvature, seals and refraction. No flat rectangles, labels inside generation, cartoon infographic, exact measurements, cracks, deformation or specific aircraft branding.
```

文件名：`V02_take01.mp4`。后期标注：`典型结构示意，不对应具体机型`。

## V03 / KF3：4 秒

```text
One continuous photoreal recovery shot, exactly 4 seconds. Begin with the approved semi-transparent engineering cutaway, then let the window return smoothly to a complete realistic passenger-window view. Keep the typical load-bearing pane intact and keep the small hole visible throughout. Use a very slight pullback and gentle cloud motion outside the window. End on a calm, believable cabin observation: the hole reads as intentional engineering, not damage. No comparison layout, no blockage experiment, no accident, no crack, no pressure numbers, no text, logo or watermark.
```

文件名：`V03_take01.mp4`。后期标注：`典型结构示意，不对应具体机型`。

## 执行规则

- 用户必须先从真实六图联系表中选定 KF1、KF2、KF3。
- 只对选定图片执行 `image_to_video`；不使用纯文生视频替代关键帧门禁。
- 每个镜头单独生成、单独审核，不批量调用。
- 手动模式不接收账号密码或 Cookie。
