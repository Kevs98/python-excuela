from flask import Flask
from flask_pymongo import PyMongo
from app.config import config
from flask_cors import CORS

mongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Start mongodb client
    mongo.init_app(app)

    # enable cors
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/")
    def test():
        return "Hello World!"

    from app.routes import register_bp

    app.register_blueprint(register_bp, url_prefix="/api")

    return app
