<template>
  <div class="timeline-wrapper">

    <!-- Zoom Controls -->
    <div class="zoom-controls">
      <button @click="zoomIn">+</button>
      <button @click="zoomOut">−</button>
    </div>

    <!-- Timeline -->
    <div class="timeline" ref="timelineEl" @click="onClickTimeline">

      <!-- Cluster Overlays -->
      <div
        v-for="(c, i) in clusters"
        :key="'cluster-' + i"
        class="cluster-overlay"
        :style="clusterStyle(c)"
      ></div>

      <!-- Event Markers -->
      <div
        v-for="(e, i) in events"
        :key="'event-' + i"
        class="event-marker"
        :class="eventClass(e)"
        :style="eventStyle(i)"
      ></div>

      <!-- Scrubber -->
      <div
        class="scrubber"
        :style="scrubberStyle"
        @mousedown="startDrag"
      ></div>

    </div>

    <!-- Timestamp -->
    <div class="timestamp">
      {{ formattedCursorTimestamp }}
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue"

const props = defineProps({
  events: { type: Array, default: () => [] },
  clusters: { type: Array, default: () => [] },
  cursor: { type: Number, default: 0 },
  zoom: { type: Number, default: 1 }
})

const emit = defineEmits(["update:cursor", "update:zoom"])

const timelineEl = ref(null)
const dragging = ref(false)
const localCursor = ref(props.cursor)
const localZoom = ref(props.zoom)

watch(() => props.cursor, v => (localCursor.value = v))
watch(() => props.zoom, v => (localZoom.value = v))

// ------------------------------------------------------------
// Computed
// ------------------------------------------------------------
const formattedCursorTimestamp = computed(() => {
  if (!props.events.length) return ""
  const ts = props.events[localCursor.value]?.timestamp
  return ts ? new Date(ts * 1000).toLocaleString() : ""
})

const scrubberStyle = computed(() => {
  if (!props.events.length) return {}
  const pct = (localCursor.value / props.events.length) * 100
  return { left: pct + "%" }
})

function eventClass(e) {
  if (e.source === "correlation") return "correlation"
  if (e.source === "risk") return "risk"
  if (e.source === "intel") return "intel"
  return "node"
}

function eventStyle(i) {
  const pct = (i / props.events.length) * 100
  return { left: pct + "%" }
}

function clusterStyle(c) {
  const startIdx = props.events.findIndex(e => e.timestamp >= c.start)
  const endIdx = props.events.findIndex(e => e.timestamp >= c.end)

  if (startIdx < 0 || endIdx < 0) return {}

  const startPct = (startIdx / props.events.length) * 100
  const endPct = (endIdx / props.events.length) * 100

  return {
    left: startPct + "%",
    width: endPct - startPct + "%"
  }
}

// ------------------------------------------------------------
// Interaction
// ------------------------------------------------------------
function onClickTimeline(e) {
  const rect = timelineEl.value.getBoundingClientRect()
  const pct = (e.clientX - rect.left) / rect.width
  const idx = Math.floor(pct * props.events.length)
  updateCursor(idx)
}

function startDrag() {
  dragging.value = true
  window.addEventListener("mousemove", onDrag)
  window.addEventListener("mouseup", stopDrag)
}

function onDrag(e) {
  if (!dragging.value) return
  const rect = timelineEl.value.getBoundingClientRect()
  const pct = (e.clientX - rect.left) / rect.width
  const idx = Math.floor(pct * props.events.length)
  updateCursor(idx)
}

function stopDrag() {
  dragging.value = false
  window.removeEventListener("mousemove", onDrag)
  window.removeEventListener("mouseup", stopDrag)
}

function updateCursor(idx) {
  const clamped = Math.max(0, Math.min(idx, props.events.length - 1))
  localCursor.value = clamped
  emit("update:cursor", clamped)
}

// ------------------------------------------------------------
// Zoom
// ------------------------------------------------------------
function zoomIn() {
  const z = Math.min(localZoom.value + 0.25, 4)
  localZoom.value = z
  emit("update:zoom", z)
}

function zoomOut() {
  const z = Math.max(localZoom.value - 0.25, 0.5)
  localZoom.value = z
  emit("update:zoom", z)
}
</script>

<style scoped>
.timeline-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.zoom-controls {
  display: flex;
  gap: 8px;
}

.timeline {
  position: relative;
  height: 40px;
  background: #2a2a2a;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
}

.event-marker {
  position: absolute;
  top: 0;
  width: 3px;
  height: 40px;
  opacity: 0.8;
}

.event-marker.node { background: #4caf50 }
.event-marker.intel { background: #2196f3 }
.event-marker.correlation { background: #ff9800 }
.event-marker.risk { background: #f44336 }

.cluster-overlay {
  position: absolute;
  top: 0;
  height: 40px;
  background: rgba(255, 152, 0, 0.2);
}

.scrubber {
  position: absolute;
  top: 0;
  width: 2px;
  height: 40px;
  background: #fff;
  cursor: ew-resize;
}

.timestamp {
  font-size: 0.9rem;
  opacity: 0.8;
}
</style>
