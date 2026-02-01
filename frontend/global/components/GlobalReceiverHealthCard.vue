<template>
  <div class="receiver-card" @click="inspect">

    <!-- Header -->
    <div class="header">
      <h3>{{ receiver.name }}</h3>
      <span class="health" :class="receiver.health">
        {{ receiver.health }}
      </span>
    </div>

    <!-- Metrics -->
    <div class="metrics">

      <div class="metric">
        <div class="label">Lock</div>
        <div class="value">{{ receiver.lock_status }}</div>
      </div>

      <div class="metric">
        <div class="label">Stability</div>
        <div class="value">{{ receiver.clock.stability }} ps</div>
      </div>

      <div class="metric">
        <div class="label">PPS</div>
        <div class="value">{{ receiver.clock.pps_quality }}</div>
      </div>

      <div class="metric">
        <div class="label">Temp</div>
        <div class="value">{{ receiver.environment.temperature }} °C</div>
      </div>

    </div>

    <!-- Sparkline Slot -->
    <div class="sparkline">
      <slot name="sparkline" :receiver="receiver" />
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  receiver: { type: Object, required: true }
})

const emit = defineEmits(["inspect"])

function inspect() {
  emit("inspect", props.receiver)
}
</script>

<style scoped>
.receiver-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  cursor: pointer;
}

.receiver-card:hover {
  background: #2a2a2a;
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

.sparkline {
  height: 40px;
  background: #2a2a2a;
  border-radius: 6px;
  padding: 4px;
}
</style>
