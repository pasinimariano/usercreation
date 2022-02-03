from flask import request, make_response, jsonify
from .controller import new_user


def users_network(server):
    @server.route('/newuser', methods=['POST'])
    def create_user():
        body = request.get_json()
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

    @server.route('/login', methods=['GET'])
    def login():
        return 'HELLO WORLD'
