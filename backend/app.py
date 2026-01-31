from flask import Flask, render_template
from backend.api.status import status_api
from backend.api.validation import validation_api
from backend.api.storage import storage_api
from backend.api.config import config_api
from backend.api.export import export_api

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
