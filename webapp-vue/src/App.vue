<script setup>
import { computed, ref } from 'vue'
import dashboardData from './data/dashboardData.json'
import ChartCard from './components/ChartCard.vue'
import KpiCard from './components/KpiCard.vue'
import SectionBlock from './components/SectionBlock.vue'
import { createBarOption, createLineOption, formatNumber, getChangeSummary, getLatestValue } from './utils/chartOptions.js'

const activeSection = ref('overview')

const sectionNav = [
  { id: 'overview', label: '能源总览' },
  { id: 'fossil', label: '化石能源' },
  { id: 'transition', label: '低碳与电力' },
  { id: 'emissions', label: '排放分析' },
]

const highlightStats = [
  { label: '工作表总数', value: '100', unit: '张', note: '已完成全量结构盘点', tone: 'orange' },
  { label: '标准时间序列表', value: '77', unit: '张', note: '主要覆盖 1965-2024', tone: 'blue' },
  { label: '补充历史价格表', value: '3', unit: '张', note: '包含 1861 年以来原油价格', tone: 'green' },
  { label: '前端图表库', value: 'ECharts', unit: 'Vue', note: '用于趋势、排名与对比图', tone: 'violet' },
]

const kpis = computed(() => [
  buildKpi('TES', '一次能源供应', '1965-2024 全周期总量', 'blue'),
  buildKpi('Electricity', '电力总发电量', '反映全球用电规模变化', 'orange'),
  buildKpi('CO2', '能源碳排放', '全球能源系统排放压力', 'rose'),
  buildKpi('Oil', '石油消费', '化石能源需求核心指标', 'green'),
  buildKpi('Gas', '天然气消费', '气体能源结构变化', 'violet'),
  buildKpi('Renewables', '可再生能源消费', '风光水等低碳增长', 'cyan'),
])

const overviewCharts = computed(() => [
  {
    eyebrow: '总览趋势',
    title: '一次能源供应趋势',
    description: '世界总量与主要区域的长期变化。',
    unit: dashboardData.sections.overview.TES.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.overview.TES.series[0].years,
      series: dashboardData.sections.overview.TES.series,
      unit: dashboardData.sections.overview.TES.series[0].unit,
      area: true,
      colors: ['#2563eb', '#f97316', '#16a34a', '#7c3aed'],
    }),
    footnote: `数据来源：${dashboardData.meta.source}。` + getChangeSummary(dashboardData.kpis.TES, 10),
  },
  {
    eyebrow: '总览趋势',
    title: '电力总发电量趋势',
    description: '电力需求增长与区域结构变化。',
    unit: dashboardData.sections.overview.Electricity.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.overview.Electricity.series[0].years,
      series: dashboardData.sections.overview.Electricity.series,
      unit: dashboardData.sections.overview.Electricity.series[0].unit,
      colors: ['#0f766e', '#2563eb', '#f97316', '#7c3aed'],
    }),
    footnote: '适合观察工业化、城市化和电气化带来的长期变化。',
  },
  {
    eyebrow: '总览趋势',
    title: '全球能源碳排放趋势',
    description: '排放变化与能源结构调整的联动关系。',
    unit: dashboardData.sections.overview.CO2.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.overview.CO2.series[0].years,
      series: dashboardData.sections.overview.CO2.series,
      unit: dashboardData.sections.overview.CO2.series[0].unit,
      area: true,
      colors: ['#dc2626', '#ea580c', '#ca8a04', '#9333ea'],
    }),
    footnote: '排放图可用于识别高排放区域与结构性变化。',
  },
  {
    eyebrow: '总览排行',
    title: '2024 年一次能源供应 Top 区域',
    description: '聚焦最新一年世界、区域与主要经济体。',
    unit: dashboardData.sections.overview.TES.series[0].unit,
    option: createBarOption({
      items: dashboardData.sections.overview.TES.rank.items.slice(0, 8),
      unit: dashboardData.sections.overview.TES.series[0].unit,
      title: '一次能源供应',
    }),
    height: 360,
    footnote: `最新排名年份：${dashboardData.sections.overview.TES.rank.year}。`,
  },
])

