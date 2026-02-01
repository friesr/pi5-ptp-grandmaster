<template>
  <div class="global-storyboards">

    <!-- Header -->
    <header class="gs-header">
      <h1>Global Storyboards</h1>
      <div class="subtitle">Narrative intelligence for global GNSS timing incidents</div>
    </header>

    <!-- Incident Summary -->
    <section class="incident-summary-card">
      <h2>Latest Incident</h2>

      <div v-if="incident">
        <div class="summary-row">
          <strong>Summary:</strong> {{ incident.summary }}
        </div>

        <div class="summary-row">
          <strong>Root Cause:</strong> {{ incident.root_cause }}
        </div>

        <div class="summary-row">
          <strong>Severity:</strong>
          <span :class="incident.severity">{{ incident.severity }}</span>
        </div>

        <div class="summary-row">
          <strong>Nodes Involved:</strong>
          <span v-if="incident.nodes_involved.length === 0">None</span>
          <ul v-else>
            <li v-for="n in incident.nodes_involved" :key="n">{{ n }}</li>
          </ul>
        </div>

        <div class="summary-row">
          <strong>Constellations:</strong>
          <span v-if="incident.constellations.length === 0">None</span>
          <ul v-else>
            <li v-for="c in incident.constellations" :key="c">{{ c }}</li>
          </ul>
        </div>

        <div class="summary-row">
          <strong>Duration:</strong> {{ incident.duration_sec }} sec
        </div>
      </div>

      <div v-else>
        No incidents detected.
      </div>
    </section>

    <!-- Major Storyboards -->
    <section class="major-storyboards-card">
      <h2>Major Event Storyboards</h2>

      <div v-if="storyboards.length === 0">
        No major events recorded.
      </div>

      <div
        v-for="sb in storyboards"
        :key="sb.start"
        class="storyboard-item"
        @click="selectStoryboard(sb)"
      >
        <div class="sb-header">
          <strong>{{ sb.root_cause }}</strong>
          <span class="severity" :class="sb.severity">{{ sb.severity }}</span>
        </div>

        <div class="sb-meta">
          <div>Start: {{ formatTS(sb.start) }}</div>
          <div>End: {{ formatTS(sb.end) }}</div>
          <div>Duration: {{ sb.duration_sec }} sec</div>
        </div>

        <div class="sb-nodes">
          <strong>Nodes:</strong>
          <span v-for="n in sb.nodes_involved" :key="n" class="node-tag">{{ n }}</span>
        </div>

        <div class="sb-constellations">
          <strong>Constellations:</strong>
          <span v-for="c in sb.constellations" :key="c" class="const-tag">{{ c }}</span>
        </div>
      </div>
    </section>

    <!-- Selected Storyboard -->
    <section v-if="selected" class="selected-storyboard-card">
      <h2>Storyboard Details</h2>

      <div class="sb-detail-row">
        <strong>Root Cause:</strong> {{ selected.root_cause }}
      </div>

      <div class="sb-detail-row">
        <strong>Severity:</strong>
        <span :class="selected.severity">{{ selected.severity }}</span>
      </div>

      <div class="sb-detail-row">
        <strong>Timeline Events:</strong>
        <ul>
          <li v-for="(e, i) in selected.timeline" :key="i">
            {{ formatTS(e.timestamp) }} — {{ e.source }}: {{ e.type }}
          </li>
        </ul>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { GlobalAPI } from "../api/global_api"

const storyboards = ref([])
const incident = ref(null)
const selected = ref(null)

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}

async function loadData() {
  storyboards.value = await GlobalAPI.storyboards.major()
  incident.value = await GlobalAPI.storyboards.incident()
}

function selectStoryboard(sb) {
  selected.value = sb
}

onMounted(() => {
  loadData()
  setInterval(loadData, 5000)
})
</script>

<style scoped>
.global-storyboards {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gs-header {
  display: flex;
  flex-direction: column;
}

.incident-summary-card,
.major-storyboards-card,
.selected-storyboard-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.summary-row,
.sb-detail-row {
  margin-bottom: 12px;
}

.storyboard-item {
  background: #2a2a2a;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
  cursor: pointer;
}

.storyboard-item:hover {
  background: #333;
}

.severity.major { color: #f44336 }
.severity.minor { color: #ff9800 }
.severity.info { color: #4caf50 }

.node-tag,
.const-tag {
  background: #444;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 6px;
}
</style>
