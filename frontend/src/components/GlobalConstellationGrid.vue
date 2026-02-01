<template>
  <div class="grid-container">
    <h2>Constellation Summary</h2>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading constellation summary</div>
    <div v-else class="grid">
      <GlobalConstellationSummaryCard
        v-for="card in cards"
        :key="card.title"
        :title="card.title"
        :api="card.api"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import GlobalConstellationSummaryCard from "./GlobalConstellationSummaryCard.vue"

const loading = ref(true)
const error = ref(false)
const cards = ref([])

onMounted(async () => {
  try {
    const res = await axios.get("/api/constellation/summary")
    cards.value = res.data.cards
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.grid-container {
  padding: 1.5rem;
  background: #1a1a1a;
  border-radius: 8px;
  border: 1px solid #333;
}

h2 {
  margin: 0 0 1rem 0;
  font-size: 1.4rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.2rem;
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}
</style>
