from werkzeug.security import safe_str_cmp
from models.User import User
from flask_jwt import JWT
from monitoring import app
from os import environ

users = [
    User(1, 'user1', 'qwerty'),
    User(2, 'user2', 'asdfgh'),
]

usernames = {u.username: u for u in users}
userids = {u.id: u for u in users}

def authenticate(username, password):
    user = usernames.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userids.get(user_id, None)

jwt = JWT(app, authenticate, identity)