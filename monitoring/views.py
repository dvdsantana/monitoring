from flask_jwt import jwt_required
from monitoring import app

@app.route('/')
@jwt_required()
def hello_world():
    return 'Hello, World!'