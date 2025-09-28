from flask import Flask
from .db import init_db
from .views import bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'DATABASE_URL',
            'postgresql://program:test@postgres:5432/persons'
        ),
        JSONIFY_PRETTYPRINT_REGULAR=False
    )

    init_db(app)
    app.register_blueprint(bp, url_prefix='/api/v1')

    # 🔑 вот эта строчка решает проблему со слэшами
    app.url_map.strict_slashes = False

    return app