<template>
  <div class="risk-gauge">

    <!-- SVG Arc -->
    <svg viewBox="0 0 100 60" class="gauge">
      <path
        class="bg-arc"
        d="M10 55 A40 40 0 0 1 90 55"
      />

      <path
        class="risk-arc"
        :d="riskArcPath"
        :stroke="riskColor"
      />

      <path
        class="forecast-arc"
        :d="forecastArcPath"
        :stroke="forecastColor"
      />
    </svg>

    <!-- Labels -->
    <div class="labels">
      <div class="value">{{ (risk * 100).toFixed(0) }}%</div>
      <div class="label">Risk</div>
      <div class="forecast">Forecast: {{ (forecast * 100).toFixed(0) }}%</div>
    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  risk: { type: Number, default: 0 },
  forecast: { type: Number, default: 0 }
})

// ------------------------------------------------------------
// Arc math
// ------------------------------------------------------------
function arcForValue(v) {
  const start = Math.PI
  const end = Math.PI + (v * Math.PI)
  const r = 40
  const cx = 50
  const cy = 55

  const x1 = cx + r * Math.cos(start)
  const y1 = cy + r * Math.sin(start)
  const x2 = cx + r * Math.cos(end)
  const y2 = cy + r * Math.sin(end)

  return `M${x1} ${y1} A${r} ${r} 0 0 1 ${x2} ${y2}`
}

const riskArcPath = computed(() => arcForValue(props.risk))
const forecastArcPath = computed(() => arcForValue(props.forecast))

// ------------------------------------------------------------
// Colors
// ------------------------------------------------------------
const riskColor = computed(() => {
  if (props.risk > 0.7) return "#f44336"
  if (props.risk > 0.5) return "#ff9800"
  return "#4caf50"
})

const forecastColor = computed(() => "#4fc3f7")
</script>

<style scoped>
.risk-gauge {
  width: 160px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.gauge {
  width: 100%;
  height: auto;
}

.bg-arc {
  fill: none;
  stroke: #333;
  stroke-width: 6;
}

.risk-arc {
  fill: none;
  stroke-width: 6;
  transition: stroke 0.3s ease, d 0.3s ease;
}

.forecast-arc {
  fill: none;
  stroke-width: 3;
  opacity: 0.6;
  transition: d 0.3s ease;
}

.labels .value {
  font-size: 1.4rem;
  font-weight: bold;
}

.labels .forecast {
  font-size: 0.85rem;
  opacity: 0.8;
}
</style>
