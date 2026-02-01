<template>
  <div class="incident-card" @click="inspect">

    <!-- Header -->
    <div class="header">
      <GlobalSeverityTag :severity="incident.severity" uppercase />
      <div class="timestamp">
        {{ formatTS(incident.start) }}
      </div>
    </div>

    <!-- Root Cause -->
    <div class="cause">
      {{ incident.root_cause }}
    </div>

    <!-- Mini Timeline -->
    <div class="timeline">
      <div
        v-for="(e, i) in incident.events"
        :key="i"
        class="marker"
        :class="eventClass(e)"
        :style="markerStyle(e.timestamp)"
        :title="eventTooltip(e)"
      ></div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div class="nodes">
        {{ incident.nodes.length }} nodes affected
      </div>
      <button class="inspect-btn">Inspect</button>
    </div>

  </div>
</template>

<script setup>
import GlobalSeverityTag from "./GlobalSeverityTag.vue"

const props = defineProps({
  incident: { type: Object, required: true }
})

const emit = defineEmits(["inspect"])

function inspect() {
  emit("inspect", props.incident)
}

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}

function eventClass(e) {
  if (e.source === "correlation") return "correlation"
  if (e.source === "risk") return "risk"
  if (e.source === "intel") return "intel"
  return "node"
}

function markerStyle(ts) {
  const pct = (ts - props.incident.start) /
              (props.incident.end - props.incident.start)
  return { left: pct * 100 + "%" }
}

function eventTooltip(e) {
  return `${e.source.toUpperCase()} — ${e.type}
${new Date(e.timestamp * 1000).toLocaleString()}`
}
</script>

<style scoped>
.incident-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
}

.incident-card:hover {
  background: #2a2a2a;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timestamp {
  opacity: 0.7;
  font-size: 0.85rem;
}

.cause {
  font-size: 1rem;
  font-weight: bold;
}

.timeline {
  position: relative;
  height: 20px;
  background: #333;
  border-radius: 4px;
}

.marker {
  position: absolute;
  top: 4px;
  width: 6px;
  height: 12px;
  border-radius: 3px;
}

.marker.node { background: #4caf50 }
.marker.intel { background: #2196f3 }
.marker.correlation { background: #ff9800 }
.marker.risk { background: #f44336 }

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nodes {
  opacity: 0.8;
}

.inspect-btn {
  background: #4caf50;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
}

.inspect-btn:hover {
  background: #43a047;
}
</style>
