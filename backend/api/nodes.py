from flask import Blueprint, jsonify

nodes_bp = Blueprint("nodes", __name__)

@nodes_bp.route("/list", methods=["GET"])
def nodes_list():
    return jsonify({
        "nodes": [],
        "count": 0
    })
  
