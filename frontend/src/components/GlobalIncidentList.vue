<template>
  <div class="incident-list">
    <h2>Global Incidents</h2>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading incidents</div>
    <div v-else>
      <GlobalIncidentCard
        v-for="incident in incidents"
        :key="incident.id"
        :incident="incident"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import GlobalIncidentCard from "./GlobalIncidentCard.vue"

const loading = ref(true)
const error = ref(false)
const incidents = ref([])

onMounted(async () => {
  try {
    const res = await axios.get("/api/incidents")
    incidents.value = res.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.incident-list {
  background: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #333;
}

h2 {
  margin: 0 0 1rem 0;
  font-size: 1.4rem;
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}
</style>
