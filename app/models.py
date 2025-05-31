#This file contains the database models — the structure of your tables.This will create a User table in your SQLite database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth
    from .routes.career import career
    from .routes.resume import resume
    from .routes.study import study
    from .routes.doubt import doubt

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(career, url_prefix='/career')
    app.register_blueprint(resume, url_prefix='/resume')
    app.register_blueprint(study, url_prefix='/study')
    app.register_blueprint(doubt, url_prefix='/doubt')

    return app
