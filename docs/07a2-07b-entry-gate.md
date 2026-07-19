# 阶段 07B 进入门禁

本门禁承接阶段 07A2 的人工裁决。07B 只能做 BreadcrumbList 隔离草稿试点，不得进入其他 Schema 类型或页面注入。

## 07B 允许

1. 为 `/facts` 创建 `BreadcrumbList` 隔离草稿。
2. 为 `/buying-guide` 创建 `BreadcrumbList` 隔离草稿。
3. 验证 breadcrumb 与真实页面导航一致。
4. 将输出写入 `tools/geo-skill/reports/schema-draft-pilot/`。
5. 不自动注入页面。

`/` 可作为 breadcrumb 根节点和试点范围确认对象，但 07B 第一实施动作只创建 `/facts` 与 `/buying-guide` 的隔离草稿。

## 07B 暂不允许

- `Organization`
- `Brand`
- `Person`
- `Article`
- `FAQPage`
- `Product`
- `Offer`
- `Review`
- `AggregateRating`
- 材料产品关系
- 京作身份关系
- 明式或清式年代关系

## 07B 进入条件

- 当前分支与远程 ahead/behind 为 `0/0`。
- 工作区干净。
- Breadcrumb 路由结构确认。
- 不读取 `internal-review/`。
- 不修改外部 canonical。
- 输出只进入隔离目录。
- 人工审核后才允许注入页面。

## 07B 停止条件

如发现任一条件不满足，07B 应立即停止并汇报，不得通过切换 `main`、合并分支、读取禁用目录、生成其他 Schema 或修改页面来绕过门禁。

## 本阶段结论

BreadcrumbList 是 07B 唯一第一目标。除 BreadcrumbList 隔离草稿外，所有其他 Schema 类型都必须等待后续人工审核、页面审核或 evidence 补采。
