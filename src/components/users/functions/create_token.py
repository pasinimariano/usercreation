import jwt
from datetime import datetime, timedelta


def create_token(user, env):
    try:
        claims = {
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "sub": user['username']
        }
        token = jwt.encode(claims, env['SECRET_KEY'], algorithm='HS256')

        return {
            'token': token,
            'user_info': {
                '_id': user['_id'],
                'username': user['username'],
                'email': user['email'],
            }
        }
    except Exception as error:
        return {'token_error': str(error)}
