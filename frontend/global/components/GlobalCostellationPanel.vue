<template>
  <div class="constellation-panel">

    <!-- Header -->
    <div class="header">
      <h2>Constellations</h2>

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
        <h3>{{ selected }} Summary</h3>

        <div class="summary-grid">
          <div><strong>Active:</strong> {{ current.summary.active }}</div>
          <div><strong>Healthy:</strong> {{ current.summary.healthy }}</div>
          <div><strong>Unhealthy:</strong> {{ current.summary.unhealthy }}</div>
          <div><strong>Eclipsed:</strong> {{ current.summary.eclipsed }}</div>
        </div>
      </div>

      <!-- Activity -->
      <div class="activity">
        <h3>Activity</h3>

        <div class="activity-grid">
          <div><strong>Signals:</strong> {{ current.activity.signals }}</div>
          <div><strong>Drops:</strong> {{ current.activity.drops }}</div>
          <div><strong>Phase shifts:</strong> {{ current.activity.phase_shifts }}</div>
        </div>
      </div>

      <!-- Satellites -->
      <div class="satellites">
        <h3>Satellites</h3>

        <ul class="sat-list">
          <li
            v-for="s in current.satellites"
            :key="s.prn"
            class="sat-row"
          >
            <div class="left">
              <div class="prn">{{ s.prn }}</div>
              <div class="health" :class="s.health">{{ s.health }}</div>
            </div>

            <div class="right">
              <div class="phase">
                Phase: <strong>{{ s.phase }}</strong>
              </div>
              <div class="eclipse" v-if="s.eclipse">
                Eclipse: <strong>{{ s.eclipse }}</strong>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Mini‑Charts Slot -->
      <div class="charts">
        <slot name="charts" />
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const props = defineProps({
  constellations: { type: Object, required: true }
})

const selected = ref(Object.keys(props.constellations)[0] || null)

const current = computed(() => {
  if (!selected.value) return null
  return props.constellations[selected.value]
})
</script>

<style scoped>
.constellation-panel {
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

.summary,
.activity,
.satellites {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}

.summary-grid,
.activity-grid {
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

.sat-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #333;
}

.sat-row:last-child {
  border-bottom: none;
}

.left {
  display: flex;
  gap: 12px;
  align-items: center;
}

.prn {
  font-weight: bold;
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

.right {
  text-align: right;
  opacity: 0.9;
}

.charts {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 8px;
}
</style>
