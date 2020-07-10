import json
from datetime import datetime
from functools import wraps

from flask import abort, jsonify
from flask_jwt import jwt_required

from monitoring import app
from monitoring.customerRepository import CustomerRepository
from monitoring.historianRepository import HistorianRepository

date_format_request = '%Y-%m-%d-%H:%M:%S'
date_format_to_query = '%d %b %Y %H:%M:%S'

repository = HistorianRepository()

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

# Decorator to validate the input dates
def validate_date(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            request_date_from = datetime.strptime(kwargs['date_from'], date_format_request)
            request_date_to = datetime.strptime(kwargs['date_to'], date_format_request)

            kwargs['date_from'] = request_date_from.strftime(date_format_to_query).strip('0')
            kwargs['date_to'] = request_date_to.strftime(date_format_to_query).strip('0')
        except ValueError:
            json_abort(400, 'Invalid date')
        return f(*args, **kwargs)
    return wrap

@app.route('/', methods=['GET'])
@jwt_required()
def hello_world():
    return 'Hello, World!'

@app.route('/customers/<customer>/active_power/<date_from>/<date_to>', methods=['GET'])
@jwt_required()
@customer_exists
@validate_date
def active_power(customer, date_from, date_to):
    data = repository.get_active_power(date_from, date_to)

    return json.dumps(data)

@app.route('/customers/<customer>/energy_consumption', methods=['GET'])
@jwt_required()
@customer_exists
@validate_date
def energy_consumption(customer, date_from, date_to):
    data = repository.get_energy_consumption(date_from, date_to)

    return json.dumps(data)

@app.route('/customers/<customer>/current_month_status', methods=['GET'])
@jwt_required()
@customer_exists
def current_month_status():
    return 'current_month_status'
