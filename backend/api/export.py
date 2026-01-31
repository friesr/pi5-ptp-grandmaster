from flask import Blueprint, jsonify

export_api = Blueprint("export_api", __name__)

@export_api.route("/excel", methods=["POST"])
def export_excel():
    # Placeholder — Excel export added later
    return jsonify({"status": "not_implemented"})
