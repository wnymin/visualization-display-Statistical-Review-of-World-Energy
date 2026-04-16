<script setup>
import VChart from 'vue-echarts'

defineProps({
  eyebrow: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  unit: {
    type: String,
    default: '',
  },
  option: {
    type: Object,
    required: true,
  },
  height: {
    type: Number,
    default: 340,
  },
  footnote: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <article class="chart-card">
    <div class="chart-card__head">
      <div>
        <p v-if="eyebrow" class="chart-card__eyebrow">{{ eyebrow }}</p>
        <h3 class="chart-card__title">{{ title }}</h3>
        <p v-if="description" class="chart-card__description">{{ description }}</p>
      </div>
      <span v-if="unit" class="chart-card__unit">{{ unit }}</span>
    </div>
    <div class="chart-card__body" :style="{ height: `${height}px` }">
      <VChart class="chart-card__chart" :option="option" autoresize />
    </div>
    <p v-if="footnote" class="chart-card__footnote">{{ footnote }}</p>
  </article>
</template>
