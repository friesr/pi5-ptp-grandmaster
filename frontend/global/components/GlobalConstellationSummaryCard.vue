<template>
  <div class="constellation-card" @click="select">

    <!-- Header -->
    <div class="header">
      <h3>{{ name }}</h3>
      <span class="trend" :class="trend">{{ trend }}</span>
    </div>

    <!-- Metrics -->
    <div class="metrics">
      <div class="metric">
        <div class="label">Healthy</div>
        <div class="value">{{ summary.healthy }}</div>
      </div>

      <div class="metric">
        <div class="label">Unhealthy</div>
        <div class="value">{{ summary.unhealthy }}</div>
      </div>

      <div class="metric">
        <div class="label">Eclipsed</div>
        <div class="value">{{ summary.eclipsed }}</div>
      </div>

      <div class="metric">
        <div class="label">Active</div>
        <div class="value">{{ summary.active }}</div>
      </div>
    </div>

    <!-- Activity -->
    <div class="activity">
      <div><strong>Signals:</strong> {{ activity.signals }}</div>
      <div><strong>Drops:</strong> {{ activity.drops }}</div>
      <div><strong>Phase shifts:</strong> {{ activity.phase_shifts }}</div>
    </div>

    <!-- Sparkline Slot -->
    <div class="sparkline">
      <slot name="sparkline" />
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  name: { type: String, required: true },
  summary: { type: Object, required: true },
  trend: { type: String, default: "steady" },
  activity: { type: Object, required: true }
})

const emit = defineEmits(["select"])

function select() {
  emit("select", props.name)
}
</script>

<style scoped>
.constellation-card {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  cursor: pointer;
}

.constellation-card:hover {
  background: #2a2a2a;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.trend {
  text-transform: capitalize;
  font-weight: bold;
}

.trend.up { color: #4caf50 }
.trend.down { color: #f44336 }
.trend.steady { color: #ff9800 }

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

.activity {
  font-size: 0.9rem;
  opacity: 0.9;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sparkline {
  height: 40px;
  background: #2a2a2a;
  border-radius: 6px;
  padding: 4px;
}
</style>
