# OpenMontage 接入试验

## 试验目的

本目录是 `video-production-station`（内容与运营中枢）与独立本地工具 OpenMontage（视频生产执行层）之间的文档桥接层。

- 主仓库继续管理账号定位、选题、事实核查、发布计划、数据复盘和项目状态。
- OpenMontage 独立位于主仓库同级目录：`/Users/dengqi/Documents/OpenMontage`。
- 不复制 OpenMontage 源码，不将其部署为线上服务，不发布其修改版。
- 第 003 条 R1/R2 原样保留，视为自研 Remotion 技术验证历史；本试验不再修改第 003 条。

## 固定版本

- 上游仓库：`calesthio/OpenMontage`
- commit：`2ab5773ef760b4906821d36514c59fcdf3b8f641`
- 许可证：AGPL-3.0-only
- 本轮使用方式：独立本地工具评估

## 当前结论

- OpenMontage 安装成功；Backlot 本地服务健康检查通过。
- 当前没有被 OpenMontage 识别为可用的图片、视频生成或 TTS Provider。
- Seedance 采用模式 B：OpenMontage 输出关键帧与运动交接单，用户在网页或客户端手动生成，文件回收到 OpenMontage 项目 `incoming/seedance/` 后再审核与合成。
- Phase 2A 已完成匿名账号主页访问与账号级分析；视频级拆解因没有稳定帖子视频输入而阻塞。优先请求 3 条具体帖子链接，无法读取时再请求本地 MP4。视频级拆解完成前不批准创意方向，不生成关键帧或 Seedance 样片。

## 文档导航

1. `00-环境与能力检查.md`：安装、Provider、Backlot、许可证结论。
2. `01-接入架构.md`：双仓库职责、数据流与安全边界。
3. `02-参考视频分析规范.md`：只学结构、不复制资产的分析规则。
4. `03-生产清单模板.yaml`：跨工具交接的机器可读清单。
5. `04-人工审批流程.md`：故事板、关键帧、Seedance 镜头三道门禁。
6. `05-Seedance手动交接规范.md`：API/手动双模式与回收命名。
7. `06-试点验收报告.md`：本轮完成度、风险和下一阶段估算。
8. `001-飞机舷窗小孔/`：首个试点的事实、创意、脚本、故事板和提示词。
