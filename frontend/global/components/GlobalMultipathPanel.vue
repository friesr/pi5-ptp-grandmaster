<template>
  <div class="multipath-panel">

    <!-- Header -->
    <div class="header">
      <h2>Multipath</h2>

      <span class="severity" :class="multipath.severity">
        {{ multipath.severity }}
      </span>
    </div>

    <div class="body">

      <!-- Summary -->
      <div class="section">
        <h3>Summary</h3>

        <div class="grid">
          <div><strong>Avg Delay:</strong> {{ multipath.avg_delay }} ns</div>
          <div><strong>Peak Delay:</strong> {{ multipath.peak_delay }} ns</div>
          <div><strong>Reflection Strength:</strong> {{ multipath.reflection_strength }} dB</div>
          <div><strong>Events:</strong> {{ multipath.events }}</div>
        </div>
      </div>

      <!-- Satellite Multipath -->
      <div class="section">
        <h3>Per‑Satellite Multipath</h3>

        <ul class="sat-list">
          <li v-for="(s, i) in multipath.satellites" :key="i">
            <span class="prn">{{ s.prn }}</span>
            <span class="delay">{{ s.delay }} ns</span>
            <span class="strength" :class="strengthClass(s.strength)">
              {{ s.strength }} dB
            </span>
          </li>
        </ul>
      </div>

      <!-- Delay Chart -->
      <div class="section">
        <h3>Delay Over Time</h3>

        <div class="chart">
          <slot name="delay-chart" :delay="multipath.delay_series" />
        </div>
      </div>

      <!-- Reflection Classification -->
      <div class="section">
        <h3>Reflection Classification</h3>

        <div class="grid">
          <div><strong>Type:</strong> {{ multipath.classification.type }}</div>
          <div><strong>Confidence:</strong> {{ multipath.classification.confidence }}%</div>
          <div><strong>Surface:</strong> {{ multipath.classification.surface }}</div>
          <div><strong>Notes:</strong> {{ multipath.classification.notes }}</div>
        </div>
      </div>

      <!-- Trends -->
      <div class="section">
        <h3>Trends</h3>

        <div class="trend-grid">
          <div>
            <span class="label">Delay</span>
            <span class="value" :class="multipath.trend.delay">{{ multipath.trend.delay }}</span>
          </div>

          <div>
            <span class="label">Strength</span>
            <span class="value" :class="multipath.trend.strength">{{ multipath.trend.strength }}</span>
          </div>

          <div>
            <span class="label">Events</span>
            <span class="value" :class="multipath.trend.events">{{ multipath.trend.events }}</span>
          </div>

          <div>
            <span class="label">Stability</span>
            <span class="value" :class="multipath.trend.stability">{{ multipath.trend.stability }}</span>
          </div>
        </div>
      </div>

      <!-- Mini‑Charts -->
      <div class="section charts">
        <h3>Charts</h3>
        <slot name="charts" :multipath="multipath" />
      </div>

    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  multipath: { type: Object, required: true }
})

function strengthClass(v) {
  if (v > 20) return "high"
  if (v > 10) return "medium"
  return "low"
}
</script>

<style scoped>
.multipath-panel {
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

.severity {
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: capitalize;
  font-weight: bold;
}

.severity.low { background: #4caf50 }
.severity.medium { background: #ff9800 }
.severity.high { background: #f44336 }

.section {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
  margin-top: 8px;
}

.sat-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sat-list li {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
}

.prn {
  font-weight: bold;
}

.delay {
  opacity: 0.8;
}

.strength {
  font-weight: bold;
}

.strength.low { color: #4caf50 }
.strength.medium { color: #ff9800 }
.strength.high { color: #f44336 }

.chart {
  background: #333;
  border-radius: 6px;
  padding: 8px;
  height: 180px;
}

.trend-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 8px;
}

.label {
  opacity: 0.7;
  font-size: 0.85rem;
}

.value {
  font-weight: bold;
  text-transform: capitalize;
}

.value.up { color: #4caf50 }
.value.down { color: #f44336 }
.value.steady { color: #ff9800 }

.charts {
  height: 200px;
}
</style>
