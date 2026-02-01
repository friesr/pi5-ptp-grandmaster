<template>
  <div class="system-health">

    <!-- Header -->
    <div class="header">
      <h2>System Health</h2>

      <span class="overall" :class="overallStatus">
        {{ overallStatus }}
      </span>
    </div>

    <div class="body">

      <!-- Constellations -->
      <div class="section">
        <h3>Constellations</h3>

        <div class="grid">
          <GlobalConstellationSummaryCard
            v-for="c in system.constellations"
            :key="c.name"
            :name="c.name"
            :summary="c.summary"
            :trend="c.trend"
            :activity="c.activity"
            @select="selectConstellation"
          >
            <template #sparkline>
              <slot name="constellation-sparkline" :constellation="c" />
            </template>
          </GlobalConstellationSummaryCard>
        </div>
      </div>

      <!-- Receivers -->
      <div class="section">
        <h3>Receivers</h3>

        <div class="grid">
          <GlobalReceiverHealthCard
            v-for="r in system.receivers"
            :key="r.name"
            :receiver="r"
            @inspect="selectReceiver"
          >
            <template #sparkline>
              <slot name="receiver-sparkline" :receiver="r" />
            </template>
          </GlobalReceiverHealthCard>
        </div>
      </div>

      <!-- Antennas -->
      <div class="section">
        <h3>Antennas</h3>

        <div class="grid">
          <div
            v-for="a in system.antennas"
            :key="a.name"
            class="antenna-card"
            @click="selectAntenna(a)"
          >
            <div class="name">{{ a.name }}</div>
            <div class="health" :class="a.health">{{ a.health }}</div>
            <div class="metric"><strong>SNR:</strong> {{ a.snr }}</div>
            <div class="metric"><strong>Multipath:</strong> {{ a.multipath }}</div>
          </div>
        </div>
      </div>

      <!-- Environment -->
      <div class="section">
        <h3>Environment</h3>

        <div class="env-grid">
          <div><strong>Temp:</strong> {{ system.environment.temperature }} °C</div>
          <div><strong>Humidity:</strong> {{ system.environment.humidity }}%</div>
          <div><strong>Noise:</strong> {{ system.environment.noise }} dB</div>
          <div><strong>Interference:</strong> {{ system.environment.interference }}</div>
        </div>

        <div class="trend-row">
          <span class="label">Trend:</span>
          <span class="value" :class="system.environment.trend">
            {{ system.environment.trend }}
          </span>
        </div>
      </div>

      <!-- Interference -->
      <div class="section">
        <h3>Interference</h3>

        <div class="interference-row">
          <div><strong>Severity:</strong> {{ system.interference.severity }}</div>
          <div><strong>Bands:</strong> {{ system.interference.bands.length }}</div>
          <div><strong>Events:</strong> {{ system.interference.events }}</div>
        </div>

        <div class="trend-row">
          <span class="label">Trend:</span>
          <span class="value" :class="system.interference.trend">
            {{ system.interference.trend }}
          </span>
        </div>
      </div>

      <!-- Multipath -->
      <div class="section">
        <h3>Multipath</h3>

        <div class="multipath-row">
          <div><strong>Avg Delay:</strong> {{ system.multipath.avg_delay }} ns</div>
          <div><strong>Peak Delay:</strong> {{ system.multipath.peak_delay }} ns</div>
          <div><strong>Events:</strong> {{ system.multipath.events }}</div>
        </div>

        <div class="trend-row">
          <span class="label">Trend:</span>
          <span class="value" :class="system.multipath.trend">
            {{ system.multipath.trend }}
          </span>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"
import GlobalConstellationSummaryCard from "./GlobalConstellationSummaryCard.vue"
import GlobalReceiverHealthCard from "./GlobalReceiverHealthCard.vue"

const props = defineProps({
  system: { type: Object, required: true }
})

const emit = defineEmits([
  "select-constellation",
  "select-receiver",
  "select-antenna"
])

function selectConstellation(name) {
  emit("select-constellation", name)
}

function selectReceiver(receiver) {
  emit("select-receiver", receiver)
}

function selectAntenna(antenna) {
  emit("select-antenna", antenna)
}

const overallStatus = computed(() => {
  const s = props.system.overall
  return s || "unknown"
})
</script>

<style scoped>
.system-health {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overall {
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: capitalize;
  font-weight: bold;
}

.overall.good { background: #4caf50 }
.overall.degraded { background: #ff9800 }
.overall.bad { background: #f44336 }

.section {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 12px;
}

.antenna-card {
  background: #333;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
}

.antenna-card:hover {
  background: #444;
}

.health {
  text-transform: capitalize;
  font-weight: bold;
}

.health.good { color: #4caf50 }
.health.degraded { color: #ff9800 }
.health.bad { color: #f44336 }

.env-grid,
.interference-row,
.multipath-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.trend-row {
  margin-top: 10px;
}

.label {
  opacity: 0.7;
}

.value {
  font-weight: bold;
  text-transform: capitalize;
}

.value.up { color: #4caf50 }
.value.down { color: #f44336 }
.value.steady { color: #ff9800 }
</style>
