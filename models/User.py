from . import db

class User(db.Model):
    __tablename__ = 'app_user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.VARCHAR, nullable=False)
    full_name = db.Column(db.VARCHAR, nullable=False)
    number = db.Column(db.VARCHAR, nullable=False)