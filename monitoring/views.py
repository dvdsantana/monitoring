from functools import wraps

from flask import jsonify, abort
from flask_jwt import jwt_required

from monitoring import app
from monitoring.customerRepository import CustomerRepository

def json_abort(status_code, message):
    """ Utility function to send json errors message and raise http exception
    :param status_code: http error code
    :param message: friendly error message
    """
    data = {
        'error': {
            'code': status_code,
            'message': message
        }
    }
    response = jsonify(data)
    response.status_code = status_code
    abort(response)

# Decorator to validate the customer
def customer_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        repository = CustomerRepository()
        customer = kwargs['customer']
        if repository.exists(customer) is None:
            json_abort(404, 'Customer not exists')
        return f(*args, **kwargs)
    return wrap

@app.route('/', methods=['GET'])
@jwt_required()
def hello_world():
    return 'Hello, World!'

@app.route('/customers/<customer>/active_power', methods=['GET'])
@customer_exists
def active_power(customer):
    return json_abort(200, 'Customer exists')

@app.route('/customers/<customer>/energy_consumption', methods=['GET'])
def energy_consumption():
    return 'energy_consumption'

@app.route('/customers/<customer>/current_month_status', methods=['GET'])
def current_month_status():
    return 'current_month_status'
