<template>
  <div class="antenna-panel">

    <!-- Header -->
    <div class="header">
      <h2>{{ antenna.name }}</h2>

      <span class="health" :class="antenna.health">
        {{ antenna.health }}
      </span>
    </div>

    <div class="body">

      <!-- Left Column -->
      <div class="left">

        <!-- SNR -->
        <div class="section">
          <h3>SNR</h3>
          <div class="chart">
            <slot name="snr-chart" :snr="antenna.snr_stats" />
          </div>
        </div>

        <!-- Multipath -->
        <div class="section">
          <h3>Multipath</h3>
          <div class="chart">
            <slot name="multipath-chart" :multipath="antenna.multipath" />
          </div>
        </div>

      </div>

      <!-- Right Column -->
      <div class="right">

        <!-- Sky Plot -->
        <div class="section">
          <h3>Sky Plot</h3>
          <div class="sky">
            <slot
              name="sky-plot"
              :satellites="antenna.satellites"
              @select="selectSatellite"
            />
          </div>
        </div>

        <!-- Environment -->
        <div class="section">
          <h3>Environment</h3>

          <div class="env-grid">
            <div><strong>Temp:</strong> {{ antenna.environment.temperature }} °C</div>
            <div><strong>Humidity:</strong> {{ antenna.environment.humidity }}%</div>
            <div><strong>Noise:</strong> {{ antenna.environment.noise }} dB</div>
            <div><strong>Interference:</strong> {{ antenna.environment.interference }}</div>
          </div>
        </div>

        <!-- Receiver -->
        <div class="section receiver">
          <h3>Receiver</h3>

          <div class="receiver-grid">
            <div><strong>Model:</strong> {{ antenna.receiver.model }}</div>
            <div><strong>Firmware:</strong> {{ antenna.receiver.firmware }}</div>
            <div><strong>Lock:</strong> {{ antenna.receiver.lock_status }}</div>
            <div><strong>Last Sync:</strong> {{ formatTS(antenna.receiver.last_sync) }}</div>
          </div>

          <button class="inspect-btn" @click="inspectReceiver">
            Inspect Receiver
          </button>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  antenna: { type: Object, required: true }
})

const emit = defineEmits(["select-satellite", "inspect-receiver"])

function selectSatellite(sat) {
  emit("select-satellite", sat)
}

function inspectReceiver() {
  emit("inspect-receiver", props.antenna.receiver)
}

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}
</script>

<style scoped>
.antenna-panel {
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

.body {
  display: flex;
  gap: 20px;
}

.left,
.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.chart,
.sky {
  background: #333;
  border-radius: 6px;
  padding: 8px;
  height: 180px;
}

.env-grid,
.receiver-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
  margin-top: 8px;
}

.inspect-btn {
  margin-top: 12px;
  background: #4caf50;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
}

.inspect-btn:hover {
  background: #43a047;
}
</style>
