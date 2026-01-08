from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()



def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    db.init_app(app)
    migrate.init_app(app, db)

    from src.models import Library, Book


    return app

