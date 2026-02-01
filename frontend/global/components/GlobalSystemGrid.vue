<template>
  <div class="system-grid">

    <!-- Header -->
    <div class="header">
      <h2>Systems</h2>

      <select v-model="localSort" class="sort">
        <option value="name">Sort by name</option>
        <option value="health">Sort by health</option>
      </select>
    </div>

    <!-- Grid -->
    <div class="grid">
      <GlobalSystemSummaryCard
        v-for="s in sorted"
        :key="s.name"
        :system="s"
        @inspect="inspect"
      >
        <template #sparkline>
          <slot name="sparkline" :system="s" />
        </template>
      </GlobalSystemSummaryCard>
    </div>

    <div v-if="sorted.length === 0" class="empty">
      No systems available
    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import GlobalSystemSummaryCard from "./GlobalSystemSummaryCard.vue"

const props = defineProps({
  systems: { type: Array, default: () => [] },
  sort: { type: String, default: "name" }
})

const emit = defineEmits(["inspect"])

const localSort = ref(props.sort)

const sorted = computed(() => {
  const arr = [...props.systems]

  if (localSort.value === "health") {
    return arr.sort((a, b) => {
      const score = s => (
        (s.constellations_ok + s.receivers_ok + s.antennas_ok) -
        (s.constellations_total + s.receivers_total + s.antennas_total)
      )
      return score(b) - score(a)
    })
  }

  return arr.sort((a, b) => a.name.localeCompare(b.name))
})

function inspect(system) {
  emit("inspect", system)
}
</script>

<style scoped>
.system-grid {
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

.sort {
  background: #2a2a2a;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  color: #fff;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.empty {
  opacity: 0.7;
  padding: 8px 0;
}
</style>
