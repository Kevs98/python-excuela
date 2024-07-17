from flask import Blueprint, request, jsonify
from app.models import User

# main = Blueprint("main", __name__)
register_bp = Blueprint("/register_bp", __name__)
login_bp = Blueprint("/login_bp", __name__)


@register_bp.route("/register", methods=["POST"])
def register():
    from app import mongo

    data = request.json

    # Validate the inputs
    if (
        not data
        or "username" not in data
        or "password_hash" not in data
        or "email" not in data
    ):
        return jsonify({"message": "Missing username, password or email"}), 400

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


@login_bp.route("/login", methods=["POST"])
def login():
    from app import mongo

    data = request.json

    if not data or "username" not in data or "password_hash" not in data:
        return jsonify({"message": "Missing username or password"}), 400

    username = data.get("username")
    password_hash = data.get("password_hash")

    # Check user on database
    user_data = mongo.db.user.find_one({"username": username})
    if not user_data:
        return jsonify({"message": "Invalid Credentials"}), 401

    # Validate password_hash
    user = User(
        username=user_data["username"],
        password_hash=user_data["password_hash"],
        email=user_data["email"],
    )

    if not user.check_password(password_hash):
        return jsonify({"message": "Invalid Credentials"}), 401

    # Generate JWT token
    auth_token = user.encode_auth_token(str(user_data["_id"]))
    return jsonify({"token": auth_token}), 200
