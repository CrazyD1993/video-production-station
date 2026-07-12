# 台风眼 GitHub 审图包

本目录仅用于ChatGPT/GitHub审图。图片为JPEG质量约80的压缩预览，不是原始无损文件；NASA卫星结构参考图未包含在本目录中。

全部候选均为：

- 1080×1920、9:16、JPG；
- `non_event_specific_visual_reconstruction: true`；
- 保留“AI视觉重建｜非真实卫星观测”标识；
- 不对应巴威某次真实卫星观测、真实现场或真实灾情。

## 文件对应关系

| 审图文件 | 本地原始文件 | 原始PNG SHA256 | 原始尺寸 | Codex评分 | 结论 |
|---|---|---|---|---:|---|
| `TE-KF1-A-preview.jpg` | `TE-KF1-A.png` | `5d60e99237e9bb791a2dd47c82a46e42649058a1710c62ff63fbad003c8b4ff1` | 1080×1920 | 8.9 | KF1首选 |
| `TE-KF1-B-preview.jpg` | `TE-KF1-B.png` | `57aba51227a5482cea87946d2507b39da9a250d745fce9f013a0d22f298ccfd6` | 1080×1920 | 8.3 | KF1备选 |
| `TE-KF2-A-preview.jpg` | `TE-KF2-A.png` | `cb8cb0b1b238ceaeefe5d8d9d7bb27236e233f81d39564eb54e373dd2b8ac741` | 1080×1920 | 8.3 | KF2首选 |
| `TE-KF2-B-preview.jpg` | `TE-KF2-B.png` | `4d6b3b72018e64bcee74bcb1261f2c0e4c03a418111e17bda01cee6a146d5a42` | 1080×1920 | 6.5 | 不推荐：双眼区/拼接歧义 |
| `TE-KF3-A-preview.jpg` | `TE-KF3-A.png` | `21dce24509373b5bcadc6b2b0192f5ddd2f18cbb9bf27cb0f6c570c237a046cd` | 1080×1920 | 7.9 | KF3备选 |
| `TE-KF3-B-preview.jpg` | `TE-KF3-B.png` | `071b1217a8d6592f9cba27da920b70c85cc12f3b01d9cb5eac4490e6110aeb0f` | 1080×1920 | 8.6 | KF3首选 |

`typhoon-eye-contact-sheet.jpg` 为2列×3行总览，顺序依次为KF1-A/KF1-B、KF2-A/KF2-B、KF3-A/KF3-B。

`typhoon-eye-packaged-contact-sheet.jpg` 为12秒完整包装样片的6帧静态联系表，1080×1280 JPG，SHA256为 `1504992e000d417c34b192fa0f2bb3e1496fe431d92aede5d666edb9b361d059`。A/B两版画面和字幕完全一致，因此只保留一张包装联系表；MP4不上传GitHub。

`typhoon-eye-25s-contact-sheet.jpg` 为25秒B版完整成片的11帧静态联系表，1120×1472 JPG，SHA256为 `20f0cc4827a1d37b22838e572b7dd47a3ee05f56c750f5f59ad5084edd285ad9`。抽帧覆盖台风眼钩子、眼墙上升、眼内缓慢下沉、增温变干、风速向中心减弱、相对平静和另一侧眼墙回收。

`typhoon-eye-25s-ffprobe.json` 保存25秒成片的机器可读技术参数及本地MP4 SHA256。MP4仍只保存在本地 `output/typhoon-eye-25s-packaged-B.mp4`，不上传GitHub。

## Codex推荐组合

**TE-KF1-A + TE-KF2-A + TE-KF3-B**

关键帧已完成审批，用户已选择B版火山Seed-TTS 2.0自然女声。25秒完整成片已生成并停在最终人工审核门禁。
