<template>
  <div class="receiver-list">

    <!-- Header -->
    <div class="header">
      <h2>Receivers</h2>

      <div class="controls">

        <!-- Sort -->
        <select v-model="localSort" class="sort">
          <option value="name">Sort by name</option>
          <option value="health">Sort by health</option>
        </select>

        <!-- Filter -->
        <select v-model="localFilter" class="filter">
          <option value="all">All</option>
          <option value="good">Good</option>
          <option value="degraded">Degraded</option>
          <option value="bad">Bad</option>
        </select>

        <!-- Grouping -->
        <label class="group-toggle">
          <input type="checkbox" v-model="localGroup" />
          Group by health
        </label>

      </div>
    </div>

    <!-- Grouped Mode -->
    <div v-if="localGroup" class="groups">

      <div
        v-for="state in healthOrder"
        :key="state"
        class="group"
      >
        <h3 class="group-title">{{ state.toUpperCase() }}</h3>

        <div class="group-body">
          <GlobalReceiverHealthCard
            v-for="r in grouped[state]"
            :key="r.name"
            :receiver="r"
            @inspect="inspect"
          />
        </div>

        <div v-if="grouped[state].length === 0" class="empty">
          No {{ state }} receivers
        </div>
      </div>

    </div>

    <!-- Flat Mode -->
    <div v-else class="flat">
      <GlobalReceiverHealthCard
        v-for="r in filteredSorted"
        :key="r.name"
        :receiver="r"
        @inspect="inspect"
      />

      <div v-if="filteredSorted.length === 0" class="empty">
        No receivers match your filters
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import GlobalReceiverHealthCard from "./GlobalReceiverHealthCard.vue"

const props = defineProps({
  receivers: { type: Array, default: () => [] },
  sort: { type: String, default: "name" },
  filter: { type: String, default: "all" },
  groupByHealth: { type: Boolean, default: false }
})

const emit = defineEmits(["inspect"])

const localSort = ref(props.sort)
const localFilter = ref(props.filter)
const localGroup = ref(props.groupByHealth)

const healthOrder = ["good", "degraded", "bad"]

// ------------------------------------------------------------
// Filtering
// ------------------------------------------------------------
const filtered = computed(() => {
  if (localFilter.value === "all") return props.receivers
  return props.receivers.filter(r => r.health === localFilter.value)
})

// ------------------------------------------------------------
// Sorting
// ------------------------------------------------------------
const filteredSorted = computed(() => {
  const arr = [...filtered.value]

  if (localSort.value === "health") {
    return arr.sort(
      (a, b) =>
        healthOrder.indexOf(a.health) -
        healthOrder.indexOf(b.health)
    )
  }

  return arr.sort((a, b) => a.name.localeCompare(b.name))
})

// ------------------------------------------------------------
// Grouping
// ------------------------------------------------------------
const grouped = computed(() => {
  const groups = {
    good: [],
    degraded: [],
    bad: []
  }

  for (const r of filteredSorted.value) {
    groups[r.health]?.push(r)
  }

  return groups
})

function inspect(receiver) {
  emit("inspect", receiver)
}
</script>

<style scoped>
.receiver-list {
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

.sort,
.filter {
  background: #2a2a2a;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  color: #fff;
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
