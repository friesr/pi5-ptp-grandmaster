<template>
  <div class="panel">
    <h2>Constellation Panel</h2>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading constellation data</div>
    <div v-else class="constellation-list">
      <div
        class="constellation"
        v-for="sat in satellites"
        :key="sat.prn"
      >
        <h3>{{ sat.name }} (PRN {{ sat.prn }})</h3>
        <p>Status: <strong>{{ sat.status }}</strong></p>
        <p>Signal Strength: {{ sat.snr }}</p>
        <p>Elevation: {{ sat.elevation }}°</p>
        <p>Azimuth: {{ sat.azimuth }}°</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const loading = ref(true)
const error = ref(false)
const satellites = ref([])

onMounted(async () => {
  try {
    const res = await axios.get("/api/constellation")
    satellites.value = res.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.panel {
  background: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #333;
}

h2 {
  margin: 0 0 1rem 0;
  font-size: 1.4rem;
}

.constellation-list {
  display: grid;
  gap: 1rem;
}

.constellation {
  background: #111;
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid #222;
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}
</style>
