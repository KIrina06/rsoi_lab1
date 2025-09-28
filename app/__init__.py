from flask import Flask
from .db import init_db
from .views import bp
import os

def create_app():
    app = Flask(__name__)
    database_url = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSONIFY_PRETTYPRINT_REGULAR=False
    )

    init_db(app)
    app.register_blueprint(bp, url_prefix="/api/v1")

    app.url_map.strict_slashes = False

    return app