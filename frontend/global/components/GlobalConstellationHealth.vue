<template>
  <div class="constellation-health">

    <!-- Header -->
    <div class="header">
      <h2>Constellation Health</h2>

      <select v-model="selected" class="selector">
        <option
          v-for="(v, name) in constellations"
          :key="name"
          :value="name"
        >
          {{ name }}
        </option>
      </select>
    </div>

    <div v-if="current" class="body">

      <!-- Summary -->
      <div class="summary">
        <h3>{{ selected }} Overview</h3>

        <div class="summary-grid">
          <div class="metric">
            <div class="label">Healthy</div>
            <div class="value">{{ current.summary.healthy }}</div>
          </div>

          <div class="metric">
            <div class="label">Unhealthy</div>
            <div class="value">{{ current.summary.unhealthy }}</div>
          </div>

          <div class="metric">
            <div class="label">Eclipsed</div>
            <div class="value">{{ current.summary.eclipsed }}</div>
          </div>

          <div class="metric">
            <div class="label">Active</div>
            <div class="value">{{ current.summary.active }}</div>
          </div>
        </div>

        <!-- Trend Indicator -->
        <div class="trend">
          <span class="trend-label">Trend:</span>
          <span :class="['trend-value', current.trend]">
            {{ current.trend }}
          </span>
        </div>
      </div>

      <!-- Mini‑Charts -->
      <div class="charts">
        <slot name="charts" />
      </div>

      <!-- Satellite Table -->
      <div class="satellites">
        <h3>Satellites</h3>

        <table class="sat-table">
          <thead>
            <tr>
              <th>PRN</th>
              <th>Health</th>
              <th>Phase</th>
              <th>Eclipse</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="s in current.satellites"
              :key="s.prn"
              @click="select(s)"
              class="sat-row"
            >
              <td>{{ s.prn }}</td>
              <td>
                <span class="health" :class="s.health">
                  {{ s.health }}
                </span>
              </td>
              <td>{{ s.phase }}</td>
              <td>{{ s.eclipse || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const props = defineProps({
  constellations: { type: Object, required: true }
})

const emit = defineEmits(["select"])

const selected = ref(Object.keys(props.constellations)[0] || null)

const current = computed(() => {
  if (!selected.value) return null
  return props.constellations[selected.value]
})

function select(sat) {
  emit("select", sat)
}
</script>

<style scoped>
.constellation-health {
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

.selector {
  background: #2a2a2a;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  color: #fff;
}

.summary {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 12px;
}

.metric .label {
  opacity: 0.7;
  font-size: 0.85rem;
}

.metric .value {
  font-size: 1.2rem;
  font-weight: bold;
}

.trend {
  margin-top: 12px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.trend-value.up { color: #4caf50 }
.trend-value.down { color: #f44336 }
.trend-value.steady { color: #ff9800 }

.charts {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.satellites {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.sat-table {
  width: 100%;
  border-collapse: collapse;
}

.sat-table th {
  text-align: left;
  opacity: 0.7;
  padding-bottom: 6px;
}

.sat-row {
  cursor: pointer;
}

.sat-row:hover {
  background: #333;
}

.sat-row td {
  padding: 6px 0;
}

.health {
  padding: 2px 6px;
  border-radius: 6px;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.health.healthy { background: #4caf50 }
.health.unhealthy { background: #f44336 }
.health.unknown { background: #777 }
</style>
