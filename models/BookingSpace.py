from . import db

class BookingSpace(db.Model):
    __tablename__ = 'booking_space'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    from_time = db.Column(db.DateTime)
    to_time = db.Column(db.DateTime)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    additional_information = db.Column(db.String, nullable=True)
    status = db.Column(db.VARCHAR, default="AVAILABLE")
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))