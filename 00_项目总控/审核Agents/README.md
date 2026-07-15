# 独立审核 Agents

本目录定义视频制作流程中的轻量审核角色。审核与生产执行分离，角色定义可复用，但每次审核必须绑定明确的 Git commit。

## 固定顺序

1. Production Agent 完成并提交生产资产。
2. Reviewer A（Contract QA）与 Reviewer B（Visual Director）从同一指定 commit 的隔离快照并行审核。
3. A、B 在形成独立结论前，不得读取 Production Agent 的自我评价、对方报告或未提交工作区。
4. Reviewer C（Review Arbiter）仅在 A、B 报告完整落盘后启动，原样保留两位 Reviewer 的结论并汇总门禁。

## 通用权限边界

- 审核为只读任务；不得修改、替换、下载或生成生产资产。
- 审核结果只写入任务指定的报告文件，不自动修复。
- 不调用生成模型、TTS 或付费视频模型，不制作预览或成片。
- 所有事实证据必须来自指定 commit 的隔离快照；工作区未提交内容不能作为证据。
- 每个问题必须填写：`镜头编号`、`时间位置`、`证据`、`严重程度`、`建议`。

## 角色

- [Reviewer A：Contract QA](contract-qa.md)
- [Reviewer B：Visual Director](visual-director.md)
- [Reviewer C：Review Arbiter](review-arbiter.md)
