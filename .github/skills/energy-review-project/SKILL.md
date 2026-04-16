---
name: energy-review-project
description: "用于本仓库的能源统计可视化开发协作。适用于：制定项目计划、拆解任务、处理 EI-Stats-Review-ALL-data.xlsx 数据、编写 Vue 页面与图表、排查构建和 GitHub Pages 部署问题。"
---

# 能源统计可视化项目技能

## 适用场景
- 需要为本项目制定或更新研发计划。
- 需要进行 Excel 数据清洗、字段映射与可视化建模。
- 需要在 Vue 项目中实现图表页面、交互筛选和信息展示。
- 需要解决构建失败、路径错误、GitHub Pages 发布异常等问题。

## 项目背景
- 项目目标：将《Statistical Review of World Energy》相关数据转换为可读、可比、可交互的网页展示。
- 当前基础：
  - 前端框架已基于 Vue + Vite 初始化。
  - GitHub Pages 自动部署流程已配置。
  - 数据源位于仓库根目录 `EI-Stats-Review-ALL-data.xlsx`。

## 技术与目录约定
- 前端工程目录：`webapp-vue`。
- 数据源原始文件：仓库根目录 `EI-Stats-Review-ALL-data.xlsx`。
- 静态发布数据目录：`webapp-vue/public/data`。
- GitHub Pages 工作流：`.github/workflows/deploy-pages.yml`。
- 若新增项目文档，统一放在 `docs` 目录。

## 开发流程规范
1. 先明确分析问题和页面目标，再动手写代码。
2. 涉及数据处理时，先建立字段字典与单位说明，再生成可视化输入数据。
3. 每完成一个页面模块，至少验证一次本地构建：`npm run build`。
4. 提交前检查是否影响 GitHub Pages 路径与静态资源引用。

## 数据处理规范
- 保留原始数据文件，禁止覆盖原文件。
- 统一约定：
  - 国家/地区字段名称一致。
  - 年份字段统一为数值类型。
  - 能源单位在页面中明确展示，并在必要时提供单位换算说明。
- 缺失值处理必须可追溯：
  - 允许为空时保持空值。
  - 需要补齐时在文档中说明补齐规则。
- 输出的数据结构应稳定，避免频繁变更字段名。

## 代码风格规范
- 使用 Vue 单文件组件，组件职责单一。
- 命名规范：
  - 组件名使用 PascalCase。
  - 变量与函数使用 camelCase。
  - 常量使用全大写加下划线。
- 目录结构建议按功能分层：`components`、`views`、`composables`、`utils`、`services`。
- 避免超大组件：单组件超过约 300 行应考虑拆分。
- 仅在复杂逻辑处添加简短注释，避免冗余注释。
- 保持代码可测试性：数据转换逻辑优先放入独立函数。

## 可视化实现规范
- 图表必须包含：标题、单位、时间范围、数据来源说明。
- 颜色方案保持一致，同类能源保持固定色映射。
- 支持基础交互：悬停提示、图例开关、筛选条件反馈。
- 移动端优先保证可读性，避免文字重叠与轴标签溢出。

## 数据分析执行规范
- 数据分析脚本统一放在 `data-analysis` 目录。
- 数据分析默认入口脚本：`data-analysis/analyze_workbook.py`。
- 分析输出统一放在 `data-analysis/output`，包含 `workbook_summary.json`、`sheet_summary.json`、`sheet_summary.csv`。
- 分析结论文档统一放在 `docs/数据分析报告.md`。
- Vue 页面信息架构与图表设计统一放在 `docs/Vue页面设计.md`。
- 代码或文档改动后，若影响数据口径或页面结构，必须同步更新上述文档。

## 构建与部署注意事项
- `vite.config.js` 的 `base` 必须与仓库名路径一致。
- 构建前需将 Excel 数据复制到 `webapp-vue/public/data`。
- GitHub Actions 中 `actions/configure-pages` 建议开启 `enablement: true`，防止首次部署时报 Pages 未启用错误。
- 部署失败时优先检查：
  - Pages 是否启用 GitHub Actions 作为来源。
  - 工作流权限是否包含 `pages: write` 与 `id-token: write`。
  - 构建产物路径是否仍为 `webapp-vue/dist`。

## 质量门禁
- 本地运行与构建均通过。
- 页面核心交互可用，移动端可正常访问。
- 关键图表数据与源数据抽样核对通过。
- README 或 docs 已同步更新必要说明。
- 数据分析脚本可重复运行，且输出结果文件完整。
