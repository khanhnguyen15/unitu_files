from flask import request, jsonify
from src.api.models import User
from functools import wraps

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = {
            "status": "fail",
            "message": "Invalid Token"
        }

        header = request.headers.get('Authorization')
        if not header:
            return jsonify(response), 403

        auth_token = header.split(" ")

        if len(auth_token) < 2:
            response["message"] = "Authorization Token not Found"
            return jsonify(response), 403

        auth_token = auth_token[1]

        user_id_from_token = User.decode_auth_token(auth_token)
        if isinstance(user_id_from_token, str):
            response["message"] = user_id_from_token
            return jsonify(response), 401

        user = User.query.filter_by(id=user_id_from_token).first()
        if not user or not user.isActive:
            response["message"] = "Invalid User either not active or not exists"
            return jsonify(response), 401

        return func(user_id_from_token, *args, **kwargs)

    return wrapper

def tryExceptResponse(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        response = {
            "status": "fail",
            "message": "Internal Error"
        }

        try:
            return func(*args, **kwargs)
        except Exception as e:
            response["error_message"]  = str(e)
            return jsonify(response), 500

    return wrapper
