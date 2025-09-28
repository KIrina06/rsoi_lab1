from flask import Flask
from .db import init_db
from .views import bp

def create_app():
    app = Flask(__name__)
    # конфиг из env vars
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = (
            # default for local dev (Postgres in docker-compose)
            # override via env var DATABASE_URL
            __import__('os').environ.get('DATABASE_URL', 'postgresql://program:test@postgres:5432/persons')
        ),
        JSONIFY_PRETTYPRINT_REGULAR=False
    )

    init_db(app)
    app.register_blueprint(bp, url_prefix='/api/v1')
    return app