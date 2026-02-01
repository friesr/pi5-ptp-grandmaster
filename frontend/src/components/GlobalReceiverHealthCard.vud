<template>
  <div class="health-card">
    <h3>{{ receiver.name }}</h3>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading health</div>
    <div v-else class="metrics">
      <div class="metric">
        <span class="label">Status:</span>
        <span class="value">{{ health.status }}</span>
      </div>

      <div class="metric">
        <span class="label">Clock Bias:</span>
        <span class="value">{{ health.clock_bias }}</span>
      </div>

      <div class="metric">
        <span class="label">Jitter:</span>
        <span class="value">{{ health.jitter }}</span>
      </div>

      <div class="metric">
        <span class="label">Last Update:</span>
        <span class="value">{{ health.last_update }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const props = defineProps({
  receiver: Object
})

const loading = ref(true)
const error = ref(false)
const health = ref({})

onMounted(async () => {
  try {
    const res = await axios.get(`/api/receiver/${props.receiver.id}/health`)
    health.value = res.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.health-card {
  background: #1a1a1a;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #333;
  margin-bottom: 1rem;
}

h3 {
  margin: 0 0 0.8rem 0;
  font-size: 1.2rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 0;
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
