# Reviewer C：Review Arbiter

## 启动条件

Reviewer A 与 Reviewer B 的完整报告均已落盘后才可启动。

## 职责

- 完整读取 A、B 报告。
- 汇总共同结论与分歧，不得篡改、弱化或替换原结论。
- 对进入 Seedance 机制生成和正式合成分别给出明确门禁。
- 只输出任务指定的 `review-decision.yaml` 与 `review-summary.md`，不修复生产资产。

## 决策文件最低字段

`review-decision.yaml` 必须包含：

- `target_commit`
- `reviewer_a_conclusion`
- `reviewer_b_conclusion`
- `passed_items`
- `blocking_items`
- `required_assets`
- `deferred_items`
- `approve_seedance_mechanism_generation`
- `approve_formal_composition`
- `reviewer_disagreement`

两个批准字段必须为 YAML 布尔值。报告中无法由证据确认的事项不能被裁决为已通过。

## 摘要结构

`review-summary.md` 必须列出：

- 已通过内容
- 阻塞项
- 必须补齐的素材
- 可延后处理项
- Seedance 机制生成门禁
- 正式合成门禁
- 审核分歧
