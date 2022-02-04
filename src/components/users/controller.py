import jwt
from datetime import datetime, timedelta
from .store import UserDB
from .functions.encryptor import check_encrypted_password


def new_user(server, username, email, password):
    user = UserDB(server, username, email, password)
    validate_username = user.validate_username()
    validate_email = user.validate_email()

    if validate_username == 'Success' and validate_email == 'Success':
        password = user.encrypt_password()
        return user.create_user(password)
    else:
        bad_response = {'Errors': {
                'username': validate_username,
                'email': validate_email
            }
        }
        return bad_response


def login_user(server, data):
    if 'password' not in data.keys():
        return 'No password'

    if 'username' in data.keys():
        data['email'] = None
    elif 'email' in data.keys():
        data['username'] = None
    else:
        return 'Invalid'

    user = UserDB(server, data['username'], data['email'], data['password'])
    login = user.login_user()

    if login is None:
        return 'Not found'
    else:
        if check_encrypted_password(data['password'], login['password']):
            try:
                claims = {
                    "exp": datetime.utcnow() + timedelta(minutes=30),
                    "iat": datetime.utcnow(),
                    "sub": login['username']
                }
                token = jwt.encode(claims, server.config['SECRET_KEY'], algorithm='HS256')

                return {'token': token}
            except Exception as error:
                return {'token_error': str(error)}
        else:
            return 'Incorrect'
