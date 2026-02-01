<template>
  <div class="cluster-list">

    <ul class="clusters">
      <li
        v-for="(c, i) in clusters"
        :key="i"
        class="cluster-row"
        :class="c.severity"
        @click="select(c)"
      >
        <div class="header">
          <strong>{{ c.root_cause }}</strong>
          <span class="severity-tag">{{ c.severity }}</span>
        </div>

        <div class="meta">
          <span>{{ formatTS(c.start) }}</span>
          <span>→</span>
          <span>{{ formatTS(c.end) }}</span>
          <span>({{ c.duration_sec }} sec)</span>
        </div>

        <div class="nodes">
          <strong>Nodes:</strong>
          <span
            v-for="n in c.nodes_involved"
            :key="n"
            class="node-tag"
          >
            {{ n }}
          </span>
        </div>

        <div class="constellations">
          <strong>Constellations:</strong>
          <span
            v-for="k in c.constellations"
            :key="k"
            class="const-tag"
          >
            {{ k }}
          </span>
        </div>
      </li>
    </ul>

  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue"

const props = defineProps({
  clusters: { type: Array, default: () => [] }
})

const emit = defineEmits(["select"])

function formatTS(ts) {
  return new Date(ts * 1000).toLocaleString()
}

function select(c) {
  emit("select", c)
}
</script>

<style scoped>
.cluster-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.clusters {
  list-style: none;
  padding: 0;
  margin: 0;
}

.cluster-row {
  background: #2a2a2a;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
  cursor: pointer;
}

.cluster-row:hover {
  background: #333;
}

.cluster-row.major { border-left: 4px solid #f44336 }
.cluster-row.minor { border-left: 4px solid #ff9800 }
.cluster-row.info { border-left: 4px solid #4caf50 }

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.severity-tag {
  opacity: 0.8;
}

.meta {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-bottom: 6px;
  display: flex;
  gap: 6px;
}

.nodes,
.constellations {
  margin-bottom: 6px;
}

.node-tag,
.const-tag {
  background: #444;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 6px;
}
</style>
