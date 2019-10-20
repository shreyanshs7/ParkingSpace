from . import db

class BookingOrder(db.Model):
    __tablename__ = 'booking_order'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.VARCHAR, default="TWO")
    booking_space_id = db.Column(db.Integer, db.ForeignKey('booking_space.id'))
    booked_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    from_time = db.Column(db.DateTime)
    to_time = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)