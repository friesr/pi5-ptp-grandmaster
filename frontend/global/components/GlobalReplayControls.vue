<template>
  <div class="replay-controls">

    <!-- Play / Pause -->
    <button class="btn" @click="togglePlay">
      {{ playing ? "Pause" : "Play" }}
    </button>

    <!-- Scrub Bar -->
    <input
      type="range"
      class="scrubber"
      :min="startTime"
      :max="endTime"
      :value="currentTime"
      @input="onSeek"
    />

    <!-- Speed -->
    <select class="speed" v-model="localSpeed" @change="onSpeed">
      <option v-for="s in speeds" :key="s" :value="s">
        {{ s }}x
      </option>
    </select>

    <!-- Jump to Event -->
    <select class="jump" @change="onJump">
      <option value="">Jump to event…</option>
      <option
        v-for="e in events"
        :key="e.timestamp"
        :value="e.timestamp"
      >
        {{ formatTS(e.timestamp) }} — {{ e.type }}
      </option>
    </select>

  </div>
</template>

<script setup>
import { ref } from "vue"

const props = defineProps({
  currentTime: { type: Number, required: true },
  startTime: { type: Number, required: true },
  endTime: { type: Number, required: true },
  events: { type: Array, default: () => [] },
  playing: { type: Boolean, default: false },
  speed: { type: Number, default: 1 }
})

const emit = defineEmits(["play", "pause", "seek", "speed", "jump"])

const speeds = [0.25, 0.5, 1, 2, 4, 8]
const localSpeed = ref(props.speed)

function togglePlay() {
  if (props.playing) emit("pause")
  else emit("play")
}

function onSeek(e) {
  emit("seek", Number(e.target.value))
}

function onSpeed() {
  emit("speed", Number(localSpeed.value))
}

function onJump(e) {
  const ts = Number(e.target.value)
  if (ts) emit("jump", ts)
}

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleTimeString()
}
</script>

<style scoped>
.replay-controls {
  background: #1e1e1e;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn {
  background: #333;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
}

.btn:hover {
  background: #444;
}

.scrubber {
  flex: 1;
}

.speed,
.jump {
  background: #2a2a2a;
  border: none;
  padding: 6px;
  border-radius: 6px;
  color: #fff;
}
</style>
