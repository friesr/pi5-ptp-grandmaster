from flask import Blueprint, request, jsonify
from backend.config.manager import load_config, save_config

alert_rules_api = Blueprint("alert_rules_api", __name__)

@alert_rules_api.route("/get")
def get_rules():
    cfg = load_config()
    return jsonify(cfg.get("alert_rules", {}))

@alert_rules_api.route("/update", methods=["POST"])
def update_rules():
    new_rules = request.json
    cfg = load_config()
    cfg["alert_rules"] = new_rules
    save_config(cfg)
    return jsonify({"status": "ok"})
