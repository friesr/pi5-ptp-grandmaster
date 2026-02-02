import os
import json
import time
from datetime import datetime

ARCHIVE_ROOT = "/opt/ptp-data/global_archive"

class GlobalArchiveEngine:
    """
    Stores and retrieves long-term global intelligence:
      - incidents
      - storyboards
      - replay snapshots
      - correlation clusters
      - risk snapshots
      - control room snapshots
    """

    def __init__(self):
        os.makedirs(ARCHIVE_ROOT, exist_ok=True)

    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------
    def _path(self, name):
        return os.path.join(ARCHIVE_ROOT, name)

    def _write_json(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def _read_json(self, path):
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return json.load(f)

    # ------------------------------------------------------------
    # Incident Archiving
    # ------------------------------------------------------------
    def archive_incident(self, incident):
        ts = int(time.time())
        path = self._path(f"incident_{ts}.json")
        self._write_json(path, incident)
        return {"saved": True, "file": path}

    def list_incidents(self):
        files = [f for f in os.listdir(ARCHIVE_ROOT) if f.startswith("incident_")]
        files.sort()
        return files

    def load_incident(self, filename):
        return self._read_json(self._path(filename))

    # ------------------------------------------------------------
    # Storyboard Archiving
    # ------------------------------------------------------------
    def archive_storyboard(self, storyboard):
        ts = int(time.time())
        path = self._path(f"storyboard_{ts}.json")
        self._write_json(path, storyboard)
        return {"saved": True, "file": path}

    def list_storyboards(self):
        files = [f for f in os.listdir(ARCHIVE_ROOT) if f.startswith("storyboard_")]
        files.sort()
        return files

    def load_storyboard(self, filename):
        return self._read_json(self._path(filename))

    # ------------------------------------------------------------
    # Replay Snapshot Archiving
    # ------------------------------------------------------------
    def archive_replay_snapshot(self, snapshot):
        ts = int(time.time())
        path = self._path(f"replay_{ts}.json")
        self._write_json(path, snapshot)
        return {"saved": True, "file": path}

    def list_replay_snapshots(self):
        files = [f for f in os.listdir(ARCHIVE_ROOT) if f.startswith("replay_")]
        files.sort()
        return files

    def load_replay_snapshot(self, filename):
        return self._read_json(self._path(filename))

    # ------------------------------------------------------------
    # Control Room Snapshot Archiving
    # ------------------------------------------------------------
    def archive_control_room(self, snapshot):
        ts = int(time.time())
        path = self._path(f"control_room_{ts}.json")
        self._write_json(path, snapshot)
        return {"saved": True, "file": path}

    def list_control_room(self):
        files = [f for f in os.listdir(ARCHIVE_ROOT) if f.startswith("control_room_")]
        files.sort()
        return files

    def load_control_room(self, filename):
        return self._read_json(self._path(filename))

    # ------------------------------------------------------------
    # Global Search
    # ------------------------------------------------------------
    def search(self, keyword):
        """
        Searches all archive files for a keyword.
        """
        results = []
        for f in os.listdir(ARCHIVE_ROOT):
            path = self._path(f)
            try:
                data = self._read_json(path)
                if data and keyword.lower() in json.dumps(data).lower():
                    results.append(f)
            except:
                pass
        return results

    # ------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------
    def snapshot(self):
        return {
            "incidents": self.list_incidents(),
            "storyboards": self.list_storyboards(),
            "replay_snapshots": self.list_replay_snapshots(),
            "control_room": self.list_control_room()
        }
