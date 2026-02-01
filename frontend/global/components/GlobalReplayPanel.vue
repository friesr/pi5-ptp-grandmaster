<template>
  <div class="replay-panel">

    <!-- Header -->
    <div class="header">
      <h2>Replay</h2>
      <div class="window">
        {{ formatTS(startTime) }} → {{ formatTS(endTime) }}
      </div>
    </div>

    <!-- Controls -->
    <GlobalReplayControls
      :currentTime="currentTime"
      :startTime="startTime"
      :endTime="endTime"
      :events="events"
      :playing="playing"
      :speed="speed"
      @play="$emit('play')"
      @pause="$emit('pause')"
      @seek="$emit('seek', $event)"
      @speed="$emit('speed', $event)"
      @jump="$emit('seek', $event)"
    />

    <!-- Timeline -->
    <GlobalReplayTimeline
      :startTime="startTime"
      :endTime="endTime"
      :currentTime="currentTime"
      :events="events"
      :clusters="clusters"
      :interference="interference"
      @seek="$emit('seek', $event)"
    />

    <div class="body">

      <!-- Sidebar -->
      <div class="sidebar">

        <!-- Snapshot -->
        <div v-if="snapshot" class="snapshot-section">
          <GlobalSnapshotMini :snapshot="snapshot" />
        </div>

        <!-- Event List -->
        <div class="events-section">
          <h3>Events</h3>
          <ul class="event-list">
            <li
              v-for="(e, i) in events"
              :key="i"
              class="event-row"
              @click="$emit('seek', e.timestamp)"
            >
              <span class="ts">{{ formatTS(e.timestamp) }}</span>
              <span class="type">{{ e.type }}</span>
            </li>
          </ul>
        </div>

      </div>

      <!-- Main Content -->
      <div class="content">
        <slot />
      </div>

    </div>

  </div>
</template>

<script setup>
import GlobalReplayControls from "./GlobalReplayControls.vue"
import GlobalReplayTimeline from "./GlobalReplayTimeline.vue"
import GlobalSnapshotMini from "./GlobalSnapshotMini.vue"

const props = defineProps({
  startTime: Number,
  endTime: Number,
  currentTime: Number,
  events: Array,
  clusters: Array,
  interference: Array,
  snapshot: Object,
  playing: Boolean,
  speed: Number
})

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}
</script>

<style scoped>
.replay-panel {
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

.window {
  opacity: 0.8;
}

.body {
  display: flex;
  gap: 20px;
}

.sidebar {
  width: 280px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.snapshot-section {
  background: #2a2a2a;
  padding: 12px;
  border-radius: 8px;
}

.events-section {
  background: #2a2a2a;
  padding: 12px;
  border-radius: 8px;
}

.event-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.event-row {
  padding: 6px 0;
  display: flex;
  justify-content: space-between;
  cursor: pointer;
}

.event-row:hover {
  background: #333;
}

.ts {
  opacity: 0.7;
  font-size: 0.85rem;
}

.content {
  flex: 1;
  background: #2a2a2a;
  border-radius: 8px;
  padding: 16px;
}
</style>
