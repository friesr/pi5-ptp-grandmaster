<template>
  <div class="page">
    <NavBar />

    <div class="card">
      <h2>Constellation Map</h2>
      <p>This is a placeholder until the full skyplot is implemented.</p>
    </div>

    <div class="card">
      <h3>Satellites Tracked</h3>

      <div v-if="satellites.length === 0">
        No satellites currently tracked.
      </div>

      <ul v-else class="sat-list">
        <li v-for="sat in satellites" :key="sat.prn">
          <strong>{{ sat.prn }}</strong>
          — {{ sat.constellation }}
          — Elev: {{ sat.elevation }}°
          — Az: {{ sat.azimuth }}°
          — SNR: {{ sat.snr }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'

import NavBar from '../components/NavBar.vue'

const satellites = ref([])

async function load() {
  try {
    const map = await api("map/nodes")
    satellites.value = map.satellites || []
  } catch (err) {
    console.error("Error loading map data:", err)
  }
}

onMounted(() => {
  load()
  setInterval(load, 2000) // refresh every 2 seconds
})
</script>

<style scoped>
.sat-list {
  list-style: none;
  padding-left: 0;
}

.sat-list li {
  padding: 0.3rem 0;
  border-bottom: 1px solid #30363d;
}
</style>
