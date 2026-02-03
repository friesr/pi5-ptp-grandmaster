<template>
  <div class="page">
    <h1>Backend Time</h1>

    <div v-if="time" class="time-card">
      {{ time }}
    </div>

    <div v-else class="loading">
      Loading…
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { api } from "@/api"

const time = ref(null)

async function loadTime() {
  try {
    const res = await api("time")
    time.value = res.time
  } catch (err) {
    console.error("Time load failed:", err)
  }
}

onMounted(() => {
  loadTime()
  setInterval(loadTime, 1000)
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
  font-size: 2rem;
  font-weight: bold;
}

.loading {
  margin-top: 2rem;
  opacity: 0.6;
}
</style>
