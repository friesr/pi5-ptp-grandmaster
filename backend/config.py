from flask import Blueprint, request, jsonify
from backend.config.manager import load_config, save_config

config_api = Blueprint("config_api", __name__)

@config_api.route("/", methods=["GET"])
def get_config():
    return jsonify(load_config())

@config_api.route("/", methods=["POST"])
def update_config():
    cfg = load_config()
    cfg.update(request.json)
    save_config(cfg)
    return jsonify({"status": "ok"})
