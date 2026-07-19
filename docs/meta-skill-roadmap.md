# yao-meta-skill 使用路线图

## 决策

`yao-meta-skill` 不在 06A 直接使用，也不作为 06B 第一接入模块。

推荐状态：`defer`

原因：它是 Skill 工程治理工具，适合创建、评估、打包和维护可复用 Skill。当前阶段要先完成业务工具选型和安全输入契约，不应直接生成或改写本项目业务内容。

## 适合使用的阶段

| 阶段 | 是否使用 | 用法 |
| --- | --- | --- |
| 06A 工具评估 | no | 只读评估其方法和治理边界 |
| 06B 第一模块接入 | no | 先人工适配 `yao-geo-page-audit`，不要急着封装内部 Skill |
| 06C 工作流固化 | yes | 将已验证的页面审计、意图映射、知识库安全输入流程封装为内部 Skill |
| 07 复测与监测 | yes | 为复测采样、人工评分、输出审核和 crawler PoC 建立 eval 与权限门 |
| 稳定维护期 | yes | 建立 SkillOps、trigger eval、输出质量检查、版本和漂移报告 |

## 推荐路线

### 06B 后置准备

先不生成 Skill 文件，只记录：

- 输入文件清单。
- 禁止输入清单。
- 输出目录。
- 人工审核门。
- 失败回滚方式。
- 与六层体系的层级绑定。
- 不自动写网站的规则。

### 06C 内部 Skill 草案

用 `yao-meta-skill` 生成或改造内部 Skill：

- `yhl-geo-page-audit-adapter`：封装公开路由 Page Audit。
- `yhl-geo-intent-map-adapter`：封装 Redwood 30 题到意图矩阵。
- `yhl-geo-public-kb-adapter`：封装安全知识库事实卡和禁用表达。
- `yhl-geo-monitoring-plan-adapter`：封装监测字段、复测计划和人工评分表。

每个内部 Skill 必须包含：

- `SKILL.md`。
- `agents/interface.yaml`。
- `references/input-boundary.md`。
- `references/output-contract.md`。
- `evals/trigger_cases.json`。
- `evals/expected_artifacts.json`。
- `reports/output-risk-profile.md`。

### 07 复测治理

如果后续评估 crawler，先用 `yao-meta-skill` 建立治理包：

- crawler 权限说明。
- 平台服务条款风险。
- 登录态和账号隔离。
- 采样频率。
- raw answers、logs、screenshots 的隐私处理。
- 人工评分和证据抽样。
- 输出发布规则。

## 使用边界

`yao-meta-skill` 不能替代业务审核。它可以生成 Skill 包和质量门，但不能决定：

- 哪些 internal-review 内容可公开。
- 哪些品牌事实可成为公开断言。
- 哪些文章样稿可发布。
- 哪些 Schema 可上线。
- 哪些采样数据可公开。

所有这些决策仍由本项目数据治理和人工审核流程处理。

## 产物位置建议

如果后续使用，产物应放在新的内部 Skill 目录或独立工具仓库，不放入当前网站运行路径。

当前网站仓库中只应保留：

- 选型文档。
- 输入输出契约。
- 审核记录。
- 未来接入计划。

不应把生成的完整 Skill 包塞进当前 Next.js 网站目录。
