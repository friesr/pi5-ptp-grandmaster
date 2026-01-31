from flask import Blueprint, jsonify
from backend.sim.scenario_loader import list_scenarios

scenario_list_api = Blueprint("scenario_list_api", __name__)

@scenario_list_api.route("/scenarios")
def scenarios():
    return jsonify(list_scenarios())
