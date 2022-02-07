def update_record(db, id_, username, email, password):
    try:
        db.update_one({'_id': id_}, {"$set": {
            'username': username,
            'email': email,
            'password': password
        }})
        return {'message': 'User updated correctly'}
    except Exception as e:
        return {'error': str(e)}