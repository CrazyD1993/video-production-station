# 关键帧手动交接

当前状态：`blocked_by_reference_analysis`。

## 流程

1. 三条参考视频到齐并完成 OpenMontage 拆解。
2. 将拆解得到的抽象视觉规律回填到 `prompts/*.yaml`。
3. 用户使用外部图片工具生成六张 PNG，放入 `incoming/`，文件名必须为：
   `KF1-01.png`、`KF1-02.png`、`KF2-01.png`、`KF2-02.png`、`KF3-01.png`、`KF3-02.png`。
4. 图片必须接近 9:16，最低 720×1280，推荐 1080×1920，格式为 PNG。横图、方图和 2:3 图片直接拒绝。
5. 运行：

```bash
/Users/dengqi/Documents/OpenMontage/.venv/bin/python \
  scripts/build_keyframe_contact_sheet.py \
  '08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/incoming' \
  '08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/contact-sheet/keyframes.jpg'
```

6. Codex 检查尺寸、格式、数量、畸变、事实风险和参考相似度；不代替用户选择。
7. 用户从真实联系表中为 KF1/KF2/KF3 各选一张，选中图复制到 `selected/`，其余进入 `rejected/`。图片始终不提交 Git。

## 目录职责

- `prompts/`：六张候选的独立交接文件。
- `incoming/`：用户生成的原始候选图。
- `contact-sheet/`：自动生成的 2 列×3 行联系表；图片等比例缩放并留边，不裁切原始构图，标签位于画面下方。
- `selected/`：用户明确选中的三张图。
- `rejected/`：未选候选，保留用于审计和避免重复生成。
