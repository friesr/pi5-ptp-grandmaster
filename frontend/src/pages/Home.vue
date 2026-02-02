<template>
  <div class="page">

    <!-- Top Navigation -->
    <NavBar />

    <!-- Time + Uncertainty -->
    <GlobalSystemSummaryCard
      :timeNow="data.time_now"
      :uncertainty95="data.uncertainty_95_ns"
      :reliability95="data.reliability_95"
      :timeError="data.time_error_ns"
      :clockStability="data.clock_stability"
    />

    <!-- Satellite Summary -->
    <GlobalConstellationSummaryCard
      :satellites="data.satellites"
      :snrAvg="data.snr_avg"
      :dops="data.dops"
    />

    <!-- Skyplot -->
    <GlobalConstellationMap :satellites="data.satellites" />

    <!-- System Health -->
    <GlobalSystemHealth :health="data.health" />

    <!-- Quick Links -->
    <GlobalSystemGrid />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import NavBar from '../components/NavBar.vue'
import GlobalSystemSummaryCard from '../components/GlobalSystemSummaryCard.vue'
import GlobalConstellationSummaryCard from '../components/GlobalConstellationSummaryCard.vue'
import GlobalConstellationMap from '../components/GlobalConstellationMap.vue'
import GlobalSystemHealth from '../components/GlobalSystemHealth.vue'
import GlobalSystemGrid from '../components/GlobalSystemGrid.vue'

const data = ref({
  time_now: null,
  uncertainty_95_ns: null,
  reliability_95: null,
  time_error_ns: null,
  clock_stability: null,
  satellites: [],
  snr_avg: null,
  dops: {},
  health: {}
})

async function loadData() {
  try {
    const intel = await fetch('/api/global/intel/snapshot').then(r => r.json())
    const map = await fetch('/api/global/map/nodes').then(r => r.json())
    const health = await fetch('/api/global/control_room/snapshot').then(r => r.json())

    data.value = {
      ...intel,
      satellites: map.satellites || [],
      health: health || {}
    }
  } catch (err) {
    console.error('Error loading home page data', err)
  }
}

onMounted(() => {
  loadData()
  setInterval(loadData, 1000) // update time every second
})
</script>

<style scoped>
.page {
  padding: 2rem;
}
</style>
