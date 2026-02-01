import time
import random
from datetime import datetime, timedelta

class FederationEngine:
    """
    Maintains federation state across real + synthetic nodes.
    Tracks:
      - heartbeat
      - availability
      - topology
      - sync status
    """

    def __init__(self, nodes):
        # nodes: dict[node_id] = NodeModel
        self.nodes = nodes
        self.heartbeat_state = {}
        self.sync_state = {}
        self.topology_cache = None

        # initialize heartbeat + sync state
        now = time.time()
        for node_id in nodes:
            self.heartbeat_state[node_id] = {
                "last_heartbeat": now,
                "status": "online"
            }
            self.sync_state[node_id] = {
                "last_sync": now,
                "status": "ok"
            }

    # ------------------------------------------------------------
    # Heartbeat
    # ------------------------------------------------------------
    def heartbeat(self, node_id):
        now = time.time()
        self.heartbeat_state[node_id]["last_heartbeat"] = now

        # simulate occasional synthetic node dropouts
        if not self.nodes[node_id].is_real:
            if random.random() < 0.02:
                self.heartbeat_state[node_id]["status"] = "degraded"
            else:
                self.heartbeat_state[node_id]["status"] = "online"

        return {
            "node_id": node_id,
            "timestamp": now,
            "status": self.heartbeat_state[node_id]["status"]
        }

    def federation_status(self):
        now = time.time()
        status = []

        for node_id, hb in self.heartbeat_state.items():
            age = now - hb["last_heartbeat"]
            if age > 30:
                hb["status"] = "offline"
            elif age > 10:
                hb["status"] = "degraded"

            status.append({
                "node_id": node_id,
                "status": hb["status"],
                "last_heartbeat": hb["last_heartbeat"]
            })

        return status

    # ------------------------------------------------------------
    # Sync Logic
    # ------------------------------------------------------------
    def sync_node(self, node_id):
        now = time.time()

        # synthetic nodes occasionally lag
        if not self.nodes[node_id].is_real and random.random() < 0.05:
            self.sync_state[node_id]["status"] = "lagging"
        else:
            self.sync_state[node_id]["status"] = "ok"

        self.sync_state[node_id]["last_sync"] = now

        return {
            "node_id": node_id,
            "timestamp": now,
            "status": self.sync_state[node_id]["status"]
        }

    def sync_status(self):
        return [{
            "node_id": node_id,
            "status": state["status"],
            "last_sync": state["last_sync"]
        } for node_id, state in self.sync_state.items()]

    # ------------------------------------------------------------
    # Topology
    # ------------------------------------------------------------
    def topology(self):
        """
        Simple regional cluster topology:
            obs-real-01 is the hub
            synthetic nodes form a ring around it
        """
        if self.topology_cache:
            return self.topology_cache

        real_node = None
        synthetic_nodes = []

        for node_id, node in self.nodes.items():
            if node.is_real:
                real_node = node_id
            else:
                synthetic_nodes.append(node_id)

        topo = {
            "hub": real_node,
            "nodes": synthetic_nodes,
            "links": []
        }

        # hub links
        for s in synthetic_nodes:
            topo["links"].append({
                "from": real_node,
                "to": s,
                "latency_ms": random.uniform(3, 12)
            })

        # ring links
        for i in range(len(synthetic_nodes)):
            a = synthetic_nodes[i]
            b = synthetic_nodes[(i + 1) % len(synthetic_nodes)]
            topo["links"].append({
                "from": a,
                "to": b,
                "latency_ms": random.uniform(5, 20)
            })

        self.topology_cache = topo
        return topo

    # ------------------------------------------------------------
    # Global Federation Snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        return {
            "heartbeat": self.federation_status(),
            "sync": self.sync_status(),
            "topology": self.topology()
        }
