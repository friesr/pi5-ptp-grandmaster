<template>
  <div class="page">
    <NavBar />

    <div class="card">
      <h2>Control Room</h2>
      <p>This is a placeholder until the full control room dashboard is implemented.</p>
    </div>

    <div class="card">
      <h3>System Health</h3>

      <div v-if="!health || Object.keys(health).length === 0">
        No health data available.
      </div>

      <div v-else class="metric">
        <span class="label">Status:</span>
        <span>{{ health.status }}</span>
      </div>

      <div v-if="health.cpu_load" class="metric">
        <span class="label">CPU Load:</span>
        <span>{{ health.cpu_load }}</span>
      </div>

      <div v-if="health.temperature" class="metric">
        <span class="label">Temperature:</span>
        <span>{{ health.temperature }} °C</span>
      </div>

      <div v-if="health.disk_usage" class="metric">
        <span class="label">Disk Usage:</span>
        <span>{{ health.disk_usage }}</span>
      </div>
    </div>

    <div class="card">
      <h3>Receivers / Nodes</h3>

      <div v-if="nodes.length === 0">
        No nodes available.
      </div>

      <ul v-else class="node-list">
        <li v-for="node in nodes" :key="node.id">
          <strong>{{ node.name }}</strong>
          — {{ node.status }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'

import NavBar from '../components/NavBar.vue'

const health = ref({})
const nodes = ref([])

async function load() {
  try {
    health.value = await api("control_room/snapshot")
    const nodeData = await api("nodes/list")
    nodes.value = nodeData.nodes || []
  } catch (err) {
    console.error("Error loading control room data:", err)
  }
}

onMounted(() => {
  load()
  setInterval(load, 2000) // refresh every 2 seconds
})
</script>

<style scoped>
.metric {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.label {
  opacity: 0.7;
}

.node-list {
  list-style: none;
  padding-left: 0;
}

.node-list li {
  padding: 0.3rem 0;
  border-bottom: 1px solid #30363d;
}
</style>
