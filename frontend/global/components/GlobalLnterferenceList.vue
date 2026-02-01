<template>
  <div class="interference-list">

    <h3>Interference Zones</h3>

    <ul class="zones">
      <li
        v-for="z in zones"
        :key="z.id"
        class="zone-row"
        :class="intensityClass(z.intensity)"
        @click="select(z)"
      >
        <div class="header">
          <strong>{{ z.label }}</strong>
          <span class="intensity">{{ z.intensity }}</span>
        </div>

        <div class="meta">
          <span>{{ z.lat.toFixed(2) }}, {{ z.lon.toFixed(2) }}</span>
          <span>•</span>
          <span>{{ (z.radius_m / 1000).toFixed(1) }} km radius</span>
        </div>
      </li>
    </ul>

  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue"

const props = defineProps({
  zones: { type: Array, default: () => [] }
})

const emit = defineEmits(["select"])

function intensityClass(i) {
  if (i > 80) return "critical"
  if (i > 40) return "warning"
  return "normal"
}

function select(z) {
  emit("select", z)
}
</script>

<style scoped>
.interference-list {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.zones {
  list-style: none;
  padding: 0;
  margin: 0;
}

.zone-row {
  background: #2a2a2a;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
  cursor: pointer;
}

.zone-row:hover {
  background: #333;
}

.zone-row.normal { border-left: 4px solid #4caf50 }
.zone-row.warning { border-left: 4px solid #ff9800 }
.zone-row.critical { border-left: 4px solid #f44336 }

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.intensity {
  opacity: 0.8;
}

.meta {
  font-size: 0.85rem;
  opacity: 0.8;
  display: flex;
  gap: 6px;
}
</style>
