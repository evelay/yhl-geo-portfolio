# 阶段 06A GEO Skill 选型

## 优先使用的 8 个 Skill

| 优先级 | Skill | 推荐状态 | 主要层级 | 使用方式 |
| ---: | --- | --- | --- | --- |
| 1 | `yao-geo-page-audit` | adapt | 3, 5 | 06B 第一接入模块，只读审计公开路由并输出 docs 修复清单 |
| 2 | `yao-geo-tracking` | adopt | 6 | 采用直接/间接归因框架，改为只读公开站和文档输出 |
| 3 | `yao-geo-intent-miner` | adapt | 2, 4, 6 | 把 Redwood 30 题映射为意图簇、追问链路和监测 Prompt |
| 4 | `yao-geo-brand-graph` | adapt | 1, 4, 5 | 基于安全知识库 JSON 生成实体关系和消歧审计，不上线 JSON-LD |
| 5 | `yao-geo-knowledge-base-builder` | adapt | 1, 4 | 生成事实卡、FAQ、禁用表达和下游 prompt input pack 草案 |
| 6 | `yao-geo-page-blueprint` | adapt | 2, 4, 5 | Page Audit 后生成页面信息架构和实施验收蓝图 |
| 7 | `yao-geo-effect-monitor` | adapt | 3, 6 | 设计五平台监测口径、指标字典、月报模板，不采样 |
| 8 | `yao-geo-content-refiner` | defer | 4, 5 | 完整文章和 prompt 审核后，仅用于公开页面改造建议 |

## 重点 12 个 Skill 判断

| Skill | 推荐状态 | 结论 |
| --- | --- | --- |
| `yao-geo-brand-graph` | adapt | 适合层 1 的实体、别名、关系和消歧治理；需关闭自动来源核验和自动 JSON-LD 上线 |
| `yao-geo-knowledge-base-builder` | adapt | 适合把安全公开知识库变成事实卡、来源索引、FAQ 和禁用表达；不得读取完整 XLSX |
| `yao-geo-intent-miner` | adapt | 适合把 30 题问题库变成意图资产；不得伪造搜索量、平台回答或转化数据 |
| `yao-geo-panorama-audit` | defer | 覆盖面太大，和现有审计/发布安全报告重叠；适合季度复盘，不适合 06B 起点 |
| `yao-geo-page-audit` | adapt | 最适合 06B 起点；只读公开页面并输出页面修复清单 |
| `yao-geo-page-blueprint` | adapt | 适合把诊断结果变成页面方案；不允许自动写 `app/`、`public/` 或 Schema |
| `yao-geo-content-refiner` | defer | 适合公开内容改造，但当前完整文章样稿仍在 internal-review，先暂缓 |
| `yao-geo-effect-monitor` | adapt | 适合监测体系设计；当前只输出口径和字段，不运行采样 |
| `yao-geo-tracking` | adopt | 可直接采用其归因设计框架，但要把通用比例降级为本项目边界说明 |
| `yao-deepseek-crawler` | defer | 后续复测 PoC 可评估；当前不适合，因为依赖登录 Web UI、原始日志和重复采样 |
| `yao-doubao-crawler` | defer | 后续复测 PoC 可评估；当前不适合，移动/Appium 和截图/XML 风险更高 |
| `yao-chatgpt-crawler` | defer | 后续复测 PoC 可评估；当前不适合，会创建 ChatGPT 会话且引用来源可见性不稳定 |

## 其他 Skill 判断

| Skill | 推荐状态 | 原因 |
| --- | --- | --- |
| `yao-geo-title-optimizer` | defer | 标题候选应在内容审核后做；当前不生成标题资产 |
| `yao-geo-explainer-builder` | defer | 会生成完整文章，违反当前阶段约束 |
| `yao-geo-comparison-builder` | defer | 竞品事实和比较口径需要先治理 |
| `yao-geo-ranking-article-builder` | reject | 榜单评测与当前非官方作品集边界冲突，容易产生排名/推荐风险 |
| `yao-geo-article-friendly` | defer | 和 Content Refiner 重叠，等完整文章审核后再比较 |
| `yao-geo-execution-roadmap` | defer | 当前已有 90 天策略工作簿且处于 internal-review，避免重复规划 |
| `yao-geoflow-cli` | defer | 只有独立 GEOFlow 实例后才适用 |
| `yao-geoflow-design` | defer | 仅用于 GEOFlow 主题 PoC，不用于当前 Next.js 静态站 |
| `yao-geoflow-template` | reject | 面向旧 PHP 模板，不适配当前项目 |

## 原 GEO Content Optimizer 脚本处理

保留：

