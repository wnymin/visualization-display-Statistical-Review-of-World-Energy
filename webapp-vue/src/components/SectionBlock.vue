<script setup>
defineProps({
  id: {
    type: String,
    required: true,
  },
  eyebrow: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  tags: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <section :id="id" class="section-block">
    <div class="section-head">
      <p class="section-eyebrow">{{ eyebrow }}</p>
      <h2 class="section-title">{{ title }}</h2>
      <p v-if="description" class="section-description">{{ description }}</p>
      <div v-if="tags.length" class="section-tags">
        <span v-for="tag in tags" :key="tag" class="section-tag">{{ tag }}</span>
      </div>
    </div>
    <div class="section-body">
      <slot />
    </div>
  </section>
</template>
