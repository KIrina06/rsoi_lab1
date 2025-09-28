from .db import db

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    address = db.Column(db.String)
    work = db.Column(db.String)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            age=self.age,
            address=self.address,
            work=self.work
        )