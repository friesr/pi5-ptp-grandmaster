from flask import Flask, render_template, Blueprint, jsonify, request, redirect
import os
import json



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
# Digital Twin / Simulation APIs
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
# Mobile Redirect
# ------------------------------------------------------------
@app.before_request
def mobile_redirect():
    ua = request.headers.get('User-Agent', '').lower()
    mobile_signatures = ["iphone", "android", "ipad", "mobile"]

    # Only redirect the root page, not API calls or subpages
    if request.path == "/":
        if any(sig in ua for sig in mobile_signatures):
            return redirect("/mobile")

PREF_FILE = "/opt/ptp-data/mobile_prefs.json"

def load_prefs():
    if os.path.exists(PREF_FILE):
        return json.load(open(PREF_FILE))
    return {"sparkline": "minimal"}

def save_prefs(prefs):
    json.dump(prefs, open(PREF_FILE, "w"))



# ------------------------------------------------------------
# Blueprint Manifest (Pattern A)
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
    (digital_twin_batch_api, "/api/digital_twin_batch"),
    (digital_twin_report_api, "/api/digital_twin_report"),
    (sensitivity_api, "/api/sensitivity"),
    (digital_twin_optimize_api, "/api/digital_twin_optimize"),
    (digital_twin_evolve_api, "/api/digital_twin_evolve"),
    (digital_twin_mc_api, "/api/digital_twin_mc"),
    (digital_twin_risk_api, "/api/digital_twin_risk"),
    (scenario_library_api, "/api/scenario_library"),
    (digital_twin_replay_api, "/api/digital_twin_replay"),
    (digital_twin_multi_replay_api, "/api/digital_twin_multi_replay"),
    (digital_twin_diff_api, "/api/digital_twin_diff"),
    (digital_twin_events_api, "/api/digital_twin_events"),
    (digital_twin_event_timeline_api, "/api/digital_twin_event_timeline"),
]

for bp, prefix in apis:
    app.register_blueprint(bp, url_prefix=prefix)

# ------------------------------------------------------------
# UI Routes
# ------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/alert-rules")
def alert_rules_page():
    return render_template("alert_rules.html")

@app.route("/allan")
def allan_page():
    return render_template("allan.html")

@app.route("/anomaly-clusters")
def anomaly_clusters_page():
    return render_template("anomaly_clusters.html")

@app.route("/anomaly-explanations")
def anomaly_explanations_page():
    return render_template("anomaly_explanations.html")

@app.route("/anomaly-ml")
def anomaly_ml_page():
    return render_template("anomaly_ml.html")

@app.route("/antenna-siting")
def antenna_siting_page():
    return render_template("antenna_siting.html")

@app.route("/backup")
def backup_page():
    return render_template("backup.html")

@app.route("/clock-stability")
def clock_stability_page():
    return render_template("clock_stability.html")

@app.route("/config")
def config_page():
    return render_template("config.html")

@app.route("/constellation-drift")
def constellation_drift_page():
    return render_template("constellation_drift.html")

@app.route("/constellation-forecast")
def constellation_forecast_page():
    return render_template("constellation_forecast.html")

@app.route("/constellation-performance")
def constellation_performance_page():
    return render_template("constellation_performance.html")

@app.route("/constellation-score")
def constellation_score_page():
    return render_template("constellation_score.html")

@app.route("/constellation-timeline")
def constellation_timeline_page():
    return render_template("constellation_timeline.html")

@app.route("/digital-twin")
def digital_twin_page():
    return render_template("digital_twin.html")

@app.route("/digital-twin-batch")
def digital_twin_batch_page():
    return render_template("digital_twin_batch.html")

@app.route("/digital-twin-diff")
def digital_twin_diff_page():
    return render_template("digital_twin_diff.html")

@app.route("/digital-twin-events")
def digital_twin_events_page():
    return render_template("digital_twin_events.html")

@app.route("/digital-twin-event-timeline")
def digital_twin_event_timeline_page():
    return render_template("digital_twin_event_timeline.html")

@app.route("/digital-twin-evolve")
def digital_twin_evolve_page():
    return render_template("digital_twin_evolve.html")

@app.route("/digital-twin-monte-carlo")
def digital_twin_monte_carlo_page():
    return render_template("digital_twin_monte_carlo.html")

@app.route("/digital-twin-multi-replay")
def digital_twin_multi_replay_page():
    return render_template("digital_twin_multi_replay.html")

@app.route("/digital-twin-optimize")
def digital_twin_optimize_page():
    return render_template("digital_twin_optimize.html")

@app.route("/digital-twin-replay")
def digital_twin_replay_page():
    return render_template("digital_twin_replay.html")

@app.route("/digital-twin-replay-sync")
def digital_twin_replay_sync_page():
    return render_template("digital_twin_replay_sync.html")

@app.route("/digital-twin-report")
def digital_twin_report_page():
    return render_template("digital_twin_report.html")

@app.route("/digital-twin-risk-curves")
def digital_twin_risk_curves_page():
    return render_template("digital_twin_risk_curves.html")

@app.route("/dop")
def dop_page():
    return render_template("dop.html")

@app.route("/drift")
def drift_page():
    return render_template("drift.html")

