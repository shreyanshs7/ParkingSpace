from . import db

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.VARCHAR, default="TWO")
    charge = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.VARCHAR, default="FREE")
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'))