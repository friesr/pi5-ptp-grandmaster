// Global API Client
// -----------------
// Strongly typed wrappers for all global intelligence endpoints.

export const GlobalAPI = {
  // Nodes
  nodes: {
    list: () => fetch("/api/global/nodes/list").then(r => r.json()),
    health: () => fetch("/api/global/nodes/health").then(r => r.json())
  },

  // Intel
  intel: {
    recent: () => fetch("/api/global/intel/recent").then(r => r.json()),
    snapshot: () => fetch("/api/global/intel/snapshot").then(r => r.json())
  },

  // Federation
  federation: {
    status: () => fetch("/api/global/federation/status").then(r => r.json()),
    topology: () => fetch("/api/global/federation/topology").then(r => r.json())
  },

  // Map
  map: {
    nodes: () => fetch("/api/global/map/nodes").then(r => r.json()),
    overlays: () => fetch("/api/global/map/overlays").then(r => r.json())
  },

  // Correlation
  correlation: {
    clusters: () => fetch("/api/global/correlation/clusters").then(r => r.json()),
    snapshot: () => fetch("/api/global/correlation/snapshot").then(r => r.json())
  },

  // Risk
  risk: {
    global: () => fetch("/api/global/risk/global").then(r => r.json()),
    forecast: () => fetch("/api/global/risk/forecast").then(r => r.json()),
    snapshot: () => fetch("/api/global/risk/snapshot").then(r => r.json())
  },

  // Control Room
  controlRoom: {
    snapshot: () => fetch("/api/global/control_room/snapshot").then(r => r.json()),
    alerts: () => fetch("/api/global/control_room/alerts").then(r => r.json())
  },

  // Replay
  replay: {
    timeline: (minutes = 120) =>
      fetch(`/api/global/replay/timeline?minutes=${minutes}`).then(r => r.json()),
    window: (start, end) =>
      fetch(`/api/global/replay/window?start=${start}&end=${end}`).then(r => r.json()),
    state: ts =>
      fetch(`/api/global/replay/state/${ts}`).then(r => r.json())
  },

  // Storyboards
  storyboards: {
    major: () => fetch("/api/global/storyboard/major").then(r => r.json()),
    incident: () => fetch("/api/global/storyboard/incident").then(r => r.json()),
    snapshot: () => fetch("/api/global/storyboard/snapshot").then(r => r.json())
  },

  // Archive
  archive: {
    list: () => fetch("/api/global/archive/list").then(r => r.json()),
    load: file => fetch(`/api/global/archive/load/${file}`).then(r => r.json()),
    search: keyword =>
      fetch(`/api/global/archive/search/${keyword}`).then(r => r.json())
  }
};
