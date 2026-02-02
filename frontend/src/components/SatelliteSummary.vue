<template>
  <div class="card">
    <h2>Satellites</h2>
    <div class="metric">
      <span class="label">Tracked:</span>
      <span>{{ satellites.length }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  satellites: Array
})
</script>

<style scoped>
.metric {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.label {
  opacity: 0.7;
}
</style>
