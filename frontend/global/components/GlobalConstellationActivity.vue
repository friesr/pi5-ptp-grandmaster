<template>
  <div class="constellation-activity">

    <h3>Constellation Activity</h3>

    <ul class="activity-list">
      <li
        v-for="(count, name) in activity"
        :key="name"
        class="activity-row"
      >
        <span class="label" :class="name">{{ name }}</span>

        <div class="bar">
          <div
            class="fill"
            :style="{ width: barWidth(count), background: colorFor(name) }"
          ></div>
        </div>

        <span class="count">{{ count }}</span>
      </li>
    </ul>

  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  activity: { type: Object, default: () => ({}) }
})

// ------------------------------------------------------------
// Bar scaling
// ------------------------------------------------------------
const maxCount = computed(() => {
  const values = Object.values(props.activity)
  return values.length ? Math.max(...values) : 1
})

function barWidth(count) {
  return (count / maxCount.value) * 100 + "%"
}

// ------------------------------------------------------------
// Colors per constellation
// ------------------------------------------------------------
function colorFor(name) {
  switch (name.toUpperCase()) {
    case "GPS": return "#4caf50"
    case "GLONASS": return "#2196f3"
    case "GALILEO": return "#ff9800"
    case "BEIDOU": return "#9c27b0"
    default: return "#ccc"
  }
}
</script>

<style scoped>
.constellation-activity {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
}

.activity-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.activity-row {
  display: grid;
  grid-template-columns: 100px 1fr 40px;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  text-transform: uppercase;
}

.label.GPS { color: #4caf50 }
.label.GLONASS { color: #2196f3 }
.label.GALILEO { color: #ff9800 }
.label.BEIDOU { color: #9c27b0 }

.bar {
  background: #333;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.fill {
  height: 100%;
  transition: width 0.3s ease;
}

.count {
  text-align: right;
  opacity: 0.8;
}
</style>
