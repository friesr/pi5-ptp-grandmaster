<template>
  <div class="interference-panel">

    <!-- Header -->
    <div class="header">
      <h2>Interference</h2>

      <span class="severity" :class="interference.severity">
        {{ interference.severity }}
      </span>
    </div>

    <div class="body">

      <!-- Bands -->
      <div class="section">
        <h3>Bands</h3>

        <ul class="band-list">
          <li v-for="(b, i) in interference.bands" :key="i">
            <span class="freq">{{ b.freq }} MHz</span>
            <span class="level" :class="b.level">{{ b.level }}</span>
          </li>
        </ul>
      </div>

      <!-- Spectral Density -->
      <div class="section">
        <h3>Spectral Density</h3>

        <div class="chart">
          <slot name="spectrum-chart" :spectrum="interference.spectrum" />
        </div>
      </div>

      <!-- Time-Frequency Heatmap -->
      <div class="section">
        <h3>Heatmap</h3>

        <div class="chart">
          <slot name="heatmap" :heatmap="interference.heatmap" />
        </div>
      </div>

      <!-- Source Classification -->
      <div class="section">
        <h3>Source Classification</h3>

        <div class="grid">
          <div><strong>Type:</strong> {{ interference.source.type }}</div>
          <div><strong>Confidence:</strong> {{ interference.source.confidence }}%</div>
          <div><strong>Pattern:</strong> {{ interference.source.pattern }}</div>
          <div><strong>Notes:</strong> {{ interference.source.notes }}</div>
        </div>
      </div>

      <!-- Trends -->
      <div class="section">
        <h3>Trends</h3>

        <div class="trend-grid">
          <div>
            <span class="label">Power</span>
            <span class="value" :class="interference.trend.power">{{ interference.trend.power }}</span>
          </div>

          <div>
            <span class="label">Bandwidth</span>
            <span class="value" :class="interference.trend.bandwidth">{{ interference.trend.bandwidth }}</span>
          </div>

          <div>
            <span class="label">Events</span>
            <span class="value" :class="interference.trend.events">{{ interference.trend.events }}</span>
          </div>

          <div>
            <span class="label">Stability</span>
            <span class="value" :class="interference.trend.stability">{{ interference.trend.stability }}</span>
          </div>
        </div>
      </div>

      <!-- Mini-Charts -->
      <div class="section charts">
        <h3>Charts</h3>
        <slot name="charts" :interference="interference" />
      </div>

    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  interference: { type: Object, required: true }
})
</script>

<style scoped>
.interference-panel {
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

.band-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.band-list li {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
}

.freq {
  opacity: 0.9;
}

.level {
  text-transform: capitalize;
  font-weight: bold;
}

.level.low { color: #4caf50 }
.level.medium { color: #ff9800 }
.level.high { color: #f44336 }

.chart {
  background: #333;
  border-radius: 6px;
  padding: 8px;
  height: 180px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
  margin-top: 8px;
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
