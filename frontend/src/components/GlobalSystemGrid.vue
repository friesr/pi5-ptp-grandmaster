<template>
  <div class="grid-container">
    <h1 class="title">Global System Overview</h1>

    <div class="grid">
      <GlobalSystemSummaryCard title="Nodes" api="/api/global/nodes" />
      <GlobalSystemSummaryCard title="Intel" api="/api/global/intel" />
      <GlobalSystemSummaryCard title="Federation" api="/api/global/federation" />
      <GlobalSystemSummaryCard title="Correlation" api="/api/global/correlation" />
      <GlobalSystemSummaryCard title="Risk" api="/api/global/risk" />
      <GlobalSystemSummaryCard title="Replay" api="/api/global/replay" />
      <GlobalSystemSummaryCard title="Storyboards" api="/api/global/storyboard" />
      <GlobalSystemSummaryCard title="Archive" api="/api/global/archive" />
    </div>
  </div>
</template>

<script setup>
import GlobalSystemSummaryCard from "./GlobalSystemSummaryCard.vue"
</script>

<style scoped>
.grid-container {
  padding: 2rem;
}

.title {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  font-weight: 600;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}
</style>
