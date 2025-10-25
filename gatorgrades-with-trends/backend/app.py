import os
from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
from db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/gatorgrades"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    CORS(app)
    init_db(app)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    import os
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
