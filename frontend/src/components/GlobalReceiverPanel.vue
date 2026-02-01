<template>
  <div class="panel">
    <h2>Receiver Panel</h2>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading receiver data</div>
    <div v-else class="receiver-list">
      <div
        class="receiver"
        v-for="rx in receivers"
        :key="rx.id"
      >
        <h3>{{ rx.name }}</h3>
        <p>Status: <strong>{{ rx.status }}</strong></p>
        <p>Last Update: {{ rx.last_update }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const loading = ref(true)
const error = ref(false)
const receivers = ref([])

onMounted(async () => {
  try {
    const res = await axios.get("/api/receivers")
    receivers.value = res.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.panel {
  background: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #333;
}

h2 {
  margin: 0 0 1rem 0;
  font-size: 1.4rem;
}

.receiver-list {
  display: grid;
  gap: 1rem;
}

.receiver {
  background: #111;
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid #222;
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}
</style>