- `readability_checker.py`：保留为本地静态文本 lint 的参考，但要改造中文阈值、营销词表和评分解释。
- `schema_generator.py`：保留为 JSON-LD 形态参考，不直接用于当前站；后续必须重写为 source_id 绑定和页面正文校验版本。
- `geo_report_generator.py`：保留“趋势报告”这个交付概念，但当前实现不适配本项目指标，实际逻辑需要重写。

不保留或替换：

- `visibility_tester.py`：必须重写。
- `geo-content-optimizer` 工作流：用 `yao-geo-page-audit` 和 `yao-geo-content-refiner` 替代。
- `pillar-template.html`：只作为内容集群概念参考，当前暂缓。

## 重复功能

| 功能 | 重复工具 | 决策 |
| --- | --- | --- |
| URL 内容差距分析 | 原 `geo-content-optimizer`、`yao-geo-page-audit`、`yao-geo-content-refiner` | 用 Page Audit 先做公开页面诊断；Content Refiner 后续做公开内容改造 |
| Schema 生成/建议 | 原 `schema_generator.py`、`yao-geo-page-blueprint`、`yao-geo-brand-graph`、GEOFlow | 当前只允许 Schema 候选清单，不允许自动生成上线 |
| 意图和 Prompt 库 | `yao-geo-intent-miner`、`yao-geo-effect-monitor`、`yao-geo-panorama-audit` | Intent Miner 负责问题库；Effect Monitor 负责监测 Prompt；Panorama 暂缓 |
| 监测和可见度 | 原 `visibility_tester.py`、`yao-geo-effect-monitor`、三类 crawler | 旧脚本替换；Effect Monitor 先做口径；crawler 后续 PoC |
| 内容生产 | `content-refiner`、`article-friendly`、`explainer`、`comparison`、`ranking` | 当前不生成文章；仅保留 Content Refiner 为后续候选 |

## 必须重写的可见度脚本

必须重写 `visibility_tester.py`，原因：

- 只支持 Kimi 和 Perplexity，不覆盖当前基线中的豆包、文心一言、通义千问、Kimi、腾讯元宝。
- 以品牌字符串是否出现作为 cited 布尔值，不能表达人工四维评分、事实错误、来源覆盖和风险标签。
- 缺少 `question_id`、平台、账号状态、联网状态、测试日期、模型版本、Prompt 版本和采样环境。
- 默认写入 `visibility_history.json`，没有 run 目录、哈希、manifest 和人工审核门。
- `.env.example` 含明文 key 样式内容，密钥治理不合格。

`geo_report_generator.py` 也需要重写后才能用于本项目复测，因为当前仅按历史数组前后半段计算引用率趋势，不适配 225 条样本、人工评分和安全发布边界。

## Crawler 是否适合当前阶段

不适合。

三类 crawler 都应暂缓到独立复测 PoC：

- 它们依赖登录态、浏览器桥、移动模拟器或可见 UI 自动化。
- 它们会生成 raw answers、logs、截图、XML、会话痕迹和概率估计。
- 它们可能触发平台风控或服务条款风险。
- 当前项目还没有冻结复测问题、采样环境、人工评分和隐私发布规则。

## 不得读取 internal-review 的模块

当前阶段所有会形成外部输入、采样输入、公开报告或网站候选输出的模块都不得读取 `internal-review`，尤其是：

- 原 `visibility_tester.py` 和 `geo-content-optimizer`。
- `yao-geo-page-audit`、`yao-geo-page-blueprint`、`yao-geo-content-refiner`。
- `yao-geo-brand-graph`、`yao-geo-knowledge-base-builder`、`yao-geo-intent-miner`。
- `yao-geo-effect-monitor`、`yao-geo-tracking`。
- `yao-deepseek-crawler`、`yao-doubao-crawler`、`yao-chatgpt-crawler`。
- GEOFlow 及 `yao-geoflow-cli`、`yao-geoflow-design`。

例外：人工审核人员可以先从 `internal-review` 制作安全公开摘录；Skill 只能读取这个摘录，不能读取原目录。

## 推荐 06B 第一模块

推荐：`yao-geo-page-audit`。

06B 安全输入：

- 当前公开路由。
- `public/downloads/yhl-geo-knowledge-base-public.json`。
- `public/downloads/manifest.json`。
- 本阶段新增的治理和选型文档。

06B 输出：

- `docs/06b/page-audit/` 下的公开页面 GEO readiness 报告、页面修复清单、证据台账和 Schema 候选清单。

06B 禁止：

- 不改 `app/`。
- 不改 `public/`。
- 不生成上线 Schema。
- 不运行平台采样。
- 不读取 `internal-review`。
