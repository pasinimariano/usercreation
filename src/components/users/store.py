import uuid
from .functions.emailRegex import valid_email
from .functions.encryptor import encryptor, check_encrypted_password
from .functions.find_user import find_user
from .functions.update_record import update_record


class UserDB:
    def __init__(self, server, username, email, password, id_=None, new_password=None):
        self.db = server.config['USER_COLLECTION']
        self.username = username
        self.email = email
        self.password = password
        self.id = id_
        self.new_password = new_password

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
        return encryptor(str(self.password))

    def create_user(self, password):
        try:
            id_ = uuid.uuid4()
            post_user = {
                '_id': id_.hex,
                'username': self.username.lower(),
                'email': self.email,
                'password': password
            }
            self.db.insert_one(post_user)

            return {'message': '{} successfully created'.format(self.username)}

        except Exception as e:
            return {'Error': e}

    def login_user(self):
        if self.username is None:
            return find_user(self.db, 'email', self.email)
        if self.email is None:
            return find_user(self.db, 'username', self.username)

    def update_user(self):
        user = self.db.find_one({'_id': self.id})

        if check_encrypted_password(self.password, str(user['password'])) and self.new_password is not None:
            return update_record(
                self.db,
                self.id,
                self.username,
                self.email,
                encryptor(str(self.new_password))
            )
        elif check_encrypted_password(self.password, str(user['password'])) and self.new_password is None:
            return update_record(
                self.db,
                self.id,
                self.username,
                self.email,
                encryptor(str(self.password))
            )
        else:
            return {'error': 'Password is incorrect'}

    def delete_user(self):
        user = self.db.find_one({'_id': self.id})

        if check_encrypted_password(self.password, str(user['password'])):
            try:
                self.db.delete_one(user)
                return {'message': '{} correctly delete'.format(self.username)}
            except Exception as e:
                return {'error': str(e)}
        else:
            return {'error': 'Password is invalid'}

    def __str__(self):
        return ''
