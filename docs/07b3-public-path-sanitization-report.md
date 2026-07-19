# 阶段 07B3 公开 Manifest 本地路径清理报告

日期：2026-07-19  
分支：`refactor/portfolio-v2`

## 1. 问题来源

阶段 07B2 报告记录全量 `out/` 扫描仍有两个既有 `/Users/` 命中，来源是 `public/downloads/manifest.json` 被静态构建复制到 `out/downloads/manifest.json`。

定位结果：

- 字段：`files[].source_file`
- 命中条目：`PLAN-PDF-PUBLIC-001`、`PLAN-DOCX-PUBLIC-001`
- 命中值：外部 14 页方案 PDF/DOCX 的本地绝对路径
- 用途：给审核者追溯下载件来源
- 公开用户是否必要：不必要；公开用户只需要逻辑来源、版本、公开状态、审核状态、文件哈希和公开 URL
- 维护方式：未发现生成 manifest 的脚本；`scripts/prepare-github-pages.mjs` 只处理 `robots.txt`、`sitemap.xml`、`.nojekyll` 和可选 `CNAME`，因此 manifest 当前按手工治理清单维护

受影响公开文件：

- `public/downloads/manifest.json`
- `out/downloads/manifest.json`

## 2. 暴露字段与风险

暴露字段为 `source_file`。两个 blocked/internal-review 下载件虽然没有公开 `public_url`，但公开 manifest 仍会被浏览器访问，因此本地用户名、工作区目录名和交付目录结构不应出现在该 JSON 中。

风险：

- 暴露本地用户名和机器目录结构
- 暴露项目工作目录命名
- 让内部交付路径被误认为公开来源
- 使构建产物扫描持续出现 false positive，降低后续安全扫描可信度

## 3. 修复方式

`public/downloads/manifest.json` 中移除所有 `source_file` 字段，新增逻辑来源字段：

- `source_id`
- `source_label`
- `source_scope`

保留并继续校验以下发布字段：

- `filename`
- `title`
- `category`
- `publication_status`
- `review_status`
- `last_verified`
- `disclaimer`
- `sha256`
- `public_url`
- `source_version`

公开来源标识示例：

- `KB-XLSX-001` / `品牌事实知识库工作簿` / `external-canonical`
- `STRATEGY-PDF-001` / `14页品牌内容优化方案 PDF 渲染件` / `external-delivery-artifact`
- `PROMPT-MD-CANONICAL-001` / `企业提示词体系 Markdown` / `restricted-logical-canonical`

## 4. 内部与公开规则

内部治理文档可以保留真实 canonical 绝对路径，用于人工审核和数据治理追溯。

浏览器可见文件只允许使用：

- 逻辑来源 ID
- 可读来源标签
- 来源范围标签
- 来源版本、日期或哈希
- 公开文件名、仓库相对路径和公开 URL

`public/downloads/manifest.json` 不得包含 `/Users/`、`file://`、`New project`、`yhl_geo_portfolio_delivery` 或 `internal-review/downloads` 真实路径。

## 5. 同步更新

已同步：

- `docs/download-manifest.md`
- `docs/data-governance-decisions.md`
- `docs/data-sync-policy.md`
- `docs/content-safety-issues.csv`
- `docs/publication-readiness.md`
- `docs/content-safety-remediation-plan.md`
- `docs/p1-quality-remediation-report.md`
- `tests/rendered-html.test.mjs`
- `scripts/scan-public-artifacts.mjs`
- `docs/07b3-public-path-scan.csv`

未修改 `app/data.ts`，因为页面下载链接只依赖公开文件名和 `downloadPath()`，没有消费 manifest 的来源字段。

## 6. 构建验证

验证结果：

- manifest JSON 解析：通过
- `vinext build`：通过
- rendered HTML 测试：12/12 通过
- Schema/BreadcrumbList 测试：2/2 通过
- GitHub Pages 等效构建：通过，14 个静态页面生成成功
- `scripts/prepare-github-pages.mjs`：通过
- 公开下载 JSON 哈希：`379fbec902654f6daabd5cf5eb5ff856cd418f78e09ba5c772f6e69b8895c991`
- public/out manifest 哈希一致：`dbfeca4ad231a0ad04a6a2d7d9a7e8d73a41a66e2952627121bea06f8a1d6932`

GitHub Pages 构建第一次在沙箱内被 Turbopack 本地进程限制阻止；按权限流程在外部执行并把 bundled Node 加入 PATH 后构建成功。未安装新依赖。

## 7. 路径扫描结果

扫描范围：

- `public/`
- `out/`

扫描规则至少覆盖：

- `/Users/`
- `file://`
- `New project`
- `yhl_geo_portfolio_delivery`
- `chatgpt.site`
- `internal-review/downloads`
- `website/internal-review`
- `localhost`

结果：

- `public/downloads/manifest.json`：不再含 `/Users/`、`file://` 或本地工作区路径
- `out/downloads/manifest.json`：不再含 `/Users/`、`file://` 或本地工作区路径
- 业务 JSON/HTML/TXT/XML/SVG/JS/CSS 公开产物：0 个违规
- `scripts/scan-public-artifacts.mjs` 检查 151 个公开文本产物，违规数 0
- 明细见 `docs/07b3-public-path-scan.csv`

## 8. Vendor Localhost 判断

`out/_next/static/chunks/03~yq9q893hmn.js` 仍包含一个 `localhost` 字符串。

判断：

- 来源：Next/Turbopack 生成的 `_next/static/chunks/*.js` vendor chunk
- 上下文：URL parser/polyfill 中的裸主机名判断
- 是否指向当前项目运行地址：否
- 是否被页面、manifest 或业务配置引用：否
- 是否属于构建工具/第三方通用常量：是

处理：

- 不修改 vendor chunk
- 不修改依赖
- 标记为 `accepted-third-party-literal`
- 新增精确 allowlist：仅 `out/_next/static/chunks/*.js` 可接受 vendor `localhost`
- 新增测试证明业务 JSON 中的 `localhost` 仍会被判为违规，不会被全局忽略

## 9. 未修改内容

本阶段未修改：

- 页面正文
- H1
- BreadcrumbList
- JSON-LD
- canonical
- sitemap 源配置
- robots 源文件
- 首页结构
- 核心指标
- 原始回答或人工评分
- 外部 canonical 文件
- `app/data.ts`
- `app/facts/page.tsx`
- `app/buying-guide/page.tsx`

未读取 `internal-review` 内容；仅确认目录存在，没有读取、移动或修改其中任何文件。

## 10. 回滚方式

提交后可执行：

```bash
git revert <07B3-commit>
```

如需手工回滚，应恢复：

- `public/downloads/manifest.json`
- `tests/rendered-html.test.mjs`
- `scripts/scan-public-artifacts.mjs`
- 本报告和扫描 CSV
- 本阶段更新过的治理/发布状态文档

回滚后必须重新运行 GitHub Pages 等效构建和公开路径扫描，确认构建状态与安全风险。
