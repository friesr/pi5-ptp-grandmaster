from flask import Flask, render_template, Blueprint, jsonify
import os
import json

# Core + system APIs
from backend.api.status import status_api
from backend.api.validation import validation_api
from backend.api.storage import storage_api
from backend.api.config import config_api
from backend.api.export import export_api
from backend.api.service_control import service_control_api
from backend.api.backup import backup_api

# GNSS / timing analytics APIs
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
from backend.api.alert_rules import alert_rules_api
from backend.api.constellation_score import constellation_score_api
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

# Advanced GNSS analytics APIs
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
from backend.api.stability_predictor import stability_api
from backend.api.mission_control import mission_api
from backend.api.master_summary import master_api
from backend.api.report import report_api

# New advanced/bonus APIs
from backend.api.anomaly_ml import anomaly_ml_api
from backend.api.multi_receiver import multi_api
from backend.api.constellation_performance import constellation_perf_api

# Unified timeline builder
from backend.analysis.unified_timeline import build_unified_timeline

#Eclipse Prediction
from backend.api.eclipse import eclipse_api

from backend.api.clock_stability import clock_api
from backend.api.satellite_aging import satellite_aging_api
from backend.api.digital_twin import digital_twin_api
from backend.api.scenario_list import scenario_list_api
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









# -------------------------------------------------------------------
# Unified timeline API (inline definition)
# -------------------------------------------------------------------

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


# -------------------------------------------------------------------
# Flask app
# -------------------------------------------------------------------

app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)

# -------------------------------------------------------------------
# Register API blueprints
# -------------------------------------------------------------------

app.register_blueprint(status_api,              url_prefix="/api/status")
app.register_blueprint(validation_api,          url_prefix="/api/validation")
app.register_blueprint(storage_api,             url_prefix="/api/storage")
app.register_blueprint(config_api,              url_prefix="/api/config")
app.register_blueprint(export_api,              url_prefix="/api/export")
app.register_blueprint(service_control_api,     url_prefix="/api/services")
app.register_blueprint(backup_api,              url_prefix="/api/backup")

app.register_blueprint(allan_api,               url_prefix="/api/allan")
app.register_blueprint(drift_api,               url_prefix="/api/drift")
app.register_blueprint(history_api,             url_prefix="/api/history")
app.register_blueprint(temp_drift_api,          url_prefix="/api/temp_drift")
app.register_blueprint(ptp_servo_api,           url_prefix="/api/ptp_servo")
app.register_blueprint(alerts_api,              url_prefix="/api/alerts")
app.register_blueprint(multipath_api,           url_prefix="/api/multipath")
app.register_blueprint(gnss_history_api,        url_prefix="/api/gnss_history")
app.register_blueprint(dop_api,                 url_prefix="/api/dop")
app.register_blueprint(system_health_api,       url_prefix="/api/system_health")
app.register_blueprint(ptp_profile_api,         url_prefix="/api/ptp_profile")
app.register_blueprint(prn_lifetime_api,        url_prefix="/api/prn_lifetime")
app.register_blueprint(skyplot_playback_api,    url_prefix="/api/skyplot_playback")
app.register_blueprint(alert_rules_api,         url_prefix="/api/alert_rules")
app.register_blueprint(constellation_score_api, url_prefix="/api/constellation_score")
app.register_blueprint(servo_history_api,       url_prefix="/api/servo_history")
app.register_blueprint(gnss_outages_api,        url_prefix="/api/gnss_outages")
app.register_blueprint(multipath_heatmap_api,   url_prefix="/api/multipath_heatmap")
app.register_blueprint(constellation_timeline_api, url_prefix="/api/constellation_timeline")
app.register_blueprint(fade_events_api,         url_prefix="/api/fade_events")
app.register_blueprint(snr_waterfall_api,       url_prefix="/api/snr_waterfall")
app.register_blueprint(geometry_timeline_api,   url_prefix="/api/geometry_timeline")
app.register_blueprint(ptp_events_api,          url_prefix="/api/ptp_events")
app.register_blueprint(skyplot_density_api,     url_prefix="/api/skyplot_density")
app.register_blueprint(signal_quality_api,      url_prefix="/api/signal_quality")
app.register_blueprint(gnss_ptp_corr_api,       url_prefix="/api/gnss_ptp_corr")

