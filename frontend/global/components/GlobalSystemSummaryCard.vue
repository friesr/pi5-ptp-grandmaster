<template>
  <div class="system-card" @click="inspect">

    <!-- Header -->
    <div class="header">
      <h3>System Health</h3>
      <span class="status" :class="system.overall">
        {{ system.overall }}
      </span>
    </div>

    <!-- Metrics -->
    <div class="metrics">

      <div class="metric">
        <div class="label">Constellations</div>
        <div class="value">{{ system.constellations_ok }}/{{ system.constellations_total }}</div>
      </div>

      <div class="metric">
        <div class="label">Receivers</div>
        <div class="value">{{ system.receivers_ok }}/{{ system.receivers_total }}</div>
      </div>

      <div class="metric">
        <div class="label">Antennas</div>
        <div class="value">{{ system.antennas_ok }}/{{ system.antennas_total }}</div>
      </div>

      <div class="metric">
        <div class="label">Environment</div>
        <div class="value">{{ system.environment_status }}</div>
      </div>

    </div>

    <!-- Trend -->
    <div class="trend">
      <span class="label">Trend:</span>
      <span class="value" :class="system.trend">
        {{ system.trend }}
      </span>
    </div>

    <!-- Sparkline Slot -->
    <div class="sparkline">
      <slot name="sparkline" :system="system" />
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  system: { type: Object, required: true }
})

const emit = defineEmits(["inspect"])

function inspect() {
  emit("inspect", props.system)
}
</script>

<style scoped>
.system-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  cursor: pointer;
}

.system-card:hover {
  background: #2a2a2a;
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
.status.degraded { background: #ff9800 }
.status.bad { background: #f44336 }

.metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.metric .label {
  opacity: 0.7;
  font-size: 0.8rem;
}

.metric .value {
  font-size: 1.1rem;
  font-weight: bold;
}

.trend {
  display: flex;
  gap: 8px;
  align-items: center;
}

.value.up { color: #4caf50 }
.value.down { color: #f44336 }
.value.steady { color: #ff9800 }

.sparkline {
  height: 40px;
  background: #2a2a2a;
  border-radius: 6px;
  padding: 4px;
}
</style>
