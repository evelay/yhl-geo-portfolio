# 阶段 06A GEO 工具评估前置检查

日期：2026-07-19

范围：只读验证当前仓库状态、现有治理边界和四个外部公开仓库快照。本阶段未修改 `app/`、`public/`、`AGENTS.md`，未安装依赖，未运行 API、爬虫或 GEOFlow。

## Git 状态

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| 当前分支 | pass | `refactor/portfolio-v2` |
| upstream | pass | `origin/refactor/portfolio-v2` |
| ahead / behind | pass | `0 / 0` |
| 远程分支包含提交 `80f861b` | pass | `origin/refactor/portfolio-v2` 指向 `80f861b6fb2f4e2a2d2799a66c9334b7234425c1` |
| 工作区干净 | pass | `git status --porcelain=v1` 无输出 |

## 已读取的本项目治理材料

| 文件 | 用途 |
| --- | --- |
| `docs/data-governance-decisions.md` | 确认 canonical、website-copy、delivery、derived、archive 的边界 |
| `docs/data-sync-policy.md` | 确认主源到网站副本的同步和冲突处理规则 |
| `docs/publication-readiness.md` | 确认当前公开页面、公开下载和 internal-review 状态 |
| `docs/p1-quality-remediation-report.md` | 确认 P1 后 GEO Skill 接入前置限制 |
| `docs/content-data-safety-audit.md` | 确认内容安全问题、发布风险和待人工决策项 |
| `docs/content-safety-remediation-plan.md` | 确认 P0/P1 修复状态和仍需 hold 的内容 |
| `docs/data-source-map.md` | 确认六类数据主从关系和 archive 禁用规则 |
| `docs/data-source-inventory.csv` | 抽查主源、网站副本、归档和外部报告角色 |

## 本阶段输入边界

当前项目采用外部 canonical 加网站展示副本的静态交付模式。06A 评估不把任何文件提交给外部 API，也不把任何外部仓库内容复制进当前项目。

禁止作为外部 API 或自动化采样输入：

- `internal-review/` 下的完整提示词、完整文章、完整工作簿、被阻塞 PDF/DOCX。
- `archive` 或 outdated 目录，包括 `first_setup`、`final`、batch1、old10 和早期复测模板。
- 外部 canonical 工作簿，包括投递版数据与分析工作簿、品牌事实知识库工作簿、90 天执行工作簿。
- `app/data.ts`、任意 TSX 页面、构建后 HTML、截图、预览、`.inspect.ndjson` 等派生物。

允许作为后续 Skill 接入输入的最低安全集合：

- 公开路由渲染内容。
- `public/downloads/yhl-geo-knowledge-base-public.json`。
- `public/downloads/manifest.json`。
- `docs/` 中已经提交的治理、发布安全和 P1 修复报告。
- 经人工审核另行导出的安全公开副本。

## 外部仓库快照

四个仓库均只读克隆到临时目录 `/private/tmp/geo-tooling-06a.Qma09M`，未复制到当前仓库。

| 仓库 | 快照 commit | 许可证观察 | 本阶段处理 |
| --- | --- | --- | --- |
| `https://github.com/liangdabiao/GEO-Content-Optimizer-Skill` | `b669ca8b2f62efb40e3778d491dcc37d1b4c5d5c` | README 标 MIT，但根目录未发现 `LICENSE` 文件；`.env.example` 含明文 key 样式内容 | 只读评估，不采纳密钥、不运行脚本 |
| `https://github.com/yaojingang/yao-geo-skills` | `dc10716d97c40fed0a0a08e538a236b5e16b4822` | MIT | 只读评估 21 个 Skill，重点评估 12 个 |
| `https://github.com/yaojingang/yao-meta-skill` | `e15472e1f5dc96f79ea0259bf9fdf67598cea356` | MIT | 只读评估 Skill 工程治理用途 |
| `https://github.com/yaojingang/GEOFlow` | `67abfd864a15d169a78429f3290c91cb3b93e849` | Apache-2.0，含 `NOTICE` | 只读评估平台能力，不部署 |

## 06A 执行约束确认

- 不复制完整外部仓库到当前项目。
- 不安装依赖。
- 不运行 API。
- 不运行爬虫。
- 不部署 GEOFlow。
- 不生成 Schema。
- 不生成文章。
- 不修改外部 canonical 文件。
- 不合并 main。
- 不创建 PR。
- 只允许新增 `docs/` 下评估文件。
