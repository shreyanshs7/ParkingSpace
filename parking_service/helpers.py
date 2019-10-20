from flask import jsonify
from parking_service import app
from parking_service import serializers

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=status_code, payload = None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response, response.status_code

def assert_true(value, status_code=403, message='Forbidden'):
    if not value:
        raise InvalidUsage(message=message, status_code=status_code)

def assert_allowed(value, message='Forbidden'):
    assert_true(value, status_code=403, message=message)

def assert_found(instance, message='Not found'):
    if instance is None:
        raise InvalidUsage(message=message, status_code=404)

def assert_valid(value, message='Bad Request'):
    assert_true(value, status_code=400, message=message)

def respond(instance):
    return serializers.serialize(instance), 200