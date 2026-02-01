<template>
  <div class="replay-timeline" @click="onClick">

    <!-- Cluster spans -->
    <div class="cluster-layer">
      <div
        v-for="(c, i) in clusters"
        :key="i"
        class="cluster-span"
        :class="severityClass(c.severity)"
        :style="spanStyle(c.start, c.end)"
        :title="clusterTooltip(c)"
      ></div>
    </div>

    <!-- Interference overlays -->
    <div class="interference-layer">
      <div
        v-for="(z, i) in interference"
        :key="i"
        class="interference-span"
        :style="spanStyle(z.start, z.end)"
        :title="interferenceTooltip(z)"
      ></div>
    </div>

    <!-- Event markers -->
    <div class="event-layer">
      <div
        v-for="(e, i) in events"
        :key="i"
        class="event-marker"
        :class="eventClass(e)"
        :style="markerStyle(e.timestamp)"
        :title="eventTooltip(e)"
      ></div>
    </div>

    <!-- Scrub cursor -->
    <div
      class="cursor"
      :style="cursorStyle"
      @mousedown="startDrag"
    ></div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const props = defineProps({
  startTime: { type: Number, required: true },
  endTime: { type: Number, required: true },
  currentTime: { type: Number, required: true },
  events: { type: Array, default: () => [] },
  clusters: { type: Array, default: () => [] },
  interference: { type: Array, default: () => [] }
})

const emit = defineEmits(["seek"])

const dragging = ref(false)

// ------------------------------------------------------------
// Position helpers
// ------------------------------------------------------------
function pct(ts) {
  return ((ts - props.startTime) / (props.endTime - props.startTime)) * 100
}

function spanStyle(start, end) {
  return {
    left: pct(start) + "%",
    width: (pct(end) - pct(start)) + "%"
  }
}

function markerStyle(ts) {
  return { left: pct(ts) + "%" }
}

const cursorStyle = computed(() => ({
  left: pct(props.currentTime) + "%"
}))

// ------------------------------------------------------------
// Classes & tooltips
// ------------------------------------------------------------
function eventClass(e) {
  if (e.source === "correlation") return "correlation"
  if (e.source === "risk") return "risk"
  if (e.source === "intel") return "intel"
  return "node"
}

function severityClass(s) {
  const v = s.toLowerCase()
  if (v === "critical" || v === "major") return "critical"
  if (v === "warning" || v === "minor") return "warning"
  return "normal"
}

function eventTooltip(e) {
  return `${e.source.toUpperCase()} — ${e.type}
${new Date(e.timestamp * 1000).toLocaleString()}`
}

function clusterTooltip(c) {
  return `${c.root_cause} (${c.severity})
${new Date(c.start * 1000).toLocaleString()} → ${new Date(c.end * 1000).toLocaleString()}`
}

function interferenceTooltip(z) {
  return `Interference: ${z.intensity}
${new Date(z.start * 1000).toLocaleString()} → ${new Date(z.end * 1000).toLocaleString()}`
}

// ------------------------------------------------------------
// Interaction
// ------------------------------------------------------------
function onClick(e) {
  const rect = e.currentTarget.getBoundingClientRect()
  const x = e.clientX - rect.left
  const pct = x / rect.width
  const ts = props.startTime + pct * (props.endTime - props.startTime)
  emit("seek", ts)
}

function startDrag() {
  dragging.value = true
  window.addEventListener("mousemove", onDrag)
  window.addEventListener("mouseup", stopDrag)
}

function onDrag(e) {
  if (!dragging.value) return
  const rect = document.querySelector(".replay-timeline").getBoundingClientRect()
  const x = e.clientX - rect.left
  const pct = Math.min(1, Math.max(0, x / rect.width))
  const ts = props.startTime + pct * (props.endTime - props.startTime)
  emit("seek", ts)
}

function stopDrag() {
  dragging.value = false
  window.removeEventListener("mousemove", onDrag)
  window.removeEventListener("mouseup", stopDrag)
}
</script>

<style scoped>
.replay-timeline {
  position: relative;
  height: 60px;
  background: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}

/* Layers */
.cluster-layer,
.interference-layer,
.event-layer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* Cluster spans */
.cluster-span {
  position: absolute;
  top: 0;
  height: 20px;
  opacity: 0.6;
}

.cluster-span.normal { background: #4caf50 }
.cluster-span.warning { background: #ff9800 }
.cluster-span.critical { background: #f44336 }

/* Interference spans */
.interference-span {
  position: absolute;
  top: 20px;
  height: 20px;
  background: #9c27b0;
  opacity: 0.4;
}

/* Event markers */
.event-marker {
  position: absolute;
  top: 42px;
  width: 6px;
  height: 12px;
  border-radius: 3px;
}

.event-marker.node { background: #4caf50 }
.event-marker.intel { background: #2196f3 }
.event-marker.correlation { background: #ff9800 }
.event-marker.risk { background: #f44336 }

/* Cursor */
.cursor {
  position: absolute;
  top: 0;
  width: 2px;
  height: 100%;
  background: #fff;
  cursor: ew-resize;
}
</style>
