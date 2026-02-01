<template>
  <div class="event-list">

    <!-- Filters -->
    <div v-if="showFilters" class="filters">
      <label v-for="s in sources" :key="s">
        <input type="checkbox" v-model="activeSources" :value="s" />
        {{ s }}
      </label>
    </div>

    <!-- Event Rows -->
    <ul class="events">
      <li
        v-for="(e, i) in filteredEvents"
        :key="i"
        class="event-row"
        :class="eventClass(e)"
        @click="select(e)"
      >
        <div class="timestamp">{{ formatTS(e.timestamp) }}</div>
        <div class="source">{{ e.source }}</div>
        <div class="type">{{ e.type }}</div>
      </li>
    </ul>

  </div>
</template>

<script setup>
import { ref, computed } from "vue"

const props = defineProps({
  events: { type: Array, default: () => [] },
  showFilters: { type: Boolean, default: true }
})

const emit = defineEmits(["select"])

const activeSources = ref(["node", "intel", "correlation", "risk"])

const sources = ["node", "intel", "correlation", "risk"]

function eventClass(e) {
  if (e.source === "correlation") return "correlation"
  if (e.source === "risk") return "risk"
  if (e.source === "intel") return "intel"
  return "node"
}

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}

const filteredEvents = computed(() =>
  props.events.filter(e => activeSources.value.includes(e.source))
)

function select(e) {
  emit("select", e)
}
</script>

<style scoped>
.event-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filters {
  display: flex;
  gap: 12px;
  font-size: 0.9rem;
}

.events {
  list-style: none;
  padding: 0;
  margin: 0;
}

.event-row {
  display: grid;
  grid-template-columns: 180px 100px 1fr;
  padding: 6px 8px;
  border-bottom: 1px solid #333;
  cursor: pointer;
}

.event-row:hover {
  background: #2a2a2a;
}

.event-row.node { color: #4caf50 }
.event-row.intel { color: #2196f3 }
.event-row.correlation { color: #ff9800 }
.event-row.risk { color: #f44336 }

.timestamp {
  opacity: 0.8;
}
</style>
