from datetime import datetime, timedelta, timezone
from flask_pymongo import pymongo
from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
from flask import current_app


class User:
    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = datetime.utcnow()

    @staticmethod
    def from_dict(data):
        return User(
            username=data.get("username"),
            password_hash=data.get("password_hash"),
            email=data.get("email"),
        )

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": generate_password_hash(self.password_hash),
            "email": self.email,
            "created_at": self.created_at,
        }

    def check_password(self, password_hash):
        return check_password_hash(self.password_hash, password_hash.encode("utf-8"))

    def encode_auth_token(self, user_id):
        try:
            payload = {
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
                "iat": datetime.now(timezone.utc),
                "sub": user_id,
            }
            return jwt.encode(
                payload, current_app.config.get("JWT_KEY"), algorithm="HS256"
            )
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            algorithms = ["HS256"]
            payload = jwt.decode(
                auth_token, current_app.config.get("JWT_KEY"), algorithms=algorithms
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError as e:
            print(e)
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError as e:
            print(e)
            return "Invalid token. Please log in again."
