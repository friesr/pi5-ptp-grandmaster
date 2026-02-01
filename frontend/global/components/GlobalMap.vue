<template>
  <div class="global-map" ref="mapContainer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

const props = defineProps({
  nodes: { type: Array, default: () => [] },
  links: { type: Array, default: () => [] },
  overlays: { type: Object, default: () => ({ interference: [], constellations: [] }) }
})

const map = ref(null)
const mapContainer = ref(null)

let nodeLayer = null
let linkLayer = null
let interferenceLayer = null
let constellationLayer = null

function initMap() {
  map.value = L.map(mapContainer.value, {
    zoomControl: true,
    worldCopyJump: true
  }).setView([20, 0], 2)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 8,
    minZoom: 2
  }).addTo(map.value)

  nodeLayer = L.layerGroup().addTo(map.value)
  linkLayer = L.layerGroup().addTo(map.value)
  interferenceLayer = L.layerGroup().addTo(map.value)
  constellationLayer = L.layerGroup().addTo(map.value)
}

function renderNodes() {
  nodeLayer.clearLayers()

  props.nodes.forEach(n => {
    if (!n.position) return

    const marker = L.circleMarker([n.position.lat, n.position.lon], {
      radius: 6,
      color: n.health.status === "ok" ? "#4caf50" : "#f44336",
      fillOpacity: 0.9
    })

    marker.bindTooltip(`${n.node_id} — ${n.health.status}`)
    marker.addTo(nodeLayer)
  })
}

function renderLinks() {
  linkLayer.clearLayers()

  props.links.forEach(l => {
    const a = props.nodes.find(n => n.node_id === l.a)
    const b = props.nodes.find(n => n.node_id === l.b)
    if (!a || !b || !a.position || !b.position) return

    L.polyline(
      [
        [a.position.lat, a.position.lon],
        [b.position.lat, b.position.lon]
      ],
      { color: "#4fc3f7", weight: 2, opacity: 0.7 }
    ).addTo(linkLayer)
  })
}

function renderInterference() {
  interferenceLayer.clearLayers()

  props.overlays.interference.forEach(z => {
    L.circle([z.lat, z.lon], {
      radius: z.radius_m,
      color: "#f44336",
      fillColor: "#f44336",
      fillOpacity: 0.2
    })
      .bindTooltip(`${z.label} — intensity ${z.intensity}`)
      .addTo(interferenceLayer)
  })
}

function renderConstellations() {
  constellationLayer.clearLayers()

  props.overlays.constellations.forEach(c => {
    L.circleMarker([c.lat, c.lon], {
      radius: 4,
      color: "#ffeb3b",
      fillOpacity: 0.8
    })
      .bindTooltip(`${c.constellation} — ${c.event_type}`)
      .addTo(constellationLayer)
  })
}

function renderAll() {
  if (!map.value) return
  renderNodes()
  renderLinks()
  renderInterference()
  renderConstellations()
}

onMounted(() => {
  initMap()
  renderAll()
})

watch(() => props.nodes, renderNodes, { deep: true })
watch(() => props.links, renderLinks, { deep: true })
watch(() => props.overlays, renderAll, { deep: true })
</script>

<style scoped>
.global-map {
  width: 100%;
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
}
</style>
