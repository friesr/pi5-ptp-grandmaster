<template>
  <span class="event-badge" :class="eventClass" :title="tooltip">
    <span class="dot"></span>
    <span v-if="showLabel" class="label">{{ event.type }}</span>
  </span>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  event: { type: Object, required: true },
  showLabel: { type: Boolean, default: false }
})

// ------------------------------------------------------------
// Color coding by source
// ------------------------------------------------------------
const eventClass = computed(() => {
  const s = props.event.source
  if (s === "correlation") return "correlation"
  if (s === "risk") return "risk"
  if (s === "intel") return "intel"
  return "node"
})

// ------------------------------------------------------------
// Tooltip
// ------------------------------------------------------------
const tooltip = computed(() => {
  const e = props.event
  return `${e.source.toUpperCase()} — ${e.type}
Timestamp: ${new Date(e.timestamp * 1000).toLocaleString()}`
})
</script>

<style scoped>
.event-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  border-radius: 6px;
  font-size: 0.75rem;
  cursor: default;
  background: #2a2a2a;
}

.event-badge .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.event-badge.node .dot { background: #4caf50 }
.event-badge.intel .dot { background: #2196f3 }
.event-badge.correlation .dot { background: #ff9800 }
.event-badge.risk .dot { background: #f44336 }

.label {
  opacity: 0.9;
}
</style>
