<template>
  <div class="node-health">

    <!-- Header -->
    <div class="header">
      <strong>{{ node.node_id }}</strong>
      <span class="status" :class="node.health.status">
        {{ node.health.status }}
      </span>
    </div>

    <!-- Drift Bar -->
    <div class="drift-bar">
      <div
        class="drift-fill"
        :style="{ width: driftPct + '%', background: driftColor }"
      ></div>
    </div>

    <!-- Details -->
    <div class="details">

      <div class="detail-row">
        <span class="label">Drift:</span>
        <span>{{ node.health.drift_ns }} ns</span>
      </div>

      <div class="detail-row">
        <span class="label">Constellation Lock:</span>
        <span class="locks">
          <span
            v-for="c in node.health.constellations"
            :key="c"
            class="lock"
          >
            {{ c }}
          </span>
        </span>
      </div>

      <div class="detail-row">
        <span class="label">Interference:</span>
        <span :class="interferenceClass">
          {{ node.health.interference ? "Yes" : "No" }}
        </span>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  node: { type: Object, required: true }
})

// ------------------------------------------------------------
// Drift visualization
// ------------------------------------------------------------
const driftPct = computed(() => {
  const d = props.node.health.drift_ns
  return Math.min(100, Math.abs(d) / 100) // scale 0–100 ns to 0–100%
})

const driftColor = computed(() => {
  const d = props.node.health.drift_ns
  if (Math.abs(d) > 80) return "#f44336"
  if (Math.abs(d) > 40) return "#ff9800"
  return "#4caf50"
})

// ------------------------------------------------------------
// Interference
// ------------------------------------------------------------
const interferenceClass = computed(() =>
  props.node.health.interference ? "interference-yes" : "interference-no"
)
</script>

<style scoped>
.node-health {
  background: #1e1e1e;
  padding: 12px;
  border-radius: 8px;
  width: 220px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header {
  display: flex;
  justify-content: space-between;
}

.status.ok { color: #4caf50 }
.status.warn { color: #ff9800 }
.status.fail { color: #f44336 }

.drift-bar {
  width: 100%;
  height: 6px;
  background: #333;
  border-radius: 4px;
  overflow: hidden;
}

.drift-fill {
  height: 100%;
  transition: width 0.3s ease, background 0.3s ease;
}

.details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.locks .lock {
  background: #444;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 4px;
}

.interference-yes { color: #f44336 }
.interference-no { color: #4caf50 }
</style>
