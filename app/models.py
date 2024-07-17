from datetime import datetime
from flask_pymongo import pymongo
from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = generate_password_hash(password_hash).decode("utf-8")
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
            "password_hash": self.password_hash,
            "email": self.email,
            "created_at": self.created_at,
        }

    def check_password(self, password_hash):
        return check_password_hash(self.password_hash, password_hash)
