<template>
  <div class="global-control-room">

    <!-- Header -->
    <header class="gcr-header">
      <h1>Global Control Room</h1>
      <div class="timestamp">Last update: {{ formattedTimestamp }}</div>
    </header>

    <!-- Top Row: Global Risk + Alerts -->
    <section class="gcr-top-row">
      <div class="risk-card">
        <h2>Global Risk</h2>
        <div class="risk-value" :class="riskClass">{{ risk.global_risk }}</div>
        <div class="forecast">
          Forecast ({{ risk.forecast.window_hours }}h): 
          <strong>{{ risk.forecast.forecast }}</strong>
        </div>
      </div>

      <div class="alerts-card">
        <h2>Active Alerts</h2>
        <ul>
          <li v-for="a in alerts" :key="a.type" :class="a.severity">
            <strong>{{ a.type }}</strong>
            <span v-if="a.node_id"> — {{ a.node_id }}</span>
          </li>
        </ul>
      </div>
    </section>

    <!-- Middle Row: Global Map + Constellation Activity -->
    <section class="gcr-middle-row">
      <div class="map-card">
        <h2>Global Map</h2>
        <GlobalMap :nodes="nodes" :overlays="mapOverlays" />
      </div>

      <div class="constellation-card">
        <h2>Constellation Activity</h2>
        <ul>
          <li v-for="(v, k) in intel.constellation_activity" :key="k">
            <strong>{{ k }}</strong>: {{ v }} events
          </li>
        </ul>
      </div>
    </section>

    <!-- Bottom Row: Clusters + Node Health -->
    <section class="gcr-bottom-row">
      <div class="clusters-card">
        <h2>Active Clusters</h2>
        <ul>
          <li v-for="c in correlation.clusters" :key="c.start">
            <strong>{{ c.root_cause }}</strong>
            <span> ({{ c.severity }})</span>
            <div>{{ c.duration_sec }} sec</div>
          </li>
        </ul>
      </div>

      <div class="nodes-card">
        <h2>Node Health</h2>
        <ul>
          <li v-for="n in nodes" :key="n.node_id">
            <strong>{{ n.node_id }}</strong>
            <span> — {{ n.health.status }}</span>
          </li>
        </ul>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { GlobalAPI } from "../api/global_api"
import GlobalMap from "../components/GlobalMap.vue"

const snapshot = ref(null)
const nodes = ref([])
const intel = ref({})
const correlation = ref({})
const risk = ref({})
const alerts = ref([])
const mapOverlays = ref([])

const formattedTimestamp = computed(() => {
  if (!snapshot.value) return ""
  return new Date(snapshot.value.timestamp * 1000).toLocaleString()
})

const riskClass = computed(() => {
  if (!risk.value.global_risk) return ""
  const r = risk.value.global_risk
  if (r > 0.7) return "critical"
  if (r > 0.5) return "warning"
  return "normal"
})

async function loadData() {
  snapshot.value = await GlobalAPI.controlRoom.snapshot()
  alerts.value = await GlobalAPI.controlRoom.alerts()

  nodes.value = snapshot.value.nodes
  intel.value = snapshot.value.intel
  correlation.value = snapshot.value.correlation
  risk.value = snapshot.value.risk

  mapOverlays.value = await GlobalAPI.map.overlays()
}

onMounted(() => {
  loadData()
  setInterval(loadData, 5000)
})
</script>

<style scoped>
.global-control-room {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gcr-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.gcr-top-row,
.gcr-middle-row,
.gcr-bottom-row {
  display: flex;
  gap: 24px;
}

.risk-card,
.alerts-card,
.map-card,
.constellation-card,
.clusters-card,
.nodes-card {
  flex: 1;
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.risk-value {
  font-size: 2rem;
  margin: 8px 0;
}

.risk-value.normal { color: #4caf50 }
.risk-value.warning { color: #ff9800 }
.risk-value.critical { color: #f44336 }

.alerts-card ul li.warning { color: #ff9800 }
.alerts-card ul li.critical { color: #f44336 }
</style>
