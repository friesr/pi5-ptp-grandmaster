<template>
  <div class="snapshot-card">

    <!-- Header -->
    <div class="header">
      <h2>Snapshot</h2>
      <div class="timestamp">{{ formattedTimestamp }}</div>
    </div>

    <!-- Risk Gauge -->
    <div class="section">
      <GlobalRiskGauge
        :risk="snapshot.risk.global_risk"
        :forecast="snapshot.risk.forecast.forecast"
      />
    </div>

    <!-- Clusters -->
    <div class="section">
      <h3>Active Clusters</h3>
      <div v-if="snapshot.correlation.clusters.length === 0" class="empty">
        No active clusters
      </div>
      <GlobalClusterList
        v-else
        :clusters="snapshot.correlation.clusters"
      />
    </div>

    <!-- Node Health -->
    <div class="section">
      <h3>Node Health</h3>
      <div class="node-grid">
        <GlobalNodeHealth
          v-for="n in snapshot.nodes"
          :key="n.node_id"
          :node="n"
        />
      </div>
    </div>

    <!-- Constellation Activity -->
    <div class="section">
      <GlobalConstellationActivity
        :activity="snapshot.intel.constellation_activity"
      />
    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"

import GlobalRiskGauge from "./GlobalRiskGauge.vue"
import GlobalClusterList from "./GlobalClusterList.vue"
import GlobalNodeHealth from "./GlobalNodeHealth.vue"
import GlobalConstellationActivity from "./GlobalConstellationActivity.vue"

const props = defineProps({
  snapshot: { type: Object, required: true }
})

const formattedTimestamp = computed(() => {
  if (!props.snapshot.timestamp) return ""
  return new Date(props.snapshot.timestamp * 1000).toLocaleString()
})
</script>

<style scoped>
.snapshot-card {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timestamp {
  opacity: 0.8;
}

.section {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.node-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.empty {
  opacity: 0.7;
  font-size: 0.9rem;
}
</style>