@app.route("/eclipse")
def eclipse_page():
    return render_template("eclipse.html")

@app.route("/environment")
def environment_page():
    return render_template("environment_fingerprint.html")

@app.route("/environment-change")
def environment_change_page():
    return render_template("environment_change.html")

@app.route("/geometry-timeline")
def geometry_timeline_page():
    return render_template("geometry_timeline.html")

@app.route("/gnss-fade-events")
def gnss_fade_events_page():
    return render_template("gnss_fade_events.html")

@app.route("/gnss-history")
def gnss_history_page():
    return render_template("gnss_history.html")

@app.route("/gnss-outages")
def gnss_outages_page():
    return render_template("gnss_outages.html")

@app.route("/gnss-ptp-corr")
def gnss_ptp_corr_page():
    return render_template("gnss_ptp_corr.html")

@app.route("/history")
def history_page():
    return render_template("history.html")

@app.route("/interference")
def interference_page():
    return render_template("interference.html")

@app.route("/mission-control")
def mission_control_page():
    return render_template("mission_control.html")

@app.route("/multi-receiver")
def multi_receiver_page():
    return render_template("multi_receiver.html")

@app.route("/multipath-3d")
def multipath_3d_page():
    return render_template("multipath_3d.html")

@app.route("/multipath-heatmap")
def multipath_heatmap_page():
    return render_template("multipath_heatmap.html")

@app.route("/orbit-phase")
def orbit_phase_page():
    return render_template("orbit_phase.html")

@app.route("/outage-forecast")
def outage_forecast_page():
    return render_template("outage_forecast.html")

@app.route("/predictive-maintenance")
def predictive_maintenance_page():
    return render_template("predictive_maintenance.html")

@app.route("/prn-fingerprint")
def prn_fingerprint_page():
    return render_template("prn_fingerprint.html")

@app.route("/prn-health")
def prn_health_page():
    return render_template("prn_health.html")

@app.route("/prn-lifetime")
def prn_lifetime_page():
    return render_template("prn_lifetime.html")

@app.route("/ptp-events")
def ptp_events_page():
    return render_template("ptp_events.html")

@app.route("/ptp-profile")
def ptp_profile_page():
    return render_template("ptp_profile.html")

@app.route("/receiver-health")
def receiver_health_page():
    return render_template("receiver_health.html")

@app.route("/replay-sync-bus")
def replay_sync_bus_page():
    return render_template("replay_sync_bus.html")

@app.route("/report")
def report_page():
    return render_template("report.html")

@app.route("/resilience-advisor")
def resilience_advisor_page():
    return render_template("resilience_advisor.html")

@app.route("/satellite-aging")
def satellite_aging_page():
    return render_template("satellite_aging.html")

@app.route("/satellites")
def satellites():
    return render_template("satellites.html")

@app.route("/scenario-designer")
def scenario_designer_page():
    return render_template("scenario_designer.html")

@app.route("/scenario-library")
def scenario_library_page():
    return render_template("scenario_library.html")

@app.route("/services")
def services_page():
    return render_template("services.html")

@app.route("/servo-history")
def servo_history_page():
    return render_template("servo_history.html")

@app.route("/signal-quality")
def signal_quality_page():
    return render_template("signal_quality.html")

@app.route("/skyplot-density")
def skyplot_density_page():
    return render_template("skyplot_density.html")

@app.route("/skyplot-playback")
def skyplot_playback_page():
    return render_template("skyplot_playback.html")

@app.route("/sla")
def sla_page():
    return render_template("sla.html")

@app.route("/sla-forecast")
def sla_forecast_page():
    return render_template("sla_forecast.html")

@app.route("/sla-root-cause")
def sla_root_cause_page():
    return render_template("sla_root_cause.html")

@app.route("/snr-waterfall")
def snr_waterfall_page():
    return render_template("snr_waterfall.html")

@app.route("/spoofing")
def spoofing_page():
    return render_template("spoofing.html")

@app.route("/stability")
def stability_page():
    return render_template("stability.html")

@app.route("/system-health")
def system_health_page():
    return render_template("system_health.html")

@app.route("/sensitivity")
def sensitivity_page():
    return render_template("sensitivity.html")

@app.route("/timing-accuracy")
def timing_accuracy_page():
    return render_template("timing_accuracy.html")

@app.route("/timing-confidence")
def timing_confidence_page():
    return render_template("timing_confidence.html")

@app.route("/timing-confidence2")
def timing_confidence2_page():
    return render_template("timing_confidence2.html")

@app.route("/unified-timeline")
def unified_timeline_page():
    return render_template("unified_timeline.html")

@app.route("/validation")
def validation_page():
    return render_template("validation.html")

@app.route("/mobile")
def mobile_page():
    return render_template("mobile.html")

@app.route("/api/mobile_prefs", methods=["GET", "POST"])
def mobile_prefs():
    if request.method == "GET":
        return jsonify(load_prefs())

    data = request.json
    prefs = load_prefs()
    prefs["sparkline"] = data.get("sparkline", prefs["sparkline"])
    save_prefs(prefs)
    return jsonify({"status": "ok"})

# ------------------------------------------------------------
# App Runner
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
