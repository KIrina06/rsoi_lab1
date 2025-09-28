import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        retries = 5
        while retries > 0:
            try:
                db.create_all()
                break
            except OperationalError:
                retries -= 1
                print("DB not ready, retrying in 2s...")
                time.sleep(2)
        else:
            raise RuntimeError("Cannot connect to database after multiple retries")