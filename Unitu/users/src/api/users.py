from flask import Blueprint, jsonify, request
from src.api.models import User
from src import bcrypt, db
from src.api.utils import authenticate, tryExceptResponse

from sqlalchemy import exc, or_

blueprint = Blueprint('users_api', __name__)

@blueprint.route('/users/ping', methods=["GET"])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong! users'
    })

@blueprint.route('/users', methods=['GET'])
@tryExceptResponse
def get_all_users():
    response_object = {
        'status': 'success',
        'message': 'successfully fetch all users data',
        'data': {
            'users': [user.convert_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200

@blueprint.route('/users/login', methods=['POST'])
def login_user():
    post_data = request.get_json()
    response = {
        "status": "fail",
        "message": "Invalid Payload"
    }

    if not post_data:
        return jsonify(response), 400

    username_or_email = post_data.get("user_identification")

    if username_or_email is None:
        response["message"] = "Username or Email isn't found"
        return jsonify(response), 400

    password = post_data.get("password")

    if password is None:
        response["message"] = "Password isn't found"
        return jsonify(response), 400

    try:
        user_from_username = User.query.filter_by(username=username_or_email).first()
        user_from_email = User.query.filter_by(email=username_or_email).first()

        user = None

        if user_from_username is not None:
            user = user_from_username
        elif user_from_email is not None:
            user = user_from_email

        if user is None:
            response["message"] = "Username or Email with Password doesn't not matched"
            return jsonify(response), 404

        if bcrypt.check_password_hash(user.password, password):
            token = user.encode_auth_token()
            if token:
                response["status"] = "success"
                response["message"] = "Successfully Log in"
                response["token"] = token.decode()
                user.isActive = True
                db.session.commit()
                return jsonify(response), 200
        else:
            response["message"] = "Username or Email with Password doesn't not matched"
            return jsonify(response), 404
    except Exception as e:
        response["status"] = "fail"
        response["message"] = "Internal Error"

        if "token" in response:
            del response["token"]

        return jsonify(response), 500

@blueprint.route('/users/logout', methods=['POST'])
@authenticate
def logout_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.isActive = False
    db.session.commit()
    response = {
        "status": "success",
        "message": "Successfully Logout",
    }

    return jsonify(response), 200

@blueprint.route('/users/status', methods=['GET'])
@tryExceptResponse
@authenticate
def status_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    response = {
        "status": "success",
        "message": "Successfully fetch user data.",
        "data": user.convert_json()
    }

    return jsonify(response), 200

@blueprint.route('/users/add', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response = {
        "status": "fail",
        "message": "Invalid Payload"
    }

    if not post_data:
        return jsonify(response), 400

    firstName = post_data.get("firstName")
    lastName = post_data.get("lastName")
    email = post_data.get("email")
    username = post_data.get("username")
    password = post_data.get("password")

    all_input = [firstName, lastName, email, username, password]
    if any(inp is None for inp in all_input):
        response["message"] = "Not Enough Information to create account"
        return jsonify(response), 400

    try:
        user = User.query.filter(or_(User.username == username, User.email == email)).first()
        if not user:
            new_user = User(
                username=username,
                email=email,
                firstName=firstName,
                lastName=lastName,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            response["status"] = "success"
            response["message"] = "User successfully added"
            return jsonify(response), 201
        else:
            response["message"] = "Username or Email Already Exists."
            return jsonify(response), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response["message"] = "Internal Error" + str(e)
        return jsonify(response), 400
