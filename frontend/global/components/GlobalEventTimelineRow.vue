<template>
  <div class="timeline-row" @click="select(event)" :title="tooltip">

    <!-- Timestamp -->
    <div class="timestamp">
      {{ formattedTS }}
    </div>

    <!-- Marker -->
    <div class="marker">
      <div class="line"></div>
      <div class="dot" :class="eventClass"></div>
    </div>

    <!-- Content -->
    <div class="content">
      <div class="header">
        <GlobalEventBadge :event="event" />
        <GlobalSeverityTag
          v-if="event.severity"
          :severity="event.severity"
          uppercase
        />
      </div>

      <div class="description">
        {{ event.type }}
        <span v-if="event.details">— {{ event.details }}</span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"
import GlobalEventBadge from "./GlobalEventBadge.vue"
import GlobalSeverityTag from "./GlobalSeverityTag.vue"

const props = defineProps({
  event: { type: Object, required: true }
})

const emit = defineEmits(["select"])

const formattedTS = computed(() =>
  new Date(props.event.timestamp * 1000).toLocaleString()
)

const eventClass = computed(() => {
  const s = props.event.source
  if (s === "correlation") return "correlation"
  if (s === "risk") return "risk"
  if (s === "intel") return "intel"
  return "node"
})

const tooltip = computed(() => {
  const e = props.event
  return `${e.source.toUpperCase()} — ${e.type}
Timestamp: ${new Date(e.timestamp * 1000).toLocaleString()}`
})

function select(e) {
  emit("select", e)
}
</script>

<style scoped>
.timeline-row {
  display: grid;
  grid-template-columns: 160px 40px 1fr;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #333;
  cursor: pointer;
}

.timeline-row:hover {
  background: #2a2a2a;
}

.timestamp {
  opacity: 0.8;
  font-size: 0.9rem;
}

.marker {
  position: relative;
  display: flex;
  justify-content: center;
}

.marker .line {
  position: absolute;
  width: 2px;
  height: 100%;
  background: #444;
}

.marker .dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 14px;
}

.dot.node { background: #4caf50 }
.dot.intel { background: #2196f3 }
.dot.correlation { background: #ff9800 }
.dot.risk { background: #f44336 }

.content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.header {
  display: flex;
  gap: 8px;
  align-items: center;
}

.description {
  opacity: 0.9;
}
</style>
