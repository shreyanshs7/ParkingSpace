import dateutil
import dateutil.parser
from haversine import haversine
from models import BookingSpace, Location, Vehicle, db, BookingOrder
from sqlalchemy import or_

def calculate_range(given_location, booking_space_location, range):
    return True
        # if haversine(booking_space_location, given_location) <= range:
        #     return True
        # else:
        #     return False

def get_booking_spaces_in_range(location, vehicle_type, from_time, to_time, quantity):
    booking_spaces_list = []
    from_time = dateutil.parser.parse(from_time)
    to_time = dateutil.parser.parse(to_time)
    booking_spaces = BookingSpace.query.join(Vehicle).filter(Vehicle.type == vehicle_type, Vehicle.status == 'FREE', Vehicle.quantity >= quantity).all()
    for bs in booking_spaces:
        location_id = bs.location_id
        bs_location = Location.query.get(location_id)
        bs_location = (bs_location.latitude, bs_location.longitude)
        if calculate_range(location, bs_location, 5):
            booking_spaces_list.append(bs)
    return booking_spaces_list

def get_booking_spaces_by_vehicle(vehicle_type):
    booking_spaces = BookingSpace.query.join(Vehicle).filter(Vehicle.type == vehicle_type, Vehicle.status == "FREE").all()
    return booking_spaces

def get_booking_spaces_by_time(from_time, to_time):
    booking_spaces = BookingSpace.query.filter(BookingSpace.from_time <= from_time, BookingSpace.to_time >= to_time).all()
    return booking_spaces

def create_vehicle(quantity, price, type, user_id):
    vehicle = Vehicle(type=type, charge=price, quantity=quantity, user_id=user_id, status="FREE")
    db.session.add(vehicle)
    db.session.commit()
    db.session.refresh(vehicle)
    return vehicle

def create_location(latitude, longitude):
    location = Location(latitude=latitude, longitude=longitude)
    db.session.add(location)
    db.session.commit()
    db.session.refresh(location)
    return location

def create(name, location_id, from_time, to_time, image, user_id, vehicle_id):
    booking_space = BookingSpace(name=name, from_time=from_time, to_time=to_time, location_id=location_id, image=image, user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(booking_space)
    db.session.commit()
    db.session.refresh(booking_space)
    return booking_space

def get_booking_by_user_id(user_id):
    return BookingOrder.query.filter_by(booked_by=user_id).all()

def create_booking_order(booking_order):
    db.session.add(booking_order)
    db.session.commit()
    db.session.refresh(booking_order)
    return booking_order

def get_bookings_done_by_user_id(user_id):
    return BookingSpace.query.join(Vehicle).filter(Vehicle.status == 'BOOKED', BookingSpace.user_id == user_id).all()

def confirm_booking(booking_space_id):
    booking_space = BookingSpace.query.get(booking_space_id)
    vehicle = get_vehicle_by_id(booking_space.vehicle_id)
    vehicle.status = 'BOOKED'
    db.session.add(vehicle)
    db.session.commit()
    db.session.refresh(vehicle)
    return booking_space

def booking_requests(user_id):
    return BookingSpace.query.join(Vehicle).filter(Vehicle.status == 'REQUESTED', BookingSpace.user_id == user_id).all()

def get_location_by_id(location_id):
    return Location.query.get(location_id)

def get_vehicle_by_id(vehicle_id):
    return Vehicle.query.get(vehicle_id)

def cancel_booking(booking_space_id):
    booking_space = BookingSpace.query.get(booking_space_id)
    vehicle = get_vehicle_by_id(booking_space.vehicle_id)
    vehicle.status = 'FREE'
    db.session.add(vehicle)
    db.session.commit()
    db.session.refresh(vehicle)
    return booking_space