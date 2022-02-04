def find_user(db, key, value):
    try:
        return db.find_one({key: value})
    except Exception as e:
        return {'Error': e}