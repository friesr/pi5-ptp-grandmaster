<template>
  <div class="constellation-map">

    <!-- Header -->
    <div class="header">
      <h2>Sky Plot</h2>
      <div class="legend">
        <span class="dot healthy"></span> Healthy
        <span class="dot unhealthy"></span> Unhealthy
        <span class="dot eclipse"></span> Eclipse
      </div>
    </div>

    <!-- Sky Plot -->
    <div class="sky">
      <svg viewBox="0 0 200 200" class="sky-svg">

        <!-- Concentric elevation rings -->
        <circle v-for="r in rings" :key="r" :cx="100" :cy="100" :r="r" class="ring" />

        <!-- Azimuth lines -->
        <line
          v-for="a in azimuths"
          :key="a"
          :x1="100"
          :y1="100"
          :x2="100 + 100 * Math.sin(a)"
          :y2="100 - 100 * Math.cos(a)"
          class="az-line"
        />

        <!-- Satellites -->
        <g
          v-for="s in satellites"
          :key="s.prn"
          class="sat"
          :transform="satTransform(s)"
          @click="select(s)"
        >
          <circle
            class="sat-dot"
            :class="satClass(s)"
            r="4"
          />
          <text
            class="label"
            dx="6"
            dy="3"
          >
            {{ s.prn }}
          </text>
        </g>

      </svg>
    </div>

  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue"

const props = defineProps({
  satellites: { type: Array, default: () => [] }
})

const emit = defineEmits(["select"])

// Elevation rings at 30°, 60°, 80°
const rings = [30, 60, 80].map(e => (90 - e) / 90 * 100)

// Azimuth lines every 45°
const azimuths = [0, 45, 90, 135, 180, 225, 270, 315].map(a => a * Math.PI / 180)

function satTransform(s) {
  // Convert az/el to polar projection
  const r = (90 - s.el) / 90 * 100
  const a = s.az * Math.PI / 180
  const x = 100 + r * Math.sin(a)
  const y = 100 - r * Math.cos(a)
  return `translate(${x}, ${y})`
}

function satClass(s) {
  if (s.eclipse) return "eclipse"
  if (s.health === "unhealthy") return "unhealthy"
  return "healthy"
}

function select(s) {
  emit("select", s)
}
</script>

<style scoped>
.constellation-map {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.legend {
  display: flex;
  gap: 12px;
  align-items: center;
  font-size: 0.85rem;
  opacity: 0.9;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.dot.healthy { background: #4caf50 }
.dot.unhealthy { background: #f44336 }
.dot.eclipse { background: #9c27b0 }

.sky {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 10px;
}

.sky-svg {
  width: 100%;
  height: 100%;
}

.ring {
  fill: none;
  stroke: #444;
  stroke-width: 1;
}

.az-line {
  stroke: #444;
  stroke-width: 1;
}

.sat-dot {
  stroke: #000;
  stroke-width: 1;
}

.sat-dot.healthy { fill: #4caf50 }
.sat-dot.unhealthy { fill: #f44336 }
.sat-dot.eclipse { fill: #9c27b0 }

.label {
  fill: #fff;
  font-size: 0.7rem;
  pointer-events: none;
}
</style>
