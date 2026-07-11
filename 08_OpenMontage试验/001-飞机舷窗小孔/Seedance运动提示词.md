# Seedance 运动提示词

当前模式：B（手动交接）。以下提示词只有在对应关键帧获批后使用。

## S01 / KF1：停留镜头，3 秒

```text
One continuous macro shot, no cuts, no zoom. A real commercial-aircraft passenger window breather hole remains sharp in the lower center. A human fingertip slowly enters from the right edge and approaches, then stops clearly before touching the hole. Extremely slow 3 cm camera push-in, subtle handheld micro-movement from a seated passenger, realistic acrylic curvature, fine surface scratches, cold blue daylight outside and warm cabin reflections. 0-1.5s: hole stays unmistakably visible. 1.5-2.5s: fingertip approaches. 2.5-3s: motion stops on the unresolved question. Natural cabin ambience only. No text, no logo, no watermark, no contact, no blocking, no cracks, no deformation, no accident, no exaggerated danger.
```

建议首帧：获批 KF1。文件名：`S01_take01.mp4`。

## S04 / KF2：原理镜头，8 秒

```text
Single continuous engineering macro visualization based on the approved realistic aircraft-window cutaway, no random cuts. Maintain exact curved transparent layers and the visible breather hole. The camera makes a slow 20-degree arc around the cutaway while subtle air particles move from the cabin side through the small hole into the designated inter-pane space; a restrained stress-light pattern gradually appears on the outer load-bearing pane. 0-2s: reveal real curved layers. 2-5s: air path becomes visible through the hole. 5-8s: focus transfers to the intact load-bearing outer pane. Photoreal material, authentic refraction and thickness, neutral engineering lighting. No written labels inside generation, no flat rectangles, no cartoon infographic, no glass cracking, no explosion, no pressure-wave spectacle, no fake experiment claim.
```

建议首帧：获批 KF2。文件名：`S04_take01.mp4`。结构标签由合成层添加。

## S06 / KF3：后果/反转镜头，7 秒

```text
One continuous photoreal aircraft-window cutaway shot, explicitly a calm engineering visualization. Begin with the approved comparison frame: the breather path is open and the inter-pane space is clear. A translucent removable patch slowly covers the hole without touching other structures; the subtle airflow particles stop and a light haze gradually forms in the inter-pane space while every pane remains completely intact. 0-2s: clear open path. 2-4s: translucent patch covers the opening. 4-7s: airflow fades and light condensation increases, then hold on the intact window as the reversal. Locked camera with a very slow rack focus only. No cracks, no explosion, no cabin decompression, no frightened passengers, no emergency lights, no realistic accident footage, no text, no logo, no watermark.
```

建议首帧：获批 KF3。文件名：`S06_take01.mp4`。后期必须叠加 `结构示意`。

## API 模式参数（未来启用时）

```yaml
preferred_provider: seedance
operation: image_to_video
aspect_ratio: "9:16"
preview:
  model_variant: fast
  resolution: 480p
  duration: "5"
final_after_approval:
  model_variant: standard
  resolution: 720p
  seed: "lock-approved-seed"
```

