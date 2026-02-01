<template>
  <div class="map-panel">
    <h2>Constellation Sky Map</h2>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading sky map data</div>
    <div v-else class="sky-map">
      <div
        class="satellite"
        v-for="sat in satellites"
        :key="sat.prn"
        :style="{
          left: sat.azimuth + '%',
          bottom: sat.elevation + '%'
        }"
      >
        {{ sat.prn }}
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
    const res = await axios.get("/api/constellation/sky")
    satellites.value = res.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.map-panel {
  background: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #333;
}

h2 {
  margin: 0 0 1rem 0;
  font-size: 1.4rem;
}

.sky-map {
  position: relative;
  width: 100%;
  height: 400px;
  background: radial-gradient(circle at center, #222, #000);
  border-radius: 8px;
  overflow: hidden;
}

.satellite {
  position: absolute;
  width: 28px;
  height: 28px;
  background: #0af;
  color: #000;
  font-weight: bold;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #fff;
  transform: translate(-50%, -50%);
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}
</style>
