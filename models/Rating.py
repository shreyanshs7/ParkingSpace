from . import db

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    booking_space_id = db.Column(db.Integer, db.ForeignKey('booking_space.id'))
    by_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer, default=3)