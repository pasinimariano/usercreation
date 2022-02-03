from .functions.emailRegex import valid_email
from .functions.encrypter import encrypt_password


class UserDB:
    def __init__(self, server, username, email, password):
        self.db = server.config['USER_COLLECTION']
        self.username = username
        self.email = email
        self.password = password

    def validate_username(self):
        response = 'Success'

        if len(self.username) < 3:
            response = 'The username must contain at least 3 characters'
            return response

        elif self.db.find_one({'username': self.username}) is None:
            return response

        else:
            response = "Username already exist"
            return response

    def validate_email(self):
        response = 'Success'

        if not self.email:
            response = 'Email is required'
            return response

        elif not valid_email(self.email):
            response = 'Invalid email'
            return response

        elif self.db.find_one({'email': self.email.lower()}) is None:
            return response

        else:
            response = 'Email already exist'
            return response

    def encrypt_password(self):
        return encrypt_password(self.password)

    def create_user(self, data):
        try:
            self.db.insert_one(data)

            return {'message': '{} successfully created'.format(self.username)}

        except Exception as e:
            return {'Error': e}

    def __str__(self):
        return ''
