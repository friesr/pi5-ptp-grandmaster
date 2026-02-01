<template>
  <div class="card">
    <h3>{{ title }}</h3>

    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">Error loading summary</div>
    <div v-else class="summary">
      <div class="metric" v-for="(value, key) in summary" :key="key">
        <span class="label">{{ key }}</span>
        <span class="value">{{ value }}</span>
      </div>
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
const summary = ref({})

onMounted(async () => {
  try {
    const res = await axios.get(props.api)
    summary.value = res.data
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

h3 {
  margin: 0 0 0.8rem 0;
  font-size: 1.2rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 0;
  border-bottom: 1px solid #222;
}

.label {
  color: #aaa;
}

.value {
  color: #fff;
}

.loading {
  color: #888;
}

.error {
  color: #ff4d4d;
}
</style>
