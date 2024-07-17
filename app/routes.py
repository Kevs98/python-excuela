from flask import Blueprint, request, jsonify
from app.models import User

# main = Blueprint("main", __name__)
register_bp = Blueprint("/register_bp", __name__)


@register_bp.route("/register", methods=["POST"])
def register():
    from app import mongo

    print("Register endpoint called")
    data = request.json
    print("request data:", data)

    # Validate the inputs
    if (
        not data
        or "username" not in data
        or "password_hash" not in data
        or "email" not in data
    ):
        return jsonify({"message": "Missing username,  password or email"}), 400

    # check if user exists
    existing_user = mongo.db.user.find_one({"username": data["username"]})
    if existing_user:
        return jsonify({"message": "User already exist"}), 409

    # check if email exists
    existing_email = mongo.db.user.find_one({"email": data["email"]})
    if existing_email:
        return jsonify({"message": "Email already exists"}), 409

    try:
        # create a new user form data
        new_user = User.from_dict(data)

        # insert user on database
        mongo.db.user.insert_one(new_user.to_dict())

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print("error", e)
        return jsonify({"message": "Error registering user"}), 500


# from app.controllers import
