from models import BookingOrder, db, Vehicle


def create_booking_order(booking_space, from_time, to_time, quantity, user_id, vehicle_type):
    booking_order = BookingOrder(booking_space_id=booking_space.id, booked_by=user_id, from_time=from_time, to_time=to_time, quantity=quantity, type=vehicle_type)
    db.session.add(booking_order)
    db.session.commit()
    db.session.refresh(booking_order)
    vehicle = Vehicle.query.get(booking_space.vehicle_id)
    vehicle.quantity = vehicle.quantity - quantity
    vehicle.status = 'REQUESTED'
    db.session.add(vehicle)
    db.session.commit()
    db.session.refresh(vehicle)