<template>
  <div class="card">
    <h2>{{ title }}</h2>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading data</div>
    <div v-else class="value">
      {{ summary }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const props = defineProps({
  title: String,
  api: String
})

const loading = ref(true)
const error = ref(false)
const summary = ref("")

onMounted(async () => {
  try {
    const res = await axios.get(props.api)
    summary.value = JSON.stringify(res.data).slice(0, 120) + "…"
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.card {
  background: #1a1a1a;
  padding: 1.2rem;
  border-radius: 8px;
  border: 1px solid #333;
}

h2 {
  margin: 0 0 0.8rem 0;
  font-size: 1.2rem;
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}

.value {
  font-size: 0.9rem;
  color: #ccc;
  word-break: break-word;
}
</style>
