# Reviewer A｜Contract QA

## 审核结论

**BLOCK**

Alpha 成片本体的媒体参数、13 镜帧预算、锁定旁白、临时字幕、Seedance 9/10 调用边界及非发布母版状态均有提交内证据支持；但绑定生产提交缺失渲染和依赖清单共同引用的临时环境声源文件，也没有该音源的哈希与来源/许可记录。该缺口使音频链无法从绑定提交复现，未满足本轮“既有临时环境声”与依赖完整性交付要求，因此阻断进入 Reviewer C 放行。

## 独立审核边界

- 任务：`petrichor-alpha-finalization-001`
- Reviewer：A / Contract QA
- 唯一生产证据提交：`4bccde9fb910ddfd0432f51e7a781fc6b76c78ab`
- 唯一生产证据快照：`/private/tmp/petrichor-alpha-production-4bccde9`
- 本结论未使用当前工作区未提交内容作为生产证据。
- 本结论形成前未读取 Alpha 的 `production-report.md`、`production-status.yaml`、Production 自评或 Reviewer B/C 报告。
- 用户覆写只将 Seedance 累计硬上限从 4 提高到 10，并要求“先诊断提示词，再进行修正”；其余锁定任务边界继续沿用。

## 阻断问题

### A-01｜绑定提交缺失已引用的环境声音源

- 镜头/时间：全片音频链，`00:00.000–00:46.800`。
- 严重度：**BLOCKING**。
- 合同依据：锁定中继要求 Alpha 加入“既有临时环境声与基础音量平衡”，并交付依赖资料（`00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md:22,57,59`）。
- 证据：
  - `petrichor-alpha-finalization-001/alpha_config.py:16` 将环境声锁定为 `director-remediation-pass-001/work/temporary-validation-ambience.wav`。
  - `petrichor-alpha-finalization-001/render_alpha.py:244-250` 在最终混音时实际读取该文件；`dependencies.yaml:12` 也把它登记为音频依赖。
  - 对生产快照执行文件存在性检查，结果为 `ambience=missing`；`ffprobe` 对该路径返回 `No such file or directory`。
  - 对绑定提交执行 `git ls-tree -r --name-only 4bccde9fb910ddfd0432f51e7a781fc6b76c78ab -- <ambience path>`，没有任何条目；同一提交能列出 Alpha MP4 与锁定旁白 WAV，故不是路径探测方式失效。
  - `asset-dependency-manifest.csv` 覆盖了逐镜画面源，但没有环境声条目；现有许可文件也没有该环境声的来源、许可或项目自制声明，`dependencies.yaml` 未记录其 SHA-256。
  - 27 项合同测试虽全部通过，但 `_prepare()` 仅检查三条 Seedance 入选素材（`render_alpha.py:54-70`），没有在混音前检查环境声存在性，因此测试通过不能消除该缺口。
- 影响：绑定提交无法完整重跑 `render_alpha.py`；也无法证明成片内环境声与登记依赖一一对应，或核验其授权/项目来源。
- 建议：在新的 Production 修复提交中恢复**实际用于本 Alpha 混音的同一 WAV**到登记路径，补充 SHA-256、来源/许可或项目自制证明，并把环境声存在性及哈希加入前置合同测试；随后重新执行全量渲染/等价性验证、完整解码、媒体 SHA 与 Reviewer A 复核。不得以从最终混音中反向分离出的近似音轨替代原始依赖。

## 逐项合同核验

