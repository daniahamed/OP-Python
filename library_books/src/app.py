from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    db.init_app(app)
    migrate.init_app(app, db)

    from src import models
    from src.routes.book import books_bp
    from src.routes.library import libraries_bp
    from src.routes.user import users_bp  

    app.register_blueprint(books_bp)
    app.register_blueprint(libraries_bp)
    app.register_blueprint(users_bp)

    return app


# schema validation
# folder structure should have a "routes" folder and a file for each endpoint, why?
# file for all functions used in endpoint -> easier to debug, clearer implementation, useful for unit testing
# in update and delete send id as <param>
# a constant file that has status codes
# env example ,,, 'SQLALCHEMY_DATABASE_URI' can be saved as an env var
# handle errors before they reach database
