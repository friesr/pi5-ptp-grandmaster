<template>
  <div class="constellation-grid">

    <!-- Header -->
    <div class="header">
      <h2>Constellations</h2>

      <select v-model="localSort" class="sort">
        <option value="name">Sort by name</option>
        <option value="health">Sort by health</option>
      </select>
    </div>

    <!-- Grid -->
    <div class="grid">
      <GlobalConstellationSummaryCard
        v-for="c in sorted"
        :key="c.name"
        :name="c.name"
        :summary="c.summary"
        :trend="c.trend"
        :activity="c.activity"
        @select="select"
      >
        <!-- Optional sparkline slot -->
        <template #sparkline>
          <slot name="sparkline" :constellation="c" />
        </template>
      </GlobalConstellationSummaryCard>
    </div>

    <div v-if="sorted.length === 0" class="empty">
      No constellations available
    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import GlobalConstellationSummaryCard from "./GlobalConstellationSummaryCard.vue"

const props = defineProps({
  constellations: { type: Array, default: () => [] },
  sort: { type: String, default: "name" }
})

const emit = defineEmits(["select"])

const localSort = ref(props.sort)

const sorted = computed(() => {
  const arr = [...props.constellations]

  if (localSort.value === "health") {
    return arr.sort((a, b) =>
      (b.summary.healthy - b.summary.unhealthy) -
      (a.summary.healthy - a.summary.unhealthy)
    )
  }

  return arr.sort((a, b) => a.name.localeCompare(b.name))
})

function select(name) {
  emit("select", name)
}
</script>

<style scoped>
.constellation-grid {
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
