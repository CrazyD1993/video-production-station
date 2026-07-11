# 关键帧手动交接

## Phase 4B 当前状态

第一轮六图已完成身份核对和视觉事实审核，但全部禁止直接进入 Seedance。第一轮元数据清单见 `candidate-manifest.yaml`，带短哈希联系表仅保存在本地 `contact-sheet/keyframes-hashed.jpg`。

第二轮改用真实照片锚定、可控图层合成和完整真实舷窗三条路线，详细合同见 `PHASE4B_R2_PRODUCTION_CONTRACT.md`。当前因缺少权利清晰的真实舷窗呼吸孔参考图，第二轮六图均未生成。

---

# Phase 3 历史手动交接说明

当前状态：`ready_for_image_candidate_generation`。

OpenMontage 当前图片生成 Provider：`0/11 configured`。因此本轮不会在 OpenMontage 内生成或伪造六张候选。

## 用户生成步骤

1. 首选在你当前可用的 **ChatGPT 图片生成界面** 中逐张生成；如你已有其他支持 9:16 的图片工具，也可使用同一份中文或英文提示词。
2. 每个 YAML 只生成一张，不批量制造近似图：
   - `prompts/KF1-01.yaml` → `KF1-01.png`
   - `prompts/KF1-02.yaml` → `KF1-02.png`
   - `prompts/KF2-01.yaml` → `KF2-01.png`
   - `prompts/KF2-02.yaml` → `KF2-02.png`
   - `prompts/KF3-01.yaml` → `KF3-01.png`
   - `prompts/KF3-02.yaml` → `KF3-02.png`
3. 选择竖版 9:16，推荐 1080×1920，最低 720×1280，保存为 PNG。
4. 将六张图放入 `incoming/`。不要把账号密码、Cookie 或页面凭据写入项目。

KF1-01 和 KF1-02 的额外前置条件：

- 必须使用真实客机舷窗小孔图片作为视觉锚点。
- 不允许只凭文字猜测小孔孔位。
- 参考图片只用于结构和位置控制，不复制其画面。
- 不得将未授权参考图放入 Git 或中继文档。
- 如果没有合规参考图，KF1 保持阻塞，不生成候选。
- KF1 属于真实舷窗微距，不叠加“典型结构示意，不对应具体机型”；该标记只用于 KF2/V02 和 V03 仍显示剖面或承压层的部分。

## 收到六图后

Codex 将依次：

1. 检查六个文件的名称、PNG 格式、尺寸和 9:16 比例。
2. 生成 2 列×3 行联系表，图片等比缩放并留边，不裁切主体，标签放在图片下方。
3. 检查真实性、小孔辨识、孔位、透视、手部、透明件物理感、典型结构与竞品相似度。
4. 不替用户选择；等用户为 KF1/KF2/KF3 各选一张。

联系表命令：

```bash
/Users/dengqi/Documents/OpenMontage/.venv/bin/python \
  scripts/build_keyframe_contact_sheet.py \
  '08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/incoming' \
  '08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/contact-sheet/keyframes.jpg'
```

## 目录职责

- `prompts/`：六张候选的最终中英文交接合同。
- `incoming/`：用户生成的六张原始候选。
- `contact-sheet/`：实际 2 列×3 行联系表。
- `selected/`：用户明确选中的三张图。
- `rejected/`：未选候选，保留用于审计和避免重复生成。

图片、联系表和参考素材均不提交 Git。
