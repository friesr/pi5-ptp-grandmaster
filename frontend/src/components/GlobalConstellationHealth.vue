<template>
  <div class="health-panel">
    <h2>Constellation Health</h2>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading constellation health</div>
    <div v-else class="metrics">
      <div
        class="metric"
        v-for="(value, key) in health"
        :key="key"
      >
        <span class="label">{{ key }}</span>
        <span class="value">{{ value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const loading = ref(true)
const error = ref(false)
const health = ref({})

onMounted(async () => {
  try {
    const res = await axios.get("/api/constellation/health")
    health.value = res.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.health-panel {
  background: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #333;
}

h2 {
  margin: 0 0 1rem 0;
  font-size: 1.4rem;
}

.metrics {
  display: grid;
  gap: 0.8rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  padding: 0.4rem 0;
  border-bottom: 1px solid #222;
}

.label {
  color: #aaa;
}

.value {
  color: #fff;
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}
</style>
