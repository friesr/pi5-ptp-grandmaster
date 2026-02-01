<template>
  <div class="global-archive">

    <!-- Header -->
    <header class="ga-header">
      <h1>Global Archive</h1>
      <div class="subtitle">Long-term global intelligence history</div>
    </header>

    <!-- Search -->
    <section class="search-card">
      <input
        v-model="query"
        @keyup.enter="search"
        placeholder="Search archive..."
        class="search-input"
      />
      <button @click="search">Search</button>
    </section>

    <!-- Archive Lists -->
    <section class="lists-card">
      <h2>Archive Contents</h2>

      <div class="lists-container">

        <div class="list-column">
          <h3>Incidents</h3>
          <ul>
            <li
              v-for="f in archive.incidents"
              :key="f"
              @click="load(f)"
              class="file-item"
            >
              {{ f }}
            </li>
          </ul>
        </div>

        <div class="list-column">
          <h3>Storyboards</h3>
          <ul>
            <li
              v-for="f in archive.storyboards"
              :key="f"
              @click="load(f)"
              class="file-item"
            >
              {{ f }}
            </li>
          </ul>
        </div>

        <div class="list-column">
          <h3>Replay Snapshots</h3>
          <ul>
            <li
              v-for="f in archive.replay_snapshots"
              :key="f"
              @click="load(f)"
              class="file-item"
            >
              {{ f }}
            </li>
          </ul>
        </div>

        <div class="list-column">
          <h3>Control Room</h3>
          <ul>
            <li
              v-for="f in archive.control_room"
              :key="f"
              @click="load(f)"
              class="file-item"
            >
              {{ f }}
            </li>
          </ul>
        </div>

      </div>
    </section>

    <!-- Search Results -->
    <section v-if="results.length" class="results-card">
      <h2>Search Results</h2>
      <ul>
        <li
          v-for="r in results"
          :key="r"
          @click="load(r)"
          class="file-item"
        >
          {{ r }}
        </li>
      </ul>
    </section>

    <!-- File Viewer -->
    <section v-if="loaded" class="viewer-card">
      <h2>Viewing: {{ loadedFile }}</h2>
      <pre class="json-viewer">{{ formattedLoaded }}</pre>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { GlobalAPI } from "../api/global_api"

const archive = ref({
  incidents: [],
  storyboards: [],
  replay_snapshots: [],
  control_room: []
})

const results = ref([])
const loaded = ref(null)
const loadedFile = ref("")
const query = ref("")

const formattedLoaded = computed(() =>
  loaded.value ? JSON.stringify(loaded.value, null, 2) : ""
)

async function refresh() {
  archive.value = await GlobalAPI.archive.list()
}

async function search() {
  if (!query.value.trim()) return
  const res = await GlobalAPI.archive.search(query.value)
  results.value = res.results
}

async function load(file) {
  loadedFile.value = file
  loaded.value = await GlobalAPI.archive.load(file)
}

onMounted(() => {
  refresh()
  setInterval(refresh, 5000)
})
</script>

<style scoped>
.global-archive {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.ga-header {
  display: flex;
  flex-direction: column;
}

.search-card,
.lists-card,
.results-card,
.viewer-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.search-input {
  width: 60%;
  padding: 8px;
  margin-right: 8px;
}

.lists-container {
  display: flex;
  gap: 24px;
}

.list-column {
  flex: 1;
}

.file-item {
  cursor: pointer;
  padding: 4px 0;
}

.file-item:hover {
  color: #4fc3f7;
}

.json-viewer {
  background: #111;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
}
</style>
