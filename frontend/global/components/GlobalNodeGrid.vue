<template>
  <div class="node-grid" :class="{ compact }">
    <component
      v-for="n in nodes"
      :key="n.node_id"
      :is="component"
      :node="n"
      @click="select(n)"
      class="node-item"
    />
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue"

const props = defineProps({
  nodes: { type: Array, default: () => [] },
  component: { type: [Object, String], required: true },
  compact: { type: Boolean, default: false }
})

const emit = defineEmits(["select"])

function select(n) {
  emit("select", n)
}
</script>

<style scoped>
.node-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.node-grid.compact {
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}

.node-item {
  cursor: pointer;
}
</style>
