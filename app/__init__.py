from flask import Flask
from flask_pymongo import PyMongo
from app.config import config
from flask_cors import CORS
import os

mongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Start mongodb client
    mongo.init_app(app)

    # enable cors
    CORS(app, resources={r"/*": {"origins": "*"}})

    # JWT config
    app.config["SECRET_KEY"] = os.getenv("JWT_KEY")

    @app.route("/")
    def test():
        return "Hello World!"

    from app.routes import register_bp, login_bp

    app.register_blueprint(register_bp, url_prefix="/api")
    app.register_blueprint(login_bp, url_prefix="/api")

    return app
