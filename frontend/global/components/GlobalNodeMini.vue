<template>
  <div class="node-mini" :title="tooltip">
    <div class="dot" :class="node.health.status">
      <div class="drift-ring" :style="{ borderColor: driftColor }"></div>
    </div>

    <span v-if="showLabel" class="label">
      {{ node.node_id }}
    </span>

    <span v-if="node.health.interference" class="interference-flag">!</span>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  node: { type: Object, required: true },
  showLabel: { type: Boolean, default: false }
})

// ------------------------------------------------------------
// Drift color
// ------------------------------------------------------------
const driftColor = computed(() => {
  const d = props.node.health.drift_ns
  if (Math.abs(d) > 80) return "#f44336"
  if (Math.abs(d) > 40) return "#ff9800"
  return "#4caf50"
})

// ------------------------------------------------------------
// Tooltip
// ------------------------------------------------------------
const tooltip = computed(() => {
  const n = props.node
  return `${n.node_id}
Status: ${n.health.status}
Drift: ${n.health.drift_ns} ns
Interference: ${n.health.interference ? "Yes" : "No"}
Constellations: ${n.health.constellations.join(", ") || "None"}`
})
</script>

<style scoped>
.node-mini {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: default;
  position: relative;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  position: relative;
}

.dot.ok { background: #4caf50 }
.dot.warn { background: #ff9800 }
.dot.fail { background: #f44336 }

.drift-ring {
  position: absolute;
  top: -3px;
  left: -3px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid;
  opacity: 0.7;
}

.label {
  font-size: 0.85rem;
  opacity: 0.85;
}

.interference-flag {
  color: #f44336;
  font-weight: bold;
  font-size: 0.9rem;
}
</style>
