"""
Point d'entrée de l'API Flask (package BACKEND du diagramme).

Lancement local :
    python app.py
ou
    flask --app app run --debug
"""

from flask import Flask, jsonify

from config import Config
from extensions import cors, init_mongo, jwt, ping_mongo
from routes.auth import auth_bp
from routes.offers import offers_bp
from routes.users import users_bp
from security import register_jwt_handlers


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    init_mongo(app)
    jwt.init_app(app)
    register_jwt_handlers(jwt)  # blocklist + réponses JSON 401/403/expiré/révoqué
    cors.init_app(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    # Blueprints («component» du package BACKEND)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(offers_bp)

    # --- Health checks ---------------------------------------------------
    @app.get("/")
    def health():
        """Ne dépend pas de Mongo : confirme juste que l'API tourne."""
        return jsonify({"status": "ok", "service": "ATS Intelligent - Backend"})

    @app.get("/health/db")
    def health_db():
        """Vérifie la connexion à MongoDB Atlas."""
        ok = ping_mongo()
        return jsonify({"mongo_connected": ok}), (200 if ok else 503)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
