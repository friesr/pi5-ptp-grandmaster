<template>
  <div class="card">
    <h2>Current Time</h2>
    <div class="time">{{ time }}</div>

    <div class="metric">
      <span class="label">Uncertainty (95%):</span>
      <span>{{ uncertainty }} ns</span>
    </div>

    <div class="metric">
      <span class="label">Reliability (95%):</span>
      <span>{{ reliability }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  time: String,
  uncertainty: Number,
  reliability: Number
})
</script>

<style scoped>
.time {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  margin-top: 0.3rem;
}

.label {
  opacity: 0.7;
}
</style>