app.register_blueprint(prn_health_api,          url_prefix="/api/prn_health")
app.register_blueprint(constellation_drift_api, url_prefix="/api/constellation_drift")
app.register_blueprint(interference_api,        url_prefix="/api/interference")
app.register_blueprint(timing_accuracy_api,     url_prefix="/api/timing_accuracy")
app.register_blueprint(anomaly_cluster_api,     url_prefix="/api/anomaly_clusters")
app.register_blueprint(receiver_health_api,     url_prefix="/api/receiver_health")
app.register_blueprint(environment_api,         url_prefix="/api/environment")
app.register_blueprint(timing_conf_api,         url_prefix="/api/timing_confidence")
app.register_blueprint(predictive_api,          url_prefix="/api/predictive")
app.register_blueprint(anomaly_explainer_api,   url_prefix="/api/anomaly_explainer")
app.register_blueprint(env_change_api,          url_prefix="/api/environment_change")
app.register_blueprint(sla_api,                 url_prefix="/api/sla")
app.register_blueprint(stability_api,           url_prefix="/api/stability")
app.register_blueprint(report_api,              url_prefix="/api/report")
app.register_blueprint(master_api,              url_prefix="/api/master")
app.register_blueprint(mission_api,             url_prefix="/api/mission")
app.register_blueprint(unified_api,             url_prefix="/api/unified_timeline")

# New advanced APIs
app.register_blueprint(anomaly_ml_api,          url_prefix="/api/anomaly_ml")
app.register_blueprint(multi_api,               url_prefix="/api/multi_receiver")
app.register_blueprint(constellation_perf_api,  url_prefix="/api/constellation_performance")
app.register_blueprint(eclipse_api, url_prefix="/api/eclipse")
app.register_blueprint(clock_api, url_prefix="/api/clock_stability")
app.register_blueprint(satellite_aging_api, url_prefix="/api/satellite_aging")
app.register_blueprint(digital_twin_api, url_prefix="/api/digital_twin")
app.register_blueprint(scenario_list_api, url_prefix="/api/gnss_history")
app.register_blueprint(scenario_save_api, url_prefix="/api/scenario")
app.register_blueprint(digital_twin_batch_api, url_prefix="/api/digital_twin_batch")
app.register_blueprint(digital_twin_report_api, url_prefix="/api/digital_twin_report")
app.register_blueprint(sensitivity_api, url_prefix="/api/sensitivity")
app.register_blueprint(digital_twin_optimize_api, url_prefix="/api/digital_twin_optimize")
app.register_blueprint(digital_twin_evolve_api, url_prefix="/api/digital_twin_evolve")
app.register_blueprint(digital_twin_mc_api, url_prefix="/api/digital_twin_monte_carlo")
app.register_blueprint(digital_twin_risk_api, url_prefix="/api/digital_twin_risk")
app.register_blueprint(scenario_library_api, url_prefix="/api/scenario_library")
app.register_blueprint(digital_twin_replay_api, url_prefix="/api/digital_twin_replay")










# -------------------------------------------------------------------
# Frontend routes
# -------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validation")
def validation():
    return render_template("validation.html")

@app.route("/config")
def config_page():
    return render_template("config.html")

@app.route("/satellites")
def satellites():
    return render_template("satellites.html")

@app.route("/gnss-history")
def gnss_history_page():
    return render_template("gnss_history.html")

@app.route("/system-health")
def system_health_page():
    return render_template("system_health.html")

@app.route("/ptp-profile")
def ptp_profile_page():
    return render_template("ptp_profile.html")

@app.route("/prn-lifetime")
def prn_lifetime_page():
    return render_template("prn_lifetime.html")

@app.route("/skyplot-playback")
def skyplot_playback_page():
    return render_template("skyplot_playback.html")

@app.route("/services")
def services_page():
    return render_template("services.html")

@app.route("/alert-rules")
def alert_rules_page():
    return render_template("alert_rules.html")

@app.route("/constellation-score")
def constellation_score_page():
    return render_template("constellation_score.html")

@app.route("/backup")
def backup_page():
    return render_template("backup.html")

@app.route("/servo-history")
def servo_history_page():
    return render_template("servo_history.html")

@app.route("/gnss-outages")
def gnss_outages_page():
    return render_template("gnss_outages.html")

@app.route("/multipath-heatmap")
def multipath_heatmap_page():
    return render_template("multipath_heatmap.html")

@app.route("/constellation-timeline")
def constellation_timeline_page():
    return render_template("constellation_timeline.html")

@app.route("/gnss-fade-events")
def gnss_fade_events_page():
    return render_template("gnss_fade_events.html")

@app.route("/snr-waterfall")
def snr_waterfall_page():
    return render_template("snr_waterfall.html")

@app.route("/geometry-timeline")
def geometry_timeline_page():
    return render_template("geometry_timeline.html")

@app.route("/ptp-events")
def ptp_events_page():
    return render_template("ptp_events.html")

@app.route("/skyplot-density")
def skyplot_density_page():
    return render_template("skyplot_density.html")

@app.route("/signal-quality")
def signal_quality_page():
    return render_template("signal_quality.html")

