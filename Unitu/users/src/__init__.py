from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(script_info=None):
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)

    from src.api.users import blueprint
    app.register_blueprint(blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
