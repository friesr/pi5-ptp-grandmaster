from flask import Flask, render_template
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




app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)

# Register API blueprints
app.register_blueprint(status_api, url_prefix="/api/status")
app.register_blueprint(validation_api, url_prefix="/api/validation")
app.register_blueprint(storage_api, url_prefix="/api/storage")
app.register_blueprint(config_api, url_prefix="/api/config")
app.register_blueprint(export_api, url_prefix="/api/export")
app.register_blueprint(allan_api, url_prefix="/api/allan")
app.register_blueprint(drift_api, url_prefix="/api/drift")
app.register_blueprint(history_api, url_prefix="/api/history")
app.register_blueprint(temp_drift_api, url_prefix="/api/temp_drift")
app.register_blueprint(ptp_servo_api, url_prefix="/api/ptp_servo")
app.register_blueprint(alerts_api, url_prefix="/api/alerts")
app.register_blueprint(multipath_api, url_prefix="/api/multipath")
app.register_blueprint(gnss_history_api, url_prefix="/api/gnss_history")
app.register_blueprint(dop_api, url_prefix="/api/dop")
app.register_blueprint(system_health_api, url_prefix="/api/system_health")
app.register_blueprint(ptp_profile_api, url_prefix="/api/ptp_profile")
app.register_blueprint(prn_lifetime_api, url_prefix="/api/prn_lifetime")
app.register_blueprint(skyplot_playback_api, url_prefix="/api/skyplot_playback")
app.register_blueprint(service_control_api, url_prefix="/api/services")
app.register_blueprint(alert_rules_api, url_prefix="/api/alert_rules")
app.register_blueprint(constellation_score_api, url_prefix="/api/constellation_score")
app.register_blueprint(backup_api, url_prefix="/api/backup")
app.register_blueprint(servo_history_api, url_prefix="/api/servo_history")
app.register_blueprint(gnss_outages_api, url_prefix="/api/gnss_outages")




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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

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


