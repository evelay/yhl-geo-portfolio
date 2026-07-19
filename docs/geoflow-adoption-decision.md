# GEOFlow 采用决策

## 决策

当前阶段不部署 GEOFlow，不把 GEOFlow 接入当前网站仓库，也不使用 `yao-geoflow-cli` 操作任何 GEOFlow 实例。

推荐状态：`defer`

## 原因

GEOFlow 是完整内容工程平台，不是轻量脚本库。只读检查确认它包含：

- Laravel 12 应用。
- PHP 8.3+ 和 Node/Vite 前端构建。
- PostgreSQL/pgvector、Redis、queue、scheduler、Reverb。
- 后台素材、提示词、标题库、关键词库、知识库和文章管理。
- OpenAI-compatible 和 Gemini 模型配置。
- 知识库切片、embedding、RAG 召回。
- REST API、Sanctum token、任务 CRUD、文章审核和发布。
- WordPress REST、通用 HTTP API、GEOFlow Agent 和远端静态站点分发。
- sitemap、`llms.txt`、TXT 地图和 JSON-LD 输出能力。

这些能力对长期 GEO 内容运营有价值，但会引入数据库、密钥、队列、模型调用、远端写入和自动发布面。当前元亨利作品集是静态交付项目，已明确不修改网站、不生成文章、不生成 Schema、不部署服务。因此 GEOFlow 不适合在 06A 或 06B 直接接入。

## 是否需要部署

不需要。

当前项目的优先目标是：

1. 固定公开页面和安全知识库边界。
2. 建立六层 GEO 工具选型。
3. 先用文档化 Skill 输出页面审计、意图映射、事实治理和监测口径。
4. 后续人工审核后再决定是否更新网站。

GEOFlow 的自动生产、审核发布和分发能力目前会放大治理风险。

## 是否应该建立独立 GEOFlow PoC

应该，但不在当前阶段执行。

推荐建立独立 PoC 的条件：

- 06B 页面审计、意图映射、跟踪口径已经完成。
- 已经有一套安全公开数据包，不含 `internal-review`、archive、完整 canonical 工作簿和客户隐私。
- 明确 PoC 目标是验证内容工程流程，而不是替换当前静态作品集。
- PoC 使用独立仓库、独立数据库、独立 `.env`、独立域名或本地端口。
- PoC 默认禁用自动发布和外部分发，只允许草稿和人工审核。

PoC 最小范围：

| 模块 | PoC 范围 |
| --- | --- |
| 知识库 | 只导入安全公开 JSON 或合成样例 |
| 模型 | 可先不用真实模型，或使用人工粘贴草稿模拟 |
| 文章 | 只生成草稿，不发布 |
| 分发 | 禁用 WordPress、HTTP API 和远端 Agent |
| 主题 | 仅评估是否能表达 GEO 证据页和知识库页 |
| 数据分析 | 只看字段模型，不接真实访问日志 |

## GEOFlow 与当前网站的关系

当前网站继续保持静态作品集角色。GEOFlow 即使 PoC 成功，也不应直接写入当前 `app/` 或 `public/`。

未来可能关系：

- GEOFlow 作为独立后台，管理公开知识资产草稿。
- 当前网站仍通过人工审核后的导出副本同步。
- GEOFlow 产物必须先进入 manifest、哈希、来源版本和发布安全审核。

## 不得作为 GEOFlow 输入的数据

- `internal-review/downloads/*`。
- 投递版数据与分析工作簿原件。
- 品牌事实知识库完整工作簿原件。
- 90 天策略工作簿原件。
- `first_setup`、`final` 和早期 batch/archive 文件。
- `app/data.ts` 或 TSX 页面作为事实 canonical。

允许输入：

- 安全公开知识库 JSON。
- 人工审核后的公开摘录。
- 合成样例数据。
- 公开路由文本快照。

## 下一步

06B 不做 GEOFlow。等 06B/06C 形成稳定的安全输入包和输出契约后，再单独开一个 GEOFlow PoC 决策阶段。
