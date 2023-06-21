from flask import request, current_app
from functools import wraps

import jwt
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return "Not authorized", 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], "HS256")
        except jwt.exceptions.DecodeError:
            return "Not authorized", 401
        except jwt.exceptions.ExpiredSignatureError:
            return "Token expired", 401

        current_user = User.query.filter_by(
            id=data['id']
        ).all()
        if not current_user:
            return "Not authorized", 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated
