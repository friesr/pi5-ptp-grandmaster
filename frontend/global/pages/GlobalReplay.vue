<template>
  <div class="global-replay">

    <!-- Header -->
    <header class="gr-header">
      <h1>Global Replay</h1>
      <div class="subtitle">Scrub through global GNSS timing history</div>
    </header>

    <!-- Timeline -->
    <section class="timeline-card">
      <h2>Timeline ({{ minutes }} min)</h2>

      <div class="timeline-container">
        <input
          type="range"
          min="0"
          :max="timeline.length - 1"
          v-model="cursor"
          class="timeline-slider"
        />

        <div class="timeline-events">
          <div
            v-for="(e, i) in timeline"
            :key="i"
            class="event-marker"
            :class="eventClass(e)"
            :style="{ left: (i / timeline.length) * 100 + '%' }"
          ></div>
        </div>
      </div>

      <div class="timestamp">
        {{ formattedCursorTimestamp }}
      </div>
    </section>

    <!-- State Reconstruction -->
    <section class="state-card">
      <h2>State at Timestamp</h2>

      <div v-if="state">
        <div class="state-row">
          <strong>Global Risk:</strong> {{ state.risk }}
        </div>

        <div class="state-row">
          <strong>Active Clusters:</strong>
          <span v-if="state.active_clusters.length === 0">None</span>
          <ul v-else>
            <li v-for="c in state.active_clusters" :key="c.start">
              {{ c.root_cause }} ({{ c.severity }})
            </li>
          </ul>
        </div>

        <div class="state-row">
          <strong>Node Health:</strong>
          <ul>
            <li v-for="(n, id) in state.nodes" :key="id">
              <strong>{{ id }}</strong> — {{ n.health.status }}
            </li>
          </ul>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue"
import { GlobalAPI } from "../api/global_api"

const minutes = 120
const timeline = ref([])
const cursor = ref(0)
const state = ref(null)

async function loadTimeline() {
  timeline.value = await GlobalAPI.replay.timeline(minutes)
}

async function loadState() {
  if (!timeline.value.length) return
  const ts = timeline.value[cursor.value].timestamp
  state.value = await GlobalAPI.replay.state(ts)
}

const formattedCursorTimestamp = computed(() => {
  if (!timeline.value.length) return ""
  const ts = timeline.value[cursor.value].timestamp
  return new Date(ts * 1000).toLocaleString()
})

function eventClass(e) {
  if (e.source === "correlation") return "correlation"
  if (e.source === "risk") return "risk"
  if (e.source === "intel") return "intel"
  return "node"
}

watch(cursor, loadState)

onMounted(async () => {
  await loadTimeline()
  await loadState()
  setInterval(loadTimeline, 5000)
})
</script>

<style scoped>
.global-replay {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gr-header {
  display: flex;
  flex-direction: column;
}

.timeline-card,
.state-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.timeline-container {
  position: relative;
  margin-top: 12px;
}

.timeline-slider {
  width: 100%;
}

.timeline-events {
  position: relative;
  height: 8px;
  margin-top: 8px;
}

.event-marker {
  position: absolute;
  top: 0;
  width: 4px;
  height: 8px;
  background: #888;
}

.event-marker.node { background: #4caf50 }
.event-marker.intel { background: #2196f3 }
.event-marker.correlation { background: #ff9800 }
.event-marker.risk { background: #f44336 }

.state-row {
  margin-bottom: 12px;
}
</style>
