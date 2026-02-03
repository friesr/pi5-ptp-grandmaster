from flask import Flask
from flask_cors import CORS
from backend.api.system_api import system_api

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Only register the minimal system API
    app.register_blueprint(system_api)

    @app.route("/")
    def root():
        return {"status": "minimal-backend-online"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
  
