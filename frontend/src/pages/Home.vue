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
