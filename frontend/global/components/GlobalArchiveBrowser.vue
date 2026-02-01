<template>
  <div class="archive-browser">

    <!-- Sidebar: File List -->
    <div class="sidebar">
      <h3>Archive</h3>

      <ul class="file-list">
        <li
          v-for="f in files"
          :key="f.name"
          :class="{ selected: f.name === selectedName }"
          @click="select(f)"
        >
          <div class="name">{{ f.name }}</div>
          <div class="ts">{{ formatTS(f.timestamp) }}</div>
        </li>

        <li v-if="files.length === 0" class="empty">
          No archive files found
        </li>
      </ul>
    </div>

    <!-- Preview Panel -->
    <div class="preview">

      <div v-if="selected" class="preview-content">

        <h2>{{ selected.name }}</h2>

        <div class="meta">
          <div><strong>Timestamp:</strong> {{ formatTS(selected.timestamp) }}</div>
          <div><strong>Type:</strong> {{ selected.type }}</div>
          <div v-if="selected.size"><strong>Size:</strong> {{ selected.size }} KB</div>
        </div>

        <!-- Snapshot Preview -->
        <div v-if="selected.snapshot" class="snapshot-section">
          <GlobalSnapshotMini :snapshot="selected.snapshot" />
        </div>

        <!-- Description -->
        <div v-if="selected.description" class="description">
          {{ selected.description }}
        </div>

        <!-- Load Button -->
        <button class="load-btn" @click="load">
          Load
        </button>

      </div>

      <div v-else class="placeholder">
        Select a file to preview
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from "vue"
import GlobalSnapshotMini from "./GlobalSnapshotMini.vue"

const props = defineProps({
  files: { type: Array, default: () => [] }
})

const emit = defineEmits(["load"])

const selected = ref(null)
const selectedName = ref(null)

function select(f) {
  selected.value = f
  selectedName.value = f.name
}

function load() {
  if (selected.value) emit("load", selected.value)
}

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}
</script>

<style scoped>
.archive-browser {
  display: flex;
  gap: 20px;
  background: #1e1e1e;
  padding: 20px;
  border-radius: 12px;
}

.sidebar {
  width: 260px;
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.file-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.file-list li {
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 8px;
}

.file-list li:hover {
  background: #333;
}

.file-list li.selected {
  background: #444;
}

.name {
  font-weight: bold;
}

.ts {
  opacity: 0.7;
  font-size: 0.85rem;
}

.empty {
  opacity: 0.7;
  padding: 8px 0;
}

.preview {
  flex: 1;
  background: #2a2a2a;
  padding: 20px;
  border-radius: 8px;
}

.placeholder {
  opacity: 0.7;
  font-size: 1rem;
}

.meta {
  margin-bottom: 12px;
  opacity: 0.9;
}

.snapshot-section {
  margin: 16px 0;
}

.load-btn {
  background: #4caf50;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  font-weight: bold;
}

.load-btn:hover {
  background: #43a047;
}
</style>
