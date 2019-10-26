import json
from io import BytesIO

from flask import Blueprint, request, make_response, jsonify
from booking_space_module import state_machine as booking_space_sa
from models import BookingOrder
from parking_service import helpers, app

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

booking_space_resource = Blueprint('booking_space_resource', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@booking_space_resource.route('/', methods=['POST'])
def booking_spaces():
    data = request.get_json()
    from_time = data['from_time']
    to_time = data['to_time']
    latitude = data['latitude']
    longitude = data['longitude']
    if "two" in data:
        two_vehicle = "TWO"
        two_quantity = data['two']
    if "four" in data:
        four_vehicle = "FOUR"
        four_quantity = data['four']
    two_booking_spaces = booking_space_sa.get_booking_spaces_in_range((latitude, longitude), two_vehicle, from_time, to_time, two_quantity)
    four_booking_spaces = booking_space_sa.get_booking_spaces_in_range((latitude, longitude), four_vehicle, from_time,
                                                                      to_time, four_quantity)
    booking_spaces_list = []
    for obj in (two_booking_spaces + four_booking_spaces):
        obj.__dict__.pop('_sa_instance_state')
        if "image" in obj.__dict__:
            obj.__dict__['image'] = (BytesIO(obj.__dict__['image']).__str__())
        if "location_id" in obj.__dict__:
            location = booking_space_sa.get_location_by_id(obj.__dict__['location_id'])
            obj.__dict__['location'] = {
                'id': location.id,
                'latitude': location.latitude,
                'longitude': location.longitude
            }
            obj.__dict__.pop('location_id')
        if "vehicle_id" in obj.__dict__:
            vehicle = booking_space_sa.get_vehicle_by_id(obj.__dict__['vehicle_id'])
            vehicle.__dict__.pop('_sa_instance_state')
            obj.__dict__['vehicle'] = vehicle.__dict__
            obj.__dict__.pop('vehicle_id')
        booking_spaces_list.append(obj.__dict__)
    return make_response(jsonify(data=booking_spaces_list), 200)

@booking_space_resource.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    # print(data)
    # print(data['vehicle'])
    data = json.loads(request.form['data'])
    name = data['name']
    user_id = data['user_id']
    from_time = data['from_time']
    to_time = data['to_time']
    latitude = data['latitude']
    longitude = data['longitude']
    image = request.files['picture']
    image = image.read()
    vehicle = data['vehicle']
    # if image and allowed_file(image):
    #     filename = secure_filename(image.filename)
    #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    location = booking_space_sa.create_location(latitude, longitude)
    if "two" in vehicle:
        quantity = vehicle['two']['quantity']
        price = vehicle['two']['charge']
        two_vehicle = booking_space_sa.create_vehicle(quantity, price, 'TWO', user_id)
        booking_space = booking_space_sa.create(name, location.id, from_time, to_time, image, user_id, two_vehicle.id)
    if "four" in vehicle:
        quantity = vehicle['four']['quantity']
        price = vehicle['four']['charge']
        four_vehicle = booking_space_sa.create_vehicle(quantity, price, 'FOUR', user_id)
        booking_space = booking_space_sa.create(name, location.id, from_time, to_time, image, user_id, four_vehicle.id)
    return make_response(jsonify(success = True), 200)

@booking_space_resource.route('/history', methods=['GET'])
def history():
    data = request.get_json()
    user_id = data['user_id']
    data = booking_space_sa.get_booking_by_user_id(user_id)
    return helpers.respond(data)

@booking_space_resource.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    user_id = data['user_id']
    bs_id = data['booking_space_id']
    from_time = data['from_time']
    to_time = data['to_time']
    quantity = data['quantity']
    booking_type = data['booking_type']
    booking_order = BookingOrder(type=booking_type, booking_space_id=bs_id, quantity=quantity, from_time=from_time, to_time=to_time, booked_by=user_id)
    booking_order = booking_space_sa.create_booking_order(booking_order)
    return helpers.respond(booking_order)

@booking_space_resource.route('/done', methods=['POST'])
def bookings_done():
    user_id = request.get_json()['user_id']
    bookings_done = booking_space_sa.get_bookings_done_by_user_id(user_id)
    return helpers.respond(bookings_done)

@booking_space_resource.route('/request', methods=['POST'])
def booking_request():
    user_id = request.get_json()['user_id']
    booking_request = booking_space_sa.booking_requests(user_id)
    booking_spaces_list = []
    for obj in booking_request:
        obj.__dict__.pop('_sa_instance_state')
        if "image" in obj.__dict__:
            obj.__dict__['image'] = (BytesIO(obj.__dict__['image']).__str__())
        if "location_id" in obj.__dict__:
            location = booking_space_sa.get_location_by_id(obj.__dict__['location_id'])
            obj.__dict__['location'] = {
                'id': location.id,
                'latitude': location.latitude,
                'longitude': location.longitude
            }
            obj.__dict__.pop('location_id')
        if "vehicle_id" in obj.__dict__:
            vehicle = booking_space_sa.get_vehicle_by_id(obj.__dict__['vehicle_id'])
            vehicle.__dict__.pop('_sa_instance_state')
            obj.__dict__['vehicle'] = vehicle.__dict__
            obj.__dict__.pop('vehicle_id')
        booking_spaces_list.append(obj.__dict__)
    return make_response(jsonify(data=booking_spaces_list), 200)

@booking_space_resource.route('/cancel', methods=['POST'])
def cancel_booking():
    booking_space_id = request.get_json()['booking_space_id']
    booking_space = booking_space_sa.cancel_booking(booking_space_id)
    return make_response(jsonify(success=True), 200)

@booking_space_resource.route('/confirm', methods=['POST'])
def booking_confirm():
    data = request.get_json()
    booking_space_id = data['booking_space_id']
    booking_space = booking_space_sa.confirm_booking(booking_space_id)
    return make_response(jsonify(success=True), 200)