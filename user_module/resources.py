from flask import Blueprint, request
from models import User
from user_module import state_machine as user_sa
from parking_service import helpers

user_resource = Blueprint('user_resource', __name__)

@user_resource.route('/create', methods=['POST'])
def create():
    user = User(**request.get_json())
    user_sa.upsert(user)
    return helpers.respond(user)

