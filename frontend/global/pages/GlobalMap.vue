<template>
  <div class="global-map-page">

    <!-- Header -->
    <header class="gm-header">
      <h1>Global Map</h1>
      <div class="subtitle">Real-time global GNSS timing topology</div>
    </header>

    <!-- Map Container -->
    <section class="map-card">
      <GlobalMap
        :nodes="nodes"
        :overlays="overlays"
        :links="links"
      />
    </section>

    <!-- Side Panel -->
    <section class="side-panel">

      <div class="panel-card">
        <h2>Nodes</h2>
        <ul>
          <li v-for="n in nodes" :key="n.node_id">
            <strong>{{ n.node_id }}</strong>
            <span> — {{ n.health.status }}</span>
          </li>
        </ul>
      </div>

      <div class="panel-card">
        <h2>Constellation Activity</h2>
        <ul>
          <li v-for="(v, k) in intel.constellation_activity" :key="k">
            <strong>{{ k }}</strong>: {{ v }} events
          </li>
        </ul>
      </div>

      <div class="panel-card">
        <h2>Interference Zones</h2>
        <ul>
          <li v-for="z in overlays.interference" :key="z.id">
            {{ z.label }} — {{ z.intensity }}
          </li>
        </ul>
      </div>

    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { GlobalAPI } from "../api/global_api"
import GlobalMap from "../components/GlobalMap.vue"

const nodes = ref([])
const overlays = ref({ interference: [], constellations: [] })
const links = ref([])
const intel = ref({ constellation_activity: {} })

async function loadData() {
  nodes.value = await GlobalAPI.map.nodes()
  overlays.value = await GlobalAPI.map.overlays()

  // Federation links come from federation topology
  const topo = await GlobalAPI.federation.topology()
  links.value = topo.links || []

  intel.value = await GlobalAPI.intel.snapshot()
}

onMounted(() => {
  loadData()
  setInterval(loadData, 5000)
})
</script>

<style scoped>
.global-map-page {
  padding: 20px;
  display: flex;
  gap: 24px;
}

.map-card {
  flex: 3;
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.side-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}
</style>
