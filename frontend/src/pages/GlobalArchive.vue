<template>
  <div class="page">
    <NavBar />

    <div class="card">
      <h2>Archive</h2>
      <p>This is a placeholder until the full archive browser is implemented.</p>
    </div>

    <div class="card">
      <h3>Available Archive Entries</h3>

      <div v-if="archives.length === 0">
        No archive entries found.
      </div>

      <ul v-else class="archive-list">
        <li v-for="entry in archives" :key="entry.id">
          <strong>{{ entry.name }}</strong>
          — {{ entry.timestamp }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'

import NavBar from '../components/NavBar.vue'

const archives = ref([])

async function load() {
  try {
    const data = await api("archive/list")
    archives.value = data.entries || []
  } catch (err) {
    console.error("Error loading archive list:", err)
  }
}

onMounted(() => {
  load()
  setInterval(load, 5000) // refresh every 5 seconds
})
</script>

<style scoped>
.archive-list {
  list-style: none;
  padding-left: 0;
}

.archive-list li {
  padding: 0.3rem 0;
  border-bottom: 1px solid #30363d;
}
</style>