const fossilCharts = computed(() => [
  {
    eyebrow: '化石能源',
    title: '石油消费趋势',
    description: '观察全球石油消费及主要区域需求。',
    unit: dashboardData.sections.fossil.Oil.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.fossil.Oil.series[0].years,
      series: dashboardData.sections.fossil.Oil.series,
      unit: dashboardData.sections.fossil.Oil.series[0].unit,
      colors: ['#1d4ed8', '#f97316', '#16a34a', '#7c3aed'],
    }),
    footnote: '油类消费是传统能源转型中的核心指标。',
  },
  {
    eyebrow: '化石能源',
    title: '天然气消费趋势',
    description: '用于对比天然气扩张和区域消费重心。',
    unit: dashboardData.sections.fossil.Gas.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.fossil.Gas.series[0].years,
      series: dashboardData.sections.fossil.Gas.series,
      unit: dashboardData.sections.fossil.Gas.series[0].unit,
      colors: ['#0f766e', '#2563eb', '#f59e0b', '#7c3aed'],
    }),
    footnote: '可用于分析气体能源在全球能源结构中的替代作用。',
  },
  {
    eyebrow: '化石能源',
    title: '煤炭消费趋势',
    description: '展示煤炭消费及其地区集中度。',
    unit: dashboardData.sections.fossil.Coal.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.fossil.Coal.series[0].years,
      series: dashboardData.sections.fossil.Coal.series,
      unit: dashboardData.sections.fossil.Coal.series[0].unit,
      colors: ['#334155', '#64748b', '#1d4ed8', '#f97316'],
    }),
    footnote: '煤炭是排放和能源安全分析中的敏感指标。',
  },
])

const transitionCharts = computed(() => [
  {
    eyebrow: '低碳与电力',
    title: '可再生能源消费趋势',
    description: '风、光、水和地热等低碳能源的长期变化。',
    unit: dashboardData.sections.transition.Renewables.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.transition.Renewables.series[0].years,
      series: dashboardData.sections.transition.Renewables.series,
      unit: dashboardData.sections.transition.Renewables.series[0].unit,
      area: true,
      colors: ['#059669', '#0f766e', '#2563eb', '#7c3aed'],
    }),
    footnote: '可再生能源是本项目最重要的增长叙事之一。',
  },
  {
    eyebrow: '低碳与电力',
    title: '风电与光伏发电趋势',
    description: '两类核心新能源发电的协同增长。',
    unit: dashboardData.sections.transition.Solar.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.transition.Solar.series[0].years,
      series: [dashboardData.sections.transition.Solar.series[0], dashboardData.sections.transition.Wind.series[0]],
      unit: dashboardData.sections.transition.Solar.series[0].unit,
      colors: ['#f59e0b', '#0ea5e9'],
    }),
    footnote: '风光是最适合做趋势联动对比的两类变量。',
  },
  {
    eyebrow: '低碳与电力',
    title: '储能与 CCUS 最新排名',
    description: '展示储能与碳捕集能力在地区上的集中度。',
    unit: dashboardData.sections.transition.BESS.series[0].unit,
    option: createBarOption({
      items: dashboardData.sections.transition.BESS.rank.items.slice(0, 8),
      unit: dashboardData.sections.transition.BESS.series[0].unit,
      title: '储能装机',
    }),
    height: 340,
    footnote: `CCUS 另一项核心指标可在数据结构中继续扩展。`,
  },
])

const emissionsCharts = computed(() => [
  {
    eyebrow: '排放分析',
    title: '能源碳排放趋势',
    description: '全球及主要区域的碳排放长期演变。',
    unit: dashboardData.sections.emissions.CO2.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.emissions.CO2.series[0].years,
      series: dashboardData.sections.emissions.CO2.series,
      unit: dashboardData.sections.emissions.CO2.series[0].unit,
      area: true,
      colors: ['#dc2626', '#b91c1c', '#ea580c', '#7c3aed'],
    }),
    footnote: '碳排放图是判断脱碳路径是否有效的核心面板。',
  },
  {
    eyebrow: '排放分析',
    title: 'CO2e 排放趋势',
    description: '将工业过程、甲烷和火炬排放纳入综合观察。',
    unit: dashboardData.sections.emissions.CO2e.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.emissions.CO2e.series[0].years,
      series: dashboardData.sections.emissions.CO2e.series,
      unit: dashboardData.sections.emissions.CO2e.series[0].unit,
      colors: ['#8b5cf6', '#2563eb', '#f97316', '#14b8a6'],
    }),
    footnote: '适合和能源碳排放一起构成排放矩阵。',
  },
  {
    eyebrow: '排放分析',
    title: '火炬排放趋势',
    description: '石油天然气开发过程中的排放压力参考。',
    unit: dashboardData.sections.emissions.Flaring.series[0].unit,
    option: createLineOption({
      years: dashboardData.sections.emissions.Flaring.series[0].years,
      series: dashboardData.sections.emissions.Flaring.series,
      unit: dashboardData.sections.emissions.Flaring.series[0].unit,
      colors: ['#f43f5e', '#fb7185', '#f97316', '#8b5cf6'],
    }),
    footnote: '可与油气生产板块联动展示。',
  },
])

