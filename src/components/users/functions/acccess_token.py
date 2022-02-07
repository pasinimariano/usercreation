import jwt
from functools import wraps
from flask import request, make_response
from dotenv import dotenv_values

ENV = dotenv_values('.env')


def access_token(func):
    @wraps(func)
    def token_required(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return make_response(
                'Token is missing',
                403,
                {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
            )
        try:
            jwt.decode(token, ENV['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return make_response(
                'Token expired, log in again',
                403,
                {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
            )
        except jwt.InvalidTokenError:
            return make_response(
                'Invalid token. Please log in again',
                403,
                {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
            )

        return func(*args, **kwargs)

    return token_required
