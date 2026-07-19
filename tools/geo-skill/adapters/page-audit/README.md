# Page Audit Adapter

本适配层把 `yao-geo-page-audit` 的页面审计方法收敛为当前项目可重复运行的离线检查。

## 输入

- `out/index.html`
- `out/facts/index.html`
- `out/buying-guide/index.html`
- `out/robots.txt`
- `out/sitemap.xml`

输入范围由 `audit-config.json` 固定。本适配层不读取 `internal-review/`、`app/`、`public/`、外部 canonical 工作簿、raw AI answers 或人工评分。

## 输出

- `tools/geo-skill/reports/page-audit-pilot/report.md`
- `tools/geo-skill/reports/page-audit-pilot/report.json`
- `tools/geo-skill/reports/page-audit-pilot/run-metadata.json`
- `docs/06b-page-audit-findings.csv`

## 运行

```bash
python3 tools/geo-skill/adapters/page-audit/run_local_page_audit.py
```

当前环境没有系统 `npm` 时，GitHub Pages 构建使用 bundled Node 直接执行等效步骤：

```bash
next build
node scripts/prepare-github-pages.mjs
```

真实执行命令记录在 `run-metadata.json` 的 `build_method` 中。

## 测试

```bash
python3 -m unittest tools.geo-skill.adapters.page-audit.tests.test_run_local_page_audit
```

测试覆盖三页 HTML 读取、缺页报错、禁止读取 `internal-review`、禁止写入 `app/` 和 `public/`、核心标签识别、JSON 输出、重复运行结构稳定、无本地绝对路径、无总分和无 AI 排名/引用概率字段。
