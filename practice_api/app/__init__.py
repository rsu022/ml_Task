from flask import Flask
from .database import db
from .blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"  # DB path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # optimization

    db.init_app(app)  # connect DB with Flask
    register_blueprints(app)  # register all controllers

    with app.app_context():
        db.create_all()  # create tables if they don't exist

    return app
