<template>
  <div class="page">
    <NavBar />

    <div class="card">
      <h2>Storyboards</h2>
      <p>This is a placeholder until the full storyboard engine is implemented.</p>
    </div>

    <div class="card">
      <h3>Latest Storyboard Snapshot</h3>

      <div v-if="!storyboard || Object.keys(storyboard).length === 0">
        No storyboard data available.
      </div>

      <div v-else>
        <div class="metric">
          <span class="label">Title:</span>
          <span>{{ storyboard.title }}</span>
        </div>

        <div class="metric">
          <span class="label">Timestamp:</span>
          <span>{{ storyboard.timestamp }}</span>
        </div>

        <div v-if="storyboard.events && storyboard.events.length > 0">
          <h4>Events</h4>
          <ul class="event-list">
            <li v-for="(event, idx) in storyboard.events" :key="idx">
              <strong>{{ event.type }}</strong>
              — {{ event.description }}
              — {{ event.time }}
            </li>
          </ul>
        </div>

        <div v-else>
          No events in this storyboard.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'

import NavBar from '../components/NavBar.vue'

const storyboard = ref({})

async function load() {
  try {
    storyboard.value = await api("storyboard/snapshot")
  } catch (err) {
    console.error("Error loading storyboard snapshot:", err)
  }
}

onMounted(() => {
  load()
  setInterval(load, 4000) // refresh every 4 seconds
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
