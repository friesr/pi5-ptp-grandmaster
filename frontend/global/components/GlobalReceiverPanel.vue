<template>
  <div class="receiver-panel">

    <!-- Header -->
    <div class="header">
      <h2>{{ receiver.name }}</h2>

      <span class="health" :class="receiver.health">
        {{ receiver.health }}
      </span>
    </div>

    <div class="body">

      <!-- Status -->
      <div class="section">
        <h3>Status</h3>

        <div class="grid">
          <div><strong>Model:</strong> {{ receiver.model }}</div>
          <div><strong>Firmware:</strong> {{ receiver.firmware }}</div>
          <div><strong>Lock:</strong> {{ receiver.lock_status }}</div>
          <div><strong>Last Sync:</strong> {{ formatTS(receiver.last_sync) }}</div>
        </div>
      </div>

      <!-- Clock -->
      <div class="section">
        <h3>Clock</h3>

        <div class="grid">
          <div><strong>Stability:</strong> {{ receiver.clock.stability }} ps</div>
          <div><strong>Drift:</strong> {{ receiver.clock.drift }} ns/s</div>
          <div><strong>PPS Quality:</strong> {{ receiver.clock.pps_quality }}</div>
          <div><strong>Jitter:</strong> {{ receiver.clock.jitter }} ps</div>
        </div>
      </div>

      <!-- Environment -->
      <div class="section">
        <h3>Environment</h3>

        <div class="grid">
          <div><strong>Temp:</strong> {{ receiver.environment.temperature }} °C</div>
          <div><strong>Humidity:</strong> {{ receiver.environment.humidity }}%</div>
          <div><strong>Noise:</strong> {{ receiver.environment.noise }} dB</div>
          <div><strong>Interference:</strong> {{ receiver.environment.interference }}</div>
        </div>
      </div>

      <!-- Self Diagnostics -->
      <div class="section">
        <h3>Self Diagnostics</h3>

        <ul class="diag-list">
          <li v-for="(d, i) in receiver.diagnostics" :key="i">
            <span class="label">{{ d.label }}:</span>
            <span class="value" :class="d.status">{{ d.status }}</span>
          </li>
        </ul>
      </div>

      <!-- Chart Slots -->
      <div class="section charts">
        <h3>Charts</h3>
        <slot name="charts" :receiver="receiver" />
      </div>

    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  receiver: { type: Object, required: true }
})

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}
</script>

<style scoped>
.receiver-panel {
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

.health {
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: capitalize;
  font-weight: bold;
}

.health.good { background: #4caf50 }
.health.degraded { background: #ff9800 }
.health.bad { background: #f44336 }

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

.diag-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.diag-list li {
  padding: 4px 0;
  display: flex;
  justify-content: space-between;
}

.value.good { color: #4caf50 }
.value.warn { color: #ff9800 }
.value.bad { color: #f44336 }

.charts {
  height: 200px;
}
</style>
