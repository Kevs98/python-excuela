from flask import Flask
from pymongo import MongoClient
from app.config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config(config_name))

    # Start mongodb client
    client = MongoClient(app.config["MONGO_URI"])
    app.db = client.get_database("excuela")

    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
