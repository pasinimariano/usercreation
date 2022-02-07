from flask import make_response, jsonify
from .controller import new_user, login_user, update_user, delete_user
from .functions.get_body import get_body
from .functions.acccess_token import access_token


def users_network(server):
    @server.route('/newuser', methods=['POST'])
    def create():
        body = get_body()
        if not body:
            return make_response(
                'No data received',
                403,
                {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
            )
        else:
            try:
                response = new_user(server, body['username'], body['email'], body['password'])

                if 'Errors' in response.keys():
                    return make_response(
                        jsonify(response),
                        403,
                        {'WWW-Authenticate': 'Basic realm ="Error occurred"'}
                    )

                return make_response(
                    jsonify(response),
                    200
                )
            except KeyError:
                return make_response(
                    'Some fields are incorrect or missing',
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )

    @server.route('/login', methods=['GET'])
    def login():
        body = get_body()
        if not body:
            return make_response(
                'No data received',
                403,
                {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
            )
        else:
            response = login_user(server, body)
            if response == 'No password':
                return make_response(
                    'No password recived',
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )
            elif response == 'Invalid':
                return make_response(
                    'No username or email recived',
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )
            elif response == 'Not found':
                return make_response(
                    'User not found',
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )
            elif response == 'Incorrect':
                return make_response(
                    'Password is incorrect',
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )
            elif 'token_error' in response:
                return make_response(
                    jsonify(response),
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not create a token"'}
                )
            else:
                return make_response(
                    jsonify(response),
                    200
                )

    @server.route('/update', methods=['POST'])
    @access_token
    def update():
        body = get_body()
        if not body:
            return make_response(
                'No data received',
                403,
                {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
            )
        else:
            response = update_user(server, body)
            if response == 'Invalid':
                return make_response(
                    'Invalid data, one or more fields are empty',
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )
            elif 'error' in response:
                return make_response(
                    jsonify(response),
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )
            else:
                return make_response(
                    jsonify(response),
                    200
                )

    @server.route('/delete', methods=['DELETE'])
    @access_token
    def delete():
        body = get_body()
        if not body:
            return make_response(
                'No data received',
                403,
                {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
            )
        else:
            response = delete_user(server, body)
            if 'error' in response:
                return make_response(
                    jsonify(response),
                    403,
                    {'WWW-Authenticate': 'Basic realm = "Could not verify"'}
                )
            else:
                return make_response(
                    jsonify(response),
                    200
                )
