<template>
  <span class="severity-tag" :class="severityClass">
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  severity: { type: String, required: true },
  uppercase: { type: Boolean, default: false }
})

const label = computed(() =>
  props.uppercase ? props.severity.toUpperCase() : props.severity
)

const severityClass = computed(() => {
  const s = props.severity.toLowerCase()
  if (s === "critical" || s === "major") return "critical"
  if (s === "warning" || s === "minor") return "warning"
  return "normal"
})
</script>

<style scoped>
.severity-tag {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #333;
  color: #fff;
  display: inline-block;
}

.severity-tag.normal {
  background: #4caf50;
}

.severity-tag.warning {
  background: #ff9800;
}

.severity-tag.critical {
  background: #f44336;
}
</style>
