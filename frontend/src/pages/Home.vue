<template>
  <div class="page">
    <h1>Control Room</h1>

    <div class="time-card" v-if="system">
      <div class="time">{{ system.time_now }}</div>
      <div class="uncertainty">± {{ system.uncertainty_95_ns }} ns</div>
    </div>

    <div v-else class="loading">
      Loading time…
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { api } from "@/api"

const system = ref(null)

async function loadSystem() {
  try {
    system.value = await api("system/health")
  } catch (err) {
    console.error("System health load failed:", err)
  }
}

onMounted(() => {
  loadSystem()
  setInterval(loadSystem, 1000)
})
</script>

<style scoped>
.page {
  padding: 2rem;
  color: #fff;
  font-family: system-ui, sans-serif;
}

.time-card {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #222;
  border-radius: 8px;
  display: inline-block;
}

.time {
  font-size: 2rem;
  font-weight: bold;
}

.uncertainty {
  font-size: 1rem;
  opacity: 0.7;
}

.loading {
  margin-top: 2rem;
  opacity: 0.6;
}
</style>
