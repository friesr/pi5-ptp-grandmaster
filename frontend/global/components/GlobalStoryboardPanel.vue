<template>
  <div class="storyboard-panel">

    <!-- Header -->
    <div class="header">
      <h2>{{ storyboard.title }}</h2>
      <div class="timestamp">
        {{ formattedTimestamp }}
      </div>
    </div>

    <!-- Snapshot Context (optional) -->
    <div v-if="storyboard.snapshot" class="snapshot-section">
      <GlobalSnapshotMini :snapshot="storyboard.snapshot" />
    </div>

    <!-- Narrative Timeline -->
    <div class="timeline-section">
      <h3>Narrative</h3>

      <div class="timeline-list">
        <GlobalEventTimelineRow
          v-for="(e, i) in storyboard.events"
          :key="i"
          :event="e"
          @select="selectEvent"
        />

        <div v-if="storyboard.events.length === 0" class="empty">
          No events in this storyboard
        </div>
      </div>
    </div>

    <!-- Operator Notes -->
    <div v-if="storyboard.notes && storyboard.notes.length" class="notes-section">
      <h3>Operator Notes</h3>
      <ul class="notes">
        <li v-for="(n, i) in storyboard.notes" :key="i">
          <div class="note-timestamp">{{ formatTS(n.timestamp) }}</div>
          <div class="note-text">{{ n.text }}</div>
        </li>
      </ul>
    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"

import GlobalSnapshotMini from "./GlobalSnapshotMini.vue"
import GlobalEventTimelineRow from "./GlobalEventTimelineRow.vue"

const props = defineProps({
  storyboard: { type: Object, required: true }
})

const emit = defineEmits(["select-event"])

const formattedTimestamp = computed(() => {
  if (!props.storyboard.timestamp) return ""
  return new Date(props.storyboard.timestamp * 1000).toLocaleString()
})

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}

function selectEvent(e) {
  emit("select-event", e)
}
</script>

<style scoped>
.storyboard-panel {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timestamp {
  opacity: 0.8;
}

.snapshot-section {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.timeline-section {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.timeline-list {
  margin-top: 12px;
}

.empty {
  opacity: 0.7;
  font-size: 0.9rem;
  padding: 8px 0;
}

.notes-section {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.notes {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notes li {
  margin-bottom: 12px;
}

.note-timestamp {
  opacity: 0.7;
  font-size: 0.85rem;
}

.note-text {
  margin-top: 4px;
}
</style>
