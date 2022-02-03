import uuid
from .store import UserDB


def new_user(server, username, email, password):
    user = UserDB(server, username, email, password)
    validate_username = user.validate_username()
    validate_email = user.validate_email()

    if validate_username == 'Success' and validate_email == 'Success':
        id_ = uuid.uuid4()
        insert_user = {
            "_id": id_.hex,
            "username": username.lower(),
            "email": email,
            "password": user.encrypt_password()
        }
        return user.create_user(insert_user)
    else:
        bad_response = {'Errors': {
                'username': validate_username,
                'email': validate_email
            }
        }
        return bad_response
