<template>
  <div class="page">
    <NavBar />

    <div class="card">
      <h2>Replay</h2>
      <p>This is a placeholder until the full replay engine is implemented.</p>
    </div>

    <div class="card">
      <h3>Recent Replay Snapshot</h3>

      <div v-if="!snapshot || Object.keys(snapshot).length === 0">
        No replay data available.
      </div>

      <div v-else>
        <div class="metric">
          <span class="label">Timestamp:</span>
          <span>{{ snapshot.timestamp }}</span>
        </div>

        <div v-if="snapshot.events && snapshot.events.length > 0">
          <h4>Events</h4>
          <ul class="event-list">
            <li v-for="(event, idx) in snapshot.events" :key="idx">
              <strong>{{ event.type }}</strong>
              — {{ event.description }}
              — {{ event.time }}
            </li>
          </ul>
        </div>

        <div v-else>
          No events in this snapshot.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'

import NavBar from '../components/NavBar.vue'

const snapshot = ref({})

async function load() {
  try {
    snapshot.value = await api("replay/snapshot")
  } catch (err) {
    console.error("Error loading replay snapshot:", err)
  }
}

onMounted(() => {
  load()
  setInterval(load, 3000) // refresh every 3 seconds
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

.event-list {
  list-style: none;
  padding-left: 0;
  margin-top: 0.5rem;
}

.event-list li {
  padding: 0.3rem 0;
  border-bottom: 1px solid #30363d;
}
</style>