@app.route("/gnss-ptp-corr")
def gnss_ptp_corr_page():
    return render_template("gnss_ptp_corr.html")

@app.route("/prn-health")
def prn_health_page():
    return render_template("prn_health.html")

@app.route("/constellation-drift")
def constellation_drift_page():
    return render_template("constellation_drift.html")

@app.route("/interference")
def interference_page():
    return render_template("interference.html")

@app.route("/timing-accuracy")
def timing_accuracy_page():
    return render_template("timing_accuracy.html")

@app.route("/anomaly-clusters")
def anomaly_clusters_page():
    return render_template("anomaly_clusters.html")

@app.route("/receiver-health")
def receiver_health_page():
    return render_template("receiver_health.html")

@app.route("/environment")
def environment_page():
    return render_template("environment_fingerprint.html")

@app.route("/timing-confidence")
def timing_confidence_page():
    return render_template("timing_confidence.html")

@app.route("/anomaly-explanations")
def anomaly_explanations_page():
    return render_template("anomaly_explanations.html")

@app.route("/predictive-maintenance")
def predictive_maintenance_page():
    return render_template("predictive_maintenance.html")

@app.route("/environment-change")
def environment_change_page():
    return render_template("environment_change.html")

@app.route("/sla")
def sla_page():
    return render_template("sla.html")

@app.route("/unified-timeline")
def unified_timeline_page():
    return render_template("unified_timeline.html")

@app.route("/report")
def report_page():
    return render_template("report.html")

@app.route("/mission-control")
def mission_control_page():
    return render_template("mission_control.html")

@app.route("/stability")
def stability_page():
    return render_template("stability.html")

@app.route("/anomaly-ml")
def anomaly_ml_page():
    return render_template("anomaly_ml.html")

@app.route("/multi-receiver")
def multi_receiver_page():
    return render_template("multi_receiver.html")

@app.route("/constellation-performance")
def constellation_performance_page():
    return render_template("constellation_performance.html")

@app.route("/multipath-3d")
def multipath_3d_page():
    return render_template("multipath_3d.html")

@app.route("/antenna-siting")
def antenna_siting_page():
    return render_template("antenna_siting.html")

@app.route("/spoofing")
def spoofing_page():
    return render_template("spoofing.html")

@app.route("/prn-fingerprint")
def prn_fingerprint_page():
    return render_template("prn_fingerprint.html")

@app.route("/orbit-phase")
def orbit_phase_page():
    return render_template("orbit_phase.html")

@app.route("/eclipse")
def eclipse_page():
    return render_template("eclipse.html")

@app.route("/clock-stability")
def clock_stability_page():
    return render_template("clock_stability.html")

@app.route("/satellite-aging")
def satellite_aging_page():
    return render_template("satellite_aging.html")

@app.route("/constellation-forecast")
def constellation_forecast_page():
    return render_template("constellation_forecast.html")

@app.route("/outage-forecast")
def outage_forecast_page():
    return render_template("outage_forecast.html")

@app.route("/sla-forecast")
def sla_forecast_page():
    return render_template("sla_forecast.html")

@app.route("/sla-root-cause")
def sla_root_cause_page():
    return render_template("sla_root_cause.html")

@app.route("/resilience-advisor")
def resilience_advisor_page():
    return render_template("resilience_advisor.html")

@app.route("/timing-confidence-2")
def timing_confidence2_page():
    return render_template("timing_confidence2.html")

@app.route("/digital-twin")
def digital_twin_page():
    return render_template("digital_twin.html")

@app.route("/scenario-designer")
def scenario_designer_page():
    return render_template("scenario_designer.html")

@app.route("/digital-twin-batch")
def digital_twin_batch_page():
    return render_template("digital_twin_batch.html")

@app.route("/digital-twin-report")
def digital_twin_report_page():
    return render_template("digital_twin_report.html")
    
@app.route("/sensitivity")
def sensitivity_page():
    return render_template("sensitivity.html")

@app.route("/digital-twin-optimize")
def digital_twin_optimize_page():
    return render_template("digital_twin_optimize.html")

@app.route("/digital-twin-evolve")
def digital_twin_evolve_page():
    return render_template("digital_twin_evolve.html")

@app.route("/digital-twin-monte-carlo")
def digital_twin_monte_carlo_page():
    return render_template("digital_twin_monte_carlo.html")

@app.route("/digital-twin-risk-curves")
def digital_twin_risk_curves_page():
    return render_template("digital_twin_risk_curves.html")

@app.route("/scenario-library")
def scenario_library_page():
    return render_template("scenario_library.html")

@app.route("/digital-twin-replay")
def digital_twin_replay_page():
    return render_template("digital_twin_replay.html")

# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
