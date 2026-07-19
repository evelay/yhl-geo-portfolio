# GEO 工具许可证与来源记录

## 外部仓库来源

| 仓库 | 快照 commit | 许可证观察 | 风险 |
| --- | --- | --- | --- |
| `liangdabiao/GEO-Content-Optimizer-Skill` | `b669ca8b2f62efb40e3778d491dcc37d1b4c5d5c` | README badge 和说明称 MIT，但根目录未发现实际 `LICENSE` 文件 | 许可证文件缺失；`.env.example` 含明文 key 样式内容；不复制代码 |
| `yaojingang/yao-geo-skills` | `dc10716d97c40fed0a0a08e538a236b5e16b4822` | MIT | 可参考和适配，但必须保留许可证与来源记录 |
| `yaojingang/yao-meta-skill` | `e15472e1f5dc96f79ea0259bf9fdf67598cea356` | MIT | 可用于后续内部 Skill 工程化，当前不复制代码 |
| `yaojingang/GEOFlow` | `67abfd864a15d169a78429f3290c91cb3b93e849` | Apache-2.0，含 `NOTICE` | 若未来 PoC，必须保留 Apache-2.0 和 NOTICE；当前不部署 |

## 本阶段拷贝边界

本阶段没有把外部仓库代码、脚本、示例输出、二进制文件、图片、依赖锁文件或完整 Skill 包复制进当前项目。

本阶段只在 `docs/` 中记录：

- 仓库定位。
- commit 快照。
- 许可证观察。
- 能力映射。
- 风险和接入建议。

## 只读检查覆盖面

| 仓库 | 已检查内容 | 活跃平台适配观察 |
| --- | --- | --- |
| `liangdabiao/GEO-Content-Optimizer-Skill` | README、Claude Skill 目录、Python 脚本、`.env.example`、requirements、示例输出路径和文件写入参数；未发现根目录 `LICENSE` | Claude Skill 形态；可见度脚本适配 Kimi/Moonshot 和 Perplexity；URL 优化工作流依赖 WebSearch/Playwright |
| `yaojingang/yao-geo-skills` | README、`LICENSE`、`registry/skills.json`、重点 12 个 `SKILL.md`、其他 Skill 概览、references、scripts、evals、示例报告契约、crawler 运行说明 | 面向 OpenAI/Codex/Claude 式 Skill 执行；crawler 适配 DeepSeek、Doubao、ChatGPT Web/UI 自动化；GEOFlow Skill 适配 GEOFlow 后台 |
| `yaojingang/yao-meta-skill` | README、`LICENSE`、`skill.json`、`SKILL.md`、agents、references、scripts、evals、tests、安装和发布说明、权限与网络政策 | 声明适配 OpenAI、Claude、generic、agent-skills-compatible 和 VS Code Skill 工程场景 |
| `yaojingang/GEOFlow` | README、`LICENSE`、`NOTICE`、Laravel/PHP/Node 配置、Docker、composer/npm 依赖、routes、services、models、database、API、后台和分发模块 | 适配 OpenAI-compatible、Gemini、embedding/RAG、WordPress REST、通用 HTTP、GEOFlow Agent、远端静态站和 `llms.txt`/JSON-LD 输出 |

## 可复用方式

| 来源 | 可复用方式 | 不可复用方式 |
| --- | --- | --- |
| 原 GEO Content Optimizer | 参考 Schema、可读性、趋势报告的概念 | 直接复制脚本、使用其 `.env.example`、直接运行 API 可见度测试 |
| `yao-geo-skills` | 参考 Skill 方法、输入输出契约、质量门；后续可单独 sparse checkout 某个 Skill 并保留许可证 | 复制整个仓库进当前网站；未经适配直接写网站或读取 internal-review |
| `yao-meta-skill` | 06C/07 用于生成内部 Skill 包和 eval | 06A 直接生成业务内容或修改网站 |
| GEOFlow | 未来独立 PoC 时按 Apache-2.0 使用 | 当前仓库内嵌、部署或让它读取当前 canonical |

## 依赖与网络观察

| 工具 | 依赖观察 |
| --- | --- |
| 原 `schema_generator.py`、`readability_checker.py`、`geo_report_generator.py` | 主要使用 Python 标准库，本地读写 |
| 原 `visibility_tester.py` | 需要 `requests` 或 `openai`，调用 Perplexity 或 Kimi/Moonshot API |
| 原 `geo-content-optimizer` | 依赖 WebSearch、Playwright 和写入 `output/<domain>/` |
| `yao-geo-skills` 多数报告 Skill | 主要是 Markdown/HTML/DOCX/PDF 报告渲染脚本；部分需要网页检索或来源核验 |
| 三类 crawler | 依赖 OpenCLI Browser Bridge、登录 Web 会话；Doubao 还可依赖 Android/Appium |
| `yao-meta-skill` | 有网络政策文件，允许部分 GitHub/version 检查；有 file_write/subprocess/interactive 权限治理 |
| GEOFlow | 需要 PHP、Composer、Node、PostgreSQL/pgvector、Redis、Docker；运行后可调用模型 API、embedding、WordPress 和 HTTP 分发 |

## 当前项目 provenance 规则

1. 任何后续实际引入的外部文件必须记录来源仓库、commit、路径、许可证和修改说明。
2. 不能复制含密钥、账号、本地绝对路径、private profile、raw answers、logs、screenshots 的示例。
3. 如果后续 sparse checkout 某个 `yao-geo-skills` Skill，应只引入必要目录，并保留 MIT 许可证说明。
4. 如果后续建立 GEOFlow PoC，应在独立仓库或独立目录保留 Apache-2.0 `LICENSE` 和 `NOTICE`。
5. 当前网站仓库不接收完整外部仓库。

## 禁止项

- 不把外部 `.env.example` 中的任何 key 样式内容带入当前项目。
- 不把外部 examples 中的 raw crawl evidence、logs、截图、XML 作为公开素材。
- 不把外部报告中的第三方品牌事实当作元亨利事实来源。
- 不用外部仓库示例结果反向覆盖本项目 canonical。
