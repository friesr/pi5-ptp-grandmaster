<template>
  <div class="environment-panel">

    <!-- Header -->
    <div class="header">
      <h2>Environment</h2>

      <span class="status" :class="env.status">
        {{ env.status }}
      </span>
    </div>

    <div class="body">

      <!-- Metrics -->
      <div class="section">
        <h3>Metrics</h3>

        <div class="grid">
          <div><strong>Temperature:</strong> {{ env.temperature }} °C</div>
          <div><strong>Humidity:</strong> {{ env.humidity }}%</div>
          <div><strong>Noise Floor:</strong> {{ env.noise }} dB</div>
          <div><strong>Interference:</strong> {{ env.interference }}</div>
        </div>
      </div>

      <!-- Trends -->
      <div class="section">
        <h3>Trends</h3>

        <div class="trend-grid">
          <div>
            <span class="label">Temp</span>
            <span class="value" :class="env.trend.temperature">{{ env.trend.temperature }}</span>
          </div>

          <div>
            <span class="label">Humidity</span>
            <span class="value" :class="env.trend.humidity">{{ env.trend.humidity }}</span>
          </div>

          <div>
            <span class="label">Noise</span>
            <span class="value" :class="env.trend.noise">{{ env.trend.noise }}</span>
          </div>

          <div>
            <span class="label">Interference</span>
            <span class="value" :class="env.trend.interference">{{ env.trend.interference }}</span>
          </div>
        </div>
      </div>

      <!-- Weather -->
      <div class="section">
        <h3>Weather</h3>

        <div class="grid">
          <div><strong>Condition:</strong> {{ env.weather.condition }}</div>
          <div><strong>Wind:</strong> {{ env.weather.wind }} km/h</div>
          <div><strong>Pressure:</strong> {{ env.weather.pressure }} hPa</div>
          <div><strong>Visibility:</strong> {{ env.weather.visibility }} km</div>
        </div>
      </div>

      <!-- Charts -->
      <div class="section charts">
        <h3>Charts</h3>
        <slot name="charts" :env="env" />
      </div>

    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  env: { type: Object, required: true }
})
</script>

<style scoped>
.environment-panel {
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

.status {
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: capitalize;
  font-weight: bold;
}

.status.good { background: #4caf50 }
.status.warn { background: #ff9800 }
.status.bad { background: #f44336 }

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
