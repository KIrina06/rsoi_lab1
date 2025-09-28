import time
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app, retries=5, delay=2):
    db.init_app(app)
    for i in range(retries):
        try:
            with app.app_context():
                db.create_all()
            return
        except Exception as e:
            print("DB not ready, retrying in {}s...".format(delay))
            time.sleep(delay)
    raise RuntimeError("Cannot connect to database after multiple retries")