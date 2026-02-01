<template>
  <div class="snapshot-mini">

    <!-- Header -->
    <div class="header">
      <div class="title">Snapshot</div>
      <div class="timestamp">{{ formattedTimestamp }}</div>
    </div>

    <!-- Risk -->
    <div class="risk">
      <GlobalRiskGauge
        :risk="snapshot.risk.global_risk"
        :forecast="snapshot.risk.forecast.forecast"
      />
    </div>

    <!-- Clusters -->
    <div class="clusters">
      <div class="section-title">Clusters</div>
      <div v-if="snapshot.correlation.clusters.length === 0" class="empty">
        None
      </div>
      <ul v-else class="cluster-list">
        <li
          v-for="c in snapshot.correlation.clusters"
          :key="c.start"
          class="cluster-row"
          :class="c.severity"
        >
          <span class="cause">{{ c.root_cause }}</span>
          <span class="sev">{{ c.severity }}</span>
        </li>
      </ul>
    </div>

    <!-- Node Health Mini -->
    <div class="nodes">
      <div class="section-title">Nodes</div>
      <div class="node-grid">
        <div
          v-for="n in snapshot.nodes"
          :key="n.node_id"
          class="node-dot"
          :class="n.health.status"
          :title="n.node_id + ' — ' + n.health.status"
        ></div>
      </div>
    </div>

    <!-- Constellation Activity -->
    <div class="constellations">
      <div class="section-title">Constellations</div>
      <div class="const-grid">
        <span
          v-for="(v, k) in snapshot.intel.constellation_activity"
          :key="k"
          class="const-tag"
        >
          {{ k }}: {{ v }}
        </span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"
import GlobalRiskGauge from "./GlobalRiskGauge.vue"

const props = defineProps({
  snapshot: { type: Object, required: true }
})

const formattedTimestamp = computed(() => {
  if (!props.snapshot.timestamp) return ""
  return new Date(props.snapshot.timestamp * 1000).toLocaleString()
})
</script>

<style scoped>
.snapshot-mini {
  background: #1e1e1e;
  padding: 14px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 260px;
}

.header {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.timestamp {
  opacity: 0.7;
}

.section-title {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-bottom: 4px;
}

.risk {
  display: flex;
  justify-content: center;
}

.cluster-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.cluster-row {
  display: flex;
  justify-content: space-between;
  padding: 2px 0;
  font-size: 0.85rem;
}

.cluster-row.major { color: #f44336 }
.cluster-row.minor { color: #ff9800 }
.cluster-row.info { color: #4caf50 }

.node-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.node-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.node-dot.ok { background: #4caf50 }
.node-dot.warn { background: #ff9800 }
.node-dot.fail { background: #f44336 }

.const-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.const-tag {
  background: #333;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
}
</style>
