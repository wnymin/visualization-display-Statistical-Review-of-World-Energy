<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: String,
    required: true,
  },
  unit: {
    type: String,
    default: '',
  },
  note: {
    type: String,
    default: '',
  },
  tone: {
    type: String,
    default: 'blue',
  },
})
</script>

<template>
  <article class="kpi-card" :data-tone="tone">
    <p class="kpi-label">{{ label }}</p>
    <div class="kpi-value-row">
      <strong class="kpi-value">{{ value }}</strong>
      <span v-if="unit" class="kpi-unit">{{ unit }}</span>
    </div>
    <p v-if="note" class="kpi-note">{{ note }}</p>
  </article>
</template>
