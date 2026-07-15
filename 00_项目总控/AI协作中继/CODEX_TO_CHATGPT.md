---
task_id: petrichor-asset-board-v1-001
status: completed
branch: experiment/openmontage-pilot
commit_sha: pending
completed_at: "2026-07-15T12:35:00+08:00"
---

# 执行摘要

「雨后泥土味」素材板与来源审核 V1 已完成。13个锁定镜头及时间范围未改，已取得 10 个不同真实母素材的审片代理（3个视频、7张照片），并完成机制 A/B 静态草图、素材板 JPG/PDF 和 18.25 秒无声低清预览。

# 产出

- 主目录：`06_成片工程/雨后泥土味/asset-board-v1/`
- 必需文件：`shot-plan-v1.yaml`、`asset-manifest-v1.csv`、`missing-assets-v1.md`、`seedance-prompts-draft-v1.md`、`petrichor-asset-board-v1.jpg`、`petrichor-asset-board-v1.pdf`、`petrichor-asset-board-preview-v1.mp4`。
- 机制 A：`mechanism/mechanism-a-geosmin-v1.png`
- 机制 B：`mechanism/mechanism-b-aerosol-v1.png`

# 来源与授权

- 10 个真实母素材代理全部来自 Pexels 原始素材页。
- 每条已记录文件名、原始页面、作者/上传者、平台、许可类型与页面、下载日期、允许范围和镜头号；授权记录完整。
- 视频为无声 720×1280 审片代理，正式合成前需根据最终取舍重取高清源文件。

# 缺口与门禁

- 缺失正式动态镜头：`S01, S05, S07, S08, S09, S10, S11, S12, S13`。
- Seedance 只保留机制 A/B 两个文字草案；本轮未执行。
- 黑场/定格只规划 S01 撞击后与 S11 破泡后两处，均未进入预览或成片。
- 当前阻塞点：等待人工确认真实素材取舍、两个 Seedance 候选与必补缺口；不进入正式合成。

# 测试与验证

- 契约测试通过：13镜时间一致、真实素材不少于7、同一母素材使用不超过2次、来源字段完整。
- 预览：18.25秒，540×960，24fps，H.264，音轨0条。
- 素材板：2160×3840 JPG；PDF 1页，完成 Poppler 渲染回验。
- 锁定旁白未重新生成、未改文字、未变速、未压缩句间停顿。

# 付费与成片状态

- Seedance/其他付费视频模型调用：`0`
- 完整 47–48.5 秒成片：未制作
- 字幕成片/正式混音：未制作

# 需要 ChatGPT / 人工判断

1. 10 个真实母素材代理中哪些保留。
2. 是否将 S07 机制 A 与 S09–S11 机制 B 作为两个 Seedance 候选。
3. 是否按缺口表继续补 S01 / S08 / S12 / S13 真实动态。
