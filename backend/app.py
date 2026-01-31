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
