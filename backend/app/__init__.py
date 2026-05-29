from flask import Flask
from app.config.config import Config
from app.database.mongodb import mongo
from app.extensions.cors import cors
from app.routes.auth_routes import auth_bp


def create_app():

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    cors.init_app(app)

    @app.route("/")
    def home():
        return {"message": "ATS Backend Running"}

    # Register blueprints
    app.register_blueprint(auth_bp)

    return app
