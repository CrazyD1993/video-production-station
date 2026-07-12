---
task_id: typhoon-eye-12s-packaged-ab-001
status: completed
branch: experiment/openmontage-pilot
commit_sha: abae9a89ea271b09541d81037638be624d2985d5
completed_at: "2026-07-12T04:20:00+08:00"
---

# 执行摘要

V2纯视觉门禁已解除。已生成两个12秒完整包装样片：A为已验证克隆音色的克制悬念版，B为火山Seed-TTS 2.0官方自然女声的自然解释版。两版使用完全相同的V2画面、六条短字幕、低频气象纪录片BGM、轻风、S03远海浪与侧链混音。MP4仅保存本地，GitHub只提交文字记录和静态联系表。

# 修改文件

- `output/typhoon-eye-12s-packaged-A.mp4` — 本地新增、Git忽略 — 克隆音色克制悬念完整包装版。
- `output/typhoon-eye-12s-packaged-B.mp4` — 本地新增、Git忽略 — Seed-TTS 2.0官方自然女声完整包装版。
- `05-完整包装样片记录.md` — 新增 — 记录配音、字幕时间轴、BGM/环境音、混音、ffprobe规格和本地/GitHub边界。
- `review-package/typhoon-eye-packaged-contact-sheet.jpg` — 新增 — 包装样片6帧静态联系表。
- `review-package/README.md` — 修改 — 增加包装联系表与MP4不上传说明。
- `.gitignore` — 修改 — 仅为新包装联系表增加例外，不解除MP4、WAV或中间帧忽略。
- `video-handoff/status.yaml` — 修改 — 记录A/B输出规格、哈希、响度、音色和新门禁。
- `00_项目总控/AI协作中继/STATE.yaml` — 修改 — 阶段改为A/B包装样片已就绪。
- `当前工作台.md` — 修改 — 更新为等待用户上传A/B并选择配音。
- `tests/test_ai_relay_contract.py` — 修改 — 验证A/B状态、共同规格、哈希、联系表和GitHub边界。
- `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md` — 覆盖修改 — 写入本回执。

# 实际执行的命令

- 读取“时间有回声”中已验证克隆音色和火山Seed-TTS 2.0配置，不输出密钥。
- 通过火山TTS API分别生成A/B两版各三句旁白；去除首尾多余静音，保留句中停顿并轻微匹配时长。
- 使用本地faster-whisper small复核A/B完整旁白的可懂度。
- 使用Pillow生成360帧可控短字幕透明图层，并用FFmpeg烧录到V2画面。
- 使用FFmpeg合成低频持续音、限带风声/云层流动感和S03远海浪。
- 使用侧链压缩和综合响度归一分别混合A/B，生成两个本地MP4。
- `ffprobe -count_frames`、FFmpeg完整解码、loudnorm分析、SHA256校验和静态联系表视觉检查。
- 项目单元测试、时间轴校验、生产合同校验和 `git diff --check`。
- 提交并推送 `experiment/openmontage-pilot`。

# 测试与验证

- TTS：已验证克隆音色和Seed-TTS 2.0官方自然女声均生成成功；未使用系统语音、`say`或003旧配音。
- 可懂度：faster-whisper对A/B两版都完整识别三句核心文字，无漏句。
- 字幕：6/6短句已实际查看，均为单行、单句显示，不遮挡风眼、S02箭头或S03右上标签。
- A版：1080×1920，H.264，30fps CFR，360帧，12.000秒，AAC 48kHz立体声；综合响度约-16.6 LUFS，真峰值约-2.0 dBTP。
- B版：1080×1920，H.264，30fps CFR，360帧，12.000秒，AAC 48kHz立体声；综合响度约-16.2 LUFS，真峰值约-4.7 dBTP。
- A版SHA256：`7f79920452c363a8b4560a50a9c7e0dfc2a2dcee02e792ab348ffd9c8ed869f8`。
- B版SHA256：`657ffaec58b3237d5dfc1c66682ab4f84387520bc3f5ad9edc1cd7eea291ece6`。
- 两版都完整解码通过。
- 包装联系表：1080×1280 JPG，已实际查看，6个字幕节点与画面结构无冲突。

# 与任务要求的差异

- A版克隆音色第一次使用过多重停顿标点，时长超出镜头合同；该输出未进入包装。使用相同文字减少多余标点重新生成后，只进行轻微节奏匹配。
- FFmpeg当前构建不含libass字幕滤镜，因此未直接使用ASS烧录；替代实现为按同一时间轴、字体、颜色和动画在本地渲染透明字幕帧序列。
- 用户要求不上传MP4；本次只为包装静态联系表增加 `.gitignore` 例外，没有解除任何MP4/WAV忽略规则。
- 机器可懂度和响度检查已通过；A/B最终听感与配音风格选择依照任务要求留给用户和ChatGPT。

# 当前阻塞点

等待用户将A/B两个本地MP4上传ChatGPT并选择配音。

# 需要ChatGPT判断的问题

在画面、字幕和混音完全相同的前提下，选择A版已验证克隆音色的克制悬念，还是B版Seed-TTS 2.0官方自然女声的自然解释。

# 完整回答

A/B两个12秒完整包装样片已生成。两版均为1080×1920、30fps CFR、360帧、12.000秒、AAC 48kHz立体声；画面、字幕、BGM、环境音和混音一致，只更换配音。MP4未上传GitHub。当前停在A/B配音选择门禁，未扩展25秒成片。
