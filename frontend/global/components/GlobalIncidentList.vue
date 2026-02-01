<template>
  <div class="incident-list">

    <!-- Header -->
    <div class="header">
      <h2>Incidents</h2>

      <div class="controls">
        <select v-model="localSort">
          <option value="time">Sort by time</option>
          <option value="severity">Sort by severity</option>
        </select>

        <label class="group-toggle">
          <input type="checkbox" v-model="localGroup" />
          Group by severity
        </label>
      </div>
    </div>

    <!-- Grouped Mode -->
    <div v-if="localGroup" class="groups">
      <div
        v-for="sev in severityOrder"
        :key="sev"
        class="group"
      >
        <h3 class="group-title">{{ sev.toUpperCase() }}</h3>

        <div class="group-body">
          <GlobalIncidentCard
            v-for="inc in grouped[sev]"
            :key="inc.start"
            :incident="inc"
            @inspect="inspect"
          />
        </div>

        <div v-if="grouped[sev].length === 0" class="empty">
          No {{ sev }} incidents
        </div>
      </div>
    </div>

    <!-- Ungrouped Mode -->
    <div v-else class="flat">
      <GlobalIncidentCard
        v-for="inc in sorted"
        :key="inc.start"
        :incident="inc"
        @inspect="inspect"
      />

      <div v-if="sorted.length === 0" class="empty">
        No incidents found
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import GlobalIncidentCard from "./GlobalIncidentCard.vue"

const props = defineProps({
  incidents: { type: Array, default: () => [] },
  groupBySeverity: { type: Boolean, default: false },
  sort: { type: String, default: "time" }
})

const emit = defineEmits(["inspect"])

const localSort = ref(props.sort)
const localGroup = ref(props.groupBySeverity)

const severityOrder = ["critical", "warning", "normal"]

// ------------------------------------------------------------
// Sorting
// ------------------------------------------------------------
const sorted = computed(() => {
  const arr = [...props.incidents]

  if (localSort.value === "severity") {
    return arr.sort((a, b) =>
      severityOrder.indexOf(a.severity) - severityOrder.indexOf(b.severity)
    )
  }

  // Default: sort by time (descending)
  return arr.sort((a, b) => b.start - a.start)
})

// ------------------------------------------------------------
// Grouping
// ------------------------------------------------------------
const grouped = computed(() => {
  const groups = {
    critical: [],
    warning: [],
    normal: []
  }

  for (const inc of sorted.value) {
    const sev = inc.severity.toLowerCase()
    if (groups[sev]) groups[sev].push(inc)
  }

  return groups
})

function inspect(incident) {
  emit("inspect", incident)
}
</script>

<style scoped>
.incident-list {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.group-toggle {
  display: flex;
  gap: 6px;
  align-items: center;
  font-size: 0.9rem;
}

.groups {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.group-title {
  opacity: 0.8;
  margin-bottom: 8px;
}

.group-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.flat {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty {
  opacity: 0.7;
  padding: 8px 0;
}
</style>
