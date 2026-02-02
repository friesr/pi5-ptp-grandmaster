from flask import Blueprint, jsonify, request
from backend.analysis.global_archive_engine import GlobalArchiveEngine

# Injected by app.py
GLOBAL_ARCHIVE_ENGINE = None

global_archive_api = Blueprint("global_archive_api", __name__)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ensure_engine():
    global GLOBAL_ARCHIVE_ENGINE
    if GLOBAL_ARCHIVE_ENGINE is None:
        GLOBAL_ARCHIVE_ENGINE = GlobalArchiveEngine()
    return GLOBAL_ARCHIVE_ENGINE

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@global_archive_api.route("/list")
def list_all():
    engine = ensure_engine()
    return jsonify(engine.snapshot())

@global_archive_api.route("/load/<filename>")
def load_file(filename):
    engine = ensure_engine()

    if filename.startswith("incident_"):
        return jsonify(engine.load_incident(filename) or {"error": "not found"})

    if filename.startswith("storyboard_"):
        return jsonify(engine.load_storyboard(filename) or {"error": "not found"})

    if filename.startswith("replay_"):
        return jsonify(engine.load_replay_snapshot(filename) or {"error": "not found"})

    if filename.startswith("control_room_"):
        return jsonify(engine.load_control_room(filename) or {"error": "not found"})

    return jsonify({"error": "unknown file type"}), 400

@global_archive_api.route("/search/<keyword>")
def search(keyword):
    engine = ensure_engine()
    return jsonify({"results": engine.search(keyword)})

@global_archive_api.route("/snapshot")
def snapshot():
    engine = ensure_engine()
    return jsonify(engine.snapshot())

# ------------------------------------------------------------
# Save Endpoints
# ------------------------------------------------------------

@global_archive_api.route("/save/incident", methods=["POST"])
def save_incident():
    engine = ensure_engine()
    data = request.json
    return jsonify(engine.archive_incident(data))

@global_archive_api.route("/save/storyboard", methods=["POST"])
def save_storyboard():
    engine = ensure_engine()
    data = request.json
    return jsonify(engine.archive_storyboard(data))

@global_archive_api.route("/save/replay", methods=["POST"])
def save_replay():
    engine = ensure_engine()
    data = request.json
    return jsonify(engine.archive_replay_snapshot(data))

@global_archive_api.route("/save/control_room", methods=["POST"])
def save_control_room():
    engine = ensure_engine()
    data = request.json
    return jsonify(engine.archive_control_room(data))
