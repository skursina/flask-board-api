import os

from flask import Flask
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager

load_dotenv()


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():

    app = Flask(__name__)

    app.json.ensure_ascii = False
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)

    from app import models
    migrate.init_app(app, db)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()


    return app