function buildKpi(key, label, note, tone) {
  const series = dashboardData.kpis[key]
  const value = getLatestValue(series)

  return {
    label,
    value: value === null ? '暂无数据' : formatNumber(value, 1),
    unit: series.unit,
    note: `${note} · ${getChangeSummary(series, 10)}`,
    tone,
  }
}

function scrollToSection(id) {
  activeSection.value = id
  const target = document.getElementById(id)
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

<template>
  <div class="dashboard-page">
    <header class="hero-panel">
      <div class="hero-copy">
        <p class="eyebrow">Statistical Review of World Energy</p>
        <h1>世界能源统计可视化面板</h1>
        <p class="hero-text">
          基于 Energy Institute 的《Statistical Review of World Energy》数据构建，
          以 Vue + ECharts 展示全球能源供应、消费、排放与转型趋势。
        </p>
        <div class="hero-meta">
          <span>数据源：{{ dashboardData.meta.workbook }}</span>
          <span>来源机构：{{ dashboardData.meta.source }}</span>
          <span>分析口径：{{ dashboardData.meta.overview }}</span>
        </div>
        <div class="hero-actions">
          <button
            v-for="item in sectionNav"
            :key="item.id"
            class="nav-pill"
            :class="{ active: activeSection === item.id }"
            @click="scrollToSection(item.id)"
          >
            {{ item.label }}
          </button>
        </div>
      </div>
      <div class="hero-aside">
        <div class="hero-note">
          <span class="hero-note__tag">项目阶段</span>
          <strong>分析已完成，页面进入首版实现</strong>
          <p>当前已具备自动部署、数据分析和页面设计文档，可直接迭代视觉层。</p>
        </div>
        <div class="hero-figure">
          <div class="hero-figure__card">
            <span>时间覆盖</span>
            <strong>1965 - 2024</strong>
          </div>
          <div class="hero-figure__card hero-figure__card--accent">
            <span>可视化主题</span>
            <strong>总览 / 化石 / 转型 / 排放</strong>
          </div>
        </div>
      </div>
    </header>

    <section class="stats-strip">
      <KpiCard
        v-for="stat in highlightStats"
        :key="stat.label"
        :label="stat.label"
        :value="stat.value"
        :unit="stat.unit"
        :note="stat.note"
        :tone="stat.tone"
      />
    </section>

    <section class="kpi-grid">
      <KpiCard
        v-for="kpi in kpis"
        :key="kpi.label"
        :label="kpi.label"
        :value="kpi.value"
        :unit="kpi.unit"
        :note="kpi.note"
        :tone="kpi.tone"
      />
    </section>

    <SectionBlock
      id="overview"
      eyebrow="页面一 · 能源总览"
      title="总览页面"
      description="聚焦一次能源供应、电力发电和能源碳排放的全局趋势。"
      :tags="['趋势总览', '世界总量', '区域对比']"
    >
      <div class="chart-grid chart-grid--two">
        <ChartCard v-for="chart in overviewCharts" :key="chart.title" v-bind="chart" />
      </div>
    </SectionBlock>

    <SectionBlock
      id="fossil"
      eyebrow="页面二 · 化石能源"
      title="化石能源页面"
      description="展示油、气、煤消费结构及其长期变化。"
      :tags="['油', '气', '煤', '消费结构']"
    >
      <div class="chart-grid chart-grid--single">
        <ChartCard v-for="chart in fossilCharts" :key="chart.title" v-bind="chart" />
      </div>
    </SectionBlock>

    <SectionBlock
      id="transition"
      eyebrow="页面三 · 低碳与电力"
      title="低碳与电力页面"
      description="聚焦可再生能源、风光发电、储能和 CCUS 的增长。"
      :tags="['风电', '光伏', '储能', 'CCUS']"
    >
      <div class="chart-grid chart-grid--two">
        <ChartCard v-for="chart in transitionCharts" :key="chart.title" v-bind="chart" />
      </div>
    </SectionBlock>

    <SectionBlock
      id="emissions"
      eyebrow="页面四 · 排放分析"
      title="排放分析页面"
      description="分析能源碳排、综合温室气体和火炬排放的变化。"
      :tags="['CO2', 'CO2e', '火炬排放']"
    >
      <div class="chart-grid chart-grid--two">
        <ChartCard v-for="chart in emissionsCharts" :key="chart.title" v-bind="chart" />
      </div>
    </SectionBlock>
  </div>
</template>
