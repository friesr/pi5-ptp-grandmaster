<template>
  <div class="card">
    <h2>System Health</h2>

    <div class="metric">
      <span class="label">Status:</span>
      <span>{{ health.status || "unknown" }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  health: Object
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
