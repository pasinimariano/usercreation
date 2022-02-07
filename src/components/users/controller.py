from dotenv import dotenv_values
from .store import UserDB
from .functions.encryptor import check_encrypted_password
from .functions.create_token import create_token

ENV = dotenv_values('.env')


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
            return create_token(login, ENV)
        else:
            return 'Incorrect'


def update_user(server, data):
    keys = data.keys()
    if 'username' in keys and 'email' in keys and 'password' in keys and '_id' in keys:
        if 'new_password' in keys:
            user = UserDB(server, data['username'], data['email'], data['password'], data['_id'], data['new_password'])
        else:
            user = UserDB(server, data['username'], data['email'], data['password'], data['_id'])

        update = user.update_user()

        return update

    else:
        return 'Invalid'


def delete_user(server, data):
    user = UserDB(server, data['username'], data['email'], data['password'], data['_id'])

    return user.delete_user()
