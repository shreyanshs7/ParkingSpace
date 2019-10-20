from flask import Blueprint, request, make_response, jsonify

from models import BookingSpace, BookingOrder
from booking_order_module import state_machine as booking_order_sa

booking_order_resource = Blueprint('booking_order_resource', __name__)

@booking_order_resource.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    booking_space_id = data['booking_space_id']
    booked_by = data['user_id']
    from_time = data['from_time']
    to_time = data['to_time']
    vehicle = data['vehicle']
    booking_space = BookingSpace.query.get(booking_space_id)
    if "two" in vehicle:
        quantity = vehicle['two']['quantity']
        two_booking_order = booking_order_sa.create_booking_order(booking_space, from_time, to_time, quantity, booked_by, "TWO")
    if "four" in vehicle:
        quantity = vehicle['four']['quantity']
        four_booking_order = booking_order_sa.create_booking_order(booking_space, from_time, to_time, quantity, booked_by, "FOUR")
    return make_response(jsonify(success=True), 200)

@booking_order_resource.route('/bookings', methods=['POST'])
def bookings():
    user_id = request.get_json()['user_id']
    booking_order = BookingOrder.query.filter_by(booked_by=user_id).all()
    booking_spaces_list = []
    for obj in booking_order:
        booking_spaces_list.append(BookingOrder.query.get(obj.id))
    return make_response(jsonify(data=booking_spaces_list), 200)