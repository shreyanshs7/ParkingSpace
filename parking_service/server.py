from flask import make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from parking_service import app

import libs

UPLOAD_FOLDER = 'files/'

logger = libs.get_logger(__name__)

#Admin
def initialise_admin(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    # Add administrative views here
    from models import db, BookingSpace
    admin.add_view(ModelView(BookingSpace, db.session))

def initialise_database(app):
    from models import db, config
    Migrate(app, db)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

CORS(app, resources=r'/*', supports_credentials=True)

# Setup DB
initialise_database(app)
initialise_admin(app)

#Booking space resource
from booking_space_module import booking_space_resource
app.register_blueprint(booking_space_resource, url_prefix='/booking_space')

#Users resource
from user_module import user_resource
app.register_blueprint(user_resource, url_prefix='/user')

#Booking Order Resource
from booking_order_module import booking_order_resource
app.register_blueprint(booking_order_resource, url_prefix='/booking_order')

@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/ready', methods = ['GET'])
def ready():
    return make_response(jsonify(message = 'Parking space is ready'), 200)
