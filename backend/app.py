from flask import Flask, render_template, Blueprint, jsonify
import os, json

# ------------------------------------------------------------
# Core API Imports
# ------------------------------------------------------------
from backend.api.status import status_api
from backend.api.validation import validation_api
from backend.api.storage import storage_api
from backend.api.config import config_api
from backend.api.export import export_api
from backend.api.allan import allan_api
from backend.api.drift import drift_api
from backend.api.history import history_api
from backend.api.temp_drift import temp_drift_api
from backend.api.ptp_servo import ptp_servo_api
from backend.api.alerts import alerts_api
from backend.api.multipath import multipath_api
from backend.api.gnss_history import gnss_history_api
from backend.api.dop import dop_api
from backend.api.system_health import system_health_api
from backend.api.ptp_profile import ptp_profile_api
from backend.api.prn_lifetime import prn_lifetime_api
from backend.api.skyplot_playback import skyplot_playback_api
from backend.api.service_control import service_control_api
from backend.api.alert_rules import alert_rules_api
from backend.api.constellation_score import constellation_score_api
from backend.api.backup import backup_api
from backend.api.servo_history import servo_history_api
from backend.api.gnss_outages import gnss_outages_api
from backend.api.multipath_heatmap import multipath_heatmap_api
from backend.api.constellation_timeline import constellation_timeline_api
from backend.api.fade_events import fade_events_api
from backend.api.snr_waterfall import snr_waterfall_api
from backend.api.geometry_timeline import geometry_timeline_api
from backend.api.ptp_events import ptp_events_api
from backend.api.skyplot_density import skyplot_density_api
from backend.api.signal_quality import signal_quality_api
from backend.api.gnss_ptp_correlation import gnss_ptp_corr_api
from backend.api.prn_health import prn_health_api
from backend.api.constellation_drift import constellation_drift_api
from backend.api.interference_detector import interference_api
from backend.api.timing_accuracy import timing_accuracy_api
from backend.api.anomaly_clustering import anomaly_cluster_api
from backend.api.receiver_health import receiver_health_api
from backend.api.environment_fingerprint import environment_api
from backend.api.timing_confidence import timing_conf_api
from backend.api.anomaly_explainer import anomaly_explainer_api
from backend.api.predictive_maintenance import predictive_api
from backend.api.environment_change import env_change_api
from backend.api.sla import sla_api
from backend.api.report import report_api
from backend.api.stability_predictor import stability_api
from backend.api.mission_control import mission_api
from backend.api.master_summary import master_api

# ------------------------------------------------------------
# Digital Twin / Simulation APIs (Steps 79–94)
# ------------------------------------------------------------
from backend.api.scenario_save import scenario_save_api
from backend.api.digital_twin_batch import digital_twin_batch_api
from backend.api.digital_twin_report import digital_twin_report_api
from backend.api.sensitivity import sensitivity_api
from backend.api.digital_twin_optimize import digital_twin_optimize_api
from backend.api.digital_twin_evolve import digital_twin_evolve_api
from backend.api.digital_twin_monte_carlo import digital_twin_mc_api
from backend.api.digital_twin_risk_curves import digital_twin_risk_api
from backend.api.scenario_library import scenario_library_api
from backend.api.digital_twin_replay import digital_twin_replay_api
from backend.api.digital_twin_multi_replay import digital_twin_multi_replay_api
from backend.api.digital_twin_diff import digital_twin_diff_api
from backend.api.digital_twin_events import digital_twin_events_api
from backend.api.digital_twin_event_timeline import digital_twin_event_timeline_api

# ------------------------------------------------------------
# Unified Timeline API
# ------------------------------------------------------------
from backend.analysis.unified_timeline import build_unified_timeline

unified_api = Blueprint("unified_api", __name__)

@unified_api.route("/load/<day>")
def load_unified(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else []

    gnss = load("gnss_events.json")
    ptp = load("ptp_events.json")
    inter = load("interference.json")
    sla = load("sla_violations.json")
    recv = load("receiver_events.json")
    env = load("environment_changes.json")

    timeline = build_unified_timeline(gnss, ptp, inter, sla, recv, env)
    return jsonify(timeline)

# ------------------------------------------------------------
# Flask App Setup
# ------------------------------------------------------------
app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)

# ------------------------------------------------------------
# Register Blueprints
# ------------------------------------------------------------
apis = [
    (status_api, "/api/status"),
    (validation_api, "/api/validation"),
    (storage_api, "/api/storage"),
    (config_api, "/api/config"),
    (export_api, "/api/export"),
    (allan_api, "/api/allan"),
    (drift_api, "/api/drift"),
    (history_api, "/api/history"),
    (temp_drift_api, "/api/temp_drift"),
    (ptp_servo_api, "/api/ptp_servo"),
    (alerts_api, "/api/alerts"),
    (multipath_api, "/api/multipath"),
    (gnss_history_api, "/api/gnss_history"),
    (dop_api, "/api/dop"),
    (system_health_api, "/api/system_health"),
    (ptp_profile_api, "/api/ptp_profile"),
    (prn_lifetime_api, "/api/prn_lifetime"),
    (skyplot_playback_api, "/api/skyplot_playback"),
    (service_control_api, "/api/services"),
    (alert_rules_api, "/api/alert_rules"),
    (constellation_score_api, "/api/constellation_score"),
    (backup_api, "/api/backup"),
    (servo_history_api, "/api/servo_history"),
    (gnss_outages_api, "/api/gnss_outages"),
    (multipath_heatmap_api, "/api/multipath_heatmap"),
    (constellation_timeline_api, "/api/constellation_timeline"),
    (fade_events_api, "/api/fade_events"),
    (snr_waterfall_api, "/api/snr_waterfall"),
    (geometry_timeline_api, "/api/geometry_timeline"),
    (ptp_events_api, "/api/ptp_events"),
    (skyplot_density_api, "/api/skyplot_density"),
    (signal_quality_api, "/api/signal_quality"),
    (gnss_ptp_corr_api, "/api/gnss_ptp_corr"),
    (prn_health_api, "/api/prn_health"),
    (constellation_drift_api, "/api/constellation_drift"),
    (interference_api, "/api/interference"),
    (timing_accuracy_api, "/api/timing_accuracy"),
    (anomaly_cluster_api, "/api/anomaly_clusters"),
    (receiver_health_api, "/api/receiver_health"),
    (environment_api, "/api/environment"),
    (timing_conf_api, "/api/timing_confidence"),
    (predictive_api, "/api/predictive"),
    (anomaly_explainer_api, "/api/anomaly_explainer"),
    (env_change_api, "/api/environment_change"),
    (sla_api, "/api/sla"),
    (unified_api, "/api/unified_timeline"),
    (stability_api, "/api/stability"),
    (report_api, "/api/report"),
    (master_api, "/api/master"),
    (mission_api, "/api/mission"),

    # Digital Twin APIs
    (scenario_save_api, "/api/scenario"),
    (digital_twin_batch_api, "/api/digital
