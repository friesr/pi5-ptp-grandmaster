<template>
  <div class="alert-list">

    <h3 v-if="title">{{ title }}</h3>

    <ul class="alerts">
      <li
        v-for="(a, i) in alerts"
        :key="i"
        class="alert-row"
        :class="severityClass(a.severity)"
        @click="select(a)"
      >
        <div class="header">
          <span class="type">{{ a.type }}</span>
          <span class="sev">{{ a.severity }}</span>
        </div>

        <div class="meta">
          <span>{{ formatTS(a.timestamp) }}</span>
          <span v-if="a.node_id">• Node: {{ a.node_id }}</span>
        </div>
      </li>

      <li v-if="alerts.length === 0" class="empty">
        No active alerts
      </li>
    </ul>

  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue"

const props = defineProps({
  alerts: { type: Array, default: () => [] },
  title: { type: String, default: "" }
})

const emit = defineEmits(["select"])

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}

function severityClass(s) {
  const v = s.toLowerCase()
  if (v === "critical" || v === "major") return "critical"
  if (v === "warning" || v === "minor") return "warning"
  return "normal"
}

function select(a) {
  emit("select", a)
}
</script>

<style scoped>
.alert-list {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.alerts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.alert-row {
  background: #2a2a2a;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
  cursor: pointer;
}

.alert-row:hover {
  background: #333;
}

.alert-row.normal { border-left: 4px solid #4caf50 }
.alert-row.warning { border-left: 4px solid #ff9800 }
.alert-row.critical { border-left: 4px solid #f44336 }

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.meta {
  font-size: 0.85rem;
  opacity: 0.8;
  display: flex;
  gap: 6px;
}

.empty {
  opacity: 0.7;
  font-size: 0.9rem;
  padding: 8px 0;
}
</style>
