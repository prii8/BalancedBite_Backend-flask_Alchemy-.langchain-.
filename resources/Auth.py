import bcrypt
from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
import requests
from db import db
from models import UserModel, user



auth_bp = Blueprint("auth", __name__, description="Sign-up and Sign-in Operations")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
            data = request.get_json()
            existing_user = UserModel.query.filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"message": "Email already exists. Please use a different email."}), 400
            
            password_bytes = data["password"].encode("utf8")
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            pwP=hashed_password.decode('utf8')
            new_user = UserModel(
                password=pwP,
                username=data["username"],
                email=data["email"],
            )
            db.session.add(new_user)
            db.session.commit()
        
            return jsonify({"user":new_user.serialize()}), 201
    
    except Exception as e:
            h=str(e)
            return jsonify({"message": "An error occurred while processing the request.","error": h}), 500

@auth_bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    user = UserModel.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"message": "User not found. Please check your email."}), 404
    password_bytes = data["password"].encode("utf8")
    stored_password_bytes = user.password.encode("utf8")
   
    if bcrypt.checkpw(password_bytes, stored_password_bytes):
        return jsonify({"user": user.serialize()}), 200
    else:
        return jsonify({"message": "Invalid password. Please try again."}), 401