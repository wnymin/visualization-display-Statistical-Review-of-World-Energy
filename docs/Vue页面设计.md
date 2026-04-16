# Vue 页面设计方案（基于数据分析结果）

## 1. 设计目标
- 让用户快速看懂全球能源格局与变化趋势。
- 支持“总览 -> 对比 -> 细节”的逐层探索路径。
- 在桌面与移动端都保持可读、可筛选、可解释。

## 2. 信息架构
建议采用 5 个一级页面：

1. 首页（home）
- 项目简介、数据来源、更新时间
- 核心 KPI 卡片（2024 年）
- 入口导航（总览、能源结构、排放、转型）

2. 能源总览（overview）
- 指标：TES、电力总发电量、总碳排
- 图表：
  - 全球趋势折线图（1965-2024）
  - 区域贡献堆叠面积图
  - 2024 年世界与 OECD/Non-OECD 对比卡片

3. 化石能源（fossil）
- 指标：油/气/煤消费与生产
- 图表：
  - 油气煤消费趋势多折线
  - 2024 横向条形图（Top 国家或区域）
  - 贸易流向摘要卡片（后续可扩展 Sankey）

4. 低碳与电力（transition）
- 指标：风电、光伏、水电、核电、储能、CCUS
- 图表：
  - 风光发电趋势
  - 电力结构堆叠柱图
  - BESS 与 CCUS 专题卡片

5. 排放分析（emissions）
- 指标：CO2 from Energy、CO2e
- 图表：
  - 全球排放趋势
  - 区域分布对比
  - 能源与排放联动散点图（可选）

## 3. 页面与数据映射（首版）

### 3.1 总览页面
- Total Energy Supply (TES) -EJ
- Electricity Generation - TWh
- CO2 from Energy

### 3.2 化石能源页面
- Oil Consumption - EJ
- Gas Consumption - EJ
- Coal Consumption - EJ
- Oil/Gas/Coal 贸易相关表（首版可先做摘要卡）

### 3.3 低碳与电力页面
- Renewables Consumption -EJ
- Solar Generation - TWh
- Wind Generation - TWh
- Elec generation by fuel
- Grid Scale BESS Capacity
- CCUS Capture Capacity

### 3.4 排放页面
- CO2 from Energy
- CO2e Emissions
- CO2-Process Emissions, Methane
- CO2 from Flaring

## 4. 组件设计建议
- 全局筛选条组件（FilterBar）
  - 维度：地区层级、国家、年份、指标单位
- 指标卡组件（KPIStatCard）
  - 展示：当前值、同比、十年变化
- 图表容器组件（ChartPanel）
  - 统一标题、单位、来源、下载按钮
- 对比表组件（CompareTable）
  - 支持排序、搜索、导出
- 说明面板组件（DataNotePanel）
  - 口径说明、单位换算、来源说明

## 5. 交互设计要点
- 全局筛选应可跨图联动，减少重复操作。
- Hover 提示统一显示：年份、实体、值、单位。
- 图例支持开关与高亮，提升多序列可读性。
- 排名图提供“世界/区域/国家”三级切换。

## 6. 视觉与可读性要求
- 同一能源类型固定颜色映射。
- 页面统一保留数据来源和更新时间。
- 移动端优先保留关键趋势图与 KPI，复杂图表可折叠。

## 7. 工程落地建议（Vue）
建议在 `webapp-vue/src` 采用以下目录：
- `views`：页面级组件
- `components`：通用可复用组件
- `composables`：筛选、格式化、图表配置逻辑
- `services`：数据加载与字段映射
- `utils`：单位换算、年份处理、实体标准化

## 8. 首版迭代目标
1. 完成总览页面（TES/发电/排放三张主图）。
2. 完成能源结构页面（油气煤+可再生对比）。
3. 完成全局筛选条与图表联动。
4. 完成移动端适配与基础可用性优化。
