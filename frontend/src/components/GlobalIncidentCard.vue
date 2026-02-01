<template>
  <div class="incident-card">
    <h3>{{ incident.title }}</h3>

    <p class="meta">
      <span>Severity: <strong>{{ incident.severity }}</strong></span>
      <span>Source: {{ incident.source }}</span>
      <span>Time: {{ incident.timestamp }}</span>
    </p>

    <p class="description">
      {{ incident.description }}
    </p>

    <div class="tags">
      <span
        class="tag"
        v-for="tag in incident.tags"
        :key="tag"
      >
        {{ tag }}
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  incident: Object
})
</script>

<style scoped>
.incident-card {
  background: #1a1a1a;
  padding: 1.2rem;
  border-radius: 8px;
  border: 1px solid #333;
  margin-bottom: 1rem;
}

h3 {
  margin: 0 0 0.6rem 0;
  font-size: 1.2rem;
}

.meta {
  font-size: 0.85rem;
  color: #aaa;
  display: flex;
  flex-direction: column;
  margin-bottom: 0.8rem;
}

.description {
  color: #ddd;
  margin-bottom: 0.8rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tag {
  background: #333;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #ccc;
}
</style>