| 检查项 | 结果 | 独立证据 |
|---|---|---|
| 13 镜顺序与帧预算 | PASS | `alpha_config.py:31-50` 固定 S01–S13 共 1123 帧；直接 `ffprobe -count_frames` 得到 H.264 视频 `720×1280`、`24/1`、`nb_frames=1123`、`nb_read_frames=1123`。逐帧 PTS 复算为 1123 帧、0 个异常步长、步长 `0.041666–0.041667s`、末帧 PTS `46.750000s`。 |
| 总时长与技术参数 | PASS | 直接探测：容器 `46.800000s`；视频轨 `46.791667s`（1123/24 的合法帧量化）；H.264/yuv420p/CFR24；音频 AAC、48kHz、双声道、`46.800000s`。全片视频与音频完整解码退出码 0。 |
| Alpha 媒体 SHA | PASS | 直接计算 `petrichor-alpha-v1.mp4` SHA-256 为 `0ef05f8da3e177a71aa4757e61b98a109399469b3e79110cbd47d91895fb289c`，与 `qa/media-sha256.txt` 一致。 |
| 锁定旁白文件 | PASS | 直接计算旁白 WAV SHA-256 为 `914a1728f12c87bff8f6f2fe607ab1708a5559a58ab0abb5d18cdb214a5f948e`，与 `alpha_config.py:17` 及 `dependencies.yaml` 一致；源音频为 PCM 48kHz 单声道、`45.937042s`。 |
| 旁白原速与 0.2 秒偏移 | PASS | `render_alpha.py:45-51` 只做 `adelay=200`、补齐、裁切、音量和平混；无 `atempo`、`asetrate`、`rubberband` 或动态处理。`dependencies.yaml` 记录 `narration_speed_ratio: 1.000`、`narration_offset_seconds: 0.200`。对应合同测试通过。 |
| Alpha 有声可审 | PASS | 成片包含 AAC 48kHz 双声道音轨；直接音量检测为均值 `-26.8 dB`、峰值 `-12.9 dB`，不是静音轨。环境声源文件完整性另见 A-01。 |
| 临时审片字幕 | PASS | `temporary-review-subtitles.srt` 共 9 条；合同测试确认逐句文字来自锁定时间戳文件且仅整体后移 0.20 秒。`render_alpha.py:228-240` 将字幕烧录进 1123 帧视频；提交内 `qa/shot-midpoints-contact-sheet.jpg` 可见克制的底部白色临时字幕。 |
| Seedance 累计上限 | PASS | 用户覆写后的硬上限为 10。`call-log-alpha.json` 记录继承 4 次、本轮调用 5–9 共 5 次、累计 9/10；日志中没有第 10 次调用，目录中也只有与调用 5–9 一一对应的 5 个新输出。五个输出 SHA 均与调用日志一致。 |
| Seedance 范围与参数 | PASS | 新调用只覆盖 S01、机制 A、S12；固定 `doubao-seedance-2-0-fast-260128`、9:16、720p、24fps、无模型音频。没有对任务禁止继续生成的 S09–S11 发起新调用。 |
| “先诊断，再修正”逐次闭环 | PASS | `prompt-diagnosis.md` 与 `call-log-alpha.json` 一一对应：S01 初诊→调用5失败诊断→调用6定时动作修正；机制 A 初诊→调用7“珠串/蓝通道/白线”失败诊断→调用8真实根土首帧与伪影禁令修正；S12 先诊断旧版橙光/均匀变色，再形成调用9修正提示。没有无诊断的追加重试。 |
| 逐镜画面依赖与许可 | PASS（音频除外） | 逐行解析 `asset-dependency-manifest.csv`：所有 `used` 与 `acquired_not_used` 画面源路径在生产快照内存在；S05–S07 递归落到 G08、S09–S11 递归落到 G02，复用次数均明确为 3；G05/G07 拒绝记录、G03 列修正、R14 直达 Mixkit 许可证据均存在。环境声音频例外见 A-01。 |
| 必交机制文件 | PASS | `mechanism-a-final.mp4`、`mechanism-b-final.mp4` 均存在；`qa/media-sha256.txt` 分别登记 SHA-256 `20fc677c79257d140f1a3057580b7566a340a4a624ba7872af302e4110fe6355` 与 `b53a7d04d1b20ce992289a14825699bde3e2a96a3562b407420718d8db37d844`。 |
| S01 硬阶段证据 | PASS（保留视觉复核） | 入选 G06 的日志确认单滴、干燥颗粒土、接触和即时局部变湿均可见，同时承认水冠与土粒抬升较弱；`render_alpha.py` 使用 G06 入选版本。是否“一眼可见”及弱响应是否达到导演阈值应由 Reviewer B 正常速度观看裁定，不构成新增付费调用授权。 |
| 不提前制作发布母版 | PASS | 输出名为 `petrichor-alpha-v1.mp4`；`dependencies.yaml` 明确 `human_final_decision: pending`、`release_master_started: false`，未发现发布母版产物。 |

## 验证记录

- `PYTHONDONTWRITEBYTECODE=1 …/.venv/bin/python -m unittest discover -s tests -v`：**27 tests，0 failures，exit 0**。
- `ffprobe -count_frames`：视频 1123/1123 帧，H.264 720×1280 CFR24；音频 AAC 48kHz stereo；容器 46.800000 秒。
- 逐帧 PTS 扫描：1123 帧，`bad_steps=0`。
- `ffmpeg -v error ... -f null -` 全量视频/音频解码：exit 0。
- 生产快照文件与绑定 commit 树双重检查：环境声路径均缺失。

## 放行条件

只有 A-01 在新的、明确绑定的 Production 修复提交中闭环，并由 Reviewer A 针对新快照复核后，结论才可重新评估；当前不得因成片本体可播放而跳过依赖与来源完整性门禁。
