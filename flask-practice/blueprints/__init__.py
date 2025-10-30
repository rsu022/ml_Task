from flask import Flask
from .routes import bp  # import Blueprint from routes.py

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)  # register the blueprint
    return app
