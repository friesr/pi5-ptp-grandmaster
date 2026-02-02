<template>
  <DefaultLayout>
    <TimeCard
      :time="intel.time_now"
      :uncertainty="intel.uncertainty_95_ns"
      :reliability="intel.reliability_95"
    />

    <SatelliteSummary :satellites="map.satellites" />

    <SystemHealthMini :health="health" />
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'

import DefaultLayout from '../layouts/DefaultLayout.vue'
import TimeCard from '../components/TimeCard.vue'
import SatelliteSummary from '../components/SatelliteSummary.vue'
import SystemHealthMini from '../components/SystemHealthMini.vue'

const intel = ref({})
const map = ref({ satellites: [] })
const health = ref({})

async function load() {
  try {
    intel.value = await api("intel/snapshot")
    map.value = await api("map/nodes")
    health.value = await api("control_room/snapshot")
  } catch (err) {
    console.error("Error loading home page data:", err)
  }
}

onMounted(() => {
  load()
  setInterval(load, 1000)
})
</script>
