from flask import Flask # Import the Flask class
from flask_caching import Cache

app = Flask(__name__) # Create an instance of the class for our use
app.config['SECRET_KEY'] = 'super-secret'
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

cache = Cache(app)